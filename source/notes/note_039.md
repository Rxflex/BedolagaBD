# Заметки из chunk_039 (id 226471..231864, 15-18.02.2026)

Период: лихорадка релизов Bedolaga Bot v3.12.x..v3.16.3 и Cabinet v1.16.x..v1.18.0 (несколько релизов в день), миграция на structlog/Alembic/aware-datetime, партнерская система, веб-ссылки кампаний, Yandex Cloud обзвоны, РКН блокировки VLESS (слухи), обвал YouTube 18.02 (мировой).

## Релизы Bedolaga Bot (changelog, Egor)
- **v3.12.0 (16.02, id 226688)**: Режим Cabinet с deep-linking (MAIN_MENU_MODE=text → cabinet, кнопки меню ведут в разделы веб-кабинета); кнопка «Админка» в Cabinet-режиме; стили и emoji для кнопок (Bot API 9.4) — цвета синий/зелёный/красный/default через CABINET_BUTTON_STYLE; покнопочная настройка через админ-API (стиль, emoji, видимость, кастомные названия для каждой кнопки); вкл/выкл кнопок и кастомные названия по локалям (ru/en/ua/zh/fa). Фиксы: фото в тикетах; дневные подписки зависали в expired/disabled; трафик-пакеты с нулевой ценой исключены; кнопка «Моя подписка» в уведомлениях (webhook с незарегистрированным callback_data); удалены избыточные проверки trial inactivity; краш при возврате из выбора периода тарифа (IndexError); валидация CABINET_BUTTON_STYLE.
- **Cabinet v1.16.0 (16.02, id 226690)**: настройка кнопок бота в админке (вкладка «Кнопки»); закреплённые сообщения в админке; компактная страница логина; инлайн смена email и сброс пароля (без кода подтверждения для неверифицированных). Фиксы: колесо удачи — сначала результат с бекенда, потом угол; карточки кнопок flex-wrap/truncate; CryptoBot openTelegramLink; OAuth защита от open redirect/path traversal/утечки; безлимитные трафик-пакеты; логотип на логине. README переписан (примеры reverse-proxy Caddy/Nginx, troubleshooting).
- **v3.12.1 (16.02, id 227172)**: 🛡 Безопасность — burst rate-limiter на /start (макс. 3 вызова за 60 сек, скользящее окно, ленивая очистка buckets при >500 записей); защита промокодов от абьюза (5 неудачных попыток за 5 мин = блок, суточный лимит 5 активаций, валидация формата 3-50 символов); обновление зависимостей (cryptography 41→44+, redis 5→7.1, fastapi 0.115→0.129, bcrypt 4.2→5.0, sqlalchemy 2.0.46, asyncpg 0.31). Фиксы: краш тикетов — все edit_message_text обёрнуты в try/except с фоллбэком на message.answer(); Query(regex=) → pattern= в FastAPI.
- **Cabinet v1.16.1 (16.02, id 227181/227185)**: кеш брендинга localStorage → sessionStorage; initialDataUpdatedAt: 0 во всех 4 точках запроса брендинга (staleTime 60с); миграция из старого хранилища; проверка WebGL в Aurora.
- **v3.13.0 (16.02, id 227360)**: полная миграция на structlog — цветные логи (info зелёный, warning жёлтый, error красный), Rich-трейсбеки; FORCE_COLOR=1 в docker-compose; подавление шума при старте (~350→30 строк); ограничение Rich-трейсбеков (show_locals=False, max_frames=20, suppress aiogram/aiohttp); 267+ файлов logging.getLogger() → structlog.get_logger(), 2000+ f-string → kwargs; ContextVarsMiddleware (user_id/username/chat_id ко всем логам); TelegramNotifierProcessor (ERROR/CRITICAL в админ-чат); конфиг в app/logging_config.py.
- **v3.14.0 (16.02, id 228055)**: краш MissingGreenlet при продлении подписки (selectinload(Subscription.tariff)); рассинхрон SUPPORT_SYSTEM_MODE (обновляет оба хранилища двунаправленно); NameError в set_user_devices_button; _prefix_logger_name.
- **v3.14.1 (17.02, id 228400)**: отрицательные суммы в UI — abs() на SUM-агрегациях (SUBSCRIPTION_PAYMENT хранились с разным знаком); полная миграция на aware datetime — 660+ datetime.utcnow() → datetime.now(UTC), 170 колонок timezone=True, migrate_datetime_to_timestamptz().
- **v3.15.0 (17.02, id 228455)**: AttributeError при уведомлении о выводе (send_admin_notification()); затенение импорта UTC (4 локальных from datetime import UTC в purchase.py); 🚀 Веб-ссылки для рекламных кампаний (campaign_slug при авторизации через кабинет с защитой от дублирования); настройка LOG_COLORS (ANSI в логах).
- **Cabinet v1.17.0 (17.02, id 228457)**: веб-ссылки кампаний полный цикл (?campaign=slug из URL, 24ч TTL в localStorage, передача при Telegram/email/OAuth, одноразовое потребление; для email до верификации); тост о бонусе CampaignBonusNotifier; два типа ссылок в админке («Ссылка для бота»/«Веб-ссылка»).
- **v3.15.1 (17.02, id 228458)**: TypeError при чтении datetime из Redis — guard'ы `if dt.tzinfo is None: dt = dt.replace(tzinfo=UTC)` (traffic_monitoring, maintenance_service).
- **v3.16.0 (18.02, id 230949)**: 🆕 Партнёрская система — заявки на партнёрство, индивидуальный процент, привязка кампаний 1-к-1, вывод средств; уведомления партнёрки (Telegram+email+WebSocket, ru/en/zh/ua); админ-настройки партнёров; campaign_id в referral_earnings (ROI); обнаружение заблокированных (sent/blocked/failed в рассылках); traffic_reset_mode в API. Фиксы: SELECT FOR UPDATE на финансовых операциях, html.escape(), безопасные реферальные коды, N+1 в earnings/AML, YooKassa NotFoundError gracefully, платёжные провайдеры freekassa/cloudpayments/kassa_ai + фикс {total_amount}, MissingGreenlet в кампаниях. Рефакторинг: переход на Alembic — удалена universal_migration.py (7791 строк, ~99 функций), −9226 строк; auto-stamp.
- **v3.16.1 (18.02, id 231006)**: Alembic-миграция для таблиц/колонок партнёрской системы (фикс «column users.partner_status does not exist» id 230974).
- **Cabinet v1.18.0 (18.02, id 230950)**: партнёрская система в админке (заявки, статистика, комиссия, страницы выводов с risk scoring/fraud-анализом); страница рефералов; настройки партнёров; партнёр-кампания интеграция; blocked_count в рассылках; бейдж daily/weekly/monthly на тарифах; WebSocket не зацикливается при невалидном токене (код 1008); серверы → локации на карточках.
- **v3.16.2 (18.02, id 231152)**: naive datetime из БД без TIMESTAMPTZ-миграции → AwareDateTime TypeDecorator (авто-конверсия naive→UTC-aware при загрузке; все 175 DateTime-колонок).
- **v3.16.3 (18.02, id 231551)**: Deadlock при удалении пользователя (кабинет и webhook Remnawave блокировали таблицы в разном порядке; единый порядок subscriptions → server_squads); Savepoints для 24 шагов каскадного удаления; Auth middleware перехват всех ошибок при commit; робастная миграция 0002 (защита на базах без referral_earnings).

