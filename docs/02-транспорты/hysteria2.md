# Hysteria2

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Hysteria2**

◀ [WebSocket + TLS](websocket.md) · [Trojan](trojan.md) ▶

> UDP-транспорт: конфиг, обфускация, лимиты

---
<!-- /KB:HEAD -->

- Inbound Hysteria (для 3x-ui/Xray) [id=322563|Николай|04.04.2026]:
```json
{"tag": "HYSTERIA_Добавь своё", "port": 443, "listen": "0.0.0.0", "protocol": "hysteria",
 "settings": {"clients": [], "version": 2},
 "streamSettings": {"network": "hysteria", "security": "tls",
   "tlsSettings": {"alpn": ["h3"],
     "certificates": [{"keyFile": "...", "certificateFile": "..."}]},
   "hysteriaSettings": {"version": 2}}}
```
- hysteria2 по LTE вроде норм, но есть шанс блокировки (UDP банится в РФ) [id=306906, 306855|30.03.2026].
- МТС режет UDP/QUIC — хистерия не работает, лучше vless [id=320950|~02.04.2026].
- TikTok на iOS при хистерии + Автовыбор: «Сервисы недоступны»; конфиг серверного моста Hysteria-BBR (QUIC, alpn h3, bbr, outbound через shadowsocks) [id=335870|MARELLO|07.04.2026].
- finalmask-вариант hysteria: network hysteria + `finalmask: {"quicParams": {"debug": false, "congestion": "bbr"}}` [note_055:190-195|30.03.2026].
- Remna не умеет передавать hysteria2 в mihomo — настраивать шаблоны сабок под правильные ядра [id=660505|09.06.2026].
- HAPP/INCY (tun) забывают маршрут для hysteria2 в таблицу маршрутизации (ядро Linux не занимается, tun сам в себя влетает; HAPP занимает подсеть docker 172.18.0.0/30 dev tun0). Воркароунд: `ip rule add to {hysteria2_server_ip} lookup main pref 50` [id=869292..869301|14.07.2026].
- «path mtu discovery over udp неважно — на низких MTU всё равно не работает» [id=868675|14.07.2026].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **Hysteria2**

◀ [WebSocket + TLS](websocket.md) · [Trojan](trojan.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
