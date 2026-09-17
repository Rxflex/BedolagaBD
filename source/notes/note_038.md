# Заметки из chunk_038 (id 221175..226454, 12-15.02.2026)

Период: релиз Bedolaga Bot v3.11.0 (закреплённые рассылки + tariffs по умолчанию), Cabinet v1.15.0, Remnawave Admin v2.1/v2.2 (Case211), битва с «слетевшими ценами» после смены дефолтов, Caddy/Traefik/nginx конфиги кабинета, SMTP/почта, РКН-блокировки нод, троллинг «Семёна» (флуд).

## Релиз Bedolaga Bot v3.11.0 (12.02, id 221863, Egor)
- Функциональные рассылки закреплённых сообщений; новые дефолты и хотфиксы.
- Cabinet Admin API для закреплённых сообщений: CRUD, activate/deactivate, broadcast, unpin, загрузка медиа, пагинация, JWT-авторизация (id 221863).
- Startup-валидация «Подключиться»: предупреждение, если HAPP_CRYPTOLINK_REDIRECT_TEMPLATE не задан в режимах guide/happ_cryptolink, и MINIAPP_CUSTOM_URL не задан в miniapp_custom (id 222001).
- Фиксы: краш создания тикетов при ENABLE_LOGO_MODE=True (edit_message_caption на текстовом сообщении; убраны 6 некорректных веток); Webhook PendingRollbackError (db.rollback() + catch при каскадном удалении подписки); NOT NULL violation при восстановлении юзера (passive_deletes=True на FK sent_notifications/subscription_servers/temporary_accesses); Flood control в закреплённых (TelegramRetryAfter), XSS-hardening sanitize_html (allowlist URI-схем); подавлена ошибка expired callback query (id 221863, 222013).

## ⚙️ Изменённые дефолты в v3.11.0 (id 222116, 222164, Egor)
- CONNECT_BUTTON_MODE: guide → miniapp_subscription
- SALES_MODE: classic → tariffs
- Следствие: у кого не было явного SALES_MODE в .env/БД, «слетели цены» — бот подтянул цены из ранее созданных тарифов; после этого цены меняются в разделе Тарифы, .env больше не влияет (id 222764/222765). Откат для «стариков»: SALES_MODE=classic в .env + перезагрузка `make reload` (id 222636/222637, ᴘᴀʀᴀʟɪᴄʜᴇᴠꜱᴋʏ).
- Константин: после обновления v3.11.0 цены стали «от 990 р», менять в боте бесполезно; дело в подтянутом тарифе из БД (id 222724, 222763).

## Remnawave Admin (Case211) v2.1 и v2.2
- v2.1 (id 222001, Илья 12.02): кастомный конструктор уведомлений, плейсхолдеры, отправка Mail/Telegram/Webhook/Web, RU/EN локализация, SMTP; «свой SMTP-сервер с отправкой/получением писем, который можно прикрутить к Bedolaga». GitHub: https://github.com/Case211/remnawave-admin ; TG: https://t.me/remnawave_admin
- v2.2 (id 225308, 15.02): настраиваемое название заголовка панели, поддержка ARM, оптимизация фронтенда, фикс кнопки очистки, интеграция ltsdev/maxmind (обход сложной регистрации на MaxMind), таблица распределения юзеров по городам в аналитике, логи обработки нарушений вместо тайлов nginx, динамическая смена уровня логирования (DEBUG/INFO/ERROR/WARNING), настройка ротации/размера лог-файлов, список юзеров при клике на точку карты, фикс правил автоматизации, указание ноды при ошибке токена агента.

## Remnawave Admin v2.1.2 (id 224466, Илья 14.02)
- Исправления, чтобы письма не попадали в спам: добавить rDNS (Hostname ВМ) на сервере отправки email. Release tag: https://github.com/Case211/remnawave-admin/releases/tag/2.1.2

