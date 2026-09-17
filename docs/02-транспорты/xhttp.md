# XHTTP (+ selfsni)

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **XHTTP**

◀ [VLESS + Reality](reality.md) · [Selfsteal](selfsteal.md) ▶

> главный рецепт с 11.2025: selfsni, режимы, padding

---
<!-- /KB:HEAD -->

- «xhttp+selfsni — главный рабочий рецепт: воскрешает всё»; большие VPN пересели на xHTTP + селфстил сни (70к юзеров), работает на iPhone (до XR, проверено на 10 айфонах 13–16), скорость у многих выросла вдвое. Минусы: Mihomo/Clash-клиенты не поддерживают [id=71060,71062,71588,72100,74926|Никита,Zavulon|23–26.11.2025].
- Инбаунд Reality+xhttp [note_014]:
```json
"streamSettings": {
  "network": "xhttp", "security": "reality",
  "xhttpSettings": {"host": "ДОМЕН", "mode": "stream-one", "path": "/video-stream"},
  "realitySettings": {"dest": "/dev/shm/nginx.sock", "show": false, "xver": 1, "spiderX": "",
    "shortIds": ["157b68017451de6d"], "privateKey": "СВОЙ", "serverNames": ["ДОМЕН"]}
}
```
- xhttp+TLS+selfsni (Никита ТПСУ, серты letsencrypt в докер ноды) [id=71088,71131,72141,72154|23–24.11.2025]:
```json
{"tag": "xHTTP", "port": 443, "listen": "0.0.0.0", "protocol": "vless",
 "settings": {"clients": [], "decryption": "none"},
 "sniffing": {"enabled": true, "routeOnly": false, "destOverride": ["http","tls","quic"], "metadataOnly": false},
 "streamSettings": {
   "network": "xhttp", "security": "tls",
   "tlsSettings": {"alpn": ["h2","http/1.1"], "maxVersion": "1.3", "minVersion": "1.2",
     "serverName": "селфсни", "fingerprint": "chrome", ...}}}
```
- mode auto: `xhttpSettings: {"mode": "auto", "path": "/germany-xhttp"}` [note_014:87].
- nginx для xhttp [id=338655|Алексей|08.04.2026]:
```nginx
location /xhttppath/ { client_max_body_size 0; grpc_set_header X-Forwarded-For;
  grpc_read_timeout 315; grpc_send_timeout 5m; grpc_pass unix:/dev/shm/xrxh.socket; }
```
- Смена дня: TCP банили → люди пересаживались на xhttp: «когда поймали tcp, на xhttp сразу заработало и почти без потери скорости» [id=319441,319460]; TCP работает, но «троить начала — планирую на xhttp пересесть» [id=319448|~02.04.2026].
- XHTTP не ставят в проде — «встретишь редко», у большинства TCP как основа [id=446994|27.04.2026]; на XHTTP у юзеров автоматом вырубается инет на айфоне [id=446728|Komori|27.04.2026].
- mihomo: vless+xhttp+tls не работает (у одного) [id=794878|03.07.2026]; поддержка xhttp в mihomo — всё ещё в альфе [id=700106,700108|libkit|16.06.2026].
- Новое ядро XHTTP (INCY на ласт ядре): изменены значения (коммит e10347bf01f28bca118002963ee29bbcf529cb25, PR #6258 XTLS/Xray-core) — старые XHTTP+CDN конфиги могут не работать; INCY поддерживает и новые, и старые поля; в Happ ядро старое, поэтому там работает [id=697609|INCY DVP|15.06.2026, id=747736].
- Переход на новое ядро: sessionKey → sessionIDKey, sessionIDPlacement аналогично — но этого мало [id=747436/747766|24.06.2026].
- XHTTP extra (пакет-режим) [id=744116|24.06.2026]: mode packet-up, path /api/v4/media/session/poll, xmux cMaxReuseTimes 32-64, maxConcurrency 4-8, hKeepAlivePeriod 0, hMaxRequestTimes 256-512, hMaxReusableSecs 600-900, seqKey offset, xPaddingKey q, sessionIDKey media_sid, uplinkDataKey X-Playback-Token, xPaddingBytes 32-128, xPaddingHeader X-Rewrite-URL, xPaddingMethod tokenish, uplinkHTTPMethod GET, xPaddingObfsMode true, xPaddingPlacement queryInHeader, scMaxBufferedPosts 16, scMaxEachPostBytes 2048+.
- Xray 26.7.11: формирование URL изменено — раньше клиент отправлял `/poll/?offset=...`, теперь `/poll?offset=...` без завершающего `/`; INCY ругался на неверный путь — фикс: добавить слеш в конец path; Happ переваривает и так и так [id=870008|nbv|14.07.2026, id=870345|Владимир Данилов|14.07.2026].
- Новый happ iOS меняет в конфиге sessionIDKey → sessionKey; в хаппе не отправляется ничего кроме sessionIDkey — сервер лог: `stream-one mode is not allowed (transport/internet/splithttp)`; причина в id-placement — держать полный набор ID-параметров разом [id=866704, 866760, 866791|13.07.2026].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **XHTTP**

◀ [VLESS + Reality](reality.md) · [Selfsteal](selfsteal.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
