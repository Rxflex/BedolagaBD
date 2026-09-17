# -*- coding: utf-8 -*-
"""Генерирует SVG-графику базы: главный баннер, шапку карты, баннеры разделов.

Запуск: python _tools/build_assets.py
Диаграммы в assets/diagrams/ рисуются руками и здесь не перезаписываются.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT, sections, stats

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
BG1, BG2 = '#161b22', '#0d1117'
FG, DIM = '#e6edf3', '#8b949e'


def defs(accent, grid=28):
    return """  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0.15"/>
    </linearGradient>
    <pattern id="grid" width="{grid}" height="{grid}" patternUnits="userSpaceOnUse">
      <path d="M {grid} 0 H 0 V {grid}" fill="none" stroke="#ffffff" stroke-opacity="0.04"/>
    </pattern>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>""".format(bg1=BG1, bg2=BG2, accent=accent, grid=grid)


def frame(w, h, accent, r=16):
    return ('  <rect width="%d" height="%d" rx="%d" fill="url(#bg)"/>\n'
            '  <rect width="%d" height="%d" rx="%d" fill="url(#grid)"/>\n'
            '  <rect width="%d" height="%d" rx="%d" fill="none" stroke="%s" stroke-opacity="0.35"/>'
            % (w, h, r, w, h, r, w, h, r, accent))


def nodes(cx, cy, accent, spread=1.0, seed=(0, 1, 2)):
    """Декоративный граф нод."""
    pts = [(-150, -46), (-70, 18), (0, -60), (60, 30), (135, -18), (30, -110), (-110, 84), (150, 70)]
    pts = [(cx + x * spread, cy + y * spread) for x, y in pts]
    out = []
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        out.append('  <line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s" stroke-opacity="0.28" stroke-width="1.2"/>'
                   % (x1, y1, x2, y2, accent))
    for i, (x, y) in enumerate(pts):
        r = 5 if i % 3 else 8
        out.append('  <circle cx="%.0f" cy="%.0f" r="%d" fill="%s" fill-opacity="%.2f"/>'
                   % (x, y, r, accent, 0.85 if i % 3 else 0.55))
    return '\n'.join(out)


def text(x, y, s, size, fill, weight='400', anchor='start', family=FONT, opacity=1.0, spacing=None):
    sp = ' letter-spacing="%s"' % spacing if spacing else ''
    return ('  <text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s" '
            'fill-opacity="%s" text-anchor="%s"%s>%s</text>'
            % (x, y, family, size, weight, fill, opacity, anchor, sp, esc(s)))


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def pill(x, y, label, value, accent, w=196):
    return '\n'.join([
        '  <g>',
        '    <rect x="%d" y="%d" width="%d" height="64" rx="12" fill="#ffffff" fill-opacity="0.04" '
        'stroke="%s" stroke-opacity="0.35"/>' % (x, y, w, accent),
        text(x + 16, y + 28, value, 22, FG, '700'),
        text(x + 16, y + 50, label, 13, DIM, '400', spacing='0.5'),
        '  </g>',
    ])


def write(path, body):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(body)
    print('svg:', path)


def kb_stats():
    tot = {'docs': 0, 'lines': 0, 'proofs': 0, 'code': 0}
    for s in sections():
        for f, t, b in s['files']:
            st = stats(s['dir'] + '/' + f)
            tot['docs'] += 1
            tot['lines'] += st['lines']
            tot['proofs'] += st['proofs']
            tot['code'] += st['code']
    return tot


def badge(slug, label, value, color):
    """Локальный бейдж в стиле shields, но без внешних зависимостей."""
    lw = 7.2 * len(label) + 20
    vw = 7.6 * len(value) + 20
    w, h = lw + vw, 22
    body = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %d" width="%.0f" height="%d" '
        'role="img" aria-label="%s: %s">' % (w, h, w, h, esc(label), esc(value)),
        '  <defs><clipPath id="r"><rect width="%.0f" height="%d" rx="4" fill="#fff"/></clipPath></defs>' % (w, h),
        '  <g clip-path="url(#r)">',
        '    <rect width="%.0f" height="%d" fill="#30363d"/>' % (lw, h),
        '    <rect x="%.0f" width="%.0f" height="%d" fill="%s"/>' % (lw, vw, h, color),
        '  </g>',
        text(lw / 2, 15, label, 11.5, '#e6edf3', '500', 'middle'),
        text(lw + vw / 2, 15, value, 11.5, '#0d1117', '700', 'middle'),
        '</svg>',
    ]
    write('assets/badges/%s.svg' % slug, '\n'.join(body) + '\n')


def badges():
    st = kb_stats()
    badge('license-kb', 'база', 'CC BY-SA 4.0', '#06d6a0')
    badge('license-tools', '_tools', 'MIT', '#7c8cff')
    badge('docs', 'документов', str(st['docs']), '#4ecdc4')
    badge('proofs', 'пруфов', '{:,}'.format(st['proofs']).replace(',', ' '), '#ffd166')
    badge('period', 'период', '08.2025 → 08.2026', '#f78c6b')


def deepwiki():
    """Крупная плашка-CTA: спросить ИИ по этой базе на DeepWiki."""
    w, h, accent = 1200, 150, '#4ecdc4'
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="Спросить ИИ по этой базе на DeepWiki">' % (w, h, w, h),
        defs(accent, 24),
        frame(w, h, accent),
        '  <ellipse cx="1040" cy="75" rx="300" ry="150" fill="url(#glow)"/>',
        # облачко диалога
        '  <g transform="translate(52 38)">',
        '    <rect width="74" height="58" rx="14" fill="%s" fill-opacity="0.16" '
        'stroke="%s" stroke-opacity="0.65"/>' % (accent, accent),
        '    <path d="M20 58 L20 74 L38 58 Z" fill="%s" fill-opacity="0.16" '
        'stroke="%s" stroke-opacity="0.65"/>' % (accent, accent),
        '    <circle cx="24" cy="29" r="4.5" fill="%s"/>' % accent,
        '    <circle cx="37" cy="29" r="4.5" fill="%s"/>' % accent,
        '    <circle cx="50" cy="29" r="4.5" fill="%s"/>' % accent,
        '  </g>',
        text(152, 56, 'DEEPWIKI', 15, accent, '700', spacing='4.2'),
        text(150, 96, 'Спросите ИИ по этой базе', 30, FG, '800'),
        text(152, 124, 'deepwiki.com/Rxflex/BedolagaBD · агент прочитал все 108 документов '
                       'и ссылается на них в ответах', 14.5, DIM),
        # кнопка-стрелка
        '  <g transform="translate(990 52)">',
        '    <rect width="166" height="46" rx="23" fill="%s" fill-opacity="0.18" '
        'stroke="%s" stroke-opacity="0.7"/>' % (accent, accent),
        text(26, 29, 'Задать вопрос', 15, FG, '700'),
        '    <path d="M132 23 h12 m-5 -5 l5 5 l-5 5" fill="none" stroke="%s" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % accent,
        '  </g>',
        '</svg>',
    ]
    write('assets/deepwiki.svg', '\n'.join(parts) + '\n')


def banner():
    w, h, accent = 1200, 380, '#7c8cff'
    st = kb_stats()
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="База знаний Bedolaga Social Club">' % (w, h, w, h),
             defs(accent), frame(w, h, accent),
             '  <ellipse cx="1010" cy="120" rx="330" ry="220" fill="url(#glow)"/>',
             nodes(985, 150, accent, 1.15),
             '  <rect x="56" y="58" width="4" height="86" rx="2" fill="%s"/>' % accent,
             text(80, 88, 'BEDOLAGA SOCIAL CLUB', 20, accent, '700', spacing='3.2'),
             text(78, 148, 'База знаний', 62, FG, '800'),
             text(78, 190, 'Remnawave · Bedolaga · Xray · обход ТСПУ · VPN-бизнес под РФ', 21, DIM),
             text(78, 222, '23.08.2025 → 23.08.2026 · 788 000 сообщений чата → 172 заметки → %d документов' % st['docs'], 16, DIM, opacity=0.85),
             pill(78, 258, 'документов', str(st['docs']), accent, 170),
             pill(262, 258, 'строк знаний', '{:,}'.format(st['lines']).replace(',', ' '), accent, 190),
             pill(466, 258, 'пруф-ссылок', '{:,}'.format(st['proofs']).replace(',', ' '), accent, 190),
             pill(670, 258, 'блоков кода', str(st['code']), accent, 180),
             pill(864, 258, 'заметок-первоисточников', '172', accent, 258),
             text(w - 28, h - 22, 'knowledge base · v2', 13, DIM, family=MONO, anchor='end', opacity=0.6),
             '</svg>']
    write('assets/banner.svg', '\n'.join(parts) + '\n')


def map_header():
    w, h, accent = 1200, 180, '#8ecae6'
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Карта базы знаний">' % (w, h, w, h),
             defs(accent, 24), frame(w, h, accent),
             '  <ellipse cx="1060" cy="90" rx="240" ry="150" fill="url(#glow)"/>',
             nodes(1020, 90, accent, 0.72),
             text(56, 78, 'КАРТА', 18, accent, '700', spacing='4'),
             text(54, 128, 'Все разделы базы знаний', 40, FG, '800'),
             '</svg>']
    write('assets/map.svg', '\n'.join(parts) + '\n')


def section_banner(sec):
    w, h = 1200, 210
    accent = sec['color']
    blurb = sec['blurb']
    if len(blurb) > 92:
        blurb = blurb[:89].rstrip() + '…'
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">' % (w, h, w, h, esc(sec['name'])),
             defs(accent, 26), frame(w, h, accent),
             '  <ellipse cx="1040" cy="105" rx="260" ry="170" fill="url(#glow)"/>',
             nodes(1010, 105, accent, 0.78),
             '  <rect x="0" y="0" width="7" height="%d" rx="3.5" fill="%s"/>' % (h, accent),
             text(1000, 196, sec['key'], 190, accent, '800', anchor='middle', opacity=0.10),
             text(48, 62, 'РАЗДЕЛ %s' % sec['key'], 15, accent, '700', spacing='3.4'),
             text(46, 118, sec['name'], 46, FG, '800'),
             text(48, 156, blurb, 19, DIM),
             text(48, 186, 'Bedolaga Social Club · база знаний', 13, DIM, family=MONO, opacity=0.55),
             '</svg>']
    write('assets/sections/%s.svg' % sec['key'], '\n'.join(parts) + '\n')


if __name__ == '__main__':
    deepwiki()
    badges()
    banner()
    map_header()
    for s in sections():
        section_banner(s)