## Миграция Alembic (v3.16.x)
- Переход автоматический: существующая БД → auto-stamp; чистая БД → создание через Alembic; повторный запуск → на head, ничего не делает. Рекомендован бекап перед обновлением (id 230949).
- Бекап БД: `docker exec remnawave_bot_db pg_dump -Fc -U postgres remnawave_bot > backup_$(date +%Y%m%d_%H%M%S).dump` (файл в текущей папке; корректный контейнер remnawave_bot_db и роль remnawave_user при другой установке: `pg_dump -U remnawave_user -d remnawave_bot -F c` id 230953/230959). Восстановление: `docker exec -i remnawave_bot_db pg_restore -U postgres -d remnawave_bot --clean --if-exists < backup_XXXXXXXX_XXXXXX.dump` (id 230957/231147).
- Ручное лечение «миграция не проходит» KeyError 'cbd1be472f3d' (id 231318, Роман): проверить наличие колонки `\d referral_earnings`; в контейнере `alembic -c /app/alembic.ini current`; при >0001 — `downgrade 0001`; при ошибке индексов — python-скрипт `asyncio.run(_stamp_alembic_revision('0001'))`; снова downgrade/upgrade head. Альтернатива (id 231309, Пётр): `docker exec remnawave_bot_db psql -U postgres -d remnawave_bot -c "ALTER TABLE subscriptions ADD COLUMN last_webhook_update_at TIMESTAMP;"`.

