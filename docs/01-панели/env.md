# Env-переменные — по периодам

<!-- KB:HEAD -->
[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Env-переменные**

◀ [Docker-compose](docker-compose.md) · [Nginx / Caddy](reverse-proxy.md) ▶

> дословные .env по периодам: бот, кабинет, панель, платёжки

<details>
<summary>📑 <b>На этой странице</b> — 47 разделов</summary>

- [Период 23.08–07.09.2025 — Bedolaga v2.0.x–2.2.x, Remnawave 2.1.x](#период-230807092025--bedolaga-v20x22x-remnawave-21x)
- [Период 12.11.2025–01.01.2026 — Bedolaga v2.7–2.9.4, Remnawave 2.3–2.4](#период-1211202501012026--bedolaga-v27294-remnawave-2324)
  - [Минимальный .env бота (2.9.x канонический)](#минимальный-env-бота-29x-канонический)
  - [Платежки (env дословно)](#платежки-env-дословно)
  - [Nginx/Caddy для хуков и панели](#nginxcaddy-для-хуков-и-панели)
- [Период 09.02–13.03.2026 — Bedolaga v3.9–3.32, Remnawave 2.6.x, Remnawave-admin 2.x](#период-090213032026--bedolaga-v39332-remnawave-26x-remnawave-admin-2x)
- [Период 16.03–06.04.2026 — Remnawave 2.7.x (breaking), Bedolaga v3.33–3.45](#период-160306042026--remnawave-27x-breaking-bedolaga-v333345)
- [Период 06–25.04.2026 — Bedolaga v3.45–3.52, Remnawave-admin 2.9–2.11](#период-0625042026--bedolaga-v345352-remnawave-admin-29211)
  - [Бот + панель (один сервер, webhook) [id=343457,343482,343497](https://t.me/c/2941121338/343457)](#бот--панель-один-сервер-webhook-id343457343482343497)
  - [Overpay v3.51.0 (16 переменных) [id=392083|23.04.2026](https://t.me/c/2941121338/392083)](#overpay-v3510-16-переменных-id39208323042026)
  - [RollyPay [id=399154|24.04.2026](https://t.me/c/2941121338/399154)](#rollypay-id39915424042026)
  - [Пример env подписок [id=384935|21.04.2026](https://t.me/c/2941121338/384935)](#пример-env-подписок-id38493521042026)
  - [Кнопки кабины [id=400574|25.04.2026](https://t.me/c/2941121338/400574)](#кнопки-кабины-id40057425042026)
  - [Прочие env (дословно из чата)](#прочие-env-дословно-из-чата)
- [Период 25.04–15.05.2026 — Bedolaga v3.49–3.55, Cabinet 1.49–1.52](#период-250415052026--bedolaga-v349355-cabinet-149152)
  - [Интерфейс и UX (дословно) [id=401587–401792, 25.04](https://t.me/c/2941121338/401587)](#интерфейс-и-ux-дословно-id401587401792-2504)
  - [WEBHOOK [id=427502, 414748, 436471](https://t.me/c/2941121338/427502)](#webhook-id427502-414748-436471)
  - [SMTP (классический пример) [id=447566](https://t.me/c/2941121338/447566)](#smtp-классический-пример-id447566)
  - [Кабинет / авторизация [id=446652, 446650, 505559, 463147, 458641, 435273, 432946](https://t.me/c/2941121338/446652)](#кабинет--авторизация-id446652-446650-505559-463147-458641-435273-432946)
  - [Платёжные переменные и webhook-пути (это настройка бота — включено)](#платёжные-переменные-и-webhook-пути-это-настройка-бота--включено)
  - [Blacklist / триалы / лимиты [id=513772, 511104, 402475, 404025](https://t.me/c/2941121338/513772)](#blacklist--триалы--лимиты-id513772-511104-402475-404025)
  - [Связка с панелью [id=458722, 433864, 458367](https://t.me/c/2941121338/458722)](#связка-с-панелью-id458722-433864-458367)
  - [ENV → БД миграция приоритета (канон)](#env--бд-миграция-приоритета-канон)
  - [Локализация / файлы](#локализация--файлы)
- [Период 16.05–05.06.2026 — Bedolaga v3.56–3.58, Remnawave-admin 2.14](#период-160505062026--bedolaga-v356358-remnawave-admin-214)
- [Период 07–26.06.2026 — Bedolaga 3.60–3.61, Subscription-page 7.2.5/7.2.6](#период-0726062026--bedolaga-360361-subscription-page-725726)
  - [Platega [id=719199|19.06.2026](https://t.me/c/2941121338/719199)](#platega-id71919919062026)
  - [Antilopay [id=663727](https://t.me/c/2941121338/663727)](#antilopay-id663727)
  - [MiniApp](#miniapp)
  - [Топики [id=703190](https://t.me/c/2941121338/703190)](#топики-id703190)
  - [Прочее](#прочее)
- [Период 26.06–08.07.2026 — Remnawave 2.8.0, Bedolaga v3.61–3.62, Cabinet 1.59](#период-260608072026--remnawave-280-bedolaga-v361362-cabinet-159)
- [Период 08–20.07.2026 — Remnawave 2.8.1, Bedolaga v3.62–3.64, Cabinet 1.61](#период-0820072026--remnawave-281-bedolaga-v362364-cabinet-161)
  - [Bedolaga Bot — выдержка из `.env` (дословно) [id=838156|09.07.2026](https://t.me/c/2941121338/838156)](#bedolaga-bot--выдержка-из-env-дословно-id83815609072026)
  - [Bedolaga Bot — прочие env-переменные (дословно из заметок)](#bedolaga-bot--прочие-env-переменные-дословно-из-заметок)
  - [Remnawave панель](#remnawave-панель)
  - [Кабинет (CABINET_*)](#кабинет-cabinet_)
- [Период 20–31.07.2026 — Bedolaga v3.66/3.67 + Cabinet 1.64 (рекурренты Platega/Lava)](#период-2031072026--bedolaga-v366367--cabinet-164-рекурренты-plategalava)
  - [Бот Bedolaga (дословные имена)](#бот-bedolaga-дословные-имена)
  - [Панель Remnawave](#панель-remnawave)
  - [Кабинет](#кабинет)
- [Период 31.07–09.08.2026 — Remnawave 3.0.0 (ломающий), Bedolaga v4.0.0, Cabinet 1.65](#период-310709082026--remnawave-300-ломающий-bedolaga-v400-cabinet-165)
  - [Remnawave Panel](#remnawave-panel)
  - [Bedolaga Bot](#bedolaga-bot)
  - [Bedolaga Cabinet (CABINET_*, VITE_*)](#bedolaga-cabinet-cabinet_-vite_)
- [Период 09–20.08.2026 — Remnawave 3.2.3/3.3.0, Bedolaga v4.1.0 (GeoCheck)](#период-0920082026--remnawave-323330-bedolaga-v410-geocheck)
- [Период 20–23.08.2026 — совместимость 2.8.x/3.2.2, GHCR, пин-борда](#период-2023082026--совместимость-28x322-ghcr-пин-борда)

</details>

---
<!-- /KB:HEAD -->

## Период 23.08–07.09.2025 — Bedolaga v2.0.x–2.2.x, Remnawave 2.1.x

- **Минимальный v2.6.x** [id=58548](https://t.me/c/2941121338/58548): `BOT_TOKEN=`, `ADMIN_IDS=`, `BOT_RUN_MODE=webhook`, `WEBHOOK_URL=https://hooks.domain.com`, `WEBHOOK_SECRET_TOKEN=`, `WEB_API_ENABLED=true`, `WEB_API_ALLOWED_ORIGINS=https://miniapp.example.com`.
- **БД/инфра**: `POSTGRES_DB/USER/PASSWORD`, `DATABASE_URL=postgresql+asyncpg://remnawave_user:...@postgres:5432/remnawave_bot`, `DATABASE_MODE=auto`, `REDIS_URL=redis://redis:6379/0`, `TZ=Europe/Moscow`, `LOCALES_PATH=./locales`, `WEB_API_HOST/PORT/DEFAULT_TOKEN/ALLOWED_ORIGINS/REQUEST_LOGGING`.
- **Remnawave**: `REMNAWAVE_API_URL=http://remnawave:3000`, `REMNAWAVE_SECRET_KEY=mykey:myvalue` [id=16559](https://t.me/c/2941121338/16559), `REMNAWAVE_AUTH_TYPE=api_key|basic_auth` [id=7374](https://t.me/c/2941121338/7374), `REMNAWAVE_USER_DESCRIPTION_TEMPLATE`, `REMNAWAVE_USER_USERNAME_TEMPLATE=user_{telegram_id}` [id=43238](https://t.me/c/2941121338/43238), `REMNAWAVE_AUTO_SYNC_ENABLED/TIMES` [id=27286](https://t.me/c/2941121338/27286).
- **Подписка/цены**: `TRAFFIC_SELECTION_MODE`, `FIXED_TRAFFIC_LIMIT_GB`, `PRICE_PER_DEVICE`, `BASE_SUBSCRIPTION_PRICE`, `PRICE_14/30/60/90/180/360_DAYS`, `AVAILABLE_SUBSCRIPTION_PERIODS/RENEWAL_PERIODS`, `DEFAULT_TRAFFIC_RESET_STRATEGY/LIMIT_GB/DEVICE_LIMIT`, `MAX_DEVICES_LIMIT`, `TRAFFIC_PACKAGES_CONFIG`, `TRIAL_DURATION_DAYS/TRIAL_TRAFFIC_LIMIT_GB/TRIAL_DEVICE_LIMIT/TRIAL_SQUAD_UUID` (с 2.6.1 флаг в списке серверов [id=59142](https://t.me/c/2941121338/59142)), `SIMPLE_SUBSCRIPTION_ENABLED/PERIOD_DAYS/DEVICE_LIMIT/TRAFFIC_GB/SQUAD_UUID` [id=28525](https://t.me/c/2941121338/28525), `DEVICES_SELECTION_ENABLED/DISABLED_AMOUNT` [id=43238](https://t.me/c/2941121338/43238), `AUTO_PURCHASE_AFTER_TOPUP_ENABLED` [id=34986](https://t.me/c/2941121338/34986), `DEFAULT_AUTOPAY_ENABLED` [id=23465](https://t.me/c/2941121338/23465).
- **Оплаты**: YooKassa `YOOKASSA_ENABLED/SHOP_ID/SECRET_KEY/RETURN_URL/DEFAULT_RECEIPT_EMAIL/SBP_ENABLED/VAT_CODE/PAYMENT_MODE/PAYMENT_SUBJECT/MIN/MAX/WEBHOOK_PATH/WEBHOOK_SECRET(empty)/WEBHOOK_HOST/QUICK_AMOUNT_SELECTION_ENABLED` [id=17846,55851](https://t.me/c/2941121338/17846); CryptoBot [id=4757](https://t.me/c/2941121338/4757); Pal24 `PAL24_ENABLED/API_KEY/SBP/CARD_BUTTON_VISIBLE`; Mulen `MULENPAY_ENABLED/SHOP_ID/API_KEY/DISPLAY_NAME`; WATA [id=27286,28320](https://t.me/c/2941121338/27286); Heleket [id=29203](https://t.me/c/2941121338/29203); Platega [id=59245](https://t.me/c/2941121338/59245); Stars `TELEGRAM_STARS_RATE_RUB=1.3` [id=1798](https://t.me/c/2941121338/1798).
- **Рефералка/промо**: `REFERRAL_*` [id=2054](https://t.me/c/2941121338/2054), `REFERRAL_PROGRAM_ENABLED` [id=27286](https://t.me/c/2941121338/27286), `DISPLAY_NAME_BANNED_KEYWORDS` [id=48624](https://t.me/c/2941121338/48624), `ADMIN_NOTIFICATIONS_*`, `VERSION_CHECK_*`, `BACKUP_*`, `SKIP_*`, `HIDE_SUBSCRIPTION_LINK`, `CHANNEL_*`, `SERVER_STATUS_*`, `PAYMENT_VERIFICATION_*`, `MINIAPP_*`, `CONNECT_BUTTON_MODE=guide|miniapp_subscription|miniapp_custom|link|happ_cryptolink` [id=20034,43801](https://t.me/c/2941121338/20034), `HAPP_CRYPTOLINK_REDIRECT_TEMPLATE` [id=20888](https://t.me/c/2941121338/20888), `MAIN_MENU_MODE` [id=25614](https://t.me/c/2941121338/25614).

## Период 12.11.2025–01.01.2026 — Bedolaga v2.7–2.9.4, Remnawave 2.3–2.4

### Минимальный .env бота (2.9.x канонический)
```
BOT_TOKEN=1234567890:AABBCCdd...
ADMIN_IDS=123456789,987654321
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=remnawave_bot
POSTGRES_USER=САМ_ГЕНЕРИРУЙ
POSTGRES_PASSWORD=САМ_ГЕНЕРИРУЙ
REDIS_URL=redis://redis:6379/0
REMNAWAVE_API_URL=https://example.com
REMNAWAVE_API_KEY=
REMNAWAVE_AUTH_TYPE=api_key
REMNAWAVE_USER_DESCRIPTION_TEMPLATE="Bot user: {full_name} {username}"
REMNAWAVE_USER_USERNAME_TEMPLATE="user_{telegram_id}"
REMNAWAVE_USER_DELETE_MODE=disable
BOT_RUN_MODE=webhook
WEBHOOK_URL=https://example.com
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET_TOKEN=САМ_ГЕНЕРИРУЙ
WEBHOOK_DROP_PENDING_UPDATES=true
WEBHOOK_MAX_QUEUE_SIZE=1024
WEBHOOK_WORKERS=4
WEBHOOK_ENQUEUE_TIMEOUT=0.1
WEBHOOK_WORKER_SHUTDOWN_TIMEOUT=30.0
WEB_API_ENABLED=true
WEB_API_HOST=0.0.0.0
WEB_API_PORT=8080
WEB_API_ALLOWED_ORIGINS=*
WEB_API_DOCS_ENABLED=false
WEB_API_DEFAULT_TOKEN=САМ_ГЕНЕРИРУЙ
AUTO_PURCHASE_AFTER_TOPUP_ENABLED=true
PAYMENT_VERIFICATION_AUTO_CHECK_ENABLED=true
PAYMENT_VERIFICATION_AUTO_CHECK_INTERVAL_MINUTES=2
```
[id=131104,128804,68063](https://t.me/c/2941121338/131104) Для webhook — `BOT_TOKEN`, `ADMIN_IDS`, `BOT_RUN_MODE=webhook`, `WEBHOOK_URL`, `WEBHOOK_PATH`, `WEBHOOK_SECRET_TOKEN` (`openssl rand -hex 32` [id=79229,100248](https://t.me/c/2941121338/79229)), `WEB_API_*`, `REMNAWAVE_API_URL/KEY` [id=67620,112179](https://t.me/c/2941121338/67620). Для панелей eGames доп.: `REMNAWAVE_SECRET_KEY=XXXXXXX:DDDDDDDD` (куки `aEmFnBcC=WbYWpixX`) [id=106223,131114](https://t.me/c/2941121338/106223). `TZ` → `TIMEZONE` в 2.9.4 [id=142219](https://t.me/c/2941121338/142219).

Приоритет env над БД — всё что в `.env` важнее админки; для правки через бота — закомментировать `#PRICE_30_DAYS=` [id=89503,96682,90828,134379,136037](https://t.me/c/2941121338/89503); пустая `PRICE_360_DAYS=` → ребут, комментировать целиком [id=89531](https://t.me/c/2941121338/89531); `sed -i 's|^PRICE_30_DAYS=|#PRICE_30_DAYS=|' .env && docker compose restart bot` [id=98621](https://t.me/c/2941121338/98621); inline `# коммент` после значения → `Input should be a valid integer` [id=84469](https://t.me/c/2941121338/84469).

Webhook-блок дословно [id=79180](https://t.me/c/2941121338/79180):
```
DEBUG=false
WEBHOOK_URL=https://bot.test.ru
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET_TOKEN=<32-hex, openssl rand -hex 16>
WEBHOOK_DROP_PENDING_UPDATES=true
WEBHOOK_MAX_QUEUE_SIZE=1024
WEBHOOK_WORKERS=4
WEBHOOK_ENQUEUE_TIMEOUT=0.1
WEBHOOK_WORKER_SHUTDOWN_TIMEOUT=30.0
BOT_RUN_MODE=webhook
```
Генерация: `openssl rand -hex 32` [id=79229](https://t.me/c/2941121338/79229).

### Платежки (env дословно)

YooKassa [id=80500](https://t.me/c/2941121338/80500):
```
YOOKASSA_ENABLED=true
YOOKASSA_SHOP_ID=112****
YOOKASSA_SECRET_KEY=live_SSO5***************
YOOKASSA_RETURN_URL=https://***.ru/payment_success
YOOKASSA_DEFAULT_RECEIPT_EMAIL=***@yandex.ru
```
Чек: description «Интернет-сервис - Пополнение баланса», vat_code 1, payment_mode full_payment, payment_subject service. Сети: 185.71.76.0/27, 185.71.77.0/27, 77.75.153.0/25, 77.75.154.128/25, 77.75.156.11/32, 77.75.156.35/32, 2a02:5180::/32 [id=113611](https://t.me/c/2941121338/113611); фикса: `YOOKASSA_TRUSTED_PROXY_NETWORKS=172.20.0.0/16` [id=120591](https://t.me/c/2941121338/120591) или `is_yookassa_ip_allowed→return True` + rebuild [id=113881](https://t.me/c/2941121338/113881).

Platega [id=115154,137757](https://t.me/c/2941121338/115154):
```
PLATEGA_ENABLED=true
PLATEGA_MERCHANT_ID=немногосимволов
PLATEGA_SECRET=многасимволов
PLATEGA_BASE_URL=https://app.platega.io
PLATEGA_RETURN_URL=https://t.me/мойбот
PLATEGA_FAILED_URL=https://t.me/мойбот
PLATEGA_CURRENCY=RUB
PLATEGA_ACTIVE_METHODS=2
PLATEGA_MIN_AMOUNT_KOPEKS=100
PLATEGA_MAX_AMOUNT_KOPEKS=100000000
PLATEGA_WEBHOOK_PATH=/platega-webhook
PLATEGA_WEBHOOK_HOST=0.0.0.0
PLATEGA_WEBHOOK_PORT=8086
```
`RETURN_URL` — `https://your-domain.com/payments/success` [id=115235](https://t.me/c/2941121338/115235); после смены env — `make reload` [id=115239](https://t.me/c/2941121338/115239).

WATA [id=67567,130507](https://t.me/c/2941121338/67567):
```
WATA_ACCESS_TOKEN=
WATA_BASE_URL=https://api.wata.pro/api/h2h
WATA_ENABLED=false
WATA_FAIL_REDIRECT_URL=
WATA_LINK_TTL_MINUTES=
WATA_MAX_AMOUNT_KOPEKS=100000000
WATA_MIN_AMOUNT_KOPEKS=10000
WATA_PAYMENT_DESCRIPTION=Пополнение баланса
WATA_PAYMENT_TYPE=OneTime
WATA_PUBLIC_KEY_CACHE_SECONDS=3600
WATA_PUBLIC_KEY_URL=
WATA_REQUEST_TIMEOUT=30
WATA_SUCCESS_REDIRECT_URL=
WATA_TERMINAL_PUBLIC_ID=
WATA_WEBHOOK_HOST=0.0.0.0
WATA_WEBHOOK_PATH=/wata-webhook
WATA_WEBHOOK_PORT=8085
```

MulenPay [id=84480](https://t.me/c/2941121338/84480):
```
MULENPAY_ENABLED=false
MULENPAY_API_KEY=
MULENPAY_SECRET_KEY=
MULENPAY_SHOP_ID=
MULENPAY_BASE_URL=https://mulenpay.ru/api
MULENPAY_WEBHOOK_PATH=/mulenpay-webhook
MULENPAY_DESCRIPTION="Пополнение баланса"
MULENPAY_LANGUAGE=ru
MULENPAY_VAT_CODE=0
MULENPAY_PAYMENT_SUBJECT=4
MULENPAY_PAYMENT_MODE=4
MULENPAY_MIN_AMOUNT_KOPEKS=10000
MULENPAY_MAX_AMOUNT_KOPEKS=10000000
```

Tribute [id=87637](https://t.me/c/2941121338/87637):
```
TRIBUTE_ENABLED=
TRIBUTE_API_KEY=
TRIBUTE_DONATE_LINK=
TRIBUTE_WEBHOOK_PATH=/tribute-webhook
TRIBUTE_WEBHOOK_HOST=0.0.0.0
```

CloudPayments 2.9.4 [id=143268](https://t.me/c/2941121338/143268): `/orders/create`, HMAC-SHA256 webhook.

НалогоГО 2.9.2+ [id=121296,132829,142206,142345](https://t.me/c/2941121338/121296):
```
NALOGO_ENABLED=false
NALOGO_INN=
NALOGO_PASSWORD=
NALOGO_DEVICE_ID=
NALOGO_STORAGE_PATH=./nalogo_tokens.json
NALOGO_QUEUE_CHECK_INTERVAL=300
NALOGO_QUEUE_RECEIPT_DELAY=3
NALOGO_QUEUE_MAX_ATTEMPTS=10
ADMIN_NOTIFICATIONS_NALOG_TOPIC_ID=
```
`NALOGO_DEVICE_ID` — `openssl rand -hex 32`.

Прочие 2.9.x [id=103051,121296,125758,142206,143268](https://t.me/c/2941121338/103051):
```
BLACKLIST_CHECK_ENABLED=false
BLACKLIST_GITHUB_URL=https://raw.githubusercontent.com/.../blacklist.txt
BLACKLIST_UPDATE_INTERVAL_HOURS=1
BLACKLIST_IGNORE_ADMINS=true
TRAFFIC_MONITORING_ENABLED=false
TRAFFIC_THRESHOLD_GB_PER_DAY=50
TRAFFIC_MONITORING_INTERVAL_HOURS=6
SUSPICIOUS_NOTIFICATIONS_TOPIC_ID=0
SUBSCRIPTION_RENEWAL_BALANCE_THRESHOLD_KOPEKS=20000
MENU_LAYOUT_ENABLED=false
CONTESTS_ENABLED=false
CONTESTS_BUTTON_VISIBLE=false
ENABLE_AUTOPAY=false
TIMEZONE=Europe/Moscow
REMNAWAVE_AUTH_TYPE=caddy
REMNAWAVE_CADDY_TOKEN=YWRtaW46cGFzc3dvcmQ=
BUY_TRAFFIC_BUTTON_VISIBLE=true
TRAFFIC_SELECTION_MODE=fixed
BACKUP_ARCHIVE_PASSWORD=
ADMIN_NOTIFICATIONS_ENABLED=true
ADMIN_NOTIFICATIONS_CHAT_ID=-1001234567890
ADMIN_NOTIFICATIONS_TOPIC_ID=123
ADMIN_NOTIFICATIONS_TICKET_TOPIC_ID=126
ADMIN_NOTIFICATIONS_NALOG_TOPIC_ID=133
ADMIN_REPORTS_ENABLED=false
ADMIN_REPORTS_CHAT_ID=
ADMIN_REPORTS_TOPIC_ID=
ADMIN_REPORTS_SEND_TIME=10:00
WEB_API_ALLOWED_ORIGINS=https://miniapp.domain.com
HAPP_CRYPTOLINK_REDIRECT_TEMPLATE=https://miniapp.domain.com/redirect/?redirect_to=
TRIAL_DURATION_DAYS=3
TRIAL_TRAFFIC_LIMIT_GB=10
TRIAL_DEVICE_LIMIT=1
TRIAL_PAYMENT_ENABLED=false
DISPLAY_NAME_BANNED_KEYWORDS=telegram.me, t.me/, @, support, admin, ...
HWID_DEVICE_LIMIT_ENABLED=true
HWID_FALLBACK_DEVICE_LIMIT=10
HWID_MAX_DEVICES_ANNOUNCE="Max devices reached"
BASE_SUBSCRIPTION_PRICE=0
SIMPLE_SUBSCRIPTION_SQUAD_UUID=<uuid>
MAIN_MENU_MODE=default|text
SUPPORT_USERNAME=
CHANNEL_IS_REQUIRED_SUB=False
DEFAULT_LANGUAGE=ru
AVAILABLE_LANGUAGES=ru
LANGUAGE_SELECTION_ENABLED=false
```
[id=104950,63441,81904,85171,119897,78677,128927,117575](https://t.me/c/2941121338/104950)

### Nginx/Caddy для хуков и панели

Caddy Valerii (30.11) — хуки+панель+сабка+miniapp [id=79181](https://t.me/c/2941121338/79181):
```caddy
apibot.домен {
  encode gzip zstd
  handle /yookassa-webhook { reverse_proxy remnawave_bot:8080 { header_up Host {host}; header_up X-Real-IP {remote_host}; transport http { read_buffer 0 } } }
  handle /platega-webhook { reverse_proxy remnawave_bot:8080 { header_up Host {host}; header_up X-Real-IP {remote_host}; transport http { read_buffer 0 } } }
  # аналогично: /cryptobot-webhook /wata-webhook /heleket-webhook /tribute-webhook /pal24-webhook /mulenpay-webhook
  handle /app-config.json { header Access-Control-Allow-Origin "*"; reverse_proxy remnawave_bot:8080 }
  handle { reverse_proxy remnawave_bot:8080 { header_up Host {host}; header_up X-Real-IP {remote_host} } }
}
miniapp.домен {
  encode gzip zstd
  handle /miniapp/* { reverse_proxy remnawave_bot:8080 }
  handle /app-config.json { header Access-Control-Allow-Origin "*"; reverse_proxy remnawave_bot:8080 }
  root * /var/www/remnawave-miniapp
  try_files {path} /index.html
  file_server
}
remna.домен { reverse_proxy * http://remnawave:3000 }
sub.домен { reverse_proxy http://remnawave-subscription-page:3010 { header_up X-Forwarded-Proto https; header_up X-Forwarded-Host {host} } }
```
Caddy hook/miniapp [id=120273](https://t.me/c/2941121338/120273):
```caddy
hook.my.store {
    encode gzip zstd
    @config path /app-config.json
    header @config Access-Control-Allow-Origin "*"
    reverse_proxy localhost:8080 { header_up Host {host}; header_up X-Real-IP {remote_host}; header_up X-Forwarded-Proto {scheme}; transport http { read_buffer 0 } }
}
miniapp.my.store {
    encode gzip zstd
    root * /miniapp; file_server
    @config path /app-config.json; header @config Access-Control-Allow-Origin "*"
    reverse_proxy /miniapp/* 127.0.0.1:8080 { header_up Host {host}; header_up X-Real-IP {remote_host} }
}
```

Nginx хуки+miniapp (06.12) дословно [id=91677](https://t.me/c/2941121338/91677):
```nginx
server {
    listen 80; listen 443 ssl http2;
    server_name hooks.domain.com;
    ssl_certificate /etc/ssl/private/hooks.fullchain.pem;
    ssl_certificate_key /etc/ssl/private/hooks.privkey.pem;
    client_max_body_size 32m;
    location = /yookassa-webhook { proxy_pass http://remnawave_bot_unified; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme; proxy_read_timeout 120s; proxy_send_timeout 120s; proxy_buffering off; proxy_request_buffering off; }
    # аналогично: /platega-webhook /cryptobot-webhook /wata-webhook /heleket-webhook /tribute-webhook /pal24-webhook /mulenpay-webhook
    location = /app-config.json { add_header Access-Control-Allow-Origin "*"; proxy_pass http://remnawave_bot_unified; }
    location / { proxy_pass http://remnawave_bot_unified; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme; }
}
server {
    listen 80; listen 443 ssl http2;
    server_name miniapp.domain.com;
    ssl_certificate /etc/ssl/private/miniapp.fullchain.pem;
    ssl_certificate_key /etc/ssl/private/miniapp.privkey.pem;
    client_max_body_size 32m;
    location /miniapp/ { proxy_pass http://remnawave_bot_unified; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme; }
    location = /app-config.json { add_header Access-Control-Allow-Origin "*"; proxy_pass http://remnawave_bot_unified; }
    location / { root /var/www/remnawave-miniapp; try_files $uri $uri/ /index.html; expires 1h; add_header Cache-Control "public, immutable"; }
}
server { listen 443 ssl default_server; listen [::]:443 ssl default_server; server_name _; ssl_reject_handshake on; }
```
Основной nginx [id=101409](https://t.me/c/2941121338/101409):
```nginx
user nginx; worker_processes auto; error_log /var/log/nginx/error.log warn; pid /var/run/nginx.pid;
events { worker_connections 1024; }
http { include /etc/nginx/mime.types; default_type application/octet-stream; upstream remnawave_bot { server 127.0.0.1:8080; } include /etc/nginx/conf.d/*.conf; }
```
Для host-режима бот `127.0.0.1:8080`, путь `/miniapp:/miniapp:ro` [id=119681](https://t.me/c/2941121338/119681); после правки `docker container restart remnawave-nginx` [id=101653](https://t.me/c/2941121338/101653); `server_names_hash_bucket_size 64;` в http при `could not build server_names_hash` [id=114513](https://t.me/c/2941121338/114513).
Проверка хуков: `curl https://домен/health/unified` [id=79200](https://t.me/c/2941121338/79200); `curl -X POST http://localhost:8080/yookassa-webhook -H "X-Forwarded-For: 77.75.153.78" -d '{ "event": "payment.succeeded" }'` [id=120647](https://t.me/c/2941121338/120647); `curl -s -o /dev/null -w "%{http_code}" https://api.telegram.org` 302=норм [id=143900](https://t.me/c/2941121338/143900).

## Период 09.02–13.03.2026 — Bedolaga v3.9–3.32, Remnawave 2.6.x, Remnawave-admin 2.x

Remnawave webhook панель:
```
WEBHOOK_ENABLED=true
WEBHOOK_URL=https://hooks.domain.ru/remnawave-webhook
WEBHOOK_SECRET_HEADER=<64-значный a-z0-9A-Z>
```
[id=216359, 238125](https://t.me/c/2941121338/216359)

Bedolaga webhook:
```
REMNAWAVE_WEBHOOK_ENABLED=true
REMNAWAVE_WEBHOOK_PATH=/remnawave-webhook
REMNAWAVE_WEBHOOK_SECRET=<openssl rand -hex 32>
```
[id=216158](https://t.me/c/2941121338/216158)

12 уведомлений:
```
WEBHOOK_NOTIFY_USER_ENABLED=true
WEBHOOK_NOTIFY_SUB_STATUS=true
WEBHOOK_NOTIFY_SUB_EXPIRED=true
WEBHOOK_NOTIFY_SUB_EXPIRING=true
WEBHOOK_NOTIFY_SUB_LIMITED=true
WEBHOOK_NOTIFY_SUB_DELETED=true
WEBHOOK_NOTIFY_SUB_REVOKED=true
WEBHOOK_NOTIFY_TRAFFIC_RESET=true
WEBHOOK_NOTIFY_BANDWIDTH_THRESHOLD=true
WEBHOOK_NOTIFY_FIRST_CONNECTED=true
WEBHOOK_NOTIFY_NOT_CONNECTED=true
WEBHOOK_NOTIFY_DEVICES=true
```
[id=220923](https://t.me/c/2941121338/220923)

Кабинет режим полный:
```
MAIN_MENU_MODE=cabinet
CABINET_BUTTON_STYLE=primary
MENU_LAYOUT_ENABLED=false
CONNECT_BUTTON_MODE=miniapp_custom
MINIAPP_CUSTOM_URL=https://cabinet.example.com
CABINET_ENABLED=true
CABINET_URL=https://cabinet.example.com
CABINET_JWT_SECRET=<secret>
CABINET_ALLOWED_ORIGINS=https://cabinet.example.com
```
[id=235078, 256333](https://t.me/c/2941121338/235078)

Приоритет: .env > админка [id=244061](https://t.me/c/2941121338/244061). VITE_* — build-time [id=222460](https://t.me/c/2941121338/222460).

## Период 16.03–06.04.2026 — Remnawave 2.7.x (breaking), Bedolaga v3.33–3.45

- Приоритет .env > БД [id=306420](https://t.me/c/2941121338/306420); для изменения из кабинета — удалить из .env [id=312970; id=327709](https://t.me/c/2941121338/312970); минимальный .env [id=330294](https://t.me/c/2941121338/330294); ADMIN_REPORTS_TOPIC_ID приоритет env [id=282901](https://t.me/c/2941121338/282901); CABINET_URL обязателен [id=283143](https://t.me/c/2941121338/283143).
- Мультиподписка: `SALES_MODE=tariffs; MULTI_TARIFF_ENABLED=true; MAX_ACTIVE_SUBSCRIPTIONS=10` [id=309211; id=316682](https://t.me/c/2941121338/309211); дока multi-tariff [id=309213](https://t.me/c/2941121338/309213).
- Только Stars: `TELEGRAM_STARS_ENABLED=true; TELEGRAM_STARS_RATE_RUB=1.79` [id=312642; id=312647](https://t.me/c/2941121338/312642).
- Логи: LOG_DIR/LOG_INFO_FILE/WARNING/ERROR/PAYMENTS [id=310362](https://t.me/c/2941121338/310362).
- Меню: MAIN_MENU_MODE default|cabinet (+MINIAPP_CUSTOM_URL), CABINET_BUTTON_STYLE, MENU_LAYOUT_ENABLED [id=318275](https://t.me/c/2941121338/318275); MENU_LAYOUT_ENABLED=true для БД [id=275973](https://t.me/c/2941121338/275973) vs false для кастомных кнопок [id=305733; id=294738; id=321034](https://t.me/c/2941121338/305733).
- Прокси: PROXY_URL, NALOGO_PROXY_URL fallback [id=283012; id=283100](https://t.me/c/2941121338/283012); дока proxy-setup [id=315627](https://t.me/c/2941121338/315627).
- Кабина/API: WEB_API_DEFAULT_TOKEN, CABINET_JWT_SECRET [id=278527](https://t.me/c/2941121338/278527); Webhook_url/Web_api_allowed_origins [id=317217](https://t.me/c/2941121338/317217).
- Фронт: VITE_API_URL=/api, VITE_TELEGRAM_BOT_USERNAME без @, VITE_APP_NAME/LOGO только вариант Б [id=307095; id=287918; id=307092](https://t.me/c/2941121338/307095).
- OIDC: TELEGRAM_OIDC_ENABLED/CLIENT_ID/SECRET [id=282915; id=284521](https://t.me/c/2941121338/282915).
- Remnawave: REMNAWAVE_USER_USERNAME_TEMPLATE, REMNAWAVE_AUTH_TYPE=caddy+CADDY_TOKEN [id=309384; id=276169](https://t.me/c/2941121338/309384); DEFAULT_TRAFFIC_RESET_STRATEGY=DAY; NALOGO_STORAGE_PATH [id=286690](https://t.me/c/2941121338/286690).
- Платежи: PLATEGA_MIN_AMOUNT_KOPEKS, PLATEGA_RETURN_URL/FAILED_URL, WATA_FAIL/SUCCESS_REDIRECT_URL [id=277219; id=291608](https://t.me/c/2941121338/277219); PLATEGA_SECRET/DISPLAY_NAME [id=316762](https://t.me/c/2941121338/316762); WATA_PAYMENT_TYPE [id=284234](https://t.me/c/2941121338/284234); YOOKASSA_SBP/RECURRENT [id=318375](https://t.me/c/2941121338/318375).
- BOT_RUN_MODE webhook→polling [id=281045; id=304023](https://t.me/c/2941121338/281045); INACTIVE_USER_DELETE_MONTHS 3 [id=322411](https://t.me/c/2941121338/322411); SIMPLE_SUBSCRIPTION_ENABLED, CONNECT_BUTTON_MODE, HAPP_CRYPTOLINK_REDIRECT_TEMPLATE [id=316345; id=316350; id=316247](https://t.me/c/2941121338/316345).
- Пуши RWA: WEBHOOK_ENABLED, WEBHOOK_URL (запятая), WEBHOOK_SECRET_HEADER не менять + restart панели [id=313606; id=314971](https://t.me/c/2941121338/313606).
- Пустые env ломают старт: ADMIN_REPORTS_TOPIC_ID, MULENPAY_SHOP_ID, FREEKASSA_*, KASSA_AI_SHOP_ID, LOG_ROTATION_TOPIC_ID [id=315636; id=305573](https://t.me/c/2941121338/315636).
- SMTP: SMTP_FROM_EMAIL=SMTP_USER, порт 587 mail.ru [id=284210; id=325473](https://t.me/c/2941121338/284210).

## Период 06–25.04.2026 — Bedolaga v3.45–3.52, Remnawave-admin 2.9–2.11

### Бот + панель (один сервер, webhook) [id=343457,343482,343497](https://t.me/c/2941121338/343457)
```
REMNAWAVE_API_URL=http://remnawave:3000
WEBHOOK_ENABLED=true
WEBHOOK_URL=https://hooks.domain.com/remnawave-webhook
WEBHOOK_SECRET_HEADER=secret_key  (либо REMNAWAVE_WEBHOOK_SECRET=secret)
```

### Overpay v3.51.0 (16 переменных) [id=392083|23.04.2026](https://t.me/c/2941121338/392083)
```
OVERPAY_ENABLED=false
OVERPAY_USERNAME=
OVERPAY_PASSWORD=
OVERPAY_PROJECT_ID=
OVERPAY_P12_PATH=/app/certs/client.p12
OVERPAY_P12_PASSPHRASE=
OVERPAY_API_URL=https://api.overpay.io
OVERPAY_PAYMENT_METHODS=card,fps
OVERPAY_DISPLAY_NAME=Overpay
OVERPAY_CURRENCY=RUB
OVERPAY_MIN_AMOUNT_KOPEKS=10000
OVERPAY_MAX_AMOUNT_KOPEKS=100000
OVERPAY_WEBHOOK_PATH=/overpay-webhook
OVERPAY_RETURN_URL=свой_юрл
OVERPAY_LIFETIME_MINUTES=1440
```

### RollyPay [id=399154|24.04.2026](https://t.me/c/2941121338/399154)
```
ROLLYPAY_ENABLED=false
ROLLYPAY_API_KEY=
ROLLYPAY_SIGNING_SECRET=
ROLLYPAY_DISPLAY_NAME=RollyPay
ROLLYPAY_CURRENCY=RUB
ROLLYPAY_MIN_AMOUNT_KOPEKS=10000
ROLLYPAY_MAX_AMOUNT_KOPEKS=10000000
ROLLYPAY_WEBHOOK_PATH=/rollypay-webhook
```

### Пример env подписок [id=384935|21.04.2026](https://t.me/c/2941121338/384935)
```
SALES_MODE=classic
AVAILABLE_SUBSCRIPTION_PERIODS=30,90,180
AVAILABLE_RENEWAL_PERIODS=30,90,180
PRICE_30_DAYS=20000  # 200₽ = 20000 копеек
PRICE_90_DAYS=60000
PRICE_180_DAYS=120000
TRAFFIC_SELECTION_MODE=fixed
FIXED_TRAFFIC_LIMIT_GB=100
TRAFFIC_TOPUP_ENABLED=true
BUY_TRAFFIC_BUTTON_VISIBLE=true
DEFAULT_DEVICE_LIMIT=1
TRIAL_DURATION_DAYS=1
TRIAL_TRAFFIC_LIMIT_GB=10
TRIAL_DEVICE_LIMIT=1
```

### Кнопки кабины [id=400574|25.04.2026](https://t.me/c/2941121338/400574)
```
MINIAPP_CUSTOM_URL=https://cabinet.<домен>
MINIAPP_STATIC_PATH=miniapp
MINIAPP_SERVICE_NAME_EN=
MINIAPP_SERVICE_NAME_RU=
MAIN_MENU_MODE=cabinet
CABINET_BUTTON_STYLE=success
MENU_LAYOUT_ENABLED=false
```

### Прочие env (дословно из чата)
```
WEB_API_TOKEN_HMAC_SECRET  # None→plain sha256, set→HMAC-SHA256; openssl rand -hex 16 [id=333799,335936](https://t.me/c/2941121338/333799)
REDIS_URL=redis://redis:6379/0  # фикс MissingGreenlet [id=338750](https://t.me/c/2941121338/338750)
PRICE_PER_DEVICE=3000
DEVICES_SELECTION_ENABLED=true
PROXY_URL=socks5://user:pass@45.1.1.1:8000  # ТГ API с ру-хостов [id=347156](https://t.me/c/2941121338/347156)
HWID_DEVICE_LIMIT_ENABLED=true  # панель Remnawave [id=356134](https://t.me/c/2941121338/356134)
MAX_DEVICES_LIMIT  # бот [id=356134](https://t.me/c/2941121338/356134)
AUTO_PURCHASE_AFTER_TOPUP_ENABLED=true  [id=358287](https://t.me/c/2941121338/358287)
CHANNEL_IS_REQUIRED_SUB=true  [id=373394](https://t.me/c/2941121338/373394)
BLACKLIST_CHECK_ENABLED=true
BLACKLIST_GITHUB_URL=https://github.com/BEDOLAGA-DEV/VPN-BLACKLIST/blob/main/blacklist.txt  [id=371253](https://t.me/c/2941121338/371253)
ADMIN_NOTIFICATIONS_CHAT_ID  # chat not found если пусто [id=386585](https://t.me/c/2941121338/386585)
NALOGO_INN / NALOGO_PASSWORD / NALOGO_DEVICE_ID  [id=390199](https://t.me/c/2941121338/390199)
CABINET_EMAIL_AUTH_ENABLED=true / TEST_EMAIL / TEST_EMAIL_PASSWORD  [id=388772](https://t.me/c/2941121338/388772)
DEFAULT_TRAFFIC_RESET_STRATEGY  # месяц/ежедневно/не сбрасывать [id=391238](https://t.me/c/2941121338/391238)
REMNAWAVE_USER_USERNAME_TEMPLATE="{username}"  # "{full_name}"→too_small 3 [id=389121](https://t.me/c/2941121338/389121)
CABINET_URL=  # для yookassa return_url [id=341428](https://t.me/c/2941121338/341428)
YOOKASSA_RETURN_URL=https://t.me/name_bot/subscription  [id=341157](https://t.me/c/2941121338/341157)
WEB_API_DEFAULT_TOKEN  # мини-апп=кабина [id=344273,398709](https://t.me/c/2941121338/344273)
CABINET_ENABLED=true  # false внизу перебивает true вверху [id=380347](https://t.me/c/2941121338/380347)
VITE_API_URL / VITE_TELEGRAM_BOT_USERNAME  # без @ [id=380619,372877](https://t.me/c/2941121338/380619)
REMNAWAVE_SECRET_KEY=XXXXXXX:DDDDDDDD  # eGames-панели [id=393391](https://t.me/c/2941121338/393391)
```
- Что менять через UI — убрать из .env [id=397978,396419](https://t.me/c/2941121338/397978).

## Период 25.04–15.05.2026 — Bedolaga v3.49–3.55, Cabinet 1.49–1.52

### Интерфейс и UX (дословно) [id=401587–401792, 25.04](https://t.me/c/2941121338/401587)
```env
# ===== ИНТЕРФЕЙС И UX =====
ENABLE_LOGO_MODE=true
LOGO_FILE=vpn_logo.png
MAIN_MENU_MODE=cabinet        # default | cabinet (требует MINIAPP_CUSTOM_URL; алиасы: text, text_only, minimal)
CABINET_BUTTON_STYLE=primary  # primary|success|danger|'' (Bot API 9.4)
MENU_LAYOUT_ENABLED=false     # управление меню через API
HIDE_SUBSCRIPTION_LINK=false  # влияет и на кнопку copyButton в кабинете (id=402241 Sayonara)
CONNECT_BUTTON_MODE=miniapp_custom
# guide | miniapp_subscription | miniapp_custom | link | happ_cryptolink
MINIAPP_CUSTOM_URL=https://miniapp.example.com
MINIAPP_STATIC_PATH=miniapp
# MINIAPP_PURCHASE_URL=
MINIAPP_SERVICE_NAME_EN=... / MINIAPP_SERVICE_NAME_RU=...
MINIAPP_SERVICE_DESCRIPTION_EN=... / _RU=...
CONNECT_BUTTON_HAPP_DOWNLOAD_ENABLED=false
HAPP_DOWNLOAD_LINK_IOS= HAPP_DOWNLOAD_LINK_ANDROID= HAPP_DOWNLOAD_LINK_MACOS= HAPP_DOWNLOAD_LINK_WINDOWS=
HAPP_DOWNLOAD_LINK_PC=
HAPP_CRYPTOLINK_REDIRECT_TEMPLATE=   # happ:// ссылки ТГ не поддерживает — нужен редирект-шаблон
SKIP_RULES_ACCEPT=false
SKIP_REFERRAL_CODE=false
```
- Переключение бота в режим кабинета не работает без `MENU_LAYOUT_ENABLED=false` («надо false поставить, не спрашивай почему»), иначе кнопки остаются в боте [id=401587–401792](https://t.me/c/2941121338/401587). Менять цвет кнопок — через `MENU_LAYOUT false` [id=417306, 417632](https://t.me/c/2941121338/417306).
- `LANGUAGE_SELECTION_ENABLED` и `SKIP_RULES_ACCEPT` отключают выбор языка и правила [id=417579, 420291](https://t.me/c/2941121338/417579).
- Новая miniapp (как у ZeroPing) появляется только при установленном кабинете; из .env одного не достаточно [id=401633, 402177](https://t.me/c/2941121338/401633).
- Кастомные кнопки бота работают только в режиме меню «Кабинет» (иначе править `app/localization/locales/ru.json`) [id=405697](https://t.me/c/2941121338/405697).
- Режим кабинета: где выставить — в BotFather (menu button) или в env (`MAIN_MENU_MODE`) [id=412829](https://t.me/c/2941121338/412829).
- `CONNECT_BUTTON_MODE=miniapp_subscription` → `link` — фикс кнопки «Подключиться» в TG-миниапп (не открывает happ://) [id=483239, 482813](https://t.me/c/2941121338/483239).

### WEBHOOK [id=427502, 414748, 436471](https://t.me/c/2941121338/427502)
```env
WEBHOOK_URL=https://...
WEBHOOK_SECRET_HEADER=
WEBHOOK_IP=х.х.х.х          # с 3.50
```
«Бот, запущенный в поллинг-шаблоне, вебхуки принимать физически не может; для вебхуков изначально нужно брать шаблон для вебхуков» [id=414748](https://t.me/c/2941121338/414748). При этом «у меня все на пулинге и вебхуки (от платежек) приходят» [id=435137, 435140](https://t.me/c/2941121338/435137).

### SMTP (классический пример) [id=447566](https://t.me/c/2941121338/447566)
```env
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=587
SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=app_password_here
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=My VPN Service
SMTP_USE_TLS=true
```

### Кабинет / авторизация [id=446652, 446650, 505559, 463147, 458641, 435273, 432946](https://t.me/c/2941121338/446652)
```env
TELEGRAM_OIDC_CLIENT_ID=           # добавить самому в .env бота
TELEGRAM_OIDC_ENABLED=false        # отключить вход через Telegram в ЛК (применять docker compose down/up)
CABINET_ALLOWED_ORIGINS=           # можно добавить dns имя cdn
PROXY_URL=socks5://...
```
- Домен для веблогина правится в .env бота (не в панели) [id=446650](https://t.me/c/2941121338/446650).
- Trusted Origins в BotFather — добавить ссылку на кабину; без него `redirect_uri required` [id=463147](https://t.me/c/2941121338/463147); виджет deprecated → OpenID Connect Login; Redirect URI `https://cabinet.example.com/auth/telegram/callback`.
- Правильные колбэки кабинета [id=447538](https://t.me/c/2941121338/447538): `https://кабина.домен.top/auth/telegram/callback` и `https://кабина.домен.top/login/`; после правки — `make reload-follow` у бота [id=447546, 447550](https://t.me/c/2941121338/447546).
- Кабинет на отдельном домене + бот в обычном режиме — совместимо: «Можно. У тебя и кабинет будет и бот обычный» [id=430048, 430050](https://t.me/c/2941121338/430048).
- Запрет регистрации по email (оставить привязку/логин) — env кабины [id=463522, 463548](https://t.me/c/2941121338/463522).

### Платёжные переменные и webhook-пути (это настройка бота — включено)
```env
ROLLYPAY_ENABLED=true                                        # [id=457569](https://t.me/c/2941121338/457569)
PLATEGA_WEBHOOK_PATH=/platega-webhook                        # просто путь [id=417306](https://t.me/c/2941121338/417306)
YOOKASSA_DEFAULT_RECEIPT_EMAIL=                              # [id=418134](https://t.me/c/2941121338/418134) нарушает 54-ФЗ: чек должен идти на email покупателя
MULENPAY_SHOP_ID=           # 0 или закомментировать [id=491327, 470047](https://t.me/c/2941121338/491327)
FREEKASSA_SHOP_ID=          # обязательны к заполнению/комментарию [id=470047](https://t.me/c/2941121338/470047)
FREEKASSA_PAYMENT_SYSTEM_ID=# [id=470047](https://t.me/c/2941121338/470047)
KASSA_AI_SHOP_ID=           # [id=470047](https://t.me/c/2941121338/470047)
SEVERPAY_MID=               # [id=470047](https://t.me/c/2941121338/470047)
ADMIN_REPORTS_TOPIC_ID=     # fast-start требует заполнения либо комментирования [id=470047](https://t.me/c/2941121338/470047)
LOG_ROTATION_TOPIC_ID=      # [id=470047](https://t.me/c/2941121338/470047)
CRYPTOBOT_WEBHOOK_SECRET=   # сам назначаешь надёжную секретную строку, валидишь хук по хедеру [id=461498, 461932, 461944](https://t.me/c/2941121338/461498)
LAVA_BASE_URL=https://api.lava.ru    # в lava_service.py указан несуществующий gate.lava.ru [id=497090, 497809](https://t.me/c/2941121338/497090)
REMNAWAVE_WEBHOOK_PATH=/... # тот же путь, что и в панели; это HTTP-путь вебхука на сервере бота, папка не создаётся [id=497500](https://t.me/c/2941121338/497500)
```
**Webhook-эндпоинты/пути:** порт общий **8080** для всех вебхуков [id=412310](https://t.me/c/2941121338/412310); «8082 устаревший порт, все вебхуки сидят на 8080 теперь, не отдельно» [id=419838, 419860](https://t.me/c/2941121338/419838); порт брать из локалки контейнера, наружу открывать не нужно [id=419871, 419874](https://t.me/c/2941121338/419871); обычно заводят отдельный поддомен `hooks.domain.com`, у каждой платёжки свой суффикс `hooks.domain.com/platega-webhook` [id=416980](https://t.me/c/2941121338/416980); схема: поддомен `pay.domain.com` → сервер, в Caddy прокси на бедолагу на порт 8080 [id=427840](https://t.me/c/2941121338/427840); проверка вебхука в браузере должна отдавать `{"status":"ok","service":"platega_webhook","enabled":true}` [id=417306, 416851](https://t.me/c/2941121338/417306); RollyPay webhook: `https://hooks.domain.com/rollypay-webhook` настраивается при создании кассы (terminal) [id=424623](https://t.me/c/2941121338/424623); интеграция встроена: Platega, YooKassa, Lava, Wata, PayPalych, Heleket, Triton; крипта — CryptoBot, CryptoCloud [id=498772](https://t.me/c/2941121338/498772).

### Blacklist / триалы / лимиты [id=513772, 511104, 402475, 404025](https://t.me/c/2941121338/513772)
```env
BLACKLIST_CHECK_ENABLED=true
BLACKLIST_GITHUB_URL=https://raw.githubusercontent.com/Blin4ickUSE/ban-vpn/refs/heads/main/blacklist.txt
BLACKLIST_UPDATE_INTERVAL_HOURS=24
BLACKLIST_IGNORE_ADMINS=true
SUBSCRIPTION_RENEWAL_BALANCE_THRESHOLD_KOPEKS=20000
TRIAL_TRAFFIC_LIMIT_GB=0        # даёт 100ГБ, а НЕ безлимит [id=402475, 402435](https://t.me/c/2941121338/402475)
TARIFF_SWITCH_UPGRADE_ENABLED=false    # [id=495618](https://t.me/c/2941121338/495618) игнорируется при включённой мультиподписке [id=402486](https://t.me/c/2941121338/402486)
TARIFF_SWITCH_DOWNGRADE_ENABLED=false  # [id=495618](https://t.me/c/2941121338/495618)
INACTIVE_USER_DELETE_MONTHS=3   # crud/user.py:1213 ставит DELETED; предложить поднять до 12 [id=508499](https://t.me/c/2941121338/508499)
DEVICES_SELECTION_DISABLED_AMOUNT=0    # [id=475512](https://t.me/c/2941121338/475512) влиять на все тарифы, шлёт в ремну после синхры при DEVICES_SELECTION_ENABLED=false
DEVICE_SELECTION_ENABLE=               # включить — пропадает MissingGreenlet [id=451538](https://t.me/c/2941121338/451538)
REFERRAL_PROGRAM_ENABLED=true          # [id=469723](https://t.me/c/2941121338/469723) баг: в кабинете не включается, в боте говорит «включено», кнопки у юзеров нет
MENU_LAYOUT_ENABLED=false
LOCALES=ru,en                          # [id=498871](https://t.me/c/2941121338/498871) nano .env из папки бота; если .env пуст — cp .env.example .env
```

### Связка с панелью [id=458722, 433864, 458367](https://t.me/c/2941121338/458722)
```env
REMNAWAVE_API_URL=https://panel.example.com   # без /api; «пробовал также /api» → API Error 404
REMNAWAVE_API_KEY=your_api_key_here
WEB_API_DEFAULT_TOKEN=                        # генерировать в панели [id=436536](https://t.me/c/2941121338/436536); health-check ≠ валидный токен [id=469546](https://t.me/c/2941121338/469546)
```
«Бот не видит ремень. Проверяй апи ключ» [id=427566](https://t.me/c/2941121338/427566).

### ENV → БД миграция приоритета (канон)
- **.env переопределяет настройки из БД/кабины**: «Из кабины невозможно перезаписать переменные, которые указаны в .env» [id=412047](https://t.me/c/2941121338/412047); «если .env полный (на миллион строк) — настройки можно менять только через енв; при минимальном .env настройки хранятся в БД и меняются через бота/кабину когда угодно» [id=416952](https://t.me/c/2941121338/416952); «.env > настройки из БД» [id=464822](https://t.me/c/2941121338/464822); «В документации есть минимальный .env — используй его, потому что настройки из env приоритетнее» [id=473917, 470548](https://t.me/c/2941121338/473917); «Если не меняется из UI — меняется в .env (правило для всех настроек)» [id=470419](https://t.me/c/2941121338/470419); «параметры, заданные в env, НЕ переопределяются из админки бота (кнопки работают только там, где не задано в env)» [id=492321](https://t.me/c/2941121338/492321); «+у енв приоритет, а если надо новую платёжку подключить, то мне не надо редачить енв» [id=434360](https://t.me/c/2941121338/434360); «Автоматом применение новых переменных, читаем ченджлоги» [id=434356, 434358](https://t.me/c/2941121338/434356).
- Практика: «У тебя куча полей в .env которые не заполнены» → «Я закомментировал все ненужные мне» [id=460688, 460696](https://t.me/c/2941121338/460688); «просто енв удали и заново заполни» [id=458091](https://t.me/c/2941121338/458091); «не чисти ничего, переименуй старый большой енв, создай новый минимальный, задай нужные значения и рестартуй down → up с билдом» [id=507041](https://t.me/c/2941121338/507041).
- Был прецедент несостыковки: «при включении rollypay и перезапуске бота значение меняется на enabled, но превью кнопки платёжных систем горит красным» [id=433241](https://t.me/c/2941121338/433241).

### Локализация / файлы
- `LOCALES=ru,en` в .env [id=498871](https://t.me/c/2941121338/498871); тексты, доступные пользователю — `bedolaga/app/localization/locales/ru.json` [id=454414, 454431](https://t.me/c/2941121338/454414); кастомные кнопки вне режима кабинета — дрочить локали [id=405697](https://t.me/c/2941121338/405697).
- Логотип: `vpn_logo.jpg`/`vpn_logo.png` в корне проекта бота [id=405074, 405056](https://t.me/c/2941121338/405074); `LOGO_FILE=vpn_logo.png` + `ENABLE_LOGO_MODE=true`.
- Кастомные (премиум) emoji — тег `<tg-emoji emoji-id="5287571024500498635">☁️</tg-emoji>`, экранировать кавычки, вставлять в json локализации; ID искать через @FIND_STICKER_ID_BOT / @Emoji_ID_Extractor_bot [id=446522, 446526, 446536–446539, 495751](https://t.me/c/2941121338/446522).

---

## Период 16.05–05.06.2026 — Bedolaga v3.56–3.58, Remnawave-admin 2.14

- Минимальный .env Bedolaga [id=642487](https://t.me/c/2941121338/642487):
```ini
BOT_TOKEN=
ADMIN_IDS=

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=remnawave_bot
POSTGRES_USER=
POSTGRES_PASSWORD=

REDIS_URL=redis://redis:6379/0

REMNAWAVE_API_URL=
REMNAWAVE_API_KEY=
REMNAWAVE_AUTH_TYPE=api_key
REMNAWAVE_USER_DESCRIPTION_TEMPLATE="Bot user: {full_name} {username}"
REMNAWAVE_USER_USERNAME_TEMPLATE="user_{telegram_id}"
REMNAWAVE_USER_DELETE_MODE=disable

BOT_RUN_MODE=webhook
WEBHOOK_URL=
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET_TOKEN=
WEBHOOK_DROP_PENDING_UPDATES=true
WEBHOOK_MAX_QUEUE_SIZE=1024
WEBHOOK_WORKERS=4
WEBHOOK_ENQUEUE_TIMEOUT=0.1
WEBHOOK_WORKER_SHUTDOWN_TIMEOUT=30.0

WEB_API_ENABLED=true
WEB_API_HOST=0.0.0.0
WEB_API_PORT=8080
WEB_API_ALLOWED_ORIGINS=
WEB_API_DOCS_ENABLED=false
WEB_API_DEFAULT_TOKEN=

AUTO_PURCHASE_AFTER_TOPUP_ENABLED=true
PAYMENT_VERIFICATION_AUTO_CHECK_ENABLED=true
PAYMENT_VERIFICATION_AUTO_CHECK_INTERVAL_MINUTES=2

CABINET_ENABLED=true
CABINET_URL=
CABINET_JWT_SECRET=
CABINET_ALLOWED_ORIGINS=
```
Совет: ставить чистый минимальный env + добавить кабину, остальное в веб-админке [id=642481](https://t.me/c/2941121338/642481)[id=624887](https://t.me/c/2941121338/624887).
- Связка доменов [id=565026](https://t.me/c/2941121338/565026):
```
CABINET_ALLOWED_ORIGINS=https://cabinet.example.com
WEBHOOK_URL=https://hooks.domain.com
WEB_API_ALLOWED_ORIGINS=https://miniapp.domain.com
MINIAPP_CUSTOM_URL=https://cabinet.example.com
```
- Режим кабинета кнопок [id=565758](https://t.me/c/2941121338/565758):
```
LAYOUT_MENU_MODE=cabinet
MAIN_MENU_MODE=cabinet
CABINET_BUTTON_STYLE=primary
MENU_LAYOUT_ENABLED=true
CONNECT_BUTTON_MODE=link
```
Откат `MENU_LAYOUT_ENABLED=false` [id=535045](https://t.me/c/2941121338/535045); `CABINET_ENABLED=true` [id=535041](https://t.me/c/2941121338/535041).
- Платежные webhook env: `PLATEGA_WEBHOOK_PATH=/platega-webhook`, `PLATEGA_WEBHOOK_HOST=0.0.0.0`, `PLATEGA_WEBHOOK_PORT=8080`, `PLATEGA_ACTIVE_METHODS=2` [id=625237](https://t.me/c/2941121338/625237); `YOOKASSA_WEBHOOK_PATH=/yookassa-webhook`, `YOOKASSA_WEBHOOK_HOST=0.0.0.0`, `YOOKASSA_WEBHOOK_PORT=8082`, `YOOKASSA_TRUSTED_PROXY_NETWORKS=185.71.76.0/24,185.71.77.0/24` [id=631299](https://t.me/c/2941121338/631299); Lava `LAVA_BASE_URL=https://api.lava.ru` [id=516957](https://t.me/c/2941121338/516957); `VITE_TELEGRAM_BOT_USERNAME=` в кабине [id=534790](https://t.me/c/2941121338/534790).
- Webhook проверка: `curl -X POST https://поддомен_кабинета/вебхук` → success [id=564804](https://t.me/c/2941121338/564804)[id=569598](https://t.me/c/2941121338/569598).
- `WEB_API_DEFAULT_TOKEN` генерировать `openssl rand -hex 32` [id=541474](https://t.me/c/2941121338/541474); .env приоритет выше БД [id=552453](https://t.me/c/2941121338/552453).

## Период 07–26.06.2026 — Bedolaga 3.60–3.61, Subscription-page 7.2.5/7.2.6

### Platega [id=719199|19.06.2026](https://t.me/c/2941121338/719199)
```ini
PLATEGA_ENABLED=true
PLATEGA_MERCHANT_ID=...
PLATEGA_SECRET=...
PLATEGA_BASE_URL=https://app.platega.io
PLATEGA_DISPLAY_NAME=Platega
PLATEGA_RETURN_URL=https://<ссылка на кабинет>
PLATEGA_FAILED_URL=https://<ссылка на кабинет>
PLATEGA_CURRENCY=RUB
PLATEGA_ACTIVE_METHODS=2,11,12,13
PLATEGA_MIN_AMOUNT_KOPEKS=100
PLATEGA_MAX_AMOUNT_KOPEKS=100000000
PLATEGA_WEBHOOK_PATH=/platega-webhook
PLATEGA_WEBHOOK_HOST=0.0.0.0
PLATEGA_WEBHOOK_PORT=8086
```

### Antilopay [id=663727](https://t.me/c/2941121338/663727)
```ini
ANTILOPAY_ENABLED=true
ANTILOPAY_SECRET_ID=your_secret_id
ANTILOPAY_PRIVATE_KEY=base64_encoded_rsa_private_key
ANTILOPAY_PUBLIC_KEY=base64_encoded_rsa_public_key
ANTILOPAY_PROJECT_ID=your_project_id
```

### MiniApp
```ini
MINIAPP_CUSTOM_URL=https://cabinet.my.domain.com/
```
[id=663465](https://t.me/c/2941121338/663465)

### Топики [id=703190](https://t.me/c/2941121338/703190)
```ini
ADMIN_NOTIFICATIONS_PURCHASES_TOPIC_ID=...
ADMIN_NOTIFICATIONS_RENEWALS_TOPIC_ID=...
ADMIN_NOTIFICATIONS_TRIALS_TOPIC_ID=...
ADMIN_NOTIFICATIONS_BALANCE_TOPIC_ID=...
ADMIN_NOTIFICATIONS_ADDONS_TOPIC_ID=...
ADMIN_NOTIFICATIONS_INFRASTRUCTURE_TOPIC_ID=...
ADMIN_NOTIFICATIONS_ERRORS_TOPIC_ID=...
ADMIN_NOTIFICATIONS_PROMO_TOPIC_ID=...
ADMIN_NOTIFICATIONS_PARTNERS_TOPIC_ID=...
```

### Прочее
```ini
MENU_LAYOUT_ENABLED=true
SIMPLE_SUBSCRIPTION_ENABLED=false
TRIAL_DURATION_DAYS=1
TRIAL_TRAFFIC_LIMIT_GB=10
TRIAL_DEVICE_LIMIT=2
RESET_DEVICES_ON_RENEWAL=false
```
[id=715784](https://t.me/c/2941121338/715784) [id=713700](https://t.me/c/2941121338/713700) [id=728306](https://t.me/c/2941121338/728306) [id=738812](https://t.me/c/2941121338/738812)

## Период 26.06–08.07.2026 — Remnawave 2.8.0, Bedolaga v3.61–3.62, Cabinet 1.59

- Бот (.env):
  - `SIMPLE_SUBSCRIPTION_SQUAD_UUID=` — UUID сквада для подписки (пусто = дефолт сквады) [id=761098](https://t.me/c/2941121338/761098)[id=761174](https://t.me/c/2941121338/761174)
  - `REMNAWAVE_API_URL` — `http://remnawave:3000` если в одной docker-сети, иначе https-ссылка [id=758793](https://t.me/c/2941121338/758793)
  - `ENABLE_LOGO_MODE=true` — не работает если в .env, надо убрать из env чтобы включалась через админку [id=764840](https://t.me/c/2941121338/764840)[id=764847](https://t.me/c/2941121338/764847)[id=764848](https://t.me/c/2941121338/764848)[id=774916](https://t.me/c/2941121338/774916)
  - `RESET_DEVICES_ON_RENEWAL=false` — реально работает с 3.62.0 [id=773269](https://t.me/c/2941121338/773269)
  - Уведомления: старые `user.expires_in_72/48/24_hours` и `user.expired_24_hours_ago` удалены → `user.expiration` [id=785692](https://t.me/c/2941121338/785692)
  - Параметры бота через UI не меняются если в .env тот же параметр — удалить из env [id=783216](https://t.me/c/2941121338/783216)
  - `SKIP_REFERAL_CODE=true` — отключить реферальный код [id=788108](https://t.me/c/2941121338/788108)
  - `TELEGRAM_OIDC_ENABLED` — `false` для проблем авторизации через ТГ [id=790573](https://t.me/c/2941121338/790573)[id=790777](https://t.me/c/2941121338/790777)

- Кабинет:
  - `CABINET_ALLOWED_ORIGINS=https://cabinet.my.domain.com` [id=758884](https://t.me/c/2941121338/758884)
  - `MINIAPP_CUSTOM_URL=https://cabinet.my.domain.com/` [id=758884](https://t.me/c/2941121338/758884)
  - `CABINET_FOOTER_ENABLED` — флаг легального футера [id=773269](https://t.me/c/2941121338/773269)
  - Кабинет не открывается из РФ за Cloudflare оранжевым облаком и на hetzner/ovh/aws — убирать CF прокси (DNS only) или проксировать через RU VPS nginx proxy_pass [id=796550](https://t.me/c/2941121338/796550)[id=796612](https://t.me/c/2941121338/796612)

- Панель Remnawave:
  - HWID лимит: включить, перезагрузить, массовые действия «use fallback limit» [id=756508](https://t.me/c/2941121338/756508)[id=756534](https://t.me/c/2941121338/756534)

- Платежки:
  - LAVA webhook: `webhook.доменбота.com/lava-webhook` [id=795562](https://t.me/c/2941121338/795562)
  - Оплата через кабинет и бота включается отдельно в .env/кабине [id=795562](https://t.me/c/2941121338/795562)

## Период 08–20.07.2026 — Remnawave 2.8.1, Bedolaga v3.62–3.64, Cabinet 1.61

### Bedolaga Bot — выдержка из `.env` (дословно) [id=838156|09.07.2026](https://t.me/c/2941121338/838156)
```
SALES_MODE=classic  # или tariffs (тарифы создаются в кабинете: Админ → Тарифы)
TARIFF_SWITCH_UPGRADE_ENABLED=true
TARIFF_SWITCH_DOWNGRADE_ENABLED=true
TARIFF_SWITCH_RESET_FREE_DAYS=true   # не переносить остаток дней с бесплатного тарифа на платный
RESET_DEVICES_ON_RENEWAL=false
TRIAL_DURATION_DAYS=2
TRIAL_TRAFFIC_LIMIT_GB=10
TRIAL_DEVICE_LIMIT=1
TRIAL_TARIFF_ID=0
TRIAL_PAYMENT_ENABLED=false
TRIAL_ACTIVATION_PRICE=0
DEFAULT_DEVICE_LIMIT=1
MAX_DEVICES_LIMIT=20
DEFAULT_TRAFFIC_LIMIT_GB=0
TRIAL_ADD_REMAINING_DAYS_TO_PAID=false
```

### Bedolaga Bot — прочие env-переменные (дословно из заметок)
- Подарки/гифт: `CABINET_GIFT_ENABLED`, `GIFT_SUBSCRIPTIONS_ENABLED` — расположение в UI: Админка → Система → Настройки → вниз → «опции интерфейса» [id=838809, 838824|09–10.07.2026](https://t.me/c/2941121338/838809).
- Rich-меню и лог действий (добавлены в 3.64.0, применяются на лету) [id=867471|13.07.2026](https://t.me/c/2941121338/867471):
  ```
  MAIN_MENU_RICH_ENABLED
  MAIN_MENU_RICH_EFFECT_ID
  MAIN_MENU_RICH_LOGO_URL
  MAIN_MENU_RICH_SUBSCRIPTIONS_COLLAPSIBLE
  USER_ACTION_LOG_ENABLED
  USER_ACTION_LOG_RETENTION_DAYS
  ```
  `MAIN_MENU_RICH_LOGO_URL=none` — пусто = **авто-режим**, а не «без логотипа»; rich не включается без логотипа (либо дефолтный, либо ждёт свой); если ссылка не картинка — бот выглядит как «не рич» [id=916532, 916665|19.07.2026](https://t.me/c/2941121338/916532).
- Кнопка кабинета в боте: `CABINET_ENABLED=true` [id=868004|13.07.2026](https://t.me/c/2941121338/868004).
- Бэкапы: `BACKUP_AUTO_ENABLED=false|true` [id=847895|11.07.2026; [id=846689..846693](https://t.me/c/2941121338/847895).
- Логотип на главной в боте отключается настройкой `ENABLE LOGO MODE` [id=870147, 870162|14.07.2026](https://t.me/c/2941121338/870147).
- Уведомления о старте («уведы о старте») настраиваются в `.env` [id=880093|15.07.2026](https://t.me/c/2941121338/880093).
- Язык/конверсия цен: цены на подписки зависят от языка интерфейса кабинета; при EN оплата в USD и кривой курс конвертации (оплата 8$ → зачисление 7.9). Отключение: настройка кабинета (выбор языка) или фикс в `.env`; можно задать язык вручную в кабинете [id=850579..850594|11.07.2026](https://t.me/c/2941121338/850579).

### Remnawave панель
- Временные рамки webhook'ов после обновления до 2.8.0 выставляются в `.env` панели [id=877540|15.07.2026](https://t.me/c/2941121338/877540).

### Кабинет (CABINET_*)
- `CABINET_URL` — используется в return-URL платёжных шлюзов (см. фикс Lava): `settings.CABINET_URL` [id=878931..878987|15.07.2026](https://t.me/c/2941121338/878931).

---

## Период 20–31.07.2026 — Bedolaga v3.66/3.67 + Cabinet 1.64 (рекурренты Platega/Lava)

### Бот Bedolaga (дословные имена)
- `PLATEGA_RECURRENT_ENABLED` — гейт СБП-рекуррентов Platega, по умолчанию `false`; у мерчанта Platega должен быть включён метод «Подписки» [id=962144|—|25.07.2026](https://t.me/c/2941121338/962144).
- `AUTO_PURCHASE_AFTER_TOPUP_ENABLED` — автопокупка после пополнения [id=936241|bypara|21.07.2026, id=936265](https://t.me/c/2941121338/936241).
- `LAVA_SBP_DISPLAY_NAME` / `LAVA_DISPLAY_NAME` — баг: для lava_sbp и lava_card использовалась одна переменная; фикс — разделить; правка в `app/utils/payment_utils.py` и `app/keyboards/inline.py` [id=971527|Lick|26.07.2026](https://t.me/c/2941121338/971527).
- `ALLOW_DEVICES_BELOW_TARIFF_LIMIT=true` — возвращает старое поведение [id=998125|Egor|30.07.2026](https://t.me/c/2941121338/998125).
- `CABINET_REQUIRE_LEGAL_CONSENT=false` — отключает согласие с офертой [id=998125](https://t.me/c/2941121338/998125); `CABINET_LEGAL_CONSENT_PRECHECKED` [id=998121](https://t.me/c/2941121338/998121).
- `MENU_BUTTON_WEBAPP_ENABLED` / `MENU_BUTTON_WEBAPP_TEXT` / `MENU_BUTTON_WEBAPP_URL` — кнопка «Меню» открывает кабинет; по умолчанию выключено [id=998125](https://t.me/c/2941121338/998125).
- `BACKUP_TIME` — время бэкапа базы бота [id=1000947|Jack J.|30.07.2026](https://t.me/c/2941121338/1000947); бэкап по расписанию — в env [id=999677-999683](https://t.me/c/2941121338/999677).
- При продлении подписки трафик не сбрасывается — «в env бедолаги есть строка, поменять значение» [id=995767-995778|Primat/kataomi.|29.07.2026](https://t.me/c/2941121338/995767).
- `Webpage access is not allowed by Remnawave's SRR` — «домен надо точно прописать, в env ищи» [id=1002966-1002977|vnik_null|30.07.2026](https://t.me/c/2941121338/1002966).
### Панель Remnawave
- Можно указать **несколько доменов subpage в env панели** [id=959998|vnik_null|25.07.2026](https://t.me/c/2941121338/959998).
- Смена домена: после перезагрузки бота включить синхронизацию из панели; в настройках бота сменить URL и пересобрать [id=959119|Mikhail, id=959253|Jordan|25.07.2026](https://t.me/c/2941121338/959119).
- Синхронизация Remna→Bedolaga: только через POST-запросы [id=934218|—|21.07.2026](https://t.me/c/2941121338/934218).
### Кабинет
- `CABINET_REQUIRE_LEGAL_CONSENT`, `CABINET_LEGAL_CONSENT_PRECHECKED` [id=998121](https://t.me/c/2941121338/998121); логотип в кабине грузится битым — «проблема в прокси была» [id=929296, 929520](https://t.me/c/2941121338/929296).

## Период 31.07–09.08.2026 — Remnawave 3.0.0 (ломающий), Bedolaga v4.0.0, Cabinet 1.65

### Remnawave Panel
- `APP_SECRET=change_me` — JWT AUTH SECRET (ранее `JWT_API_TOKENS_SECRET`) [id=1039553](https://t.me/c/2941121338/1039553)
- `REMNAWAVE_AUTH_TYPE=caddy` — обязательная переменная для связки бот+кабина на разных серверах [id=1015437](https://t.me/c/2941121338/1015437)
- `REMNAWAVE_API_URL=https://sub2.example2.tld` — URL API панели для бота; при 401 в логах бот — не ошибка бота, это `/api/system/stats` → HTTP 401 (нужен токен) [id=1011401](https://t.me/c/2941121338/1011401)
- `REMNAWAVE_USER_DELETE_MODE=delete` — при удалении юзера через панель удаляет (а не отключает) [id=1013970](https://t.me/c/2941121338/1013970)
- `MENU_LAYOUT_ENABLED=true` — по умолчанию в доке; может ломать редактор меню [id=1005758](https://t.me/c/2941121338/1005758)
- `TRAFFIC_EXCLUDED_USER_UUIDS` → переименовано в `TRAFFIC_EXCLUDED_USER_IDS` (числовые id) [id=1032536](https://t.me/c/2941121338/1032536)

### Bedolaga Bot
- `GRACE_ACCESS_MODE` — режимы: `false` / `observe` / `true` / `drain` [id=1032713](https://t.me/c/2941121338/1032713)
- `GRACE_ACCESS_EXPIRED_TRAFFIC_GB=1` — старые переменные больше не используются [id=1056551](https://t.me/c/2941121338/1056551)
- `GRACE_ACCESS_LIMITED_TRAFFIC_GB=1` — старые переменные больше не используются [id=1056551](https://t.me/c/2941121338/1056551)
- `INACTIVE_USER_DELETE_MONTHS=1200` — отключение неактивных юзеров; не ставить 0 — «могут попасть под очистку все пользователи» [id=1057118](https://t.me/c/2941121338/1057118)
- `YOOKASSA_TEST_MODE=true` — тестовый режим (10 ₽ для проверки баланса); после теста вернуть `WEBHOOK_URL=https://hooks.domain.net/payment-success` + `YOOKASSA_WEBHOOK_PATH=/yookassa-webhook` [id=1011432](https://t.me/c/2941121338/1011432)
- `ENABLE_LOGO_MODE=false` — скрыть логотип в боте [id=1060772](https://t.me/c/2941121338/1060772)
- `MAIN_MENU_RICH_LOGO_URL=none` — скрыть логотип в боте [id=1060772](https://t.me/c/2941121338/1060772)
- `MAIN_MENU_MODE=default` — при `cabinet` → из веб-интерфейса; при `default` → кнопки главного меню редактируются [id=1029599](https://t.me/c/2941121338/1029599)
- `WEBHOOK_URL=https://hooks.domain.net/payment-success` [id=1011432](https://t.me/c/2941121338/1011432)
- `YOOKASSA_WEBHOOK_PATH=/yookassa-webhook` [id=1011432](https://t.me/c/2941121338/1011432)

### Bedolaga Cabinet (CABINET_*, VITE_*)
- Вебхук-роуты монтируются только по env-флагу `*_ENABLED`, а не по DB-конфигу: если включаешь через админку `is_enabled=true`, но .env-флага нет — GET вебхук-эндпоинта отдаёт 404 → «Пропущенный колбек = висящий платёж» [id=1023658](https://t.me/c/2941121338/1023658)

## Период 09–20.08.2026 — Remnawave 3.2.3/3.3.0, Bedolaga v4.1.0 (GeoCheck)

- APP_SECRET (ex JWT_*) [id=1094452](https://t.me/c/2941121338/1094452) [id=1121658](https://t.me/c/2941121338/1121658); ForceIP ex UseIP [id=1086718](https://t.me/c/2941121338/1086718); trafic_excluded [id=1095275](https://t.me/c/2941121338/1095275)
- Main_menu_mode=cabinet [id=1096440](https://t.me/c/2941121338/1096440); MAIN_MENU_RICH_ENABLED [id=1116372](https://t.me/c/2941121338/1116372); REMNAWAVE_AUTO_SYNC_TIMES UTC [id=1130564](https://t.me/c/2941121338/1130564); SMTP_REPLY_TO [id=1152078](https://t.me/c/2941121338/1152078); BAN_MSG_* [id=1152078](https://t.me/c/2941121338/1152078)
- CABINET_REQUIRE_LEGAL_CONSENT [id=1105934](https://t.me/c/2941121338/1105934); auth_date 30 суток [id=1154502](https://t.me/c/2941121338/1154502)
- Webhook URL в платёжке [id=1101041](https://t.me/c/2941121338/1101041); 405 реверс-прокси [id=1101027](https://t.me/c/2941121338/1101027)

## Период 20–23.08.2026 — совместимость 2.8.x/3.2.2, GHCR, пин-борда

- `.env` панели: при мажорном апгрейде версия меняется **с `2` на `3`** [id=1163018|21.08](https://t.me/c/2941121338/1163018).
- `.env` бота Bedolaga — дословно упомянутая переменная:
  ```
  ADMIN_IDS=111222333
  ```
  [id=1177374|23.08](https://t.me/c/2941121338/1177374) — при этом бот не реагировал (контейнер проброшен, токен верный, логи чистые, сервер не в РФ); решение в чанке не дано [id=1177374|23.08](https://t.me/c/2941121338/1177374).
- При фиксе кабины отдельно требуется **обновить `.env` бота** (вместе с обновлением бота/кабинета/панели до ласт + прописыванием скрипта из поста) [id=1174288|22.08](https://t.me/c/2941121338/1174288).
- Панельный вебхук бота — путь и сигнатура (из логов):
  ```
  RemnaWave webhook: invalid signature http_method=POST http_path=/remnawave-webhook
  ```
  [id=1159430|21.08](https://t.me/c/2941121338/1159430) — из-за этого сообщения об обновлении бота не приходят (инфа при этом есть в кабинете); чинить подпись вебхука/токен [id=1159430|21.08](https://t.me/c/2941121338/1159430).
- Стратегии сброса трафика в Remnawave, фигурирующие в настройках подписок: `NO_RESET`, `MONTH_ROLLING` [id=1157934|20.08](https://t.me/c/2941121338/1157934).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Env-переменные**

◀ [Docker-compose](docker-compose.md) · [Nginx / Caddy](reverse-proxy.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
