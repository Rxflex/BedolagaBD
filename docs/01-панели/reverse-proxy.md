# Nginx / Caddy для панели, бота и кабинета

<!-- KB:HEAD -->
[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Nginx / Caddy**

◀ [Env-переменные](env.md) · [Конфиги и настройки](конфиги-настройки.md) ▶

> реверс для панели, вебхуков, миниаппы, кабинета

---
<!-- /KB:HEAD -->

## Период 09.02–13.03.2026 — Bedolaga v3.9–3.32, Remnawave 2.6.x, Remnawave-admin 2.x

Каноничный Caddy кабинета от Егора:
```
{$CABINET_DOMAIN} {
    import geoip_block
    encode gzip zstd
    handle /api/* { uri strip_prefix /api; reverse_proxy remnawave_bot:8080 { import proxy_defaults } }
    handle { root * /srv/cabinet; try_files {path} /index.html; file_server; @static path *.js *.css *.woff2 *.ico *.png *.jpg *.svg *.webp *.gif; header @static Cache-Control "public, max-age=31536000, immutable"; @html path *.html /; header @html Cache-Control "no-cache, must-revalidate" }
}
```
[id=220889](https://t.me/c/2941121338/220889)

Caddy hooks+cabinet от c0mrade:
```
(proxy_defaults) { header_up Host {host}; header_up X-Real-IP {remote_host}; transport http { read_buffer 0 } }
hooks.example.com { encode gzip zstd; @webhooks { path /yookassa-webhook; path /platega-webhook; path /cryptobot-webhook; path /wata-webhook } handle @webhooks { reverse_proxy remnawave_bot:8080 { import proxy_defaults } } handle /app-config.json { header Access-Control-Allow-Origin "*"; reverse_proxy remnawave_bot:8080 } handle { reverse_proxy remnawave_bot:8080 } }
cabinet.example.com { encode gzip zstd; handle /api/* { uri strip_prefix /api; reverse_proxy remnawave_bot:8080 } handle { root * /srv/cabinet; try_files {path} /index.html; file_server } }
```
[id=226539](https://t.me/c/2941121338/226539)

Рекомендуемая архитектура: идеал панель/сабка/бот/кабинет — 4 сервера [id=271017](https://t.me/c/2941121338/271017); минимум бот+кабинет / панель+сабка [id=271016](https://t.me/c/2941121338/271016).

---

## Период 16.03–06.04.2026 — Remnawave 2.7.x (breaking), Bedolaga v3.33–3.45

- nginx upstream обязателен вверху `/etc/nginx/conf.d/default.conf`: `upstream remnawave_bot { server remnawave_bot:8080; }` иначе host not found; proxy_ssl_server_name on; rewrite ^/api/(.*) /$1 break [id=281060](https://t.me/c/2941121338/281060). Прокси бота на другом сервере — без https:// [id=278496; id=301547](https://t.me/c/2941121338/278496); не кидать бота наружу [id=301554](https://t.me/c/2941121338/301554). Юкасса: `location = /yookassa-webhook` + полный https URL [id=285903; id=286351](https://t.me/c/2941121338/285903). Скрипт R4z смены BOT_IP [id=317011](https://t.me/c/2941121338/317011).
- Caddy telegram-web-app.js прокси + sed index.html [id=274193](https://t.me/c/2941121338/274193).
- Caddy wss: `handle /cabinet/ws* { reverse_proxy remnawave_bot:8080 }` [id=294843](https://t.me/c/2941121338/294843).
- Caddyfile всех хуков+кабинет (proxy_defaults, hooks.example.com @webhooks 11 путей, cabinet.example.com) [id=324376](https://t.me/c/2941121338/324376); боевой Фантомаса [id=329231, id=329238](https://t.me/c/2941121338/329231); haproxy SNI на 443 [id=295035](https://t.me/c/2941121338/295035).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Nginx / Caddy**

◀ [Env-переменные](env.md) · [Конфиги и настройки](конфиги-настройки.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
