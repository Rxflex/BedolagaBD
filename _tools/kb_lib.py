# -*- coding: utf-8 -*-
"""Спека структуры базы знаний + примитивы для генераторов.

Здесь описано ВСЁ дерево: разделы, порядок файлов, человеческие названия,
цвета и иконки. Генераторы (build_nav / build_indexes / check_links)
не знают ничего, кроме этой спеки.
"""
import re
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# key, папка, имя, эмодзи, акцентный цвет, краткое описание
SECTIONS = [
    {
        'key': '01', 'dir': 'docs/01-панели', 'name': 'Панели', 'emoji': '🛠',
        'color': '#7c8cff',
        'blurb': 'Remnawave, Bedolaga-бот, Cabinet, admin-панели, миграции с Marzban и 3x-ui',
        'files': [
            ('релизы.md', 'Релизы', 'каталог версий Bedolaga v2.0.4→v4.1.0, Cabinet 1.1→1.65, Remnawave 2.1.9→3.3.0'),
            ('установка-обновление.md', 'Установка и обновление', 'команды, порядок поднятия, миграции, откаты'),
            ('docker-compose.md', 'Docker-compose', 'рабочие compose-файлы бота, панели, кабинета, сабпейджа'),
            ('env.md', 'Env-переменные', 'дословные .env по периодам: бот, кабинет, панель, платёжки'),
            ('reverse-proxy.md', 'Nginx / Caddy', 'реверс для панели, вебхуков, миниаппы, кабинета'),
            ('конфиги-настройки.md', 'Конфиги и настройки', 'Burst Observatory, XHTTP-inject, Rich Menu, логи нод'),
            ('ошибки-фиксы.md', 'Ошибки → фиксы', '~150 разобранных поломок: миграции, вебхуки, кабинет, панель'),
            ('admin-панели.md', 'Admin-панели', 'remnawave-admin, вебадминка бота, дашборды, плагины'),
            ('кейсы.md', 'Кейсы и разборы', 'живые разборы обновлений и багов'),
            ('marzban-3x-ui.md', 'Marzban и 3x-ui', 'миграции, сравнение, остатки старого стека'),
            ('ссылки-инструменты.md', 'Ссылки и инструменты', 'репозитории экосистемы, документация, утилиты'),
        ],
    },
    {
        'key': '02', 'dir': 'docs/02-транспорты', 'name': 'Транспорты', 'emoji': '🔌',
        'color': '#4ecdc4',
        'blurb': 'Xray-конфиги дословно: Reality, XHTTP, gRPC, WS, Hysteria2, Trojan, SS-2022, клиенты',
        'files': [
            ('reality.md', 'VLESS + Reality', 'базовый рецепт инбаунда, xver, shortIds, destOverride'),
            ('xhttp.md', 'XHTTP', 'главный рецепт с 11.2025: selfsni, режимы, padding'),
            ('selfsteal.md', 'Selfsteal', 'свой SNI: как поднять и чем накрыть'),
            ('sni-fingerprint.md', 'SNI и fingerprint', 'подбор SNI, uTLS-отпечатки, что горело по датам'),
            ('grpc.md', 'gRPC', 'конфиг, multiMode, когда выигрывает'),
            ('websocket.md', 'WebSocket + TLS', 'ws-инбаунд под CDN и реверс'),
            ('hysteria2.md', 'Hysteria2', 'UDP-транспорт: конфиг, обфускация, лимиты'),
            ('trojan.md', 'Trojan', 'конфиг и место в схеме'),
            ('shadowsocks.md', 'Shadowsocks / SS-2022', 'мосты RU→EU, 2022-blake3, цепочки'),
            ('мультитранспорт-порты.md', 'Мультитранспорт и порты', 'несколько инбаундов на ноде, разводка портов'),
            ('роутинг.md', 'Роутинг', 'серверные и клиентские правила, domainStrategy'),
            ('балансеры.md', 'Балансеры', 'leastLoad / leastPing, observatory, health-checks'),
            ('клиенты.md', 'Клиенты', 'Happ, INCY, Throne, mihomo, sing-box, v2rayN'),
            ('ошибки-фиксы.md', 'Ошибки → фиксы', 'типовые поломки транспортов и лечение'),
            ('вехи.md', 'Вехи', 'что и когда отваливалось по транспортам'),
        ],
    },
    {
        'key': '03', 'dir': 'docs/03-обход-тспу', 'name': 'Обход ТСПУ', 'emoji': '🛡',
        'color': '#ff6b6b',
        'blurb': 'Блокировки по датам, ТСПУ-механика, CDN-фронтинг, БС-подсети, мосты, детект',
        'files': [
            ('хронология.md', 'Хронология блокировок', 'что отвалилось и когда — год по датам'),
            ('методы-обхода.md', 'Работающие методы', 'устойчивые схемы, новинки 2026, finalmask (SSH/DNS/XMC)'),
            ('cdn-фронтинг.md', 'CDN-фронтинг', 'Yandex, Beeline/CDNVideo, VK, Selectel, MWS — с конфигами'),
            ('бс-подсети.md', 'БС (белые списки)', 'механика белых подсетей, кто их даёт, как проверять'),
            ('мосты.md', 'Мосты RU→EU', 'каскады, пары «вход в РФ → выход в ЕС»'),
            ('warp.md', 'WARP и Cloudflare', 'wgcf, NaiveProxy, когда помогает'),
            ('детект-fingerprint.md', 'Детект и fingerprint', 'uTLS, TLS-in-TLS, отпечатки по датам'),
            ('dns.md', 'DNS-трюки', 'DoH/DoT, подмены, фильтрация'),
            ('чекеры.md', 'Чекеры ТСПУ/БС', 'инструменты проверки блокировок и подсетей'),
            ('релизы-вехи.md', 'Релизы как вехи', 'Remnawave 3.0, утечка сабпейджа и прочие переломы'),
            ('экономика.md', 'Экономика обхода', 'сколько стоит держать схему живой'),
            ('правовое.md', 'Правовое', 'что происходило в законах и практике'),
            ('итоги.md', 'Итог на 23.08.2026', 'состояние обхода на конец архива'),
        ],
    },
    {
        'key': '04', 'dir': 'docs/04-сеть-серверы', 'name': 'Сеть и серверы', 'emoji': '🖧',
        'color': '#ffd166',
        'blurb': 'sysctl/BBR, шейпинг, firewall и анти-DDoS, реверс-прокси, сертификаты, бэкапы',
        'files': [
            ('sysctl-bbr-mtu.md', 'sysctl, BBR, MTU', 'полные наборы тюнинга ядра для нод'),
            ('шейпинг.md', 'Шейпинг', 'ограничение скорости, tc, честная раздача'),
            ('firewall-ddos.md', 'Firewall и анти-DDoS', 'iptables/nftables, hashlimit, ipset, XDP, fail2ban'),
            ('reverse-proxy.md', 'Реверс-прокси', 'Caddy, Nginx, HAProxy, Traefik — конфиги дословно'),
            ('сертификаты.md', 'Сертификаты', 'acme.sh, выпуск, продление, подводные камни'),
            ('dns.md', 'DNS', 'зоны, резолверы, ускорение'),
            ('docker.md', 'Docker', 'сети, compose, изоляция компонентов'),
            ('мониторинг.md', 'Мониторинг', 'алерты, метрики трафика, health-чеки'),
            ('бэкапы.md', 'Бэкапы и restore', 'что бэкапить, как восстанавливать'),
            ('ssh-доступ.md', 'SSH и доступ', 'порты, ключи, гигиена доступа'),
            ('тспу-серверное.md', 'ТСПУ: серверная часть', 'что видно со стороны сервера'),
            ('вехи.md', 'Вехи', 'сетевые события года'),
        ],
    },
    {
        'key': '05', 'dir': 'docs/05-хостинги', 'name': 'Хостинги', 'emoji': '🌍',
        'color': '#06d6a0',
        'blurb': '~50 хостеров: цены, пинги, ТСПУ-статусы, конфискации, локации и подсети',
        'files': [
            ('правила-выбора.md', 'Правила выбора', 'выводы сообщества: на что смотреть до оплаты'),
            ('рф-хостеры.md', 'РФ-хостеры и облака', 'Яндекс, VK, MWS/МТС, Selectel, Reg.ru и прочие'),
            ('зарубежные-хостеры.md', 'Зарубежные хостеры', 'Aeza, Play2Go, dhost, Hetzner, OVH, NodeHost…'),
            ('страны-локации.md', 'Страны и локации', 'что работало когда — по датам'),
            ('тспу-регионы.md', 'ТСПУ по регионам', 'политика операторов и регионов'),
            ('бс-подсети.md', 'Списки БС-подсетей', 'полные выгрузки по датам'),
            ('sni-бс.md', 'SNI для БС', 'практика подбора под белые списки'),
            ('asn.md', 'ASN', 'списки автономных систем'),
            ('мосты.md', 'Мосты RU→EU', 'связки и каскады с точки зрения хостинга'),
            ('ёмкость-нод.md', 'Ёмкость нод', 'сколько юзеров держит железо'),
            ('тесты-vps.md', 'Тесты VPS', 'канонический набор проверок сервера — дословно'),
            ('боты-сервисы.md', 'Боты и сервисы', 'чем проверять локации и подсети'),
            ('экономика.md', 'Экономика', 'цены, комиссии, что во что обходится'),
            ('рынок-подсетей.md', 'Рынок подсетей', 'сколько стоят БС-подсети и аккаунты'),
            ('хронология.md', 'Хронология', 'вехи по хостерам за год'),
            ('прочее.md', 'Прочее', 'остальное по теме'),
        ],
    },
    {
        'key': '06', 'dir': 'docs/06-платёжки', 'name': 'Платёжки и бизнес', 'emoji': '💳',
        'color': '#f78c6b',
        'blurb': 'Комиссии, вебхуки, профили провайдеров, юнит-экономика, право и скам-истории',
        'files': [
            ('комиссии.md', 'Комиссии', 'сводная таблица по всем платёжкам'),
            ('профили-платёжек.md', 'Профили платёжек', 'ЮKassa, Platega, Lava, RollyPay, WATA, cisPay и др.'),
            ('env-вебхуки.md', 'Env и вебхуки', 'дословные конфиги подключения и грабли'),
            ('юкасса.md', 'ЮKassa и легальные кассы', 'что требует, чем рискуешь'),
            ('юнит-экономика.md', 'Юнит-экономика', 'цены подписок, конверсия, реклама, рефералка'),
            ('экономика-хостинга.md', 'Экономика хостинга', 'мульти-IP, подсети, серверы — прайсы рынка'),
            ('cdn-биллинг.md', 'CDN и биллинг', 'тарификация CDN, антифрод, оверселл'),
            ('риски-скам.md', 'Риски и скам', 'кто кинул, как не попасть'),
            ('право-рф.md', 'Право РФ', 'ФЗ, штрафы, аресты, OpSec-план'),
            ('вехи.md', 'Вехи', 'события экономики и платёжек по датам'),
            ('тезисы.md', 'Тезисы для выживания', 'короткий свод главного'),
        ],
    },
    {
        'key': '07', 'dir': 'docs/07-скрипты', 'name': 'Скрипты и API', 'emoji': '⚙',
        'color': '#c792ea',
        'blurb': 'Установщики, чекеры, мониторинг, генераторы роутинга, API Remnawave и Bedolaga',
        'files': [
            ('экосистема.md', 'Экосистема', 'официальные репозитории и проекты из закрепа'),
            ('установщики.md', 'Установщики', 'скрипты установки бота, панели, нод'),
            ('api.md', 'API', 'WebAPI бота, 30 вебхуков Remnawave, bulk-операции'),
            ('чекеры.md', 'Чекеры и бенчмарки', 'censorcheck, YABS, iperf, ipregion, sysbench'),
            ('мониторинг.md', 'Мониторинг', 'скрипты слежения за нодами и трафиком'),
            ('решала-защита.md', 'Решала и защита', 'Reshala, Traffic Guard, брандмауэры'),
            ('роутинг-генераторы.md', 'Генераторы роутинга', 'geo-правила, списки, автогенерация'),
            ('warp-psiphon.md', 'WARP / Psiphon', 'скрипты поднятия и связки'),
            ('боты-помощники.md', 'Боты-помощники', 'самописные боты сообщества'),
            ('mtproto.md', 'MTProto', 'telemt: панель и скрипты'),
            ('налоги.md', 'Налоги и чеки', 'НалоGO, самозанятость, чеки'),
            ('секреты.md', 'Генерация секретов', 'ключи, токены, пароли — как правильно'),
            ('ошибки-фиксы.md', 'Ошибки → фиксы', 'самое частое по скриптам'),
            ('итоги.md', 'Итог на 23.08.2026', 'состояние инструментов на конец архива'),
        ],
    },
    {
        'key': '08', 'dir': 'docs/08-хронология', 'name': 'Хронология', 'emoji': '🗓',
        'color': '#8ecae6',
        'blurb': '1940 датированных вех: блокировки, релизы, конфискации, атаки, законы — месяц за месяцем',
        'files': [],   # заполняется автоматически: файлы по месяцам
    },
]

