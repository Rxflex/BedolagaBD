# Реверс-прокси: Caddy, Nginx, HAProxy, Traefik

<!-- KB:HEAD -->
[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **Реверс-прокси**

◀ [Firewall и анти-DDoS](firewall-ddos.md) · [Сертификаты](сертификаты.md) ▶

> Caddy, Nginx, HAProxy, Traefik — конфиги дословно

<details>
<summary>📑 <b>На этой странице</b> — 4 разделов</summary>

- [4.1 Caddy](#41-caddy)
- [4.2 Nginx](#42-nginx)
- [4.3 HAProxy](#43-haproxy)
- [4.4 Traefik](#44-traefik)

</details>

---
<!-- /KB:HEAD -->

Общий фон: caddy — «скопировал вставил», серты автоматом; nginx — модули/контроль [id=135101, 55501]. 443 — у обратного прокси; бот 8080, панель 3000, метрики 3001, сабка 3010 [id=135294]. Два прокси на одном сервере (nginx+caddy) не живут [id=83827]. nginx и бот обязаны быть в одной docker-сети, иначе `host not found in upstream "remnawave_bot"` [id=20376..20378].

## 4.1 Caddy
- Полная схема стека (мейн-сервер) [id=7270..7287]:
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
- Единый webhook-сервер бота (v2.6+): один порт 8080, пути `/yookassa-webhook`, `/platega-webhook`, `/cryptobot-webhook`, `/wata-webhook`, `/heleket-webhook`, `/tribute-webhook`, `/pal24-webhook`, `/mulenpay-webhook`, `/freekassa-webhook`, `/cloudpayments-webhook`, `/remnawave-webhook`; эталон Caddyfile c `(proxy_defaults)`: [id=324376|c0mrade, 226539]:
```
(proxy_defaults) {
    header_up Host {host}
    header_up X-Real-IP {remote_host}
    transport http { read_buffer 0 }
}

hooks.example.com {
    encode gzip zstd
    @webhooks {
        path /yookassa-webhook
        path /platega-webhook
        path /cryptobot-webhook
        path /wata-webhook
        path /heleket-webhook
        path /tribute-webhook
        path /pal24-webhook
        path /mulenpay-webhook
        path /freekassa-webhook
        path /cloudpayments-webhook
        path /remnawave-webhook
    }
    handle @webhooks { reverse_proxy remnawave_bot:8080 { import proxy_defaults } }
    handle /app-config.json {
        header Access-Control-Allow-Origin "*"
        reverse_proxy remnawave_bot:8080 { import proxy_defaults }
    }
    handle { reverse_proxy remnawave_bot:8080 { import proxy_defaults } }
}

cabinet.example.com {
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
- Канонический Caddyfile кабинета от Егора — с `import geoip_block` и теми же кеш-правилами [id=220889|12.02.2026]; вебсокет кабинета работает сам (`cabinet/ws сноси в caddy`) [id=226512]; wss-фикс [id=294843]: `handle /cabinet/ws* { reverse_proxy remnawave_bot:8080 }`.
- Selfsteal-заглушка Caddy [id=244529|27.02.2026]:
```
{
    https_port {$SELF_STEAL_PORT}
    default_bind 127.0.0.1
    servers { listener_wrappers { proxy_protocol { allow 127.0.0.1/32 } tls } }
    auto_https disable_redirects
}
http://{$SELF_STEAL_DOMAIN} { bind 0.0.0.0; redir https://{$SELF_STEAL_DOMAIN}{uri} permanent }
https://{$SELF_STEAL_DOMAIN} { root * /var/www/html; try_files {path} /index.html; file_server }
:{$SELF_STEAL_PORT} { tls internal; respond 204 }
:80 { bind 0.0.0.0; respond 204 }
```
`.env: SELF_STEAL_DOMAIN=subdomen.domen.ru, SELF_STEAL_PORT=9443`; docker-compose с `network_mode: "host"`; target ноды = `127.0.0.1:9443`, SNI = СВОЙ домен [id=653860..653903|08.06.2026].
- Caddy на два порта для xhttp+TCP selfsteal: `https_port {$SELF_STEAL_PORT_TCP}` + `https_port {$SELF_STEAL_PORT_XHTTP}` [id=94738|08.12.2025].
- Caddy DNS-challenge Cloudflare (wildcard без перетасовки) [id=17404|Danila Tsaplin|27.09.2025]:
```dockerfile
FROM caddy:2.9.1-builder AS builder
RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```
```caddy
{
    email {$EMAIL}
    acme_dns cloudflare {$CF_API_TOKEN}
    https_port {$SELF_STEAL_PORT}
    default_bind 127.0.0.1
    servers {
        listener_wrappers {
            proxy_protocol { allow 127.0.0.1/32 }
            tls
        }
    }
    auto_https disable_redirects
    log {
        output file /var/log/caddy/access.log {
            roll_size 10MB
            roll_keep 5
            roll_keep_for 720h
            roll_compression gzip
        }
        level ERROR
        format json
    }
}
```
- XHTTP за Caddy без селфстила (TLS у Caddy, Xray без шифрования) [id=651359|07.06.2026]:
```
yourdomain.com {
    handle /api* {
        reverse_proxy 127.0.0.1:8443 {
                flush_interval -1
                transport http { versions h2c 1.1 }
        }
    }
    respond "OK" 200
}
```
- Caddy для кабинета из README: `handle /api/* { uri strip_prefix /api; reverse_proxy remnawave_bot:8080 }` [id=173966].
- Пересборка caddy-security (защита/ratelimit/geolocation) [id=247708|01.03.2026]:
```docker
FROM caddy:2.10.2-builder AS builder
RUN xcaddy build \
    --with github.com/greenpau/caddy-security@v1.1.27 \
    --with github.com/caddy-dns/cloudflare \
    --with github.com/mholt/caddy-ratelimit \
    --with github.com/caddyserver/cache-handler@v0.16.0 \
    --with pkg.jsn.cam/caddy-defender \
    --with github.com/porech/caddy-maxmind-geolocation
FROM caddy:2.10.2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```
- Caddy reload ошибка `dial tcp 127.0.0.1:2019: connection refused` — рестартовать контейнер [id=169523]; в докере caddy слушает только localhost:9443 при селфстиле [id=213999].

## 4.2 Nginx
- Полный конфиг hooks+miniapp (дословно) [id=91677..91687|06.12.2025]:
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
# Miniapp domain
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
- Upstream — в основной nginx.conf, НЕ в conf.d (`events {} и http {} в default.conf запрещены`) [id=101409, 236397]:
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;
events { worker_connections 1024; }
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    upstream remnawave_bot { server 127.0.0.1:8080; }
    include /etc/nginx/conf.d/*.conf;
}
```
- Компактный конфиг вебхуков одной локацией [id=166475..166477]:
```nginx
client_max_body_size 32m;
location ~ ^/(webhook|.*-webhook|app-config\.json) {
    if ($request_uri ~* "/app-config.json") { add_header Access-Control-Allow-Origin "*"; }
    proxy_pass http://remnawave-bot;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 120s; proxy_send_timeout 120s;
    proxy_buffering off; proxy_request_buffering off;
}
```
- API-локация ремны с websocket-апгрейдом [id=154757]:
```nginx
location ^~ /api/ {
    proxy_http_version 1.1;
    proxy_pass http://remnawave;
    proxy_set_header Host $host;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Port $server_port;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```
- Кабинет за nginx: upstream обязателен вверху conf.d; `location /api/ { rewrite ^/api/(.*) /$1 break; proxy_pass http://remnawave_bot:8080; ... }`; фронт — `proxy_pass http://cabinet_frontend:80` c error_page 404 → /index.html [id=281060, 174773].
- Блок-кэш кабинета + статики [id=196643]:
```nginx
location ~* \.html?$ {
    add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
    expires -1;
    add_header Pragma "no-cache";
}
location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg)$ {
    expires 1y;
    access_log off;
    add_header Cache-Control "public";
}
```
- allowlist IP ЮKassa на реверсе [id=55579]:
```nginx
allow 185.71.76.0/27;
allow 185.71.77.0/27;
allow 77.75.153.0/25;
allow 77.75.154.128/25;
allow 77.75.156.11;
allow 77.75.156.35;
allow 2a02:5180::/32;
deny all;
```
(бот должен видеть реальный IP через X-Forwarded-For; в .env `YOOKASSA_TRUSTED_PROXY_NETWORKS=172.20.0.0/16` или подсети юкассы `185.71.76.0/24,185.71.77.0/24` [id=120591, 631299].)
- http2: `listen ... http2` deprecated → `http2 on;` [id=91744]; `server_names_hash_bucket_size 64;` при `could not build server_names_hash` [id=114513, 43804]; `ssl_reject_handshake on` на default_server для пустых SNI [id=91677].
- Один `upstream remnawave_bot_unified { server remnawave_bot:8080; }` на все хуки (после единого webhook-сервера 2.6) [id=59948]; локейшены `location = /yookassa-webhook` с `proxy_buffering off` [id=59948, 58789].
- nginx для xhttp (grpc_pass на unix-сокет) [id=338655]:
```nginx
location /xhttppath/ {
  client_max_body_size 0;
  grpc_set_header X-Forwarded-For;
  grpc_read_timeout 315;
  grpc_send_timeout 5m;
  grpc_pass unix:/dev/shm/xrxh.socket;
}
```
- nginx поток с `ssl_preread` для нескольких SNI на 443 [id=320791|Josh]: вход 443 → по SNI на сайт (127.0.0.1:4443) или в Xray (127.0.0.1:18443).
- nginx перезаписывает OPTIONS→POST (Tw CDN режет POST) [id=590049]: `map $request_method $proxy_method_override { default $request_method; OPTIONS POST; }`
- nginx переписывает poll-путь для старого ядра (26.7.11 добавил слеш) [id=919011]:
```nginx
location /api/v4/media/session/poll {
  error_page 418 = @xhttp_poll_legacy;
  if ($arg_sid = "") { return 418; }
  rewrite ^/api/v4/media/session/poll$ /api/v4/media/session/poll/ break;
  proxy_pass http://127.0.0.1:10085;
}
```
- vhost для сабки (двумя строками) [id=659893]:
```nginx
location / { proxy_pass http://remnawave-subscription-page:3010; include /etc/nginx/conf.d/proxy.conf; }
```
healthcheck на localhost (иначе `Reverse proxy and HTTPS are required`) [id=659906].
- VLESS WS + nginx masquerade (decoy) [id=651979|07.06.2026]:
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/private.key;
    location / {
        root /var/www/html;
        index index.html;
    }
    location /ray {
        if ($http_upgrade != "websocket") { return 404; }
        proxy_redirect off;
        proxy_pass http://127.0.0.1:12345;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
- Локальный nginx.conf после обновления (уязвимость nginx 14.05.2026, Caddy не пострадал) [id=508722, 509017]; обновление — github.com/tagashi666/nginx-updater [id=508889].
- ЦДН-лучше-nginx-нарратив: nginx — для маскировки под сайт и сложных роутов, HAProxy — для SNI-роутинга, Caddy — по стандарту для панель/бот/кабинет [id=351082].

## 4.3 HAProxy
- Несколько инбаундов на 443 с разными SNI через haproxy [id=295035|User 777]:
```
frontend front0
    mode tcp
    bind *:443 tfo
    tcp-request inspect-delay 5s
    tcp-request content accept if { req_ssl_hello_type 1 }
    use_backend back0 if { req.ssl_sni -i end ads.x5.ru }
    use_backend back1 if { req.ssl_sni -i end web.max.ru }
    use_backend back2 if { req.ssl_sni -i end cloud.mail.ru }
    use_backend back3 if { req.ssl_sni -i end rutube.ru }
    use_backend back4 if { req.ssl_sni -i end preview.rutube.ru }
    use_backend back5 if { req.ssl_sni -i end api.ok.ru }
    default_backend back0
backend back0
    server srv1 127.0.0.1:10000 send-proxy-v2 tfo
backend back1
    server srv1 127.0.0.1:10001 send-proxy-v2 tfo
```
- HAProxy vs iptables TCP-relay: iptables проще, HAProxy распихивает исходящий трафик (в iptables — только в 1 ноду) [id=1075007]; мосты можно делать через haproxy/nginx/iptables [id=599854]; обход маршрутизации по SNI — через haproxy [id=476837].
- Прокидывание ноды через haproxy 443 по SNI → 8443/8444 (селфсни) [id=761623].

## 4.4 Traefik
- Labels для Bedolaga bot /api + кабинет (дословно) [id=635595|04.06.2026]:
```yaml
services:
  bot:
    networks: [remnawave-network, bot_network]
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
```
Кабинет: `Host(cabinet)` → порт 80; ws — PathPrefix(`/cabinet/ws`) priority 110 [id=222502].
- Traefik-проблема 2.6.0: webhook-режим не стартует с одним маршрутом в traefik [id=55634].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **Реверс-прокси**

◀ [Firewall и анти-DDoS](firewall-ddos.md) · [Сертификаты](сертификаты.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