## Проблемы сборки/обновления Cabinet (docker + npm)
- Ошибка при docker build: TS2305 «Module '@telegram-apps/sdk-react' has no exported member 'retrieveRawInitData'» и аналогичные (photo_url vs photoUrl, tgWebAppPlatform) — из-за устаревших/несовместимых типов @telegram-apps (id 222194–222203).
- Docker-команда сборки статической миниапки из репозитория: `npm i && npx vite build` (id 222408/222413).
- npm-пакеты @telegram-apps/types@2.0.3 и transformers/bridge — deprecated, рекомендуют @tma.js (id 222413/222316).
- Vladimir: у тех, кто поднял кабинет из образа, нет кнопки авторизации через телегу — VITE_* переменные это build-time переменные Vite, они вшиваются в JS-бандл при npm run build и не читаются из .env контейнера; образ собран с пустым VITE_TELEGRAM_BOT_USERNAME; фикс — извлечь JS-бандл, заменить значение, смонтировать cabinet-index.js в контейнер через volume (id 222460/222502, монтирование `./cabinet-index.js:/usr/share/nginx/html/assets/index-CTQq2TBB.js:ro`).
- Если кабинет из образа и нет Telegram-логина: пересобрать из исходников npm-ом — заработало (id 224458/224459).
- www (nginx) отдаёт 403 «directory index of /var/www/remnawave-miniapp/ is forbidden» — про index файлы миниаппы (id 225434).
- При npm install выводится `6 high severity vulnerabilities` (инфо, не блокирует).

## Docker compose/окружения кабинета (id 222404)
- Пример compose для локальной разработки: сервис cabinet-frontend с build-аргументами VITE_API_URL=/api, VITE_TELEGRAM_BOT_USERNAME, VITE_APP_NAME, VITE_APP_LOGO; порт `${CABINET_PORT:-3020}:80`; healthcheck wget; env_file .env.
- Совет: чтобы можно было оставить кабинет без контейнера, собирается папка dist и она подключается к вебсерверу (id 226065/226068 Max R): `npm install && npx vite build`, затем volume `- /srv/bedolaga-cabinet/dist:/srv/cabinet:ro` в caddy.

## Caddy конфиги кабинета
- Дословный Caddyfile с вебхуками платежек и статикой miniapp (id 222344, { AimedMaksim }):
```
webhook.24.ru {
 encode gzip zstd
 handle /yookassa-webhook { reverse_proxy localhost:8080 { header_up Host {host} header_up X-Real-IP {remote_host} } }
 handle /platega-webhook { ... }
 handle /cryptobot-webhook { ... }
 handle /wata-webhook { ... }
 handle /heleket-webhook { ... }
 handle /tribute-webhook { ... }
 handle /pal24-webhook { ... }
 handle /mulenpay-webhook { ... }
 handle { reverse_proxy localhost:8080 { header_up Host {host} header_up X-Real-IP {remote_host} } }
}
subapp.24.ru {
 root * /srv/cabinet
 encode gzip
 handle /api/* { uri strip_prefix /api; reverse_proxy remnawave_bot:8080 }
 @websockets { header_regexp Connection *Upgrade*; header Upgrade websocket }
 handle /cabinet/ws { uri strip_prefix /api; reverse_proxy remnawave_bot:8080 { transport http { read_timeout 0; write_timeout 0 } } }
 handle { try_files {path} /index.html; file_server }
}
```
- docker-compose для caddy (id 222388): caddy:2.9.1, network_mode host, volume Caddyfile, логи, статика `/root/remnawave-bedolaga-telegram-bot/miniapp:/var/www/remnawave->` и `./cabinet-dist:/srv/cabinet:ro`, логирование json-file max-size 10m, сеть bot_network external.
- Минимальный рабочий Caddy для кабинета (id 223174, Josh):
```
cabinetyourdomain.com {
  handle /api/* { uri strip_prefix /api; reverse_proxy 127.0.0.1:8080 }
  handle { reverse_proxy 127.0.0.1:3020 }
}
hooksyourdomain.com { reverse_proxy 127.0.0.1:8080 }
```
- Аналогичный вариант (id 224534, Josh): кабинет на одном домене с VITE_API_URL=/api, hooks на отдельном.
- Продвинутый caddy-конфиг с кешем статики (id 226078, Max R):
```
lk... {
 encode gzip zstd
 handle /api/* { uri strip_prefix /api; reverse_proxy remnawave_bot:8080 { header_up Host {host} header_up X-Real-IP {remote_host} transport http { read_buffer 0 } } }
 handle /cabinet/ws { uri strip_prefix /cabinet; reverse_proxy remnawave_bot:8080 { header_up Host {host} header_up X-Real-IP {remote_host} transport http { read_timeout 0; write_timeout 0 } } }
 handle {
   @static path *.css *.js *.png *.jpg *.jpeg *.gif *.svg *.ico *.webp *.woff *.woff2
   header @static Cache-Control "public, max-age=31536000, must-revalidate"
   @html file /index.html
   header @html { Cache-Control "no-cache, no-store, must-revalidate"; Pragma "no-cache"; Expires "0" }
   root * /srv/cabinet
   try_files {path} /index.html
   file_server
 }
}
```

