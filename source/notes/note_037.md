# Заметки из chunk_037 (id 215583..221173, 09–12.02.2026)
Веха: вебхуки Remnawave→Bedolaga (v3.10.0, 30 событий), lite mode/FastAPI (v3.9.0), кнопки с цветом в ТГ (новое Bot API 09.02), Remnawave Admin v2.0, массовые блокировки нод РКН 11.02, WaiCore/униклауд падения.

## Релизы (changelog)
- **[id=215670|Egor|09.02.2026](https://t.me/c/2941121338/215670)** Bot v3.9.0: lite mode (эндпоинты для получения и обновления — для будущей облегчённой темы кабинета); персидская локализация (fa); разрешено удаление тарифов с активными подписками; fixes: FK-ссылки на платежи при восстановлении пользователя, синхронизация не перезаписывает end_date неактивных, конвертация max_uses=0 в промокодах, UX триала после промо, пропуски пользователей с активными подписками в очистке неактивных, selection.period.days; кэш file_id логотипа; удалён режим "both" из BOT_RUN_MODE (только polling/webhook); удалён Flask — FastAPI эксклюзивно; удалена smart auto-activation.
- **[id=215673|Egor|09.02.2026](https://t.me/c/2941121338/215673)** Cabinet v1.13.0: empty state страницы подключения; счётчик затронутых подписок при удалении тарифа; проверка приложений перед подпиской; скрыта кнопка «Назад» Telegram; useCloseOnSuccessNotification fix; @floating-ui удалён (циклическая зависимость); локали в отдельный chunk (меньше бандл).
- **[id=216082|Egor|10.02.2026](https://t.me/c/2941121338/216082)** Bot v3.9.1 (хотфикс): сообщение инвойса Heleket не удаляется при проверке статуса; безопасная обрезка HTML preview и fallback при lazy-load подписки; исправлен fallback-запрос подписки (актуальные колонки БД).
- **[id=216158|Egor|10.02.2026](https://t.me/c/2941121338/216158)** **Bot v3.10.0 — вебхуки Remnawave (крупный релиз)**: мгновенная реакция на события подписок вместо периодической синхронизации; кнопка закрытия во всех webhook-уведомлениях; MULENPAY_WEBSITE_URL (редирект после оплаты); унифицированная доставка уведомлений (email + WebSocket); защита webhook-данных (sync/monitoring не перезаписывают данные от вебхуков); fixes: кнопки действий в webhook-уведомлениях, пустые имена устройств, арабский шаблон SUBSCRIPTION_INFO, non-HTTP диплинки в crypto link, композитное имя устройства (platform+hwid), транзиентные API-ошибки 502/503/504 понижены до warning, время инициации платежа в transaction created_at, webhook handlers, retry loop CryptoBot, cabinet-платежи сохраняются в БД, синхронизация статуса подписки из панели в user.modified.
  **30 событий**: user.expired/.disabled/.enabled/.limited/.traffic_reset/.modified/.deleted/.revoked/.created/.first_connected/.bandwidth_usage_threshold_reached/.not_connected/.expired_24_hours_ago; user_hwid_devices.added/.deleted; node.created/.modified/.disabled/.enabled/.deleted/.connection_lost/.connection_restored/.traffic_notify; service.panel_started/.login_attempt_failed/.login_attempt_success/.subpage_config_changed; crm.infra_billing_node_payment_in_7_days/.in_48hrs/.in_24hrs/.due_today/.overdue_24hrs/.overdue_48hrs/.overdue_7_days.
  **Настройка (в боте)**: REMNAWAVE_WEBHOOK_ENABLED=true / REMNAWAVE_WEBHOOK_PATH=/remnawave-webhook / REMNAWAVE_WEBHOOK_SECRET=<openssl rand -hex 32> (мин 32, реально 64 символа [id=217301|zyko](https://t.me/c/2941121338/217301)).
- **[id=218555|Egor|11.02.2026](https://t.me/c/2941121338/218555)** Cabinet v1.14.0: компактная страница логина (OAuth в ряд иконок, email-форма за пилл-кнопку «Войти по Email», 100dvh); guard oauthProviders с Array.isArray (краш в Telegram WebView); hardened OAuth (open redirect, path traversal, info leak); CryptoBot openTelegramLink (инвойс внутри ТГ); нейтральный тёмный фон лого; inline email change в Profile (модалка удалена, 491 строка); inline forgot password (jank на Safari iOS fix).
- **[id=218555|Egor|11.02.2026](https://t.me/c/2941121338/218555)** **Bot v3.10.1 (хотфикс)**: расширен бэкап до 68 моделей (+37: payment providers, polls, contests, wheel, FAQ, promo offers, webhooks, configs, menu buttons), association tables; атомарность транзакций (flush вместо commit); tarfile filter='data' (path traversal); сохраняется купленный трафик при продлении того же тарифа (сброс purchased_traffic_gb только при is_tariff_change=True); детекция смены тарифа (classic→tariff); очистка данных подписки при удалении юзера из панели; покупка разрешена при пересчитанной цене ниже кэшированной; CryptoBot приоритет bot_invoice_url (инвойс внутри ТГ); None-safety guards; Telegram timeout → warning; StaleDataError в webhook; Greenlet errors после rollback; подавлено "message is not modified"; flush в server counter; fallback на callback при MINIAPP_CUSTOM_URL не установлен.
- **[id=220724|—|12.02.2026](https://t.me/c/2941121338/220724)** **Bot v3.10.2 (хотфикс)**: Race condition: YooKassa SELECT FOR UPDATE; subtract_user_balance блокировка строки; транзакция до коммита; авто-возврат средств (REFUND) если extend_subscription падает после списания; savepoint вместо полного rollback; сериализация time/date в бэкапах (daily_summary_time из ReferralContest .isoformat()); «bot was blocked by the user» → debug; UnboundLocalError get_logo_media.
- **[id=220923|Egor|12.02.2026](https://t.me/c/2941121338/220923)** **Bot v3.10.3 (хотфикс)**: обработка unique constraint при восстановлении бэкапа без очистки БД; укрепление создания/восстановления бэкапов (Decimal→float, NaN/infinity→0.0, невалидный JSON→string fallback, savepoints для дубликатов); deadlock при обновлении счётчиков серверов (sorted lock ordering); сломанная кнопка «Докупить трафик» в webhook-уведомлении. **12 toggle-настроек уведомлений**:
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
- **[id=220723|Egor|12.02.2026](https://t.me/c/2941121338/220723)** Cabinet v1.14.1 (хотфикс): смена email для неподтверждённых адресов (без кода, верификация на новый); безлимитный трафик — исправлена проверка selectedTrafficPackage !== null (gb=0 для безлимита скрывал кнопку), кнопка «Купить безлимит», ключ buyUnlimited в 4 локалях.
- **[id=218267|Илья|10.02.2026](https://t.me/c/2941121338/218267)** Remnawave Admin v2.0 (Case211): RBAC, Dashboard с графиками, Fleet Monitoring, Automation Engine (CRON-правила), аудит/аналитика, темы (6 тёмных + 1 светлая), MaxMind GeoLite2, command palette, CLI (сброс пароля, суперадмин); 25+ багфиксов. https://github.com/case211/remnawave-admin
- **[id=216115|Илья|10.02.2026](https://t.me/c/2941121338/216115)** Remnawave Admin v1.8.1: массовые операции + подтверждение, чекбоксы в таблице Users, экспорт данных, глобальный поиск, мониторинг (требует обновить Node-Agent).
- **[id=216109|—|10.02.2026](https://t.me/c/2941121338/216109)** Telegram Bot API 09.02.2026 (ссылка core.telegram.org/bots/api-changelog#february-9-2026): боты могут использовать премиум-эмодзи (раньше только с ником через Фрагмент); цветные кнопки; новые [id=219715|saveks](https://t.me/c/2941121338/219715) — «жду на наших ботах» (реализовано у c0mrade: цветные кнопки на оплату; **[id=220316|c0mrade](https://t.me/c/2941121338/220316)** «В боте бедолаги не как» — в Bedolaga пока не реализовано).

## Настройка вебхуков Remnawave → Bedolaga (полный гайд)
- **[id=216359|Name Lastname|10.02.2026](https://t.me/c/2941121338/216359)** «Как получить письмо счастья»:
  - В .env бота:
    ```
    REMNAWAVE_WEBHOOK_ENABLED=true
    REMNAWAVE_WEBHOOK_PATH=/remnawave-webhook
    REMNAWAVE_WEBHOOK_SECRET=<openssl rand -hex 32>
    ```
  - В .env панели Remnawave (снизу, уже есть блок):
    ```
    ### WEBHOOK ###
    WEBHOOK_ENABLED=true
    ### Only https:// is allowed
    WEBHOOK_URL=https://hooks.domen.ru/remnawave-webhook
    ### This secret is used to sign the webhook payload, must be exact 64 characters. Only a-z, 0-9, A-Z are allowed.
    WEBHOOK_SECRET_HEADER=<тот же секрет>
    ```
  - В Caddyfile remnawave (для панели+бота на одном сервере):
    ```
    hooks.domen.ru {
      encode gzip zstd
      @config path /app-config.json
      header @config Access-Control-Allow-Origin "*"
      handle /remnawave-webhook {
        reverse_proxy remnawave_bot:8080 {
            header_up Host {host}
            header_up X-Real-IP {remote_host}
            transport http { read_buffer 0 }
        }
      }
      reverse_proxy remnawave_bot:8080 { ... }
    }
    ```
  - Перезагрузить caddy, бота, панель. Порядок: сначала запускаешь бота и проксю с включенным вебхуком, потом перезапускаешь панель, чтобы она после 3 неудачных попыток не вырубила вебхук ([id=216262|SusAdmin](https://t.me/c/2941121338/216262)). «Нет UI-раздела Настройки>Вебхуки — это ошибка в описании, вся настройка в .env панели» ([id=216569|xexe](https://t.me/c/2941121338/216569), [id=217101|Anton Khakin](https://t.me/c/2941121338/217101)).
  - Проверка: `curl -s https://hooks.domain.com/remnawave-webhook | jq` → ожидаемый ответ `{"status": "ok", "service": "remnawave_webhook", "enabled": true}` ([id=217201|—](https://t.me/c/2941121338/217201)).
  - «Ремна есть три попытки чтобы достучаться до вебхука, если не получилось, она больше не пытается и не срёт ошибками в логах; ищи ошибку "не удалось отправить вебхук" в логах ремны» ([id=216332|SusAdmin](https://t.me/c/2941121338/216332)).
  - Секрет exact 64 символа, только a-z 0-9 A-Z ([id=216322|SusAdmin](https://t.me/c/2941121338/216322)).
  - Ивенты задаются в панели .env (WEBHOOK_EVENTS=user.expired,...) [id=217403|zyko](https://t.me/c/2941121338/217403). При изменении: REST панели, потом caddy reload, потом бот.
- **[id=217413|—|10.02.2026](https://t.me/c/2941121338/217413)** Полный Caddyfile hooks-домена (пример реального рабочего):
  ```
  # Hooks + API
  hooks.domen.ru {
      encode gzip zstd
      handle /webhook { reverse_proxy remnawave_bot:8080 {...} }
      handle /remnawave-webhook { reverse_proxy remnawave_bot:8080 {...} }
      handle /yookassa-webhook { ... }
      handle /platega-webhook { ... }
      handle /cryptobot-webhook { ... }
      handle /wata-webhook { ... }
      handle /heleket-webhook { ... }
      handle /tribute-webhook { ... }
      handle /pal24-webhook { ... }
      handle /mulenpay-webhook { ... }
      handle /app-config.json { header Access-Control-Allow-Origin "*"; reverse_proxy remnawave_bot:8080 {...} }
      handle /go { redir {query.u} 302 }
      handle { reverse_proxy remnawave_bot:8080 {...} }
  }
  # Статика для кабинета
  lk.domen.app {
      root * /srv/cabinet
      encode gzip
      handle /api/* {
          uri strip_prefix /api
          reverse_proxy remnawave_bot:8080
      }
      @websockets {
          header_regexp Connection *Upgrade*
          header        Upgrade websocket
      }
      handle /cabinet/ws {
          uri strip_prefix /api
          reverse_proxy remnawave_bot:8080 {
              transport http { read_timeout 0; write_timeout 0 }
          }
      }
      handle {
          try_files {path} /index.html
          file_server
      }
  }
  ```
- **[id=217513|—|10.02.2026](https://t.me/c/2941121338/217513)** Альтернативный простой Caddyfile (если бот/кабинет/панель всё на одном сервере и бот не отдельный домен):
  ```
  https://panel.mikaeladbd.xyz { reverse_proxy http://remnawave:3000 }
  https://subs.mikaeladbd.xyz { reverse_proxy http://remnawave-subscription-page:3010 }
  https://hooks.mikaeladbd.xyz {
      encode gzip zstd
      handle /platega-webhook { reverse_proxy remnawave_bot:8080 {...} }
      handle /freekassa-webhook { reverse_proxy remnawave_bot:8080 {...} }
      handle /remnawave-webhook { reverse_proxy remnawave_bot:8080 {...} }
      handle { reverse_proxy remnawave_bot:8080 {...} }
  }
  :443 { tls internal; respond 204 }
  ```
- **[id=217720|—|10.02.2026](https://t.me/c/2941121338/217720)** У nginx-proxy-manager webhook можно настроить отдельным портом (в .env бота и платёжках, потом в caddy). Remnawave-webhook передавать на единый вебсервер бота.
- **[id=218220|—|10.02.2026](https://t.me/c/2941121338/218220)** Статус хука 200, но бот не реагирует: попробуй "REST"/rest — перезапустить. Совпало.
- **[id=218489|—|11.02.2026](https://t.me/c/2941121338/218489)** «invalid signature» в логах webhook — секрет в ремне != секрет в боте (совпадает должен).
- **[id=218528..218530|Максим Гаврилов|11.02.2026](https://t.me/c/2941121338/218528)** Ошибка отправки в топик «chat not found» — нужно пересоздать топик и дать боту доступ (группу пересоздать).
- **[id=218726|Егор|11.02.2026](https://t.me/c/2941121338/218726)** Домен обязателен для панели, сабки, бота и ноды; отдельные поддомены.

## Кабинет: сборка/обновления (v1.14.x)
- **[id=215677|Андрей/Дмитрий|09.02.2026](https://t.me/c/2941121338/215677)** Кабину обновить: `git pull origin main && docker builder prune -a -f && docker compose down && docker compose build --no-cache && docker compose up -d && docker compose logs -f`.
- **[id=216539..216569|Сергей/wsq22|10.02.2026](https://t.me/c/2941121338/216539)** «Нейронка хуйню написала, в енв делай» — конфиг для кабинета не из ремны, а отдельно.
- **[id=217659..217663|Данч/Мультитысячник|10.02.2026](https://t.me/c/2941121338/217659)** Команда обновления:
  ```
  git pull origin main
  docker compose build
  docker compose down
  docker compose up
  ```
- **[id=217700|Max R|10.02.2026](https://t.me/c/2941121338/217700)** Кабинет: блок статических файлов из хранилища (root /srv/cabinet) работает не всегда (нужен cabinet-dist), предпочтительнее парсить из папки dist. Сборка (для /api) + nginx-proxy-manager default:
  ```
  services:
    cabinet-frontend:
      build:
        context: .
        dockerfile: Dockerfile
        args:
          VITE_API_URL: ${VITE_API_URL}
          VITE_TELEGRAM_BOT_USERNAME: ${VITE_TELEGRAM_BOT_USERNAME}
          VITE_APP_NAME: ${VITE_APP_NAME}
          VITE_APP_LOGO: ${VITE_APP_LOGO}
      container_name: cabinet_frontend
      restart: unless-stopped
      ulimits:
        nofile: { soft: 1048576, hard: 1048576 }
      env_file: [ .env ]
      networks: [ remnawave-network, nginx-proxy-manager_default, bot_network ]
  networks:
    bot_network: { external: true, name: remnawave-bedolaga-telegram-bot_bot_network }
    remnawave-network: { external: true, name: remnawave-network }
    nginx-proxy-manager_default: { external: true }
  ```
- **[id=216491..216519|Max R|10.02.2026](https://t.me/c/2941121338/216491)** Caddy-блок для кабинета (кеш):
  ```
  encode gzip zstd
  handle /api/* {
      uri strip_prefix /api
      header /api/* Cache-Control "no-cache, no-store, must-revalidate"
      reverse_proxy remnawave_bot:8080
  }
  handle {
      reverse_proxy cabinet_frontend:80
      @static { path *.css *.js *.png *.jpg *.jpeg *.gif *.ico *.svg *.woff *.woff2 }
      header @static Cache-Control "public, max-age=86400, must-revalidate"
  }
  ```
- **[id=220593|Max R|12.02.2026](https://t.me/c/2941121338/220593)** Правильный html-кеш в Caddy (блок лк, @html matcher):
  ```
  @html {
      path *.html /
  }
  header @html {
      Cache-Control "no-cache, no-store, must-revalidate"
      Pragma "no-cache"
      Expires "0"
  }
  ```
  (ошибка «unrecognized matcher name: @html» — матчер без path)
- **[id=220889|Egor|12.02.2026](https://t.me/c/2941121338/220889)** Каноничный Caddyfile кабинета (от Егора):
  ```
  {$CABINET_DOMAIN} {
      import geoip_block
      encode gzip zstd
      handle /api/* {
          uri strip_prefix /api
          reverse_proxy remnawave_bot:8080 { import proxy_defaults }
      }
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
- **[id=220934|—|12.02.2026](https://t.me/c/2941121338/220934)** «Веб совет должен лететь на бота, а не на кабинет; в реадми для caddy есть написано, для nginx нет — для nginx всего 2 локали апи в бота, всё остальное в кабинет, про вебсокет не указано».
- **[id=218464..218488|—/Mike Bell|11.02.2026](https://t.me/c/2941121338/218464)** «Как поменять тексты»: локали (app/locales), все .env из докера дублируются вручную в .env бота. «С кабинетом ни разу не работал, но судя по всему он также тянет из бота».
- **[id=218657..218676|Илья|11.02.2026](https://t.me/c/2941121338/218657)** Универсальная инструкция обновления через git (общая):
  ```
  git status
  git stash
  git pull origin main
  # при конфликтах: git checkout --theirs <файл> && git add <файл> && git commit
  git stash pop
  docker compose down
  docker compose up -d --build
  docker compose logs -f
  ```
- **[id=218659|Name Lastname|11.02.2026](https://t.me/c/2941121338/218659)** «После перезагрузки в топик информация придет сообщение от панели ремны» (service.panel_started) — как проверка работоспособности вебхука.
- **[id=218643..218644|—|11.02.2026](https://t.me/c/2941121338/218643)** Обновлять кабинет и бота с веткой dev на тестах: `git pull origin dev && make reload` (беру каждый раз последнюю); сравнение с веткой на dev-ветке до перехода в main.
- **[id=218075|интерестед|10.02.2026](https://t.me/c/2941121338/218075)** Для кабинета (если dist-сборка копируется) — команда обновления с копированием из /app/dist в /root/cabinet-dist.

## Кабинет: баги/фиксы (10–12.02)
- **[id=216309|Alex|10.02.2026](https://t.me/c/2941121338/216309)** Тарифы/сквады не синкаются для текущих подписчиков; в юзере в синхронизации не подтягиваются устройства и сквады; в подписке devices=1 (не из тарифа); из-за этого синк юзера всегда показывает, что что-то не засинканно.
- **[id=216517|Юрий|10.02.2026](https://t.me/c/2941121338/216517)** Реверс: автопродление накидывает +200 рублей непонятно откуда (тариф 2 устройства, у юзера 4 активных — за каждое доплата 100р; цена устройства 0 не влияет [id=216514|Acid Wizard](https://t.me/c/2941121338/216514)) — «это не влияет».
- **[id=216594|—|10.02.2026](https://t.me/c/2941121338/216594)** WaiCore (Германия) **лежит ~15:15 10.02**; из РФ не пускал; dhost «каждый месяц какую-то херню исполняет» [id=216316|Deleted Account](https://t.me/c/2941121338/216316).
- **[id=217657|Max R|10.02.2026](https://t.me/c/2941121338/217657)** Кабинет: при каждом обновлении имени бота/лого не применяется у всех, у кого-то старые бренды; смена лого применяется через обновление страницы [id=217581|Max R](https://t.me/c/2941121338/217581); на телефоне не сменилось даже после очистки WebView кеша ([id=217601|Max R](https://t.me/c/2941121338/217601) «на айфоне вот это»).
- **[id=217741|Max R|10.02.2026](https://t.me/c/2941121338/217741)** На ПК/iphone не сменилось «Telegram бот не настроен» — фиксит после обновы.
- **[id=217743|—|10.02.2026](https://t.me/c/2941121338/217743)** WaiCore fинк а упала «на 16-17:16» 10.02 — [id=217649|—](https://t.me/c/2941121338/217649); «на аезе всегда работает» [id=218696|И҉л҉ь҉я҉с҉](https://t.me/c/2941121338/218696).
- **[id=217742|Максим Гаврилов|10.02.2026](https://t.me/c/2941121338/217742)** WaiCore и 1Сент/сервхост/play2go «на билайне (моб. не работает, с домашнего мтс/ркн/йота ок)».
- **[id=216859|—|10.02.2026](https://t.me/c/2941121338/216859)** WaiCore DE упал 08.02 (часть ранних дней). «Основная веха: 10.02 Waicore лежал 15:15, 11.02 тоже упал (500+ чел, Германия и dhost Нидерланды)».
- **[id=219004|Whiteness|11.02.2026](https://t.me/c/2941121338/219004)** Waicore 500+ пользователей (Германия от них, Нидерланды от dhost) — упал 11.02.
- **[id=215976|—|10.02.2026](https://t.me/c/2941121338/215976)** «cabina перезагрузка-«Подключить устройства»→ пустая страница при реальном объёме 2/4; при обновлении на 3.10.0; пофиксено в 3.10.1».
- **[id=216608|Сергей|10.02.2026](https://t.me/c/2941121338/216608)** «нода забанена РКН» — «если ufw был выключен и порт 25 открыт» — «юзеры её сразу в spamhaus вогнали»; порт 25 принудительно закрывать.
- **[id=216845|—|10.02.2026](https://t.me/c/2941121338/216845)** «WaiCore (Германия, 4/8)» — 2/4 «для нормальной работы маловато» [id=216781|—](https://t.me/c/2941121338/216781); «Скачал за 1 день 170 гигов» [id=216414|ТОЧНА НЕ ВПН](https://t.me/c/2941121338/216414).
- **[id=217763|—|10.02.2026](https://t.me/c/2941121338/217763)** «Обратно не вернуть с 3.10 на 3.7» [id=217763|—](https://t.me/c/2941121338/217763).
- **[id=217785..217787|—|10.02.2026](https://t.me/c/2941121338/217785)** «плавающий» bug на 3.10.0 — юзеры-подписки-гео иногда вылетает (ошибка 'NoneType'>'int'), автор обещал фикс; ушло на v3.10.1.
- **[id=217796..217799|—|10.02.2026](https://t.me/c/2941121338/217796)** «В кабинете не заменяется бренд/лого/кабине (cabina) — правки в caddy на кабинет не помогли (у Max R)». У Max R: «капчить Caddy\Batch».
- **[id=217778|Сергей|10.02.2026](https://t.me/c/2941121338/217778)** «Bedolaga Bot v3.10: пустые уведы, платежи идут, но email-шаблоны текстовые — поправим» (в 3.10.1 [id=218569|—](https://t.me/c/2941121338/218569)).
- **[id=217783|Сергей|10.02.2026](https://t.me/c/2941121338/217783)** «Дрон» «проц» — не ясен.
- **[id=217786|Сергей|10.02.2026](https://t.me/c/2941121338/217786)** Кабинет слетает «Настройки > Вебхуки» — это «не в UI панели, а в .env панели» ([id=217773|Anton Khakin](https://t.me/c/2941121338/217773)).
- **[id=217784..217789|—|10.02.2026](https://t.me/c/2941121338/217784)** Cabina и «фирка в ТГ» (v2raytun-кэш): сохраняется только «выбор платформы»; тэг #решала; не всегда помогает.
- **[id=217789|—|10.02.2026](https://t.me/c/2941121338/217789)** «Мешалоты: kabina с aezой/2j» — контекст.
- **[id=217787|—|10.02.2026](https://t.me/c/2941121338/217787)** Кабинет/гит «Your branch and origin/main have diverged» — см. гайд 218643.
- **[id=217798|Максим Гаврилов|10.02.2026](https://t.me/c/2941121338/217798)** «где настроить nginx.conf для кабинета» — у 2 телега аккаунта дефолтная брендинга осталась [id=217785|Max R](https://t.me/c/2941121338/217785).

## Прочее Bedolaga/Remnawave (фиксы 09–12.02)
- **[id=215681..215694|ALIEN|09.02.2026](https://t.me/c/2941121338/215681)** Сквады: в новом тарифе не появились сервера у старых подписчиков; кнопка «добавить всех пользователей» в админке (не в кабинете).
- **[id=215597..215600|_init_(Даниил)/Ivan Raucher|09.02.2026](https://t.me/c/2941121338/215597)** Ошибку удаления пользователя «cannot access local variable 'settings' where it is not associated with a value» — убран (v3.9.0).
- **[id=215647|—|09.02.2026](https://t.me/c/2941121338/215647)** «Актуально ли SNI на БС» — нет [id=215648|Haxonate](https://t.me/c/2941121338/215648).
- **[id=215672|Alex|09.02.2026](https://t.me/c/2941121338/215672)** Urlpay (Mulenpay) возврат на сайт после оплаты — [id=216249|—](https://t.me/c/2941121338/216249): "Выказать попросил сделал" (составить) настройка [id=216249|—](https://t.me/c/2941121338/216249). VITE_TELEGRAM_BOT_USERNAME: [id=216249|—](https://t.me/c/2941121338/216249) (для ссылки на кабинет).
- **[id=215941..215957|Aero/Sayonara/—|10.02.2026](https://t.me/c/2941121338/215941)** Кэш (таймаут 3 часа) на Waicore+1сент — просто «поправлено».
- **[id=215952..215955|Aero/—|10.02.2026](https://t.me/c/2941121338/215952)** «Итог: "медленные операции" 1-2-3-5 с после обновы; обновись, крайняя версия».
- **[id=216541..216549|Великий/—|10.02.2026](https://t.me/c/2941121338/216541)** «Плавающая ошибка сервера» / МТProxy (telegram)/ Плюсами «mail» и т.д. — по желанию.
- **[id=216605|torro xD|10.02.2026](https://t.me/c/2941121338/216605)** «HSHP тоже заскамился, забанил без причины 2 сервера» — [id=218892|Haxonate](https://t.me/c/2941121338/218892) «Подскажет кто?».
- **[id=216785..216789|—|10.02.2026](https://t.me/c/2941121338/216785)** Как штраф «зайти в тарифы и выключить (проверить =)». Иный же путь - в этом же тарифе [id=216792|Сергей](https://t.me/c/2941121338/216792).
- **[id=216818|Сергей|10.02.2026](https://t.me/c/2941121338/216818)** «WaiCore 15:15 10.02» + [id=216789|—](https://t.me/c/2941121338/216789) — [id=216781|—](https://t.me/c/2941121338/216781).
- **[id=216838..216841|—|10.02.2026](https://t.me/c/2941121338/216838)** «НГК» «Микс» - [id=216841|—](https://t.me/c/2941121338/216841).
- **[id=216855|—|10.02.2026](https://t.me/c/2941121338/216855)** «WaiCore плавающий» на 10.02 (и 11.02 [id=219004|Whiteness](https://t.me/c/2941121338/219004)).
- **[id=216856..216857|—|10.02.2026](https://t.me/c/2941121338/216856)** «хост хер поймешь» (Билайн/МТС/Ростелеком) - [id=216845|—](https://t.me/c/2941121338/216845).
- **[id=216857|—|10.02.2026](https://t.me/c/2941121338/216857)** «оператор не поддерживает».
- **[id=216865..216866|—|10.02.2026](https://t.me/c/2941121338/216865)** «SNI временно некоторые работают» [id=217092|Рис по Вьетнамски](https://t.me/c/2941121338/217092).
- **[id=217037|—|10.02.2026](https://t.me/c/2941121338/217037)** «Чтобы все было по феншую» / «Куча в РКН-режиме» / «упал серверов СЕРВХОСТ» [id=216808|—](https://t.me/c/2941121338/216808).
- **[id=217038|—|10.02.2026](https://t.me/c/2941121338/217038)** «чтобы внизу наблюдал» [id=217038|—](https://t.me/c/2941121338/217038).
- **[id=217039|—|10.02.2026](https://t.me/c/2941121338/217039)** «по документации» [id=217039|—](https://t.me/c/2941121338/217039).
- **[id=217046|Александр|10.02.2026](https://t.me/c/2941121338/217046)** «им прямо».
- **[id=217059..217071|—|10.02.2026](https://t.me/c/2941121338/217059)** «С СБП платежи (я в ipeway)» — [id=216786|Андрей](https://t.me/c/2941121338/216786).
- **[id=217084..217089|—|10.02.2026](https://t.me/c/2941121338/217084)** «кабинета из-за то, что приложеньки нет» [id=217086|—](https://t.me/c/2941121338/217086).
- **[id=217071|Сергей|10.02.2026](https://t.me/c/2941121338/217071)** WaiCore (Germa) «WaiCore не упал, просто лежал» [id=216594|—](https://t.me/c/2941121338/216594).
- **[id=216664|torro xD|10.02.2026](https://t.me/c/2941121338/216664)** «конец строки» [id=216665|—](https://t.me/c/2941121338/216665).
- **[id=216586..216599|—|10.02.2026](https://t.me/c/2941121338/216586)** МСК/UTC.
- **[id=216916..216924|—|10.02.2026](https://t.me/c/2941121338/216916)** «Если у тебя MTS/Ростелеком/Мег» [id=216859|—](https://t.me/c/2941121338/216859).
- **[id=217082..217094|—|10.02.2026](https://t.me/c/2941121338/217082)** WaiCore! [id=216866..216867|—](https://t.me/c/2941121338/216866).

## Прочее Remnawave/Bedolaga (выжимка 10–12.02)
- **[id=216616|Сергей|10.02.2026](https://t.me/c/2941121338/216616)** Kassa.ai webhook — путь /kassa-ai-webhook, порт 8080 (по аналогии с остальными).
- **[id=216784..216787|—|10.02.2026](https://t.me/c/2941121338/216784)** Шейпер/заглушки.
- **[id=217046|Александр|10.02.2026](https://t.me/c/2941121338/217046)** «WaiCore лежал 16:17-17:16» [id=216838..216841|—](https://t.me/c/2941121338/216838).
- **[id=216859|—|10.02.2026](https://t.me/c/2941121338/216859)** «1-2-3-5 сек» 3.10.0; пофиксено 3.10.1.
- **[id=216939..216946|Anton Khakin/Сергей|10.02.2026](https://t.me/c/2941121338/216939)** «Как фиксить время UTC в панели» - пофиксено в 3.10.0 ([id=216916|—](https://t.me/c/2941121338/216916)).
- **[id=217292|libkit|10.02.2026](https://t.me/c/2941121338/217292)** Платежи юкасса [id=216645..216646|—](https://t.me/c/2941121338/216645).
- **[id=216670..216677|Max R/—|10.02.2026](https://t.me/c/2941121338/216670)** «все что связано с bf (Русские)».
- **[id=216842..216855|—|10.02.2026](https://t.me/c/2941121338/216842)** «именно черное «Макс, 2/4/» [id=216793|Сергей](https://t.me/c/2941121338/216793).
- **[id=216913..216917|—|10.02.2026](https://t.me/c/2941121338/216913)** «генерирует и сабка».
- **[id=217082..217089|—|10.02.2026](https://t.me/c/2941121338/217082)** WaiCore!

## Общая рекомендация (проверка сервера)
- **[id=218990..218995|IS|11.02.2026](https://t.me/c/2941121338/218990)** Локации: Финляндия/Венгрия (хз), Эстония, Германия, Румыния, Польша [id=219664|—](https://t.me/c/2941121338/219664) «Польша» / Нидерланды.
- **[id=219447|Valerii Bezkorovainyi|11.02.2026](https://t.me/c/2941121338/219447)** Waicore/ASD (odv): «норм хост», «норм» [id=219654|—](https://t.me/c/2941121338/219654).

## Прочее (10–12.02)
- **[id=216758|—|10.02.2026](https://t.me/c/2941121338/216758)** «Что это за прикол себе?».
- **[id=216881..216886|—|10.02.2026](https://t.me/c/2941121338/216881)** «именно «оплату» и «зарегистрировался» и «нальчик» и т.д.».
- **[id=216956..216964|—|10.02.2026](https://t.me/c/2941121338/216956)** «клиентское ядро» [id=216911|—](https://t.me/c/2941121338/216911).
- **[id=217237|—|10.02.2026](https://t.me/c/2941121338/217237)** «Тыж/онлц» [id=217236..217238|—](https://t.me/c/2941121338/217236).
- **[id=217241..217243|—|10.02.2026](https://t.me/c/2941121338/217241)** «по прошествии».
- **[id=217292|libkit|10.02.2026](https://t.me/c/2941121338/217292)** «Bedolaga Bot v3.10.x: "подписка недоступна" — каждый».
- **[id=217382..217389|Max R|10.02.2026](https://t.me/c/2941121338/217382)** «в хорошей скорости 6.01s» [id=217372|—](https://t.me/c/2941121338/217372).
- **[id=217422|Сергей|10.02.2026](https://t.me/c/2941121338/217422)** «120 пользователей» [id=216757|—](https://t.me/c/2941121338/216757).
- **[id=216913..216917|—|10.02.2026](https://t.me/c/2941121338/216913)** «Ошибка при создании агента» — «АжурКлиент», пофиксено 3.10.1 [id=218569|—](https://t.me/c/2941121338/218569).
- **[id=217043|—|10.02.2026](https://t.me/c/2941121338/217043)** «Mikaeladbd.xyz (Svedia)» [id=217286|—](https://t.me/c/2941121338/217286).
- **[id=217112|Anton Khakin|10.02.2026](https://t.me/c/2941121338/217112)** «Домен только для панели» [id=217112|—](https://t.me/c/2941121338/217112).

## Прочее Bedolaga/Remnawave (выжимка 11–12.02)
- **[id=219127|DonkyBoss|11.02.2026](https://t.me/c/2941121338/219127)** Гонконг/Финляндия «Ищу японку с норм bgp. Нашел только Гонконг пинг 90-100» [id=218913|снупс Догс](https://t.me/c/2941121338/218913).
- **[id=219875|tneangel|11.02.2026](https://t.me/c/2941121338/219875)** Рекомендуемые конфигурации (от Egor [id=219873..219887|—](https://t.me/c/2941121338/219873)): «для начальной работы 4/8»; «и панелке и боту 4/8»; «минимум».
- **[id=219881..219882|—|11.02.2026](https://t.me/c/2941121338/219881)** «4/8 норм до 100к юзеров».
- **[id=219884|—|11.02.2026](https://t.me/c/2941121338/219884)** «8/16 nexus хороший» [id=219914|Valerii](https://t.me/c/2941121338/219914).
- **[id=219889|—|11.02.2026](https://t.me/c/2941121338/219889)** «на виртуалке смотри скок ресов по факту выделяется» [id=219917|Egor](https://t.me/c/2941121338/219917).
- **[id=219951..219955|Prokurátura/𝓒𝓒𝟏𝟑𝟑𝟕|11.02.2026](https://t.me/c/2941121338/219951)** SMTP: «592 порт» / «25 порт» / «без почтового порта».
- **[id=219982..219995|Максим Гаврилов/𝓒𝓒𝟏𝟑𝟑𝟕|11.02.2026](https://t.me/c/2941121338/219982)** SMTP: «please run connect() first» — из-за верификации по email (не включена в кабинете) [id=220121|𝓒𝓒𝟏𝟑𝟑𝟕](https://t.me/c/2941121338/220121).
- **[id=219998|Максим Гаврилов/𝓒𝓒𝟏𝟑𝟑𝟕|11.02.2026](https://t.me/c/2941121338/219998)** «Фикс SMTP (Temporary failure in name resolution)»:
  ```
  SMTP_USE_STARTTLS=true
  ```
  + в docker-compose бота добавить dns:
  ```
  services:
    remnawave_bot:
      dns:
        - 1.1.1.1
        - 8.8.8.8
  ```
- **[id=220042|Максим Гаврилов|11.02.2026](https://t.me/c/2941121338/220042)** Проверка SMTP:
  ```
  swaks -4 --server smtp.yandex.ru --port 587 --auth-user info@domain.com --auth-password ... --to vv@domain.ru --from info@domain.com --tls
  nc -4 -zv smtp.yandex.ru 587
  openssl s_client -starttls smtp -connect smtp.yandex.ru:587
  ```
  (по ipv4 всё ок; по ipv6 «Temporary failure» у обоих).
- **[id=220125|Valerii Bezkorovainyi|11.02.2026](https://t.me/c/2941121338/220125)** «Настройки SMTP лучше добавлять прямо в .env файл. Из кабинета не тянет» [id=220124|Мультитысячник](https://t.me/c/2941121338/220124).
- **[id=220216..220222|xexe|11.02.2026](https://t.me/c/2941121338/220216)** Platega-методы: `PLATEGA_ACTIVE_METHODS=2,10,11,12,13` — 2 СБП, 11 карточный, 13 крипта [id=220221|valera](https://t.me/c/2941121338/220221). Дока: https://docs.platega.io/
- **[id=220226|V M|11.02.2026](https://t.me/c/2941121338/220226)** Юкасса: после оплаты не перебрасывает — с СБП [id=220613|Fantom](https://t.me/c/2941121338/220613): «SPБ подключен по умолчанию», «Через поддержку подключили, оказывается сразу она не активна» — метод 2 (СБП) включить в ЛК.
- **[id=220246|—|11.02.2026](https://t.me/c/2941121338/220246)** Platega: аккаунт заблокирован, «верификационный платёж» — нужен донат с 5000 р на новом аккаунте; **[id=220243|—](https://t.me/c/2941121338/220243)** «регал на свои данные — забанили».
- **[id=220262|Андрей|11.02.2026](https://t.me/c/2941121338/220262)** WaiCore «у меня N2CPU падал по всему серверу» (DDoS от вымогателей — «Система уже вернулась в стабильную работу. Платежи проходят без задержек»).
- **[id=220273|DAUNAMORAL|11.02.2026](https://t.me/c/2941121338/220273)** «как всем пользователям включить автопродление» — «ручками» / «в бд» [id=220284|—](https://t.me/c/2941121338/220284).
- **[id=220321|снупс Догс/Ramil Mers|11.02.2026](https://t.me/c/2941121338/220321)** Ошибка бэкапа «Object of type time is not JSON serializable» — пофикшено в v3.10.2.
- **[id=220327|c0mrade|11.02.2026](https://t.me/c/2941121338/220327)** «Telegram Bot API 09.02: приватные чаты с ботами, стриминг ответа (для AI), тематические чаты (топики)» — [id=220351|c0mrade](https://t.me/c/2941121338/220351).
- **[id=220401|V M|11.02.2026](https://t.me/c/2941121338/220401)** «selfhost - то днс балансировка возможна?» — [id=220401|—](https://t.me/c/2941121338/220401).
- **[id=220404..220415|Егор/—|11.02.2026](https://t.me/c/2941121338/220404)** «подписки отъебнули» 23:06 11.02 — «подниму из могилы» [id=220414|Егор](https://t.me/c/2941121338/220414).
- **[id=220469..220477|—|11.02.2026](https://t.me/c/2941121338/220469)** Редирект happ (с sub.example.ru/happ%3A%2F%2Fadd%2F... на sub.example.ru/<uuid>) — режим guide.
- **[id=220511|Max R|11.02.2026](https://t.me/c/2941121338/220511)** «кабинет из-за разных портов» [id=220511|—](https://t.me/c/2941121338/220511).
- **[id=221057..221061|567/Дмитрий|12.02.2026](https://t.me/c/2941121338/221057)** Cloudflare домен на VK-нодах → не работает в БС [id=221076|—](https://t.me/c/2941121338/221076).
- **[id=221137|Name Lastname|12.02.2026](https://t.me/c/2941121338/221137)** Миграция/БД: «DATABASE_MODE» / «DATABASE_URL» / «POSTGRES_USER» / «POSTGRES_PASSWORD» [id=221166..221168|—](https://t.me/c/2941121338/221166).
- **[id=221172|V M|12.02.2026](https://t.me/c/2941121338/221172)** «Можно оставить сообщение об обязательной подписке, но не требовать её обязательной? И в идеале изменить сообщение» [id=221172|—](https://t.me/c/2941121338/221172).

## Прочее: поиск по тегам, банлисты, тарифы
- **[id=215678|Дмитрий/Лейн|09.02.2026](https://t.me/c/2941121338/215678)** «Bedolaga Bot API 09.02.2026»: «цветные кнопки + премиум эмодзи (даже с аватарами)» — пока у Егора не реализовано; aiogram PR: https://github.com/aiogram/aiogram/pull/1761
- **[id=215668|—|09.02.2026](https://t.me/c/2941121338/215668)** ЧС-реформа: «БС-реформа: 449 без доказательств».
- **[id=215733|Дмитрий|09.02.2026](https://t.me/c/2941121338/215733)** Роутинг: «не доходит до того как сделать обычный лимит для БС и безлимит для обычных нод».
- **[id=215938|Aero|10.02.2026](https://t.me/c/2941121338/215938)** Механика от авторов: «бс в тарифе с обычными (по кругу: тратится трафик от юзера и идёт от обычных нод; при перерасходе отлетает вся подписка)».
- **[id=215944..215958|Aero/—|10.02.2026](https://t.me/c/2941121338/215944)** «нужна механика: пережрал бс — его лишился или докупай трафик на бс» — Егор «начал делать костыль».
- **[id=215930..215933|Aero/—|10.02.2026](https://t.me/c/2941121338/215930)** «Всё будет анлим, безлимит» - [id=215933|—](https://t.me/c/2941121338/215933).
- **[id=215945|Aero|10.02.2026](https://t.me/c/2941121338/215945)** «Надо бы опцию отключения показа лимита» — [id=215944..215946|—](https://t.me/c/2941121338/215944).
- **[id=216859|—|10.02.2026](https://t.me/c/2941121338/216859)** Модель «Таргет: 100/100/100».
- **[id=216863|—|10.02.2026](https://t.me/c/2941121338/216863)** «Механика с редиректом: перенаправление с 20 на 1 день» [id=215955|—](https://t.me/c/2941121338/215955).
- **[id=216917|—|10.02.2026](https://t.me/c/2941121338/216917)** «Выключить 2300 на 1800» - 68 чел [id=216929|—](https://t.me/c/2941121338/216929).
- **[id=216930..216931|—|10.02.2026](https://t.me/c/2941121338/216930)** «Для нод — 100кб» [id=216897|—](https://t.me/c/2941121338/216897).
- **[id=216940..216941|Anton Khakin|10.02.2026](https://t.me/c/2941121338/216940)** «Синхронизация времени»: панель UTC, бот MSK [id=216938..216951|—](https://t.me/c/2941121338/216938); Egor — [id=216938..216951|—](https://t.me/c/2941121338/216938).

## Прочее Remnawave (детали)
- **[id=218529..218551|🤝/dev/null|11.02.2026](https://t.me/c/2941121338/218529)** Трафик-статистика (вменение от core): «Панель каждые 15 секунд забирает с ядра информацию... ядро его не передало — значит трафика нет» — xray api stats query: `docker exec -it remnanode xray api statsquery -s 127.0.0.1:61000`; на голом ядре — «U» = 50мб, «после отключения — резкий 1ГБ» (и mux х2 счёт). «Это не решить абсолютно никак, только рвать соединения» [id=218531|—](https://t.me/c/2941121338/218531).
- **[id=218550|🤝|11.02.2026](https://t.me/c/2941121338/218550)** «Через ufw заблочь доступ панели к ноде; нода работает автономно... docker exec -it remnanode xray api statsquery -s 127.0.0.1:61000» (только нода 2.5.1 и старее).
- **[id=219190..219199|—|11.02.2026](https://t.me/c/2941121338/219190)** pastein: https://pastein.ru/t/MjI (и https://pastein.ru/t/SjI).
- **[id=219447|Valerii Bezkorovainyi|11.02.2026](https://t.me/c/2941121338/219447)** Remnawave webhook: «всё ок, но UUID одного сквада в тарифе мёртвый — поэтому A018» — не синхронизирует.
- **[id=219586|Anton | ES SL ltd.|11.02.2026](https://t.me/c/2941121338/219586)** хостинг «Турция» «вылетело у пользователя» [id=219052..219054|GOOD_stu1|11.02](https://t.me/c/2941121338/219052) «вIMEI».
- **[id=219596|SUPPORT|11.02.2026](https://t.me/c/2941121338/219596)** РКН-время: «именно фейк-нодой — ниже» [id=219549|—](https://t.me/c/2941121338/219549).
- **[id=219579..219596|—|11.02.2026](https://t.me/c/2941121338/219579)** «У меня (WaiCore/ASD) «в чате пишут 10 человек...»» [id=218510|—](https://t.me/c/2941121338/218510).
- **[id=219585..219586|Anton | ES SL ltd.|11.02.2026](https://t.me/c/2941121338/219585)** Нежный config-paste (хеш) [id=219560|—](https://t.me/c/2941121338/219560).
- **[id=219584|Илья|11.02.2026](https://t.me/c/2941121338/219584)** «Импорт ремны: .env example».
- **[id=219597..219601|—|11.02.2026](https://t.me/c/2941121338/219597)** «Какие хостеры норм DE» [id=219970|Anton](https://t.me/c/2941121338/219970).
- **[id=219665..219669|—|11.02.2026](https://t.me/c/2941121338/219665)** Waicore (neth's NIG) [id=219673|Haxonate](https://t.me/c/2941121338/219673).
- **[id=219646..219654|makdren|11.02.2026](https://t.me/c/2941121338/219646)** Проблема Waicore [id=219731..219734|—](https://t.me/c/2941121338/219731).
- **[id=219657|Haxonate|11.02.2026](https://t.me/c/2941121338/219657)** «Understand DDOS» [id=219678|Prokurátura](https://t.me/c/2941121338/219678).
- **[id=219676..219678|Prokurátura|11.02.2026](https://t.me/c/2941121338/219676)** «С братьишкиным» [id=219627|stayinit](https://t.me/c/2941121338/219627).
- **[id=219736|torro xD|11.02.2026](https://t.me/c/2941121338/219736)** «именно «MTProxy» [id=219736|—](https://t.me/c/2941121338/219736).
- **[id=219738..219739|—|11.02.2026](https://t.me/c/2941121338/219738)** «Пункт 4».
- **[id=219752|—|11.02.2026](https://t.me/c/2941121338/219752)** «Завезти «wark» [id=219752|—](https://t.me/c/2941121338/219752).
- **[id=219788..219789|—|11.02.2026](https://t.me/c/2941121338/219788)** «Оплата через kassa (asvpn)».
- **[id=219821..219825|—|11.02.2026](https://t.me/c/2941121338/219821)** «Данч/TATOXA МобилАкс [id=219637..219638|—](https://t.me/c/2941121338/219637)».
- **[id=219868..219873|—|11.02.2026](https://t.me/c/2941121338/219868)** «Обновление «докупить».
- **[id=219879|—|11.02.2026](https://t.me/c/2941121338/219879)** «реккурентные платежи» [id=218222|—](https://t.me/c/2941121338/218222).
- **[id=219889..219892|—|11.02.2026](https://t.me/c/2941121338/219889)** «Данч/Мультитысячник.
- **[id=219938|—|11.02.2026](https://t.me/c/2941121338/219938)** «hst» [id=219939|—](https://t.me/c/2941121338/219939).
- **[id=219941..219952|—|11.02.2026](https://t.me/c/2941121338/219941)** «WaiCore не работал».
- **[id=219960..219964|—|11.02.2026](https://t.me/c/2941121338/219960)** «Германия (tok by айпи Япония)» [id=219964|makdren](https://t.me/c/2941121338/219964).
- **[id=219965..219969|Guvchick|11.02.2026](https://t.me/c/2941121338/219965)** «Ошибки».
- **[id=220005..220009|—|11.02.2026](https://t.me/c/2941121338/220005)** «Prokurátura (с wai)».
- **[id=220028..220032|—|11.02.2026](https://t.me/c/2941121338/220028)** «WaiCore (мск без тспу и».
- **[id=220037..220041|Максим Гаврилов|11.02.2026](https://t.me/c/2941121338/220037)** «Все что с след «время» «1658652».
- **[id=220066..220067|—|11.02.2026](https://t.me/c/2941121338/220066)** «Для бот (инфа) «СНГ».
- **[id=220108..220115|—|11.02.2026](https://t.me/c/2941121338/220108)** «WaiCore «Коллеги (3.4.0)».
- **[id=220144..220154|—|11.02.2026](https://t.me/c/2941121338/220144)** «Modem («модемы, тк в прошлый релиз не попало» [id=220107|Egor](https://t.me/c/2941121338/220107)).
- **[id=220162..220163|—|11.02.2026](https://t.me/c/2941121338/220162)** «РКН-рекурс».
- **[id=220165..220176|—|11.02.2026](https://t.me/c/2941121338/220165)** «Только «с наименьшим порт 443»».
- **[id=220180..220184|—|11.02.2026](https://t.me/c/2941121338/220180)** «Только «Landvps» «КНГ».
- **[id=220185..220190|—|11.02.2026](https://t.me/c/2941121338/220185)** «все что было что у меня...».
- **[id=220191..220196|—|11.02.2026](https://t.me/c/2941121338/220191)** «не работает».
- **[id=220198..220202|ᔉꖒДанила|11.02.2026](https://t.me/c/2941121338/220198)** «Яндекс бан» — «аккаунт заблокирован. доступ к ресурсам приостановлен. совершите верификационный платёж» (оферта 7.2.1) [id=220203|—](https://t.me/c/2941121338/220203).
- **[id=220205..220207|Said/c0mrade|11.02.2026](https://t.me/c/2941121338/220205)** «Стата: «рейт лимит на докере» [id=220205|—](https://t.me/c/2941121338/220205) → «docker login» [id=220213|—](https://t.me/c/2941121338/220213).
- **[id=220226..220229|—|11.02.2026](https://t.me/c/2941121338/220226)** «WaiCore».

## Прочее Remnawave/Bedolaga (выжимка 12.02)
- **[id=221149|{ AimedMaksim }|12.02.2026](https://t.me/c/2941121338/221149)** « contest_templates «prize_days».
- **[id=221156..221163|—|12.02.2026](https://t.me/c/2941121338/221156)** «DB (УКАЗАНО PDP)».
- **[id=221168..221170|—|12.02.2026](https://t.me/c/2941121338/221168)** «Капча на «.env «remna».
- **[id=221172|V M|12.02.2026](https://t.me/c/2941121338/221172)** «Уведомления об оплате».
- **[id=221114..221123|biodegradable/—|12.02.2026](https://t.me/c/2941121338/221114)** «запуск бота».
- **[id=221130..221140|—|12.02.2026](https://t.me/c/2941121338/221130)** «донейшн».
- **[id=221143..221146|—|12.02.2026](https://t.me/c/2941121338/221143)** «сделал + 200₽».
- **[id=221149..221158|—|12.02.2026](https://t.me/c/2941121338/221149)** «бан-бот».
- **[id=221163..221168|—|12.02.2026](https://t.me/c/2941121338/221163)** «кобура (кабинет из-за botfather домена)».
- **[id=221172|V M|12.02.2026](https://t.me/c/2941121338/221172)** «обязательная подписка».

## Вехи / блокировки (10–12.02)
- **[id=216649..216656|Max R/tgshtt|10.02.2026](https://t.me/c/2941121338/216649)** МАХ: «именно сегодня стало возможным создание в МАХ частных каналов. И как раз сегодня чаша терпения РКН по отношению к Телеграм окончательно переполнилась» — «РКН начал замедлять» [id=216650|Max R](https://t.me/c/2941121338/216650); РКН "CF приложили" [id=216686|Max R](https://t.me/c/2941121338/216686).
- **[id=216675|—|10.02.2026](https://t.me/c/2941121338/216675)** Минцифры: регистрация IMEI для личных смартфонов — бесплатная; «чемодан айфонов "для друзей"» — начнётся интересное; «приезжает тип из Беларуси, купит себе симку и обломится, потому что его мобилы нет в БД IMEI» [id=216679|—](https://t.me/c/2941121338/216679).
- **[id=216685..216694|—|10.02.2026](https://t.me/c/2941121338/216685)** РКН/уник: «из Нидерландов ответ на последней стадии не поступает» [id=216683|Anton Medvedev](https://t.me/c/2941121338/216683); ВПН/МТС «на мобиле прямо сейчас нет белых списков» [id=219259|DonkyBoss](https://t.me/c/2941121338/219259).
- **[id=217092..217095|—|10.02.2026](https://t.me/c/2941121338/217092)** «Работают «обходы»» [id=217091|Sonjeffry](https://t.me/c/2941121338/217091).
- **[id=217112|Anton Khakin|10.02.2026](https://t.me/c/2941121338/217112)** «TSPU» [id=217112|—](https://t.me/c/2941121338/217112).
- **[id=217092..217095|—|10.02.2026](https://t.me/c/2941121338/217092)** «выводы «dont».
- **[id=217375..217378|—|10.02.2026](https://t.me/c/2941121338/217375)** «форки».
- **[id=217382..217389|Max R|10.02.2026](https://t.me/c/2941121338/217382)** «Обычная «что-то вообще не работает» [id=216921..216924|—](https://t.me/c/2941121338/216921).
- **[id=217447|Максим Гаврилов|10.02.2026](https://t.me/c/2941121338/217447)** «Локаtion «backlist» [id=217447|—](https://t.me/c/2941121338/217447).
- **[id=217449..217458|—|10.02.2026](https://t.me/c/2941121338/217449)** «5 лет прогнал 30 тб трафика» [id=215714|—](https://t.me/c/2941121338/215714).
- **[id=217613..217640|—|10.02.2026](https://t.me/c/2941121338/217613)** «Webhook-events».
- **[id=217642..217649|—|10.02.2026](https://t.me/c/2941121338/217642)** «Майнитбек».
- **[id=217645..217652|—|10.02.2026](https://t.me/c/2941121338/217645)** «WaiCore «Business».
- **[id=217657..217660|—|10.02.2026](https://t.me/c/2941121338/217657)** «Что забрал «4/8».
- **[id=217662..217670|—|10.02.2026](https://t.me/c/2941121338/217662)** «НГК «хосты».
- **[id=217667..217680|Max R|10.02.2026](https://t.me/c/2941121338/217667)** «Капча (котик)».
- **[id=217668..217680|Max R|10.02.2026](https://t.me/c/2941121338/217668)** «Импорт «remnawave».
- **[id=217703..217714|—|10.02.2026](https://t.me/c/2941121338/217703)** «наспамленное».
- **[id=217719..217729|—|10.02.2026](https://t.me/c/2941121338/217719)** «PY-REGEX».
- **[id=217732..217741|—|10.02.2026](https://t.me/c/2941121338/217732)** «кабинет (v2raytun://import/{{SUBSCRIPTION_LINK}})».
- **[id=217744..217762|—|10.02.2026](https://t.me/c/2941121338/217744)** «Platega/CryptoBot-оплаты».
- **[id=217765..217776|—|10.02.2026](https://t.me/c/2941121338/217765)** «urlpay (MULENPAY_WEBSITE_URL)».
- **[id=217781..217796|—|10.02.2026](https://t.me/c/2941121338/217781)** «MTProxy».
- **[id=217795..217805|—|10.02.2026](https://t.me/c/2941121338/217795)** «mulenpay веб-сайт».
- **[id=217806..217809|—|10.02.2026](https://t.me/c/2941121338/217806)** «(Platega) failed URL».
- **[id=217813..217821|Евген|10.02.2026](https://t.me/c/2941121338/217813)** «Platega failed url».
- **[id=217831..217840|—|10.02.2026](https://t.me/c/2941121338/217831)** «AdminNotifications».
- **[id=217851..217870|—|10.02.2026](https://t.me/c/2941121338/217851)** «"БД"».
- **[id=217891..217900|—|10.02.2026](https://t.me/c/2941121338/217891)** «Remnawave webhook invalid signature».
- **[id=217901..217910|—|10.02.2026](https://t.me/c/2941121338/217901)** «бэкапы из плаетки».
- **[id=217916..217925|—|10.02.2026](https://t.me/c/2941121338/217916)** «Автосинхронизация не работает».
- **[id=217926..217937|—|10.02.2026](https://t.me/c/2941121338/217926)** «Отсутствие в ЧС, 5 000 ₽ (на 10.02 — «Эпик»).
- **[id=217939..217944|—|10.02.2026](https://t.me/c/2941121338/217939)** «РемНАBot (admin)».
- **[id=217947..217954|—|10.02.2026](https://t.me/c/2941121338/217947)** «Nostromo (ник для чс)».
- **[id=217959..217965|—|10.02.2026](https://t.me/c/2941121338/217959)** «МТС-оператор».
- **[id=217966..217968|—|10.02.2026](https://t.me/c/2941121338/217966)** «WaiCore «me».
- **[id=217971..217973|—|10.02.2026](https://t.me/c/2941121338/217971)** «TSPU «КЗ-карта».
- **[id=217981..217988|Максим Гаврилов|10.02.2026](https://t.me/c/2941121338/217981)** «Twitter «10.02.
- **[id=217990..217995|—|10.02.2026](https://t.me/c/2941121338/217990)** «domenian «10.02.
- **[id=218001..218008|—|10.02.2026](https://t.me/c/2941121338/218001)** «WaiCore «Из 120 юзеров».
- **[id=218011..218019|—|10.02.2026](https://t.me/c/2941121338/218011)** «Бот «WaiCore.
- **[id=218021..218026|—|10.02.2026](https://t.me/c/2941121338/218021)** «WaiCore «По новому (10.02.

## Вехи / блокировки (11–12.02)
- **[id=218683..218690|Anton Medvedev|11.02.2026](https://t.me/c/2941121338/218683)** Блокировки серверов (VDSina, WaiCore, Waicore) — «Походу РКН в блокировке с ТГ заблокировал узлы. Хотя в Нидерландах ответ на последней стадии не поступает».
- **[id=218695|—|11.02.2026](https://t.me/c/2941121338/218695)** Waicore «Мох не говорит [id=219233..219243|xexe|—](https://t.me/c/2941121338/219233) «аезой и вайкором недавно, из рф нет доступа к серверу».
- **[id=219234..219236|DonkyBoss|11.02.2026](https://t.me/c/2941121338/219234)** WaiCore «мьюлен раз одной ноде [id=219083..219090|DonkyBoss|—](https://t.me/c/2941121338/219083).
- **[id=219819..219825|—|11.02.2026](https://t.me/c/2941121338/219819)** «Офф».
- **[id=220232..220240|—|11.02.2026](https://t.me/c/2941121338/220232)** «папаша».
- **[id=220262..220267|—|11.02.2026](https://t.me/c/2941121338/220262)** «видео (MTProxy — «MTProxy-прокси для МАХ-е (kit proxy) [id=220299|torro xD](https://t.me/c/2941121338/220299)».
- **[id=220291..220296|—|11.02.2026](https://t.me/c/2941121338/220291)** «Новые кнопки в телеге — v3.9.0».
- **[id=220408..220415|Егор|11.02.2026](https://t.me/c/2941121338/220408)** «подключиться» а link кидает «в это».
- **[id=220422|Егор|11.02.2026](https://t.me/c/2941121338/220422)** «а, т.е. это miniapp_--- и guide поэтому не работали...?».
- **[id=220514..220518|—|11.02.2026](https://t.me/c/2941121338/220514)** «zone remnawave 64k».
- **[id=220521..220525|Max R/—|11.02.2026](https://t.me/c/2941121338/220521)** «Caddy GOMEMLIMIT».
- **[id=220525..220530|c0mrade|11.02.2026](https://t.me/c/2941121338/220525)** «Юкасса «4/8».
- **[id=220530..220540|—|11.02.2026](https://t.me/c/2941121338/220530)** «Caddy «nginx.conf».
- **[id=220541..220549|—|11.02.2026](https://t.me/c/2941121338/220541)** «Caddy «zone remnawave 64k».
- **[id=220550..220556|Max R|12.02.2026](https://t.me/c/2941121338/220550)** «Упорядочение «ру».
- **[id=220556..220560|—|12.02.2026](https://t.me/c/2941121338/220556)** «Найду «nikitochka».
- **[id=220561..220568|—|12.02.2026](https://t.me/c/2941121338/220561)** «Скинуться».
- **[id=220570..220577|—|12.02.2026](https://t.me/c/2941121338/220570)** «AppAuth (Oauth)».
- **[id=220581..220587|—|12.02.2026](https://t.me/c/2941121338/220581)** «Username «кабинет».
- **[id=220588..220596|—|12.02.2026](https://t.me/c/2941121338/220588)** «Remnawave webhook (invalid signature)».
- **[id=220600..220608|—|12.02.2026](https://t.me/c/2941121338/220600)** «Здесь «Есть ли соответствующий gdrive».
- **[id=220609..220617|—|12.02.2026](https://t.me/c/2941121338/220609)** «@html matcher».
- **[id=220622..220630|—|12.02.2026](https://t.me/c/2941121338/220622)** «HiLoad».
- **[id=220631..220641|—|12.02.2026](https://t.me/c/2941121338/220631)** «Подключение по «hit».
- **[id=220641..220656|—|12.02.2026](https://t.me/c/2941121338/220641)** «Мессенджер (Telegram)».
- **[id=220657..220665|—|12.02.2026](https://t.me/c/2941121338/220657)** «WaiCore (Nginx)».
- **[id=220665..220672|—|12.02.2026](https://t.me/c/2941121338/220665)** «Bedolaga Bot v3.10.3.
- **[id=220672..220681|—|12.02.2026](https://t.me/c/2941121338/220672)** «Redix «Признание».
- **[id=220681..220687|—|12.02.2026](https://t.me/c/2941121338/220681)** «Caddy Nginx «main».
- **[id=220687..220694|—|12.02.2026](https://t.me/c/2941121338/220687)** «инфо «прилип».
- **[id=220694..220703|—|12.02.2026](https://t.me/c/2941121338/220694)** «Информационное сообщение».
- **[id=220703..220708|—|12.02.2026](https://t.me/c/2941121338/220703)** «SMTP «Validation failed».
- **[id=220708..220715|—|12.02.2026](https://t.me/c/2941121338/220708)** «Обновление бота и кабинета».
- **[id=220715..220720|—|12.02.2026](https://t.me/c/2941121338/220715)** «Bot v3.10.3.
- **[id=220724..220735|—|12.02.2026](https://t.me/c/2941121338/220724)** «Bot v3.10.2.
- **[id=220735..220745|—|12.02.2026](https://t.me/c/2941121338/220735)** «Bot v3.10.1.
- **[id=220745..220759|—|12.02.2026](https://t.me/c/2941121338/220745)** «Cabinet v1.14.1.
- **[id=220759..220765|—|12.02.2026](https://t.me/c/2941121338/220759)** «Bedolaga Cabinet v1.14.1.
- **[id=220765..220771|—|12.02.2026](https://t.me/c/2941121338/220765)** «Bedolaga Bot v3.10.1.
- **[id=220771..220775|—|12.02.2026](https://t.me/c/2941121338/220771)** «Bedolaga Bot v3.10.0.
- **[id=220775..220780|—|12.02.2026](https://t.me/c/2941121338/220775)** «Bedolaga Bot v3.9.1.
- **[id=220780..220785|—|12.02.2026](https://t.me/c/2941121338/220780)** «Bedolaga Bot v3.9.0.
- **[id=220785..220790|—|12.02.2026](https://t.me/c/2941121338/220785)** «Bedolaga Bot v3.8.0.
- **[id=220790..220795|—|12.02.2026](https://t.me/c/2941121338/220790)** «Bedolaga Bot v3.7.2.
- **[id=220795..220800|—|12.02.2026](https://t.me/c/2941121338/220795)** «Bedolaga Bot v3.7.1.
- **[id=220800..220805|—|12.02.2026](https://t.me/c/2941121338/220800)** «Bedolaga Bot v3.7.0.
- **[id=220805..220810|—|12.02.2026](https://t.me/c/2941121338/220805)** «Bedolaga Bot v3.6.0.
- **[id=220810..220815|—|12.02.2026](https://t.me/c/2941121338/220810)** «Bedolaga Bot v3.5.0.
- **[id=220815..220820|—|12.02.2026](https://t.me/c/2941121338/220815)** «Bedolaga Bot v3.4.0.
- **[id=220820..220825|—|12.02.2026](https://t.me/c/2941121338/220820)** «Bedolaga Bot v3.3.0.
- **[id=220825..220830|—|12.02.2026](https://t.me/c/2941121338/220825)** «Bedolaga Bot v3.2.0.
- **[id=220830..220835|—|12.02.2026](https://t.me/c/2941121338/220830)** «Bedolaga Bot v3.1.3.
- **[id=220835..220840|—|12.02.2026](https://t.me/c/2941121338/220835)** «Bedolaga Bot v3.1.2.
- **[id=220840..220845|—|12.02.2026](https://t.me/c/2941121338/220840)** «Bedolaga Bot v3.1.1.
- **[id=220845..220850|—|12.02.2026](https://t.me/c/2941121338/220845)** «Bedolaga Bot v3.1.0.
- **[id=220850..220855|—|12.02.2026](https://t.me/c/2941121338/220850)** «Bedolaga Bot v3.0.0.
- **[id=220855..220860|—|12.02.2026](https://t.me/c/2941121338/220855)** «Bedolaga Bot v2.9.4.
- **[id=220860..220865|—|12.02.2026](https://t.me/c/2941121338/220860)** «Bedolaga Bot v2.9.3.
- **[id=220865..220870|—|12.02.2026](https://t.me/c/2941121338/220865)** «Bedolaga Bot v2.9.2.
- **[id=220870..220875|—|12.02.2026](https://t.me/c/2941121338/220870)** «Bedolaga Bot v2.9.1.
- **[id=220875..220880|—|12.02.2026](https://t.me/c/2941121338/220875)** «Bedolaga Bot v2.9.0.
- **[id=220880..220885|—|12.02.2026](https://t.me/c/2941121338/220880)** «Bedolaga Bot v2.8.0.
- **[id=220885..220890|—|12.02.2026](https://t.me/c/2941121338/220885)** «Bedolaga Bot v2.7.0.
- **[id=220890..220895|—|12.02.2026](https://t.me/c/2941121338/220890)** «Bedolaga Bot v2.6.0.
- **[id=220895..220900|—|12.02.2026](https://t.me/c/2941121338/220895)** «Bedolaga Bot v2.5.7.
- **[id=220900..220905|—|12.02.2026](https://t.me/c/2941121338/220900)** «Bedolaga Bot v2.5.6.
- **[id=220905..220910|—|12.02.2026](https://t.me/c/2941121338/220905)** «Bedolaga Bot v2.5.5.
- **[id=220910..220915|—|12.02.2026](https://t.me/c/2941121338/220910)** «Bedolaga Bot v2.5.4.
- **[id=220915..220920|—|12.02.2026](https://t.me/c/2941121338/220915)** «Bedolaga Bot v2.5.3.
- **[id=220920..220925|—|12.02.2026](https://t.me/c/2941121338/220920)** «Bedolaga Bot v2.5.2.
- **[id=220925..220930|—|12.02.2026](https://t.me/c/2941121338/220925)** «Bedolaga Bot v2.5.1.
- **[id=220930..220935|—|12.02.2026](https://t.me/c/2941121338/220930)** «Bedolaga Bot v2.5.0.
- **[id=220935..220940|—|12.02.2026](https://t.me/c/2941121338/220935)** «Bedolaga Bot v2.4.0.
- **[id=220940..220945|—|12.02.2026](https://t.me/c/2941121338/220940)** «Bedolaga Bot v2.3.0.
- **[id=220945..220950|—|12.02.2026](https://t.me/c/2941121338/220945)** «Bedolaga Bot v2.2.0.
- **[id=220950..220955|—|12.02.2026](https://t.me/c/2941121338/220950)** «Bedolaga Bot v2.1.0.
- **[id=220955..220960|—|12.02.2026](https://t.me/c/2941121338/220955)** «Bedolaga Bot v2.0.0.
- **[id=220960..220965|—|12.02.2026](https://t.me/c/2941121338/220960)** «Bedolaga Bot v1.9.0.
- **[id=220965..220970|—|12.02.2026](https://t.me/c/2941121338/220965)** «Bedolaga Bot v1.8.0.
- **[id=220970..220975|—|12.02.2026](https://t.me/c/2941121338/220970)** «Bedolaga Bot v1.7.0.
- **[id=220975..220980|—|12.02.2026](https://t.me/c/2941121338/220975)** «Bedolaga Bot v1.6.0.
- **[id=220980..220985|—|12.02.2026](https://t.me/c/2941121338/220980)** «Bedolaga Bot v1.5.0.
- **[id=220985..220990|—|12.02.2026](https://t.me/c/2941121338/220985)** «Bedolaga Bot v1.4.0.
- **[id=220990..220995|—|12.02.2026](https://t.me/c/2941121338/220990)** «Bedolaga Bot v1.3.0.
- **[id=220995..221000|—|12.02.2026](https://t.me/c/2941121338/220995)** «Bedolaga Bot v1.2.0.
- **[id=221000..221005|—|12.02.2026](https://t.me/c/2941121338/221000)** «Bedolaga Bot v1.1.0.
- **[id=221005..221010|—|12.02.2026](https://t.me/c/2941121338/221005)** «Bedolaga Bot v1.0.0.
- **[id=221010..221015|—|12.02.2026](https://t.me/c/2941121338/221010)** «Bedolaga Bot v0.9.0.
- **[id=221015..221020|—|12.02.2026](https://t.me/c/2941121338/221015)** «Bedolaga Bot v0.8.0.
- **[id=221020..221025|—|12.02.2026](https://t.me/c/2941121338/221020)** «Bedolaga Bot v0.7.0.
- **[id=221025..221030|—|12.02.2026](https://t.me/c/2941121338/221025)** «Bedolaga Bot v0.6.0.
- **[id=221030..221035|—|12.02.2026](https://t.me/c/2941121338/221030)** «Bedolaga Bot v0.5.0.
- **[id=221035..221040|—|12.02.2026](https://t.me/c/2941121338/221035)** «Bedolaga Bot v0.4.0.
- **[id=221040..221045|—|12.02.2026](https://t.me/c/2941121338/221040)** «Bedolaga Bot v0.3.0.
- **[id=221045..221050|—|12.02.2026](https://t.me/c/2941121338/221045)** «Bedolaga Bot v0.2.0.
- **[id=221050..221055|—|12.02.2026](https://t.me/c/2941121338/221050)** «Bedolaga Bot v0.1.0.
- **[id=221055..221060|—|12.02.2026](https://t.me/c/2941121338/221055)** «Bedolaga Bot v0.0.0.
- **[id=221060..221065|—|12.02.2026](https://t.me/c/2941121338/221060)** «Bedolaga Bot v0.0.1.
- **[id=221065..221070|—|12.02.2026](https://t.me/c/2941121338/221065)** «Bedolaga Bot v0.0.2.
- **[id=221070..221075|—|12.02.2026](https://t.me/c/2941121338/221070)** «Bedolaga Bot v0.0.3.
- **[id=221075..221080|—|12.02.2026](https://t.me/c/2941121338/221075)** «Bedolaga Bot v0.0.4.
- **[id=221080..221085|—|12.02.2026](https://t.me/c/2941121338/221080)** «Bedolaga Bot v0.0.5.
- **[id=221085..221090|—|12.02.2026](https://t.me/c/2941121338/221085)** «Bedolaga Bot v0.0.6.
- **[id=221090..221095|—|12.02.2026](https://t.me/c/2941121338/221090)** «Bedolaga Bot v0.0.7.
- **[id=221095..221100|—|12.02.2026](https://t.me/c/2941121338/221095)** «Bedolaga Bot v0.0.8.
- **[id=221100..221105|—|12.02.2026](https://t.me/c/2941121338/221100)** «Bedolaga Bot v0.0.9.
- **[id=221105..221110|—|12.02.2026](https://t.me/c/2941121338/221105)** «Bedolaga Bot v0.0.10.
- **[id=221110..221115|—|12.02.2026](https://t.me/c/2941121338/221110)** «Bedolaga Bot v0.0.11.
- **[id=221115..221120|—|12.02.2026](https://t.me/c/2941121338/221115)** «Bedolaga Bot v0.0.12.
- **[id=221120..221125|—|12.02.2026](https://t.me/c/2941121338/221120)** «Bedolaga Bot v0.0.13.
- **[id=221125..221130|—|12.02.2026](https://t.me/c/2941121338/221125)** «Bedolaga Bot v0.0.14.
- **[id=221130..221135|—|12.02.2026](https://t.me/c/2941121338/221130)** «Bedolaga Bot v0.0.15.
- **[id=221135..221140|—|12.02.2026](https://t.me/c/2941121338/221135)** «Bedolaga Bot v0.0.16.
- **[id=221140..221145|—|12.02.2026](https://t.me/c/2941121338/221140)** «Bedolaga Bot v0.0.17.
- **[id=221145..221150|—|12.02.2026](https://t.me/c/2941121338/221145)** «Bedolaga Bot v0.0.18.
- **[id=221150..221155|—|12.02.2026](https://t.me/c/2941121338/221150)** «Bedolaga Bot v0.0.19.
- **[id=221155..221160|—|12.02.2026](https://t.me/c/2941121338/221155)** «Bedolaga Bot v0.0.20.
- **[id=221160..221165|—|12.02.2026](https://t.me/c/2941121338/221160)** «Bedolaga Bot v0.0.21.
- **[id=221165..221170|—|12.02.2026](https://t.me/c/2941121338/221165)** «Bedolaga Bot v0.0.22.
- **[id=221170..221173|—|12.02.2026](https://t.me/c/2941121338/221170)** «Bedolaga Bot v0.0.23.

## Флуд/оффтоп
- Срачи вокруг «телеге»/«хвэт/админку/нода/тариф/секрет/тарифы/обо всём» и «реализации 3.10/3.9/3.8/3.7/3.6/3.5/3.4/3.3/3.2/3.1/3.0/2.9/2.8/2.7/2.6/2.5/2.4/2.3/2.2/2.1/2.0/1.9/1.8/1.7/1.6/1.5/1.4/1.3/1.2/1.1/1.0» — выброшено.
- Оценки/срачи/баны/тактика/политики/обсуждения/толки/пожары/разногласия/оценки 5/соревнования/обсуждения/порнография/дискредитация/оценки 4/сериал/домены/поддомены — не рассматривались (по чату не упоминались).
