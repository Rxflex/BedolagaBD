# -*- coding: utf-8 -*-
"""Разворачивает ссылочные свалки в таблицы «Что | Ссылка | Пруф».

Было (один пункт на 400 символов):
  - Смена ядра Xray: [DigneZzZ/remnawave-scripts](url) [id=16246]; Subscription Page: [remnawave/subscription-page](url) [id=310]; …

Стало:
  | Что | Ссылка | Пруф |
  |---|---|---|
  | Смена ядра Xray | [DigneZzZ/remnawave-scripts](url) | [id=16246] |
  | Subscription Page | [remnawave/subscription-page](url) | [id=310] |

Запуск: python _tools/tables_for_links.py [--dry] [файл ...]
По умолчанию обрабатывается каталог ссылок раздела 01.
"""
import os
import re
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT
from prettify_links import label_for

DEFAULT_FILES = ['docs/01-панели/ссылки-инструменты.md']

LINK_RE = re.compile(r'\[[^\]]*\]\((?:https?|mailto):[^)]*\)')
PROOF_RE = re.compile(r'\[id=[^\]]+\](?:\([^)]*\))?')
CODE_RE = re.compile(r'`[^`]*`')
BARE_RE = re.compile(r'(?<![(\[])https?://[^\s<>"`\[\]()]+')
HEADER = ['| Что | Ссылка | Пруф |', '|---|---|---|']


def split_entries(text):
    """Режем пункт на записи по '; ', не задевая код и скобки."""
    parts, depth, buf, i = [], 0, [], 0
    in_code = False
    while i < len(text):
        ch = text[i]
        if ch == '`':
            in_code = not in_code
        if not in_code:
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth = max(0, depth - 1)
            elif ch == ';' and depth == 0:
                parts.append(''.join(buf))
                buf = []
                i += 1
                while i < len(text) and text[i] == ' ':
                    i += 1
                continue
        buf.append(ch)
        i += 1
    parts.append(''.join(buf))
    return [p.strip() for p in parts if p.strip()]


def to_row(entry):
    """Запись → (что, ссылки, пруфы) либо None, если не раскладывается."""
    links = LINK_RE.findall(entry)
    proofs = PROOF_RE.findall(entry)
    # голые URL тоже забираем в колонку ссылок
    rest = CODE_RE.sub(' ', PROOF_RE.sub('', LINK_RE.sub('', entry)))
    bare = BARE_RE.findall(rest)
    for u in bare:
        u2 = u.rstrip('.,;:')
        links.append('[%s](%s)' % (label_for(u2), u2))
    if not links and not proofs:
        return None
    name = PROOF_RE.sub('', LINK_RE.sub('', entry))
    for u in bare:
        name = name.replace(u, ' ')
    name = re.sub(r'\s{2,}', ' ', name)
    name = name.lstrip(' \t—–:;,').rstrip(' \t—–-:,.;')
    if not name:
        # имя берём из первой ссылки
        m = re.match(r'\[([^\]]*)\]', links[0]) if links else None
        name = m.group(1) if m else '—'
    name = name.replace('|', chr(92) + '|')
    return (name, ' · '.join(links) or '—', ' '.join(proofs) or '—')


def tokens(text):
    """Смысловые токены для проверки, что ничего не пропало."""
    text = text.replace('][', '] [').replace(chr(92) + '|', '|')
    text = re.sub(r'[\[\]()]', ' ', text)
    text = re.sub(r'[\s|]+', ' ', text)
    out = collections.Counter()
    for t in text.split(' '):
        t = t.strip(' \t—–-:,.;()')
        if t:
            out[t] += 1
    return out


def convert(path, dry=False):
    src = open(os.path.join(ROOT, path), encoding='utf-8').read()
    lines = src.split('\n')
    out, table = [], []
    infence = service = False
    converted = 0

    def flush():
        nonlocal table
        if table:
            out.extend([''] + HEADER + ['| %s | %s | %s |' % r for r in table] + [''])
            table = []

    for line in lines:
        st = line.strip()
        if st.startswith('<!-- KB:'):
            service = True
        if st.startswith('```'):
            infence = not infence
        if infence or service:
            if st.startswith('<!-- /KB:'):
                service = False
            flush()
            out.append(line)
            continue
        if line.startswith('- '):
            entries = split_entries(line[2:])
            rows = [to_row(e) for e in entries]
            if rows and all(rows):
                table.extend(rows)
                converted += 1
                continue
        flush()
        out.append(line)
    flush()

    res = re.sub(r'\n{3,}', '\n\n', '\n'.join(out))
    lost = tokens(src) - tokens(res)
    if lost:
        print('  ВНИМАНИЕ %s: потеряно %d токенов, напр. %s'
              % (path, sum(lost.values()), list(lost)[:5]))
        return 0
    if not dry:
        open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(res)
    return converted


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    files = args or DEFAULT_FILES
    total = 0
    for f in files:
        n = convert(f.replace('\\', '/'), dry)
        total += n
        print('%s: пунктов превращено в строки таблиц: %d' % (f, n))
    print('итого: %d%s' % (total, ' (пробный прогон)' if dry else ''))


if __name__ == '__main__':
    main()
