# Заметки из chunk_095 (id 635495..644635, 04.06.2026 .. 05.06.2026)

## Волна блокировок 04.06–05.06.2026 (массовый отвал VLESS/TCP)
- **[639113|Honey M.|04.06]** Вечером упала половина нод; селфстил, смена fp, транспорта, сни не помогают.
- **[639264|—|04.06]** Финка 2 ноды и 2 нидерландца ушли; другие протоколы на тех же серверах поднимаются — это работа ТСПУ.
- **[639229|yng dev Zover|04.06]** Мост через Германию работает, мост через Россию — не работает.
- **[641683|—|05.06]** Волна утренняя 05.06: у Nodehost айпишники не заблокировали («рКН поняли, что ей пользоваться не будут»); у прочих ноды пингуются, но при подключении интернет умирает.
- **[642460|Руслан И.|05.06]** Новый уровень блокировок: прямое подключение к ру-ноде таймаутит, а редирект на ру-ноду со всех иностранных нод (в т.ч. Казахстан) работает.
- **[643295|Данил|05.06]** ТСПУ начали блокировать прокси-сервера методом активного спуфинга: перехватывают TLS-рукопожатие и подсовывают клиенту настоящий сертификат маскировочного сайта, из-за чего Xray аварийно рвёт соединение в целях безопасности.
- **[644289|whereareyou|05.06]** В логах Xray: REALITY: received real certificate (potential MITM or redirection) — ТСПУ подсовывает серт реального сайта, Xray видит MITM → разрыв.
- **[643462|compact disc|05.06]** В ядре Xray убрали allowInsecure — сертификат должен совпадать с прописанным SNI; см. verifyPeerByCertName.
- **[643309|—|05.06]** AmneziaWG v2 пока работает (шлёт мусор); смена порта не помогает, кроме 445 (и тот периодически сбоит).
- **[643333|Dmitry|05.06]** VLESS/TCP/REALITY и VLESS/XHTTP/REALITY задышали с ALPN h2,http/1,1 и отпечатком qq.
- **[643524|Ян|05.06]** 3 ноды отлетели одномоментно; остался рабочим единственный профиль, где нода шла через другую ноду (каскад).
- **[642701|—|05.06]** Проблема решилась настройкой fingerprint: заработали randomized и firefox — «для подключения к русским нодам она тоже нужна».
- **[643011|—|05.06]** В Ингушетии работали только обходы; **[642996|Gorec|05.06]** в Дагестане все VPN сдохли, обход CDN тоже моросит.
- **[642631|Урна|04.06]** Финляндия по wifi: на компе Германия пашет, с телефона пингуется, но не грузит.

## Детект/обходы
- **[636030|—|04.06]** xhttp грузит машины сильнее — там утечка памяти; hейлы рекомендуют не использовать xhttp.
- **[635540|search|04.06]** Hysteria2: если телефон заблокирован на какое-то время, хистерия отваливается у пользователя, заводится снова через ~20 сек (поведение в happ и incy одинаковое).
- **[635838..635875|Frist/—|04.06]** Hysteria: пинг ниже, быстрее; работает на http/3, который замедляют; в Иране/Китае прибили UDP. Хистерию ставить как альтернативу, если влесс отъехал; чисто для геймеров.
- **[647201|—|04.06]** Про переменные-«шляпы» (не найдено в чанке) — нет данных.
- **[636091..636115|—|04.06]** WARP: нужен, чтобы геобазы считали тебя нужной страной (пример: IP финский, для Google мы в Финке); варп не убирает рекламу ютуба, он подстраивает геобазы; Cloudflare-выходы варпа стоят в Финляндии.
- **[636113|Frist|04.06]** Ремна-сервис для настроек/скачивания варпа: https://github.com/Capybara-z/RemnaSetup
- **[636115|—|04.06]** Шаблоны аутбаундов варпа: https://github.com/distillium/warp-native/blob/main/README_ru.md
- **[636249|yng dev Zover|04.06]** Борьба с торрентами: tblocker плагин, рулы на ноде, рулы в JSON клиент, утилита tblocker.
- **[636040|Ранзай Р.|04.06]** Проблема, что ios (Happ/v2raytun) сами отключаются, ютуб тормозит — обсуждали, что из-за роутинга (конфиг ниже).
- **[636063|Frist|04.06]** В конфиге клиента вместо яндексовского DNS советуют простые 1.1.1.1 и 1.0.0.1.
- **[636380|—|04.06]** DNS с AdGuard (94.140.14.14/15 + DoH) для блокировки рекламы:
  ```json
  "dns": {
    "servers": [
      "94.140.14.14",
      "94.140.15.15",
      { "address": "https://dns.adguard-dns.com/dns-query" }
    ],
    "queryStrategy": "UseIPv4"
  }
  ```
  **[636387|Frist|04.06]** AdGuard не убирает рекламу ютуба; реклама уходит только если гео IP ру (ютуб на ру сервере / через варп).
