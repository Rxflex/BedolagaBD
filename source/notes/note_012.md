# Заметки из chunk_012 (id 57659..62966, 08.11.2025–12.11.2025)

## Переход Bedolaga на единые вебхуки (v2.6.x)
- **[id=57781–57782|art vs,17|08.11]** Релизнули единую систему вебхуков; бот теперь слушает ОДИН порт 8080 (webhooks + Web API + miniapp API), платежки ходят по разным путям.
- **[id=58548|Egor|08.11]** Минимальный .env для старта бота (дословно):
  ```
  BOT_TOKEN=
  ADMIN_IDS=
  BOT_RUN_MODE=webhook
  WEBHOOK_URL=https://hooks.domain.com
  WEBHOOK_SECRET_TOKEN=super-secret-token
  WEB_API_ENABLED=true
  WEB_API_ALLOWED_ORIGINS=https://miniapp.example.com
  ```
  Остальное можно держать в БД бота (настройки в админке бота), .env имеет приоритет над БД.
- **[id=57754|art vs|08.11]** Удаляешь переменную из .env → значение берется из БД (env приоритет).
- **[id=59245|Илья Захаров|09.11]** Env-конфиг Platega (дословно):
  ```
  PLATEGA_ENABLED=true
  PLATEGA_MERCHANT_ID=your_merchant_id
  PLATEGA_SECRET=your_secret_key
  PLATEGA_RETURN_URL=https://your-domain.com/payments/success
  PLATEGA_FAILED_URL=https://your-domain.com/payments/failed
  PLATEGA_ACTIVE_METHODS=2,10,11
  PLATEGA_MIN_AMOUNT_KOPEKS=10000
  PLATEGA_MAX_AMOUNT_KOPEKS=5000000
  PLATEGA_CURRENCY=RUB
  PLATEGA_WEBHOOK_PATH=/platega-webhook
  ```
  Плюс вебхук https://your-domain.com/platega-webhook в ЛК Platega; PLATEGA_BASE_URL/WEBHOOK_HOST/WEBHOOK_PORT оставить по умолчанию. **[id=60672|❤️‍🔥|11.11]** Опыт: на старте 9% комиссии (понижают с оборотом; другим дали 11%/10% карта/СБП — [id=60821]), СБП сразу, карты через ~неделю, вывод только в крипту (3$ TRC), вывод по выходным не идет, регистрация по почте, чеков в налоговую нет.
- **[id=58756|—|09.11]** Миф: для единого хука все платежки ведут на /webhook — НЕВЕРНО. Бот слушает один порт/домен, но у каждой платежки свой путь: /tribute-webhook, /yookassa-webhook, /cryptobot-webhook, /mulenpay-webhook и т.д. (env: TRIBUTE_WEBHOOK_PATH, YOOKASSA_WEBHOOK_PATH, CRYPTOBOT_WEBHOOK_PATH...). Ошибка 401 «Telegram webhook с неверным секретом» возникала из-за запросов платежек на телеграм-эндпоинт.
- **[id=58756|Дмитрий|09.11]** Фикс 401 неверного секрета: сгенерировать `openssl rand -hex 32` → WEBHOOK_SECRET_TOKEN; снести старый вебхук `https://api.telegram.org/bot<TOKEN>/deleteWebhook`; перезапустить бота `make reload` — бот перерегистрирует вебхук с новым секретом.
- **[id=58789|—|09.11]** Старые location-блоки nginx (до единого хука) — порт один, адреса разные, каждый proxy_pass на 127.0.0.1:8081:
  ```nginx
  location /tribute-webhook {
      proxy_pass http://127.0.0.1:8081;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_read_timeout 30s;
      proxy_send_timeout 30s;
      client_max_body_size 1M;
  }
  location /urlpay-webhook { ... то же ... }
  ```
