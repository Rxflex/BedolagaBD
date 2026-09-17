# Заметки из chunk_002 (id 4041..9391, период 07.09.2025 .. 15.09.2025)

## Bedolaga релизы (продолжение), автор Egor/Fr1ngg, контрибьюторы @yazhog, @Legacyyy777
- **[id=4404|Egor|08.09.2025](https://t.me/c/2941121338/4404)** #v2_2_4 — Система авто-обновлений: бот сам проверяет новые версии на GitHub каждый час, меню «Обновления» в админке, уведомления в админский топик о релизах (фильтрация dev/beta). Конфиг:
  ```env
  VERSION_CHECK_ENABLED=true
  VERSION_CHECK_REPO=...
  VERSION_CHECK_INTERVAL_HOURS=1
  ```
  Docker-образы: метаданные VERSION/BUILD_DATE/VCS_REF, OCI-лейблы. Убраны копейки (@yazhog), QR-коды в реферальном разделе (@yazhog).
- **[id=4757|09.09.2025](https://t.me/c/2941121338/4757)** #v2_2_5 — CryptoBot: пополнение криптой (USDT, TON, BTC, ETH, LTC, BNB, TRX, USDC), автоконвертация курса USD/RUB с ЦБ РФ + exchangerate-api.com (кеш 1 час), таблица cryptobot_payments, enum PaymentMethod + CRYPTOBOT. Конфиг:
  ```env
  CRYPTOBOT_ENABLED=true
  CRYPTOBOT_API_TOKEN=your_token
  CRYPTOBOT_WEBHOOK_SECRET=your_secret
  CRYPTOBOT_TESTNET=false
  CRYPTOBOT_ASSETS=USDT,TON,BTC,ETH,LTC,BNB,TRX,USDC
  CRYPTOBOT_INVOICE_EXPIRES_HOURS=24
  ```
- **[id=5391,5433|09-10.09.2025](https://t.me/c/2941121338/5391)** #v2_2_6 (PRы @yazhog: #48 тест-подписка сразу после /start + продление в любой момент; #49 режим link + фикс напоминаний об истечении): CONNECT_BUTTON_MODE=link (прямая ссылка на подписку), таблица SentNotification против дублей уведомлений (Alembic-миграции, автоочистка при продлении), кнопки «Подключиться бесплатно»/«Пропустить» после регистрации, кнопка продления всегда видима.
- **[id=6195|11.09.2025](https://t.me/c/2941121338/6195)** #v2_2_7 — авто-бэкапы + приветственный текст:
  ```env
  BACKUP_AUTO_ENABLED=true
  BACKUP_INTERVAL_HOURS=24
  BACKUP_TIME=03:00
  BACKUP_MAX_KEEP=7
  BACKUP_COMPRESSION=true
  BACKUP_INCLUDE_LOGS=false
  BACKUP_LOCATION=./data/backups
  ```
  Плейсхолдеры приветствия: {user_name}, {first_name}, {username}, {username_clean}; HTML-валидация; таблица welcome_texts.
- **[id=6561|12.09.2025](https://t.me/c/2941121338/6561)** #v2_2_8 — режим логотипа:
  ```env
  ENABLE_LOGO_MODE=...
  LOGO_FILE=vpn_logo.png
  ```
  Монтирование vpn_logo.png в контейнер; сообщение с логотипом (message_patch.py / photo_message.py). Управление подписками: «Изменить устройства» (+/- с доплатой), сброс конкретного устройства или всех, «Переключить трафик» вместо «Добавить трафик» (доплата при увеличении, при уменьшении возврата нет).
- **[id=7132|12.09.2025](https://t.me/c/2941121338/7132)** #v2_2_9 — вкл/выкл приветствия кнопкой (is_enabled в welcome_texts); пропуск этапов регистрации:
  ```env
  SKIP_RULES_ACCEPT=...
  SKIP_REFERRAL_CODE=...
  ```
  Отправка бэкапов в Telegram:
  ```env
  BACKUP_SEND_ENABLED=...
  BACKUP_SEND_CHAT_ID=...
  BACKUP_SEND_TOPIC_ID=...
  ```
- **[id=7268|13.09.2025](https://t.me/c/2941121338/7268)** #v2_3_0 — кнопочный интерфейс админки (юзеры как кнопки: `[✅ 🎁 name | 💰 0₽ | 📅 7 ч. назад]`, статусы ✅/🚫/🗑, подписки 💎/🎁/⏰/❌), счётчик «🟢 Онлайн сейчас: X» (@Legacyyy777), `HIDE_SUBSCRIPTION_LINK=true` — скрыть ссылку подключения; реорганизация админ-меню (Юзеры и Подписки / Промокоды и статистика / Коммуникации / Настройки / Системные функции); фикс синхронизации счётчиков серверов (`name 'Subscription' is not defined`, некорректные PostgreSQL-функции).
- **[id=7374|13.09.2025](https://t.me/c/2941121338/7374)** #v2_3_1 — авторизация Remnawave: `REMNAWAVE_AUTH_TYPE = api_key | basic_auth` + REMNAWAVE_USERNAME/REMNAWAVE_PASSWORD, поддержка X-Api-Key и Basic Auth через X-Api-Key, `_prepare_auth_headers()`, совместимость с Bearer. Глобальная обработка ошибок Telegram: GlobalErrorMiddleware (app/middlewares/global_error.py) — «query is too old», «message is not modified», «bot was blocked by the user», «user is deactivated», «chat not found». Webhook-сервер: стартует при активном Tribute **или** CryptoBot; /health на 8081 работает всегда. Баг был: вебсервер не стартовал без включённого Tribute ([id=7296..7301](https://t.me/c/2941121338/7296), фикс [id=7308](https://t.me/c/2941121338/7308): health → `{"status":"ok","service":"payment-webhooks","tribute_enabled":false,"cryptobot_enabled":true,"port":8081,...}`).
- **[id=7766|14.09.2025](https://t.me/c/2941121338/7766)** #v2_3_2 — рассылки: селектор кнопок (💰 Пополнить баланс, 🤝 Рефералы, 🎫 Промокод, + «На главную»), медиа в рассылках (фото/видео/доки ≤50 МБ, file_id), статистика «онлайн сегодня/за неделю», быстрые действия после оплаты, управление правилами (валидация HTML, история версий, команды /clear_rules /rules_stats /admin_help), уведомления админам об изменениях подписки. БД: has_media, media_type, media_file_id, media_caption. Баг: после рассылки с медиа у юзеров менялось фото (аватар бота) — «Без кнопок отправляйте фотки пока» [id=7848..7852](https://t.me/c/2941121338/7848); /start возвращает лого.
- **[id=7413|Илья/@yazhog|13.09.2025](https://t.me/c/2941121338/7413)** PR: распознавание промокодов при вводе реферального кода (не реф → проверить промо), активация промокода после регистрации. Планировался PR обязательной подписки на канал [id=8431..8433](https://t.me/c/2941121338/8431).

## Ключевые фичи/знания по боту
- **[id=4108|Egor|07.09.2025](https://t.me/c/2941121338/4108)** Формула цены: `Период + (Трафик + сервера + устройства × месяцев периода)`. Базовая подписка = доп-переменная ([id=4069..4088](https://t.me/c/2941121338/4069): юзеру предложили доплату за сервера при анлим-тарифе — ставь цены серверов, базу 0).
- **[id=4126..4131|07.09.2025](https://t.me/c/2941121338/4126)** TRAFFIC_PACKAGES_CONFIG формат `"GB:цены_копейки:продавать(bool)"`; для безлим-тарифа: `0:0:true`, остальные false.
- **[id=4106..4134, 4140..4145|07.09.2025](https://t.me/c/2941121338/4106)** Ошибка pydantic «Extra inputs are not permitted: postgres_db» — env регистр: должно быть `POSTGRES_DB`/`POSTGRES_USER`/`POSTGRES_PASSWORD` (верхний регистр), DATABASE_URL=`postgresql+asyncpg://remnawave_user:...@postgres:5432/remnawave_bot`, REDIS_URL=`redis://redis:6379/0`. После правки: down/pull/up.
- **[id=4156|07.09.2025](https://t.me/c/2941121338/4156)** Ошибка `Bad Request: message thread not found` — ADMIN_NOTIFICATIONS_TOPIC_ID задан, а чат не с топиками (или наоборот). **[id=7777..7803|14.09.2025](https://t.me/c/2941121338/7777)** Уведомления шлются строго в **группу с топиками** (не канал, не связка канал+группа); в README поправили.
- **[id=4446..4450|08.09.2025](https://t.me/c/2941121338/4446)** `/health` на 8081 работает только при включённом Tribute (тогдашняя логика; в 2.3.1 исправлено на «всегда»). Workaround: убрать healthcheck из docker-compose.
- **[id=4466..4471|08.09.2025](https://t.me/c/2941121338/4466)** Уведомления об истечении подписки шлёт сам бот (за 3 дня и за 1 день), механики Remnawave и бота не связаны; если не приходят — рестарт бота + логи.
- **[id=4868|09.09.2025](https://t.me/c/2941121338/4868)** CRYPTOBOT_WEBHOOK_PORT=8083 — отдельный порт для криптобота; итог 13.09: **8083 не нужен** — `CRYPTOBOT_WEBHOOK_PORT=8081`, вебхук криптобота `/cryptobot-webhook` на общем 8081; в docker-compose для криптобота добавить `- "${CRYPTOBOT_WEBHOOK_PORT:-8083}:8083"` [id=4888/8430](https://t.me/c/2941121338/4888). В nginx/Caddy примере location для криптобота: `proxy_pass http://127.0.0.1:8081` (или `reverse_proxy http://remnawave_bot:8081`).
- **[id=7817|Aleksey V.|14.09.2025](https://t.me/c/2941121338/7817)** Трибьют сломался после правки Caddyfile — кадди и бот в разных сетях; возвращение в одну сеть починило Tribute+YooKassa; криптобот ругался на подпись — закомментировал CRYPTOBOT_WEBHOOK_SECRET и заработало. Секрет webhook = HMAC на основе API-токена (sha256) [id=7828..7829](https://t.me/c/2941121338/7828), как настроить толком не разобрались.
- **[id=7270..7287, 8315|13-14.09.2025](https://t.me/c/2941121338/7270)** Типовая Caddy-схема полного стека (мейн-сервер):
  ```
  https://webhook.domain.com {
      handle /tribute-webhook* { reverse_proxy localhost:8081 }
      handle /cryptobot-webhook* { reverse_proxy localhost:8081 }
      handle /health { reverse_proxy localhost:8081/health }
  }
  https://miniapp.domain.com { reverse_proxy * http://remnawave-telegram-mini-app:3020 }
  https://sub.domain.com { reverse_proxy * http://remnawave-subscription-page:3010 }
  https://monitoring.domain.com { reverse_proxy * http://uptime-kuma:3001 }
  https://besz.domain.com { reverse_proxy * http://beszel:8090 }
  :443 { tls internal; respond 204 }
  ```
  Криптобот-приложение в CryptoBot: создать через Crypto Pay, включить вебхуки, в настройках приложения указать ссылку на своего бота ([id=8545..8566](https://t.me/c/2941121338/8545)).
- **[id=8313|14.09.2025](https://t.me/c/2941121338/8313)** RU-нода (транзит/шэдоу для ютуба) — блок routing Xray на входной ноде: DIRECT для connectivity-check доменов (msftconnecttest, connectivitycheck.gstatic, captive.apple, detectportal.firefox, networkcheck.kde, *.gstatic); правило `inboundTag: ["vless-for-nl"]` → `outboundTag: "shadow-out"` для geosite:youtube (+youtube-домены), 2ip.io, geoip:ru, category-ru-gov, kinopoisk.ru, pochta.ru и т.п.; BLOCK bittorrent и geoip:private; domainStrategy: IPIfNonMatch. Ссылка на доку: https://xtls.github.io/ru/document/level-1/routing-lv1-part2.html. Ошибка смешивания доменов и IP в одном правиле: "geoip:ru" — отдельным правилом [id=9379](https://t.me/c/2941121338/9379).
- **[id=9382|15.09.2025](https://t.me/c/2941121338/9382)** Курс звёзд: рыночная цена 100 звёзд в premium bot ≈180₽ → коэффициент 1.8; безопасно ставить 2.0-2.1. **[id=9383..9388](https://t.me/c/2941121338/9383)** Вывод звёзд: только на крипту через Fragment (комиссия 50%+ при выводе на карту); 150 звёзд ≈ 239₽ → по факту получаешь 100-130₽. Совет: ставь курс выгодный себе либо не используй звёзды.
- **[id=4403|08.09.2025](https://t.me/c/2941121338/4403)** ЮМани-кошелёк: нельзя получать оплату и сразу переводить (бан кошелька по их правилам) — только держать/выводить аккуратно.
- **[id=5533..5537|10.09.2025](https://t.me/c/2941121338/5533)** Автоподстановка суммы пополнения в платёжку: самописная мини-апп форма → юкасса с предзаполненной суммой.
- **[id=7160..7169|12-13.09.2025](https://t.me/c/2941121338/7160)** Реферальная система: сейчас % с пополнения баланса рефами; обсуждали альтернативы (дни к подписке за реф, скидки, вывод с баланса); вывод с баланса — функцией с отключением [id=7213](https://t.me/c/2941121338/7213).
- **[id=7058..7062|12.09.2025](https://t.me/c/2941121338/7058)** Автоопределение сквадов не работает корректно — удалять старые сквады в боте, активировать нужные, названия править вручную в списке серверов.
- **[id=8039..8042|14.09.2025](https://t.me/c/2941121338/8039)** Если бот и панель на одном сервере — бот может задизейблить ~20 юзеров при первом запуске до синхронизации (внимание при первом старте на проде).
- **[id=8047..8057|14.09.2025](https://t.me/c/2941121338/8047)** Дать ноде доступ панели: в docker-compose бота добавить сеть remnawave-network (в конец docker-compose бота, и в секцию bot); следить за отступами (два пробела в YAML).
- **[id=8568..8575|15.09.2025](https://t.me/c/2941121338/8568)** Безлим-трафик: поставить 0 за безлимитный трафик (PRICE_TRAFFIC_UNLIMITED=0).
- **[id=9389..9391|15.09.2025](https://t.me/c/2941121338/9389)** Бот Bedolaga используется на проде (Илья, ~сотни юзеров).

## Локации RU-нод / ютуб
- **[id=8399..8404|14.09.2025](https://t.me/c/2941121338/8399)** Хостинг с RU-серверами под YouTube: aeza (сервер куплен, людей для ютуба устраивает, инста вроде работает).
- **[id=6955..6962|12.09.2025](https://t.me/c/2941121338/6955)** Вывод звёзд на крипту — только через Fragment.

## Ссылки/инструменты
- **[id=4068|07.09.2025](https://t.me/c/2941121338/4068)** awesome-remnawave: https://remna.st/docs/awesome-remnawave
- **[id=4082|07.09.2025](https://t.me/c/2941121338/4082)** Получить chat_id: бот @LeadConverterToolkitBot → добавить в группу админом → `/get_chat_id` в нужном топике. (Также: браузерная версия web.telegram.org/a — ссылка сообщения вида t.me/c/chat_id/topic_id/).
- **[id=5488|10.09.2025](https://t.me/c/2941121338/5488)** app-config.json с HWID-белым списком: https://github.com/legiz-ru/my-remnawave/blob/main/sub-page/hwid/app-config.json (кастомная саб-страница; HTML не обязателен; json монтируют в докер; логотип грузить на свой хост).
- **[id=7151|12.09.2025](https://t.me/c/2941121338/7151)** Wiki-интеграция с eGames-скриптом: https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot/wiki/8.-Интеграция-со-скриптом-установки-панели-eGames
- **[id=7788|14.09.2025](https://t.me/c/2941121338/7788)** Wiki по .env: https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot/wiki/2.-Настройка-бота-.env
- **[id=4444|08.09.2025](https://t.me/c/2941121338/4444)** СБП ЮKassa отдельно подключается: https://yookassa.ru/sbp/ (в тестовом магазине СБП не работает).
- **[id=8173|14.09.2025](https://t.me/c/2941121338/8173)** Дока Xray routing: https://xtls.github.io/ru/document/level-1/routing-lv1-part2.html
- **[id=5456..5457|10.09.2025](https://t.me/c/2941121338/5456)** Проверка апдейтов бота уведомлениями в топики.
- **[id=9380|15.09.2025](https://t.me/c/2941121338/9380)** Частые ошибки в конфигурации маршрутизации Xray (смешанные домены/IP).

## Хостинг-опыт
- **[id=5399..5414|10.09.2025](https://t.me/c/2941121338/5399)** dhostVPS: закончились сервера, юзеры 3 суток не могли заказать; поддержка обещала компенсацию; обещали добавление к концу недели; «10гбит вкусные».
- **[id=8404|14.09.2025](https://t.me/c/2941121338/8404)** Aeza — RU-сервер под ютуб работает у клиентов.
