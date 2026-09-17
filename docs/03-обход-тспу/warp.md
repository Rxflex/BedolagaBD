# WARP, Cloudflare, NaiveProxy

<!-- KB:HEAD -->
[⌂](../../README.md) › [🛡 03. Обход ТСПУ](README.md) › **WARP и Cloudflare**

◀ [Мосты RU→EU](мосты.md) · [Детект и fingerprint](детект-fingerprint.md) ▶

> wgcf, NaiveProxy, когда помогает

---
<!-- /KB:HEAD -->

## WARP / Cloudflare / NaiveProxy · Часть A

- **[id=81696|08.06.2026](https://t.me/c/2941121338/81696)** Роутинг WARP на ноду для Gemini:
  ```json
  {"routing":{"rules":[{"type":"field","domain":["gemini.google.com","generativelanguage.googleapis.com","ai.google.dev","aistudio.google.com"],"outboundTag":"warp"}]}}
  ```
- **[id=749432](https://t.me/c/2941121338/749432)** Конфиг warp-outbound (дословно):
  ```json
  {"tag":"warp","protocol":"wireguard","settings":{"mtu":1280,"peers":[{"endpoint":"162.159.192.1:2408","publicKey":"bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo="}],"address":["172.16.0.2/32"],"reserved":[0,0,0],"secretKey":"***"}}
  ```
- **[id=791162|YukiOff1cial|02.07.2026](https://t.me/c/2941121338/791162)** Инструкция: установка WARP-native на сервер и проброс трафика через него на Gemini:
  ```bash
  bash <(curl -fsSL https://raw.githubusercontent.com/distillium/warp-native/main/install.sh)
  ```
- **[id=791127..791572|Александр|02.07.2026](https://t.me/c/2941121338/791127)** WARP-интерфейс warp был на хосте, а Remnawave Node/Xray работал внутри Docker-контейнера в отдельной сети. После перевода контейнера в `network_mode: host` — заработало.
- **[id=1113856|Makenov|14.08.2026](https://t.me/c/2941121338/1113856)** «Пока через WARP нет рекламы на ютубе — пойдут ли европейцы/америкосы качать WARP ради ютуба без рекламы».
- **[id=1150970|Egor|20.08.2026](https://t.me/c/2941121338/1150970)** «WARP — ВСЁ» (WARP отвалился полностью).
- **[id=1112398|;)|14.08.2026](https://t.me/c/2941121338/1112398)** Gemini перестал работать у части россиян даже с VPN; Google: «произошла русификация айпишников Cloudflare, скорее всего не вручную, а автоматически».
- **[id=1150989|20.08.2026](https://t.me/c/2941121338/1150989)** Скрипт `ShortsForge` — конвейер шортсов (плагин для Claude Code).

## WARP (продолжение) · Часть B

- **[id=1113856|Makenov|14.08.2026](https://t.me/c/2941121338/1113856)** «Пока через WARP нет рекламы на ютубе — пойдут ли европейцы/америкосы качать WARP ради ютуба без рекламы».
- **[id=1150970|Egor|20.08.2026](https://t.me/c/2941121338/1150970)** «WARP — ВСЁ» (WARP отвалился полностью).
- **[id=1164631|21.08.2026](https://t.me/c/2941121338/1164631)** Telegram готовит новый способ обхода блокировок через веб-прокси: маскирует прокси-соединение под обычный HTTPS-трафик; Telegram Desktop подключается к сайту через HTTPS/WebSocket, внутри которого проходит MTProxy-трафик.
- **[id=1169562|Дмитрий|22.08.2026](https://t.me/c/2941121338/1169562)** «Web-прокси УЖЕ В ТГ — обнову наконец завезли».

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🛡 03. Обход ТСПУ](README.md) › **WARP и Cloudflare**

◀ [Мосты RU→EU](мосты.md) · [Детект и fingerprint](детект-fingerprint.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