- **[636471|—|04.06]** Проверка «триггерных блокировок»: ipreg/ДПИ-детектор https://github.com/Runnin4ik/dpi-detector (советуют DarkDragonFlame [636471] и pupukich [636499]).
- **[640273|—|04.06]** Домен-зеркало доки Bedolaga: https://bedolagadev.mintlify.app/getting-started/quickstart (основной docs.bedolagam.ru лежал [638465]).
- **[640318|Константин К.|04.06]** Дока ремны: https://docs.rw/docs/awesome-remnawave
- **[642242|Дмитрий|05.06]** ТСПУ проверяют IP: так что банить листинг и город для обхода — как у Селектела.
- **[645556|ТОЧНА НЕ ВПН|05.06]** Хостинг объявляет: ТСПУ обновляет настройки у части провайдеров (Бегет, SpaceWeb, Datacheap, Timeweb), недоступность зависит от оператора/региона/браузера.
- **[644331|—|04.06]** Селектел уник: сетка 200/35 (вабного).
- **[646121|—|04.06]** Для ру хоста Cloudflare.
- **[640476|TUTTAM ADMIN|04.06]** Все запускается через CDN.

## Конфиги (дословно)

### Traefik-лейблы для Bedolaga bot /api через кабину [635595|Deleted Account|04.06]
```yaml
services:
  bot:
    networks:
      - remnawave-network  # Добавляем для связи с Traefik
      - bot_network        # Оставляем, чтобы бот видел БД и Redis
    labels:
      - "traefik.enable=true"
      # ДОБАВЛЕН Host. Теперь запросы идут ТОЛЬКО с этого домена на /api
      - "traefik.http.routers.bot-api.rule=Host(`cabinet.домен.ru`) && PathPrefix(`/api`)"
      - "traefik.http.routers.bot-api.entrypoints=https"
      - "traefik.http.routers.bot-api.tls=true"
      - "traefik.http.routers.bot-api.tls.certresolver=letsencrypt"
      - "traefik.http.middlewares.bot-strip.stripprefix.prefixes=/api"
      - "traefik.http.routers.bot-api.middlewares=bot-strip"
      - "traefik.http.routers.bot-api.priority=100"
      - "traefik.http.services.bot-api.loadbalancer.server.port=8080"
      # ВАЖНО: Указываем Traefik использовать правильную сеть
      - "traefik.docker.network=remnawave-network"
  cabinet-frontend:
    image: ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
    container_name: cabinet_frontend
    restart: unless-stopped
    depends_on:
      bot:
        condition: service_healthy
    healthcheck:
      disable: true
    networks:
      - remnawave-network
      - bot_network
    environment:
      - TZ=Europe/Moscow
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.cabinet-ui.rule=Host(`cabinet.домен.ru`)"
      - "traefik.http.routers.cabinet-ui.entrypoints=https"
      - "traefik.http.routers.cabinet-ui.tls=true"
      - "traefik.http.routers.cabinet-ui.tls.certresolver=letsencrypt"
      # ВАЖНО: Указываем внутренний порт контейнера (80)
      - "traefik.http.services.cabinet-ui.loadbalancer.server.port=80"
      - "traefik.docker.network=remnawave-network"
networks:
  remnawave-network:
    external: true
```

