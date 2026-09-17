# Заметки из chunk_043 (id 247087..252353, 28.02–03.03.2026)

## Remnawave Bedolaga Bot / Cabinet — релизы 28.02–03.03
- **[id=251354|Egor|02.03](https://t.me/c/2941121338/251354)** Bedolaga Bot v3.21.0: API статистики продаж (6 аналитических эндпоинтов: summary, trials, subscriptions, renewals, addons, deposits), VK ID OAuth 2.1 с PKCE, сброс трафика при смене тарифа (админ-настройка), желаемая комиссия в заявке партнёра. Фиксы статистики, подписок (двойной вызов panel API, разделение базового/докупленного трафика), партнёрки, авторизации, промокодов, синхронизации, Freekassa OP-SP-7.
- **[id=251358|Egor|02.03](https://t.me/c/2941121338/251358)** Cabinet v1.23.0: дашборд статистики продаж (5 вкладок), аналитика кампаний, полноэкранный QR-код, VK ID OAuth 2.1. Оптимизация фонов (Canvas вместо 225 DOM-элементов), поток покупки/продления на отдельную страницу.
- **[id=249893|Илья|03.03](https://t.me/c/2941121338/249893)** Remnawave Admin v2.6.0 — Liquid Glass UI, Dashboard 2.0, аналитика Retention (когортный), история метрик нод, обнаружение торрент-трафика (детекция BitTorrent через Xray routing rules + автоблокировка через шаблон auto_block_torrent). https://github.com/Case211/remnawave-admin

## Bedolaga: полезные переменные .env
- **[id=249397|—|03.03](https://t.me/c/2941121338/249397)** `PRICE_360_DAYS` не применяется — надо сменить режим (обычно за счёт тарифов).
- **[id=249412|Мультитысячник|03.03](https://t.me/c/2941121338/249412)** Ошибка бэкапа: `Object of type time is not JSON serializable` (баг).
- **[id=250341|—|03.03](https://t.me/c/2941121338/250341)** Переменные с бэкапами в бот: `BACKUP_SEND_ENABLED=true`, `BACKUP_SEND_CHAT_ID=-100...`, `BACKUP_SEND_TOPIC_ID=...`, `BACKUP_ARCHIVE_PASSWORD=`.
- **[id=251879|Мультитысячник|03.03](https://t.me/c/2941121338/251879)** Переменные для ИИ саппорта:
  ```
  REMNAWAVE_API_URL=https://panel.example.com
  REMNAWAVE_API_KEY=your_api_key_here
  REMNAWAVE_SECRET_KEY=XXXXXXX:DDDDDDDD
  ```
- **[id=248075|libkit|01.03](https://t.me/c/2941121338/248075)** `DEFAULT_TRAFFIC_RESET_STRATEGY=MONTH` — глобальная сброска трафика в бедолаге.
- **[id=250088|zyko|02.03](https://t.me/c/2941121338/250088)** Автоплатёж удваивает цену (баг), Егор обещал убрать.
- **[id=248906|Клин|03.03](https://t.me/c/2941121338/248906)** Ошибка из-за SMTP-домена (`.shop` заблокирован). `.online`/`.pro` работают.
- **[id=251795|—|03.03](https://t.me/c/2941121338/251795)** Основная причина: бот и кабинет в разной docker-сети (`MINIAPP_DOMAIN` или `CABINET_URL`), сеть к панели из бота. Решение: `docker-compose.override.yml` / единая docker-network.
- **[id=249458|Whiteness|02.03](https://t.me/c/2941121338/249458)** Домены: `com`, `net`, `online`, `pro` — работают; `.shop`, `.lat`, `.xyz`, `.top`, `.org` — не пускают ТГ.

## Кабина (bedolaga-cabinet) — обновления
- **[id=247554|Egor|28.02](https://t.me/c/2941121338/247554)** Кабина v1.23: `Cabinet_url` и `usernamebot` в .env; в настройках -> remnawave -> синхронизация.
- **[id=249382|Egor|02.03](https://t.me/c/2941121338/249382)** `MINIAPP_CUSTOM_URL` + `CABINET_ENABLED` — кабинет из ТГ.
- **[id=247406|Djingle|28.02](https://t.me/c/2941121338/247406)** Кабина v1.22: что за Freekassa и NaloGO.
- **[id=246379|max|28.02](https://t.me/c/2941121338/246379)** КРИПТОЛИНК — юзкейс.
- **[id=246560|MAKS|27.02](https://t.me/c/2941121338/246560)** RKN-blockin «163.580.820» и «142.250.180.233» — «это» (не нажимать).

## Кабина: мессенджеры/ТГ-логин
- **[id=247161|Whiteness|28.02](https://t.me/c/2941121338/247161)** `TG_LOGO` в .env.
- **[id=249605|tgshtt|02.03](https://t.me/c/2941121338/249605)** Telegram Login Widget (`https://core.telegram.org/bots/telegram-login`).

## Payment / Freekassa (критика)
- **[id=250513|—|02.03](https://t.me/c/2941121338/250513)** Freekassa: минимальная сумма пополнения кошелька 2 000 ₽ (p2p), комиссия до 13%, требует фриваллет; код 400 — норма (валидный отказ).
- **[id=250912|—|02.03](https://t.me/c/2941121338/250912)** «Тестирующая валюта» — FkWallet — привязывается к одному аккаунту (телеге).
- **[id=251014|DarkKingArthas|02.03](https://t.me/c/2941121338/251014)** Freekassa минимальное: кошелёк/мерчант 5 дней, 400 при тестах.
- **[id=250628|—|02.03](https://t.me/c/2941121338/250628)** Вата: 12% карт, 11% СБП, «можно предложить 10-15%».
- **[id=249666|—|01.03](https://t.me/c/2941121338/249666)** Platega: метод 11 (карт) → 2, 10, 13; «10-й метод» не используется.
- **[id=246297|libkit|28.02](https://t.me/c/2941121338/246297)** Касса AI: мин 10% СБП, 12% карт (как у ваты).
- **[id=246044|—|28.02](https://t.me/c/2941121338/246044)** NaloGO: «меня загоняют на 3-4%»; юкасса «0,4% СБП/0,6%». Налоговая «дурацкая» (доставка чеков всем вручную).
- **[id=247906|—|01.03](https://t.me/c/2941121338/247906)** NaloGO (Касса АИ): «у меня нет».

## Обновления Remnawave (мск-структура)
- **[id=247411|MAKS|28.02](https://t.me/c/2941121338/247411)** Remnawave Admin v2.5.2: сортировка нарушений, пароль в уведомлениях, фильтры сохраняются в URL, удалённые хосты сразу исчезают.
- **[id=243451|Дмитрий|26.02](https://t.me/c/2941121338/243451)** Remna: `cap_add: NET_ADMIN` в docker-compose для функции `Xray-Json Advanced`.
- **[id=242311|Владимир Данилов|25.02](https://t.me/c/2941121338/242311)** Remnawave v2.6.4: Xray-Json Advanced, addVirtualHostAsOutbound, Mihomo + hidden hosts.
- **[id=242311|Дмитрий|26.02](https://t.me/c/2941121338/242311)** Panel v2.6.2+: просмотр/удаление пользовательских сессий, Xray-Json Advanced, скрытые hosts, Remna Node 2.6.0+.

## Remnawave: уязвимости / безопасность
- **[id=247707|—|01.03](https://t.me/c/2941121338/247707)** Использование caddy-security (1.1.27) + cloudflare + caddy-ratelimit + cache-handler + caddy-defender + caddy-maxmind-geolocation (решение c0mrade):
  ```docker
  FROM caddy:2.10.2-builder AS builder
  RUN xcaddy build \
      --with github.com/greenpau/caddy-security@v1.1.27 \
      --with github.com/caddy-dns/cloudflare \
      --with github.com/mholt/caddy-ratelimit \
      --with github.com/caddyserver/cache-handler@v0.16.0 \
      --with pkg.jsn.cam/caddy-defender \
      --with github.com/porech/caddy-maxmind-geolocation
  FROM caddy:2.10.2
  COPY --from=builder /usr/bin/caddy /usr/bin/caddy
  ```
- **[id=247536|/dev/null|02.03](https://t.me/c/2941121338/247536)** Traffic-Guard (сканеры РКН): https://raw.githubusercontent.com/shadow-netlab/traffic-guard-lists/refs/heads/main/public/government_networks.list
- **[id=249042|Artur Karimov|01.03](https://t.me/c/2941121338/249042)** Ремнавейв, разрешение на форки и `.io/.xyz/.top/.shop` домены, «localhost 8080»: веб-панель бедолаги.
- **[id=248137|DonkyBoss|01.03](https://t.me/c/2941121338/248137)** `Invalid HTTP request received.` (отказ запросов от 8080).

## Экономика (цены, платежи)
- **[id=247349|kevin|28.02](https://t.me/c/2941121338/247349)** 1cent.host: 89.208.216, 95.163.248.0 — нодам ОВХ из-за новых шлюзах; «4vps - 🇺🇸США, Атланта 770₽ (2/4/25/2Gbit)», «IP пободрее», «канал пободрее, чем в австралии».
- **[id=247458|—|28.02](https://t.me/c/2941121338/247458)** Play2Go HI-LOAD NL 425₽ (1/2/80/10Gbit) — «геоайпи очень порадовал».
- **[id=247772|Prokurátura|01.03](https://t.me/c/2941121338/247772)** vibehost_bot (Реселл Hetzner) Финляндия Хельсинки 4.95$ (2/4/40 NVMe) — «подсеть забанена в РФ, для ноды только мост», диск 1.2-1.3 GB/s, сеть 5 Gbit/s.
- **[id=247789|—|01.03](https://t.me/c/2941121338/247789)** Play2Go FI Хельсинки 340₽ (1/2/80/1Gbit, AMD Ryzen 9 5950X) — «аипишник норм, сети 700-800 Мбит».
- **[id=247805|—|01.03](https://t.me/c/2941121338/247805)** selectel.ru СПб 660₽ (1/2/5GB HDD, 3-4 Gbit) — «тспу есть, ютуб и дискорд работают, инста заблочена».
- **[id=247829|—|01.03](https://t.me/c/2941121338/247829)** veesp.com Латвия/Нидерланды/Швеция 5$ (1/1/20/1Gbit Unlimited) — «шикарный сервер», «скорости отличные», «IP чистые».
- **[id=247839|—|01.03](https://t.me/c/2941121338/247839)** cloud.vk.com Москва 1493₽ (1/2/10 NVMe) — «очень дорого», «сети 4-10 Gbit».
- **[id=247934|—|01.03](https://t.me/c/2941121338/247934)** NKTelekom AMS-CLOUD-20 2.99$ (1/2/20) — «не рекомендую, конченый IP, AES-NI выключен, steal 15-40».
- **[id=247931|Tatoxa|01.03](https://t.me/c/2941121338/247931)** FirstVDS «Разгон» 909₽ (2/4/60/100Мбит) — «SLA хостера высокий», «SSD дохлый», поддержка вернула деньги.
- **[id=248334|Roman|01.03](https://t.me/c/2941121338/248334)** Warpx ( Германия 77.239.113.0/24, AS201048, «эпик zen 2», «сеть 850мб/с», «финка 27мб/с и 14 на загрузку») — «не рекомендую финку».
- **[id=248582|MAKS|01.03](https://t.me/c/2941121338/248582)** AlexHost SE 10€ (2/4/40/1Gbit) — «на ноде без нареканий», BBR2.
- **[id=248322|Колян|01.03](https://t.me/c/2941121338/248322)** servhost (Epyc-7502-1, 1/1/10/250Mbps, Москва 150₽).
- **[id=248067|—|01.03](https://t.me/c/2941121338/248067)** cloudrix (S1-MSK 2/2/25/1Gbit Москва).
- **[id=248075|—|01.03](https://t.me/c/2941121338/248075)** vps.tc (Турция) 160₽ (1/1/20/10Gbit, 2ТБ лимит).
- **[id=248082|—|01.03](https://t.me/c/2941121338/248082)** 1centhost EE 180₽ (EE-PROMO, 1/1/10/1Gbit) — дубль.

## Remnawave Bedolaga: Remnawave-админ (новые фичи)
- **[id=247192|Илья|28.02](https://t.me/c/2941121338/247192)** Remnawave Admin v2.5.2 — история релизов, принудительная смена пароля, поиск нарушений по имени, пароль в уведомлениях.
- **[id=247190|Илья|28.02](https://t.me/c/2941121338/247190)** Remnawave Admin v2.5.2 — дубликаты при сортировке нарушений.
- **[id=247218|Илья|28.02](https://t.me/c/2941121338/247218)** Remnawave Admin v2.5.2 — «Подробнее».
- **[id=247214|Илья|28.02](https://t.me/c/2941121338/247214)** Remnawave Admin v2.5.2 — «Горячие клавиши».
- **[id=247214|Илья|28.02](https://t.me/c/2941121338/247214)** Remnawave Admin v2.5.2 — «Горячие клавиши».

## Remnawave Bedolaga: Нода (Remnawave Node)
- **[id=247838|Илья|01.03](https://t.me/c/2941121338/247838)** Remnawave Node v2.5.2 — «Xray-конфиги + скрытие».
- **[id=247838|Илья|01.03](https://t.me/c/2941121338/247838)** Remnawave Node v2.5.2 — «Xray-конфиги + скрытие».
- **[id=247838|Илья|01.03](https://t.me/c/2941121338/247838)** Remnawave Node v2.5.2 — «Xray-конфиги + скрытие».

## Remnawave Bedolaga: Обновления
- **[id=249397|MAKS|03.03](https://t.me/c/2941121338/249397)** Remnawave Admin v2.6.0 — Liquid Glass UI, Dashboard 2.0.
- **[id=249397|Илья|03.03](https://t.me/c/2941121338/249397)** Remnawave Admin v2.6.0 — аналитика Retention.
- **[id=249397|Илья|03.03](https://t.me/c/2941121338/249397)** Remnawave Admin v2.6.0 — история метрик нод.

## Полезные ссылки из чанка
- https://github.com/Case211/remnawave-admin
- https://github.com/Case211/remnanode-install
- https://github.com/P-Neutrino/Neutrino/
- https://github.com/d3156/RemnawavePlugins
- https://github.com/dotX12/traffic-guard
- https://github.com/evoll/xui2remnawave-migrate
- https://github.com/shadow-netlab/traffic-guard-lists
- https://docs.bedolagam.ru/bot/channel-subscription
- https://docs.bedolagam.ru/getting-started/requirements
- https://utils.docs.rw/happ-rb
- https://hyperion-cs.github.io/dpi-checkers/ru/ipv4-whitelisted-subnets/
- https://github.com/kutovoys/xray-torrent-blocker
- https://github.com/eGamesAPI/remnawave-reverse-proxy
- https://log.rw/Bw8tv5MJ
- https://log.rw/5wyEPiRV
