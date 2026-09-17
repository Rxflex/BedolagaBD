# -*- coding: utf-8 -*-
"""Разбивает монолитные документы 01..08 на тематические файлы в docs/<раздел>/.

Разбиение lossless: каждая непустая строка исходника попадает ровно в один
целевой файл (проверяется в конце по многомножеству строк).

Запуск: python _tools/split_docs.py
"""
import re
import os
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kb_lib import slug

SRC = {
    '01': '01-панели.md',
    '02': '02-ноды-транспорты.md',
    '03': '03-обход-блокировок.md',
    '04': '04-сеть-серверы.md',
    '05': '05-хостинги.md',
    '06': '06-платёжки-бизнес.md',
    '07': '07-скрипты-инструменты.md',
    '08': '08-события-хронология.md',
}

DIRS = {
    '01': 'docs/01-панели',
    '02': 'docs/02-транспорты',
    '03': 'docs/03-обход-тспу',
    '04': 'docs/04-сеть-серверы',
    '05': 'docs/05-хостинги',
    '06': 'docs/06-платёжки',
    '07': 'docs/07-скрипты',
    '08': 'docs/08-хронология',
}

# --- 01: раздел внутри периода -> файл -------------------------------------
MAP01 = {
    'Релизы (хронология)': ('релизы.md', 'Релизы панелей, бота и кабинета — по периодам'),
    'Установка и обновление': ('установка-обновление.md', 'Установка и обновление — по периодам'),
    'Docker-compose': ('docker-compose.md', 'Docker-compose: рабочие файлы — по периодам'),
    'Env': ('env.md', 'Env-переменные — по периодам'),
    'Ошибки → фиксы': ('ошибки-фиксы.md', 'Ошибки → фиксы (панели, бот, кабинет)'),
    'Marzban / 3x-ui': ('marzban-3x-ui.md', 'Marzban и 3x-ui: миграции и опыт'),
    'Admin-панели': ('admin-панели.md', 'Admin-панели и внешние дашборды'),
    'Ссылки и инструменты': ('ссылки-инструменты.md', 'Ссылки и инструменты (панельные)'),
    'Nginx/Caddy': ('reverse-proxy.md', 'Nginx / Caddy для панели, бота и кабинета'),
    'Caddy кабинета': ('reverse-proxy.md', 'Nginx / Caddy для панели, бота и кабинета'),
    'Важные конфиги и настройки': ('конфиги-настройки.md', 'Важные конфиги и настройки панели'),
    'Remnawave / Bedolaga: обновления, баги, кейсы': ('кейсы.md', 'Кейсы: обновления, баги, разборы'),
}