## Ошибки после релизов 18.02 (скопом)
- Обновившийся бот весь в ошибках и не отвечает (id 230957/230968/230970) — после v3.16.0 без миграции; фикс v3.16.1 + пересборка.
- TypeError «can't compare offset-naive and offset-aware datetimes» в user.subscription.is_active (models.py:1186) и в мониторинге трафика (id 231024/231066/228434) — фиксы v3.16.2/v3.15.1.
- UnboundLocalError «cannot access local variable 'UTC'» при запросе статуса подписки/докупке трафика (id 228420/228949) — фикс v3.15.0 (затенение импорта).
- ServerDisconnectedError при API connection test /api/system/stats (id 230990) — из-за рассинхрона, Egor: поправил.
- KeyError в AuthMiddleware (id 231010) — из репорта без логов.
- «Ошибка Telegram API в required_sub_channel_check: Bad Request: message caption is too long» при регистрации нового пользователя (id 231731/231759) — связано с огромными стартовыми правилами + картинкой; защита добавлена на дев (id 231827/231829).
- TelegramBadRequest в app.handlers.admin.payments при просмотре платежей (id 230921) — инфа в сообщении не обновилась, Egor поправит.
- Ошибка добавления трафика UnboundLocalError UTC (id 228949) — v3.15.0.
- После v3.16.2 без причин забанило ~10 юзеров (id 231356) — из-за миграции datetime (софт-факт).
- Расхождения версии в консоли/кабине: кеш, пересборка с --build и чистка кеша браузера.

## Кнопки/режимы меню (v3.12+)
- Цветные кнопки требуют: MAIN_MENU_MODE=cabinet + MINIAPP_CUSTOM_URL=ссылка на кабинет + MENU_LAYOUT_ENABLED выключить (id 227321, eval; id 227836/227839/227840, Egor/—; id 228353 Caberock).
- MAIN_MENU_MODE=cabinet работает только с цветными кнопками, default режим на рефакторе (id 227008, Egor).
- Кабинет без видимости пользователям: CONNECT_BUTTON_MODE без miniapp, MAIN_MENU_MODE="полное меню", кабинет через браузер (id 228383, momai; id 228382, tgshtt).
- Скрыть кнопки/переопределить названия: веб-админка «Кнопки» (id 228205 wsq22, id 229516/229517/229522..229524).
- CABINET_BUTTON_STYLE в env ломает кабинет (id 227609/227613, Иван; id 227630, —; решено обновлением v3.14.x).
- «Мониторинг трафика: Отключен / Проверка пополнений: Отключена / Отчеты: Отключен» в логах при старте бота — активные фоновые сервисы перечислены в консоли (id 227564, Valerii).

