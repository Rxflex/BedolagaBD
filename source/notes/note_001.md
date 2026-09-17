# Заметки из chunk_001 (id 17..4040, период 23.08.2025 .. 07.09.2025)

## Рождение чата и бот Bedolaga (автор Egor/Fr1ngg, @FringVPN_bot)
- **[id=17..46|Egor|23.08.2025](https://t.me/c/2941121338/10/17)** Чат создан для пользователей бота remnawave-bedolaga-telegram-bot (https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot). Бот переписан с нуля с v1 на v2 (v2.0.4): разные режимы вывода подключения к подписке; локальный запуск автоопределяет ссылку (local/remote mode не нужен).
- **[id=68..70|23.08.2025](https://t.me/c/2941121338/6/68)** Частая ошибка запуска: `docker compose up -d` → "no configuration file provided: not found" — в папке нет docker-compose.yml (в ранних релизах его нужно было собирать вручную по примеру из README).
- **[id=75|Egor|23.08.2025](https://t.me/c/2941121338/2/75)** #v2_0_5: режим выбора трафика.
  ```env
  TRAFFIC_SELECTION_MODE=selectable   # selectable | fixed
  FIXED_TRAFFIC_LIMIT_GB=0            # 0 = безлимит
  # для fixed проставить цены всем PRICE_TRAFFIC_5/10/25/50/100/250/0=0
  ```
  Обновление: `docker compose pull && docker compose up -d` (позже стал канон `docker compose down; pull; up -d`).
- **[id=102..138|23.08.2025](https://t.me/c/2941121338/52/102)** Ценообразование: цены пакетов трафика в env (PRICE_TRAFFIC_5GB и т.д.), PRICE_PER_DEVICE=5000 — цена за доп. устройство. В режиме fixed всё по нулям, цену брать только за дни подписки. Соль: «поставь цену на дни, на остальное 0».
- **[id=148..167|23.08.2025](https://t.me/c/2941121338/2/148)** Промокоды на дни (продление) и триалы; баг двойного списания в истории; совет: подписку удалять только через бота (удаление юзера в панели + синк ломало данные — «все через попу»). В v2.0.6 [id=289](https://t.me/c/2941121338/2/289) это пофикшено: удалённые в панели подписки при синке затираются, юзер откатывается к триальному состоянию без права повторного триала.
- **[id=283, 289, 320, 500|Egor|24-26.08.2025](https://t.me/c/2941121338/6/283)** Релизы v2_0_6 (промокоды+редактирование подписки), v2_0_7 (фикс синка/статуса истёкших подписок, цена убрана из профиля), v2_0_8 — автомиграция БД: удаляет дубли записей в таблице subscriptions (несколько записей на один user_id), работает с SQLite/PostgreSQL/MySQL.
- **[id=515..517|Egor|26.08.2025](https://t.me/c/2941121338/144/515)** Xray-конфиг «YouTube без рекламы» (нюанс: YouTube в РФ из РФ-ноды идёт напрямую без VPN-трафика, реклама режется на исходе):
  ```json
  {
    "log": { "loglevel": "none" },
    "dns": { "servers": ["8.8.8.8","8.8.4.4","1.1.1.1"], "disableFallback": false },
    "inbounds": [{
      "tag": "YoutubeFree_PROFILE", "port": 443, "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "raw", "security": "reality",
        "realitySettings": {
          "show": false, "xver": 1, "target": "127.0.0.1:9443", "spiderX": "",
          "shortIds": ["XXXXXXXXXXXXXX"],
          "privateKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "serverNames": ["domain.com"]
        }
      }
    }],
    "outbounds": [
      { "tag": "DIRECT", "protocol": "freedom" },
      { "tag": "BLOCK", "protocol": "blackhole" }
    ],
    "routing": { "rules": [
      { "type": "field", "domain": ["domain:youtube.com","domain:youtubei.googleapis.com","domain:ggpht.com","domain:ytimg.com","domain:googleapis.com"], "outboundTag": "DIRECT" },
      { "type": "field", "domain": ["domain:googlesyndication.com","domain:googleadservices.com","domain:doubleclick.net","domain:googleads.g.doubleclick.net","domain:pagead2.googlesyndication.com","domain:partnerad.l.doubleclick.net","domain:ads.youtube.com","regexp:.*pagead.*","regexp:.*doubleclick.*"], "outboundTag": "BLOCK" },
      { "ip": ["geoip:private"], "type": "field", "outboundTag": "BLOCK" },
      { "type": "field", "domain": ["geosite:private"], "outboundTag": "BLOCK" },
      { "type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK" }
    ] }
  }
  ```
  Идея: поднять RU-ноду и направлять трафик ютуба на неё (в РФ ютуб из РФ не тормозится).
- **[id=522..530|26.08.2025](https://t.me/c/2941121338/522)** English-локализации нет, тексты в `app/localization/texts.py`; править + монтировать в докер `- ./texts.py:/app/localization/texts.py` ([id=826|art vs](https://t.me/c/2941121338/826)). При docker compose pull изменения репы не перетрут ваш файл, но обновления переводов руками мерджить.
- **[id=448..453|25.08.2025](https://t.me/c/2941121338/448)** YooKassa: порядок отображения способов оплаты менять нельзя (ограничение ЮKassa); СБП через юкассу выгоднее — комиссия 0.4% против 3.5% карт; reference https://yookassa.ru/developers/payment-acceptance/integration-scenarios/widget/additional-settings/separate-payment-methods. С 1.09.2025 ожидались проблемы с «впн»-платежами (аккредитация РКН) — в 2.1.4 добавили настраиваемые описания платежей:
  ```env
  PAYMENT_SERVICE_NAME=Интернет-сервис
  PAYMENT_BALANCE_DESCRIPTION=Пополнение баланса
  PAYMENT_SUBSCRIPTION_DESCRIPTION=Оплата подписки
  ```
- **[id=796..872, 1263|29-31.08.2025](https://t.me/c/2941121338/6/796)** Интеграция YooKassa (v2.1.0): вебхук `https://your-domain.com:8082/yookassa-webhook`, в docker-compose бота должен быть проброшен порт 8082. Серия багов фиксов: `'async_generator' object does not support the asynchronous context manager protocol` (process_topup_amount), `cannot import name 'async_session_maker'` (ImportError), `can't subtract offset-naive and offset-aware datetimes` (asyncpg DataError при вставке yookassa_payments), 405/500/502 из-за веб-сервера в контейнере, «Webhook без подписи» → «Неверная подпись webhook» (проверка подписи v1, в отладочном режиме обработка продолжается). Итог: платежи проходят, подпись YooKassa так и не верифицируется корректно у некоторых (v2.2.3 заявлял валидацию HMAC-SHA256 для Tribute @yazhog).
- **[id=933..945|30.08.2025](https://t.me/c/2941121338/52/933)** Баг: донат через Tribute зачислялся в копейках (`amount_kopeks = int(amount_rubles * 100)`) — юзеру падало в 100 раз больше; экстренно пофикшено после релиза 2.1.0.
- **[id=775..785, 877..881|29.08.2025](https://t.me/c/2941121338/649/775)** Если Redis некорректно настроен, уведомления дублируются/теряются (история между циклами теряется; после рестарта бота повторные уведомления). Проверять Redis в докере и env.
- **[id=490|24.08.2025](https://t.me/c/2941121338/10/490)** Postgres ошибка `Role "user" does not exist` + FATAL password authentication failed: env должен содержать переменные в верхнем регистре:
  ```env
  # Было (сломано):
  postgres_db=remnawave_bot
  postgres_user=
  postgres_password=
  # Должно быть:
  POSTGRES_DB=remnawave_bot
  POSTGRES_USER=
  POSTGRES_PASSWORD=
  ```
- **[id=1156, 1272|30-31.08.2025](https://t.me/c/2941121338/1156)** v2_1_1 Maintenance Mode System: авто-режим техработ при недоступности RemnaWave API (3 неуспешных проверки подряд → техрежим), мониторинг API каждые 30 сек, защита юзеров, админы сохраняют доступ, авто-выход при поднятии панели, ручное вкл/выкл в админке, новые env параметры. Баг на 2.1.1: `'MaintenanceService' object has no attribute 'set_bot'` → скоро фикс.
- **[id=1272|31.08.2025](https://t.me/c/2941121338/1272)** v2_1_2: периоды подписки env.
  ```env
  AVAILABLE_SUBSCRIPTION_PERIODS=14,30,60,90,180,360
  AVAILABLE_RENEWAL_PERIODS=30,90,180
  ```
  + Улучшения YooKassa; из меню синхронизации вырезаны лишние кнопки.
- **[id=1276|31.08.2025](https://t.me/c/2941121338/1276)** v2_1_3: редактирование промокодов, статистика промокодов с username, фикс ошибок реферальной системы (дубли при регистрации с рефкодом, блокировка ввода реф-кодов в AuthMiddleware), автообновление профиля юзера при каждом взаимодействии (/start, кнопки) — username/имя/фамилия актуальны. **[id=1319..1321|31.08.2025](https://t.me/c/2941121338/1319)** v2_1_4: авто-пропуск шага выбора серверов при одном сервере; уведомления админам о событиях (RemnaWave API state, вкл/выкл техработ); настраиваемые описания платежей (см. выше), убран хардкод «пополнение баланса VPN».
- **[id=1425, 1455..1456, 1655|01-02.09.2025](https://t.me/c/2941121338/1425)** Deфолт подписки: `DEFAULT_TRAFFIC_RESET_STRATEGY=MONTH` (сброс трафика день/неделя/месяц/год/никогда), `DEFAULT_TRAFFIC_LIMIT_GB=100`, `DEFAULT_DEVICE_LIMIT=1`.
- **[id=1656|02.09.2025](https://t.me/c/2941121338/1656)** v2_1_5: поддержка защищённых панелей Remnawave через remnawave-reverse-proxy (cookie):
  ```env
  REMNAWAVE_SECRET_KEY=mykey:myvalue
  ```
  Принцип: если панель доступна только через https://panel.example.com/auth/login?secret=value — бот автоматически добавляет куки к каждому API запросу. Для eGames скрипта (egam.es) REMNAWAVE_API_URL=https://panel.example.com/auth/login?XXXXXXX=DDDDDDDD и тот же secret в REMNAWAVE_SECRET_KEY.
- **[id=1716|03.09.2025](https://t.me/c/2941121338/1716)** payanyway (@Глеб): «менее популярная, но с более приятной комиссией и подключением за 10 сек»; art vs посчитал — 4% за вывод на карту для самозанятых, смысла менять мало; для ИП/ООО 4.7%+50р.
- **[id=1784..1786|03.09.2025](https://t.me/c/2941121338/1784)** Пример docker-compose для Caddy (selfsteal) с host-сеткой, чтобы вебхуки доходили:
  ```yaml
  services:
    caddy:
      image: caddy:2.9.1
      container_name: caddy-selfsteal
      restart: unless-stopped
      volumes:
        - ./Caddyfile:/etc/caddy/Caddyfile
        - /opt/caddy/html:/var/www/html
        - ./logs:/var/log/caddy
        - caddy_data:/data
        - caddy_config:/config
      env_file: [.env]
      network_mode: "host"
      logging:
        driver: "json-file"
        options: { max-size: "10m", max-file: "3" }
  volumes:
    caddy_data:
    caddy_config:
  ```
  Боту нужна своя сеть (bot_network, driver bridge).
- **[id=1798..1800, 2009|03.09.2025](https://t.me/c/2941121338/1798)** Курс Telegram Stars через env: `TELEGRAM_STARS_RATE_RUB=1.3` (был баг с оплатой за Stars, исправлен).
- **[id=1953|04.09.2025](https://t.me/c/2941121338/1953)** v2_1_8: динамические пакеты трафика.
  ```env
  TRAFFIC_PACKAGES_CONFIG="5:2000:false,10:3500:false,25:7000:false,50:11000:true,100:15000:true,250:17000:false,500:19000:false,1000:19500:true,0:20000:true"
  MAX_DEVICES_LIMIT=50   # 0 = без лимита
  ```
  (добавлены пакеты 500 и 1000 ГБ).
- **[id=1990|04.09.2025](https://t.me/c/2941121338/1990)** v2_1_9: мультивыбор серверов для юзеров, управление устройствами/трафиком, сброс HWID; фиксы дублирования уведомлений об истечении подписки.
- **[id=2010|05.09.2025](https://t.me/c/2941121338/2010)** v2_2_0: новая формула цены: `базовая цена + (услуги × месяцы)`. Периоды 30/90/180 дней (1/3/6 мес); продления умножением на месяцы; доплаты за услуги по оставшимся месяцам. Пример расчёта (180 дней): 400₽ (база) + 1200₽ (трафик) + 300₽ (устройства) + 1200₽ (сервера) = 3100₽.
- **[id=2054|06.09.2025](https://t.me/c/2941121338/2054)** v2_2_1: анти-абуз реферальной системы. Env:
  ```env
  REFERRAL_MINIMUM_TOPUP_KOPEKS=10000     # минимальное пополнение для активации бонусов
  REFERRAL_FIRST_TOPUP_BONUS_KOPEKS=10000 # бонус новому при первом пополнении
  REFERRAL_INVITER_BONUS_KOPEKS=10000     # бонус пригласившему при первом пополнении
  REFERRAL_COMMISSION_PERCENT=25          # комиссия с последующих пополнений
  REFERRAL_NOTIFICATIONS_ENABLED=true
  REFERRAL_NOTIFICATION_RETRY_ATTEMPTS=3
  ```
  + колонка has_made_first_topup; убраны мгновенные награды при регистрации; ранее (v2.1.7) в 2.1.x была настройка `REFERRAL_NOTIFICATIONS_ENABLED=true` только.
- **[id=2075|06.09.2025](https://t.me/c/2941121338/2075)** v2_2_2: уведомления администраторам в приватный канал/топик:
  ```env
  ADMIN_NOTIFICATIONS_ENABLED=true
  ADMIN_NOTIFICATIONS_CHAT_ID=-100XXXXXXXXXXXX  # -100 префикс
  ADMIN_NOTIFICATIONS_TOPIC_ID=123              # ID топика
  ```
- **[id=2102|07.09.2025](https://t.me/c/2941121338/2102)** v2_2_3: управляемые сообщения в главном меню (случайный показ при нескольких, HTML разметка с валидацией); защита вебхуков Tribute HMAC-SHA256 (@yazhog); фикс рефки (реф-код принимается сообщением, партнёрка за первый платёж).
- **[id=2119..2127|04.09.2025](https://t.me/c/2941121338/2119)** MAX_DEVICES_LIMIT=0 — снят жёсткий лимит 10 устройств.
- **[id=2185|04.09.2025](https://t.me/c/2941121338/2185)** #v2_1_9 патчноут также упоминал: правило очистки транзакций при удалении юзера, исправление дублирования уведомлений.
- **[id=2248..2252|05.09.2025](https://t.me/c/2941121338/2248)** #v2_2_1 (ранее 2.2.0 не публиковали) — повтор: см. выше.
- **[id=3352|06.09.2025](https://t.me/c/2941121338/3352)** Pull request переключения типа подписки: https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot/pull/33.
- **[id=3486|06.09.2025](https://t.me/c/2941121338/3486)** v2_2_3 улучшенное уведомление о статусе API Remnawave, отображение @username (ID: 123).
- **[id=3670, 3672..3674|07.09.2025](https://t.me/c/2941121338/3670)** Remnawave releases: Panel v2.1.9 (Restore curl in Dockerfile), Node v2.1.6 и XTLS-SDK v0.6.2 (Xray Core bump 25.9.5).
- **[id=3732, 3888..3890, 3913..3916, 3923, 3928..3929|07.09.2025](https://t.me/c/2941121338/3732)** Проверка подписи юкассы — «Подпись не совпала, но продолжаем обработку (режим отладки)»; для нормального вебхука Tribute+ЮKassa: либо одна сеть bot_network в докере и reverse_proxy http://remnawave_bot:8081, либо разные сети и localhost. У кого-то Tribute и ЮKassa оба висели на 8081 и не работали.

## Команды запуска/обновления бота
- **[id=1789, 1806, 1835, 2062, 2294, 2358..2364, 3065, 3147, 3610..3616|на протяжении](https://t.me/c/2941121338/1789)** Каноничное обновление:
  ```bash
  docker compose down
  docker compose pull
  docker compose up -d
  # с live-логами:
  docker compose down && docker compose pull && docker compose up && docker compose logs -f
  ```
  Критический нюанс: `.env` перечитывается только при `docker compose down` → `up` (не при рестарте бота). `docker compose down -v` **потрёт базы** — использовать только осознанно.
- **[id=2149, 3025, 3030, 3116..3128|06.09.2025](https://t.me/c/2941121338/2149)** Для сборки image из исходников: в docker-compose в секции bot:
  ```yaml
  bot:
      build: .
      container_name: remnawave_bot
      restart: unless-stopped
  ```
  (замена `image: fr1ngg/remnawave-bedolaga-telegram-bot:latest` на `build: .` — если хотите билдить локально и править переводы). Обратно при обновлении: вернуть `image:`, `docker compose pull`.
- **[id=3093, 3097, 3102, 3118, 3151..3341|06.09.2025](https://t.me/c/2941121338/3093)** Ошибка `failed to create network ... invalid pool request: Pool overlaps with other one on this address space` — свободные IP-пулы docker посмотреть и подставить другой в bot_network:
  ```bash
  docker network ls
  docker network inspect $(docker network ls -q) -f '{{.Name}} {{range .IPAM.Config}}{{.Subnet}}{{end}}'
  ```
  В docker-compose бота в секции networks менять `subnet: 172.20.0.0/16` на свободный (например 172.50.0.0/16).
- **[id=2132, 3117, 3129..3132, 3381|06.09.2025](https://t.me/c/2941121338/2132)** Права на логи: `sudo chown -R 1000:1000 ./logs ./data` в папке с ботом (контейнер работает под user 1000:1000).
- **[id=3456..3457|06.09.2025](https://t.me/c/2941121338/3456)** Ошибка при запуске `Token is invalid!` — если BOT_TOKEN в .env без кавычек/с неверным форматом; формат `BOT_TOKEN=2143243:tysfwquiyreuiqwop`. (Сервер в РФ также может не достучаться до api.telegram.org.)
- **[id=3503..3509, 3514|06.09.2025](https://t.me/c/2941121338/3503)** Если панель на одном сервере с ботом, можно поставить их в одну docker сеть (`networks: bot_network`), разницы с внешним API нет; с eGames-панелью наоборот — включить внешний доступ к API (https://wiki.egam.es/ru/configuration/external-api/).

## Хостинг-опыт
- **[id=78..86|23.08.2025](https://t.me/c/2941121338/52/78)** bill.blackmore.cloud — промо сервер за 10р первый месяц, 2 ядра, 2 ГБ RAM, 1000 Гбит канал.
- **[id=198|23.08.2025](https://t.me/c/2941121338/52/198)** litnets.com — гигабит по тарифу (обещания).
- **[id=239..247|23.08.2025](https://t.me/c/2941121338/52/239)** Hostkey — дешёвые сервера, неограниченный трафик, выбран для панели; оценка «700-900» (по слову), скорости на бою у некоторых не мерили. Требуют API.
- **[id=248|28.08.2025](https://t.me/c/2941121338/52/248)** geohosting — выдаёт не более 300 Мб/с.
- **[id=658|28.08.2025](https://t.me/c/2941121338/649/658)** Adminvps — «кусок говна»; Webhost1 — «норм за свою цену, но нужно хантить доступные сервера»; Vdsina com — «стабильно хорошо».
- **[id=661..671|28.08.2025](https://t.me/c/2941121338/649/661)** Aeza — негатив: грязные IP, частые дудосы; но скорость не плохая ([id=2036|03.09.2025](https://t.me/c/2941121338/2036)). У Aeza сервер для тестов удобно переустановить одной кнопкой.
- **[id=679|28.08.2025](https://t.me/c/2941121338/649/679)** @biil_robot — рекомендация Egor: аптайм высокий, гигабит (по спидтесту 800+ Мб/с), промки по 150р 2 ядра 3 ГБ (лимит сети 100 Мбит — под панель); завезли Японию (на выхах тест). [id=680](https://t.me/c/2941121338/649/680) @dhostVPS_bot — 10 гбит Нидерланды, по спидтесту 7000 Мбит на скаче/загрузке, аптайм высокий, от 3$ за 1 ядро/1 ГБ, без KYC, оплата любыми способами; промокод `BEDOLAGA` — 25% на первый заказ (реклама не оплачена). [id=680](https://t.me/c/2941121338/649/680) qwins.co — тестируется, гигабит, грузит-качает 500 Мбит днём.
- **[id=736|28.08.2025](https://t.me/c/2941121338/649/736)** bluevps.com (Швеция) — оплата только криптой.
- **[id=766|28.08.2025](https://t.me/c/2941121338/649/766)** 4vps.su — рекомендует Илья (рефка).
- **[id=2017..2029|03.09.2025](https://t.me/c/2941121338/2017)** dhostVPS: у Egor второй месяц, скорость норм, промик под панель за 150р; сайт в разработке; на дедиках бывают предложения за 6000-8000р со своей сетью. «Лучше сидеть на небольших хостах, но плюс-минус проверенных».
- **[id=2291|03.09.2025](https://t.me/c/2941121338/2291)** «большинство серверов у аезы» (у кого-то), «скорость выдает».
- **[id=2322|04.09.2025](https://t.me/c/2941121338/2322)** Aeza имеет 25 гигабитный сервер в Германии (дорого).
- **[id=2325|04.09.2025](https://t.me/c/2941121338/2325)** Melbicom — ещё вариант (если «бабок дофига»).
- **[id=2324|04.09.2025](https://t.me/c/2941121338/2324)** Beget — использует Юрий.
- **[id=1274|31.08.2025](https://t.me/c/2941121338/1274)** Contabo — 7.26 usd за доп. ноду «вроде ничего».
- **[id=675..676|28.08.2025](https://t.me/c/2941121338/649/675)** Казахстанские сервера — «работают но скорость такая себе», «отключил даже добавлять стыдно» (в боте).
- **[id=678..681|28.08.2025](https://t.me/c/2941121338/678)** По скорости гигабит на VPS: сети переебаны вдоль и поперёк + санкции, до клиента (с дом. интернета) реально доходит 300-500 Мбит; на нормальном Wi-Fi 6e и телефонных тарифах на 800-900 Мбит под впн поднять реально 700+ ([id=705..715](https://t.me/c/2941121338/649/705)).

## Прокси/сети/сертификаты
- **[id=387..395|25.08.2025](https://t.me/c/2941121338/52/387)** Автообновление сертификатов: скрипт Fringg с гитхаба + API TimeWeb для wildcard-сертификатов по крону; для 5 сабдоменов раньше было 10 файлов сертов в папке; после — 2 файла (key+PEM) на домен. Hostkey тоже имеет API.
- **[id=141..143|23.08.2025](https://t.me/c/2941121338/52/141)** Перенос панели на другой хост — есть готовые скрипты переноса.
- **[id=439..447|25.08.2025](https://t.me/c/2941121338/52/439)** Панель Remnawave + nginx в докере: если контейнер nginx смонтирован без конфига — появляется папка config.d и панель/бот попеременно падают; гпт предложил добавить `resolver` в конфиг nginx (контейнеры меняют IP при рестартах).
- **[id=442|30.08.2025](https://t.me/c/2941121338/52/442)** Caddy на РФ-ноде как точка входа в подписку: `netbird`/VPN-туннель до мейн-сервера; редирект-страницу подписки надо выдавать через локали (maposia remnawave-telegram-sub-mini-app, шаблон Egora https://github.com/Fr1ngg/remnawave-multistep-xraychecker-subpage-adaptive).
- **[id=2909|07.09.2025](https://t.me/c/2941121338/2909)** Миниапп не открывает ссылки с подпиской — редирект мутить на странице подписки (свой app-config.json). Подписка в бот можно вставить своим app-config.json (свои ключи верхнего уровня). Шаблон redirect-page от Egora — /opt/app/frontend/redirect-page.

## Remnawave структуры (сквады/профили)
- **[id=1050..1078|30.08.2025](https://t.me/c/2941121338/52/1050)** Remnawave «сквады» = страны/серверы в боте; профиль = конфиг Xray; хост = нода. Сквады назначаются юзерам, профили сквадам, хосты профилям. Ссылка на объяснение: https://remna.st/blog/misc/new-profiles-and-squads/explaining-new-profile-and-squads-system. В боте сквад=страна.
- **[id=1090, 2379..2397, 3484..3486|04-06.09.2025](https://t.me/c/2941121338/1090)** Логика через сквады: триал сквад (в env TRIAL_SQUAD), платный сквад один → шаг выбора серверов скипается, доп. сервера скрыты; несколько сквадов с одинаковыми инбаундами — можно (Remna не ограничивает), но «один сквад для всех» проще. Порядок инбаундов/лимит юзеров на сквад только в боте (Remna их не знает).
- **[id=2110..2114, 3654..3657|04.09, 07.09.2025](https://t.me/c/2941121338/2110)** Лимит пользователей на сквад задаётся в боте (внутренний лимит, по исчерпании сквад пропадает из продажи); в Remnawave лимит есть, но в бот не подтягивается.

## Полезные ссылки/инструменты
- **[id=310|25.08.2025](https://t.me/c/2941121338/52/310)** Стоковый subscription-page: https://github.com/remnawave/subscription-page (скачать, заменить лого, смонтировать).
- **[id=322|30.08.2025](https://t.me/c/2941121338/52/322)** Мини-апка (страница подписки) от maposia: https://github.com/maposia/remnawave-telegram-sub-mini-app.
- **[id=861|30.08.2025](https://t.me/c/2941121338/861)** Шаблон саб-страницы Egora: https://github.com/Fr1ngg/remnawave-multistep-xraychecker-subpage-adaptive.
- **[id=453|25.08.2025](https://t.me/c/2941121338/10/453)** Separate payment methods в YooKassa: https://yookassa.ru/developers/payment-acceptance/integration-scenarios/widget/additional-settings/separate-payment-methods.
- **[id=1016|03.09.2025](https://t.me/c/2941121338/52/1016)** Найденный пример 3xui-shop (платёжка): https://github.com/snoups/3xui-shop.
- **[id=1103|05.09.2025](https://t.me/c/2941121338/1103)** 3xui shop пример (повтор): https://github.com/snoups/3xui-shop.
- **[id=1756, 2966|03.09.2025](https://t.me/c/2941121338/1756)** Доки внешнего API eGames-панели: https://wiki.egam.es/ru/configuration/external-api/.
- **[id=1318|31.08.2025](https://t.me/c/2941121338/1318)** Полный список env-параметров бота: https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot/blob/main/.env.example.
- **[id=3354|06.09.2025](https://t.me/c/2941121338/3354)** Топ спонсоров проекта: https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot/tree/v2.1.8?tab=readme-ov-file#-%D1%82%D0%BE%D0%BF-%D1%81%D0%BF%D0%BE%D0%BD%D1%81%D0%BE%D1%80%D1%8B-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0
- **[id=1013, 1078|30.08.2025](https://t.me/c/2941121338/52/1013)** Доки Remnawave по профилям/сквадам: https://remna.st (и статья выше).

## Разное/бизнес-логика
- **[id=2286|04.09.2025](https://t.me/c/2941121338/2286)** Автопродление: продлит по тем же настройкам, что выбраны юзером.
- **[id=2332|04.09.2025](https://t.me/c/2941121338/2332)** Покупка доп. услуг (сквады/устройства/трафик) — единоразово на период подписки (позже пересчитали на помесячную).
- **[id=2595..2599|05.09.2025](https://t.me/c/2941121338/2595)** Формула расчёта: базовая цена тарифа + (кол-во доп. устройств + трафик + сервера) × месяцы тарифа. Нейронки помогут подобрать цены под желаемую стоимость за 1/3/6/12 мес.
- **[id=2600|05.09.2025](https://t.me/c/2941121338/2600)** Планируется скидка на доп. услуги по сроку подписки (чем больше срок — больше скидка).
- **[id=2701..2704|05.09.2025](https://t.me/c/2941121338/2701)** Стратегии ценообразования от Edward Forix: минимальная подписка 150₽, Tribute min 100₽ — остаток 50₽ «лежит на балансе» и «включается человеческая жадность» (UX-приём удержания).
- **[id=3491|06.09.2025](https://t.me/c/2941121338/3491)** Сброс HWID и настройка сброса трафика — в env (см. DEFAULT_TRAFFIC_RESET_STRATEGY).
- **[id=2224..2227|06.09.2025](https://t.me/c/2941121338/2224)** Первичная настройка бота после запуска: 1) Синхронизация серверов (обязательно) — Админ панель → Подписки → Управление серверами → Синхронизация; 2) Синхронизация пользователей (если есть база) — Админ панель → Remnawave → Синхронизация. Названия стран и цены серверов правятся в боте: Админ панель → Подписки → Управление серверами → список серверов (меняются и название, цена, лимит, значки стран).
- **[id=3488|06.09.2025](https://t.me/c/2941121338/3488)** Админ может сам себя забанить через бота — разбанить себя: через базу данных или твика в админах.
- **[id=3005..3007, 3011, 3014..3015, 3531|06-07.09.2025](https://t.me/c/2941121338/3005)** Перенос юзеров с бота «Мачка»/Иисуса на Bedolaga: синки нормальные, переносит по тг айди подписки; балансы мачки не перенести (у мачки их нет, «только у моего форка»), рефералов тоже надо руками/из старой БД.
- **[id=3079..3080, 3092|06-07.09.2025](https://t.me/c/2941121338/3079)** Для эгейма/eGames-панели при наличии TinyAuth (nginx) перед API: для бота прокидывать запросы на панель через location /api/ { proxy_pass http://remnawave_backend; } (без TinyAuth), а TinyAuth оставить только на веб-интерфейс (см. [id=3231](https://t.me/c/2941121338/3231)).
- **[id=3426..3427|07.09.2025](https://t.me/c/2941121338/3426)** Caddy: если бот на том же сервере, что и Caddy — нужен shared docker network (контейнер Caddy подключить к сети бота); иначе reverse_proxy на localhost работает только при network_mode: host.
- **[id=3435|07.09.2025](https://t.me/c/2941121338/3435)** Напоминание: по умолчанию поллинг (не вебхуки), потому что «легче отлаживать»; при падении панели бот уходит в режим тех работ.
- **[id=3486, 3487|07.09.2025](https://t.me/c/2941121338/3486)** Health-check чата бота: если трибьют отключён — «webhook сервер не запускается» и http://0.0.0.0:8081/tribute-webhook; если payment трибьют включен — healthy.