# --- 02..08: H2-раздел (по порядку) -> (файл, заголовок) -------------------
MAP_H2 = {
    '02': [
        ('reality.md', 'VLESS + Reality (TCP/raw)'),
        ('selfsteal.md', 'Selfsteal (свой SNI)'),
        ('sni-fingerprint.md', 'SNI-подбор и fingerprint'),
        ('xhttp.md', 'XHTTP (+ selfsni)'),
        ('grpc.md', 'gRPC'),
        ('websocket.md', 'WebSocket (WS + TLS)'),
        ('hysteria2.md', 'Hysteria2'),
        ('trojan.md', 'Trojan'),
        ('shadowsocks.md', 'Shadowsocks, SS-2022, мосты RU→EU'),
        ('мультитранспорт-порты.md', 'Многотранспортные ноды и порты'),
        ('роутинг.md', 'Роутинг: серверный и клиентский'),
        ('балансеры.md', 'Балансеры leastLoad / leastPing'),
        ('клиенты.md', 'Клиенты: Happ, INCY, Throne, mihomo, sing-box'),
        ('ошибки-фиксы.md', 'Ошибки → фиксы (транспорты)'),
        ('вехи.md', 'Вехи транспортов'),
    ],
    '04': [
        ('sysctl-bbr-mtu.md', 'Ядро: sysctl, BBR, IPv6, MTU'),
        ('шейпинг.md', 'Ограничение скорости и шейпинг'),
        ('firewall-ddos.md', 'iptables / nftables / XDP / анти-DDoS'),
        ('reverse-proxy.md', 'Реверс-прокси: Caddy, Nginx, HAProxy, Traefik'),
        ('сертификаты.md', 'Сертификаты'),
        ('dns.md', 'DNS'),
        ('docker.md', 'Docker-сети и compose'),
        ('мониторинг.md', 'Мониторинг'),
        ('бэкапы.md', 'Бэкапы и restore'),
        ('ssh-доступ.md', 'Порты, SSH, доступ'),
        ('тспу-серверное.md', 'ТСПУ и БС: серверная механика'),
        ('вехи.md', 'Вехи (сеть и серверы)'),
    ],
    '05': [
        ('хронология.md', 'Хронология вех по хостингам'),
        ('правила-выбора.md', 'Базовые правила выбора хостера'),
        ('рф-хостеры.md', 'Российские хостеры и облака'),
        ('зарубежные-хостеры.md', 'Зарубежные хостеры (Европа)'),
        ('страны-локации.md', 'Страны для нод: что работало когда'),
        ('мосты.md', 'Мосты RU→EU и каскады'),
        ('тспу-регионы.md', 'ТСПУ-политика по регионам и операторам'),
        ('sni-бс.md', 'SNI для БС (практика)'),
        ('ёмкость-нод.md', 'Ёмкость нод и требования к серверам'),
        ('экономика.md', 'Экономика: платёжки и комиссии'),
        ('тесты-vps.md', 'Инструменты проверки локаций и подсетей'),
        ('боты-сервисы.md', 'Боты и сервисы проверки'),
        ('asn.md', 'Список ASN'),
        ('бс-подсети.md', 'Полные списки подсетей БС'),
        ('рынок-подсетей.md', 'Рынок продажи БС-подсетей и аккаунтов'),
        ('прочее.md', 'Прочее по теме хостингов'),
    ],
    '06': [
        ('комиссии.md', 'Сводная таблица комиссий'),
        ('env-вебхуки.md', 'Env-конфиги и вебхуки платёжек'),
        ('профили-платёжек.md', 'Профили платёжек: кто есть кто'),
        ('юнит-экономика.md', 'Ценообразование подписок и юнит-экономика'),
        ('право-рф.md', 'Правовой статус VPN в РФ'),
        ('юкасса.md', 'ЮKassa и легальные кассы'),
        ('экономика-хостинга.md', 'Экономика хостинга и CDN'),
        ('вехи.md', 'Вехи экономики и платёжек'),
        ('риски-скам.md', 'Риски, скам-истории, выводы'),
        ('cdn-биллинг.md', 'CDN, биллинг и платёжный контекст'),
        ('тезисы.md', 'Тезисы для выживания'),
    ],
    '07': [
        ('экосистема.md', 'Официальная экосистема Remnawave / Bedolaga'),
        ('установщики.md', 'Установочные скрипты'),
        ('решала-защита.md', 'Решала (DonMatteoVPN) и защита'),
        ('мониторинг.md', 'Мониторинг'),
        ('warp-psiphon.md', 'WARP / Psiphon'),
        ('чекеры.md', 'Чекеры, тесты, бенчмарки'),
        ('роутинг-генераторы.md', 'Роутинг-генераторы и geo-правила'),
        ('боты-помощники.md', 'Боты-помощники и самописные'),
        ('mtproto.md', 'MTProto (telemt)'),
        ('налоги.md', 'Налоги, НалоGO, чеки'),
        ('api.md', 'API-фишки Remnawave и Bedolaga'),
        ('ошибки-фиксы.md', 'Ошибки и их фиксы (самое частое)'),
        ('секреты.md', 'Генерация секретов'),
        ('итоги.md', 'Итоговое состояние на 23.08.2026'),
    ],
}

