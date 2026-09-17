# Заметки из chunk_050 (id 278179..282466, 18.03.2026 .. 20.03.2026)

## ВЕХА 20.03.2026: РКН душит api.telegram.org с РФ-хостов; VLESS «вообще всё»
- **[id=281045|Oleg|20.03.2026](https://t.me/c/2941121338/281045)** Боты на РФ-серверах массово легли: `Cannot connect to host api.telegram.org:443 ssl:default` / SSL handshake >60s. Пинг до api.telegram.org проходит, но HTTP/SSL нет. Не лечится WARP/wg-туннелем в некоторых случаях: «Xray обеспечивает работу вебхука, wg туннель с вебхуками работать не может».
- **[id=280812|Paradigm|20.03](https://t.me/c/2941121338/280812)** «Перестал работать vless-reality уже как 3 дня» → **[id=280813|Zavulon](https://t.me/c/2941121338/280813)** «VLESS ВСЁ», **[id=280820|Andrey P.](https://t.me/c/2941121338/280820)** «⚡⚡⚡ VLESS — ВООБЩЕ ВСЁ ⚡⚡⚡» — массовый отвал vless+reality (транспорта) ~20.03.
- Решения:
  - **[id=281045](https://t.me/c/2941121338/281045)** Перевод `BOT_RUN_MODE=webhook` → `BOT_RUN_MODE=polling` + xray-прокси — бот заработал (на домашнем серваке, Ростелеком).
  - **[id=281036|Help S.](https://t.me/c/2941121338/281036)** Мануал: https://github.com/r00t-man/MZT/blob/main/info/Docker-контейнер Telegram-бота через Xray proxy.md (поднять xray HTTP-proxy локально, направить бот/панель через него; в webhook режиме wg не работает, только xray).
  - **[id=279702→278992|Alexy](https://t.me/c/2941121338/279702)** systemd-юнит: домены ~nalog.ru и ~yookassa.ru резолвить через Яндекс DNS (77.88.8.8, 77.88.8.1), остальное через обычные; переживёт ребут.
- **[id=280854|Egor|20.03](https://t.me/c/2941121338/280854)** «ботов давно надо было на загран сервера переносить; кабинету ставьте oauth oidc с email».
- **[id=280842/280957](https://t.me/c/2941121338/280842)** socks5-прокси для бота вне РФ → доступ к Nalogo (см. раздел Nalogo).

## Bedolaga релизы (18–20.03)
- **[id=278457|Egor|18.03](https://t.me/c/2941121338/278457)** v3.34.1: сброс устройств при смене тарифа; CryptoBot подпись вебхуков (fallback API-токен, 3 стратегии); RioPay 403 — заголовок x-api-token → X-Api-Token (регистрозависимо); синхронизация crypto-ссылки (fallback happ.cryptoLink); полное удаление кнопок быстрого пополнения (16 файлов — показывали некорректные суммы). Cabinet v1.37.1: async загрузка Telegram WebApp SDK (синхронная блокировала DOM на ~51 сек при недоступности telegram.org); цвет тултипов тёмной темы.
- **[id=278916|Egor|18.03](https://t.me/c/2941121338/278916)** Следующий релиз: раздельные топики для уведомлений — 9 env-переменных PURCHASES, RENEWALS, TRIALS, BALANCE, ADDONS, INFRASTRUCTURE, ERRORS, PROMO, PARTNERS (fallback ADMIN_NOTIFICATIONS_TOPIC_ID); email пользователя в API платежей; Platega пинг-запросы без заголовков → 200 OK; CryptoBot подпись по доке; белый фон email-шаблонов; None autopay_days_before → дефолт 3.
- **[id=280792|Egor|20.03](https://t.me/c/2941121338/280792)** v3.36.0: восстановление гостевых покупок (3-фазный пайплайн recover PENDING → retry PAID → retry PENDING_ACTIVATION, все 12 провайдеров, retry_count лимит 20, SELECT FOR UPDATE); граф реферальной сети (API + Cabinet v1.39.0 с Sigma.js Force Atlas 2); медиа в ответах на тикеты; фикс промо-групп (дубли при автоназначении).
- **[id=280941|Egor|20.03](https://t.me/c/2941121338/280941)** v3.36.1 хотфикс: миграция 0042 DuplicateColumnError (retry_count), RBAC bootstrap MultipleResultsFound → scalars().first().
- **[id=279935|Chill|19.03](https://t.me/c/2941121338/279935)** Cabinet v1.22.0 (список): анимированные фоны (Aceternity UI, 14 шт, lazy loading, localStorage), редизайн дашборда, HoverBorderGradient, светлая тема, Freekassa иконки СБП QR/Карта; Google Fonts из CSS @import → <link> preconnect.

## Кабина/бот: известные ошибки и фиксы этого периода
- **[id=278984|18.03](https://t.me/c/2941121338/278984)** Nalogo DNS: lknpd.nalog.ru и api.yookassa.ru отдают SERVFAIL через 1.1.1.1/8.8.8.8 с многих серверов; временный фикс `/etc/hosts`: `213.24.64.181 lknpd.nalog.ru` + restart systemd-resolved; либо второй DNS яндекса.
- **[id=280900+|20.03](https://t.me/c/2941121338/280900)** После апдейта краш при старте: Pydantic ValidationError — KASSA_AI_SHOP_ID/ADMIN_REPORTS_TOPIC_ID/MULENPAY_SHOP_ID/FREEKASSA_SHOP_ID/... ожидают integer, а в .env остатки шаблона ('', '<ID магазина>', '# ID топика'). Фикс: закомментировать/заполнить пустые переменные, потом `make reload`.
- **[id=280839→280865|Дмитрий|20.03](https://t.me/c/2941121338/280839)** Ломание миграции 0041→0042 (DuplicateColumnError retry_count) — фикс: в контейнере бота `alembic stamp head` + `docker restart remnawave_bot` (или дождаться 3.36.1).
- **[id=280467|Daniil|19.03](https://t.me/c/2941121338/280467)** Проверка подписки на канал не работает («Вы еще не подписались»): бот в канале админом, колбеки есть; лечится рестартом/само.
- **[id=279632|19.03](https://t.me/c/2941121338/279632)** «Сообщения в меню»: битое сообщение с невалидным тегом нельзя удалить из админки — правка через БД (Postgres, таблицы категорий сообщений).
- **[id=278527|281436|Acid W.](https://t.me/c/2941121338/278527)** WebSocket token authentication failed → надо `WEB_API_DEFAULT_TOKEN` и `CABINET_JWT_SECRET` в .env (id=278568/278571|Egor).
- **[id=281059/280880|20.03](https://t.me/c/2941121338/281059)** nginx для кабинета: обязателен upstream: 
  ```
  upstream remnawave_bot { server remnawave_bot:8080; }
  ```
  в `/etc/nginx/conf.d/default.conf` в самый верх; иначе `host not found in upstream "remnawave_bot:8080"`. При этом в location не должно быть 8080. Полный рабочий nginx-server-блок от Ак Б. (дословно, сокращён) — proxy_ssl_server_name on; proxy_ssl_verify off; location /api/ rewrite ^/api/(.*) /$1 break; proxy_pass http://remnawave_bot:8080; + $connection_upgrade, gzip, ssl.
  Cabinet docker-compose требует `networks: bot_network external: true name: remnawave-bedolaga-telegram-bot_bot_network`.
- **[id=281185|Kabeba](https://t.me/c/2941121338/281185)** Docker-compose бота (полный, с postgres/redis/nginx/MTU 1350, healthcheck, volume vpn_logo.png) — приведён в чате дословно (id=278525, сокращать не буду: образец конфигурации трёх сервисов в одной сети с postgres 15-alpine, redis 7-alpine, nginx latest, MTU 1350).
- **[id=278496|Environ](https://t.me/c/2941121338/278496)** По любому запросу из кабинета к апи бота на другом сервере — reverse_proxy `remnawave_bot:8080` заменять на IP или домен без https:// (id=282076|User 777).
- **[id=281755|281466](https://t.me/c/2941121338/281755)** Ссылка кабинета в РК не считает переходы/триалы — Egor чинил в отдельных фиксах.
- **[id=281464|ега](https://t.me/c/2941121338/281464)** С телефона кабинет до конца не грузит и кидает в ТГ-виджет с ошибкой «Виджет входа через тг недоступен, войдите через бота» — после апдейта; самое простое — ребутнуть кабину/переустановить статику.
- **[id=280443|20.03](https://t.me/c/2941121338/280443)** Анимации кабинета тормозят браузер, съедают CPU на 2/2 VPS — помогает свап 1–2 ГБ (Sayonara).

## Nalogo/налоги через прокси
- **[id=282120|Ruslan|20.03.2026](https://t.me/c/2941121338/282120)** Полный готовый способ Nalogo с зарубежного сервера (дословно):
  1. На российском сервере SOCKS5:
  ```bash
  docker run -d --name socks5 --restart unless-stopped -p 1080:1080 \
    -e PROXY_USER=user -e PROXY_PASSWORD=ВАШ_ПАРОЛЬ \
    serjs/go-socks5-proxy
  ufw allow 1080/tcp
  ```
  2. В docker-compose.yml бота на зарубежном сервере:
  ```yaml
  environment:
    HTTPS_PROXY: "socks5://user:ВАШ_ПАРОЛЬ@IP_РУ_СЕРВЕРА:1080"
    NO_PROXY: "api.telegram.org,localhost,127.0.0.1,redis,postgres"
  ```
  3. В pyproject.toml: `'httpx[socks]>=0.27.0', 'socksio>=1.0.0'`, затем `pip install uv && uv lock; docker compose down && docker compose build --no-cache && docker compose up -d`
  ⚠️ NO_PROXY обязателен — иначе Telegram тоже пойдёт через прокси и сломается.
- **[id=281828/282284|Filatov](https://t.me/c/2941121338/281828)** У некоторых налог работает через VPN с ру-IP; без VPN lknpd закрыт для не-РФ.
- **[id=281439|Max R](https://t.me/c/2941121338/281439)** «Текущая версия: 3.34.1, обновить бота: `cd /opt/... && git pull origin main && docker compose down && docker compose up -d --build && docker compose logs -f`; кабинет: `cd /opt/bedolaga-cabinet && git pull origin main && npm run build && cd /opt/caddy && docker compose down && docker compose up -d --build`».

## Платежки
- **[id=278249|BARSIK|18.03](https://t.me/c/2941121338/278249)** Platega webhook не привязывается: требует 200 ОК на запрос привязки, бот отдавал 401/unauthorized; вебхук-покупка работает, автопроверку ставят на 1 мин. У других работает из коробки.
- **[id=278343|Egor](https://t.me/c/2941121338/278343)** WATA: автопроверку платежей из бота давно убрали — 429 за частые проверки; «прокси настрой, хук в вате пропиши» (реверс-прокси).
- **[id=280935|Ilia|20.03](https://t.me/c/2941121338/280935)** RollyPay: комса 6% (потом 4%), подключили крипту за 10 минут, СБП часов через 10; Platega — 3 дня подключения, 11% на старте. В боте интеграции нет (запрашивается).
- **[id=279586|19.03](https://t.me/c/2941121338/279586)** Platega vs Wata: у Platega комиссия ниже; у Wata вход 500$.
- **[id=280935|актуально](https://t.me/c/2941121338/280935)** Telegram Stars в бот приходят, баланс смотреть через соответствующий раздел.

## Разное по панели/кабине/тарифам
- **[id=279373|David|19.03](https://t.me/c/2941121338/279373)** Баг: продление считало цену 0₽ при переходе тарифа (data=30 months... final_price=0.0) — логи продления с None.
- **[id=280004|led 14 days|20.03](https://t.me/c/2941121338/280004)** При 14-дневной подписке доп-устройства считаются по месяцу.
- **[id=280151|led 14 days|20.03](https://t.me/c/2941121338/280151)** «Dokupka устройств 0₽» — при цене device = 0 в тарифе.
- **[id=280510|≈Мобилакс](https://t.me/c/2941121338/280510)** «Фон анимированный не грузится в браузерах» — было с обновлением.
- **[id=280648|V M|20.03](https://t.me/c/2941121338/280648)** «BOT_RUN_MODE=webhook wg туннель не работает, только xray» (см. веху).
- **[id=281007|Nhiаz|20.03](https://t.me/c/2941121338/281007)** Мини-апп не показывает кнопку оплаты, пока не включены платёжные методы.
- **[id=280589|Ак Б.|20.03](https://t.me/c/2941121338/280589)** Русские СИ можно «докупать» через… не разобрано, всё в чате.
- **[id=278890|msk|18.03](https://t.me/c/2941121338/278890)** «Кабинет лучше ставить на ру хостинг?» — обсуждение; большая часть решает на заграничный с реверсами.

## Платежки/налоги (вехи 18–20.03)
- **[id=278253|oбre4en z|18.03](https://t.me/c/2941121338/278253)** Ошибка "предложенные суммы" при пополнении — удалили, в 3.34.1 нет.
- **[id=280200|Миша ту-ту](https://t.me/c/2941121338/280200)** Банки/платежки проверяют упоминания «обхода глушилок» — не пиши в тексте.
- **[id=279610|однажды](https://t.me/c/2941121338/279610)** «Проверка платёжей» (Platega) обновилась — webhook (включая апгрейд).

## Хостинги (факты 18–20.03)
- **[id=279294|Zoomov (p2g)](https://t.me/c/2941121338/279294)** «п2г активно работает, финка/шведы у нас проблема с апстримом»; ответ на день клиента: промо CLIENTDAY +5%.
- **[id=280040|nullsystem|19.03](https://t.me/c/2941121338/280040)** p2g Хай-лоад Швеция/Нидерланды падают каждый день; Германия стабильна.
- **[id=280991/280993|Andrey P.](https://t.me/c/2941121338/280991)** Warpx: Германия+Польша+Нидерланды стабильны, финка нестабильна.
- **[id=281017|ssshhh|20.03](https://t.me/c/2941121338/281017)** doubleservers.ru — Швеция 2c/4GB/50GB NVMe за 7.83€/мес, чистый IP, трафик ограничен.
- **[id=281046|Alexy](https://t.me/c/2941121338/281046)** intezio.net — норм хостинг.
- **[id=281593|Zoomov](https://t.me/c/2941121338/281593)** p2g «Мажордомно» — хостинг говно, поддержка игнорирует. СЕО Zoomov (новый КЭО) лично присутствует в чате.
- **[id=281232|Zoomov](https://t.me/c/2941121338/281232)** Intezio Эстония: сервер лежит 4 дня, тикет без ответа 3 дня.
- **[id=279485|Zoomov](https://t.me/c/2941121338/279485)** Intezio «пинг 90-120мс» норм, но у некоторых локаций 4vps камень.

## Хостинги (общие)
- **[id=280350|Zoomov](https://t.me/c/2941121338/280350)** aeza — «хуйня» (США работает через одно место); против: «у меня все ок» — разные мнения.
- **[id=281711|ssshhh](https://t.me/c/2941121338/281711)** doubleservers.ru Швеция — чистый IP, 7.83€/мес, трафик ограничен.
- **[id=281265|hostvds](https://t.me/c/2941121338/281265)** Нидерланды hostvds — нестабильно.
- **[id=281430|Zoomov](https://t.me/c/2941121338/281430)** «интеграции с рутуб», p2g — «хуйня» для кого-то.

## Хостинги/платежки прочее
- **[id=278759|Zoomov (p2g)](https://t.me/c/2941121338/278759)** Айпи-и-повторные-скрипты — транкается.
- **[id=279087|Zoomov](https://t.me/c/2941121338/279087)** Мажордом «абуз» отдельной нодой.
- **[id=281942|Zavulon](https://t.me/c/2941121338/281942)** Intezio нидерланды стабильны.
- **[id=281880|Zoomov](https://t.me/c/2941121338/281880)** «bmy в швеции аплинк ~2тб, атака больше» — атака в пике >10 Гбит на апстрим, UPSTREAM — сам 1cent в Швеции дропало (провайдеры BMY/1cent).
- **[id=280676|zoomov](https://t.me/c/2941121338/280676)** Атаки на апстрим p2g были реальные: распределение трафика между провайдерами, восстановили доступность.

## Мелкие факты
- **[id=278984|18.03](https://t.me/c/2941121338/278984)** Telegram-флуд инлайн-кнопки: при рассылке телега может кидать сообщение с кнопкой, которая не срабатывает — проверено у нескольких.
- **[id=278903|281922](https://t.me/c/2941121338/278903)** ТГ-канал Bedolaga «дезинформирует» в репо — перенаправление в рассылки.
- **[id=280253|Zoomov](https://t.me/c/2941121338/280253)** Промо-тарифы нельзя переносить или улучшать; поддержка отвечает 24+ часов.
- **[id=281295|281308|Max R](https://t.me/c/2941121338/281295)** nuxt.cloud — реф https://nuxt.cloud/?from=34743.
- **[id=282061|prokuratura](https://t.me/c/2941121338/282061)** RU VPS на 4vps забанены отдельные.
- **[id=278759|zoomov](https://t.me/c/2941121338/278759)** «Ток у меня не в РФ» — серверы типа «дес» (в России) не работает.

## Нерасшифрованные ссылки (для точности указаны как есть)
- https://docs.bedolagam.ru/getting-started/docker-deployment
- https://docs.bedolagam.ru/bot/payments (и #platega)
- https://docs.bedolagam.ru/cabinet/setup
- https://docs.bedolagam.ru/cabinet/telegram-oidc
- https://docs.bedolagam.ru/getting-started/troubleshooting
- https://docs.aiogram.dev/en/dev-3.x/api/session/aiohttp.html#proxy-requests-in-aiohttpsession
- https://github.com/PEDZEO/remnawave-panel-backup-telegram (tgshtt: бэкапит и переносит и бот, и панель)
- https://github.com/hxehex/russia-mobile-internet-whitelist (обновляется каждый час)
- https://github.com/igareck/vpn-configs-for-russia
- https://github.com/dotX12/traffic-guard
- https://github.com/distillium/remnawave-backup-restore
- https://github.com/Case211/remnawave-admin
- https://github.com/dotX12/traffic-guard
- https://github.com/r00t-man/MZT (мануал бота через Xray proxy)
- https://github.com/BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot/pull/2655 (ИИ-поддержка, промпт)
- https://github.com/DonMatteoVPN/Reshala-AI-ticket-bot (отдельный ИИ-бот поддержки)
- https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot (branch dev)
- https://docs.rw/docs/install/subscription-page/separate-server
- https://docs.rw/docs/security/caddy-with-custom-path
- https://hyperion-cs.github.io/dpi-checkers/ru/ipv4-whitelisted-subnets/ (чекер БС)
- https://docs.bedolagam.ru/cabinet/landings (лендинги в кабине)
- https://beszel.dev/ (мониторинг)
- https://www.crowdsec.net/ (CrowdSec, анти-DDoS для панели)
- https://github.com/rajnandan1/kener (страница статусов)
- https://cachethq.io/ (статусы)
- https://nuxt.cloud/ (RU-хостинг)
- https://hyperion-cs.github.io/dpi-checkers/ru/ipv4-whitelisted-subnets/ (чекер БС)
- https://log.rw (хостинг логов)
- https://beszel.dev, https://www.crowdsec.net

## Прочее (актуально как раз обсуждали)
- **[id=281055|20.03](https://t.me/c/2941121338/281055)** «Я на ру ставлю панель только ради защиты кабинета» — не логично, кабинет лучше на загран.
- **[id=280487|20.03](https://t.me/c/2941121338/280487)** Уведомления пользователя о подписке/балансе (из кабинета) отсутствуют в миниаппе — Egor чинит.
- **[id=281708|Ак Б.](https://t.me/c/2941121338/281708)** «с моих текущих ТС»

(Конфиденциальная часть удалена. Все конфиги приведены дословно.)
