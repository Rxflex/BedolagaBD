# -*- coding: utf-8 -*-
"""Скан на утечки: секреты, ключи, персональные данные.

Запуск:
    python _tools/pii_scan.py            # отчёт
    python _tools/pii_scan.py --samples  # с примерами строк
    python _tools/pii_scan.py --all      # показать и «шумные» категории

Код возврата 1, если нашлось что-то из критичных категорий (ключи, токены,
телефоны, номера карт, приватные ключи Reality). Остальное — справочно:
в базе полно технических строк, похожих на секреты (хеши коммитов, якоря,
подсети, DNS-адреса), и они там по делу.
"""
import os
import re
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT
from sanitize import NOT_PEOPLE

SKIP_DIRS = {'.git', '_extraction', '.continuum', '__pycache__'}

PLACEHOLDER = re.compile(
    r'^(?:|x+|X+|\.{3}|…|<.*>|\{.*\}|your[-_].*|YOUR[-_].*|change[-_]?me|changeme|'
    r'сам_генерируй|САМ_ГЕНЕРИРУЙ|токен|token|секрет|secret|password|пароль|'
    r'ваш.*|ВАШ.*|твой.*|тут.*|здесь.*|свой|СВОЙ|ДОМЕН|домен|example.*|EXAMPLE.*|'
    r'super-secret.*|app_password.*|secure_password.*|base64_encoded.*|многасимволов|'
    r'MyVeryStrong.*|Your_.*|API_TOKEN_FROM.*|пупупу|[0-9]{5,10}:AA[A-Za-z0-9_-]{0,20}\.\.\..*|'
    r'[0-9]{5,10}:[a-z]{10,25}|xxx.*|XXX.*|nnn.*|abc.*|123.*|aaa.*|[*]+|-+|_+|\?+|'
    r'YWRtaW46cGFzc3dvcmQ=)$')

# (имя, регексп, критично?)
CHECKS = [
    ('telegram_bot_token', re.compile(r'\b\d{8,10}:[A-Za-z0-9_-]{35}\b'), True),
    ('jwt', re.compile(r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{5,}'), True),
    ('aws_key', re.compile(r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b'), True),
    ('ssh_key', re.compile(r'\bssh-(?:rsa|ed25519) AAAA[0-9A-Za-z+/=]{20,}'), True),
    ('private_key_body', re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----\s*\n?[A-Za-z0-9+/=]{40,}'), True),
    ('phone', re.compile(r'(?<![\d.])(?:\+7|8)[\s(-]?\d{3}[\s)-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?![\d.])'), True),
    ('card_number', re.compile(r'\b(?:\d{4}[ -]){3}\d{4}\b'), True),
    ('xray_private_key', re.compile(r'"privateKey"\s*:\s*"([A-Za-z0-9_-]{40,})"'), True),
    ('assigned_secret', re.compile(
        r'\b([A-Z][A-Z0-9_]*(?:PASSWORD|SECRET|TOKEN|API_KEY|PRIVATE_KEY|CLIENT_SECRET))\s*[=:]\s*'
        r'["\']?([A-Za-z0-9+/=_-]{16,})'), True),
    ('full_name', re.compile(r'\[id=[^\]|]+\|([A-ZА-ЯЁ][a-zа-яё]{2,}\s+[A-ZА-ЯЁ][a-zа-яё]{2,})\|'), True),
    ('email', re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'), False),
    ('private_key_mention', re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'), False),
    ('hex_32_64', re.compile(r'\b[0-9a-fA-F]{32,64}\b'), False),
    ('ipv4', re.compile(r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d./])'), False),
    ('telegram_private_link', re.compile(r'https://t\.me/c/\d+'), False),
]

PRIVATE_IP = re.compile(r'^(?:10\.|127\.|0\.|169\.254\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.|255\.)')
# публичные сервисы и заведомо технические адреса — не утечка
KNOWN_IP = {'1.1.1.1', '1.0.0.1', '8.8.8.8', '8.8.4.4', '9.9.9.9', '2.2.2.2',
            '77.88.8.8', '77.88.8.1', '94.140.14.14', '94.140.14.15',
            '94.140.14.140', '94.140.14.141', '208.67.222.222'}
# «мягкие» адреса почты: публичные контакты и очевидные примеры
MAIL_OK = re.compile(r'(?i)(?:@(?:your|example|test|domain|yourdomain|mail|gmail|yandex)'
                     r'|abuse@|noreply@|info@|admin@|support@|@rkn\.gov\.ru)')


def luhn(num):
    digits = [int(c) for c in re.sub(r'\D', '', num)][::-1]
    total = 0
    for i, d in enumerate(digits):
        if i % 2:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0 and len(digits) == 16


def files():
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(('.md', '.py', '.tsv', '.json', '.yml', '.yaml', '.txt')):
                yield os.path.relpath(os.path.join(base, n), ROOT).replace('\\', '/')


def main():
    show = '--samples' in sys.argv
    show_all = '--all' in sys.argv
    hits = collections.defaultdict(list)
    for rel in sorted(files()):
        try:
            text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        except UnicodeDecodeError:
            continue
        is_tool = rel.startswith('_tools/')
        for lineno, line in enumerate(text.split('\n'), 1):
            for name, rx, critical in CHECKS:
                for m in rx.finditer(line):
                    val = m.group(m.lastindex) if m.lastindex else m.group(0)
                    val = str(val).strip(' -' + chr(34) + chr(39))
                    if name == 'full_name' and NOT_PEOPLE.search(val):
                        continue
                    if PLACEHOLDER.match(val):
                        continue
                    if name == 'card_number' and not luhn(val):
                        continue
                    if name == 'ipv4' and (PRIVATE_IP.match(val) or val in KNOWN_IP):
                        continue
                    if name == 'email' and MAIL_OK.search(m.group(0)):
                        continue
                    if is_tool and name in ('assigned_secret', 'xray_private_key', 'hex_32_64',
                                            'full_name', 'phone', 'card_number'):
                        # в _tools лежат сами регекспы и список заглушек
                        continue
                    hits[name].append((rel, lineno, val, line.strip()[:150]))

    critical = {n for n, _, c in CHECKS if c}
    bad = {n: v for n, v in hits.items() if n in critical}
    soft = {n: v for n, v in hits.items() if n not in critical}

    print('КРИТИЧНОЕ')
    if not bad:
        print('  чисто')
    for name, _, _ in CHECKS:
        lst = bad.get(name)
        if not lst:
            continue
        print('  %-22s %4d в %d файлах' % (name, len(lst), len({h[0] for h in lst})))
        for rel, ln, val, ctx in lst[:5 if not show else 20]:
            print('      %s:%d  %s' % (rel, ln, ctx))

    if show_all or show:
        print('\nСПРАВОЧНО (обычно технические строки, не утечки)')
        for name, _, _ in CHECKS:
            lst = soft.get(name)
            if not lst:
                continue
            print('  %-22s %5d в %d файлах' % (name, len(lst), len({h[0] for h in lst})))
            if show_all:
                seen = set()
                for rel, ln, val, ctx in lst:
                    if val in seen:
                        continue
                    seen.add(val)
                    if len(seen) > 6:
                        print('        …')
                        break
                    print('        %s:%d  %s' % (rel, ln, ctx))

    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