### Xray сервер: VLESS raw Reality + xhttp inbound (glue через unix socket) [635609|khanzele|04.06]
```json
{
  "log": { "loglevel": "warning" },
  "dns": { "servers": [ { "address": "https://dns.google/dns-query", "skipFallback": false } ], "queryStrategy": "UseIPv4" },
  "inbounds": [
    {
      "tag": "Dragon-FL-1",
      "port": 443,
      "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "raw",
        "security": "reality",
        "realitySettings": {
          "show": false, "xver": 1,
          "target": "/dev/shm/api-v1-edge.sock",
          "shortIds": ["f1bb493f8c789496"],
          "privateKey": "...",
          "serverNames": ["мой домен ноды"]
        }
      }
    },
    {
      "tag": "Dragon-FL-1-XHTTP",
      "listen": "/dev/shm/api-v1-edge.sock,0666",
      "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "xhttp",
        "sockopt": { "acceptProxyProtocol": true },
        "security": "reality",
        "xhttpSettings": { "host": "", "mode": "auto", "path": "/remote.php/dav/uploads" },
        "realitySettings": {
          "show": false, "xver": 1,
          "target": "/dev/shm/nginx.sock",
          "spiderX": "",
          "shortIds": ["a3f4c2d9e8b7016a"],
          "privateKey": "...",
          "serverNames": ["мой домен ноды"]
        }
      }
    }
  ],
  "outbounds": [
    { "tag": "DIRECT", "protocol": "freedom" },
    { "tag": "BLOCK", "protocol": "blackhole" }
  ],
  "routing": {
    "rules": [
      { "ip": ["geoip:private"], "outboundTag": "BLOCK" },
      { "domain": ["geosite:private"], "outboundTag": "BLOCK" },
      { "protocol": ["bittorrent"], "outboundTag": "BLOCK" }
    ]
  }
}
```

### VLESS TCP Reality с роутингом RU→ру-нода (ютуб без рекламы) [636062|P A R A D I S E🥭|04.06]
```json
{
  "log": { "loglevel": "warning" },
  "dns": {
    "servers": [
      { "address": "77.88.8.8", "domains": ["geosite:category-ru"], "expectIPs": ["geoip:ru"] },
      "1.1.1.1",
      "8.8.8.8"
    ],
    "queryStrategy": "UseIPv4"
  },
  "inbounds": [
    {
      "tag": "vless-fin-in",
      "port": 443,
      "listen": "0.0.0.0",
      "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "dest": "127.0.0.1:9443",
          "show": false, "xver": 1,
          "shortIds": ["50"],
          "privateKey": "123213",
          "serverNames": ["selfsteal"]
        }
      }
    }
  ],
  "outbounds": [
    { "tag": "DIRECT", "protocol": "freedom" },
    { "tag": "BLOCK", "protocol": "blackhole" },
    {
      "tag": "RU_VLESS",
      "protocol": "vless",
      "settings": {
        "vnext": [ { "port": 443, "users": [ { "id": "17131271-5bcb-438b-b170-7953adf7e4c7", "flow": "xtls-rprx-vision", "encryption": "none" } ], "address": "ru.selfsteal" } ]
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "shortId": "",
          "publicKey": "123123",
          "serverName": "ru.selfsteal",
          "fingerprint": "chrome"
        }
      }
    }
  ],
  "routing": {
    "rules": [
      { "ip": ["geoip:private"], "outboundTag": "BLOCK" },
      { "domain": ["geosite:private"], "outboundTag": "BLOCK" },
      { "protocol": ["bittorrent"], "outboundTag": "BLOCK" },
      {
        "domain": ["geosite:category-ru","geosite:yandex","geosite:vk","geosite:youtube","geosite:google"],
        "outboundTag": "RU_VLESS"
      },
      { "inboundTag": ["vless-fin-in"], "outboundTag": "DIRECT" }
    ],
    "domainStrategy": "AsIs"
  }
}
```
- **[636072|Frist|04.06]** Правильно: EU > RU (зарубежная нода → ру-нода), а не наоборот; ру-нода — аутбаунд, ютуб идёт на ру.

