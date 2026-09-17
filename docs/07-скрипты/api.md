# API-фишки Remnawave и Bedolaga

<!-- KB:HEAD -->
[⌂](../../README.md) › [⚙ 07. Скрипты и API](README.md) › **API**

◀ [Установщики](установщики.md) · [Чекеры и бенчмарки](чекеры.md) ▶

> WebAPI бота, 30 вебхуков Remnawave, bulk-операции

<details>
<summary>📑 <b>На этой странице</b> — 5 разделов</summary>

- [11.1 WebAPI бота (порт 8080)](#111-webapi-бота-порт-8080)
- [11.2 Webhooks Remnawave → Bedolaga (30 событий, v3.10.0, 10.02.2026)](#112-webhooks-remnawave--bedolaga-30-событий-v3100-10022026)
- [11.3 Единый webhook-сервер Bedolaga (v2.6.0, 07.11.2025)](#113-единый-webhook-сервер-bedolaga-v260-07112025)
- [11.4 Bulk-операции через Remnawave REST API](#114-bulk-операции-через-remnawave-rest-api)
- [11.5 Патчи/PR, на которые ссылаются](#115-патчиpr-на-которые-ссылаются)

</details>

---
<!-- /KB:HEAD -->

## 11.1 WebAPI бота (порт 8080)

Включение: `WEB_API_ENABLED=true`, `WEB_API_PORT=8080`, `WEB_API_ALLOWED_ORIGINS=*` (или конкретные), `WEB_API_TOKEN=`/`WEB_API_DEFAULT_TOKEN=` (6–20 символов) [id=19813..19957, 273227, 390500].
Проверка: `{"status":"ok","api_version":"1.0.0","bot_version":"…","features":{"monitoring":true,…}}` [id=19971]. «Метод Not Allowed» без ключа — норм [id=19971].
Публикация через reverse-proxy: nginx/caddy/traefik, скрывать /docs /redoc /openapi.json в проде, `WEB_API_REQUEST_LOGGING` отключить, ограничить по IP/VPN [id=27094].
REST-эндпоинты: `/promo-offers` (GET/POST/{id}/logs/templates), `/pages` (CRUD политика/оферта/FAQ/правил), `/broadcasts`, `/api/system/stats`, `/api/bandwidth-stats/nodes/{uuid}/users/legacy` (Remna 2.4+), `/menu-layout` (GET список JSON, PATCH /menu-layout/buttons/{button_id} raw JSON) [id=124963, 121296, 23024].
Пагинация `?limit=`/`offset`, токен Bearer `Authorization: Bearer <WEB_API_TOKEN>` [id=273227, 541461].

## 11.2 Webhooks Remnawave → Bedolaga (30 событий, v3.10.0, 10.02.2026)

- В боте: `REMNAWAVE_WEBHOOK_ENABLED=true`, `REMNAWAVE_WEBHOOK_PATH=/remnawave-webhook`, `REMNAWAVE_WEBHOOK_SECRET=<openssl rand -hex 32>` (мин 32, реально 64 символа).
- В панели .env: `WEBHOOK_URL=https://hooks.domen.ru/remnawave-webhook`, `WEBHOOK_SECRET_HEADER=<тот же секрет>` (exact 64, только a-z 0-9 A-Z) [id=216109..217403].
- События (30): user.expired/.disabled/.enabled/.limited/.traffic_reset/.modified/.deleted/.revoked/.created/.first_connected/.bandwidth_usage_threshold_reached/.not_connected/.expired_24_hours_ago; user_hwid_devices.added/.deleted; node.created/.modified/.disabled/.enabled/.deleted/.connection_lost/.connection_restored/.traffic_notify; service.panel_started/.login_attempt_failed/.login_attempt_success/.subpage_config_changed; crm.infra_billing_node_payment_in_7_days/.in_48hrs/.in_24hrs/.due_tod… [id=216158]
- Ивенты задаются в панели .env (WEBHOOK_EVENTS=user.expired,…) [id=217403].
- Порядок запуска: сначала бот+прокси, потом панель (иначе после 3 неудачных попыток вебхук вырубается) [id=216262].
- Проверка: `curl -s https://hooks.domain.com/remnawave-webhook | jq` → `{"status":"ok","service":"remnawave_webhook","enabled":true}` [id=217201].
- «У ремны есть три попытки достучаться до вебхука, если не получилось — больше не пытается и не срёт ошибками» [id=216332].

## 11.3 Единый webhook-сервер Bedolaga (v2.6.0, 07.11.2025)

FastAPI на порту 8080 для всех компонентов (Telegram webhook + платёжные колбэки + админ API + мини-приложение) [id=54824]. Режимы: `BOT_RUN_MODE=webhook|polling|both`. Минимальный .env:
```env
BOT_TOKEN=
ADMIN_IDS=
BOT_RUN_MODE=webhook
WEBHOOK_URL=https://hooks.domain.com
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET_TOKEN=super-secret-token
WEB_API_ENABLED=true
WEB_API_PORT=8080
```
Платёжки ходят по разным путям: /tribute-webhook, /yookassa-webhook, /cryptobot-webhook, /mulenpay-webhook, /pal24-webhook, /wata-webhook, /heleket-webhook, /platega-webhook, /overpay-webhook, /freekassa-webhook, /cloudpayments-webhook, /rollypay-webhook, /urlpay-webhook, /remnawave-webhook [id=58756, 311449].
Ручная переустановка вебхука (после переезда/переноса):
```
https://api.telegram.org/bot<TOKEN>/setwebhook?url=https://<ДОМЕН>/webhook&ip_address=<АЙПИ>&secret_token=<СЕКРЕТ>
```
(ТГ кэширует айпи вебхуков старого сервера до 3 дней) [id=273012].
WEBHOOK_MAX_QUEUE_SIZE=1024, WEBHOOK_WORKERS=4 — дефолт; при массовых активациях промокодов поднять х4-х8 [id=255336].

## 11.4 Bulk-операции через Remnawave REST API

Массовая смена fingerprint (legiz, 25.05.2026, [id=582145]) — PATCH /api/hosts:
```bash
API_URL="https://YOUR_PANEL_URL"
TOKEN="YOUR_TOKEN"
NEW_FP="firefox"   # chrome | firefox | safari | ios | android | edge | qq | random | randomized
UUIDS=$(curl -s -X GET "$API_URL/api/hosts" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "import sys,json; [print(h['uuid']) for h in json.load(sys.stdin)['response']]")
for UUID in $UUIDS; do
  curl -s -X PATCH "$API_URL/api/hosts" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"uuid\": \"$UUID\", \"fingerprint\": \"$NEW_FP\"}"
done
```
PowerShell-версия (fp только у хостов с chrome):
```powershell
$API_URL = "https://YOUR_PANEL_URL"; $TOKEN = "YOUR_TOKEN"
$OLD_FP = "chrome"; $NEW_FP = "firefox"
$headers = @{ "Authorization" = "Bearer $TOKEN"; "Content-Type" = "application/json" }
$hosts   = (Invoke-RestMethod -Uri "$API_URL/api/hosts" -Method GET -Headers $headers).response
$targets = $hosts | Where-Object { $_.fingerprint -eq $OLD_FP }
foreach ($h in $targets) {
    $body = @{ uuid = $h.uuid; fingerprint = $NEW_FP } | ConvertTo-Json
    Invoke-RestMethod -Uri "$API_URL/api/hosts" -Method PATCH -Headers $headers -Body $body | Out-Null
}
```
Тем же патчем можно менять sni, alpn, allowInsecure, port, path и др. [id=582145]. Тот же патч — присвоение хоста к ноде:
```bash
curl -X PATCH "$REMNA_API_BASE_URL/api/hosts" \
  -H "Authorization: Bearer $REMNA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uuid":"<host-uuid>","nodes":["<node-uuid>"]}'
```
[id=661136].

Перевыпуск подписок при смене домена саб-ссылки: в ремне массовые действия → «отозвать подписку» = `POST /api/users/bulk/revoke-subscription` [id=924023..924076].

## 11.5 Патчи/PR, на которые ссылаются

- Xray-core PR 6258 (`injectHosts` {"tagPrefix":"proxy"}) [id=659864, 655073].
- Xray-core PR 6181 (possible fp-related) [id=582273].
- Xray-core PR 5414 (доп. правки) [id=713906].
- Xray-core discussions 4113 (полная документация xhttp) [id=712563].
- Xray-core PR 6307 (слеши) [id=780858].
- Xray-core issue 6264 (детект по UUID) [id=647650].
- aiogram PR 1761 (Bot API 9.4, цветные кнопки) [id=227015, 215678].
- Bedolaga PR 2847 (WEBHOOK_TORRENT_DETECTED) [id=320350].
- Bedolaga PR 3066–3070, cabinet PR 492–493, 551 [id=868616, 1130369].
- Bedolaga PR 2655 (ИИ-поддержка, промпт) [id=122127].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [⚙ 07. Скрипты и API](README.md) › **API**

◀ [Установщики](установщики.md) · [Чекеры и бенчмарки](чекеры.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
