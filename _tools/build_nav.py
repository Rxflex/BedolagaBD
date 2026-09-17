# -*- coding: utf-8 -*-
"""Навигация базы знаний: шапки/подвалы документов, хабы разделов, MAP.md.

Идемпотентно — служебные блоки живут между маркерами <!-- KB:NAV --> и т.п.
Запуск: python _tools/build_nav.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT, sections, headings, slug, rel, stats


def events_count(path):
    n = 0
    for line in open(os.path.join(ROOT, path), encoding='utf-8'):
        if line.startswith('- **'):
            n += 1
    return n


def blurb_of(sec, fname, blurb):
    """Для хронологии подпись считается из содержимого."""
    if blurb:
        return blurb
    if sec['key'] == '08':
        n = events_count(sec['dir'] + '/' + fname)
        return 'датированных вех: %d' % n
    return ''

IDX_FILES = [('релизы.md', 'релизы'), ('ошибки.md', 'ошибки'), ('env.md', 'env'),
             ('термины.md', 'термины'), ('ссылки.md', 'ссылки')]


def idx_bar(from_file):
    parts = ['[⌂ База знаний](%s)' % rel('README.md', from_file),
             '[🗺 Карта](%s)' % rel('MAP.md', from_file)]
    links = ' · '.join('[%s](%s)' % (label, rel('indexes/' + f, from_file)) for f, label in IDX_FILES)
    parts.append('Индексы: ' + links)
    return ' · '.join(parts)


def block(name, payload):
    return ['<!-- KB:%s -->' % name] + payload + ['<!-- /KB:%s -->' % name]


def strip_blocks(lines):
    out, skip = [], False
    for l in lines:
        s = l.strip()
        if s.startswith('<!-- KB:'):
            skip = True
            continue
        if s.startswith('<!-- /KB:'):
            skip = False
            continue
        if not skip:
            out.append(l)
    return out


def toc(path, from_file, depth=3):
    hs = [h for h in headings(path) if 2 <= h[0] <= depth]
    if len(hs) < 3:
        return []
    body = ['<details>', '<summary>📑 <b>На этой странице</b> — %d разделов</summary>' % len(hs), '']
    for lvl, txt, sl, ln in hs:
        body.append('%s- [%s](#%s)' % ('  ' * (lvl - 2), txt, sl))
    body += ['', '</details>']
    return body


def doc_header(sec, i, path):
    """Хлебные крошки + пред/след внутри раздела."""
    files = sec['files']
    fname, title, blurb = files[i]
    crumbs = '[⌂](%s) › [%s %s. %s](%s) › **%s**' % (
        rel('README.md', path), sec['emoji'], sec['key'], sec['name'], 'README.md', title)
    nav = []
    if i > 0:
        nav.append('◀ [%s](%s)' % (files[i - 1][1], files[i - 1][0]))
    if i < len(files) - 1:
        nav.append('[%s](%s) ▶' % (files[i + 1][1], files[i + 1][0]))
    out = [crumbs]
    if nav:
        out += ['', ' · '.join(nav)]
    return out


def process_doc(sec, i):
    fname, title, blurb = sec['files'][i]
    blurb = blurb_of(sec, fname, blurb)
    path = os.path.join(sec['dir'], fname).replace('\\', '/')
    full = os.path.join(ROOT, path)
    lines = strip_blocks(open(full, encoding='utf-8').read().split('\n'))
    while lines and lines[0].strip() == '':
        lines.pop(0)
    has_h1 = bool(lines) and lines[0].startswith('# ')
    h1 = lines[0] if has_h1 else '# ' + title
    rest = lines[1:] if has_h1 else lines
    while rest and rest[0].strip() == '':
        rest.pop(0)
    while rest and rest[-1].strip() == '':
        rest.pop()
    # подчищаем следы прежних прогонов: подпись и разделители жили в контенте
    junk = {'', '---', '> ' + blurb if blurb else '\0'}
    while rest and rest[0].strip() in junk:
        rest.pop(0)
    while rest and rest[-1].strip() in junk:
        rest.pop()

    head = doc_header(sec, i, path)
    if blurb:
        head += ['', '> ' + blurb]
    t = toc(path, path)
    if t:
        head += [''] + t
    head += ['', '---']
    new = [h1, ''] + block('HEAD', head) + [''] + rest + ['']
    new += block('FOOT', ['---', ''] + doc_header(sec, i, path) + ['', idx_bar(path)])
    open(full, 'w', encoding='utf-8').write('\n'.join(new) + '\n')
    return path


def section_hub(sec, prev_sec, next_sec):
    path = os.path.join(sec['dir'], 'README.md').replace('\\', '/')
    icon = rel('assets/sections/%s.svg' % sec['key'], path)
    tot = {'lines': 0, 'proofs': 0, 'code': 0}
    rows = []
    for fname, title, blurb in sec['files']:
        st = stats(os.path.join(sec['dir'], fname).replace('\\', '/'))
        for k in tot:
            tot[k] += st[k]
        rows.append((fname, title, blurb_of(sec, fname, blurb), st))
    out = ['<div align="center">', '',
           '<img src="%s" alt="%s" width="860">' % (icon, sec['name']), '',
           '</div>', '',
           '# %s %s · %s' % (sec['emoji'], sec['key'], sec['name']), '',
           '> %s' % sec['blurb'], '',
           idx_bar(path), '',
           '`%d документов` · `%d строк` · `%d пруфов` · `%d блоков кода`' %
           (len(sec['files']), tot['lines'], tot['proofs'], tot['code']), '',
           '---', '', '## Документы раздела', '',
           '| # | Документ | О чём | Строк | Пруфов |', '|---|---|---|---:|---:|']
    for n, (fname, title, blurb, st) in enumerate(rows, 1):
        out.append('| %d | **[%s](%s)** | %s | %d | %d |' %
                   (n, title, fname, blurb or '—', st['lines'], st['proofs']))
    inner = [(fname, title,
              [h for h in headings(os.path.join(sec['dir'], fname).replace('\\', '/')) if h[0] == 2])
             for fname, title, blurb, st in rows]
    if any(hs for _, _, hs in inner):
        out += ['', '---', '', '## Что внутри документов', '']
    for fname, title, hs in inner:
        if not hs:
            continue
        out += ['<details>', '<summary><b>%s</b> — %d разделов</summary>' % (title, len(hs)), '']
        for lvl, txt, sl, ln in hs:
            out.append('- [%s](%s#%s)' % (txt, fname, sl))
        out += ['', '</details>', '']
    nav = []
    if prev_sec:
        nav.append('◀ [%s %s. %s](%s)' % (prev_sec['emoji'], prev_sec['key'], prev_sec['name'],
                                          rel(prev_sec['dir'] + '/README.md', path)))
    if next_sec:
        nav.append('[%s %s. %s](%s) ▶' % (next_sec['emoji'], next_sec['key'], next_sec['name'],
                                          rel(next_sec['dir'] + '/README.md', path)))
    out += ['---', '', ' · '.join(nav) if nav else '', '', idx_bar(path)]
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return path


def build_map():
    path = 'MAP.md'
    out = ['<div align="center">', '',
           '<img src="assets/map.svg" alt="Карта базы знаний" width="860">', '',
           '</div>', '', '# 🗺 Карта разделов', '',
           idx_bar(path), '',
           '> Все разделы всех документов на одной странице: для поиска глазами и через Ctrl+F.', '',
           '---', '']
    for sec in sections():
        st = {'lines': 0, 'proofs': 0}
        for fname, title, blurb in sec['files']:
            s = stats(os.path.join(sec['dir'], fname).replace('\\', '/'))
            st['lines'] += s['lines']
            st['proofs'] += s['proofs']
        out += ['## %s [%s. %s](%s)' % (sec['emoji'], sec['key'], sec['name'], sec['dir'] + '/README.md'), '',
                '%s · `%d документов` · `%d строк` · `%d пруфов`' %
                (sec['blurb'], len(sec['files']), st['lines'], st['proofs']), '']
        flat = []
        for fname, title, blurb in sec['files']:
            p = sec['dir'] + '/' + fname
            hs = [h for h in headings(p) if h[0] == 2]
            if not hs:
                # документ без внутренних разделов (например, месяц хронологии)
                flat.append('[%s](%s)' % (title, p))
                continue
            out.append('<details>')
            out.append('<summary><b><a href="%s">%s</a></b> — %d разделов</summary>' % (p, title, len(hs)))
            out.append('')
            for lvl, txt, sl, ln in hs:
                out.append('- [%s](%s#%s)' % (txt, p, sl))
            out += ['', '</details>', '']
        if flat:
            out += [' · '.join(flat), '']
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('обновлено: MAP.md')


def main():
    secs = sections()
    n_docs = 0
    for j, sec in enumerate(secs):
        for i in range(len(sec['files'])):
            process_doc(sec, i)
            n_docs += 1
        section_hub(sec, secs[j - 1] if j > 0 else None, secs[j + 1] if j < len(secs) - 1 else None)
        print('раздел %s: %d документов + хаб' % (sec['key'], len(sec['files'])))
    build_map()
    print('всего документов: %d' % n_docs)


if __name__ == '__main__':
    main()
