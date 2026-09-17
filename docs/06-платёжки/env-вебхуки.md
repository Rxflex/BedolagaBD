# Env-конфиги и вебхуки платёжек

<!-- KB:HEAD -->
[⌂](../../README.md) › [💳 06. Платёжки и бизнес](README.md) › **Env и вебхуки**

◀ [Профили платёжек](профили-платёжек.md) · [ЮKassa и легальные кассы](юкасса.md) ▶

> дословные конфиги подключения и грабли

<details>
<summary>📑 <b>На этой странице</b> — 8 разделов</summary>

- [Общий запуск бота (08.11.2025)](#общий-запуск-бота-08112025)
- [Platega](#platega)
- [CryptoBot (v2.2.5, [id=4757](https://t.me/c/2941121338/4757), 09.09.2025)](#cryptobot-v225-id4757-09092025)
- [Проверка/отмена платежей](#проверкаотмена-платежей)
- [Ценообразование трафика (v2.0.5, [id=75](https://t.me/c/2941121338/2/75))](#ценообразование-трафика-v205-id75)
- [Пути вебхуков (Caddy/Nginx reverse-proxy)](#пути-вебхуков-caddynginx-reverse-proxy)
- [Грабли вебхуков](#грабли-вебхуков)
- [Вывод средств (bedolaga-cabinet)](#вывод-средств-bedolaga-cabinet)

</details>

---
<!-- /KB:HEAD -->

## Общий запуск бота (08.11.2025)
```env
BOT_TOKEN=...
ADMIN_IDS=...
BOT_RUN_MODE=webhook            # 0: webhook, 1: polling
WEBHOOK_URL=https://hooks.domain.com/
WEBHOOK_SECRET_TOKEN=super-secret-token
WEB_API_ENABLED=true
WEB_API_ALLOWED_ORIGINS=...
# настройки Web API хранятся в БД; env имеет приоритет
```

## Platega
```env
PLATEGA_ENABLED=true
PLATEGA_MERCHANT_ID=your_merchant_id
PLATEGA_SECRET_KEY=your_secret
PLATEGA_RETURN_URL=https://your-domain.com/payment-failed
PLATEGA_FAILED_URL=https://your-domain.com/payment-failed
```

## CryptoBot (v2.2.5, [id=4757](https://t.me/c/2941121338/4757), 09.09.2025)
```env
CRYPTOBOT_ENABLED=true
CRYPTOBOT_API_TOKEN=your_token
CRYPTOBOT_WEBHOOK_SECRET=your_secret
CRYPTOBOT_TESTNET=false
CRYPTOBOT_ASSETS=USDT,TON,BTC,ETH,LTC,BNB,TRX,USDC
CRYPTOBOT_INVOICE_EXPIRATION=<срок>
# таблица cryptobot_payments, enum PaymentMethod + CRYPTOBOT
# курс USD/RUB: ЦБ РФ + exchangerate-api.com, кеш 1 час
```

## Проверка/отмена платежей
```env
PAYMENT_VERIFICATION_AUTO_CHECK_ENABLED=true
PAYMENT_VERIFICATION_AUTO_CHECK_INTERVAL_MINUTES=10
# автоотмена неоплаченных подписок; умные скидки после пополнения
```

## Ценообразование трафика (v2.0.5, [id=75](https://t.me/c/2941121338/2/75))
```env
TRAFFIC_SELECTION_MODE=selectable   # selectable | fixed
FIXED_TRAFFIC_LIMIT_GB=0            # 0 = безлимит
# для fixed проставить цены всем: PRICE_TRAFFIC_5/10/25/50/100/250/0=0
```

## Пути вебхуков (Caddy/Nginx reverse-proxy)
- Канонические пути бота: `/yookassa-webhook`, `/platega-webhook`, `/cryptobot-webhook`, `/wata-webhook`, `/heleket-webhook`, `/tribute-webhook`, `/omney-webhook`.
- Tribute: при выключенном трибьюте webhook-сервер не запускается; адрес `http://0.0.0.0:8081/tribute-webhook` [id=3486, 3487](https://t.me/c/2941121338/3486).
- С 06.08.2026 Platega требует заголовки `X-MerchantId` / `X-Secret` в GET-запросах статуса транзакции, иначе 401 [id=1040119](https://t.me/c/2941121338/1040119).

## Грабли вебхуков
- Вебхук-роуты платёжек монтируются только по env-флагу `*_ENABLED`, а не по DB-конфигу `payment_method_configs`: включение через админку (`is_enabled=true`) без env-флага → GET вебхука отдаёт 404; пропущенный колббек = висящий платёж [id=1023658](https://t.me/c/2941121338/1023658).
- «Платёж есть в платёжке, в боте не пополнился» → URL вебхука не был прописан в настройках платёжки [id=1101041](https://t.me/c/2941121338/1101041).
- HTTP 405 при отправке хука → в 99% случаев виноват реверс-прокси (опыт с Lava) [id=1101027](https://t.me/c/2941121338/1101027).
- В ЛК платёжки есть вся инфа о вебхуке и причина провала; вебхук переотправляется отдельным пунктом «переотправить» [id=1101033](https://t.me/c/2941121338/1101033).
- Если платёжка выключена и бот перезагружен, после включения оплата проходит, но хуки не работают (feature-запрос) [id=1093661](https://t.me/c/2941121338/1093661).
- Remnawave → Bedolaga: синхронизация подписок через вебхуки панели, доки `docs.bedolagam.ru/integrations/remnawave#webhooks-от-панели`; без вебхуков изменения на панели не видны в боте [id=1056977](https://t.me/c/2941121338/1056977). Ошибка `RemnaWave webhook: invalid signature http_path=/remnawave-webhook` — чинить подпись/токен [id=1159430](https://t.me/c/2941121338/1159430).
- Скорость вебхуков: cisPay 5–7 сек [id=1159539](https://t.me/c/2941121338/1159539); WATA 2–3 минуты (критично) [id=1159426](https://t.me/c/2941121338/1159426).

## Вывод средств (bedolaga-cabinet)
Способы вывода в кабинете: СБП, карта РФ, карта других стран, SEPA, крипта, CryptoBot, TG Stars, баланс бота [id=1033881](https://t.me/c/2941121338/1033881). Реф-баланс нельзя конвертировать в подписку — только реф-доход в общий баланс [id=1032893](https://t.me/c/2941121338/1032893). Рефка: 50% с первого пополнения, 25% с последующих [id=1032939](https://t.me/c/2941121338/1032939).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [💳 06. Платёжки и бизнес](README.md) › **Env и вебхуки**

◀ [Профили платёжек](профили-платёжек.md) · [ЮKassa и легальные кассы](юкасса.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
