# -*- coding: utf-8 -*-
"""Превращает голые URL в компактные markdown-ссылки.

Было:  Смена ядра Xray: https://github.com/DigneZzZ/remnawave-scripts [id=16246]
Стало: Смена ядра Xray: [DigneZzZ/remnawave-scripts](https://github.com/DigneZzZ/remnawave-scripts) [id=16246]

Сам URL остаётся в href — для грепа и для агентов ничего не теряется,
а строка становится в разы короче. Идемпотентно: уже оформленные ссылки,
код в бэктиках и блоки кода не трогаются.

Запуск: python _tools/prettify_links.py [--dry]
"""
import os
import re
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT

URL_RE = re.compile(r'https?://[^\s<>"`\[\]()]+')
MAX = 46


def label_for(url):
    u = url.rstrip('.,;:')
    body = re.sub(r'^https?://', '', u)
    host, _, path = body.partition('/')
    host = host.replace('www.', '')
    parts = [p for p in path.split('/') if p]

    if host in ('github.com',) and len(parts) >= 2:
        base = '%s/%s' % (parts[0], parts[1])
        rest = parts[2:]
        if not rest:
            return base
        kind = rest[0]
        if kind == 'releases':
            return base + ' · releases'
        if kind == 'wiki':
            return base + ' · wiki'
        if kind in ('blob', 'tree') and len(rest) >= 3:
            return base + ' · ' + rest[-1]
        if kind in ('issues', 'pull') and len(rest) >= 2:
            return base + '#' + rest[1]
        if kind == 'commit':
            return base + ' · commit'
        return base + ' · ' + kind
    if host in ('raw.githubusercontent.com', 'gist.github.com') and len(parts) >= 2:
        return '%s/%s · raw' % (parts[0], parts[1])
    if host == 'ghcr.io':
        return 'ghcr.io/' + '/'.join(parts[:2])
    if host == 't.me':
        if parts and parts[0] == 'c':
            return 'сообщение в чате'
        if parts:
            return '@' + parts[0].lstrip('@')
        return 't.me'
    if not parts:
        return host
    tail = parts[-1]
    if len(tail) > 24 or re.fullmatch(r'[\d.]+', tail):
        tail = parts[0] if parts[0] != tail else ''
    out = host + ('/' + tail if tail else '')
    return out if len(out) <= MAX else host


def process_line(line):
    """Оформляет голые URL вне кода и вне существующих ссылок."""
    out = []
    i = 0
    # куски в бэктиках не трогаем
    for chunk in re.split(r'(`[^`]*`)', line):
        if chunk.startswith('`'):
            out.append(chunk)
            continue
        res = []
        pos = 0
        for m in URL_RE.finditer(chunk):
            before = chunk[:m.start()]
            # уже внутри markdown-ссылки: ...](URL) или <URL>
            if before.endswith('](') or before.endswith('<'):
                continue
            url = m.group(0)
            trail = ''
            while url and url[-1] in '.,;:':
                trail = url[-1] + trail
                url = url[:-1]
            label = label_for(url)
            if label == url or len(url) <= len(label) + 8:
                continue
            res.append(chunk[pos:m.start()])
            res.append('[%s](%s)%s' % (label, url, trail))
            pos = m.end()
        res.append(chunk[pos:])
        out.append(''.join(res))
    return ''.join(out)


def main():
    dry = '--dry' in sys.argv
    files = [os.path.relpath(p, ROOT).replace('\\', '/')
             for p in glob.glob(os.path.join(ROOT, 'docs/**/*.md'), recursive=True)]
    changed_files = links = 0
    for rel in sorted(files):
        if rel.endswith('/README.md'):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        lines = src.split('\n')
        out, infence, service = [], False, False
        for line in lines:
            st = line.strip()
            if st.startswith('<!-- KB:'):
                service = True
            if st.startswith('```'):
                infence = not infence
            if infence or service:
                out.append(line)
                if st.startswith('<!-- /KB:'):
                    service = False
                continue
            new = process_line(line)
            links += len(URL_RE.findall(line)) if new != line else 0
            out.append(new)
        res = '\n'.join(out)
        if res != src:
            # проверка: множество URL не изменилось
            def norm(seq):
                return sorted(u.rstrip('.,;:') for u in seq)

            if norm(URL_RE.findall(src)) != norm(URL_RE.findall(res)):
                sys.exit('URL потерялись в %s' % rel)
            changed_files += 1
            if not dry:
                open(path, 'w', encoding='utf-8').write(res)
    print('оформлено ссылок: ~%d, файлов изменено: %d%s'
          % (links, changed_files, ' (пробный прогон)' if dry else ''))


if __name__ == '__main__':
    main()