## Кабинет/миниаппы
- Ноды/сквады: то, что ты видишь в боте — внутренний сквад; сквад это «подъезд», нода — «жилец» (id 227423, Name Lastname). Чтобы в боте были серверы, создай сквады, сквады не синхронизируются автоматически (id 227415/227418, 227421/227588).
- Адреса: cabinet_frontend:80 фронт, remnawave_bot:8080 API (id 227430, Name Lastname); в докере порты 80 и 8080 (id 227452).
- Бекенд/фронт отдельно: если бот и панель на разных серверах, в .env кабинета в api укажи полную ссылку, а не /api (id 229128, Name Lastname).
- Накатываешь SMTP на хосте: проверка работает, а в кабинете не приходят письма — заполни SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASSWORD/SMTP_FROM_EMAIL/SMTP_FROM_NAME/SMTP_USE_TLS=true в .env и перезапусти бота (make reload) (id 231228/231239/231243/231245, Anton Khakin/Dmitriy Balakshin).
- Статика кабинета: root, docker, /srv/cabinet (id 226665, c0mrade).
- Caddy-конфиг (id 226539, c0mrade):
```
(proxy_defaults) {
    header_up Host {host}
    header_up X-Real-IP {remote_host}
    transport http { read_buffer 0 }
}
hooks.example.com {
    encode gzip zstd
    @webhooks { path /yookassa-webhook; path /platega-webhook; path /cryptobot-webhook; path /wata-webhook; path /heleket-webhook; path /tribute-webhook; path /pal24-webhook; path /mulenpay-webhook; path /freekassa-webhook; path /cloudpayments-webhook; path /remnawave-webhook }
    handle @webhooks { reverse_proxy remnawave_bot:8080 { import proxy_defaults } }
    handle /app-config.json { header Access-Control-Allow-Origin "*"; reverse_proxy remnawave_bot:8080 { import proxy_defaults } }
    handle { reverse_proxy remnawave_bot:8080 { import proxy_defaults } }
}
cabinet.example.com {
    encode gzip zstd
    handle /api/* { uri strip_prefix /api; reverse_proxy remnawave_bot:8080 { import proxy_defaults } }
    handle {
        root * /srv/cabinet
        try_files {path} /index.html
        file_server
        @static path *.js *.css *.woff *.woff2 *.ttf *.ico *.png *.jpg *.jpeg *.svg *.webp *.gif
        header @static Cache-Control "public, max-age=31536000, immutable"
        @html path *.html /
        header @html Cache-Control "no-cache, must-revalidate"
    }
}
```
- Caddy-конфиг для кабинета с websockets и rich headers (id 226593, Mike Bell):
```
https://cabinet.mysite.com {
  header { Server cloudflare; -Via -X-Powered-By -X-Caddy-Cache-Status }
  encode gzip zstd
  handle /api/* { uri strip_prefix /api; header { Access-Control-Allow-Origin *; Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"; Access-Control-Allow-Headers "Content-Type, Authorization" } reverse_proxy bedolaga-bot:8080 { header_up X-Real-IP {remote_host}; header_up Host {host}; transport http { read_buffer 0; write_buffer 0; dial_timeout 10s; response_header_timeout 60s; keepalive 120s; keepalive_idle_conns 100 } } }
  @websockets { header_regexp Connection *Upgrade*; header Upgrade websocket }
  handle /cabinet/ws { uri strip_prefix /api; reverse_proxy bedolaga-bot:8080 { header_up X-Real-IP {remote_host}; header_up Host {host}; transport http { read_buffer 0; write_buffer 0; dial_timeout 10s; response_header_timeout 60s; keepalive 120s; keepalive_idle_conns 100 } } }
  handle { root * /home/www/cabinet.my.site; try_files {path} /index.html; file_server; @static { path *.css *.js *.png *.jpg *.jpeg *.gif *.svg *.ico *.webp *.woff *.woff2 }; header @static Cache-Control "public, max-age=31536000, immutable"; @html { path *.html / }; header @html { Cache-Control "no-cache, no-store, must-revalidate"; Pragma "no-cache"; Expires "0" } }
}
```
- c0mrade: «cabinet/ws вообще сноси в caddy, он сам умеет вебсокеты обрабатывать» (id 226512) — снимок против ws-блока.