# --- 03: тема (H3 в части A/B) -> файл ------------------------------------
MAP03 = [
    ('хронология.md', 'Хронология блокировок и вех',
     ['Хронология блокировок и вехи', 'Хронология вех (продолжение)', 'События (12.08-23.08.2026)']),
    ('бс-подсети.md', 'БС (белые списки): механика и подсети',
     ['БС (белые списки)', 'БС-механика (обновление', 'Селектел / подсети на продажу']),
    ('cdn-фронтинг.md', 'CDN-фронтинг: Yandex, Beeline, VK, Selectel, MWS',
     ['CDN-фронтинг (Yandex', 'CDN-фронтинг по операторам']),
    ('мосты.md', 'Мосты RU→EU и каскады',
     ['Мосты (ru→eu) и каскады', 'Мосты ru→eu (продолжение)']),
    ('warp.md', 'WARP, Cloudflare, NaiveProxy',
     ['WARP / Cloudflare / NaiveProxy', 'WARP (продолжение)']),
    ('детект-fingerprint.md', 'Детект: uTLS, fingerprint, TLS-in-TLS',
     ['Детект uTLS / fingerprint / TLS-in-TLS', 'Детект uTLS / fingerprint / TLS-in-TLS (обновление']),
    ('dns.md', 'DNS-трюки', ['DNS-трюки']),
    ('методы-обхода.md', 'Работающие методы обхода',
     ['Устойчивые методы', 'Обходы (новое', 'Finalmask-транспорты']),
    ('чекеры.md', 'Чекеры ТСПУ/БС и инструменты',
     ['Чекеры ТСПУ/БС', 'Инструменты и ссылки']),
    ('правовое.md', 'Правовое',
     ['Правовое', 'Правовое (06-08.2026)']),
    ('экономика.md', 'Экономика: хостинг, платёжки, рынок услуг',
     ['Экономика (комиссии', 'Хостинг: цены и опыт', 'Платёжки (комиссии/выводы', 'Рынок услуг (август 2026)']),
    ('релизы-вехи.md', 'Релизы Remnawave / Bedolaga как вехи обхода',
     ['Remnawave / Bedolaga релизы 2025', 'Remnawave / Bedolaga релизы 06.2026', 'Remnawave 3.0 (Breaking change)',
      'Утечка уязвимости сабпейджа Remnawave']),
    ('итоги.md', 'Состояние обхода на 23.08.2026',
     ['Состояние обхода на 23.08.2026']),
]