- **[id=59948|Дмитрий|10.11]** Полный гайд переезда на вебхуки (Решала): в .env удалить порты 8081–8086 (TRIBUTE/YOOKASSA/CRYPTOBOT/PAL24/WATA/HELEKET_WEBHOOK_PORT), добавить:
  ```
  BOT_RUN_MODE=webhook
  WEBHOOK_URL=https://hooks.your-domain.com
  WEBHOOK_PATH=/webhook
  WEBHOOK_SECRET_TOKEN=<openssl rand -hex 32>
  WEB_API_ENABLED=true
  WEB_API_HOST=0.0.0.0
  WEB_API_PORT=8080
  WEB_API_ALLOWED_ORIGINS=https://subapp.your-domain.com,https://miniapp.your-domain.com
  WEB_API_DEFAULT_TOKEN=<секрет>
  ```
  docker-compose: оставить один порт `- "127.0.0.1:8080:8080"`; healthcheck два варианта:
  ```
  curl -f http://localhost:8080/health/unified || exit 1
  curl -f -H 'X-API-Key: ТВОЙ_WEB_API_DEFAULT_TOKEN' http://localhost:8080/health || exit 1
  ```
  nginx: убрать старые upstream, один `upstream remnawave_bot_unified { server 127.0.0.1:8080; }`, `location / { proxy_pass http://remnawave_bot_unified; }` — nginx путь не меняет, а платежкам в ЛК указывать полные пути с разными хвостами.
- **[id=59964,59971,59980|—,c0mrade,Дмитрий|10.11]** Типовая ошибка юкассы: proxy_pass на /api/yookassa/webhook → 404. Правильно: `location /yookassa-webhook { proxy_pass http://remnawave_bot:8080/yookassa-webhook; }` либо в ЛК юкассы URL без /api; после правки .env обязательно пересоздать контейнер.
- **[id=58063|—|08.11]** Рабочий Caddyfile (хуки api.domain.com + статика miniapp):
  ```
  api.domain.com {
      encode gzip zstd
      @config path /app-config.json
      header @config Access-Control-Allow-Origin "*"
      reverse_proxy localhost:8080 {
          header_up Host {host}
          header_up X-Real-IP {remote_host}
          transport http { read_buffer 0 }
      }
  }
  podpiska.domain.com {
      encode gzip zstd
      handle /miniapp/* { reverse_proxy localhost:8080 { ... read_buffer 0 } }
      handle /app-config.json { header Access-Control-Allow-Origin "*"; reverse_proxy localhost:8080 { ... } }
      handle { root * /var/www/remnawave-miniapp; try_files {path} /index.html; file_server }
  }
  ```