## Сеть/порты/докер
- На 1 IP не обходится все: docker network connect bot_network remnawave_bot (id 227396/227413, Name Lastname; id 231281, —) — добавляет контейнер в сеть ремны.
- 3.13.0 docker-compose обновился — снесла сеть ремны (id 227409, —), c0mrade: лучше руками в компоуз прописать (id 227414).
- Пакеты типа force_color '1' в docker-compose (секция bot:) (id 227494/227497, Max R).
- 4vps — несколько машин, не жалуются (id 230864, Max R).
- Кабинет 2.0.0 — не скоро, нужен рефакторинг (id 227198).

## Цветные логи
- Отключить: FORCE_COLOR: '0' в docker compose (id 227529/227531, Max R; id 228067, Egor); либо logging_config.py `structlog.dev.ConsoleRenderer(colors=False, pad_event_to=0, pad_level=False, exception_formatter=structlog.dev.plain_traceback)` (id 228092, Сергей); либо настройка LOG_COLORS в .env (id 228455 v3.15.0).

## Платежки
- Платега: вывод — писать менеджеру, id транзакции или квитанция (id 227546/227548, 𝓒𝓒𝟏𝟑𝟑𝟕/Arstan); понижение комиссии от оборота 100к руб (id 227643/227653, Sonjeffry/Жан). Отмена вывода через менеджера (id 227467/227546).
- Platega - временные перебои в работе ЛК (id 229061, Евген).
- YooKassa NotFoundError для старых платежей — WARNING вместо ERROR (id 230949 v3.16.0).
- Издержки: «почта домен top-зона не работает» (id 228005..228010, Bulat) — т.е. не берут .top; «live работает» (id 228010, Bulat).
- Рассылки: «блокировка отправки сообщений боту» (id 231306, Мультитысячник).
- remnawave bot v3.13.0: отключение «проверка пополнений» — VALERII из админ-панели бота (id 227564).

## Уведомления/структура
- v2.6.1/2.6.2: Responses Rules (SRR) ignoreHostXrayJsonTemplate, dynamic outline conf, отдельная страница snippets (id 228179/228180 — Remnawave panel v2.6.1; Node v2.5.5 Rescue CLI `docker exec -it remnanode cli`).
- Локализация: AVAILABLE_LANGUAGES=ru,en не скрывает все языки в кабинете; фоллбек при LANGUAGE_SELECTION_ENABLED=false (id 228961/228963/228964, Yaroslav/—).
- Приветственное сообщение: В боте → Админ панель → сообщения → Приветственное сообщение (id 229219, Андрей).
- Похоже на «couple questions» (id 229203..229228, Артём Соловьёв): уровни тарифов 1/2/3: расчет стоимости одного дня, переход бесплатный если «стоимость дня» дороже тарифа равна/ниже. Перенесено из id 224272 (предыдущий чанк).
- Кабинет скрыть кнопку Админку? пока не (id 231464/231477/231491...).

## РКН/блокировки (слухи и факты)
- «vless заблокирован все» (id 228773, Egor) — но это шутка/ложное; многие говорят работает штатно (id 230076/230077).
- На ntc.party пишут, часть подсетей блокнул РКН (id 228701/228707, Max R).
- РКН случайно «убил» обновления Windows — вместе с телегой в банлист улетели IP/домены обновлений (id 228709, Max R, новость).
- ⚡ Telegram в РФ полностью заблокируют с 1 апреля (источники «Базы»), по аналогии с Instagram/Facebook; мессенджер MAX как замена (id 228712, Max R, новость 17.02).
- РКН сплэшем заблокировал Linux в РФ (id 229741, Max R, новость).
- RKN душит и SSH: «из-за замедления телеги VPN невозможен» (id 226678, R0xTaDDy).
- Мост дабл-влесс: МСК/СПБ нода без ТСПУ → зарубежная нода (id 228954, whereareyou; id 229077, Valerii Bezkorovainyi).
- Прокладки через 3x-ui/Amnezia (id 228381) — (не пытался), детали не разобраны.
- YouTube упал 18.02 ~2:00 по всему миру — массовый мировой сбой Google, не РКН (id 230677-230801, Aero/—: «YouTube упал у всех, по всему миру, без паники, это не баги впн/ркн»); проверять Downdetector (id 230743, Aero).
- Реклама VPN: ЮТ видео «закон запрещает рекламить VPN» — и листовки в Ростове/Краснодаре привели к штрафам и закрытию сервиса (id 229185, Aero).
- Безопасная реклама VPN — крипта + телеграм-звезды (id 229183, Aero) — касса (id 229178, Тёма/Black Konda).