MONTH_RU = {'01': 'январь', '02': 'февраль', '03': 'март', '04': 'апрель', '05': 'май', '06': 'июнь',
            '07': 'июль', '08': 'август', '09': 'сентябрь', '10': 'октябрь', '11': 'ноябрь', '12': 'декабрь'}


def month_files():
    d = 'docs/08-хронология'
    out = []
    if os.path.isdir(os.path.join(ROOT, d)):
        for name in sorted(os.listdir(os.path.join(ROOT, d))):
            m = re.match(r'^(\d{4})-(\d{2})\.md$', name)
            if m:
                out.append((name, '%s %s' % (MONTH_RU[m.group(2)].capitalize(), m.group(1)), ''))
    return out


def sections():
    """Спека с подставленными файлами хронологии."""
    out = []
    for s in SECTIONS:
        s = dict(s)
        if s['key'] == '08':
            s['files'] = month_files()
        out.append(s)
    return out


def doc_paths():
    """Все файлы контента в порядке спеки."""
    res = []
    for s in sections():
        for fname, title, blurb in s['files']:
            res.append((os.path.join(s['dir'], fname).replace('\\', '/'), s, title))
    return res


def slug(text, used=None):
    """Аналог github-slugger: lowercase, выкидываем пунктуацию/символы, пробелы → '-'."""
    s = re.sub(r'<[^>]+>', '', text).strip().lower()
    s = s.replace('`', '')
    s = re.sub(r'[^\w\s-]', '', s, flags=re.UNICODE)
    s = s.replace(' ', '-')
    if used is not None:
        n = used.get(s, 0)
        used[s] = n + 1
        if n:
            s = '%s-%d' % (s, n)
    return s


