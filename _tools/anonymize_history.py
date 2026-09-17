# -*- coding: utf-8 -*-
"""Разовый добивающий проход обезличивания.

sanitize.py берёт список имён из полей автора в текущих файлах. После первого
прогона поля уже сокращены, а упоминания тех же людей в тексте («доработанный
Edward Forix») остаются. Этот скрипт берёт список имён из git-истории
(состояние до обезличивания) и правит оставшиеся упоминания в рабочем дереве.

Список имён нигде не сохраняется — иначе обезличивание теряет смысл.

Запуск: python _tools/anonymize_history.py [--dry] [--rev HEAD]
"""
import os
import re
import sys
import glob
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT
from sanitize import FULLNAME, NOT_PEOPLE, PROOF_BODY, name_regex


def git(args):
    return subprocess.run(['git'] + args, cwd=ROOT, capture_output=True).stdout


def names_from(rev):
    raw = git(['ls-tree', '-r', '--name-only', '-z', rev]).decode('utf-8', 'replace')
    out = set()
    for name in raw.split('\0'):
        if not name.endswith('.md'):
            continue
        text = git(['show', '%s:%s' % (rev, name)]).decode('utf-8', 'replace')
        for body in PROOF_BODY.findall(text):
            parts = [x.strip() for x in body.replace(chr(92) + '|', '|').split('|')]
            if len(parts) < 2:
                continue
            cand = parts[1]
            if cand and not NOT_PEOPLE.search(cand) and FULLNAME.match(cand):
                out.add(cand)
    return out


def main():
    dry = '--dry' in sys.argv
    rev = sys.argv[sys.argv.index('--rev') + 1] if '--rev' in sys.argv else 'HEAD'
    names = names_from(rev)
    if not names:
        print('в %s имён не найдено' % rev)
        return
    mapping = {}
    for n in names:
        m = FULLNAME.match(n)
        mapping[n] = m.group(1) + ' ' + m.group(2)[0] + '.'
    rx = name_regex(mapping)
    total = files = 0
    for pat in ('docs/**/*.md', 'source/notes/*.md', 'indexes/*.md', '*.md'):
        for path in glob.glob(os.path.join(ROOT, pat), recursive=True):
            src = open(path, encoding='utf-8').read()

            def swap(m):
                head = src[max(0, m.start() - 40):m.start()]
                if 'http' in head and ' ' not in head[head.rfind('http'):]:
                    return m.group(1)
                return mapping[m.group(1)]

            out, n = rx.subn(swap, src)
            if n:
                total += n
                files += 1
                if not dry:
                    open(path, 'w', encoding='utf-8').write(out)
    print('имён из %s: %d | обезличено упоминаний: %d в %d файлах%s'
          % (rev, len(names), total, files, ' (пробный прогон)' if dry else ''))


if __name__ == '__main__':
    main()