## Бюджет/цены (опционально)
- Цены раскрашены с шагом 50 (id 228301..228303).
- Сумма списания больше стоимости тарифа: причины из БД/тарифов (id 228292-228316, Valerii Bezkorovainyi/Sayonara) — «чекай стоимость серверов(сквадов) в боте, по умолчанию 10р каждый, если в env активны пакеты трафика, он пытается присрать их к стоимости» (id 228311, Sayonara).
- Цены при продлении выше (id 229196, Dzhokhar).

## Выводы/ссылки
- https://github.com/DonMatteoVPN/Reshala-AI-ticket-bot (id 228388, Дмитрий) — Reshala Support (AI-ассистент для техподдержки).
- https://github.com/DonMatteoVPN/Reshala-Remnawave-Bedolaga (id 228448/228494, Дмитрий) — интеграция с Remnawave/Bedolaga.
- https://github.com/Case211/remnawave-admin (id 230944, Илья) — Remnawave Admin v2.3: Fleet Management (веб-терминал для нод xterm.js, gauge CPU/RAM/Disk, каталог скриптов); Collector и детекция нарушений перенесены из бота в Web Backend (−9000 строк дублирования, 800+ тестов, покрытие core 62%); Violation Detection (настройки анализаторов через веб-панель); System Logs (5 вкладок All/Backend/Bot/Frontend/Violations, structlog JSON, фронтенд-ошибки в реальном времени). ⚠️ При обновлении: перенаправить AGENT_COLLECTOR_URL node-agent на URL панели (вместо бота).
- https://pypi.org/project/aioplatega/ + https://github.com/DOFER998/aioplatega (id 230805, Egor) — библиотека для платеги (уже готова).
- https://dnschecker.org — проверка DNS, «как ток Питер меняется, то весь рф регион меняется» (id 229304, Haxonate).
- hosting101.ru/hip-hosting — проверка хостинга перед покупкой (id 230861/230862, Valerii Bezkorovainyi/—).
- vps.today — каталог VPS (id 229432, Виктор Белых).
- Скрипт для проверки региона/IP: https://github.com/Davoyan/ipregion/raw/main/ipregion.sh / bench.gig.ovh/ipregion.sh (id 229760/229762, Valerii Bezkorovainyi/—).
- XTLS документация по routing: https://xtls.github.io/en/config/routing.html#ruleobject (id 228443).
- Роутинг для ютуба на ру-ноде: `{"domain": ["geosite:youtube"], "outboundTag": "DIRECT"}` (id 229898, Prokurátura); routing rule на сервере РФ: `{"inboundTag": ["001_PUBLIC_RU_INBOUND"], "outboundTag": "SS_OUTBOUND_TO_FI"}` (id 229861, В. Б.) и «использовать не ru, а канал 25-гигабитовый» (id 229752).
- Скрипт защиты от DDoS L7 от DonMatteo: README раздел «Комплексный модуль безопасности» (id 228476/228503/228506, 💔/—) — только Nginx, для Caddy нет поддержки (id 228476).
- Отладка/дебаг: логи в дебаг включи (id 228681, Egor).

