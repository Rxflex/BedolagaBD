# WARP / Psiphon

<!-- KB:HEAD -->
[⌂](../../README.md) › [⚙ 07. Скрипты и API](README.md) › **WARP / Psiphon**

◀ [Генераторы роутинга](роутинг-генераторы.md) · [Боты-помощники](боты-помощники.md) ▶

> скрипты поднятия и связки

---
<!-- /KB:HEAD -->

- `github.com/distillium/warp-native` — нативный WARP (wgcf); установка:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/distillium/warp-native/main/install.sh)
```
[id=504448, 1086697]. Шаблоны аутбаундов: README_ru.md [id=636115]. WARP поднимается на ноду, аутбаунд в warp → гугл/гемини роутить [id=427566]. «Ниже правил DIRECT и BLOCK добавь варп, а не между ними» [id=427683, 427860].
- `github.com/tagashi666/vps-warp` — WARP-установщик с авто-ротацией IP из пула 162.159.{192,193,195}.x, TCP MSS Clamping, Table=off, поддержка WARP+; CLI vps-warp; README под Remnawave 2.8.1 UseIP→ForceIP [id=723065, 1086718].
- `github.com/Capybara-z/RemnaSetup` — «полный пакет» selfsteal + WARP [id=483752, 636113].
- `github.com/Chara-Freedom/vps-psiphon` — Psiphon для Gemini; «ставьте регион Нидерланды и Ютуб пашет без рекламы» [id=1166999, 1153563].
- WARP outbound (Xray wireguard, дословно [id=749432]):
```json
{ "tag": "warp", "protocol": "wireguard", "settings": {
  "mtu": 1280,
  "peers": [ { "endpoint": "162.159.192.1:2408", "publicKey": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=" } ],
  "address": ["172.16.0.2/32"],
  "reserved": [0,0,0],
  "secretKey": "***"
} }
```
Роутинг в warp: geosite:openai, domain:spotify.com, domain:scdn.co, geosite:netflix, domain:chatgpt.com, domain:oaistatic.com, domain:gemini.google.com → outboundTag warp [id=749436].
- Ошибка запуска warp в RemnaNode (Docker): `failed to create virtual tun interface > failed to disable ipv4 rp_filter for all: read-only file system` — нужен NET_ADMIN: в docker-compose `cap_add: - NET_ADMIN` [id=749423].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [⚙ 07. Скрипты и API](README.md) › **WARP / Psiphon**

◀ [Генераторы роутинга](роутинг-генераторы.md) · [Боты-помощники](боты-помощники.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
