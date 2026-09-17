# Selfsteal (свой SNI)

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Selfsteal**

◀ [XHTTP](xhttp.md) · [SNI и fingerprint](sni-fingerprint.md) ▶

> свой SNI: как поднять и чем накрыть

---
<!-- /KB:HEAD -->

- Selfsteal: поднять свой сайт вместо SNI google; на 443 спереди xray, за ним caddy/nginx с fallback на локалку. Маскироваться под свои сайты (иначе первый запрос = бан IP-хоста) [id=10360..10516|16.09.2025].
- Не прятаться под Google/8443; само-стил на 443 [id=439284|Stanislav Torichnev|27.04.2026].
- Caddy fallback + xray xhttp inbound: `edge.example.com: root /var/www/html file_server; handle_path /secretpath* reverse_proxy 127.0.0.1:10000` + xray vless xhttp security none, listen 127.0.0.1:10000, path /secretpath, host edge.example.com, outbound freedom [id=322178|vibes|04.04.2026].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Selfsteal**

◀ [XHTTP](xhttp.md) · [SNI и fingerprint](sni-fingerprint.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