### GRPC inbound для теста моста [636230|undr|04.06]
```json
{
  "tag": "GRPCTEST",
  "port": 2345,
  "protocol": "vless",
  "settings": { "clients": [], "decryption": "none" },
  "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
  "streamSettings": {
    "network": "grpc",
    "security": "reality",
    "grpcSettings": { "serviceName": "LvlAppSync" },
    "realitySettings": {
      "dest": "gateway.icloud.com:443",
      "show": false, "xver": 0,
      "shortIds": ["XXXXX"],
      "privateKey": "XXXXX",
      "serverNames": ["gateway.icloud.com","mask-api.icloud.com"]
    }
  }
}
```

### VLESS raw Reality (target st.ozone.ru) + grpc инбаунд [636346|khanzele|04.06]
```json
{
  "log": { "loglevel": "warning" },
  "dns": { "servers": [ { "address": "https://dns.google/dns-query", "skipFallback": false } ], "queryStrategy": "UseIPv4" },
  "inbounds": [
    {
      "tag": "Dragon-FL-1",
      "port": 443,
      "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "raw",
        "security": "reality",
        "realitySettings": {
          "show": false, "xver": 0,
          "target": "st.ozone.ru:443",
          "shortIds": [""],
          "privateKey": "…",
          "serverNames": ["st.ozone.ru"]
        }
      }
    },
    {
      "tag": "Dragon-FL-1-GRPC",
      "port": 443,
      "listen": "0.0.0.0",
      "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "grpc",
        "security": "none",
        "grpcSettings": { "serviceName": "vless" }
      }
    }
  ],
  "outbounds": [
    { "tag": "DIRECT", "protocol": "freedom" },
    { "tag": "BLOCK", "protocol": "blackhole" }
  ],
  "routing": {
    "rules": [
      { "ip": ["geoip:private"], "outboundTag": "BLOCK" },
      { "domain": ["geosite:private"], "outboundTag": "BLOCK" },
      { "protocol": ["bittorrent"], "outboundTag": "BLOCK" }
    ]
  }
}
```

### Часть Bedolaga .env (минимал) [642488|c0mrade|05.06]
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
- **[642481|Артем|05.06]** Совет: ставьте чистый минимальный env и добавьте строчку для кабины; тогда всё остальное настраивается в веб-админке.

### VLESS_xhttp инбаунд под CDN (selfsni) [643695|Dmitry|05.06]
```json
{
  "tag": "vless_xhttp",
  "port": 443,
  "listen": "0.0.0.0",
  "protocol": "vless",
  "settings": { "clients": [], "decryption": "none" },
  "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
  "streamSettings": {
    "network": "xhttp",
    "security": "reality",
    "xhttpSettings": { "host": "", "mode": "auto", "path": "/" },
    "realitySettings": {
      "dest": "мой домен:443",
      "show": false, "xver": 0,
      "shortIds": ["6f","4g6f"],
      "privateKey": "приватный ключ",
      "serverNames": ["мой домен"]
    }
  }
}
```
- **[643714|Dmitry|05.06]** shortIds можно попросить у ИИ сгенерить, но по правилам примера.

### VLESS WS + nginx (подарок чата) [647996|Wyatt H.|07.06] — реально в чанке 096, id 647996 — но сообщение в 095-м диапазоне? — Нет, id 647996 > 644635, это chunk_096. Не сюда.

