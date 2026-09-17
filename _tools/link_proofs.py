# -*- coding: utf-8 -*-
"""Делает пруфы `[id=N]` кликабельными ссылками на сообщения Telegram.

Чат — форум, поэтому ссылка вида https://t.me/c/<chat>/<тред>/<id>: тред
(топик) у каждого сообщения свой, и он вычисляется из HTML-экспорта по
цепочке reply_to до корня топика.

Запуск:
    python _tools/link_proofs.py [--export "<путь к ChatExport_*>"] [--dry]

Карта id → тред кешируется в _cache/threads.tsv, чтобы не парсить 576 МБ
экспорта каждый раз. Повторный запуск идемпотентен: уже размеченные пруфы
(за которыми идёт `(https://t.me/...)`) не трогаются.
"""
import os
import re
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT

CHAT_ID = '2941121338'
BASE = 'https://t.me/c/' + CHAT_ID
DEFAULT_EXPORT = r'C:\Users\andy\Downloads\AyuGram Desktop\ChatExport_2026-08-23'
CACHE = os.path.join(ROOT, '_tools', 'data', 'threads.tsv')

MSG_RE = re.compile(r'id="message(-?\d+)"')
GOTO_RE = re.compile(r'GoToMessage\((\d+)\)')
TOPIC_RE = re.compile(r'created topic')
PROOF_RE = re.compile(r'\[id=(?P<body>[^\]]+)\](?P<tail>\((?:https?:)?[^)]*\))?')
FIRST_ID_RE = re.compile(r'(\d+)')


def parse_export(export_dir):
    """id → reply_to по всему экспорту + множество корней топиков."""
    files = sorted(glob.glob(os.path.join(export_dir, 'messages*.html')),
                   key=lambda p: int(re.sub(r'\D', '', os.path.basename(p)) or 0))
    if not files:
        sys.exit('не найдены messages*.html в %s' % export_dir)
    reply = {}
    roots = set()
    total = 0
    for n, path in enumerate(files, 1):
        html = open(path, encoding='utf-8').read()
        # режем на блоки сообщений по позициям id="messageN"
        marks = [(m.start(), m.group(1)) for m in MSG_RE.finditer(html)]
        for i, (pos, mid) in enumerate(marks):
            end = marks[i + 1][0] if i + 1 < len(marks) else len(html)
            block = html[pos:end]
            total += 1
            if TOPIC_RE.search(block):
                roots.add(mid)
                continue
            g = GOTO_RE.search(block)
            if g:
                reply[mid] = g.group(1)
        if n % 100 == 0:
            print('  прочитано файлов: %d/%d, сообщений: %d' % (n, len(files), total))
    print('сообщений: %d, корней топиков: %s' % (total, sorted(roots, key=int)))
    return reply, roots


def resolve_threads(reply, roots):
    """Тред сообщения = корень его reply-цепочки (если это корень топика)."""
    thread = {}

    def walk(mid):
        chain = []
        cur = mid
        seen = set()
        while True:
            if cur in thread:
                res = thread[cur]
                break
            if cur in roots:
                res = cur
                break
            if cur in seen or cur not in reply:
                res = thread.get(cur, '')
                break
            seen.add(cur)
            chain.append(cur)
            cur = reply[cur]
        for c in chain:
            thread[c] = res
        thread[mid] = res
        return res

    for mid in list(reply):
        walk(mid)
    for r in roots:
        thread[r] = r
    return thread


def load_cache():
    if not os.path.exists(CACHE):
        return None
    out = {}
    for line in open(CACHE, encoding='utf-8'):
        a, _, b = line.rstrip('\n').partition('\t')
        if a:
            out[a] = b
    return out


def save_cache(thread):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, 'w', encoding='utf-8') as fh:
        for k in sorted(thread, key=int):
            fh.write('%s\t%s\n' % (k, thread[k]))
    print('кеш: %s (%d записей)' % (os.path.relpath(CACHE, ROOT), len(thread)))


def url_for(mid, thread):
    t = thread.get(mid)
    if t and t != mid:
        return '%s/%s/%s' % (BASE, t, mid)
    return '%s/%s' % (BASE, mid)


def md_files():
    for pat in ('docs/**/*.md', 'source/notes/*.md'):
        for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
            yield os.path.relpath(p, ROOT).replace('\\', '/')


def rewrite(thread, dry=False):
    changed = files_changed = skipped = 0
    for rel in sorted(md_files()):
        path = os.path.join(ROOT, rel)
        lines = open(path, encoding='utf-8').read().split('\n')
        out = []
        touched = False
        for line in lines:
            in_table = line.lstrip().startswith('|')

            def repl(m):
                nonlocal changed, skipped, touched
                body, tail = m.group('body'), m.group('tail')
                if tail:                      # уже ссылка
                    return m.group(0)
                fid = FIRST_ID_RE.search(body)
                if not fid:
                    skipped += 1
                    return m.group(0)
                label = 'id=' + body
                if in_table:
                    label = label.replace('|', chr(92) + '|')
                changed += 1
                touched = True
                return '[%s](%s)' % (label, url_for(fid.group(1), thread))

            out.append(PROOF_RE.sub(repl, line))
        if touched:
            files_changed += 1
            if not dry:
                open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print('пруфов размечено: %d, файлов: %d, без номера: %d%s'
          % (changed, files_changed, skipped, ' (пробный прогон)' if dry else ''))


def main():
    args = sys.argv[1:]
    dry = '--dry' in args
    export = DEFAULT_EXPORT
    if '--export' in args:
        export = args[args.index('--export') + 1]
    thread = load_cache()
    if thread is None:
        print('парсю экспорт: %s' % export)
        reply, roots = parse_export(export)
        thread = resolve_threads(reply, roots)
        save_cache(thread)
    else:
        print('карта тредов из кеша: %d записей' % len(thread))
    rewrite(thread, dry)


if __name__ == '__main__':
    main()
