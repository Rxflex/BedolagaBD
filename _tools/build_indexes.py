# -*- coding: utf-8 -*-
"""Генерирует indexes/*.md из документов docs/**.

Индексы — производные файлы: правки вносятся в docs/, не здесь.
Запуск: python _tools/build_indexes.py
"""
import re
import os
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import ROOT, sections, doc_paths, body_lines, section_of, slug, rel

IDX = 'indexes'
PIPE = chr(92) + '|'
GEN = ('<!-- Сгенерировано: python _tools/build_indexes.py — '
       'правьте документы в docs/, не этот файл -->')

BOLD_RE = re.compile(r'^\s*[-*] [*][*](?P<t>[^*]{3,200})[*][*](?P<rest>.*)$')
H456_RE = re.compile(r'^#{3,6} +(.*)$')
URL_RE = re.compile(r'https?://[^\s)\]}>`,"|]+')
ENV_RE = re.compile(r'\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b')
ID_RE = re.compile(r'\[id=[^\]]+\](?:\((?:https?:)?[^)]*\))?')
DATE_RE = re.compile(r'\d{2}\.\d{2}\.\d{4}')
VERTOK_RE = re.compile(r'v?\d+\.\d+(?:\.\d+)?[a-z0-9+-]*')

PRODUCTS = [
    ('Bedolaga Bot', ('bedolaga bot', 'bedolaga бот', 'bedolaga telegram', 'bedolaga-бот',
                      'бот bedolaga', 'bedolaga v', 'бот (')),
    ('Bedolaga Cabinet', ('cabinet', 'кабинет', 'кабина')),
    ('Remnawave Panel', ('remnawave panel', 'remnawave панель', 'панель remnawave', 'remnawave (панель')),
    ('Remnawave Node', ('нода', 'node')),
    ('Remnawave Admin', ('admin', 'админ')),
    ('Subscription Page', ('subscription', 'сабпейдж', 'сабка')),
    ('Xray-core', ('xray',)),
    ('Клиенты', ('happ', 'incy', 'throne', 'клиент')),
    ('3x-ui / Marzban', ('3x-ui', 'marzban')),
]
PROD_ORDER = [p for p, _ in PRODUCTS] + ['Прочее']

ENV_STOP = {'NET_ADMIN', 'NET_RAW', 'SYS_ADMIN', 'NOT_FOUND', 'READ_ONLY', 'NO_PROXY',
            'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NET_BIND_SERVICE'}


def bar(from_file):
    items = [('⌂ База знаний', rel('README.md', from_file)), ('🗺 Карта', rel('MAP.md', from_file))]
    line = ' · '.join('[%s](%s)' % (t, u) for t, u in items)
    idx = ' · '.join('[%s](%s)' % (n, f) for f, n in
                     [('релизы.md', 'релизы'), ('ошибки.md', 'ошибки'), ('env.md', 'env'),
                      ('термины.md', 'термины'), ('ссылки.md', 'ссылки')])
    return line + ' · Индексы: ' + idx


def clean(text, limit=0):
    out = ID_RE.sub('', text)
    out = re.sub(r'^\s*[:—–-]\s*', '', out).strip()
    out = re.sub(r'\s+', ' ', out)
    if limit and len(out) > limit:
        out = out[:limit - 1].rstrip() + '…'
    return out.replace('|', PIPE)


def product_of(hpath, line=''):
    low = line.lower()
    for name, keys in PRODUCTS:
        if any(k in low for k in keys):
            return name
    for lvl in sorted(hpath, reverse=True):
        txt = hpath[lvl][0].lower()
        for name, keys in PRODUCTS:
            if any(k in txt for k in keys):
                return name
    return 'Прочее'


def where(path, sec, title, hpath, maxlevel=3, from_dir=IDX):
    """Ссылка «раздел › документ › подраздел»."""
    s = section_of(hpath, maxlevel)
    href = rel(path, from_dir + '/x.md')
    label = '%s › %s' % (sec['key'], title)
    if s:
        sub = ID_RE.sub('', s[0]).strip()
        if len(sub) > 46:
            sub = sub[:45].rstrip() + '…'
        return '[%s › %s](%s#%s)' % (label, sub.replace('|', PIPE), href, s[1])
    return '[%s](%s)' % (label, href)


def sort_date(d):
    dd, mm, yy = d.split('.')
    return (yy, mm, dd)


def head(title, lead, emoji=''):
    f = IDX + '/x.md'
    return ['# %s%s' % (emoji + ' ' if emoji else '', title), '', bar(f), '', GEN, '', lead, '']