## Traefik конфиг для кабинета + бота (id 222502, Vladimir)
- Labels для бота: router Host(bot...) → порт 8080; cabinet-api Host(app...) && PathPrefix(/api) со stripprefix /api priority 100; cabinet-ws Host(app...) && PathPrefix(/cabinet/ws) priority 110; miniapp-api Host(app...) && PathPrefix(/miniapp/) priority 100; статика кабинета на порту 80, приоритет 10.
- Для superpupervpn.ru аналогично с letsencrypt вместо cloudflare; кабинет image ghcr.io/bedolaga-dev/bedolaga-cabinet:latest, volume ./cabinet-index.js:/usr/share/nginx/html/assets/index-CTQq2TBB.js:ro, сеть remnawave-network.
- Важно: oauth требует, чтобы cabinet_url совпадал с доменом (id 222480, art vs) — работает только до подключения oauth.

## Полезное по доменам кабинета
- .xyz и .shop — не работают для кабинета/телеги (для .xyz известно, .shop тоже), .live и .online работают (id 224465, Chill).
- VITE_API_URL=/api работает на одном домене, если на разных доменах нужен линк miniapp.com (id 224534, Josh).

## Настройки Bedolaga Bot: коннект/криптолинки
- CONNECT_BUTTON_MODE варианты (id 224819, 🛡): guide, miniapp_subscription, miniapp_custom, link, happ_cryptolink; обязательный MINIAPP_CUSTOM_URL для miniapp_custom.
- Кабинет умеет работать с CONNECT_BUTTON_MODE=happ_cryptolink (id 222784, Yaroslav).
- Подсказка: используйте https://happ.su/main/ru/dev-docs/crypto-link (id 222525).
- В HAPP_CRYPTOLINK_REDIRECT_TEMPLATE можно забить редирект ссылку (id 222139, Áslan Chernov) — работает через safari, но редирект останавливается, нужен index.html на своём домене.
- Архитектура нескольких доменов (id 222489, art vs): аппка в ТГ на один домен, web-версия в браузере на другой (например app на .com, web на .net), oauth и тг-виджет — на web-домен; «кто запретил проксировать веб на два поддомена сразу?» (id 222495).
- Декрипт happ crypt4/crypt5 существует, декрипт 5-й версии вышел одновременно с её релизом (id 222714, sайq); ссылка на декрипт v1-v4: https://codeby.net/threads/free-rasshifrovka-konfigov-happ-crypt-v1-v4-telegram-bot.92126/ (id 222537).

