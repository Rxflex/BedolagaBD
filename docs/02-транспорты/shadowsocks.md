# Shadowsocks, SS-2022, мосты RU→EU

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Shadowsocks / SS-2022**

◀ [Trojan](trojan.md) · [Мультитранспорт и порты](мультитранспорт-порты.md) ▶

> мосты RU→EU, 2022-blake3, цепочки

---
<!-- /KB:HEAD -->

- Мост через shadowsocks (EU inbound / RU outbound) [id=308113|хеуклер|30.03.2026](https://t.me/c/2941121338/308113):
```json
"inbounds": [{"tag": "ss", "port": ..., "listen": "0.0.0.0", "protocol": "shadowsocks",
  "settings": {"clients": [], "network": "tcp,udp"},
  "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]}}]
```
```json
{"tag": "abv", "protocol": "shadowsocks",
 "settings": {"servers": [{"port": ..., "level": 0, "method": "chacha20-ietf-poly1305",
   "address": "...", "password": "..."}]}}
```
- Схема моста: vless in → ss out → ss in [id=309287|снупс Догс|31.03.2026](https://t.me/c/2941121338/309287).
- Каскад vless→ss: на зарубежном конце SS, в public vless; vless→vless никто не делает из-за пинга и скорости, только если vless→ss не работает; для моста SS на отдельном порту («открой порт для SS, на влесе тоже 443 как минимум») [id=439235..439239, 439005, 439015|Frist, c0mrade|27.04.2026](https://t.me/c/2941121338/439235).
- Shadowsocks на ТСПУ банится на большинстве провайдеров [id=439173, 439176|Frist|27.04.2026](https://t.me/c/2941121338/439173).
- Selectel блокирует vless tcp: на мосту только ss работает [id=698859|16.06.2026](https://t.me/c/2941121338/698859).
- WARP на ноде (RU vless → DE ss) — 100% не воркало [id=126865|23.12.2025](https://t.me/c/2941121338/126865).
- Практика: «ремна в Германии, нода в РФ и Нидерландах; из РФ проксируется по ss на нидеры; vless→ru→сокс→германия. Shadowsocks заебись» [id=322542,322527|Frist|04.04.2026](https://t.me/c/2941121338/322542).
- Три SS-outbound на TR/DE/NL (chacha20-ietf-poly1305, port 9999) + три VLESS TCP REALITY inbound (555/556/557, target google.com:443); балансер не завёлся, пропадало соединение со всеми инбаундами [id=323750|Sakred_|04.04.2026](https://t.me/c/2941121338/323750).
- Remnawave 2.7: добавлен shadowsocks 2022 [id=303247|libkit|29.03.2026](https://t.me/c/2941121338/303247); длина ключа SS-2022 проверяется в Xray-UI-Editor v1.2.0 [note_151|05.08.2026].
- YooKassa обход: ss_tunnel (shadowsocks-libev) + privoxy, `forward-socks5t /api.yookassa.ru/ ss_tunnel:1081 .`; проверка curl → HTTP/2 401 = работает [id=81016|02.12.2025, id=102457|Genik|11.12.2025](https://t.me/c/2941121338/81016).
- RU-нода классика: PUBLIC_RU_INBOUND (443, vless+reality, target google.com:443, xver 0) + SS_OUTBOUND_TO_DE (chacha20-ietf-poly1305, port 9999); DE-нода BRIDGE_DE_IN (9999, shadowsocks tcp,udp) [note_022|~22.12.2025].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Shadowsocks / SS-2022**

◀ [Trojan](trojan.md) · [Мультитранспорт и порты](мультитранспорт-порты.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