## Хостеры/опыт
- **[635599|Мдооо|04.06]** Финляндия p2go lowcost 180₽/мес, IP пару раз меняют бесплатно.
- **[635802|—|04.06]** Оверселл на p2go похоже: 6 человек и уже красное.
- **[635903|Schwarz|04.06]** IHC (Интернет Хостинг Центр): дедик 8 ядер Xeon + 32GB RAM, 30ТБ трафика/мес, дальше 800р/1ТБ, канал 1 гбит/с; VPS IHC 4/8 и 6/12, 2ТБ, дальше 800р/1ТБ, канал 500-1000 Мбит/с.
- **[636810|Support|04.06]** Продажа IHC ВМ с БС-IP (46.254.16/17, 91.218.231, 37.143.14), цены 35к–55к руб; аккаунт RUvDS с 8 ВМ и 13 БС-IP (Казань) — 30к.
- **[636525|poly|04.06]** Node Host — ужасные аптаймы, проблемы с сетью, тикеты висят с мая.
- **[636527|Creed Aventus|04.06]** Node Host: взял на месяц, скачал и не работает, ТП молчит.
- **[637318|Roman S.|04.06]** Express Hosting: худший за последнее время в Нидерландах; два ядра Ryzen 9 9950X улетают под 100% от 25 человек; Польша с такими же параметрами всё ок.
- **[638566..638596|yng dev Zover|04.06]** ExpressHost: старые подсети 154.83.129.* в бан; в Европе IP доступны, сами сервера работают штатно; SSH работает.
- **[638599|—|04.06]** Экспресс-подсети в РФ вынесли в январе 2026, заносили в октябре 2025; Кента не коснулось.
- **[637571|—|04.06]** Hetzner: РКН новую подсеть хетзника в бан отправила; на федералках хетзнер больше года не работает; есть мнение, что масс-бана не было, только проёбавшиеся.
- **[636216|—|04.06]** Aeza: ASN банят целиком; 2025 год, апрель — юрку выебли, маршруты потом вылечили (у Aeza финку можно взять).
- **[636424|yng dev Zover|04.06]** Aeza MSKs-1 (1/2) 25 Гбит/с 5.93 EUR/мес — ipv6 стоит отключить; проверка по TSPU 16-20; достучаться можно, но до ютуба сомнительно; ipreg пробил.
- **[637530|Михаил|04.06]** Aeza MSKs-1 (1/2), 25 Гбит/с, 5.93 EUR/m, ipv6 стоит отключить; тесты ТСПУ 16-20: https://t.me/c/2941121338/649/636478?single
- **[638478|—|04.06]** Даблы (doubleservers.com) — Польша, Warsaw, 9 EUR/мес (1 vCPU/2GB/20GB NVMe, до 1 гбит/с): идеальное ГЕО, все сервисы определяются как нужно; IPv6 выключен, BBR включен; #рекомендую.
- **[639427|YukiOff1cial|04.06]** Nodehost Швеция/Германия не работают; подсеть 45.138.215.0/24.
- **[639454|YukiOff1cial|04.06]** Nodehost 2.27.12.0/24 — одна из худших сеток.
- **[637539|yng dev Zover|04.06]** Datagio: DE-2 (2/4/60) Ryzen 9 9950X, 1 Гбит/с, 540₽/мес — выдал сервер под тесты; айпишники чистые, нода пустая, скорости хорошие.
- **[637756|yng dev Zover|04.06]** У datagio на узел входят две витухи по гигабиту максимум; **[637757|—|04.06]** сервер стоит в интерзионе (тир 3 ДЦ), DE-CIX на территории эквиникса.
- **[637809|—|04.06]** У datagio своя инфра: ру (своя), Германия — аренда (Interzone).
- **[638041|—|04.06]** У datagio своя сеть, реселлить можно смело.
- **[636425|mah1cul|04.06]** RuVDS: по подсетям (внутри) всё работает норм.
- **[636804|—|04.06]** Хостеры RU: IHC, hostvds — берём, проблем нет (IS: Hostvds беру, проблем нема).
- **[638341|yng dev Zover|04.06]** Ру VPS: selectel, беget, reg.ру.
- **[640009|—|04.06]** Швеция (hostvds).
- **[637571|—|04.06]** «У хостапа топовые ВМ, за свои деньги и без верифа» (undr), но hostup и OVH в 0 блок (undr [636199]).
- **[636205|undr|04.06]** Hostup (Полайтовый) — 4.5$ тест; OVH и Hostup в 0 блок [636199].
- **[636477|undr|04.06]** Cloudflare, dedik.io, nod host — «без мостов» перечислять можно долго (RiSSE [636479]).
- **[637007|—|04.06]** Play2go деградирует; п2г гбитная финка.
- **[637004|—|04.06]** Aeza и Play2go: панель и бот на отдельном сервере, в чате проясняли.
- **[636077|—|04.06]** Hostvds (беру, проблем нема).
- **[640025|—|04.06]** Fairyhosting Эстония (fairyhosting) — с Эстонией проблем, дедик за 5 минут отвечает (fairyhosting) — жопа (jopa vpn) / «fairyhosting купите на тест» — 5 минут отвечает.
- **[638566..638596|—|04.06]** fairyhosting дедик не запускают (хеуклер, 05.06).
- **[639766|хеуклер|04.06]** Сова (Blackmore): чёрный список не работает из-за смены IP.
- **[638806|KubVpn|04.06]** vdsina.com тоже умерла полностью.
- **[638459|Андрей Пугачев|04.06]** Если подписка добавилась до падения панели и панель упала не успев синхронизировать конфиг с нодами — ноды могут не знать о подписке и не пускать.
- **[638877|Sergey K.|04.06]** Отсутствие POST у Яндекс CDN — не обойти (Frist: никак [636406]).
- **[640064|—|04.06]** Аеза: у П2Г подсеть 45.138.215 улетела, 6 км с напелем.

