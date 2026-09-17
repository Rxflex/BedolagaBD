# -*- coding: utf-8 -*-
"""Рисует assets/diagrams/transports-timeline.svg — что из транспортов жило и когда.

Данные берутся из docs/03-обход-тспу/хронология.md и docs/02-транспорты/вехи.md
(вручную сведённые интервалы; при правках базы обновлять здесь).
Запуск: python _tools/build_timeline.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT

MONTHS = ['08.25', '09.25', '10.25', '11.25', '12.25', '01.26', '02.26', '03.26',
          '04.26', '05.26', '06.26', '07.26', '08.26']

OK, WARN, DEAD, NEW = '#06d6a0', '#ffd166', '#ff6b6b', '#7c8cff'

# (название, подпись, [(старт, конец, состояние, подпись-на-сегменте)]) — индексы месяцев, конец включительно
ROWS = [
    ('VLESS + Reality (TCP)', 'основа 2025-го', [
        (0, 3, OK, 'рабочая база'),
        (3, 4, DEAD, ''),
        (4, 9, WARN, 'частично, по регионам'),
        (9, 10, DEAD, ''),
        (10, 12, DEAD, '«выгнали» 16.06, бан 25.06'),
    ]),
    ('XHTTP + selfsni', 'главный рецепт с 11.2025', [
        (3, 10, OK, 'воскрешает всё'),
        (10, 12, OK, 'держится, местами шейпинг'),
    ]),
    ('Hysteria2 (UDP)', 'запас прочности', [
        (0, 9, OK, ''),
        (9, 11, OK, '«идеально под обфускацией»'),
        (11, 12, WARN, ''),
    ]),
    ('gRPC', 'резерв при отвале TCP', [
        (0, 9, WARN, ''),
        (9, 11, OK, '«сидим на gRPC» 28.05'),
        (11, 12, WARN, ''),
    ]),
    ('WebSocket + TLS', 'под CDN и реверс', [
        (0, 9, WARN, ''),
        (9, 10, DEAD, ''),
        (10, 12, WARN, ''),
    ]),
    ('SS-2022 / мосты RU→EU', 'вход в РФ, выход в ЕС', [
        (0, 9, OK, ''),
        (9, 12, OK, 'мост «фиксит» шейпинг'),
    ]),
    ('CDN-фронтинг', 'Yandex · Beeline · VK · MWS', [
        (4, 10, OK, 'дешёвый обход через РФ-CDN'),
        (10, 11, WARN, ''),
        (11, 12, DEAD, 'Beeline, VK, Yandex — 08.26'),
    ]),
    ('БС (белые списки)', 'то включают, то отбирают', [
        (4, 8, OK, 'массовая выдача'),
        (8, 10, WARN, 'VK отбирает 01.04'),
        (10, 11, WARN, ''),
        (11, 12, WARN, 'бан по /32'),
    ]),
    ('finalmask (SSH/DNS/XMC)', 'новое, август 2026', [
        (11, 12, NEW, 'SSH · DNS · XMC'),
    ]),
]

EVENTS = [
    (3.1, '22–25.11.25', 'массовый отвал Reality'),
    (5.1, '01.12.25', 'ЮKassa требует РФ-IP'),
    (9.2, '25–27.05.26', 'детект TLS-in-TLS'),
    (10.1, '08.06.26', '«БСЫ ВСЁ», nLighten'),
    (10.7, '25.06.26', 'VLESS забанен у многих'),
    (12.0, '04–13.08.26', 'CDN-аккаунты снесли'),
]

W, H = 1200, 700
X0, X1 = 250, 1160
TOP = 150
ROW_H = 46


def x_of(i):
    return X0 + (X1 - X0) * i / len(MONTHS)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def main():
    p = []
    a = p.append
    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
      'aria-label="Таймлайн жизни транспортов 2025-2026">' % (W, H, W, H))
    a('''  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#161b22"/><stop offset="1" stop-color="#0d1117"/>
    </linearGradient>
    <pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">
      <path d="M 26 0 H 0 V 26" fill="none" stroke="#ffffff" stroke-opacity="0.03"/>
    </pattern>
    <style>
      .t{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
      .m{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
      .h{font-size:22px;font-weight:700;fill:#e6edf3}
      .s{font-size:13px;fill:#8b949e}
      .row{font-size:14.5px;font-weight:600;fill:#e6edf3}
      .sub{font-size:11.5px;fill:#8b949e}
      .seg{font-size:11px;fill:#0d1117;font-weight:600}
      .mon{font-size:11.5px;fill:#8b949e}
      .ev{font-size:11px;fill:#8b949e}
    </style>
  </defs>''')
    a('  <rect width="%d" height="%d" rx="16" fill="url(#bg)"/>' % (W, H))
    a('  <rect width="%d" height="%d" rx="16" fill="url(#grid)"/>' % (W, H))
    a('  <rect width="%d" height="%d" rx="16" fill="none" stroke="#ff6b6b" stroke-opacity="0.3"/>' % (W, H))
    a('  <text x="36" y="48" class="t h">Транспорты: что работало и когда</text>')
    a('  <text x="36" y="72" class="t s">08.2025 → 08.2026 по данным чата. Зелёный — работает, жёлтый — шатко/по регионам, '
      'красный — отвал, синий — новое.</text>')

    # легенда
    lx = 36
    for color, label in ((OK, 'работает'), (WARN, 'шатко'), (DEAD, 'отвал'), (NEW, 'новое')):
        a('  <rect x="%d" y="96" width="14" height="14" rx="4" fill="%s"/>' % (lx, color))
        a('  <text x="%d" y="108" class="t s">%s</text>' % (lx + 20, label))
        lx += 24 + 9 * len(label) + 26

    # сетка месяцев
    for i, m in enumerate(MONTHS):
        x = x_of(i)
        a('  <line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#ffffff" stroke-opacity="0.06"/>'
          % (x, TOP - 18, x, TOP + ROW_H * len(ROWS) + 6))
        a('  <text x="%.1f" y="%d" class="t mon" text-anchor="middle">%s</text>'
          % (x + (X1 - X0) / len(MONTHS) / 2, TOP - 24, m))

    # строки
    for r, (name, sub, segs) in enumerate(ROWS):
        y = TOP + r * ROW_H
        a('  <text x="36" y="%d" class="t row">%s</text>' % (y + 18, esc(name)))
        a('  <text x="36" y="%d" class="t sub">%s</text>' % (y + 34, esc(sub)))
        a('  <rect x="%d" y="%d" width="%d" height="30" rx="8" fill="#ffffff" fill-opacity="0.03"/>'
          % (X0, y + 4, X1 - X0))
        for s, e, color, label in segs:
            xs, xe = x_of(s), x_of(e + 1)
            a('  <rect x="%.1f" y="%d" width="%.1f" height="30" rx="8" fill="%s" fill-opacity="0.85"/>'
              % (xs, y + 4, max(10, xe - xs - 3), color))
            seg_w = max(10, xe - xs - 3)
            if label and 7.6 * len(label) + 22 <= seg_w:
                a('  <text x="%.1f" y="%d" class="t seg">%s</text>' % (xs + 10, y + 24, esc(label)))

    # переломные даты — только тики с датами, описания идут подписью в markdown
    ey = TOP + ROW_H * len(ROWS) + 18
    a('  <text x="36" y="%d" class="t row">Переломы</text>' % (ey + 20))
    last_x = [-1e9, -1e9, -1e9]
    for i, (pos, date, label) in enumerate(EVENTS):
        x = x_of(pos)
        row = next((r_ for r_ in range(3) if x - last_x[r_] > 130),
                   min(range(3), key=lambda r_: last_x[r_]))
        last_x[row] = x
        yy = ey + 14 + row * 24
        a('  <line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#ff6b6b" stroke-opacity="0.5" stroke-dasharray="4 3"/>'
          % (x, TOP - 18, x, yy - 8))
        a('  <circle cx="%.1f" cy="%d" r="3.5" fill="#ff6b6b"/>' % (x, yy - 8))
        far = x > W - 140
        anchor = 'end' if far else 'middle'
        tx = x - 6 if far else x
        a('  <text x="%.1f" y="%d" class="t m ev" fill="#ff6b6b" text-anchor="%s">%s</text>' % (tx, yy + 8, anchor, date))

    a('  <text x="%d" y="%d" class="t m" font-size="11.5" fill="#8b949e" fill-opacity="0.6" text-anchor="end">'
      'assets/diagrams/transports-timeline.svg</text>' % (W - 36, H - 20))
    a('</svg>')
    path = os.path.join(ROOT, 'assets/diagrams/transports-timeline.svg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write('\n'.join(p) + '\n')
    print('svg: assets/diagrams/transports-timeline.svg')


if __name__ == '__main__':
    main()
