# Заметка по chunk_016 (id 80989..89506, 01.12..05.12.2025)

## Гайд: обход блокировки YooKassa для бота за рубежом через Shadowsocks + Privoxy [id=81016, art vs, 02.12]
Полный гайд. Суть: только запросы к api.yookassa.ru идут через российский SS-сервер, остальной трафик бота прямой.
docker-compose (добавляемые секции):
```yaml
services:
  bot:
    image: your-bot-image
    environment:
      HTTP_PROXY: http://privoxy:8118
      HTTPS_PROXY: http://privoxy:8118
    networks:
      - remnawave-network
  ss_tunnel:
    image: shadowsocks/shadowsocks-libev:latest
    container_name: ss_tunnel
    restart: unless-stopped
    command: >
      ss-local
      -s SS_SERVER_IP
      -p SS_SERVER_PORT
      -k "SS_PASSWORD"
      -m aes-256-gcm
      -l 1081
    networks:
      - remnawave-network
  privoxy:
    image: caligari/privoxy:latest
    container_name: privoxy
    restart: unless-stopped
    volumes:
      - ./privoxy.conf:/etc/privoxy/config:ro
    networks:
      - remnawave-network
networks:
  bot_network:
    driver: bridge
  remnawave-network:
    external: true
```
privoxy.conf:
```
listen-address 0.0.0.0:8118
toggle 1
enable-remote-toggle 0
enable-remote-http-toggle 0
allow 172.0.0.0/8
# Только api.yookassa.ru → через Shadowsocks
forward-socks5t /api.yookassa.ru/ ss_tunnel:1081 .
```
Запуск: `docker compose up -d`, `docker compose restart remnawave_bot`. Проверка:
`docker run --rm -it --network remnawave-network curlimages/curl curl -x http://privoxy_yookassa:8118 -I https://api.yookassa.ru/v3/payments --max-time 20` → ожидаем HTTP/1.1 200 Connection established + HTTP/2 401.
Технически важно: достаточно, чтобы запрос на СОЗДАНИЕ платежа шёл из РФ-сети; вебхук придёт независимо от исходного IP.
Простая альтернатива [id=81010, Zavulon]: в hosts прописать `api.yookassa.ru <подставной IP>`, на нём поднять nginx с доменом юкассы (костыль).
Другие способы: писать в ТП юкассы (добавляют IP в белый список за час-два, звонить на горячую линию и просить техника — быстрее) [id=81162, 81167, 85359]; был период, когда юкасса сама всё починила [id=83202, 83214, 83447?]. ЮМани: для сервера не в РФ — писать в ТП ЮМани, добавить IP сервера в белый список платёжки [id=85174].

## XHTTP конфиги (полные, дословно)
### Рабочий xhttp+reality через yandex.ru (selfsteal-независимый) [id=82568, hdhdh4226ru, 02.12]
```json
{
  "log": {"loglevel": "none"},
  "inbounds": [{
    "tag": "VLESS_XHTTP_YANDEX_REALITY",
    "port": 443, "listen": "0.0.0.0",
    "protocol": "vless",
    "settings": {"clients": [], "decryption": "none"},
    "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
    "streamSettings": {
      "network": "xhttp",
      "security": "reality",
      "xhttpSettings": {"path": "/"},
      "realitySettings": {"show": false, "xver": 0, "target": "yandex.ru:443",
        "shortIds": [""], "privateKey": "",
        "serverNames": ["yandex.ru","www.yandex.ru"]}
    }
  }],
  "outbounds": [
    {"tag":"DIRECT","protocol":"freedom","settings":{"domainStrategy":"ForceIPv4"}},
    {"tag":"BLOCK","protocol":"blackhole"},
    {"tag":"IPv4","protocol":"freedom","settings":{"domainStrategy":"ForceIPv4"}}
  ],
  "routing": {"rules": [
    {"ip":["geoip:private"],"type":"field","outboundTag":"BLOCK"},
    {"type":"field","domain":["geosite:private"],"outboundTag":"BLOCK"},
    {"type":"field","protocol":["bittorrent"],"outboundTag":"BLOCK"}
  ]}
}
```
Автор: самый дефолтный вариант; добавить DNS и перенаправления по необходимости. У него tcp BS не блокировали, этот конфиг работоспособен, но у некоторых клиентов требовался перезапуск каждые 20 мин.
### Пример (НЕ рабочий сам по себе) xhttp+reality c github.com SNI через nginx-сокет [id=80989, Артем Яковлев]
Профиль ноды: inbound 443 vless, xhttp mode auto path /germany-xhttp, reality dest `/dev/shm/nginx.sock` xver 1, serverNames ["github.com"]. XHTTP extra params в хостах:
```json
{"xmux":{"cMaxReuseTimes":0,"maxConcurrency":"16-32","maxConnections":0,"hKeepAlivePeriod":0,"hMaxRequestTimes":"600-900","hMaxReusableSecs":"1800-3000"},
 "headers":{},"noGRPCHeader":false,"xPaddingBytes":"100-1000",
 "scMaxEachPostBytes":1000000,"scMinPostsIntervalMs":30,"scStreamUpServerSecs":"20-80"}
```
Ошибка: serverNames github.com, а должен быть свой SNI (селфстил) [id=80991-80993].
### Другой TLS-конфиг с проблемами пинга [id=82297, Maksim Tovkalov]
VLESS+TCP+TLS 443 (letsencrypt сертификаты, ocspStapling 3600, cipherSuites список, maxVersion 1.3): пинг 500/3000+; на maxVersion 1.2 не работает; пингометр — Happ (это фича Happ, проверять в другом приложении) [id=82314, 82320].

