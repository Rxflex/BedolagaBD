# VLESS + Reality (TCP/raw)

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **VLESS + Reality**

[XHTTP](xhttp.md) ▶

> базовый рецепт инбаунда, xver, shortIds, destOverride

---
<!-- /KB:HEAD -->

Типовой инбаунд (шаблон чата):
```json
"inbounds": [{
  "tag": "NODA1_VPN_VLESS", "port": 443, "protocol": "vless",
  "settings": { "clients": [], "decryption": "none" },
  "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
  "streamSettings": {
    "network": "raw", "security": "reality",
    "realitySettings": {
      "show": false, "xver": 1, "target": "127.0.0.1:9443", "spiderX": "",
      "shortIds": ["XXXXXXXXXXXXXX"],
      "privateKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "serverNames": ["domain.com"]
    }
  }
}]
```
[xid 114..~117, note_001; вариант note_020 id=114755+]

- Реверс-прокси вариант: `dest: "/dev/shm/nginx.sock"`, `xver: 1`, `spiderX: ""` [id=18313|note_004](https://t.me/c/2941121338/18313).
- «target — порт самой переадресации, который указывал при настройке selfsteal» [id=28441..28454|Egor|29.11.2025](https://t.me/c/2941121338/28441): полный шаблон selfsteal — NL_VLESS_PROFILE port 443, target 127.0.0.1:9443, sniffing http/tls/quic; routing: block bittorrent / geoip:private / geosite:private; DNS 1.1.1.1/1.0.0.1.
- Спор про shortIds: Илья — для каждого юзера не нужен (UUID уникален, актуально для SS); Дмитрий — shortId в Client Hello отличает клиента Reality от обычного HTTPS и сокращает handshake [id=18313..18324|note_004](https://t.me/c/2941121338/18313).
- У некоторых клиентов отключалось: совет — network поменять с raw на tcp/tls, `target` → `dest`, стало лучше [id=18302|29.09.2025](https://t.me/c/2941121338/18302).
- «Реалити не охото оставлять — реалити сложнее блокировать по DPI» [id=28443|c0mrade|29.11.2025](https://t.me/c/2941121338/28443).

Генерация ключей на ноде:
```
docker exec <container_id> xray x25519 && openssl rand -hex 8
```
(privateKey — первый вывод, shortIds — последний hex) [id=note_017, ~10.12.2025](https://t.me/c/2941121338/017).

Примеры target/serverNames из практики: `yandex.ru:443` + serverNames `yandex.ru,www.yandex.ru` [note_016]; `vk.com:443`, routeOnly true [note_018]; `max.ru:10000` (serverNames max.ru, www.max.ru) [id=196003|DONK|26.01.2026](https://t.me/c/2941121338/196003); `yandex.ru:7443` [note_042]; `www.amd.com:443` [id=306460|30.03.2026](https://t.me/c/2941121338/306460); `ads.x5.ru:443` + fingerprint chrome + `sockopt: {"tcpFastOpen": true, "tcpKeepAliveIdle": 100}` [note_057]; `st.ozone.ru:443` [id=636346|khanzele|04.06.2026](https://t.me/c/2941121338/636346).

Обход Reality для блокировок (ТСПУ-регионы): `realitySettings.dest = 1.1.1.1:443`, `serverNames = [""]` — работает в Приморском крае, Иркутской, Новосибирской обл. Профиль vless-reality-vision, port 443, sniffing routeOnly true, DNS cloudflare/google [id=71159,72142,72155|Камушек|23.11.2025](https://t.me/c/2941121338/71159).

Полный конфиг ру-ноды с балансировкой на 2 EU [id=699075|Руслан И.|15.06.2026](https://t.me/c/2941121338/699075): inbound RU_IN (vless, 443, reality, dest ads.x5.ru:443, serverNames ads.x5.ru, fingerprint firefox, sniffing routeOnly http/tls/quic); outbounds EU_OUT_1/EU_OUT_2 (vless xtls-rprx-vision, reality, serverName www.amazon.com, fingerprint firefox), RU_DIRECT (freedom), RU_BLOCK (blackhole); routing: bittorrent→BLOCK, geoip:private→BLOCK, geoip:ru→RU_DIRECT, geosite:category-ru→RU_DIRECT, RU_IN→balancerTag EU_BALANCER; balancers: selector EU_OUT, strategy leastPing; domainStrategy IPIfNonMatch; policy connIdle 120, handshake 4, uplinkOnly 1, downlinkOnly 2; observatory probeUrl [google.com/generate_204](https://www.google.com/generate_204), probeInterval 30s, subjectSelector EU_OUT, enableConcurrency true.

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **VLESS + Reality**

[XHTTP](xhttp.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