def write(name, lines):
    while lines and lines[-1].strip() == '':
        lines.pop()
    lines += ['', '---', '', bar(IDX + '/x.md')]
    path = os.path.join(ROOT, IDX, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('индекс:', IDX + '/' + name)


# ------------------------------------------------------------------ релизы
def build_releases():
    rows = []
    for path, sec, title in doc_paths():
        if 'релиз' not in path and 'вехи' not in path and 'кейсы' not in path:
            continue
        for ln, line, infence, hpath in body_lines(path):
            if infence or not line.startswith('- ') or line.startswith('- ['):
                continue
            dm = DATE_RE.search(line[:160])
            vm = VERTOK_RE.search(line[:120])
            if not dm or not vm:
                continue
            label = line[2:]
            bm = re.match(r'^[*][*](?P<t>[^*]{2,80})[*][*]', label)
            ver = bm.group('t') if bm else vm.group(0)
            ver = ID_RE.sub('', ver).strip(' —–-:,')
            ver = re.sub(r'\s*[—–-]\s*\d{2}.*$', '', ver).strip()
            if len(ver) > 60:
                ver = vm.group(0)
            rest = label[bm.end():] if bm else label[vm.end():]
            rows.append((product_of(hpath, line), sort_date(dm.group(0)), dm.group(0),
                         ver, clean(rest, 140), where(path, sec, title, hpath)))
    by_prod = collections.defaultdict(list)
    for r in rows:
        by_prod[r[0]].append(r)
    out = head('Индекс релизов', 'Версия → дата → что поменялось → где описано. Всего **%d записей**.' % len(rows), '🏷')
    out.append('Продукты: ' + ' · '.join('[%s](#%s)' % (p, slug(p)) for p in PROD_ORDER if p in by_prod))
    out.append('')
    for prod in PROD_ORDER:
        if prod not in by_prod:
            continue
        items = sorted(by_prod[prod], key=lambda r: (r[1], r[3]))
        out += ['## %s' % prod, '', '<details open>',
                '<summary><b>%d релизов</b> — развернуть таблицу</summary>' % len(items), '',
                '| Версия | Дата | Что изменилось | Где |', '|---|---|---|---|']
        for _, _, date, ver, rest, w in items:
            out.append('| `%s` | %s | %s | %s |' % (ver, date, rest, w))
        out += ['', '</details>', '']
    write('релизы.md', out)
    return len(rows)


# ------------------------------------------------------------------ ошибки
def build_errors():
    rows = []
    for path, sec, title in doc_paths():
        for ln, line, infence, hpath in body_lines(path):
            if infence:
                continue
            here = ' '.join(v[0].lower() for v in hpath.values()) + ' ' + path.lower()
            if not any(k in here for k in ('ошибк', 'фикс', 'грабли', 'баг')):
                continue
            m = BOLD_RE.match(line)
            hm = H456_RE.match(line)
            if m:
                name, rest = m.group('t'), m.group('rest')
            elif hm and 'id=' in line:
                name, rest = hm.group(1), ''
            elif line.startswith('|') and not re.match(r'^\|[\s:|-]+$', line):
                # в таблицах пайпы внутри пруфов экранированы — по ним не режем
                safe = line.replace(chr(92) + '|', chr(1))
                cells = [c.strip().replace(chr(1), chr(92) + '|')
                         for c in safe.strip('|').split('|')]
                if len(cells) < 2 or cells[0].lower() in ('симптом', 'ошибка', 'проблема', 'дата', 'что', ''):
                    continue
                name = cells[0]
                rest = cells[1]
            elif line.startswith('- ') and 'ошибк' in path.lower():
                # в тематических файлах ошибки записаны обычными пунктами:
                # «симптом — фикс» или «симптом → фикс»
                body = ID_RE.sub('', line[2:]).strip()
                parts = re.split(r'\s+[—→]\s+', body, maxsplit=1)
                name = parts[0]
                rest = parts[1] if len(parts) > 1 else ''
            else:
                continue
            name = ID_RE.sub('', name).strip(' —–-:`')
            if len(name) < 6:
                continue
            if len(name) > 130:
                name = name[:127].rstrip() + '…'
            rows.append((sec['key'], sec, title, path, name.replace('|', PIPE),
                         clean(rest, 150), where(path, sec, title, hpath)))
    by_sec = collections.defaultdict(list)
    for r in rows:
        by_sec[r[0]].append(r)
    out = head('Индекс ошибок → фиксов',
               'Симптом → куда смотреть. **%d записей** из всех разделов «Ошибки → фиксы», «Грабли», «Баги».' % len(rows), '🩺')
    out.append('Разделы: ' + ' · '.join('[%s %s](#%s-%s)' % (s['emoji'], s['name'], s['key'], slug(s['name']))
                                        for s in sections() if s['key'] in by_sec))
    out.append('')
    for s in sections():
        if s['key'] not in by_sec:
            continue
        items = by_sec[s['key']]
        out += ['## %s %s' % (s['key'], s['name']), '', '<details open>',
                '<summary><b>%d записей</b></summary>' % len(items), '',
                '| Симптом / ошибка | Фикс (кратко) | Где |', '|---|---|---|']
        for _, _, _, _, name, fix, w in items:
            out.append('| %s | %s | %s |' % (name, fix, w))
        out += ['', '</details>', '']
    write('ошибки.md', out)
    return len(rows)


# ------------------------------------------------------------------ env
def build_env():
    places = collections.defaultdict(list)
    counts = collections.Counter()
    for path, sec, title in doc_paths():
        for ln, line, infence, hpath in body_lines(path):
            for var in set(ENV_RE.findall(line)):
                if var in ENV_STOP or len(var) < 6:
                    continue
                counts[var] += 1
                w = where(path, sec, title, hpath)
                if w not in places[var]:
                    places[var].append(w)
    groups = collections.defaultdict(list)
    for var in sorted(places):
        groups[var[0]].append(var)
    out = head('Индекс env-переменных',
               '**%d переменных** окружения (бот, кабинет, панель, платёжки, инфра) — и где каждая описана.' % len(places), '🔧')
    out.append('Буквы: ' + ' · '.join('[%s](#%s)' % (g, g.lower()) for g in sorted(groups)))
    out.append('')
    for g in sorted(groups):
        out += ['## %s' % g, '', '<details>',
                '<summary><b>%d переменных</b></summary>' % len(groups[g]), '',
                '| Переменная | Упом. | Где |', '|---|---|---|']
        for var in groups[g]:
            links = ' · '.join(places[var][:3])
            if len(places[var]) > 3:
                links += ' · …'
            out.append('| `%s` | %d | %s |' % (var, counts[var], links))
        out += ['', '</details>', '']
    write('env.md', out)
    return len(places)


# ------------------------------------------------------------------ ссылки
def build_links():
    info = {}
    for path, sec, title in doc_paths():
        for ln, line, infence, hpath in body_lines(path):
            for url in URL_RE.findall(line):
                url = url.rstrip('.,;:)>')
                if (url.startswith('https://your-') or 'example.com' in url
                        or 'domain.com' in url or 'localhost' in url
                        or url.startswith('https://t.me/c/')):
                    continue
                e = info.setdefault(url, {'count': 0, 'where': []})
                e['count'] += 1
                w = where(path, sec, title, hpath)
                if w not in e['where']:
                    e['where'].append(w)

    def group_of(u):
        if 'github.com' in u or 'githubusercontent' in u or 'ghcr.io' in u:
            return ('🐙 GitHub: репозитории и релизы', 1)
        if 't.me' in u or 'telegram' in u:
            return ('✈ Telegram: каналы, боты, чаты', 3)
        if any(k in u for k in ('docs.', 'wiki', '/docs', 'xtls.github.io', 'remna.st')):
            return ('📚 Документация', 2)
        return ('🔗 Сервисы и прочее', 4)

    groups = collections.defaultdict(list)
    order = {}
    for u in info:
        g, o = group_of(u)
        groups[g].append(u)
        order[g] = o
    out = head('Индекс ссылок', '**%d внешних ссылок** из базы, без дублей, сгруппированы по типу.' % len(info), '🔗')
    for g in sorted(groups, key=lambda x: order[x]):
        out += ['## %s' % g, '', '<details>',
                '<summary><b>%d ссылок</b></summary>' % len(groups[g]), '',
                '| Ссылка | Упом. | Где |', '|---|---|---|']
        for u in sorted(groups[g], key=lambda x: (-info[x]['count'], x)):
            w = ' · '.join(info[u]['where'][:2])
            if len(info[u]['where']) > 2:
                w += ' · …'
            out.append('| <%s> | %d | %s |' % (u, info[u]['count'], w))
        out += ['', '</details>', '']
    write('ссылки.md', out)
    return len(info)


if __name__ == '__main__':
    stats = {'релизы': build_releases(), 'ошибки': build_errors(),
             'env': build_env(), 'ссылки': build_links()}
    print('итого:', stats)
