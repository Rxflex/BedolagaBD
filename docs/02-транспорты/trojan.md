# Trojan

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Trojan**

◀ [Hysteria2](hysteria2.md) · [Shadowsocks / SS-2022](shadowsocks.md) ▶

> конфиг и место в схеме

---
<!-- /KB:HEAD -->

- Трояны даже в БС работают; vmess ремна не умеет [id=760254, 760260, 760262-760267|23.06.2026](https://t.me/c/2941121338/760254) («на vmess одно время сидел — хорошая штука»).
- Схема 4-протокольной ноды через Caddy (443): VLESS XHTTP, Hysteria, Trojan + балансир leastload, маршрутизация через geodat/geoip хедером, клиентский json [id=737107|kataomi|22.06.2026](https://t.me/c/2941121338/737107).
- Trojan в балансерах ру-мостов: RUMSK_Trojan_Inbound / PROXY_FIN1_Trojan_Outbound [id=685741|14.06.2026, id=653971|08.06.2026](https://t.me/c/2941121338/685741).
- TROJAN TCP REALITY | SELFSNI и ЧУЖОЙ SNI — в наборе транспортов многопротокольной ноды [id=1001772|30.07.2026](https://t.me/c/2941121338/1001772).
- Фича-реквест Bedolaga 3.0: выбор протокола Vless/Trojan/WireGuard при подключении [id=115340|18.12.2025](https://t.me/c/2941121338/115340).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Trojan**

◀ [Hysteria2](hysteria2.md) · [Shadowsocks / SS-2022](shadowsocks.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
