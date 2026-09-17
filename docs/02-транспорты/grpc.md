# gRPC

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **gRPC**

◀ [SNI и fingerprint](sni-fingerprint.md) · [WebSocket + TLS](websocket.md) ▶

> конфиг, multiMode, когда выигрывает

---
<!-- /KB:HEAD -->

- gRPC как inbound — костыль для клиентов, которые не могут XHTTP; легче палится, на iOS пинг растёт до 1000 мс; лучше не использовать либо выделять отдельный сервер [id=530401,530262,530273,530275|Stanislav Torichnev|18.05.2026].
- grpc+reality работает [id=578834|Tesla|24.05.2026]: `network: grpc, security: reality, grpcSettings: {mode:false, serviceName:"service"}, target: 127.0.0.1:9443`, xver:1.
- gRPC+Reality через CDN не заработал [id=578984|Ак Барс|24.05.2026]:
```json
{"tag": "grpc-cdn", "port": 10445, "protocol": "vless",
 "settings": {"clients": [], "decryption": "none"},
 "streamSettings": {
   "network": "grpc", "security": "none",
   "grpcSettings": {"multiMode": true,
     "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0.0.0 Safari/537.36",
     "idleTimeout": 15, "serviceName": "/api", "healthCheckTimeout": 12,
     "initialWindowsSize": 0, "permitWithoutStream": false}}}
```
- gRPC-тест моста [id=636230|undr|04.06.2026]: port 2345, grpc reality, serviceName LvlAppSync, dest gateway.icloud.com:443, serverNames gateway.icloud.com/mask-api.icloud.com.
- raw Reality target st.ozone.ru:443 + grpc-инбаунд на том же 443 (security none, serviceName vless) [id=636346|khanzele|04.06.2026].
- «Только Telegram» конфиг: vless 443 + flow xtls-rprx-vision + grpc serviceName telegram-only + tls-сертификаты; routing: geosite:telegram/geoip:telegram → telegram, остальное tcp,udp → block [id=728264|Vladislav|21.06.2026].
- При автовыборе (балансер) gRPC — периодические обрывы, по-видимому конфликт Happ [id=585235|24.05.2026].
- «Перейдите на grpc; xhttp не особо рекомендую, но на запас можно» [id=647695|Pavel Kosyakov|06.06.2026].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **gRPC**

◀ [SNI и fingerprint](sni-fingerprint.md) · [WebSocket + TLS](websocket.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