## Технология БС/обходы
- РКН усилил блокировки: ТСПУ ограничивают SOCKS5, VLESS, L2TP (конец ноября — проблемы в Татарстане, Удмуртии, Нижегородской, Свердловской, Новосибирской, Томской, Волгоградской обл., Приморье) — новость, часть считает накруткой [id=85365].
- БС теперь по CIDR-подсетям, не по доменам/SNI: работающие подсети — Яндекс и VK Cloud; IP надо выбивать (перевыпуск/поддержка) [id=82020, 85340?]. SNI-обходы почти не работают: «От сни я сомневаюсь что будет работать» [id=82628]; при сни vk.com у клиентов вылетает из учётки ВК [id=82641].
- Я.Клауд/VK: пул белых IP ограничен (13, 51, 52, 228 воркают; 213 у одного ворк; 217 у VK выпилен из пула) [id=83708-83721, 85317?]. VK Cloud и Яндекс — «лотерея»: перевыпуск бесплатно (новый сервер) [id=83642], в Яндексе смена IP платная.
- Кластерная альтернатива:selectors/cIDR — обход БС только через ЯКлауд/VK; остальные хостеры (Hetzner, OVH, blackmore и т.п.) недоступны с РФ напрямую — нужен ру-мост.
- Мосты: ру-сервер как мост на зарубежный (150р hosting-russia, безлим, ~гигабит); полный проброс портов rinetd: `0.0.0.0 443 <IP> 443`, `0.0.0.0 2222 <IP> 2222` [id=83835-83843]; nginx-мост/фейл; netbird/tailscale/GRE/WG-туннели.
- ВК-приложение на ру-ноде не работает из-за БС — лечится роутингом ВК в direct [id=85807].
- NFQWS-нода — открытый вопрос [id=87911].
- amneziawg на ноде для роутеров с xkeen: быстрее настроить, чем xkeen [id=87034].

## Клиенты и HWID
- xhttp поддерживают: Happ, v2raytun, v2rayN, NekoBox, Throne [id=81086, 81091]. Hiddify — не рекомендуют: старое приложение без обнов ~1.5 года [id=85982]. Hiddify подписки/ключи не работают у всех [id=85646].
- HWID-лимит: `HWID_DEVICE_LIMIT_ENABLED=true`, `HWID_FALLBACK_DEVICE_LIMIT=10`, `HWID_MAX_DEVICES_ANNOUNCE="Max devices reached"` [id=81904]. NeKoray/nekoray — HWID нет [id=85953].
- Клиент "Coala"-типа без HWID не показывает, сколько человек реально пользуют подписку (HWID-статистика независима, но аномальный трафик — единственный признак) [id=85941-85950].
- packet-up в xhttp решает проблему на iOS [id=82582].

