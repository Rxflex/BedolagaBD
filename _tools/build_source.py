# -*- coding: utf-8 -*-
"""Переносит заметки-первоисточники в source/notes и строит их указатель.

Заметки — слой пруфов: в них дословный текст сообщений с `[id=...]`.
Исходник: _extraction/notes (не коммитится, там же 99 МБ чанков).
Запуск: python _tools/build_source.py
"""
import os
import re
import sys
import json
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT

SRC_NOTES = os.path.join(ROOT, '_extraction', 'notes')
DST_NOTES = os.path.join(ROOT, 'source', 'notes')
TOPIC_IDX = os.path.join(ROOT, '_extraction', '_extraction_topic_idx.json')

TOPIC_RU = {
    'reality': 'Reality', 'xhttp': 'XHTTP', 'grpc': 'gRPC', 'hysteria': 'Hysteria2',
    'warp': 'WARP', 'cdn': 'CDN', 'tspu': 'ТСПУ', 'fp': 'fingerprint', 'mtu': 'MTU',
    'bbr': 'BBR', 'sysctl': 'sysctl', 'panel': 'панель', 'bedolaga': 'Bedolaga',
    'marzban': 'Marzban', '3xui': '3x-ui', 'hosting': 'хостинг', 'payment': 'платёжки',
    'nginx': 'nginx', 'caddy': 'Caddy', 'haproxy': 'HAProxy', 'docker': 'Docker',
    'dns': 'DNS', 'block-events': 'блокировки',
}

HEAD_RE = re.compile(r'^#\s*Заметк[аи][^(]*\((?P<body>[^)]*)\)')


def parse_head(path):
    with open(path, encoding='utf-8') as fh:
        first = fh.readline().strip()
    m = HEAD_RE.match(first)
    ids, period = '', ''
    if m:
        body = m.group('body')
        mi = re.search(r'id\s*([\d]+)\s*\.\.\s*([\d]+)', body)
        if mi:
            ids = '%s–%s' % (mi.group(1), mi.group(2))
        mp = re.search(r'(\d{2}\.\d{2}\.\d{4})(?:\s*\.\.\s*|\s*[—–-]\s*)?(\d{2}\.\d{2}\.\d{4})?', body)
        if mp:
            period = mp.group(1) + (' – ' + mp.group(2) if mp.group(2) else '')
    return ids, period


def main():
    if not os.path.isdir(SRC_NOTES):
        print('нет %s — заметки не перенесены' % SRC_NOTES)
        return
    os.makedirs(DST_NOTES, exist_ok=True)
    names = sorted(n for n in os.listdir(SRC_NOTES) if n.endswith('.md'))
    force = '--force' in sys.argv
    copied = 0
    for n in names:
        dst = os.path.join(DST_NOTES, n)
        # уже перенесённые заметки не перезатираем: они прошли обезличивание
        # (sanitize.py). Повторный импорт — только с --force, после него
        # обязательно прогнать python _tools/sanitize.py
        if os.path.exists(dst) and not force:
            continue
        shutil.copyfile(os.path.join(SRC_NOTES, n), dst)
        copied += 1
    topics = {}
    if os.path.exists(TOPIC_IDX):
        topics = json.load(open(TOPIC_IDX, encoding='utf-8'))

    rows = []
    for n in names:
        num = re.sub(r'\D', '', n)
        ids, period = parse_head(os.path.join(DST_NOTES, n))
        t = topics.get(num.lstrip('0').zfill(3), {})
        top = sorted(t.items(), key=lambda kv: -kv[1])[:4]
        tags = ' · '.join('`%s`' % TOPIC_RU.get(k, k) for k, v in top if v > 0)
        size = os.path.getsize(os.path.join(DST_NOTES, n)) // 1024
        rows.append((n, ids, period, tags, size))

    out = ['# 🗃 Первоисточники: заметки по чанкам чата', '',
           '[⌂ База знаний](../README.md) · [🗺 Карта](../MAP.md)', '',
           '<!-- Сгенерировано: python _tools/build_source.py -->', '',
           'Экспорт чата (788 тыс. сообщений) нарезан на 172 чанка; по каждому есть заметка с дословными '
           'конфигами, командами и цитатами и метками `[id=N]`. Документы в [docs/](../docs) собраны из этих '
           'заметок — сюда ходят, когда нужен исходный текст сообщения или пруф.', '',
           '**Как найти пруф `[id=123456]`:** возьмите строку с нужным id в документе, определите заметку по '
           'диапазону ниже (id монотонно растут), откройте её и ищите тот же `[id=...]`.', '',
           '| Заметка | id сообщений | Период | Главные темы | КБ |', '|---|---|---|---|---:|']
    for n, ids, period, tags, size in rows:
        out.append('| [%s](notes/%s) | `%s` | %s | %s | %d |' % (n.replace('.md', ''), n, ids, period, tags, size))
    out += ['', '---', '', '[⌂ База знаний](../README.md)']
    path = os.path.join(ROOT, 'source', 'README.md')
    open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('заметок всего: %d, перенесено заново: %d%s'
          % (len(names), copied, ' — прогоните sanitize.py' if copied else ''))
    print('указатель: source/README.md')


if __name__ == '__main__':
    main()