## Ошибки Bedolaga Bot
- FREEKASSA_PAYMENT_SYSTEM_ID пустой в .env → pydantic ValidationError, бот падает при старте: int_parsing, input_value='' (id 222563/222564). Если Фрикасса не используется, поставить число (42/52/67) или закомментить (id 222567/222569/222570).
- «query is too old and response timeout expired or query ID is invalid» — Telegram при медленной обработке (id 222071/222073, Egor).
- Пометка юзера blocked: asyncpg DataError «can't subtract offset-naive and offset-aware datetimes» в UPDATE users SET status=$1, updated_at=... — масс-блок пользователей не работает (id 222766, /dev/null).
- «greenlet_spawn has not been called; can't call await_only() here» при синхронизации с ремной — SQLite/asyncpg на пользователя, дергается в синхре бота с панелью (id 224894, Mark Afanasiev).
- channel_checker «there is no text in the message to edit» при создании тикета — ENABLE_LOGO_MODE делает промпт фото-сообщением, edit_message_text на нём невозможен (id 223507, - -; баг-репорт с affected lines в app/handlers/tickets.py: handle_ticket_title_input / handle_ticket_message_input; suggested fix: try/except вокруг edit_message_text, fallback на message.answer(); Env: bot 3.11.0, Python 3.13, aiogram 3.x).
- Кабинет: «Ошибка в select_tariff_extend_period: list index out of range» на периоде продления тарифа (id 225378, Артём; traceback /app/app/handlers/subscription/tariff_purchase.py:1555, `period = int(parts[2])`).
- Кабинет: «Error sending email to m@gmail.com: please run connect() first» и «Connection timed out» + asyncpg InterfaceError «cannot call Transaction.rollback(): the underlying connection is closed» — SMTP не подключился (id 224629, 224795).
- Рекомендация Mike Bell по PostgreSQL (id 222322): проверить `idle_in_transaction_session_timeout` и `statement_timeout` — если слишком маленькие, сервер закрывает коннект посреди транзакции → «underlying connection is closed»; либо таймаут smtp.
- После обновления не работает happ_cryptolink у старых подписок, созданных до включения cryptolink (id 225350, Фантомас) — старая ссылка остаётся, надо пересоздать подписку/обновить.
- При выборке «оплатить подписку» после триала вылезает Unknown «c6xv..» (id 225357/225362, { AimedMaksim }; частое после триала, решается удалением юзера и заново).
- Админ-панель: «Настройка MAIN_MENU_MODE сохранена в БД, но не применена: значение задаётся через окружение» — .env приоритетнее настроек кабинета; чтобы перенести настройку в кабинет, закомментировать в .env (id 223422/224897, 🪲).
- Старое: не работает кнопка «Моя подписка» из-за webhook:close (id 224238, Name L.) — историческая бага с click.
- Бот: telegram webhook endpoints не настроены / «нет активных endpoints» — вебхук не создался, смотреть конфиг nginx (id 225354).
- В .env: убрать `web_api` в false → пропали ошибки на платежку/классик (id 225385, Vladimir M.).
- Тикеты из телеги не создаются на 3.11.0 — выключить фото лого в меню (id 225784, Egor; id 225704, 225778).
- «Устройство не поддерживается» с HWID у части клиентов при включении HWID (id 224863–224870, ТОЧНА НЕ ВПН).
- Бот при выборе триала выдаёт 4 устройства вместо 1 из .env — TRIAL_DEVICE_LIMIT игнорируется, берётся из тарифа к которому привязана триалка; чтобы зафиксировать, надо убрать опцию TRIAL_TARIFF_ID в .env (id 223175/223206, Ванечка/Роман).
- Когда в .env пустой параметр (например FREEKASSA_PAYMENT_SYSTEM_ID=) бот падает при старте: pydantic int_parsing, input_value='' (id 222563).
- Логи бота: свободные string-и в callback, дубликаты «query is too old» при спаме кнопок.

## Тарифы в кабинете
- Переход между уровнями: тариф с уровнем 1 за 100р, уровень 2 за 150р → при переходе юзер доплатит 50р; на одном уровне разные цены → переход бесплатный (id 224272, Name L.).
- В тарифе можно менять сервера (квады) — при изменении квадов в тарифе пользовательские подписки не пересоздаются, нужно массово обновить подписку (id 224140, Миша ту-ту). Happ Premium умеет заставить пользователей обновить подписку (id 224141, Илья).
- Скидки: на периоды создаются вручную, у тарифов берутся от трафика и устройств (id 223849/223850, Egor).
- Возможность попасть на триальный тариф и продлевать его повторно — баг, был заявлен (id 224055, EV), Egor: «отключи его просто» (id 224060).
- Периоды продаж: баг с выбранным периодом при продлении (id 225378, Артём).
- Автовыдача подписки в дефолтной группе не переключается при оплате, приоритет выше дефолта (id 226088, Vladimir M.).
- База тарифов и дефолт: «свободная» подписка «Свобода полная» из тарифа выдаётся юзерам (id 225357).
- Кабинет: вывод средств пока только в боте (id 224471, il migliore del mondo; id 224477, Name L.).
- Оплата «доп. устройств» пропала в кабинете (id 224745, RAKSLINEVPN).
- Реализация «разделение трафика между инбаундами»: workaround через коэффициент трафика на ноде — 1 для лимитной, 0 для безлимной; минус — трафик на нодах с коэф 0 не считается, при исчерпании лимита всё отваливается (id 224507/224508). Правильное решение обещают в боте позже (id 224500).

