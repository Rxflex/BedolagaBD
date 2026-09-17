# -*- coding: utf-8 -*-
"""Подготовка к публикации: обезличивание имён и вычистка секретов.

Что делает:
  1. «Имя Фамилия» → «Имя Ф.» везде, где встречается (в пруфах и в тексте).
     Набор имён берётся из поля автора в пруфах `[id=N|автор|дата]`, ники
     из одного слова и явно не-людские названия не трогаются.
  2. Заменяет реальные секреты, попавшие в базу из чужих конфигов,
     на понятные заглушки (список REDACTIONS — правится руками).
  3. Маскирует телефоны и отдельные «спалённые» адреса чужих панелей.

Запуск: python _tools/sanitize.py [--dry]
Идемпотентно: повторный прогон ничего не меняет.
"""
import os
import re
import sys
import glob
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT

PROOF_BODY = re.compile(r'\[id=([^\]]+)\]')
NAME_WORD = r"[A-ZА-ЯЁ][a-zа-яё'’-]{1,}"
FULLNAME = re.compile(r'^(%s)\s+(%s)$' % (NAME_WORD, NAME_WORD))

# не имена людей: бренды, сервисы, служебные подписи Telegram
NOT_PEOPLE = re.compile(
    r'(?i)\b(bedolaga|vpn|bot|cash|team|shop|support|admin|cloud|host|pay|'
    r'deleted account|channel|news|service|store|market|dev|group|chat)\b')

# точные замены секретов: что → на что
REDACTIONS = [
    # 32-hex секрет вебхука из чужого .env
    ('c39c685e4dd315981c9bb738012afd0a', '<32-hex, openssl rand -hex 16>'),
    # приватные ключи Reality (x25519), попавшие в цитаты конфигов
    ('50JrHAPzS1vj1BC3b3P2jHFOGhKFS2-Kayz8K8P2Kaw', '<приватный ключ Reality>'),
    ('PJiLkkaJOvlaQ9yeyGJ6pl7a0ngoTCEjpxSATypFZ20', '<приватный ключ Reality>'),
    ('9ho77A1QVREFFDhQkM', '<приватный ключ Reality>'),
    # чужая открытая панель Remnawave (адрес + порт админки)
    ('128.140.103.90', '128.140.x.x'),
    # «вышли на конкурента»: чужая нода и хосты
    ('51.250.121.69', '51.250.x.x'),
]

PHONE = re.compile(r'(?<![\d.])(?:\+7|8)[\s(-]?\d{3}[\s)-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?![\d.])')


def targets():
    for pat in ('docs/**/*.md', 'source/notes/*.md', 'indexes/*.md', '*.md'):
        for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
            yield os.path.relpath(p, ROOT).replace('\\', '/')


def collect_names():
    """Полные имена, встречающиеся как автор сообщения."""
    names = collections.Counter()
    for rel in targets():
        text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        for body in PROOF_BODY.findall(text):
            parts = [x.strip() for x in body.replace(chr(92) + '|', '|').split('|')]
            for cand in parts[1:2]:
                if not cand or NOT_PEOPLE.search(cand):
                    continue
                m = FULLNAME.match(cand)
                if m:
                    names[cand] += 1
    return names


def name_regex(names):
    """Регексп под список полных имён: ловит «@Имя Фамилия» и падежи («Ак Барса»)."""
    if not names:
        return None
    body = '|'.join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    return re.compile(r'(?<!\w)(' + body + r')([а-яё]{1,3})?(?![A-Za-zЀ-ӿ])')


def main():
    dry = '--dry' in sys.argv
    names = collect_names()
    mapping = {}
    for full in names:
        first, last = FULLNAME.match(full).groups()
        mapping[full] = '%s %s.' % (first, last[0])
    # длинные имена заменяем первыми, чтобы не ломать вложенные совпадения
    ordered = sorted(mapping, key=len, reverse=True)
    name_rx = name_regex(ordered)

    stats = collections.Counter()
    for rel in sorted(targets()):
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        out = src
        if name_rx:
            def swap(m):
                # внутри URL не трогаем (там имён нет, но бывают похожие пути)
                head = out[max(0, m.start() - 40):m.start()]
                if 'http' in head and ' ' not in head[head.rfind('http'):]:
                    return m.group(1)
                return mapping[m.group(1)]

            out, n = name_rx.subn(swap, out)
            stats['имён обезличено'] += n
        for old, new in REDACTIONS:
            if old in out:
                stats['секретов вычищено'] += out.count(old)
                out = out.replace(old, new)
        out, n = PHONE.subn('[номер скрыт]', out)
        stats['телефонов скрыто'] += n
        if out != src:
            stats['файлов изменено'] += 1
            if not dry:
                open(path, 'w', encoding='utf-8').write(out)
    print('полных имён в базе: %d (обращений: %d)' % (len(names), sum(names.values())))
    for k in ('имён обезличено', 'секретов вычищено', 'телефонов скрыто', 'файлов изменено'):
        print('  %-20s %d' % (k, stats[k]))
    if dry:
        print('  (пробный прогон, файлы не тронуты)')
        print('  примеры замен:', list(mapping.items())[:6])


if __name__ == '__main__':
    main()
