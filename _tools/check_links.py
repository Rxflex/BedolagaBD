# -*- coding: utf-8 -*-
"""Проверяет внутренние ссылки и якоря во всех markdown-файлах базы.

Запуск: python _tools/check_links.py
Код возврата 1, если есть битые ссылки.
"""
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT, slug

LINK_RE = re.compile(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HREF_RE = re.compile(r'<a\s+href="([^"]+)"', re.I)
IMG_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"', re.I)
SKIP_DIRS = {'.git', '_extraction', '.continuum'}


def md_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.md'):
                yield os.path.relpath(os.path.join(base, f), ROOT).replace('\\', '/')


def anchors_of(path):
    """Все якоря файла: слаги заголовков вне блоков кода."""
    res, used, infence = set(), {}, False
    for line in open(os.path.join(ROOT, path), encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('```'):
            infence = not infence
            continue
        if infence:
            continue
        m = re.match(r'^#{1,6} +(.*?)\s*$', line)
        if m:
            res.add(slug(m.group(1), used))
        for mm in re.finditer(r'<a\s+(?:name|id)="([^"]+)"', line, re.I):
            res.add(mm.group(1))
    return res


def main():
    anchors_cache = {}
    bad = []
    total = 0
    for path in sorted(md_files()):
        text = open(os.path.join(ROOT, path), encoding='utf-8').read()
        # ссылки вне блоков кода
        clean_lines, infence = [], False
        for line in text.split('\n'):
            if line.startswith('```'):
                infence = not infence
                continue
            clean_lines.append('' if infence else re.sub(r'`[^`]*`', '', line))
        body = '\n'.join(clean_lines)
        targets = LINK_RE.findall(body) + HREF_RE.findall(body) + IMG_RE.findall(body)
        for t in targets:
            if t.startswith(('http://', 'https://', 'mailto:', 'tg://')):
                continue
            total += 1
            t = urllib.parse.unquote(t)
            file_part, _, anchor = t.partition('#')
            if not file_part:
                target_path = path
            else:
                target_path = os.path.normpath(os.path.join(os.path.dirname(path), file_part)).replace('\\', '/')
            full = os.path.join(ROOT, target_path)
            if not os.path.exists(full):
                bad.append((path, t, 'нет файла %s' % target_path))
                continue
            if anchor and target_path.endswith('.md'):
                if target_path not in anchors_cache:
                    anchors_cache[target_path] = anchors_of(target_path)
                if anchor not in anchors_cache[target_path]:
                    bad.append((path, t, 'нет якоря #%s в %s' % (anchor, target_path)))
    print('проверено ссылок: %d' % total)
    if not bad:
        print('OK: битых ссылок нет')
        return 0
    print('БИТЫХ: %d' % len(bad))
    for src, t, why in bad[:60]:
        print('  %s → %s  (%s)' % (src, t, why))
    if len(bad) > 60:
        print('  … и ещё %d' % (len(bad) - 60))
    return 1


if __name__ == '__main__':
    sys.exit(main())