MONTHS = {'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04', 'май': '05', 'июнь': '06',
          'июль': '07', 'август': '08', 'сентябрь': '09', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'}


def read_body(path):
    """Строки документа без H1, подзаголовка и служебных KB-блоков."""
    lines = open(path, encoding='utf-8').read().split('\n')
    out, skip, infence = [], False, False
    for l in lines:
        s = l.strip()
        if s.startswith('<!-- KB:'):
            skip = True
            continue
        if s.startswith('<!-- /KB:'):
            skip = False
            continue
        if skip:
            continue
        out.append(l)
    # отрезаем всё до первого H2 (заголовок + подзаголовок + разделители)
    intro, body = [], []
    started = False
    for l in out:
        if not started and re.match(r'^## ', l):
            started = True
        (body if started else intro).append(l)
    return intro, body


def blocks(body, level):
    """Разбивает поток на блоки по заголовкам заданного уровня: [(title, lines)]."""
    res, cur, infence = [], None, False
    for l in body:
        if l.startswith('```'):
            infence = not infence
        if not infence:
            m = re.match(r'^#{%d} +(.*?)\s*$' % level, l)
            if m and not re.match(r'^#{%d} ' % (level + 1), l):
                cur = (m.group(1), [])
                res.append(cur)
                continue
        if cur is not None:
            cur[1].append(l)
    return res


def shift(lines, delta):
    """Сдвигает уровни заголовков вне блоков кода."""
    out, infence = [], False
    for l in lines:
        if l.startswith('```'):
            infence = not infence
            out.append(l)
            continue
        m = re.match(r'^(#{1,6}) +(.*)$', l)
        if m and not infence:
            lvl = max(2, len(m.group(1)) + delta)
            out.append('#' * lvl + ' ' + m.group(2))
        else:
            out.append(l)
    return out


def trim(lines):
    while lines and lines[0].strip() == '':
        lines.pop(0)
    while lines and lines[-1].strip() == '':
        lines.pop()
    return lines


def collect():
    """Возвращает {relpath: {'title':..., 'parts':[(подзаголовок|None, lines)]}}"""
    files = collections.OrderedDict()

    def add(relpath, title, sub, lines, order=None):
        e = files.setdefault(relpath, {'title': title, 'parts': [], 'order': order})
        e['parts'].append((sub, lines))

    # ---- 01: периоды x разделы
    intro01, body01 = read_body(SRC['01'])
    for period, plines in blocks(body01, 2):
        for sec, slines in blocks(plines, 3):
            name = re.sub(r'\s*·\s*[^·]*$', '', sec).strip()
            if name not in MAP01:
                raise SystemExit('01: неизвестный раздел %r' % sec)
            fname, title = MAP01[name]
            add('01/' + fname, title, period, shift(trim(slines), -1))

    # ---- 02, 04..07: H2 -> файл
    for key in ('02', '04', '05', '06', '07'):
        intro, body = read_body(SRC[key])
        bl = blocks(body, 2)
        spec = MAP_H2[key]
        if len(bl) != len(spec):
            raise SystemExit('%s: разделов %d, в карте %d' % (key, len(bl), len(spec)))
        for (src_title, lines), (fname, title) in zip(bl, spec):
            add(key + '/' + fname, title, None, shift(trim(lines), -1))

    # ---- 03: части A/B -> темы
    intro, body = read_body(SRC['03'])
    theme_to_file = {}
    for fname, title, keys in MAP03:
        for k in keys:
            theme_to_file[k] = (fname, title)
    for part, plines in blocks(body, 2):
        part_tag = 'Часть A' if 'Часть A' in part else 'Часть B'
        for sec, slines in blocks(plines, 3):
            hit = None
            for k, v in theme_to_file.items():
                if sec.startswith(k):
                    if hit is None or len(k) > len(hit[0]):
                        hit = (k, v)
            if not hit:
                raise SystemExit('03: не размечен раздел %r' % sec)
            fname, title = hit[1]
            add('03/' + fname, title, '%s · %s' % (sec, part_tag), shift(trim(slines), -1))

    # ---- 08: месяцы -> файлы
    intro, body = read_body(SRC['08'])
    for month, mlines in blocks(body, 2):
        m = re.match(r'^(\S+)\s+(\d{4})$', month.strip())
        if not m:
            raise SystemExit('08: не разобран месяц %r' % month)
        name, year = m.group(1).lower(), m.group(2)
        fname = '%s-%s.md' % (year, MONTHS[name])
        add('08/' + fname, month.strip().capitalize(), None, shift(trim(mlines), -1))

    return files


def source_lines_of(path):
    _, body = read_body(path)
    return [l for l in body if l.strip()]


def main():
    files = collect()
    written = {}
    for rel, e in files.items():
        key, fname = rel.split('/')
        outdir = DIRS[key]
        os.makedirs(outdir, exist_ok=True)
        lines = ['# ' + e['title'], '']
        src_lines = []
        multi = len(e['parts']) > 1
        for sub, plines in e['parts']:
            if sub and (multi or key in ('01', '03')):
                lines += ['## ' + sub, '']
            body = trim(list(plines))
            lines += body + ['']
            src_lines += [l for l in body if l.strip()]
        path = os.path.join(outdir, fname)
        open(path, 'w', encoding='utf-8').write('\n'.join(trim(lines)) + '\n')
        written[path] = src_lines

    # ---- проверка: ни одна строка не потеряна и не размножена
    out_counter = collections.Counter()
    for path, src in written.items():
        for l in src:
            out_counter[re.sub(r'^#+ ', '', l).strip()] += 1
    src_counter = collections.Counter()
    for key, path in SRC.items():
        for l in source_lines_of(path):
            src_counter[re.sub(r'^#+ ', '', l).strip()] += 1
    lost = src_counter - out_counter
    extra = out_counter - src_counter
    print('файлов создано: %d' % len(written))
    print('строк в исходниках: %d, в результате: %d' % (sum(src_counter.values()), sum(out_counter.values())))
    if lost:
        print('ПОТЕРЯНО %d строк, примеры:' % sum(lost.values()))
        for l, n in list(lost.items())[:15]:
            print('   -', n, l[:120])
    if extra:
        print('ЛИШНЕЕ %d строк, примеры:' % sum(extra.values()))
        for l, n in list(extra.items())[:15]:
            print('   +', n, l[:120])
    if not lost and not extra:
        print('OK: контент перенесён без потерь')


if __name__ == '__main__':
    main()