## Доп. детали
- «РКН случайно убил Windows Update» — ссылка «КиберТопор» (id 228709, Max R).
- Caber: 3.15.1 затенение импорта UTC, баг с UTC при оплате фиксится обновлением (id 228400).
- Обновления: `git pull origin main && docker compose down && docker compose up -d --build && docker compose logs -f` (id 226754/227491, Valerii Bezkorovainyi); если ошибка «Your local changes to the following files would be overwritten by merge: docker-compose.yml» — git stash → обнови → git stash pop (id 228693/229693..229699; id 231556/231617).
- 4vps в каталоге — id 230884..230898 (тесты). Хосты «Pq, The.hosting, Ufo.hosting» — топ-хосты (id 231233, stayinit). Занесены: «не один из них не советую», «1cent вообще говно тп» (id 231364/231366, SUPPORT) —
- Рекомендация по повестке — оставить роутинг ютуба на ru-сервере, а всё остальное — на helsinki (id 229684, Виктор Белых).
- Новая хостинговая «шляпа»: Nuxt Cloud отвалы: «двое суток выдают сервер, не советую» (id 228645, Kamil` Nikiforov). Смежное: «Отталкивается от сервисов» (id 229137, Nekrasov).
- NaloGO (самозанятый): remnawave_bot ERROR "NaloGO временно недоступен (техработы)" — настройка DNS яндекса в yaml: 77.88.8.8 (id 228223/228230/228234, Данил Уваров/libkit) — чеки уже работают после DNS.
- IP-гео из Play2go NL выдал US — «геобазы не обновились» (id 228925/228927, Daniil/Haxonate).
- Русские хосты ютуб без рекламы: Aeza локации норм (id 230630, —), таймвеб (id 230629, Prokurátura), hosting-russia (id 229749, Виктор Белых), нн Midas (id 231798, Whiteness), 1cent (id 230075/230061), dhost (id 231299/231296 — Германия 10 Гбит).
- 4vds.su — «сервак отключили через 15 мин, приостановлен, без письма» (id 230790/230791, Valerii Bezkorovainyi).
- Рефералка из кабинета в бота: человек переходит по реф-ссылке в кабинет, регается почтой или переходит в телегу — теряется реф (id 231858/231776, zyko) — бот-кампания ссылка на бота и веб-ссылка в кабинете (id 231744/231750).
- Экспорт/логи: логи приложения remnawave_bot (id 228368, Андрей Костылев — download_system_logs error).
- Кабинет: свернуть блок email, кнопки OAuth и т.д. (id 226691).
- Изменение тикетов: «app/handlers/tickets.py» (id 223507, chunk_038) — здесь нет.
- Хосты: «Nalogo» и «кнопка в настройках» (id 229205/229212, Bulat/Александр).
- Ремна код: app-config.json (id 231037..231061) — (флуд).
- CryptoBot/Kassa AI/Wata: Kassa AI: https://freekassa.net/auth/registration?inv=kassaai&input_type=blocked (id 228802, .); Wata рекомендация GRANIT https://wata.pro/ (id 228802).
- Whitelist CHS: Кольцо: /report (id 228825/228826, Мультитысячник).
- Кабинет has Пацаны, сквады: «сквады в тарифах «вырезать» их» (id 229667/229669).

## Хостинг-тесты (Whiteness, id 230786/230801/231180/231293/231299/231789/231817/231849)
- 1cent.host - 🇪🇪 Эстония, Таллин: 180 руб./мес. (1 vCPU / 1 DRAM / 10GB / 1Gbit), IPv6 включён, BBR включён; ссылка @centhost_bot; #1centhost #ee #vps. (id 230786/230828/231748)
- play2go.cloud - 🇩🇪 Германия, Франкфурт: DE-1 340 руб./мес. (1 vCPU / 2 DRAM / 80GB / 1Gbit), IPv6 отключён, BBR включён; #play2go #de #vps. (id 230801/231293)
- @dhostVPS_bot - 🇩🇪 Германия, Франкфурт: 3 евро./мес. (1 vCPU / 1 DRAM / 10GB / 10Gbit), IPv6 отключён, BBR включён; 💎 Ютуб как RU — Рекламы нет!; #dhost #de #vps. (id 231299/231755)
- @Midas_Hosting_bot - 🇬🇧 Великобритания, Лондон: 4 евро./мес. (2 vCPU / 2 DRAM / 30GB / 3Gbit), IPv6 отключён, BBR включён; 💎 Ютуб — Рекламы нет!; #MHost #gb #vps. (id 231794/231812)
- @nodehost_bot - 🇩🇪 Германия, Франкфурт: 2.2$./мес. (1 vCPU / 1 DRAM / 10GB / 10Gbit), IPv6 отключён, BBR включён; #nodehost #de #vps. (id 231844/231868)
- Node Host Нидерланды: 4.5$/мес (2 vCPU / 2 RAM / 20GB / 10Gbit), IPv6 выключен; «неплохо, большой канал, но айпишник грязноват» (id 228370, tgshtt).
- vds.selectel.ru локации СПб и Москва, 200р/мес (id 228358, Сергей).
- Adminvps.ru 🇩🇪: 1 CPU / 2048МБ RAM / 15ГБ NVMe / до 1Гбит, BBR вкл, IPv6 выкл, 5ТБ трафик, 499₽/мес (id 228789, Никита).
- Ожидания: «чисто теоретически ркн может по поддоменам банить?» (id 230954/230955, Артём).
- «Выборка хостеров» (id 228645, Kamil` Nikiforov): nuxt.cloud отвратительно, сутки выдают, поддержка игнорит; #Несоветую.
- OVH Cloud: «все ноды на половину мёртвые» (id 230623, —), «активно блокируется в рф» (id 231495, Prokurátura).
- 1cent: «дермище» (id 229998, IS); «троит жесть» (id 231688, Рафаэль Мавлютов); «скорость 5 Мбит и сказали фаир политика» (id 231691/231699, Whiteness).
- dhost «норм» (id 228645 — нет; id 231739, 9: dhost мощ; id 229923, saveks: «прям дерьмецо?»).
- Айпишники в чате — не показывать, дудосеры (id 229678/229686, 17/Данч).

