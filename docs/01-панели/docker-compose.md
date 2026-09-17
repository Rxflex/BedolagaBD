# Docker-compose: рабочие файлы — по периодам

<!-- KB:HEAD -->
[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Docker-compose**

◀ [Установка и обновление](установка-обновление.md) · [Env-переменные](env.md) ▶

> рабочие compose-файлы бота, панели, кабинета, сабпейджа

<details>
<summary>📑 <b>На этой странице</b> — 29 разделов</summary>

- [Период 23.08–07.09.2025 — Bedolaga v2.0.x–2.2.x, Remnawave 2.1.x](#период-230807092025--bedolaga-v20x22x-remnawave-21x)
- [Период 12.11.2025–01.01.2026 — Bedolaga v2.7–2.9.4, Remnawave 2.3–2.4](#период-1211202501012026--bedolaga-v27294-remnawave-2324)
  - [Бот отдельно (канонический 2.9.x)](#бот-отдельно-канонический-29x)
  - [Бот с панелью (external сеть панели)](#бот-с-панелью-external-сеть-панели)
  - [Subscription-page (отдельно / 2.4.4 с токеном)](#subscription-page-отдельно--244-с-токеном)
  - [Miniapp монтирование](#miniapp-монтирование)
  - [Caddy selfsteal для ноды (два порта)](#caddy-selfsteal-для-ноды-два-порта)
  - [SS+Privoxy для YooKassa (обход блокировки не-RU IP)](#ssprivoxy-для-yookassa-обход-блокировки-не-ru-ip)
- [Период 09.02–13.03.2026 — Bedolaga v3.9–3.32, Remnawave 2.6.x, Remnawave-admin 2.x](#период-090213032026--bedolaga-v39332-remnawave-26x-remnawave-admin-2x)
- [Период 16.03–06.04.2026 — Remnawave 2.7.x (breaking), Bedolaga v3.33–3.45](#период-160306042026--remnawave-27x-breaking-bedolaga-v333345)
- [Период 06–25.04.2026 — Bedolaga v3.45–3.52, Remnawave-admin 2.9–2.11](#период-0625042026--bedolaga-v345352-remnawave-admin-29211)
  - [Remnawave web-backend (dev) [id=394991|23.04.2026]](#remnawave-web-backend-dev-id39499123042026)
  - [Статика кабинета C + Caddy [id=380858|20.04.2026]](#статика-кабинета-c--caddy-id38085820042026)
  - [Перевод кабинета на сервер с сабкой [id=335462|07.04.2026]](#перевод-кабинета-на-сервер-с-сабкой-id33546207042026)
  - [tinyauth (nginx) [id=335456|07.04.2026]](#tinyauth-nginx-id33545607042026)
- [Период 25.04–15.05.2026 — Bedolaga v3.49–3.55, Cabinet 1.49–1.52](#период-250415052026--bedolaga-v349355-cabinet-149152)
- [Период 16.05–05.06.2026 — Bedolaga v3.56–3.58, Remnawave-admin 2.14](#период-160505062026--bedolaga-v356358-remnawave-admin-214)
- [Период 07–26.06.2026 — Bedolaga 3.60–3.61, Subscription-page 7.2.5/7.2.6](#период-0726062026--bedolaga-360361-subscription-page-725726)
  - [Subscription-page healthcheck](#subscription-page-healthcheck)
  - [Nginx vhost](#nginx-vhost)
- [Период 26.06–08.07.2026 — Remnawave 2.8.0, Bedolaga v3.61–3.62, Cabinet 1.59](#период-260608072026--remnawave-280-bedolaga-v361362-cabinet-159)
- [Период 08–20.07.2026 — Remnawave 2.8.1, Bedolaga v3.62–3.64, Cabinet 1.61](#период-0820072026--remnawave-281-bedolaga-v362364-cabinet-161)
- [Период 20–31.07.2026 — Bedolaga v3.66/3.67 + Cabinet 1.64 (рекурренты Platega/Lava)](#период-2031072026--bedolaga-v366367--cabinet-164-рекурренты-plategalava)
- [Период 31.07–09.08.2026 — Remnawave 3.0.0 (ломающий), Bedolaga v4.0.0, Cabinet 1.65](#период-310709082026--remnawave-300-ломающий-bedolaga-v400-cabinet-165)
  - [Структура сервисов](#структура-сервисов)
  - [Бэкап БД в Cloudflare R2 [id=1023171, id=1022797]](#бэкап-бд-в-cloudflare-r2-id1023171-id1022797)
  - [Удаление API-токенов (ручное) [id=1040792]](#удаление-api-токенов-ручное-id1040792)
- [Период 09–20.08.2026 — Remnawave 3.2.3/3.3.0, Bedolaga v4.1.0 (GeoCheck)](#период-0920082026--remnawave-323330-bedolaga-v410-geocheck)
- [Период 20–23.08.2026 — совместимость 2.8.x/3.2.2, GHCR, пин-борда](#период-2023082026--совместимость-28x322-ghcr-пин-борда)

</details>

---
<!-- /KB:HEAD -->

## Период 23.08–07.09.2025 — Bedolaga v2.0.x–2.2.x, Remnawave 2.1.x

- **Бот v2.4.2** [id=20203] — postgres15-alpine + redis7-alpine (`--maxmemory 256mb --maxmemory-policy allkeys-lru`), `bot: build:.` env `DOCKER_ENV`, `DATABASE_MODE:auto`, `TZ:Europe/Moscow`, volumes logs/data/locales/app-config.json/miniapp/vpn_logo.png, ports `WEB_API_PORT:8080`, `TRIBUTE:8081`, `YOOKASSA:8082`, `CRYPTOBOT:8083`, `PAL24:8084`, `WATA:8085`, `HELEKET:8086`, network `bot_network 172.20.0.0/16`.
- **Бот v2.6.x unified** [id=59948] — один порт `127.0.0.1:8080:8080`, healthcheck `curl -f http://localhost:8080/health/unified`, сеть `remnawave-network external 172.30.0.0/16` [id=33819,44812,60210].
- **Remnawave панель eGames** [id=43239] — `remnawave: network_mode: service:remnawave-scheduler`, scheduler `127.0.0.1:3000,3001`, db postgres16, redis valkey7.2, subscription-page `REMNAWAVE_PANEL_URL=http://remnawave-scheduler:3000 APP_PORT=3010`, nginx host.
- **Caddy** до unified: `webhook.domain.com { handle /tribute-webhook* {reverse_proxy localhost:8081} ... /yookassa-webhook→8082 /pal24→8084 /health→8081/health }` [id=7270,16788]; selfsteal `caddy:2.9.1 network_mode:host` [id=1784,22316]; Cloudflare DNS-challenge Dockerfile+Caddyfile [id=17404]; unified `api.domain.com {encode gzip zstd; @config path /app-config.json; reverse_proxy localhost:8080}` и `miniapp.domain.com + webhook.domain.com → remnawave_bot:8080` [id=58063,32140].
- **Nginx** Gy9vin вебхуки [id=17866]; MiniApp v2.4.2 `server { listen 80,443 ssl; root /var/www/remnawave-miniapp; location =/miniapp/app-config.json {CORS}; location /miniapp/ {proxy_pass http://remnawave_bot:8080/miniapp/} }` [id=20376,25458]; unified `upstream remnawave_bot_unified 127.0.0.1:8080` и YooKassa IP allow [id=55579,59948].

## Период 12.11.2025–01.01.2026 — Bedolaga v2.7–2.9.4, Remnawave 2.3–2.4

### Бот отдельно (канонический 2.9.x)
```yaml
services:
  postgres:
    image: postgres:15-alpine
    container_name: remnawave_bot_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-remnawave_bot}
      POSTGRES_USER: ${POSTGRES_USER:-remnawave_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secure_password_123}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"
    volumes: [postgres_data:/var/lib/postgresql/data]
    networks: [bot_network]
  redis:
    image: redis:7-alpine
    container_name: remnawave_bot_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes: [redis_data:/data]
    networks: [bot_network]
  bot:
    build: .
    container_name: remnawave_bot
    restart: unless-stopped
    depends_on: {postgres: {condition: service_healthy}, redis: {condition: service_healthy}}
    env_file: [.env]
    environment:
      DOCKER_ENV: "true"
      DATABASE_MODE: "auto"
      POSTGRES_HOST: "postgres"
      POSTGRES_PORT: "5432"
      REDIS_URL: "redis://redis:6379/0"
      TZ: "Europe/Moscow"
    volumes:
      - ./logs:/app/logs:rw
      - ./data:/app/data:rw
      - ./locales:/app/locales:rw
      - ./vpn_logo.png:/app/vpn_logo.png:ro
    ports:
      - "${WEB_API_PORT:-8080}:8080"
    networks: [bot_network]
networks:
  bot_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```
[id=101800]

### Бот с панелью (external сеть панели)
```yaml
services:
  bot:
    build: .
    networks: [remnawave-network]
networks:
  remnawave-network:
    name: remnawave-network
    external: true
```
[id=101833,68063] `REMNAWAVE_API_URL=http://remnawave:3000`.

### Subscription-page (отдельно / 2.4.4 с токеном)
```yaml
services:
    remnawave-subscription-page:
        image: remnawave/subscription-page:latest
        container_name: remnawave-subscription-page
        hostname: remnawave-subscription-page
        restart: always
        env_file: [.env]
        ports: ['127.0.0.1:3010:3010']
        networks: [remnawave-network]
networks:
    remnawave-network:
        driver: bridge
        external: true
```
[id=98367]
```yaml
  remnawave-subscription-page:
    image: remnawave/subscription-page:latest
    container_name: remnawave-subscription-page
    hostname: remnawave-subscription-page
    restart: always
    depends_on: {remnawave: {condition: service_healthy}}
    environment:
      - REMNAWAVE_PANEL_URL=http://remnawave:3000
      - SUBSCRIPTION_UI_DISPLAY_RAW_KEYS=true
      - APP_PORT=3010
      - META_TITLE="Remnawave Subscription"
      - META_DESCRIPTION="page"
      - REMNAWAVE_API_TOKEN=пупупу
    ports: ['127.0.0.1:3010:3010']
    networks: [remnawave-network]
    logging: {driver: 'json-file', options: {max-size: '30m', max-file: '5'}}
```
[id=137490] Панель от eGames — compose c postgres-18, `remnawave-nginx` host-режим, `remnawave-network` [id=68085].

### Miniapp монтирование
```yaml
volumes: ["/var/www/remnawave-miniapp:/miniapp:ro"]  # [id=79204]
./miniapp:/miniapp:ro       # [id=124041]
./miniapp:/app/miniapp:ro   # [id=124957]
```

### Caddy selfsteal для ноды (два порта)
```caddy
{
    https_port {$SELF_STEAL_PORT_TCP}
    https_port {$SELF_STEAL_PORT_XHTTP}
    default_bind 127.0.0.1
    servers {
        listener_wrappers {
            proxy_protocol { allow 127.0.0.1/32 }
            tls
        }
    }
    auto_https disable_redirects
}
:{$SELF_STEAL_PORT_TCP} { tls internal; respond 204 }
:{$SELF_STEAL_PORT_XHTTP} { tls internal; respond 204 }
http://{$SELF_STEAL_DOMAIN} { bind 0.0.0.0; redir https://{$SELF_STEAL_DOMAIN}{uri} permanent }
https://{$SELF_STEAL_DOMAIN} { root * /var/www/html; try_files {path} /index.html; file_server }
:80 { bind 0.0.0.0; respond 204 }
```
[id=94738] Мини-заглушка: `:9443 { tls internal { on_demand } respond 200 }` — target 9443, отдельная под каждую ноду [id=121817,121950].

### SS+Privoxy для YooKassa (обход блокировки не-RU IP)
```yaml
services:
  bot:
    image: your-bot-image
    environment:
      HTTP_PROXY: http://privoxy:8118
      HTTPS_PROXY: http://privoxy:8118
    networks: [remnawave-network]
  ss_tunnel:
    image: shadowsocks/shadowsocks-libev:latest
    container_name: ss_tunnel
    restart: unless-stopped
    command: > ss-local -s SS_SERVER_IP -p SS_SERVER_PORT -k "SS_PASSWORD" -m aes-256-gcm -l 1081
    networks: [remnawave-network]
  privoxy:
    image: caligari/privoxy:latest
    container_name: privoxy
    restart: unless-stopped
    volumes: [./privoxy.conf:/etc/privoxy/config:ro]
    networks: [remnawave-network]
networks:
  bot_network: {driver: bridge}
  remnawave-network: {external: true}
```
`privoxy.conf`:
```
listen-address 0.0.0.0:8118
toggle 1
enable-remote-toggle 0
allow 172.0.0.0/8
forward-socks5t /api.yookassa.ru/ ss_tunnel:1081 .
```
[id=81016,102457] Проверка: `docker run --rm -it --network remnawave-network curlimages/curl curl -x http://privoxy_yookassa:8118 -I https://api.yookassa.ru/v3/payments --max-time 20` → HTTP/2 401.

## Период 09.02–13.03.2026 — Bedolaga v3.9–3.32, Remnawave 2.6.x, Remnawave-admin 2.x

Базовый build кабинета:
```yaml
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
```
[id=217700]

Из образа:
```yaml
services:
  cabinet-frontend:
    image: ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
    container_name: cabinet_frontend
    restart: unless-stopped
    ports: ['${CABINET_PORT:-3020}:80']
    volumes: ['./cabinet-dist:/usr/share/nginx/html:ro']
```
[id=245525]

## Период 16.03–06.04.2026 — Remnawave 2.7.x (breaking), Bedolaga v3.33–3.45

- Эталон бота postgres 15-alpine/redis 7-alpine/nginx MTU 1350 healthcheck vpn_logo.png [id=281185].
- Кабина: `networks: bot_network external: true name: remnawave-bedolaga-telegram-bot_bot_network` [id=281060].
- Прокси налога compose: `HTTPS_PROXY: socks5://user:PASS@IP:1080; NO_PROXY: api.telegram.org,localhost,127.0.0.1,redis,postgres` + `serjs/go-socks5-proxy -p 1080` + httpx[socks] [id=282120; id=306223]; extra_hosts старый IP ломает [id=285327].

## Период 06–25.04.2026 — Bedolaga v3.45–3.52, Remnawave-admin 2.9–2.11

### Remnawave web-backend (dev) [id=394991|23.04.2026]
```yaml
web-backend:
    image: ghcr.io/case211/remnawave-admin-web-backend:dev
    container_name: remnawave-web-backend
    restart: unless-stopped
    init: true
    env_file:
      - .env
    environment:
      - WEB_HOST=0.0.0.0
      - WEB_PORT=8081
      - MAXMIND_CITY_DB=${MAXMIND_CITY_DB:-/app/geoip/GeoLite2-City.mmdb}
      - MAXMIND_ASN_DB=${MAXMIND_ASN_DB:-/app/geoip/GeoLite2-ASN.mmdb}
      - BACKUP_DIR=/app/backups
    volumes:
      - ./logs:/app/logs
      - ./geoip:/app/geoip
      - ./backups:/app/backups
    ports:
      - "${WEB_BACKEND_PORT:-8081}:8081"
    networks:
      - remnawave-network
    depends_on:
      remnawave-admin-db:
        condition: service_healthy
```

### Статика кабинета C + Caddy [id=380858|20.04.2026]
```caddy
https://cabinet.example.com {
    encode gzip zstd
    handle /api/* {
        uri strip_prefix /api
        reverse_proxy remnawave_bot:8080
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
# volumes:
#   - /opt/bedolaga-cabinet/dist:/srv/cabinet:ro
```

### Перевод кабинета на сервер с сабкой [id=335462|07.04.2026]
```caddy
https://sub.domen.top {
    reverse_proxy * http://remnawave-subscription-page:3010
}
:443 {
    tls internal
    respond 204
}
https://lk.domen.top {
    reverse_proxy https://lk2.domen.top {
        header_up Host lk2.domen.top
    }
}
```

### tinyauth (nginx) [id=335456|07.04.2026]
```nginx
location /tinyauth {
  proxy_pass http://tinyauth/api/auth/nginx;
  proxy_set_header Authorization $http_x_api_key;
  proxy_set_header x-forwarded-proto $scheme;
  proxy_set_header x-forwarded-host $http_host;
  proxy_set_header x-forwarded-uri $request_uri;
}
```

- Фикс сети контейнера: сеть remnawave-network + `REMNAWAVE_API_URL=http://remnawave:3000` [id=332529,333253].
- Зомби-процессы бота → `init: true` (tini) [id=382467].
- Порт 8080 открыт наружу → `127.0.0.1:` перед '${WEB...}' [id=388116].
- Dockge — управлялка docker-compose: https://github.com/louislam/dockge [id=357516].

## Период 25.04–15.05.2026 — Bedolaga v3.49–3.55, Cabinet 1.49–1.52

**Логи запуска бота 3.53.0** [id=429254]: сервисы — единый веб-сервер (8080/8082), Telegram webhook, служба мониторинга, суточные подписки (интервал 30 мин), проверка версий (repo=fr1ngg/remnawave-bedolaga-telegram-bot), NaloGO отключен.

**Реальный стек (docker ps)** [id=505794]: Caddy-контейнер + remnawave-bedolaga-telegram-bot + postgres:15-alpine + redis:7-alpine; бот Unhealthy.

**Пароль БД бота** в docker-compose.yml, дефолт `secure_password_123` [id=458809, 458813].

**Внешняя сеть для проброса webhook** [id=416498]:
```yaml
networks:
  remnawave-bedolaga-telegram-bot_bot_network:
    driver: bridge
    external: true
```

**Volumes гео/сертификатов (нода)** [id=462045]:
```yaml
volumes:
  - /var/log/remnanode:/var/log/remnanode
  - ./geoip_ru.dat:/usr/local/share/xray/geoip_ru.dat
  - ./geosite_ru.dat:/usr/local/share/xray/geosite_ru.dat
  - ./zapret.dat:/usr/local/bin/zapret.dat
  - /var/lib/remnawave/caddy/certificates:/certificates
```
**Сертификаты в xray** [id=462061]:
```json
"certificates": [
  { "keyFile": "/certificates/current.key", "certificateFile": "/certificates/current.crt" }
]
```

**cap_add** для WARP/xray: `cap_add: - NET_ADMIN` [id=427492].

**WEB_API_PORT (некритичный баг)** [id=443309]: в compose `ports: - '${WEB_API_PORT:-8080}:8080'` — если поставить в env 9095, хост-порт 9095 пробросится в контейнер, а приложение внутри смотрит 8080 и не увидит 9095.

**Несколько панелей на одном сервере**: можно хоть 10 — разные порты в nginx/caddy и контейнерах, сети docker разнести, чтобы не пересекались [id=446622, 446623]; «На 32 ядрах ставь хоть 30 панелек» [id=473760]; ремна + два бота на одном серваке на разных портах [id=446622].

**Перенос панели на другой сервер с NPM** [id=423873]: панель отвечает только по внутренней сети; надо подключить сеть ремнавейва к npm и проксировать по hostname (docker name, например `remnawave:3000`), а не 127.0.0.1 — «у тебя в контейнере локалхост свой, изолированный» [id=423736]. Официальная дока ремны nginx proxy manager не описывает [id=423822].

**Recompilation без докера** [id=440391]: `npm install && npm run build` напрямую на хосте — в докере tsc не устанавливается.

**bedolaga-mover** — перенос БД/конфигов/контейнеров, docker-контейнеры Bot + Bedolaga-cabinet + админка на одном сервере, поддержка Caddy, Ubuntu 24 [id=499253, 499253, 499254]. Ищемые пути: `/root/remnawave-bedolaga-telegram-bot`, `/opt/remnawave-bedolaga-telegram-bot`, `/home/*/...`, `/root/bedolaga-cabinet`, `/opt/remnawave-admin`.

**Гайд переноса Панели+БД** (автор Егор): https://telegra.ph/Perenos-Paneli--BD-na-novyj-server-05-11 — «скрипт distillium/remnawave-backup-restore дал ошибку, руками получилось быстрее» [id=492564].

---

## Период 16.05–05.06.2026 — Bedolaga v3.56–3.58, Remnawave-admin 2.14

- Traefik лейблы для бота /api через кабину [id=635595]:
```yaml
services:
  bot:
    networks:
      - remnawave-network
      - bot_network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.bot-api.rule=Host(`cabinet.домен.ru`) && PathPrefix(`/api`)"
      - "traefik.http.routers.bot-api.entrypoints=https"
      - "traefik.http.routers.bot-api.tls=true"
      - "traefik.http.routers.bot-api.tls.certresolver=letsencrypt"
      - "traefik.http.middlewares.bot-strip.stripprefix.prefixes=/api"
      - "traefik.http.routers.bot-api.middlewares=bot-strip"
      - "traefik.http.routers.bot-api.priority=100"
      - "traefik.http.services.bot-api.loadbalancer.server.port=8080"
      - "traefik.docker.network=remnawave-network"
  cabinet-frontend:
    image: ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
    container_name: cabinet_frontend
    restart: unless-stopped
    depends_on:
      bot:
        condition: service_healthy
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
      - "traefik.http.services.cabinet-ui.loadbalancer.server.port=80"
      - "traefik.docker.network=remnawave-network"
networks:
  remnawave-network:
    external: true
```
- Hysteria2 + certbot compose [id=647736]:
```yaml
services:
  certbot:
    container_name: certbot
    image: certbot/certbot
    network_mode: host
    volumes:
      - ./certs:/etc/letsencrypt
```
```bash
docker run --rm \
  -v $(pwd)/certs:/etc/letsencrypt \
  -v $(pwd)/var-lib-letsencrypt:/var/lib/letsencrypt \
  --network host \
  certbot/certbot certonly --standalone \
  --non-interactive --agree-tos \
  --email admin@your-domain.com \
  -d your-domain.com
```
В compose ноды:
```yaml
    volumes:
      - '/opt/certbot/certs:/etc/letsencrypt:ro'
```
Cron: `0 0 28 * * cd /opt/certbot && docker compose run --rm certbot renew`

## Период 07–26.06.2026 — Bedolaga 3.60–3.61, Subscription-page 7.2.5/7.2.6

### Subscription-page healthcheck
```yaml
healthcheck:
  test: curl -f http://localhost:3010/
```
depends_on remnawave service_healthy — на localhost иначе Reverse proxy required [id=659893]

### Nginx vhost
```nginx
location / { proxy_pass http://remnawave-subscription-page:3010; include /etc/nginx/conf.d/proxy.conf; }
```
[id=659893]

## Период 26.06–08.07.2026 — Remnawave 2.8.0, Bedolaga v3.61–3.62, Cabinet 1.59

- Эталон Caddy (панель/подписка/бот/заглушка) [id=755725]:
```caddy
https://panel.duckdns.org {
  encode gzip
  handle_path /monitoring* { reverse_proxy beszel:8090 }
  reverse_proxy /webhook* remnawave_bot:8080
  reverse_proxy remnawave:3000 {
    transport http { read_buffer 8192; write_buffer 8192 }
    flush_interval 500ms
  }
  header { -Server; Cache-Control "no-store" }
}
https://subscription.duckdns.org {
  encode gzip
  reverse_proxy remnawave-subscription-page:3010 {
    transport http { read_buffer 8192; write_buffer 8192 }
    flush_interval 500ms
  }
  header { -Server; Cache-Control "no-store" }
}
:443 { tls internal; respond 204 }
```
- Redis fix: `docker --unixsocketperm 777 --port 6379; healthcheck ['CMD','valkey-cli','-p','6379','ping'] interval 3s; REDIS_HOST=remnawave-redis, REDIS_PORT=6379` [id=755748]
- Бот+панель на одном сервере: в compose бота ports обязательно `127.0.0.1:8080`; лучше не держать вместе [id=757731]
- Сеть бота: бот создаёт свою сеть и не коннектится к remnawave [id=786360]; error Cannot connect to host remnawave:3000 — завести в одну сеть [id=758775]

- x1roko базовый config (4 инбаунда) [id=781565]:
```json
{
  "log": { "loglevel": "none" },
  "dns": { "tag": "dns_inbound", "servers": ["1.1.1.1","1.0.0.1","2606:4700:4700::1111","2606:4700:4700::1001"], "queryStrategy": "UseIP" },
  "inbounds": [
    { "tag": "Multi-Raw", "port": 443, "listen": "0.0.0.0", "protocol": "vless", "settings": { "clients": [], "decryption": "none" }, "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] }, "streamSettings": { "network": "raw", "security": "reality", "realitySettings": { "xver": 1, "target": "/dev/shm/nginx.sock", "shortIds": [""], "privateKey": "", "fingerprint": "", "serverNames": [""] } } },
    { "tag": "Multi-gRPC", "listen": "/dev/shm/grpc.socket,0666", "protocol": "vless", "settings": { "clients": [], "decryption": "none" }, "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] }, "streamSettings": { "network": "grpc", "security": "none", "grpcSettings": { "serviceName": "grpcpath" } } },
    { "tag": "Multi-XHTTP", "listen": "/dev/shm/xrxh.socket,0666", "protocol": "vless", "settings": { "clients": [], "decryption": "none" }, "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] }, "streamSettings": { "network": "xhttp", "xhttpSettings": { "mode": "auto", "path": "/xhttppath/", "extra": { "noSSEHeader": true, "xPaddingBytes": "100-1000", "scMaxBufferedPosts": 30, "scMaxEachPostBytes": 1000000, "scStreamUpServerSecs": "20-80" } } } },
    { "tag": "Multi-Hy2", "port": 443, "listen": "0.0.0.0", "protocol": "hysteria", "settings": { "clients": [], "version": 2 }, "streamSettings": { "network": "hysteria", "security": "tls", "finalmask": { "quicParams": { "debug": false, "congestion": "bbr" } }, "tlsSettings": { "alpn": ["h3"], "certificates": [{ "keyFile": "/etc/nginx/certs/privkey.key", "certificateFile": "/etc/nginx/certs/fullchain.pem" }] }, "hysteriaSettings": { "version": 2 } } }
  ],
  "outbounds": [ { "tag": "DIRECT", "protocol": "freedom" }, { "tag": "BLOCK", "protocol": "blackhole" }, { "tag": "warp", "protocol": "socks", "settings": { "servers": [{ "port": 40000, "address": "127.0.0.1" }] } } ],
  "routing": { "rules": [] }
}
```
Весь vless на 443/tcp, hy2 на 443/udp [id=781566]

## Период 08–20.07.2026 — Remnawave 2.8.1, Bedolaga v3.62–3.64, Cabinet 1.61

Дословных docker-compose-файлов в заметках 121–132 нет. Зафиксированы только compose-команды и факты про compose:
- `docker compose pull` + `docker compose up -d --build` — обновление бота [id=837220]; `docker compose up -d --build` — установка бедолаги [id=850467].
- Caddy: `cd /opt/reverse-proxy` + `docker compose exec caddy …` (см. выше) [id=840807, 852039].
- Имя сервиса бота в compose может отличаться от `remnawave_bot` — смотреть `docker-compose.yml` [id=840770]; при этом `docker restart remnawave_bot` — реальное имя контейнера бота [id=847895].
- Compose-файл ноды несёт панельные секреты; зафиксирован случай применения compose новой ноды к активной ноде из-за неротируемых секретов [id=862791..862855].
- Ноду в docker связке `docker compose down && docker compose up` (из гайда) критикуют как ненадёжную [id=911094, 911128].
- Бедолага-контейнер: после правок env обязателен перезапуск контейнера [id=867989].

---

## Период 20–31.07.2026 — Bedolaga v3.66/3.67 + Cabinet 1.64 (рекурренты Platega/Lava)

- Каноническая команда обновления кабинета:
  ```
  docker compose pull && docker compose up -d --build
  ```
  [id=1000760|bypara|30.07.2026]
- Remnawave-Xray-UI-Editor (установка дословно) [id=974370|Vladislav|26.07.2026]:
  ```
  curl -fsSLO https://raw.githubusercontent.com/VAQYBIN/Remnawave-Xray-UI-Editor/main/docker-compose.yml
  curl -fsSL -o .env https://raw.githubusercontent.com/VAQYBIN/Remnawave-Xray-UI-Editor/main/.env.example
  nano .env
  docker compose up -d && docker compose logs -f
  ```
- Скрипт nDPI + Suricata (не открытый код) [id=950368|moment|23.07.2026], будьте бдительны [id=950649|Zavulon]:
  ```
  curl -fsSL https://doubleservers.com/6eaygszz4o2yjlwfqs7lu5iw/k3coxnqhumw4fhcyzoh334hj -o ds-guard && chmod +x ds-guard && ./ds-guard
  ```

## Период 31.07–09.08.2026 — Remnawave 3.0.0 (ломающий), Bedolaga v4.0.0, Cabinet 1.65

### Структура сервисов
Сервисы: `bot`, `cabinet` (иногда `bedolaga-cabinet-frontend` в compose-файле) [id=1034989].

Для кабинета:
```yaml
services:
  cabinet-frontend:
    image: ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
    healthcheck:
      test: wget -q --spider http://127.0.0.1:80/
```
[id=1034611]

Если `no such service: cabinet` → искать `bedolaga-cabinet-frontend` [id=1034978, id=1034989].

### Бэкап БД в Cloudflare R2 [id=1023171, id=1022797]
Сохранение БД панели/бота в Cloudflare R2.

### Удаление API-токенов (ручное) [id=1040792]
```bash
docker exec -it remnawave-db sh -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "DELETE FROM api_tokens;"'
```
После перезапустить панель.

## Период 09–20.08.2026 — Remnawave 3.2.3/3.3.0, Bedolaga v4.1.0 (GeoCheck)

- /opt/remnanode/docker-compose.yml [id=1094514]; /opt/remnawave [id=1145027]; сервис remnawave [id=1106749]
- remnawave_bot_db remnawave_user remnawave_bot [id=1148751]
- billing-monitoring Docker/npm [id=1092782]

## Период 20–23.08.2026 — совместимость 2.8.x/3.2.2, GHCR, пин-борда

- Принудительная фиксация версии ноды в docker-compose при панели 2.8.0 — дословная формулировка из чата:
  ```
  2.8.0 с ластовой нодой не работает, пиши в docker-compose `3.2.2` вместо latest
  ```
  [id=1174272|23.08] (повтор дословно: «2.8.0 с ластовой нодой не работает, пиши в компоузе 3.2.2 вместо latest» — «точный фикс для панели 2.8») [id=1174256|23.08].
- Вариант того же фикса от bypara: в docker-compose **принудительно указать старую версию ноды и пуллить**; для панели **2.8.0** откатывать ноду на **v3.1.1** («последняя до глобальных изменений», совместима) [id=1157938|20.08], [id=1158072|21.08].
- После обновления Xray-ядра (xray 26.7.11 beta) «все пропало» — фикс-совет: **откатить версию ядра на нодах**; отдельная несовместимость: нода **3.3.0** не заведётся на панели **3.2.2** [id=1156884, id=1158134|21.08].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Docker-compose**

◀ [Установка и обновление](установка-обновление.md) · [Env-переменные](env.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