## Про сабу и ркн
- РКН пишет и заблокировал бот SUBA (Haxonate, id 222938–222956): получил официальное письмо от РКН на почту, закрыл сервис; очистили 0.5 млн денег (id 223501), до 5 гб/с. «не используешь VPN» аргумент. Поиск шел через hoster-запросы + платежки (юмани) + Telegram-запросы (id 223558/223566/223570/223576/223585).
- Дойти до оwner'а можно: зарегать левый яндекс-аккаунт, платежку только криптой, домен не на свои данные — но телега выдает данные по запросу (id 223561–223576).
- Платежки с бенефициарами в РФ типа Платеги — могут слить (id 223626, R0xTaDDy); Platega - эстонская юрка, «может похер» (id 223623).
- Пэй-палы, STP, Durov и т.п. обсуждались, надо учитывать, что любой РФ-хостер сольет (id 223575).
- Прокси для Telegram в боте после блокировок: заявка настроить прокси для ТГ бота/для nalogo — налоговая недоступна с серверных IP (id 225260, Ruslan): запросы nalogo идут на https://lknpd.nalog.ru/ (id 225270), с 9.02.2026 с РУ серверов недоступна, только домашний и мобильный (id 225273), лечится сменой DNS на яндекс 77.88.8.8 через netplan (id 225287, мысли; id 225276, R0xTaDDy).
- Налого: ПД. Налоги nalogo работают с серверных IP, если DNS яндекс (id 225287).
- Сам РКН платит 500к штраф и тому подобное; «одним фактом владения можно попасть под 500к штраф» (id 225647/225649, R0xTaDDy, шутка).

## Полезное про прокси/YouTube/обход
- YouTube без рекламы: сервер РФ без ТПСУ (ТСПУ), либо поднимать запрет (id 222212, V M); зарубежные хостинги с IP, определяемыми как РФ — Гемини не работает, но YouTube без рекламы (id 222212).
- Проверка цензурности сервера: `bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode dpi` (id 222219, —). Вывод по youtube.com/discord.com/instagram.com/facebook.com/x.com/linkedin.com/rutracker.org (Blocked) /digitalocean/amnezia/getoutline/mailfence/flibusta/rezka (id 222221).
- В Сочи работают местные бан-листы: waicore и dhost недоступны, LTE-ограничение отражается и на проводном (id 223500, V M).
- AdGuardHome не перебивает рекламу ютуба: контент и реклама грузятся с одних серверов, рф-рекламу можно душить фильтрами (id 222255/222271, Valerii B. / Áslan Chernov).

## Полезное по клиентам
- На iOS xHTTP рвёт соединения — iOS мало выделила кэша на xray-ядро; лечится сменой транспорта на grpc (id 224539/224592, SUPPORT/PipPup).
- v2raytun premium позволяет менять URL подписок (id 225313, Борис Б.).
- Happ Premium: менять URL подписок, скрывать пинг, скрывать конфиг сервера, кастомные темы — фичи только премиум-юзеров; подписочная модель «продажа фич» (id 224031/224036/224037/224042/224046, tgshtt).
- Happ: бесплатный декрипт конфигов не спасает, фича «happ://crypt5/» — новое шифрование (id 222526).
- Happ платный: https://happ-proxy.com/security/login (id 225468, .).
- На openwrt ставится SSClash (mihomo) для работы с подпиской (id 224838, Ramil M.).
- Страница подписки берёт username из base64 внутри html, по uuid из ремны (id 222652/222654, —/Name L.).
- Пользователь в описании ремны: username, иначе email до @, иначе id-telegram_id (id 223895, Tatoxa; id 223872, Илья: «идет user_email_имя как в email до @_id в ремне»).

## Платежки
- YOOKASSA_RETURN_URL: ставить ссылку на лк/бота; возвращение в кабинет пока нет диплинков (id 224237–224245, Mike Bell).
- Yookassa webhooks: в настройках ЛК юкасссы надо указать адрес обработчика (URL для технических уведомлений), иначе бот сам запрашивает статусы после оплаты (id 223230, Fantom; решено).
- Платега: возврат средств — писать менеджеру, id транзакции или квитанция (id 225377, Arstan | Platega S.). В кабинетах поле «секрет» и есть API от платеги (id 225303/225304).
- Platega и Wata — партнёры (id 225871/225872).
- Кавказ: проект «АИ касса» (libkit, id 224924) — серая, без KYC (id 224987/224988).
- Криптобот позволяет куаром оплачивать рубли (id 223600, Йоэ) — но не во всех регионах есть СБП; в VK и Яндексе нельзя платить куар (id 223609, 17).
- Платежка на 8086 (HELEKET_WEBHOOK_PORT / PLATEGA_WEBHOOK_PORT) vs 8080: внешний порт, все хуки выходят на 8080, если порт не меняли (id 225194/225197/225201, libkit). Егор: бот в вебхуке на одном порту; пуллинг — дележка портов; FastAPI-сервер обслуживает Telegram webhook, платежные webhooks, админ API и статику миниапки на одном порту 8080 (id 225202, Egor).
- Порты платежек нужны при пуллинге — бот в режиме пуллинга, при падении хука удобно вернуться на пулл (id 225219/225221, Egor).
- Freekassa насильно навязывает свой кошелек FK Wallet (id 222788/222790, Илья/Zavulon).