## Бот/панель Bedolaga
- **[640086|P|04.06]** Happ provider-id платный: 20 бесплатно, 0.08$ (all users) — 0.12$ (active users) за клиента; 1000 users = 80–120$; пушки при 400$.
- **[640047|P|04.06]** Дока хаппа: https://happ.mintlify.app/technical-docs/provider-id
- **[644694|c0mrade|05.06]** Bedolaga Bot — обновление (50 коммитов, ~2550 строк новых тестов): безопасность аккаунтов (Google/Discord/Yandex нельзя молча утащить, вход через ТГ одноразовый и ограничен по времени), платежи/баланс (Tribute и Telegram Stars без двойных списаний, оплата Pal24 выбранным способом), автоплатёж и пополнение, колесо фортуны, подарки/пробный период/конкурсы, языки (RU/EN/UA/FA/ZH), стабильность (лимит запросов у платёжек).
- **[644698|c0mrade|05.06]** Bedolaga Cabinet — обновление (36 коммитов): новый хедер на десктопе, мобильная вёрстка, безопасность (подписанные ссылки на вложения тикетов, закрыта уязвимость с подменой ссылки в мини-аппе), аккаунты (объединение по почте с кодом-подтверждением), Happ TV на Apple TV, админка колеса, подарки и лендинги.
- **[640358|—|04.06]** Не ставьте панель+бота на один сервер (по опыту пару).
- **[641076|—|04.06]** bedolaga и хостер.

## Прочее
- **[641881|—|04.06]** Соксы/WG внутри России ещё живут (Sergey K.: и WG, и AWG спокойно живут).
- **[641401|—|04.06]** Проверка на бане РКН: https://cheburcheck.ru/ (и chebur.me [644640]).
- **[642128|Дмитрий Г.|05.06]** МTPROTO упал у всех (05.06 утро) — за вчера всё пахало.
- **[642259|oyphy|05.06]** Сервера пингуются, ничего не работает, в панели ремны всё норм.
- **[640796|—|05.06]** Hostoff.net: целый день ни один сервер не работает (Alex).
- **[641471|Andrey P.|05.06]** Домены: spaceship [650882|veloriia|06.06].
- **[643015|Subnet|05.06]** 1 цент (0.5).
- **[645075|—|05.06]** Скачал «База хостингов с сохранением».

(флуд: срачи вокруг Chara F./Frist о «ноде без рекламы ютуба», скам-истории, ддрары, продажи акков/уников — опущено)