def rel(target, from_file):
    """Относительная ссылка из from_file (путь к файлу) на target."""
    base = os.path.dirname(from_file)
    out = os.path.relpath(target, base) if base else target
    return out.replace('\\', '/')


def headings(path):
    """[(level, text, slug, lineno)] — заголовки вне блоков кода."""
    res, used, infence = [], {}, False
    with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
        for i, line in enumerate(fh, 1):
            line = line.rstrip('\n')
            if line.startswith('```'):
                infence = not infence
                continue
            if infence:
                continue
            m = re.match(r'^(#{1,6}) +(.*?)\s*$', line)
            if m:
                res.append((len(m.group(1)), m.group(2), slug(m.group(2), used), i))
    return res


def body_lines(path):
    """[(lineno, line, infence, {level: (текст, slug)})] — поток строк с контекстом заголовков."""
    infence, stack, used, out = False, {}, {}, []
    in_service = False
    with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
        for i, line in enumerate(fh, 1):
            line = line.rstrip('\n')
            stripped = line.strip()
            # служебные блоки навигации не являются контентом
            if stripped.startswith('<!-- KB:'):
                in_service = True
                continue
            if stripped.startswith('<!-- /KB:'):
                in_service = False
                continue
            if in_service:
                continue
            if line.startswith('```'):
                infence = not infence
                out.append((i, line, True, dict(stack)))
                continue
            if not infence:
                m = re.match(r'^(#{1,6}) +(.*?)\s*$', line)
                if m:
                    lvl = len(m.group(1))
                    stack = {k: v for k, v in stack.items() if k < lvl}
                    stack[lvl] = (m.group(2), slug(m.group(2), used))
            out.append((i, line, infence, dict(stack)))
    return out


def section_of(hpath, maxlevel=3):
    for lvl in sorted([k for k in hpath if k <= maxlevel], reverse=True):
        return hpath[lvl]
    return None


def stats(path):
    """Счётчики по содержательной части файла: служебные блоки навигации не считаются."""
    content, in_service = [], False
    for line in open(os.path.join(ROOT, path), encoding='utf-8'):
        s = line.strip()
        if s.startswith('<!-- KB:'):
            in_service = True
            continue
        if s.startswith('<!-- /KB:'):
            in_service = False
            continue
        if in_service:
            continue
        content.append(line)
    txt = ''.join(content)
    return {
        'lines': len([l for l in content if l.strip()]),
        'proofs': len(re.findall(r'\[id=', txt)),
        'code': txt.count('```') // 2,
        'bytes': len(txt.encode('utf-8')),
    }