## Почта/SMTP кабинета
- SMTP-конфиг бота (id 224245, —):
```
SMTP_HOST=mail.mymailserver.com
SMTP_PORT=587
SMTP_USER=service@myvpn.com
SMTP_PASSWORD=MyVeryStrongPassword
SMTP_FROM_NAME=My Cool VPN Service
SMTP_USE_TLS=true
```
- Проверка с хоста: `curl -v --url "smtp://smtp.mymailserver.com:587" --ssl-reqd --mail-from ... --mail-rcpt ... --user "username:password" --upload-file <(echo -e "Subject: Test SMTP\n\nTest message.") --anyauth` (id 224245/222685).
- SMTP таймвеб: smtp.timeweb.ru порт 465 не работает (openssl s_client: таймаут), порт 587 отдаёт «wrong version number» — это STARTTLS, а не implicit TLS (id 224829/224802, { AimedMaksim }).
- Заблокирован порт 25 у 90% хостеров по дефолту (id 224632, R0xTaDDy).
- Яндекс-почта: спам-фильтр не релеит письма от бота (id 224371, Mike Bell).
- Письма в спам: добавить rDNS/hostname ВМ у хостера (id 224466, Илья/Case211).
- Кабинет: страница с email активации (id 224911, Илья), поле email есть у каждого юзера (id 223865, Илья).