## Про баланс/транзакции
- Негативные значения при «Потрачено» — фиксы v3.14.1 (id 228400).
- Кабинет 2.0.0 — еще нет, не скоро (id 227198, id 231197).
- Ошибка получения WATA ссылки: WATA API rate limited on GET /links/... (id 227234, Motion) — Egor фиксит «рейтлимиты ваты» (id 227244/227250).

## Прочее
- Ютуб-роутинг с германии на ру — ютуб без рекламы с ру-нодах (id 229675/229684/230060).
- «Вы вложили сотни часов в эти проекты» — спам закрепов бота.
- «никак нельзя упростить процесс: ссылка на ЛК потом логин в телегу в браузере» (id 228820, Мультитысячник) — учёт мнений (отклонено, открытый вопрос).
- Промокод на скидку: суммируется с базовой скидкой промогруппы — обсуждение (id 228826/228827).
- Nalogo: api.knpd — DNS яндекса на сервере.
- Смотреть чат: АЕЗА не контекст «отвалилась из-за РКН» (id 228275, —). «При полугоде аеза была хороша, потом РКН душит» (id 228942, V M).
- Выборка «гуд» проектов: Pq, The.hosting, Ufo.hosting (id 231233, stayinit). Помечены «не один не советую» — SUPPORT (id 231364).
- Кампании в лк отображают две ссылки (бот/веб) — id 228744/228750.
- bot api 9.4: aiogram 25го - линк https://github.com/aiogram/aiogram/pull/1761/changes (id 227015).
- «Партнерка» (id 230949) — см. выше.
- Ключ AppID в Remna: https://docs.rw/utils/happ-rb (id 226684, Max R — happ routing).
- Выборка Telegram/MTProto: «из за особенности телеги, лучше всего на вифи» (id 227786, —) — (флуд).
- Прокси для телеги: (id 228963/228965, D) — «кто прокси себе делал, подключение долгое» — обсуждение без выводов.
- Vless | JSON подписки (id 230612, Valerii Bezkorovainyi) — вопросы к оформлению ссылки.

## Итог (1 строка)
Заметка: точные changelog'и, alembic-миграции, бэкапы/восстановление, настройка кнопок, кабинеты, конфиги Caddy, блокировки РКН, YouTube (18.02 упал весь мир), blacklist и связку.
