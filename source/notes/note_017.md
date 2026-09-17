# Заметки из chunk_017 (id 89508..96616, 05.12.2025–09.12.2025)

## Bedolaga-бот: настройки через админку и env
- **[id=89531|—|05.12](https://t.me/c/2941121338/89531)** Бот бесконечно ребутится, если в .env есть поля с незаполненными значениями (например `PRICE_360_DAYS=`). Чтобы менять цены через админ-панель бота — закомментировать строки env целиком: `#PRICE_360_DAYS=`.
- **[id=90828..90830|06.12](https://t.me/c/2941121338/90828)** «Настройка сохранена в БД, но не применена: значение задаётся через окружение» → приоритет у env, удалить/закомментировать настройки из .env.
- **[id=95975|—|08.12](https://t.me/c/2941121338/95975)** Цены формируются не только за период, но и за сервера/трафик/устройства — проверять все слагаемые, если цена «сбилась».
- **[id=95776|c0mrade|08.12](https://t.me/c/2941121338/95776)** Для ручной проверки платежей в env:
```
AUTO_PURCHASE_AFTER_TOPUP_ENABLED=true
PAYMENT_VERIFICATION_AUTO_CHECK_ENABLED=true
PAYMENT_VERIFICATION_AUTO_CHECK_INTERVAL_MINUTES=2
```
- **[id=89978|hdhdh4226ru|05.12](https://t.me/c/2941121338/89978)** В свежих версиях бота есть готовые страницы оплаты: `miniapp.домен/payment/fail.html` и `miniapp.домен/payment/succes.html`. Иначе — страницы успеха/ошибки с редиректом в бота (любой ИИ сделает за 30 сек).
- **[id=89946|—|05.12](https://t.me/c/2941121338/89946)** MulenPay (UrlPay) — работает, но выплаты вручную и плохой дизайн. Platega — хвалят: менеджер в чате @platega_connect, @ArstanPlatega; комплаенс бывает долгий (дни), в выходные согласование не проходит (id 90823–90852).

## Bedolaga v2.9.0 (обновление 07–08.12.2025)
- **[id=94189|Egor|08.12](https://t.me/c/2941121338/94189)** Интеграция с новым API Remnawave 2.3.0+ (метаданные нод: порт, версия Xray, CPU/RAM, провайдер; bulk-операции сквадов; обратная совместимость со старым API).
- Автотеги пользователей: `TRIAL_USER_TAG=TRIAL`, `PAID_SUBSCRIPTION_USER_TAG=PAID` (A-Z, 0-9, _, до 16 символов).
- Округление звёзд вверх (math.ceil), минимум 1 звезда, `settings.rubles_to_stars`.
- Обновление бота: `cd /root/remnawave-bedolaga-telegram-bot && git pull origin main && make reload`.
- **[id=95926..95929|08.12](https://t.me/c/2941121338/95926)** Ошибка `'usedTrafficBytes'` — критическая ошибка синхронизации пользователей (юзер создался, но нет ссылки подписки); после повторного pull прошло.
- **[id=96004..96018, meme|08.12](https://t.me/c/2941121338/96004)** После обновления Remnawave по `GET /api/users/{uuid}` нет happ crypto link — бот в режиме Happ Crypto Link отдавал незашифрованную ссылку. Временный фикс (замена файлов `happ_crypto.py`, `remnawave_service.py`, `subscription_service.py`) от @meme: закинуть `happ_crypto.py` в `app/utils`, заменить `remnawave_service.py`/`subscription_service.py` в `app/services`, затем `make reload`.
- **[id=95986|08.12](https://t.me/c/2941121338/95986)** Ошибка юзера в промо-группе «Нельзя отключить все страны. Должна быть подключена хотя бы одна страна».
- **[id=95981..95990|08.12](https://t.me/c/2941121338/95981)** `make reload` после Ctrl+C может ронять контейнеры (проверять версии; фикс — повторный pull).
- **[id=96008|—|09.12](https://t.me/c/2941121338/96008)** Ошибка aiogram "Bad Request: there is no text in the message to edit" — при переходе в меню, где сообщение содержит картинку (edit_text на медиа-сообщение).
- **[id=96615|09.12](https://t.me/c/2941121338/96615)** `git pull` падает «Your local changes would be overwritten by merge: docker-compose.yml» → закоммитить/застешить/скачать оригинальный файл своей версии (id 95929: скачать файл СВОЕЙ версии; правка texts.py ломает обновления).
- **[id=96579|Egor|09.12](https://t.me/c/2941121338/96579)** Уведомления о покупках: конфигурации бота → уведомления; создать группу с топиками (уведы/бекапы), бот добавляется в группу, privacy mode выключен, ID группы -100XXXXXXXXXX + ID топика. Топики превращают чат в супергруппу (id -100).

## Remnawave v2.3.x (релиз 07–09.12.2025)
- **[id=93968|Egor|07.12](https://t.me/c/2941121338/93968)** Обязательно бекап; серьёзные изменения API; панель 2.3.0 требует ноды 2.3.0. Алгоритм:
```
cd /opt/remnawave && docker compose pull remnawave && docker compose down && docker compose up -d && docker compose logs -f
cd /opt/remnanode && docker compose pull remnanode && docker compose down && docker compose up -d
```
- HWID-настройки из .env переехали внутрь панели (Подписка → Настройки).
- В v2.3.0 поддержка старых переменных APP_PORT/SSL_CERT полностью прекращена → `NODE_PORT`, `SECRET_KEY`.
- Панель больше не передаёт username в ядро: в логах Xray поле email = id пользователя (важно для парсеров логов, напр. Torrent-Blocker). Полный контроль flow для VLESS-инбаундов.
- **[id=93991|Egor|07.12](https://t.me/c/2941121338/93991)** Прочее: внешние сквады (переопределение HWID/примечаний), balancers в сниппетах, табличный вид нод, ZSTD-сжатие конфига на ноды, `REDIS_SOCKET` (unix-сокет), индивидуальный Xray-JSON для каждого хоста, теги нод, массовое изменение профиля/инбаундов нод, `USER_USAGE_IGNORE_BELOW_BYTES` (игнор трафика < N байт за 15с), `SERVICE_DISABLE_USER_USAGE_RECORDS` (отключить запись истории трафика).
- **[id=96542|Egor|09.12](https://t.me/c/2941121338/96542)** Panel v2.3.2: HWID Inspector, Rescue CLI `docker exec -it remnawave cli` (truncate HWID/SRH таблиц), фикс "Online Now" 60s→30s, restore Internal Squads в TG-нотификациях.
- **[id=91885..91902|06.12](https://t.me/c/2941121338/91885)** Нода Remnawave не управляет подписками сама — при падении панели подписка не отключается, удаление профиля произойдёт только когда панель поднимется. Панель — централизованное управление.
- **[id=94795, legiz|08.12](https://t.me/c/2941121338/94795)** Кто обновился до 2.3 и использует Orion: обновить шаблон страницы подписки (happ cryptolink убран из публичного /api/sub).
- **[id=94691|TheKekich|08.12](https://t.me/c/2941121338/94691)** Проблема: домен хуков слушает 80/443 и перекрывает сертификат домена панели (missing hostname); отдельный nginx-контейнер не поднять — порт занят ремной → конфиг прокидывать в docker-compose ремны.
- **[id=91833|06.12](https://t.me/c/2941121338/91833)** nginx warns: `listen ... http2` deprecated → использовать директиву `http2`; `ssl_stapling` ignored (нет OCSP responder у сертификата); emerg `cannot load certificate miniapp.fullchain.pem` — нет/битый сертификат.

## Конфиг nginx для Bedolaga (hooks + miniapp), дословно
- **[id=91677..91687|06.12](https://t.me/c/2941121338/91677)** Сервер hooks.domain.com с локациями для вебхуков всех платёжек (yookassa/platega/cryptobot/wata/heleket/tribute/pal24/mulenpay) на `remnawave_bot_unified`, `app-config.json` с CORS, локация `/` (прокси всего), miniapp.domain.com (API `/miniapp/*` + статика `root /var/www/remnawave-miniapp; try_files $uri $uri/ /index.html; expires 1h`), default server `ssl_reject_handshake on`. Полный текст:
```nginx
# Hooks + API domain - hooks.domain.com
server {
    listen 80;
    listen 443 ssl http2;
    server_name hooks.domain.com;
    ssl_certificate /etc/ssl/private/hooks.fullchain.pem;
    ssl_certificate_key /etc/ssl/private/hooks.privkey.pem;
    client_max_body_size 32m;
    location = /yookassa-webhook {
        proxy_pass http://remnawave_bot_unified;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s; proxy_send_timeout 120s;
        proxy_buffering off; proxy_request_buffering off;
    }
    # аналогично: /platega-webhook, /cryptobot-webhook, /wata-webhook,
    # /heleket-webhook, /tribute-webhook, /pal24-webhook, /mulenpay-webhook
    location = /app-config.json {
        add_header Access-Control-Allow-Origin "*";
        proxy_pass http://remnawave_bot_unified;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location / {
        proxy_pass http://remnawave_bot_unified;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s; proxy_send_timeout 120s;
        proxy_buffering off; proxy_request_buffering off;
    }
}
# Miniapp domain - miniapp.domain.com (static files + API)
server {
    listen 80; listen 443 ssl http2;
    server_name miniapp.domain.com;
    ssl_certificate /etc/ssl/private/miniapp.fullchain.pem;
    ssl_certificate_key /etc/ssl/private/miniapp.privkey.pem;
    client_max_body_size 32m;
    location /miniapp/ {
        proxy_pass http://remnawave_bot_unified;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s; proxy_send_timeout 120s;
        proxy_buffering off; proxy_request_buffering off;
    }
    location = /app-config.json {
        add_header Access-Control-Allow-Origin "*";
        proxy_pass http://remnawave_bot_unified;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location / {
        root /var/www/remnawave-miniapp;
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }
}
server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;
    ssl_reject_handshake on;
}
```
- **[id=91744|SawGoD|06.12](https://t.me/c/2941121338/91744)** Разбор логов nginx: `listen ... http2` deprecated → `http2 on;`; `ssl_stapling` ignored (нет OCSP); ошибка загрузки сертификата = неверно подключён volume с сертами.
- **[id=96030..96033|08.12](https://t.me/c/2941121338/96030)** 502 после обновления → `docker container restart remnawave-nginx` помог.
- **[id=90304..90305|романтика.com|05.12](https://t.me/c/2941121338/90304)** Caddy 502 `dial tcp [::1]:8080: connect: connection refused` — не был поднят бэкенд; обновление бота решило.

## Caddy selfsteal на два порта (TCP + xhttp)
- **[id=94738|Фантомас|08.12](https://t.me/c/2941121338/94738)** «Если нужен конфиг caddy... два порта на реверс прокси, 2 инбаунда в ремне и правильный конфиг в nginx/caddy». Дословно:
```caddy
{
    https_port {$SELF_STEAL_PORT_TCP}
    https_port {$SELF_STEAL_PORT_XHTTP}
    default_bind 127.0.0.1
    servers {
        listener_wrappers {
            proxy_protocol {
                allow 127.0.0.1/32
            }
            tls
        }
    }
    auto_https disable_redirects
}

:{$SELF_STEAL_PORT_TCP} {
    tls internal
    respond 204
}
:{$SELF_STEAL_PORT_XHTTP} {
    tls internal
    respond 204
}

http://{$SELF_STEAL_DOMAIN} {
    bind 0.0.0.0
    redir https://{$SELF_STEAL_DOMAIN}{uri} permanent
}
https://{$SELF_STEAL_DOMAIN} {
    root * /var/www/html
    try_files {path} /index.html
    file_server
}

:80 {
    bind 0.0.0.0
    respond 204
}
```

## Multi-transport на одной ноде (Reality + xhttp + ws через fallback)
- **[id=94778|мысли|08.12](https://t.me/c/2941121338/94778)** Все на 443; VLESS-Reality принимает TCP 443, fallback'и отдают xhttp и ws на 127.0.0.1. Xray-JSON (сокращено до сути, дословная структура):
```json
{
  "log": {"loglevel": "info"},
  "inbounds": [
    {
      "tag": "VLESS_DE-01",
      "port": 5443,
      "listen": "127.0.0.1",
      "protocol": "vless",
      "settings": {
        "clients": [],
        "fallbacks": [{"dest": 2023}, {"dest": 2063}],
        "decryption": "none"
      },
      "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
      "streamSettings": {
        "network": "raw",
        "security": "reality",
        "rawSettings": {"acceptProxyProtocol": true},
        "realitySettings": {
          "xver": 2,
          "target": "127.0.0.1:8443",
          "shortIds": [""],
          "publicKey": "",
          "privateKey": "",
          "fingerprint": "random",
          "serverNames": [""]
        }
      }
    },
    {
      "tag": "xHTTP_DE-01",
      "port": 2023,
      "listen": "127.0.0.1",
      "protocol": "vless",
      "settings": {"clients": [], "decryption": "none"},
      "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
      "streamSettings": {
        "network": "xhttp",
        "xhttpSettings": {"path": "/api/v1/stream/events"}
      }
    },
    {
      "tag": "WS_DE-01",
      "port": 2063,
      "listen": "127.0.0.1",
      "protocol": "vless",
      "settings": {"clients": [], "decryption": "none"},
      "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
      "streamSettings": {
        "network": "ws",
        "wsSettings": {"path": "/api/v2/stream/events"}
      }
    }
  ],
  "outbounds": [
    {"tag": "DIRECT", "protocol": "freedom"},
    {"tag": "BLOCK", "protocol": "blackhole"}
  ],
  "routing": {
    "rules": [
      {"ip": ["geoip:private"], "type": "field", "outboundTag": "BLOCK"},
      {"type": "field", "domain": ["geosite:private"], "outboundTag": "BLOCK"},
      {"type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK"}
    ]
  }
}
```

## Гайд: vless selfsteal через Caddy (Egor, 09.12)
- **[id=96262..96276|Egor|09.12](https://t.me/c/2941121338/96262)** Скрипт `DigneZzZ/remnawave-scripts` → раздел «Caddy selfsteal for Reality»:
  - Направить поддомен на сервер с нодой, запустить скрипт, ввести домен.
  - Xray JSON инбаунд: port 443, `xver: 1`, `target: 127.0.0.1:9443` (там Caddy), shortIds/privateKey/serverNames от вашего домена.
  - В ремне создать конфиг (профиль): заполнить shortIds, privateKey, serverNames; создать хост, в адрес — домен = serverNames.
  - Генерация на ноде:
```
docker exec <container_id> xray x25519 && openssl rand -hex 8
```
  (privateKey — первый вывод, shortIds — последний вывод hex).
  - В routing конфига пример с блокировкой рекламы ютуба и прямой на youtube (domain:youtube.com, youtubei.googleapis.com, ggpht.com, ytimg.com, googleapis.com → DIRECT; doubleclick/pagead/googlesyndication → BLOCK), плюс BLOCK на geoip:private, geosite:private, bittorrent.
  - Ссылка на шаблон mihomo от SawGoD: https://github.com/SawGoD/mihomo-rule-sets/blob/main/full_template.yaml

## Скрипты проверки/бенчмарка серверов
- **[id=93499|Egor|07.12](https://t.me/c/2941121338/93499)** Дословно:
```
# Проверка IP сервера на блокировки зарубежными сервисами:
bash <(curl -Ls IP.Check.Place) -l en
# Параметры сервера и проверка скорости к российским провайдерам:
wget -qO- bench.gig.ovh | bash
wget -qO- bench.tlab.pw | bash
# Параметры сервера и проверка скорости к зарубежным провайдерам:
wget -qO- bench.sh | bash
wget -qO- speed.tlab.pw | bash
# Проверка блокировки аудио в Instagram:
bash <(curl -L -s https://bench.openode.xyz/checker_inst.sh)
# YABS (диск, сеть iperf3, GeekBench):
curl -sL yabs.sh | bash -s -- -4
# IP Region (какой регион видит сайт по IP):
bash <(wget -qO - https://github.com/vernette/ipregion/raw/master/ipregion.sh)
bash <(wget -qO- https://ipregion.xyz)
# CensorCheck, проверка блока по DPI (для российских серверов):
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode dpi
# Процент CPU, выделенный хостером:
sysbench cpu run --threads=1
```
- **[id=93514|Никита|07.12](https://t.me/c/2941121338/93514)** Установка speedtest CLI:
```
wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz
tar -xf ookla-speedtest-1.2.0-linux-x86_64.tgz
./speedtest
```

## Полезные репозитории и ссылки (от BedolagamNaPivoBot, много раз)
- remnawave/panel (основной)
- BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot
- kutovoys/xray-checker
- eGamesAPI/remnawave-reverse-proxy
- Jolymmiels/remnawave-telegram-shop
- machka-pasla/remnawave-tg-shop
- DigneZzZ/remnawave-scripts
- distillium/remnawave-backup-restore
- maposia/remnawave-telegram-sub-mini-app
- legiz-ru/my-remnawave
- **[id=93414|Egor|07.12](https://t.me/c/2941121338/93414)** Уязвимость в React в miniapp → обновиться до https://github.com/maposia/remnawave-telegram-sub-mini-app/releases/tag/v2.2.5
- **[id=92847|Egor|06.12](https://t.me/c/2941121338/92847)** Реестр РКН: https://github.com/kutovoys/ru_gov_zapret ; инструкция с обновлением: https://docs.rw/docs/learn/zapret-ru-gov . Скачивать файл и обновлять раз в сутки шедулером (id 92858).
- **[id=93545|Bangtott|07.12](https://t.me/c/2941121338/93545)** Просмотр категорий geoip.dat: https://jomertix.github.io/geofileviewer
- **[id=91070|Евген|06.12](https://t.me/c/2941121338/91070)** Роутинг для клиентов: https://github.com/frayZV/simple-ru-routing
- **[id=96098|—|09.12](https://t.me/c/2941121338/96098)** Страница подписки: https://docs.rw/docs/install/subscription-page/bundled

## Xray Checker настройка
- **[id=94876..94900|LeX|08.12](https://t.me/c/2941121338/94876)** docker-compose:
```yaml
services:
  xray-checker:
    image: kutovoys/xray-checker
    environment:
      - SUBSCRIPTION_URL=
    ports:
      - "2112:2112"
```
В `SUBSCRIPTION_URL` — ссылка подписки специально созданного юзера (без лимита HWID, безлимитный трафик, даты — id 94882, 94883, 94899). HWID работает только при получении подписки — прямые ссылки убивают проверку HWID.

## SNI для белых списков (Zavulon, бесплатно)
- **[id=92623|Zavulon|06.12](https://t.me/c/2941121338/92623)** Выкладывает бесплатно:
```
мегафн тмобайл билайн сни ads.x5.ru
ёта МТС сни io.ozone.ru
билайн мтс ростелеком сни eh.vk.com
тмобайл т2 сни sun6-22.userapi.com
всё на яндекс клауде
```
IP на Yandex Cloud: 158.160.197.205 и 158.160.190.229 (потом добавлял). Там обычный reality на TCP. Оговорка других: подсеть 158.x "не работает" (id 92638-92639) — YC может давать другие IP; ТСПУ сетевые настройки меняют, SNI может отвалиться (VoidSignal). Замечание Aeg: продавал подобные услуги; Haxonate предлагает помощь сделать белые списки на всех операторах.

## Опыт хостеров
- **dhost** (dhostVPS_bot): Нидерланды 10 Гбит/с, недорого; но банят сервер при длительной нагрузке >500 Мбит/с (защита от DDoS) — история DeadIce 08.12, DHOST Admin объясняет: канал 10 Гбит на узле, гарантированная скорость 5-6 Гбит/с, трафик безлимит; лимит повышается по запросу. Возврат с комиссией на клиенте.
- **play2go**: режут скорость до 100 Мбит/с после 10 ТБ в месяц на ноду (id 95717, 95725); можно купить гарантированный Гбит/с за +95 евро.
- **aeza**: у всех нод 100 Мбит/с (пишут), Германия/Швеция/Финляндия у некоторых ок, но кто-то не любит (Genik: "взял сегодня США, шляпа по 100"). Аеза — bestof the worst но и bad: у Алексея сервера встали (id 90243, 91092), у SawGoD сервер лёг (08.12), у Mr L. удалили поддомен. Аеза требует удалить VPN с серверов RU (id 94838-94853).
- **u1host** — частые разрывы (id 93412).
- **senkodigital** — Германия хорошая, SawGoD получает 1 Гбит/с по VPN (id 93530).
- **infomaniak** — Швейцария, верификация легко проходится (id 95930, 95870).
- **firstbyte.ru** — стабильный (id 94148).
- **timeweb.cloud**, **beget.com** — Егор рекомендует для панелек (id 94826, 94830).
- **vaicore** (Evgeniy) — сервера ещё нет, скоро.
- **хостинг для панели на домашнем сервере** vs VPS: спор, но 900 платных подписок тянут на VPS; bил/gii "биил" жаловался (id 91255).
- **reg.ru** домены без паспорта (старый аккаунт 2012). `.ru/.рф/.su` по закону через паспорт (свежий закон ~2020, id 95901-95906). `.com` на reg.ru — 1600 руб, брал IS.
- **safedomainsbot** (`https://t.me/safedomainsbot`) — регистрация доменов из Telegram, у 17 домены в панельке работают 2 месяца (id 95750).
- **cp.regway.com** — регистрация доменов без паспорта (id 95812).
- **dynadot.com** — зарубежка/крипта (id 95769).
- **sweb.ru** с паспортом, **luxhost.cc** анонимно (id 95687).
- Панель + бот на 1 тачке — можно, но не стоит для большого проекта (id 94774-94776, 94802-94811); ноды отдельно.
- Бот/панель/ноды мигрировать: бот 5 мин, панель 10 мин (id 94116-94122).

## Балансировка нагрузки между нодами
- **[id=92863|R0xTaDDy|06.12](https://t.me/c/2941121338/92863)** DNS-балансировка — обычный round-robin, не переключает на менее загруженный.
- **[id=92868|IS|06.12](https://t.me/c/2941121338/92868)** Можно на уровне ядра, но не знает как.
- **[id=96365..96399|09.12](https://t.me/c/2941121338/96365)** С двумя серверами США DNS не даёт 50/50, раскидывает рандомно (иногда 80/20). Решения: Cloudflare (нужно включить прокси), в Xray `balancer` с режимом `roundrobin` (50/50) или `leastload` (мост, заблокированные хосты → глобальная нода).
- **[id=96425|Egor|09.12](https://t.me/c/2941121338/96425)** ishosting упоминается.

## Безопасность / DDoS
- **[id=93547|Egor|07.12](https://t.me/c/2941121338/93547)** Группа вымогателей кладёт проекты со слабой защитой (третья неделя). Убрать упоминания сервиса из профиля/ника, не делиться ссылками; панель прятать, на страницу подписки вешать защиту (Cloudflare), займитесь минимальной серверной защитой.
- **[id=93556|—|07.12](https://t.me/c/2941121338/93556)** Дудос от "щколоты со сттресером"; хостерская защита отрабатывала; nginx на нодах забирал память и крашился.
- **[id=93584|—|07.12](https://t.me/c/2941121338/93584)** В 3x-ui чатах — дно (доносы в РКН, дудосы, взломы по ssh).
- **[id=93597|Haxonate|07.12](https://t.me/c/2941121338/93597)** Продажа панели/бота на 3x-ui стоит 2к долларов.

## События/факты
- **[id=91093|Ozama|06.12](https://t.me/c/2941121338/91093)** Яндекс Клауд + ТСПУ: YouTube перестал работать (даёт ошибку «видео не доступно»).
- **[id=90956..90959|07.12](https://t.me/c/2941121338/90956)** Финляндия/Нидерланды hostvds: по 100 Мбит/с, проблем нет; Латвия — куча потерь, 100 у чата.
- **[id=90523|17|06.12](https://t.me/c/2941121338/90523)** Германия и Швеция — топ по цене/качеству у hostvds.
- **[id=93520|Egor|07.12](https://t.me/c/2941121338/93520)** Панель и бот на одном хосте: бот+панель+miniapp+nginx+нода на одном VPS — «делать не надо» (для критики), но у многих так.
- **[id=91197|17|06.12](https://t.me/c/2941121338/91197)** Стартовые цены: «Дзен-хост, Нидерланды 300р/мес, Франция 775р, Германия 1481р» (это то, что увидел).
- **[id=95849|/ suzi //|08.12](https://t.me/c/2941121338/95849)** Полная настройка сервиса (панель+ноды+бот) — 30 TON, предлагали в чате; Haxonate жёстко «10 баксов за 50 нод» как троллинг.
- **[id=92597..92767|06.12](https://t.me/c/2941121338/92597)** Реклама в Roblox-каналах: rb1 — залиться первому, rb2 — рассылка по боту 4к активных (деньги небольшие но приходит), rb3 — залить на следующий день после бана.
- **[id=92786|—|06.12](https://t.me/c/2941121338/92786)** «из 693 триалов 9 конверсий» (плохая конверсия).
- **[id=91745|SawGoD|06.12](https://t.me/c/2941121338/91745)** О ценообразовании: цена 300-500р за 10 серверов норм; SawGoD сам 350р за 7 серверов и +200р за премиум-сервер.
- **[id=91752|Egor|08.12](https://t.me/c/2941121338/91752)** Бот/панель/нода обновление панели 10 мин, бота 5 мин; миграция панели сложнее (Caddy/домен, БД Postgres, первый раз 10 ч с миграцией с 3x-ui, потом 10 мин).
- **[id=93991|—|07.12](https://t.me/c/2941121338/93991)** Миграция Remnawave: панель 10 мин, бот 5 мин, ноды работают независимо от панели.

## Прочее
- **[id=91086|—|06.12](https://t.me/c/2941121338/91086)** Сопутствующее: rabbitmq "где сервера Франции, Беларуси?" — конверсия в логах.
- **[id=95959|08.12](https://t.me/c/2941121338/95959)** WARP через wireproxy soc5 ест 1.7 ГБ ОЗУ — многовато.
- **[id=91280|—|06.12](https://t.me/c/2941121338/91280)** Мониторинг: Grafana (SawGoD), Prometheus, Beszel (легкий, микросервисы).
- **[id=96046|—|08.12](https://t.me/c/2941121338/96046)** WARP по локалкам: «шведка как» — геобаза не понравилась, остальное ок.
- **[id=92879|—|06.12](https://t.me/c/2941121338/92879)** Уведомления бота про покупку: «проникновение бота в чужой бот» — игнорировать, см. вопрос выше.
- **[id=93699|—|09.12](https://t.me/c/2941121338/93699)** Реферальные выплаты: 25% + 100р за первое пополнение, вывод в USDT (id 94162).
- **[id=91009|17|05.12](https://t.me/c/2941121338/91009)** «Сарафанка мертва для маленьких проектов», LTV клиента 5-8 мес в среднем, пробный в пей 15% конверсии — молодец, 40% нереально (id 89738-89755).
- **[id=89745|—|05.12](https://t.me/c/2941121338/89745)** Если цена подписки 100р, а пробка 100р и конверсия 10% — банкротишься.
- **[id=89752|—|05.12](https://t.me/c/2941121338/89752)** Платный триал — только для ИП (для маркетинга).