## Bedolaga/Remnawave баги и фичи
- env-приоритет: коммит 17768c30 (1 ноя 2025) — настройки в .env теперь имеют приоритет над DB (админкой бота нельзя менять то, что есть в env) [id=89503, 89506].
- После обновления: `Bad Request: inline keyboard button URL 'clash://install-config?url=...' is invalid: Unsupported URL protocol` [id=81132] — Telegram не пускает схему clash в inline-кнопках; happ://add тоже (Bad Request) [id=78454 из chunk15; здесь тоже].
- `Bad Request: can't parse entities: Unsupported start tag "b>"` — HTML-теги `<b>` в промо-сообщении не парсятся (нужен HTML parse mode или экранирование) [id=83927-83930].
- Рассылка застряла на 23к пользователей [id=81845]; Рассылка фотки → `there is no text in the message to edit` (фикс, раньше bug) [id=78916].
- Донат-бот (BedolagamNaPivoBot, c0mrade_ton): Tribute API не даёт читать старые донаты; в API группы не даёт список участников — решается сохранением пользователей из сообщений; теги в донатах экранируются; лидерборд обновляется по донату; сообщения >48ч в группах не редактируются (ограничение TG) [id=82228, 82081, 82091-82097].
- Миниапка продлевает триал (баг): через миниапп можно продлить триал вместо покупки новой подписки; нужен фикс в коде миниаппа [id=81373, 81377, 81529].
- Скрытие подписок/настроек конфига в happ: happ routing / скрыть конфиги (открытый вопрос) [id=89260, 89299].
- `MULENPAY_*` настройки в .env (полный блок с FIRMWARE ...) [id=84480]:
  MULENPAY_ENABLED=false, MULENPAY_API_KEY=, MULENPAY_SECRET_KEY=, MULENPAY_SHOP_ID=, MULENPAY_BASE_URL=https://mulenpay.ru/api, MULENPAY_WEBHOOK_PATH=/mulenpay-webhook, MULENPAY_DESCRIPTION="Пополнение баланса", MULENPAY_LANGUAGE=ru, MULENPAY_VAT_CODE=0, MULENPAY_PAYMENT_SUBJECT=4, MULENPAY_PAYMENT_MODE=4, MULENPAY_MIN_AMOUNT_KOPEKS=10000, MULENPAY_MAX_AMOUNT_KOPEKS=10000000.
- В env нельзя вставлять inline-комментарии `# ...` после значения — pydantic ругается `Input should be a valid integer` [id=84469].
- BASE_SUBSCRIPTION_PRICE=0 — цена для «быстрой покупки» (fixed-режим); режимы выбора цен: базовый (per-period) и fixed [id=85171, 88838, 88843].
- Продление подписки суммирует дни (15+30=45) [id=82232, 82234].
- YOOKASSA_RETURN_URL: «от юкассы не приходит подтверждение, деньги списываются, автопроверка вручную» [id=86574].
- Kassing: если бот в ру, а панель на дхосте — периодические дисконекты (тех. редкость); ставить бот+панель рядом, или туннель [id=87621].
- Tribut webhook 404: URL в .env полный [id=82780-82781].
- Platega: настройка в .env (токен, айди мерчанта) + ссылка на вебхуки в настройках платёжки [id=87570, 87573].
- Platega минимальный чек по СБП от 100 ₽ [id=87634].
- Tribute: API key получить после верификации; TRIBUTE_ENABLED, TRIBUTE_API_KEY, TRIBUTE_DONATE_LINK, TRIBUTE_WEBHOOK_PATH=/tribute-webhook, TRIBUTE_WEBHOOK_HOST=0.0.0.0 [id=87637].
- ЮKassa чек: description «Интернет-сервис - Пополнение баланса», vat_code 1, payment_mode full_payment, payment_subject service (повтор).
- Убрать фичу копеек нельзя — платежки требуют копейки, в БД все в копейках [id=85999].
- Лидерборд донатов: 10 валютных категорий; по 2 часа опрос БД; будущая картинка через Pillow [id=81933, 82130, 82104].
- Maintenance Service уведомления: API Remnawave недоступен; выставить 3 попытки в .env вместо 1 (не работает на 2.8.0: 3 попытки, иногда всё равно после 1) [id=83776, 88954, 88962].
- xray-checker (kutovoys) — легкий мониторинг нод; bezzel — самый простой способ, ставится легко, жрет меньше графаны [id=87839].
- Remnawave ad-бот (админ-бот с открытым исходником) v0.2: поддержка Remnawave API v2.2.6, сквады, HWID, локализация: https://github.com/Case211/remna-ad/releases/tag/v0.2 [id=85324].
- miniapp Payment: github.com/BEDOLAGA-DEV/... miniapp-payment путь; обновление через `git pull origin main` + `make reload` иногда не докачивает файлы [id=85676, 86281].
- Изменение картинок в админке бота не работает, если значение есть в .env (env-приоритет) [id=87652, 87665].
- Проверка скорости curl до api.telegram.org: `curl -o /dev/null -s -w 'Connect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n' https://api.telegram.org` и `curl -o /dev/null -s -w 'Total: %{time_total}s\n' "https://api.telegram.org/bot<TOKEN>/getMe"` [id=87774, 87785].
- sysbench CPU: `sysbench cpu run --threads=1` [id=87627].
- api.remna ложится 5-10 раз в день, восстанавливается за минуту (иногда дольше) — у нескольких пользователей; Cloudflare вордпресс-запросы с Клауда помечаются как WP; Multitenant нет; установка Medallist-защиты не помогла [id=88890, 89037-89063].
- Начат migration: панель и бота переносят через backup/restore; аеза → решение: Egor e.a. ищут альтернативу.