- **[id=59167|eval(rm -rf /*)|09.11]** Этот блок app-config.json с reverse_proxy ЛОМАЕТ импорт app-config на новых вебхуках (лучше отдавать файл напрямую, как в 58063/59008).
- **[id=59008|hdhdh4226ru|09.11]** Пример Caddy на репе: pay.домен → `reverse_proxy remnawave_bot:8080`; miniapp.домен: /health* в бота, /app-config.json отдавать file_server с CORS, статика root /XDXAVpnBot/miniapp.
- **[id=57997|eval(rm -rf /*)|08.11]** В docker-compose healthcheck поменять `/health` на `/health/unified` — уходит 401 на /health.
- **[id=61254,61302|IS,—|11.11]** app-config не грузится в боте после перехода — закомментировать проблемный блок (старый handle с CORS) — работает.
- **[id=60944|—|11.11]** Проверка: `curl -s https://bot.example.com/health/unified | jq`. Для полноценной работы нужны 2 поддомена (hooks/bot + miniapp) — [id=60947|Egor], пример Caddy из README репо.
- **[id=60853,60859,60861|—,Egor|11.11]** Старый прокси на 8080 от апишки продолжает работать; дефолт теперь 8080, можно оставить 8082 в env. Лишние порты в docker можно снести. Минимальный запуск: ~8 параметров env, остальное в БД ([id=60864|Egor]).
- **[id=61047,61192|Egor,—|11.11]** Платежки после обновы «не полетели» — просто нужно поправить свой прокси; из env убрать лишнее, все в реадми.

## Бот: баги и фиксы v2.6.1–2.6.2
- **[id=59851|Egor|10.11]** Релиз #v2_6_2: БД ускорение до 300% (connection pooling до 50, read-реплики, /health с метриками); YooKassa — корректная обработка IP через Cloudflare, надежные вебхуки за CDN; Pal24 — фикс ссылок СБП и коллбэков; Platega — лимиты пополнения; CryptoBot — округление сумм до целых рублей; переработан pipeline бэкапов (PostgreSQL без pg_dump); предзаполнение суммы при активации платного триала. Обновление: `git pull origin main && make reload`.
- **[id=59587|Valerii Bezkorovainyi|09.11]** Чистая установка падала: PostgreSQL не выполняет несколько SQL-команд в одном запросе миграций (CREATE TABLE ...; CREATE INDEX...; в одном exec) — все таблицы не создаются. **[id=59765|Egor|10.11]** Фикс миграции на чистых БД выпущен (PR 1853 на бою — [id=59778]).
- **[id=59669|{ AimedMaksim }|09.11]** После обновления PermissionError: /app/data/backups — бот работает под UID:GID 1000:1000. Фикс прав:
  ```bash
  git clone https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot.git
  cd remnawave-bedolaga-telegram-bot
  mkdir -p ./logs ./data ./data/backups ./data/referral_qr
  chmod -R 755 ./logs ./data
  sudo chown -R 1000:1000 ./logs ./data
  ```
  ([id=59101|art vs]; повторено в [id=62725|c0mrade] для бэкапов 2.6.2).
- **[id=59132|ViToS|09.11]** Фикс Pal24 вебхука: добавить `python-multipart==0.0.9` в requirements.txt и в pal24.py заменить postback на callback:
  ```bash
  sed -i 's/postback_payload=postback/callback_payload=postback/g' app/services/payment/pal24.py
  ```
- **[id=58125,58126|R0xTaDDy,c0mrade|08.11]** CryptoBot: `greenlet_spawn has not been called` (SQLAlchemy async) при отправке уведомления о пополнении — баг бота (авточек спасал).
- **[id=58155–58156|—|08.11]** Дыра безопасности миниапки: эндпоинт `/api/getSubscriptionInfo?telegramId=` отдает подписку любому по telegramId без проверки initdata.
- **[id=61526|art vs|11.11]** Удаление юзера падает: ForeignKeyViolationError platega_payments_user_id_fkey (platega_payments держит ссылку).
- **[id=59167,59168,61522|Дмитрий|09.11/11.11]** Спам «автоплатеж» у юзеров отключается правкой в БД (снять галочки в таблице юзеров) — костыль до фикса; DEFAULT_AUTOPAY_ENABLED=false в env не влияет на уже зарегистрированных.
- **[id=58218–58220|c0mrade|08.11]** aiogram RuntimeError в manage_squad_action (method not mounted to bot instance) + TelegramBadRequest message is not modified — баг при добавлении юзера в сквад.
- **[id=59127|KeepСalm|09.11]** Рассылка с медиа + кнопка подключиться: `edit_text` вместо `edit_caption` → Bad Request: there is no text in the message to edit.
- **[id=59743|art vs|11.11]** Bad Request: can't parse entities: Unsupported start tag "1с)" — кривой тег в тексте автосинхронизации; фикс-патч `_format_duration` (менее 1с / X мин / X мин Y с) выложен [id=61263|SUPPORT|11.11].
- **[id=60203–60206|Alexey Zyryanov|10.11]** Реферальный диплинк: в режиме меню «текст» (не full) диплинк отсутствует, в миниапке копируется только хвост без домена; вручную собранный диплинк работает.
- **[id=61023,61028,61661|IS,—|11.11]** Оплата через миниапп: `POST /miniapp/payments/status 422 Unprocessable Content` — проверка платежа не проходит (urlpay), в боте при этом уведомление об успехе приходит.
- **[id=60648–60670|Фантомас|10–11.11]** Через Web API `POST /users` + `POST /subscriptions` юзер не создается в RemnaWave → нет ссылки. Фантомас сделал PR (создание пользователя в remnawave вместе с подпиской в боте).
- **[id=59651–59652|DonaldBTC,—|09.11]** Проблема создания миграций alembic: не создается таблица discount (цепочка версий битая) — шел в общий фикс.
- **[id=57754,57757|art vs|08.11]** Ошибка запуска бота (pydantic): убрать из env Admin report topic и muled shop id, если не используешь — неиспользуемые переменные удалять/комментировать.
- **[id=58651–58653,58671–58676|—,Egor|09.11]** ЮКасса: вебхуки временно отключены — YooKassa не умеет слать вебхуки с секретом, любой зная домен может curl-ом накидывать баланс; временное решение — включить автоподтверждение платежей (авточек); планируется фикc, где бот сам стучит в кассу и проверяет платежи.
- **[id=59750,59754|Deleted Account,—|10.11]** Криптоссылки: на ПК не работают; в миниапп редирект на https://sawgod.github.io/redirect-page/?theme=aurora&redirect_to= — на мобилках ок, на Windows криво ([id=60456]).
- **[id=62946|Дмитрий|12.11]** Предложения (issues/1892): кнопки серверов в один столбец, бесплатные опции выбирать по умолчанию, показывать описание сквадов под названием.

## Триальный сквад / сервера в боте
- **[id=59142–59145|R0xTaDDy,Дмитрий|09.11]** В 2.6.1 uuid триального сквада больше не в env: указывается в списке серверов бота; несколько сквадов → рандомная выдача.
- **[id=60414,60418|Aleksey Vist|10.11]** Если триал не выдает сквад: в настройках сервера появился пункт «выдавать сквад для триала» (раньше был env-параметр) — надо включить вручную.
- **[id=60964,60998|-|11.11]** Подтверждено: после обновы триальный сквад не подтягивается из env — нужно вручную сделать сквад доступным для триала.
- **[id=60153,60156|Egor|10.11]** Ошибка `API Error 404: Users not found` при выдаче триала = не настроена выдача сквада на сервере: Сервера → список серверов → открыть сервер → «выдача сквада».
- **[id=61052–61057|Egor,—|11.11]** SIMPLE_SUBSCRIPTION_SQUAD_UUID — только для кнопки «простая покупка»; дефолтный сквад для подписок назначается через пункт «сервера» в боте. Для триала: выбрать сквады → внутри проставить «выдавать сквад» (1 или много, рандом). Для продажи — активировать сквад.
- **[id=60776|q|11.11]** Env простой покупки (дословно):
  ```
  SIMPLE_SUBSCRIPTION_ENABLED=false
  SIMPLE_SUBSCRIPTION_PERIOD_DAYS=30
  SIMPLE_SUBSCRIPTION_DEVICE_LIMIT=1
  SIMPLE_SUBSCRIPTION_TRAFFIC_GB=0
  # SIMPLE_SUBSCRIPTION_SQUAD_UUID=
  ```
- **[id=61750,61754|Zavulon,Egor|12.11]** TRIAL_SQUAD_UUID переехал: прямо в «сервера» (бот).
- **[id=60436,60402|Егор,—|09.11]** Если у 2 нод 1 профиль vless — бот покажет 1 сервер; разделить ноды по разным профилям/сквадам (тег поменять, т.к. дубликаты запрещены: `"tag": "VLESS_TCP_REALITY2"`).
- **[id=59048|Фантомас|09.11]** Всем юзерам все ноды: внутренний сквад в панели со всеми серверами → в боте назначить дефолтный сквад для подписок.
- **[id=62685|Михаил|12.11]** В index.html миниапп в body добавить `margin-bottom: 65px;` — иначе кнопка «подключиться» перекрывает раздел устройств.
- **[id=62828|Михаил|12.11]** Кастомные подписки legiz: в скрипте eGames, руками — /opt/remnawave файлы app-config.json и index.html (кастом сначала установить).

## Docker/сети/установка
- **[id=57711,57732|c0mrade|08.11]** Бот и панель на одном сервере → всё в одну docker-сеть, обращение локально через docker network; следить за непересекающимися портами. `REMNAWAVE_API_URL` — это URL панели (через него же API-запросы).
- **[id=60210–60211|c0mrade,—|10.11]** Бот рядом с панелью → положить в сеть ремны, сеть бота удалить.
- **[id=58536|Egor|08.11]** Чистая установка:
  ```bash
  cd ~
  rm -rf XDXAVpnBot
  git clone https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot XDXAVpnBot
  cd XDXAVpnBot
  make up
  ```
- **[id=60297–60304|c0mrade,—|10.11]** `make: docker: No such file or directory` — в актуальном docker compose v2 пишется `docker compose`, а не docker-compose; make должен быть установлен (в Ubuntu предлагается apt install make).
- **[id=57754,61269–61274|art vs,IS|08.11/11.11]** env имеет приоритет над настройками бота: менять через админку можно только если параметр не задан в .env.
- **[id=61003|—|11.11]** `network remnawave_bot_network declared as external, but could not be found` — создать сеть/подключить бот к сети панели.
- **[id=62933|Ilya Mukhachev|12.11]** Обновление 2.5.7→2.6.2: резервная копия, затем git pull / make reload ([id=61775] команда make: up/up-follow/down/reload/reload-follow/test).
- **[id=62704,62700|c0mrade|12.11]** На вебхуках домен для платежки = один хук-домен + путь из настроек: `https://example.com/pay-webhook`.

## Идеальный нод / sysctl
- **[id=60218|c0mrade|10.11]** sysctl для нод ремны (вариант 1, дословно частично): disable IPv6, ip_forward=0, rp_filter=1, tcp_syncookies=1, fin_timeout=20, tcp_max_tw_buckets=262144, tcp_fastopen=3, tw_reuse=1, tcp_max_syn_backlog=8192, tcp_rmem/wmem 4096 87380/65536 16777216, somaxconn=4096, netdev_max_backlog=5000, default_qdisc=fq, congestion_control=bbr, fs.file-max=2097152, vm.swappiness=0. (sudo nano /etc/sysctl.conf → sudo sysctl -p)
- **[id=60229|Zavulon|10.11]** Исправленный вариант для VPN-ноды (дословно ключевые отличия):
  ```
  # IPv6: либо полностью отключить (disable_ipv6=1), либо вариант B: forwarding=1, accept_ra=0, autoconf=0, redirects=0
  net.ipv4.ip_forward = 1            # на маршрутизаторе нужна переадресация
  net.ipv4.conf.all.rp_filter = 2    # loose: многосетевость/Docker/VPN, strict режет легитимный трафик
  net.ipv4.tcp_fastopen = 1          # только клиент; серверная TFO конфликтует через NAT/прокси
  # tcp_max_tw_buckets, tcp_fack, tcp_tw_reuse — удалить (не фикс TIME_WAIT, устарело)
  net.ipv4.tcp_ecn = 1
  net.ipv4.tcp_sack = 1
  net.ipv4.tcp_keepalive_time = 600 / intvl=60 / probes=5
  net.ipv4.tcp_rmem = 4096 87380 16777216
  net.ipv4.tcp_wmem = 4096 65536 16777216
  net.core.somaxconn = 4096
  net.core.netdev_max_backlog = 5000
  net.core.rmem_max = 16777216
  net.core.wmem_max = 16777216
  net.core.default_qdisc = fq
  net.ipv4.tcp_congestion_control = bbr
  kernel.yama.ptrace_scope = 1
  kernel.randomize_va_space = 2
  fs.suid_dumpable = 0
  vm.swappiness = 10
  fs.file-max = 2097152
  ```
- **[id=61467,61214,61216|—|11.11]** Практика: IPv6 на нодах отключать («рудимент»), оплачивать только IPv4.
- **[id=60194,60811,60815,60827|Илья,Vladimir,Евген,mikhail|10–11.11]** Вместимость ноды: в среднем 40–60 человек комфортно; 1 ядро/1 ГБ RAM хватает на ~30 пользователей (WA/TG звонки); важнее сеть и проценты vCPU.
- **[id=59082|Егор|09.11]** Роутинг (разделение трафика) доки: https://docs.rw/docs/learn/server-routing.

## Ютуб без рекламы на ру-ноде (youtubeUnblock)
- **[id=59776|—|10.11]** Дословный сетап:
  ```bash
  cd /opt
  git clone https://github.com/Waujito/youtubeUnblock.git
  cd /opt/youtubeUnblock
  sudo apt install autoconf automake autotools-dev
  sudo apt install libtool pkg-config
  sudo modprobe nfnetlink_queue
  sudo iptables -t mangle -N YOUTUBEUNBLOCK
  sudo iptables -t mangle -A YOUTUBEUNBLOCK -p tcp --dport 443 -m connbytes --connbytes-dir original --connbytes-mode packets --connbytes 0:19 -j NFQUEUE --queue-num 537 --queue-bypass
  sudo iptables -t mangle -A YOUTUBEUNBLOCK -p udp -m connbytes --connbytes-dir original --connbytes-mode packets --connbytes 0:8 -j NFQUEUE --queue-num 537 --queue-bypass
  sudo iptables -t mangle -A POSTROUTING -j YOUTUBEUNBLOCK
  sudo iptables -I OUTPUT -m mark --mark 32768/32768 -j ACCEPT
  make
  # youtubeUnblock.service в /usr/lib/systemd/system, ExecStart=/opt/youtubeUnblock/build/youtubeUnblock
  sudo systemctl start youtubeUnblock
  ```
  Работает на ру-ноде без роутинга и рекламы; шортсы работают херово, обычные видео ок ([id=59768,59893]).
- **[id=59783,59791|Egor,—|10.11]** Альтернатива — двойной туннель по SS: профиль на сервер, ss ключ, routing-блок под ключ ss на нужном сервере, по доке ремны; работает норм ([id=59807] — настраивал месяц назад, все fine). Отвал ру-ноды → отвал роутинга ([id=59802]).
- **[id=62026–62027|Евген,Фантомас|11.11]** Билайн/Т2: у автора есть конфиг, где обход вайтлистов работает на обоих (в лс, без деталей).

## Клиенты / Happ
- **[id=60217|Дмитрий|10.11]** Ссылки Happ: iOS https://apps.apple.com/us/app/happ-proxy-utility/id6504287215, iOS Plus https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973, Android https://play.google.com/store/apps/details?id=com.happproxy, APK https://github.com/Happ-proxy/happ-android/releases/latest/download/Happ.apk, Windows https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x86.exe.
- **[id=59476,59482–59488|Фантомас,Евген|09.11]** Happ реверс-инжинирили: парень вытащил приватный ключ для расшифровки зашифрованных подписок с GPT за 40 минут (лето 2025); ключ нигде не выложен. Happ — топ клиент до появления конкурентов; opencourse кроссплатформенный альтернативный клиент — hiddify ([id=59527]).
- **[id=59417–59446,60435|Евген,Pedzeo,c0mrade|09.11]** Разработка собственных клиентов (iOS Swift/Android Kotlin нативно; кроссплатформа на Flutter возможна но «лажа»); Pedzeo делал связку с ядром VPN в App Store — под заказ ~300к минималка.
- **[id=60170,60173|—,R0xTaDDy|10.11]** Сколько юзеров выдержит нода — в доке ремны только минимальные требования; зависит от сервера/канала/поведения юзеров.

## События / блокировки
- **[id=58222|Серёжа|08.11]** Постановление: РКН+ФБС+Минцифры получили полномочия изолировать Рунет, редирект трафика и произвольные блокировки; вступает в силу с 01.03.2026 (мнения в чате: де-факто это уже было, «ничего не изменится»).
- **[id=62521|SUPPORT|12.11]** В некоторых регионах РФ отключают интернет до окончания СВО (слухи/ящик).
- **[id=59224,60230|Илья Захаров|09–10.11]** Обход белых списков: где взять сервер под SNI — вопрос; vk cloud мб с подсетью повезет ([id=59230|R0xTaDDy]).
- **[id=62948–62963|—,Илья Захаров|12.11]** РУ-адреса 82.208.* — без ТСПУ (гигабит, разгон до 25 Гбит, инста/ютуб работают без впн); встречаются у Сбера и ВК клаудов.
- **[id=62692–62694|Илья Захаров,Женя,Глеб|12.11]** vk cloud: серверы работают, но IP в белых списках почти нет (0 из 7 с глушением), минимальный сервер ~1к/мес. ufo.hosting = the.hosting = pq.hosting ([id=62694|Глеб]).
- **[id=59126|Рамиль|09.11]** Некий хостер (у которого хотел NL/DE + домены) — НЕ советую: серверы не создаются, ТП на отвали, аптайм говно, падения; зависает при покупке домена.
- **[id=61648–61650|Egor|11.11]** Хосты автора бота: waicore, dhost, h2.nexus + промка bill за 150р. **[id=62665,62667,62669|—,Женя|12.11]** vdsina: комиссия за пополнение 42% (из-за неё уходили), навязчивые рассылки; у одного NL без проблем, у другого негатив.
- **[id=58021|Deleted Account|08.11]** Bero-host: Германия only, KVM prepaid 2.4€/мес (1/4 тариф, др.), 5 Гбит/с, отличный аптайм.
- **[id=61487,61495|Edward Forix,—|11.11]** UFO.Hosting акция 11.11: VPS на год —50% (промокод UFOSALE), SSL −70%, FTP −20%; «постоянные просадки и грязные IP» по мнению других.
- **[id=62869,62879|Глеб|12.11]** Waicore: Германия — 1-2 недели (раскупили быстро), финка — к концу месяца новости, РФ-локация в планах но сложно.
- **[id=59665,59663|Евгений,R0xTaDDy|09.11]** AdminVPS: бот каждые 2 минуты ловит «API недоступно/доступно» — проблемы с сетью хостера.
- **[id=60779,60780|DonaldBTC,R0xTaDDy|11.11]** Панель+нода+бот от eGames на одном сервере: конфликт порта 443, API постоянно отваливается → панель и ноду на разные сервера.
- **[id=59348,60647|Egor,Евгений|09.11/10.11]** Авторизация в панели: вход через Telegram глючит постоянно — лучше Яндекс или GitHub.
- **[id=59338,59431|c0mrade,Edward Forix|09.11]** Может лиВАICanva считать РФ: гео по IP; проверить свои IP по геобазам, мб ipv6 в RU гео — отключить IPv6 ([id=59361]).

## Прочее
- **[id=59410–59421|c0mrade|09.11]** Сгенерировать WEB_API_DEFAULT_TOKEN в .env: `sed -i "s/^WEB_API_DEFAULT_TOKEN=.*/WEB_API_DEFAULT_TOKEN=$(openssl rand -hex 32)/" .env`.
- **[id=59071|Павел Шумов|09.11]** Режим кнопки «Подключиться» (env): `CONNECT_BUTTON_MODE` = guide | miniapp_subscription | miniapp_custom | link | happ_cryptolink.
- **[id=59395|Серёжа|09.11]** `DEVICES_SELECTION_DISABLED_AMOUNT=0` — отключает функционал устройств.
- **[id=59598|—|09.11]** «Автономный магазин» без Telegram: сайт + email, бэкенд-посредник через API бота создает юзера и счет, поллинг статуса раз в 3–5 сек; примерный nginx-блок shop.домен (proxy_pass /api/ на бэкенд 9000, остальное статиc) — [id=59595|Дмитрий|09.11] дословный пример с ssl_certificate letsencrypt.
- **[id=60772|—|11.11]** Мнения о платежках: плatega на старте 9% (далее понижают); «юкасса белая, все остальное около того» — [id=61783].
- **[id=60672|❤️‍🔥|11.11]** Platega: вывод в лк только крипта ($3 TRC, быстро), в выходные не выплачивают; минус — нет Т-Пей/Сбер Пей.
- **[id=60784,60789,60790|Евген,BURJUY|11.11]** UrlPay настройка: в поле сайт — ссылка на бота, остальное не нужно, пройдете верификацию; в кабинете мулен Callback url — `https://домен/pay-webhook` (путь из настроек бота) [id=62696,62702].
- **[id=61501,61528,61546|Deleted Account,С,Илья|11.11]** CryptoBot: для вебхука беру min_amount/api токен из кабинета КБ; вебхук = домен/путь.
- **[id=60616|⁠⁠|11.11]** Helеket: писать secret key, хук должен уходить с секретом ([id=61091]).
- **[id=59211|Pedzeo|09.11]** Замер скорости из миниапп: замер идет с сервера; если блокируешь measure-сайты в редирект — фича не сработает ([id=59202|Дмитрий]).
- **[id=62844|Valerii Bezkorovainyi|12.11]** NPM (Nginx Proxy Manager) конфиг миниапп (advanced):
  ```nginx
  location / { root /miniapp; index index.html; try_files $uri /index.html =404; }
  location = /miniapp/app-config.json { add_header Access-Control-Allow-Origin "*"; try_files $uri =404; }
  location /miniapp/ { proxy_pass http://127.0.0.1:8080/miniapp/; proxy_set_header Host $host; ... }
  ```
- **[id=62875,62893,62905|Valerii,Илья|12.11]** Свежий домен сразу долбят сканеры WordPress (wp-admin/setup-config.php 404); с Cloudflare не настроено доверие прокси; норм — забить или fail2ban; чек IP на abuseipdb.
- **[id=60052,62867|—|10.11/12.11]** Сканы /.git/config, wp-admin на свежеподнятых бэкендах — фоновый шум, норма.
- **[id=59225–59260|Edward Forix,Egor|09.11]** Автопродление считало только период (50р вместо полного тарифа) — у автора включилась «простая покупка» после обновы (env приоритет затер настройку); рекомендация: логи смотри, срок автоплаты уменьши и проверь сумму списания; рефактор оплаты планируется (единая модель).

## Флуд
- Футболки, сны, болезни (39.8 температура у нескольких), Dota, воскрешение, мем-тексты «Решалы», шутки про Марио/майнкрафт/ФСБ — флуд, не фиксирую.