## Хостинг/сетка (факты из обсуждений)
- YeezyHost: Нидерланды, IP чистые, 1Гбит (id 222932/222960/222961, qqwsore); процессор load (id 225305, Lywome); юрлицо Украина/ЕС, модерация контента клиентом по законодательству Украины и ЕС (id 225299, Александр); в Греции, Финляндии, Швеции есть ноды (id 222934/222935).
- Play2Go (P2G): можно взять "Low-Cheap" с каналом 5 Гбит/с Shared, реальная 800Мбит-1Гбит (id 223256, 🛡); «Пробовал на Play2Go, я в dest и target русские сайты прописал и заработало» (id 222669, Тимофей); «п2го шляпа» (id 224417, —); в Нидерландах (id 224412).
- asdhere (my.asdhere.net/?from=399): скорость «17000 выдавливает», порт до 25 Гбит за 400р, до 10 Тбит/мес; это реселлер Вайкора; доступна Германия (id 222738–222758, Zavulon/9). Есть нюанс: асд тоже блокируют по той же AS, что и Вайкор (id 222818, stayinit).
- Waicore: « randomly dies and rises in 5 min» (id 223460, прevsходен); коллаб с братишкиным, трафик пошёл (id 223465); в Сочи недоступен местами (id 223500). Есть и промо BEDOLAGA (id 224098, Egor) — промокод удалён (id 224101, Evgeniy).
- Dhost: сабка отдельно, панель на dhost, таймауты (id 223502, Nowa).
- nuxt (nuxt.cloud): отваливаются подключения к сервисам; сеть была хорошей (id 225888, 🛡). Реф https://nuxt.cloud/?from=34743 (id 223248, Max R).
- 4vps.su (@FourServer_bot): 1 ядро, 1 ГБ ОЗУ, 10 ГБ памяти, 2 Гбит/с, 420₽/мес; «скорость до нужных не доходят, не советую» (id 225386, Черно-белый Ёж).
- netcup Австрия (id 223275, 𝓒𝓒𝟏𝟑𝟑𝟕) — вопрос, без ответа.
- Selectel: дедики, 10 Гбит по РФ, сеть отдельным сервисом; цены от 45к (id 226239/226243/226290, ⁠⁠/Сергей).
- rootvds.ru / багет — сервера (id 226213/226217, —).
- Aeza: «Aeza.net» по RU 10 Гбит (id 224452, Zavulon); 5 Гбит с 2.5 за 1$ апгрейд (id 226229, ALIEN).
- Контабо (id 222168, Александр; id 222717).
- Datacheap: RU, гигабит, 2 RAM 2 CPU; IP иногда Япония, скорость ~600 (id 225367, Kabeba).
- Эксперимент Kabeba (id 224306): fallbacks VLESS на порту 443 с Reality (dest disk.yandex.ru), сброс на локальные инбаунды TCP/XHTTP/gRPC (порты 10001-10003) по path /xhttp и /grpc — не заработал; path для fallback-инбаундов задавался руками в хосте = n/a
- Сеноко (senko) — Финляндия, днс 0 даунтайм (id 225956, —).
- hip hosting: Варшава/Мск, 200 Мбит Швеция, -20% скидка (id 225963, Matvey G.), но жёстко режется трафик мск→варшава по SS туннелю (id 225782, Fuji San).
- hostkey.com: USA норм, IP чистые, докупать до 10 Тбит, потом 180-200р/Тбит (id 224333/224341, Александр/Lywome); hostkey.ru и .com — только язык интерфейса (id 224346/224348).
- nodehost: Нидерланды 10 Гбит (id 225854/225856, Васян) и Швеция 1 Гбит (id 225860), дешево (id 225314, Мишка - Албанию за ~100р — «не найдено»).
- cloud core (RF): 1/2, безлимит, ~100 руб (id 225321/225324, makdren).
- Биллинг нод: «Биллинг» раздел в панели ремны (id 222701/222703, —/a; провайдеры (id 222704, .) поле закрыто, создается ниже «провайдер» (id 222767, saveks).
- YeezyHost доб. 3 Финляндии; VDSina? нет ответа (id 222934/222935).
- «сдохла» Waicore (id 223493, saveks; id 223460) и waicore.gg будет (id 222736, Zavulon).
- Гео данные: если гео файлы большие — RAM отображается некорректно (id 224599/224600, Nick/R0xTaDDy).
- Скорость на SpeedTest нормальная, в XBox не (id 223260, 9) — провайдер.
- После рекламы братишкина Билайн стал «хуевым» (id 223486, saveks) — ну, субъективно.
- Время работы нод с ПХА (id 225810) — (флуд).

## Яндекс/ВК Cloud
- Яндекс Клауд: сервер 2500р/мес + трафик 1.65 руб за ГБ >100 ГБ (id 223443/223444, Йоэ/R0xTaDDy).
- На ВК нужны «определенные подсети, которые уже заняты», на Яндексе тоже (id 223449, R0xTaDDy); «вызывать могут» (id 223481, V M).
- VK Cloud IP-пул кончился: «Всего IP 129, осталось 0 в пуле» (id 226374/226377, Haxonate).
- На вк/яшке нельзя платить куар (id 223609, 17).

## Разное/архитектура
- Remna: panel.com / sub.com / node.com; Bot: miniapp.com + hooks.com; Cabinet: cabinet.com, в VITE_API_URL — hooks.com; в Web Login панели указывается значение MINIAPP_CUSTOM_URL (id 224643, Josh).
- Бот можно ставить на один хост с панелькой (id 223025/223032, Egor): «по заветам ремны раздельно можно ставить всё», боту для вебсервера нужен только 443 (id 223034).
- Бот бесплатный опенсурс, код/API открыты; платная поддержка (id 223037–223043, Egor).
- FastAPI встроенный: Telegram webhook + платежные webhooks + административное API + статика миниапки на одном порту 8080; снаружи только HTTPS-прокси (id 225202, Egor).
- Веб-кабинет может работать отдельно от бота (id 225409, Павел) — бот это бекенд; платежки в боте (id 225453/225479, Name L.).
- Сквады в боте = внутренние сквады ремны, названия рандомные, сравнивать по UUID (id 221861/221634/222803/224885, xexe).
- Фантомные сервера «1 Германия, 2 Испании» после смены панели — это твои реальные сквады с рандомными названиями (id 224881/224899, Josh/—).
- Синхронизация: сквады ремны → сервера в боте (id 223205, —); новые сквады не подтягиваются сами в кабинете, нужно пересоздать/обновить подписку (id 223200/223205).
- Панель поддерживает только xray (id 223922, Илья).
- Оплата доп. устройств пропала после обновления (id 224745).
- Разные боты на одной панели: юзеры перетекают (id 222789, ломаю пальцы...); чистить бота без панели — возможно через кабинет; иначе (флуд).
- Массовые действия по «удалению» юзеров из бота: вручную в кабинете (id 224931, saveks).
- Отзыв рефералок: в карточке юзера в боте есть админка, добавить вручную реферала (id 224305/224228/224230, Zavulon/Name L.).
- Кэш: после переключения на новый домен — чисти кэш браузера (id 224461, Chill); «перезапуск с билдом» (id 224590, —).
- Кеширование статики: см. caddy-конфиг выше (id 226078).
- После смены домена подписка в клиенте не обновится автоматически; рекомендация: оставить страницу подписки на старом домене, панель/бота переносить (id 225177, Mark Afanasiev); Happ платный тоже вариант (id 225178, Илья).
- Переезд бота на другой сервер: поднять бота, перекинуть .env и бэкап (id 225902, Egor).
- Дешевые API нейронок ~400₽/1млн токенов (id 224151, —).
- AI-библиотеки-гайды: claude лучше чата GPT для кодинга, codex — для маленьких проектов (id 224194, Илья).
- Dev-версия бота на git: `git pull; git fetch origin; git checkout -b dev origin/dev` (id 222154/222156, Egor), обратно `git checkout main` (id 222156). Данные БД и .env сохраняются, слетит картинка в главном меню (id 222239).
- Уведомления: «Ошибка отправки стартового уведомления: Telegram server says - Bad Request: chat not found» — проверять chat_id (id 226084, Влад).
- Блокировка всех клиентов кроме Happ и v2raytun: правила ответов в ремне (id 223349/223384/223387, ТОЧНА НЕ ВПН/R0xTaDDy).
- Юзеры со статусом disabled: бот отключает старых истекших подписчиков (id 223325/223326, GOOD_stu1/ddddd), либо отписка от обязательного канала (id 223367/223369, Egor).
- Хуки (webhooks) Remna: first connect event коряво обновляет данные в боте, баг (id 223802, Egor).
- Колесо: промокоды на крутки (id 224227, Сергей Тепляшин).
- Бесплатные крутки колеса при пополнении от N суммы (id 224227).
- Логи: поддерживаются архивы logs_YYYY-MM-DD.tar.gz на api.telegram.org (id 225318, Nick); HTTP Client says - ClientConnectorError: Cannot connect to host api.telegram.org:443 (id 225318).
- HTTP 400: «can't parse entities: Unsupported start tag "br" at byte offset 250» — <br> в HTML сообщениях Telegram не поддерживается (id 222964, zyko; править в БД через pgadmin).
- «can't parse entities: Unsupported start tag "3"» при отправке уведомлений (id 223282, ТОЧНА НЕ ВПН) — спецсимволы.
- Кампании: в боте переходы по рекламной кампании не всегда засчитываются — double-считается при двух кликах (id 224887, Egor: «один и тот же юзер дважды перейдет по ссылке, будет две уведы, но засчитает переход один»); у кого-то бот 100 переходов из 200 (id 224731/224839, ddddd).
- GET /api/users/{userid} тянет username (id 222648, Name L.) — но фактически username в base64 в html саб-пейджа (id 222652).
- Хуки: коряво обновляют данные в боте first_connect (id 223802, Egor).
- AIO ai-касса — «серая» касса (id 224987, libkit).
- «Zero ping» бот @zero_ping_vpn_bot — готовый бот, есть на гите (id 225136/225138, IS/Mark Afanasiev).
- Oauth: вход через Яндекс/Гугл подставляет email аккаунта, у юзера могут быть дубли из-за разных ящиков; TRIAL_DISABLED_FOR (email/telegram/all) — отключение триала по типу пользователя (id 226397/226416/226426/226432/226449, Aero/Egor).
- Идея: специальные тарифы для роутеров с выводом голого vless-конфига — роутеры не поддерживают подписки (id 224470/224478, Илья/art vs); на openwrt SSClash вместо этого (id 224838).
- Ошибка nginx «directory index of /var/www/remnawave-miniapp/ is forbidden» (id 225434, Владислав).