## Bedolaga 3.0 / веб-админка
- Веб-админка в тесте с 04.12; лайт-версия веба фри, полный веб по подписке; селфхост-версия тоже будет [id=84666-84719, 86979].
- Мониторинг (графана-подобный) внутри админки; тикеты с фотками [id=84696, 84713].
- 3.0 — доработка функционала, красивая архитектура [id=86968, 86973].
- Ноды раскатываются и подключаются к ремне «в клик» [id=84685].

## Хостинги (много)
- TimeWeb.cloud — пол года без проблем; почасовой тариф; для панели ок, нода не оч (прилетает ограничение); ютуб работает с Moscow-локации [id=81347-81369, 88966, 85158]. SSH до мск-таймвеб из Сибири заблокирован (портовая блокировка ТСПУ) [id=86351].
- vdska (Вдсина) — негатив: обиженка-владелец, в МСК другое юрлицо, но подсети в бане РКН, не рекомендуют [id=84830, 87125].
- Play2Go (https://play2go.cloud/?ref_id=8ZqeBJW03Pg) — Егор с 3.0 съехал с аезы на них; ютуб норм, но иногда "кони" [id=89014, 89019].
- 1cents/hostvds (Финляндия) — анлим за $1/мес (0.5ТБ база + $1 анлим; $1.99 если 10Гбит); суппорты против коммерческого VPN, на сайте алерт [id=85850, 85799, 85853].
- hip.hosting (реф `?code=37d25ad0b3b05ca581f0`) — Германия выдает 6-9 Гб при 100/200 заявленных; финка говно [id=81998, 85989].
- blackmore.cloud — ресейл OVH (Германия/Франция/Грузия), ютуб плохо работает, ~500мбит при 1гбит; 350р за 2/1/20; 2 месяца по месяцу бесплатно для теста; РФ-доступ только через VPN (OVH заблокирован) [id=86251, 86351].
- ishosting — смена IP 15$, рекомендуют ru-CDN за x10 цены; сайт сабки с ру лучше держать на ру-ВДС [id=85339].
- Дхост (dhost) — 2 ноды Германия, 335р 1/2/3ТБ, 1Гбит (реально 800-900), аптайм 100% 2 мес; финка у них говно [id=85885].
- VeEsp (https://veesp.com/ru/) — SH (Дания?), 10 гигабит, Fair Use, самый живучий из дешевых, Висп [id=85848, 85846].
- dhostVPS бот: https://t.me/dhostVPS_bot?start=2104519441 [id=81972].
- Blackmore cloud — OVH-ресейл [id=83787].
- Латвия на serva.one — гигабит, 12 баксов/3 мес [id=81302, 81315].
- Нексус — Польша пиздатая, 24 бакса [id=81293].
- Сенко (senko.digital) — 450р за 2/4/30 100мбит; норм для панели, для ноды не оч [id=89018, 81028, 82997].
- firstvds — ру-ноду отьебали (старый, 2-3 года юзал) [id=86022-86025].
- rocketcloud, hosting-russia.ru [id=87126].
- Я.Клауд/VK-сети — для БС; первый айпишник в ЯКлауде выбрать нетрудно [id=81447].
- Del VPN hosting: WK-класса нет. Hetzner (blackmore) — берут через ovh, недоступен из РФ.
- Сенка `senko.digital` — Финляндия [id=87523].
- Латвия, Польша (224 гб), Испания — на Сенке [id=87565].

## Платежи
- Платежки на QR для нерезидентов РФ — открытый вопрос (из бота: Telegram Stars + Tribute + CryptoBot + Heleket + YooKassa СБП/карты + MulenPay + PayPalych СБП/карты + Platega карты/СБП + WATA) [id=84462, 89297].
- Platega комиссия 7-11%; Вата — лучше юзать Платегу [id=84695, 84764, 82737].
- Крипту легалайзить — нельзя (161 ФЗ); Сбер и Тинькофф самые душные к крипте; ВТБ банит за один перевод; выход — выводить наличку через обменники (Гарантекс, БериБит в Москве) [id=88882-88923].
- Скинь cryptobot QR-оплата появилась в CryptoBot [id=88926].
- CryptoBot: ходят слухи о потерях при выводе — не подтверждено [id=89327].
- Tribute «наебал» донат: не зачислился, в истории транзакций не видно [id=85644, 86543].
- Юкасса — то фиксится, то отваливается (РКН пидорасы, по словам техника) [id=85359].
- Меню тейпа: При пополнении пишет «С баланса» вместо способа платежа (Platega/Юкасса) [id=81802].

## Разное
- ВК/Telegram-реклама: маркированная реклама запрещена для каналов в РКН (erid-токен), но теневые каналы без регистрации — можно [id=81249-81257].
- Дисклеймер сервиса: запрет обхода блокировок РКН/Мининформ РБ — пример текста ToS [id=81228, 81237].
- HolorISO/SteamOS — арч-база, holoiso заброшен; Steam Machine скоро [id=82923-82941].
- AI: Gemini бесплатно на год (гайд telegra.ph/googleaipro-11-10, через малайзию/украину VPN), Qwen.ai, DeepSeek, Claude Sonnet [id=83083, 83058-83074].
- Легальные VPN (MAX, «мембрана» МТС) — сами продают обход, госструктуры форсят [id=88810, 88815].
- Кроудсек на ноды — только если не 1/1 [id=88151].
- Сервер на OPKG Entware для keenetic: help.keenetic.com/hc/ru/articles/360021888880 [id=82339].
- «Автоинсталл от Амира Хусейна на openwrt» — не ставить, засирает роутер [id=82335].
- Yandex/ВК обсуждают «выбивание» IP через саппорт и смена подсети (перевыпуск сервера).
- Разные «идеи» и флуд вокруг Ивана-nginx (см. chunk 015 тоже).
- РКН хочет блокировать майнинг [id=87967].
- Caddy vs Nginx холивар; «кадди говно нджикс топ» мем; для новичков —ИИ + реверс-прокси из доков [id=87926, 87939, 88858].
- Caddy-конфиг от Александра [id=88858]: hook.domen.com с path_regexp на все вебхуки (yookassa|platega|cryptobot|wata|heleket|tribute|pal24|mulenpay)-webhook, handle_path /app-config.json с CORS, miniapp.domen.com (handle_path /miniapp/*, статика root /miniapp), bot.domen.com (всё на бота). Рабочий, по словам автора.
- Перенос бота на nginx с caddy — реально, конфиги есть в репо бота [id=84505].
- docker compose: `docker compose down && docker compose up -d --build && docker compose logs -f`; у бота одну сеть оставить (external), bot_network снести [id=84437-84450].
- «happ redirects» конфигурация (снипов нет в этой заметке — отсылка в скринах).
- Remnawave routing.happ.su — конструктор happ-роутинга: https://routing.happ.su/ [id=86744].
- Хостинг России (hosting-russia.ru) — vpska для моста 150р, безлим, гигабит [id=83800].
- Не монтировать 2 инстанса прокси на одном сервере (nginx + caddy вместе не живут) [id=83827].
- ТСПУ в некоторых регионах шейпят ТСП-Reality, некоторые регионы вообще не могут ssh до ру-серверов [id=86351].
- Платежная система Telegram Stars: оплата звездами включена по умолчанию; курс по дефолту 1.79 [id=85172, 85173].
- bedolaga-чат: звезды GitHub: remnawave/panel, BEDOLAGA-DEV/..., kutovoys/xray-checker, eGamesAPI/remnawave-reverse-proxy, Jolymmiels/remnawave-telegram-shop, machka-pasla/remnawave-tg-shop, DigneZzZ/remnawave-scripts, distillium/remnawave-backup-restore, maposia/remnawave-telegram-sub-mini-app, legiz-ru/my-remnawave.
