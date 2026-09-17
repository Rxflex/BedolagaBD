# -*- coding: utf-8 -*-
"""Рисует карточки для донатов: assets/donate/*.svg + шапку блока.

Каждая карточка — монета, сеть, QR-код адреса и сам адрес в две строки.
QR считается segno (pip install segno), рисуется как один <path> внутри
белой плашки, чтобы сканировался в любой теме GitHub.

Запуск: python _tools/build_donate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT

try:
    import segno
except ImportError:
    sys.exit('нужен segno: pip install segno')

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

WALLETS = [
    {
        'slug': 'usdt-trc20', 'coin': 'USDT', 'network': 'TRON · TRC20',
        'color': '#26a17b', 'glyph': '₮',
        'address': 'TYHgzVKjxiBkvXnnrQdGaYQiCrzoEYjrr7',
    },
    {
        'slug': 'usdt-bep20', 'coin': 'USDT', 'network': 'BNB Chain · BEP20',
        'color': '#f0b90b', 'glyph': '₮',
        'address': '0xb3954ccd45ade87f1fee9006f56cdeac41ff8707',
    },
    {
        'slug': 'btc', 'coin': 'BTC', 'network': 'Bitcoin',
        'color': '#f7931a', 'glyph': '₿',
        'address': '1JxKsR9hBXqdWdJYSQpogWEtZKo8ZdnZGG',
    },
    {
        'slug': 'eth', 'coin': 'ETH', 'network': 'Ethereum · ERC20',
        'color': '#8a92b2', 'glyph': 'Ξ',
        'address': '0xb3954ccd45ade87f1fee9006f56cdeac41ff8707',
    },
]

W, H = 320, 456
QR_BOX = 236               # белая плашка под QR
QR_PAD = 12                # поля внутри плашки


def qr_path(data, size, x0, y0):
    """QR как один path: горизонтальные пробеги тёмных модулей."""
    qr = segno.make(data, error='m')
    matrix = [list(row) for row in qr.matrix]
    n = len(matrix)
    unit = size / n
    parts = []
    for r, row in enumerate(matrix):
        c = 0
        while c < n:
            if row[c]:
                start = c
                while c < n and row[c]:
                    c += 1
                parts.append('M%.2f %.2fh%.2fv%.2fh-%.2fz'
                             % (x0 + start * unit, y0 + r * unit,
                                (c - start) * unit, unit, (c - start) * unit))
            else:
                c += 1
    return ''.join(parts), n


def split_address(addr, per=22):
    return [addr[i:i + per] for i in range(0, len(addr), per)]


def card(w):
    color = w['color']
    qx = (W - QR_BOX) / 2
    qy = 118
    path, modules = qr_path(w['address'], QR_BOX - 2 * QR_PAD, qx + QR_PAD, qy + QR_PAD)
    lines = split_address(w['address'])
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="%s %s">' % (W, H, W, H, w['coin'], w['network']),
        '  <defs>',
        '    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '      <stop offset="0" stop-color="#161b22"/><stop offset="1" stop-color="#0d1117"/>',
        '    </linearGradient>',
        '    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">',
        '      <stop offset="0" stop-color="%s" stop-opacity="0.30"/>' % color,
        '      <stop offset="1" stop-color="%s" stop-opacity="0"/>' % color,
        '    </radialGradient>',
        '  </defs>',
        '  <rect width="%d" height="%d" rx="18" fill="url(#bg)"/>' % (W, H),
        '  <rect width="%d" height="%d" rx="18" fill="none" stroke="%s" stroke-opacity="0.45"/>'
        % (W, H, color),
        '  <ellipse cx="%d" cy="16" rx="150" ry="70" fill="url(#glow)"/>' % (W // 2),
        # бейдж монеты
        '  <circle cx="46" cy="52" r="24" fill="%s" fill-opacity="0.16" stroke="%s" stroke-opacity="0.6"/>'
        % (color, color),
        '  <text x="46" y="62" font-family="%s" font-size="27" font-weight="700" fill="%s" '
        'text-anchor="middle">%s</text>' % (FONT, color, w['glyph']),
        '  <text x="84" y="46" font-family="%s" font-size="22" font-weight="800" fill="#e6edf3">%s</text>'
        % (FONT, w['coin']),
        '  <text x="84" y="68" font-family="%s" font-size="13" fill="#8b949e">%s</text>'
        % (FONT, w['network']),
        # плашка с QR
        '  <rect x="%.0f" y="%d" width="%d" height="%d" rx="14" fill="#ffffff"/>'
        % (qx, qy, QR_BOX, QR_BOX),
        '  <path d="%s" fill="#0d1117"/>' % path,
    ]
    y = qy + QR_BOX + 34
    for ln in lines:
        out.append('  <text x="%d" y="%d" font-family="%s" font-size="13" fill="#c9d1d9" '
                   'text-anchor="middle" letter-spacing="0.4">%s</text>' % (W // 2, y, MONO, ln))
        y += 19
    out.append('  <text x="%d" y="%d" font-family="%s" font-size="11" fill="#8b949e" '
               'fill-opacity="0.7" text-anchor="middle">сканируй или скопируй адрес ниже</text>'
               % (W // 2, H - 18, FONT))
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def banner():
    w, h, accent = 1200, 150, '#26a17b'
    return '\n'.join([
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="Поддержать базу знаний">' % (w, h, w, h),
        '  <defs>',
        '    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '      <stop offset="0" stop-color="#161b22"/><stop offset="1" stop-color="#0d1117"/>',
        '    </linearGradient>',
        '    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">',
        '      <path d="M 24 0 H 0 V 24" fill="none" stroke="#ffffff" stroke-opacity="0.04"/>',
        '    </pattern>',
        '    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">',
        '      <stop offset="0" stop-color="%s" stop-opacity="0.32"/>' % accent,
        '      <stop offset="1" stop-color="%s" stop-opacity="0"/>' % accent,
        '    </radialGradient>',
        '  </defs>',
        '  <rect width="%d" height="%d" rx="16" fill="url(#bg)"/>' % (w, h),
        '  <rect width="%d" height="%d" rx="16" fill="url(#grid)"/>' % (w, h),
        '  <rect width="%d" height="%d" rx="16" fill="none" stroke="%s" stroke-opacity="0.35"/>'
        % (w, h, accent),
        '  <ellipse cx="1010" cy="75" rx="260" ry="130" fill="url(#glow)"/>',
        '  <rect x="44" y="40" width="4" height="70" rx="2" fill="%s"/>' % accent,
        '  <text x="66" y="66" font-family="%s" font-size="15" font-weight="700" fill="%s" '
        'letter-spacing="3">ПОДДЕРЖАТЬ</text>' % (FONT, accent),
        '  <text x="64" y="104" font-family="%s" font-size="34" font-weight="800" fill="#e6edf3">'
        'Донат на поддержку базы знаний</text>' % FONT,
        # монетки справа
        ] + [
        '  <g><circle cx="%d" cy="75" r="26" fill="%s" fill-opacity="0.16" stroke="%s" '
        'stroke-opacity="0.6"/><text x="%d" y="86" font-family="%s" font-size="28" '
        'font-weight="700" fill="%s" text-anchor="middle">%s</text></g>'
        % (900 + i * 74, wl['color'], wl['color'], 900 + i * 74, FONT, wl['color'], wl['glyph'])
        for i, wl in enumerate(WALLETS)
        ] + ['</svg>']) + '\n'


def main():
    out_dir = os.path.join(ROOT, 'assets', 'donate')
    os.makedirs(out_dir, exist_ok=True)
    for w in WALLETS:
        path = os.path.join(out_dir, w['slug'] + '.svg')
        open(path, 'w', encoding='utf-8').write(card(w))
        print('svg: assets/donate/%s.svg (%s)' % (w['slug'], w['address']))
    open(os.path.join(ROOT, 'assets', 'donate-banner.svg'), 'w', encoding='utf-8').write(banner())
    print('svg: assets/donate-banner.svg')


if __name__ == '__main__':
    main()
