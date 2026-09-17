# Admin-панели и внешние дашборды

<!-- KB:HEAD -->
[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Admin-панели**

◀ [Ошибки → фиксы](ошибки-фиксы.md) · [Кейсы и разборы](кейсы.md) ▶

> remnawave-admin, вебадминка бота, дашборды, плагины

<details>
<summary>📑 <b>На этой странице</b> — 23 разделов</summary>

- [Период 23.08–07.09.2025 — Bedolaga v2.0.x–2.2.x, Remnawave 2.1.x](#период-230807092025--bedolaga-v20x22x-remnawave-21x)
- [Период 12.11.2025–01.01.2026 — Bedolaga v2.7–2.9.4, Remnawave 2.3–2.4](#период-1211202501012026--bedolaga-v27294-remnawave-2324)
- [Период 09.02–13.03.2026 — Bedolaga v3.9–3.32, Remnawave 2.6.x, Remnawave-admin 2.x](#период-090213032026--bedolaga-v39332-remnawave-26x-remnawave-admin-2x)
- [Период 16.03–06.04.2026 — Remnawave 2.7.x (breaking), Bedolaga v3.33–3.45](#период-160306042026--remnawave-27x-breaking-bedolaga-v333345)
- [Период 06–25.04.2026 — Bedolaga v3.45–3.52, Remnawave-admin 2.9–2.11](#период-0625042026--bedolaga-v345352-remnawave-admin-29211)
- [Период 25.04–15.05.2026 — Bedolaga v3.49–3.55, Cabinet 1.49–1.52](#период-250415052026--bedolaga-v349355-cabinet-149152)
  - [remnawave-admin (Case211) — см. Релизы](#remnawave-admin-case211--см-релизы)
  - [Web-админка бота (штатная Bedolaga)](#web-админка-бота-штатная-bedolaga)
  - [Bedolagam / документация](#bedolagam--документация)
  - [Прочие панели управления](#прочие-панели-управления)
- [Период 16.05–05.06.2026 — Bedolaga v3.56–3.58, Remnawave-admin 2.14](#период-160505062026--bedolaga-v356358-remnawave-admin-214)
- [Период 07–26.06.2026 — Bedolaga 3.60–3.61, Subscription-page 7.2.5/7.2.6](#период-0726062026--bedolaga-360361-subscription-page-725726)
- [Период 26.06–08.07.2026 — Remnawave 2.8.0, Bedolaga v3.61–3.62, Cabinet 1.59](#период-260608072026--remnawave-280-bedolaga-v361362-cabinet-159)
- [Период 08–20.07.2026 — Remnawave 2.8.1, Bedolaga v3.62–3.64, Cabinet 1.61](#период-0820072026--remnawave-281-bedolaga-v362364-cabinet-161)
- [Период 20–31.07.2026 — Bedolaga v3.66/3.67 + Cabinet 1.64 (рекурренты Platega/Lava)](#период-2031072026--bedolaga-v366367--cabinet-164-рекурренты-plategalava)
  - [Защита панели](#защита-панели)
- [Период 31.07–09.08.2026 — Remnawave 3.0.0 (ломающий), Bedolaga v4.0.0, Cabinet 1.65](#период-310709082026--remnawave-300-ломающий-bedolaga-v400-cabinet-165)
  - [REMNA-ADMIN [id=1033967](https://t.me/c/2941121338/1033967)](#remna-admin-id1033967)
  - [bedolaga-support (автоответчик тикетов) [id=1064918, id=1084107](https://t.me/c/2941121338/1064918)](#bedolaga-support-автоответчик-тикетов-id1064918-id1084107)
  - [Радар блокировок (плагин Remnawave) [id=1062871, id=1069403](https://t.me/c/2941121338/1062871)](#радар-блокировок-плагин-remnawave-id1062871-id1069403)
  - [bedolaga-cabinet: переделка ссылок [id=1007274](https://t.me/c/2941121338/1007274)](#bedolaga-cabinet-переделка-ссылок-id1007274)
- [Период 09–20.08.2026 — Remnawave 3.2.3/3.3.0, Bedolaga v4.1.0 (GeoCheck)](#период-0920082026--remnawave-323330-bedolaga-v410-geocheck)
- [Период 20–23.08.2026 — совместимость 2.8.x/3.2.2, GHCR, пин-борда](#период-2023082026--совместимость-28x322-ghcr-пин-борда)

</details>

---
<!-- /KB:HEAD -->

## Период 23.08–07.09.2025 — Bedolaga v2.0.x–2.2.x, Remnawave 2.1.x

- **Bedolaga Bot Admin Panel (Telegram)** — Юзеры и Подписки / Промокоды и статистика / Коммуникации / Настройки / Системные функции [id=7268](https://t.me/c/2941121338/7268); мониторинг серверов [id=14284](https://t.me/c/2941121338/14284); логи, модераторы/SLA [id=15132,19736](https://t.me/c/2941121338/15132).
- **Remnawave Admin** — `http://remnawave:3000` / `http://remnawave-scheduler:3000` [id=25099,43239](https://t.me/c/2941121338/25099); сквады=серверы/страны, профили=Xray-конфиги, хосты=ноды [id=1050](https://t.me/c/2941121338/52/1050).
- **remnawave-admin (Case211/remna-ad)** — [Case211/remna-ad](https://github.com/Case211/remna-ad) [id=22877](https://t.me/c/2941121338/22877).
- **Bedolaga Web Cabinet / MiniApp ЛК** — MiniApp как ЛК [id=19736,24979](https://t.me/c/2941121338/19736); Web API [id=18904,58548](https://t.me/c/2941121338/18904); Swagger `/docs` `/redoc` [id=18904](https://t.me/c/2941121338/18904).
- **bedolagam.ru / платная вебадминка** — ~1000₽/мес (лайт бесплатно) [id=18799,26220](https://t.me/c/2941121338/18799); делает сторонняя команда [id=18830](https://t.me/c/2941121338/18830).
- **eGames панель** — [wiki.egam.es/external-api](https://wiki.egam.es/ru/configuration/external-api/) [id=1756](https://t.me/c/2941121338/1756).

## Период 12.11.2025–01.01.2026 — Bedolaga v2.7–2.9.4, Remnawave 2.3–2.4

- Встроенная ТГ-админка бота: триалы, сервера=сквады [id=78649,63994](https://t.me/c/2941121338/78649), `SIMPLE_SUBSCRIPTION_SQUAD_UUID` — сквад Быстрой покупки [id=119897](https://t.me/c/2941121338/119897), «выдавать триалам» [id=78793](https://t.me/c/2941121338/78793), `PRICE_30_DAYS` [id=65545](https://t.me/c/2941121338/65545), `SUPPORT_USERNAME` [id=128927](https://t.me/c/2941121338/128927), `CHANNEL_IS_REQUIRED_SUB` [id=128919](https://t.me/c/2941121338/128919).
- Веб-админка Bedolaga — https://bedolagam.ru 2500₽/мес мониторинг+тикеты [id=84666,84713,86979,108515](https://t.me/c/2941121338/84666); конструктор меню `/menu-layout` GET/PATCH [id=124963,125758](https://t.me/c/2941121338/124963); правка менюшки с подпиской скоро бесплатно [id=125848,121319](https://t.me/c/2941121338/125848).
- remnawave-ad Case211 [Case211/remna-ad · releases](https://github.com/Case211/remna-ad/releases/tag/v0.2) [id=85324](https://t.me/c/2941121338/85324) — HWID, сквады.
- bedolagam.ru — публичная админка Egor [id=108515](https://t.me/c/2941121338/108515).
- Сторонние: Jolymmiels/remnawave-telegram-shop, machka-pasla/remnawave-tg-shop [id=132963](https://t.me/c/2941121338/132963); nginx UI [id=128901](https://t.me/c/2941121338/128901); DigneZzZ/remnawave-scripts [id=97750](https://t.me/c/2941121338/97750).

## Период 09.02–13.03.2026 — Bedolaga v3.9–3.32, Remnawave 2.6.x, Remnawave-admin 2.x

- Remnawave Admin [Case211/remnawave-admin](https://github.com/Case211/remnawave-admin) TG [@remnawave_admin](https://t.me/remnawave_admin); порт агента = backend :8081 [id=270396](https://t.me/c/2941121338/270396).
- Web-админка бота WEB_API_ENABLED=true :8080; Кнопки — Настройки→Интерфейс→Кнопки [id=232068](https://t.me/c/2941121338/232068); редактор меню RBAC settings:edit [id=269107](https://t.me/c/2941121338/269107).

## Период 16.03–06.04.2026 — Remnawave 2.7.x (breaking), Bedolaga v3.33–3.45

- remnawave-admin v2.7.4 Case211 [id=277925](https://t.me/c/2941121338/277925); Bedolaga web-админка: приветственный текст [id=317099](https://t.me/c/2941121338/317099), платёжные методы раздельно [id=317175](https://t.me/c/2941121338/317175), тикеты [id=322266](https://t.me/c/2941121338/322266), неактивные 3м [id=322411](https://t.me/c/2941121338/322411), RBAC [id=305806](https://t.me/c/2941121338/305806) ENV суперадмин [id=285614](https://t.me/c/2941121338/285614), новости [id=288963](https://t.me/c/2941121338/288963); bedolagam.ru/mintlify доки; miniapp legiz-ru/my-remnawave, maposia; RWA TestFlight potato.cc [id=314697; id=314971](https://t.me/c/2941121338/314697); kener/cachethq, beszel, crowdsec, traffic-guard [id=276623](https://t.me/c/2941121338/276623); фильтр ноды JSON [id=315895](https://t.me/c/2941121338/315895); балансер/сквады/мультиподписка: balancer теги [id=274045](https://t.me/c/2941121338/274045), leastping/leastload [id=276618](https://t.me/c/2941121338/276618), мультиподписка [id=302561](https://t.me/c/2941121338/302561), лимиты трафика multiplier 0/1 [id=310474; id=309942](https://t.me/c/2941121338/310474), профили 1:1 [id=327628](https://t.me/c/2941121338/327628); ресурсы 2/4→4/8 [id=308925; id=316902](https://t.me/c/2941121338/308925).

## Период 06–25.04.2026 — Bedolaga v3.45–3.52, Remnawave-admin 2.9–2.11

- Remnawave Admin Case211 v2.9.4/v2.10.0/v2.10.4/v2.11.0; канал [@remnawave_admin](https://t.me/remnawave_admin).
- Бот-админка: Админка → система → настройки [id=342394](https://t.me/c/2941121338/342394); Настройки → Кнопки [id=389527](https://t.me/c/2941121338/389527).
- bedolagam.ru / docs — только через VPN; зеркало [bedolagadev.mintlify.app](https://bedolagadev.mintlify.app/) [id=380651,397990,388749](https://t.me/c/2941121338/380651).

## Период 25.04–15.05.2026 — Bedolaga v3.49–3.55, Cabinet 1.49–1.52

### remnawave-admin (Case211) — см. Релизы
- Репозиторий: [Case211/remnawave-admin](https://github.com/Case211/remnawave-admin) [id=416384](https://t.me/c/2941121338/416384)
- Миграции: `docker compose exec remnawave-admin-bot alembic upgrade heads && docker compose restart remnawave-admin-bot` [id=429338](https://t.me/c/2941121338/429338)
- Путь: `/opt/remnawave-admin` [id=499253](https://t.me/c/2941121338/499253)
- **Защита триалов**: «remnawave-admin ищет по схожим hwid + ip; снизил триал со 100 ГБ до 25 ГБ и 3 дней» [id=429490](https://t.me/c/2941121338/429490)
- **Мониторинг потребления трафика**: пункт «🔥 Мониторинг скорости потребления трафика с настраиваемыми порогами» [id=473514](https://t.me/c/2941121338/473514); путь «Бот → админка → настройки → настройки мониторинга → управление уведомлениями» [id=473505](https://t.me/c/2941121338/473505)
- «Атаки на Remnawave Admin (BIF): "Я когда делал все к хуя отвалилось"» [id=453180](https://t.me/c/2941121338/453180); «"rwa admin" только с указанием cookie получает доступ к api ремны» [id=436964](https://t.me/c/2941121338/436964); «отключать куки — стрелять себе в ногу» [id=436970](https://t.me/c/2941121338/436970)
- **Защита панели**: «fail2ban + crowdsec как защита от сканов» [id=414896](https://t.me/c/2941121338/414896); «Защита на панели с MFA» — в приложении не нашёл, «не важно, оно к апи подключается» [id=428163, 428249](https://t.me/c/2941121338/428163)

### Web-админка бота (штатная Bedolaga)
- Редактор меню (визуальный) — в админке кабинета, версия от 3.52.1/1.49.0 [id=410861](https://t.me/c/2941121338/410861).
- Как включить сквад, если юзер создаётся без сквада: в настройках тарифа [id=412286, 412303](https://t.me/c/2941121338/412286).
- Платёжные методы включаются в настройках бота / админке кабинета `/admin/payment-methods` [id=447586, 446660, 446680](https://t.me/c/2941121338/447586); секция оплаты есть и в админке, и в кабинете.
- «Один рестарт докера после правки настроек в кабинете не нужен для платёжек» [id=446690](https://t.me/c/2941121338/446690).
- Инфо-страницы (текст соглашения/правил) — в боте; в кабинете: панель → настройки → политика/факу/оферта [id=453000–453031](https://t.me/c/2941121338/453000).
- Группы скидок: создать группу, куда попадают все, потратившие N рублей [id=429374](https://t.me/c/2941121338/429374).
- Кастомные аудитории для рассылок через кабинет [id=434680](https://t.me/c/2941121338/434680).
- Переопределение `.env`: кабина переопределяет .env; для переноса на другой сервер настройки сохранятся [id=471701, 464835](https://t.me/c/2941121338/471701).
- Авторизация в кабинете теперь в разделе **Login Widget** (OAuth), не в Bot Settings [id=421994, 422022](https://t.me/c/2941121338/421994).
- «Как убрать кнопки "Оферта" и прочие» [id=434675](https://t.me/c/2941121338/434675) — через `SKIP_RULES_ACCEPT`/`LANGUAGE_SELECTION_ENABLED`; «В оферте — принять» не показывается при режиме «кабинет»; чтобы показывалось — юзера удалить и добавить заново [id=417607, 420145](https://t.me/c/2941121338/417607).
- В BotFather (miniapp) страница «Language selection» — по умолчанию выключить [id=417619](https://t.me/c/2941121338/417619).
- Смена короткого имени/названия логотипа: «название такое же? или прокинул в докер с новым?» [id=461392](https://t.me/c/2941121338/461392).
- Управление кнопками бота (текст, порядок, свои кнопки) — плагин кабинета, образец github.com/systemmaster1200-eng/remnawave-STEALTHNET-Bot [id=511724](https://t.me/c/2941121338/511724).
- Убрать поддержку в кабинете: «Админка настройки, удалить его с бота» [id=514480](https://t.me/c/2941121338/514480).

### Bedolagam / документация
- [docs.bedolagam.ru](https://docs.bedolagam.ru/) (периодически недоступна) [id=406531](https://t.me/c/2941121338/406531); зеркало (открывается без VPN): [bedolagadev.mintlify.app/setup](https://bedolagadev.mintlify.app/cabinet/setup) [id=406334, 430887, 460190](https://t.me/c/2941121338/406334); «у тебя ру в директ — документация с ру не открывается» [id=460190](https://t.me/c/2941121338/460190)
- Quickstart: [docs.bedolagam.ru/quickstart](https://docs.bedolagam.ru/getting-started/quickstart) [id=459640](https://t.me/c/2941121338/459640)
- Env-референс кабины: [docs.bedolagam.ru/getting-started](https://docs.bedolagam.ru/getting-started/environment#cabinet-личный-кабинет) [id=463548](https://t.me/c/2941121338/463548)
- Telegram OIDC: [docs.bedolagam.ru/telegram-oidc](https://docs.bedolagam.ru/cabinet/telegram-oidc) [id=435180](https://t.me/c/2941121338/435180)
- Proxy-config (в доке не хватает заголовков, дословно) [id=435195](https://t.me/c/2941121338/435195):
```
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
server {
    listen 443 ssl http2;
    server_name cabinet.example.com;
```
- «Дока Bedolaga: при установке по доке реверс-прокси не поставил — из-за этого вебхук не работает; по доке это отдельный шаг» [id=416941](https://t.me/c/2941121338/416941). Ошибка в доке: «при попытке посмотреть лог написано ввести remnawave_bot, а выдаёт ошибку — надо ввести чисто `bot`» [id=435226](https://t.me/c/2941121338/435226).

### Прочие панели управления
- **Jolymmiels/remnawave-telegram-shop**, **machka-pasla/remnawave-tg-shop** — магазины-панели [id=404708, 464551](https://t.me/c/2941121338/404708)
- **maposia/remnawave-telegram-sub-mini-app** — miniapp-панель [id=404708](https://t.me/c/2941121338/404708)
- **legiz-ru/my-remnawave** [id=404708](https://t.me/c/2941121338/404708)
- **eGamesAPI/remnawave-reverse-proxy** [id=404708](https://t.me/c/2941121338/404708)
- **MTProto-панели**: `github.com/DedusVPN/mtproto-panel`, `github.com/SamNet-dev/MTProxyMax`, `github.com/amirotin/telemt_panel` (полноценная UI-панель для Телемта одного сервера), `github.com/lost-coder/panvex` (панель управления Телемтом, включая ноды) [id=497013, 497973](https://t.me/c/2941121338/497013)
- **Dockge** — графическая надстройка над Docker (редактировать конфиги, стопать, пересоздавать контейнеры), папка `/opt/stacks` вместо `/opt` [id=412779](https://t.me/c/2941121338/412779)
- **«Лайка» — сервис-аналог бедолаги** [id=425903](https://t.me/c/2941121338/425903)
- **Fedarisha** — «собственный протокол», интегрирован с xray-core и Remnawave (форки v2rayN/v2rayNG), $4000 [id=490275](https://t.me/c/2941121338/490275)
- **XBM (Xray Balancer Middleware) 3.1.1** — прослойка балансировки: автобалансировка, leastLoad (задержка+потери), фейловер <1 мин, LTE-логика с tier-системой (основа → резерв tier1 → tier2), фильтрация по CPU/RAM/онлайну, rate limit по HWID/IP, кэш подписки, sticky-session; $200 [id=486010, 507790](https://t.me/c/2941121338/486010)
- **Remnawave API к одной панели несколько ботов** — «И так тоже))» [id=459802, 459806](https://t.me/c/2941121338/459802)
- **Опенклау**: «одно из приложений под панель» [id=419669](https://t.me/c/2941121338/419669)

---

## Период 16.05–05.06.2026 — Bedolaga v3.56–3.58, Remnawave-admin 2.14

- Remnawave Admin v2.14.0 [id=534082](https://t.me/c/2941121338/534082) — Prometheus/Grafana, /metrics Bearer, 5 дашбордов.
- Связка Remnawave Admin ↔ Bedolaga API [id=541474](https://t.me/c/2941121338/541474)[id=541888](https://t.me/c/2941121338/541888):
```
WEB_API_DEFAULT_TOKEN=<openssl rand -hex 32>  (в .env Bedolaga)
BEDOLAGA_API_URL=https://your-bedolaga-bot-domain.com  (или .../api если Caddy)
BEDOLAGA_API_TOKEN=<тот же токен>  (в .env remnawave-admin)
```
Перезапустить оба; частый фикс `BEDOLAGA_API_URL=WEBHOOK_URL` [id=542232](https://t.me/c/2941121338/542232).
- bedolagam.ru / docs: [docs.bedolagam.ru](https://docs.bedolagam.ru/) [id=635052](https://t.me/c/2941121338/635052), зеркало [bedolagadev.mintlify.app/quickstart](https://bedolagadev.mintlify.app/getting-started/quickstart) [id=640272](https://t.me/c/2941121338/640272).
- Web-админка бота: приоритет .env над БД [id=552453](https://t.me/c/2941121338/552453).

## Период 07–26.06.2026 — Bedolaga 3.60–3.61, Subscription-page 7.2.5/7.2.6

- remnawave-admin Case211 2999₽ [id=689837](https://t.me/c/2941121338/689837)
- bedolagam.ru [id=683551](https://t.me/c/2941121338/683551)
- Доступ к панели → безлимит [id=691102](https://t.me/c/2941121338/691102); саб-линк random(24,30) [id=735471](https://t.me/c/2941121338/735471)
- Кнопки Админка-настройки-кнопки [id=713188](https://t.me/c/2941121338/713188)
- Промо Триалы всем [id=715163](https://t.me/c/2941121338/715163)

## Период 26.06–08.07.2026 — Remnawave 2.8.0, Bedolaga v3.61–3.62, Cabinet 1.59

- Web-админка бота: настройки→кнопки — поднять кнопку «открыть приложение» [id=761340](https://t.me/c/2941121338/761340)[id=761341](https://t.me/c/2941121338/761341); кабинет ставится по docs.bedolagam.ru [id=761346](https://t.me/c/2941121338/761346); настройки→remnawave→синхронизация [id=796285](https://t.me/c/2941121338/796285); системные страницы отключение [id=788108](https://t.me/c/2941121338/788108)
- Remnawave Admin (Case211): аномальные множественные IP разных регионов с 1 подписки → перевыпуск (2.7.0+, net_cap кик) [id=772426](https://t.me/c/2941121338/772426)
- bedolagam.ru / docs: https://docs.bedolagam.ru/introduction (с VPN) [id=757626](https://t.me/c/2941121338/757626); [docs.bedolagam.ru/telegram-oidc](https://docs.bedolagam.ru/cabinet/telegram-oidc) [id=799097](https://t.me/c/2941121338/799097)
- Смена ядра Xray через панель: по умолчанию панель оверрайдит flow:"" для mux.cool; в 2.8 dev default none [id=755612](https://t.me/c/2941121338/755612)[id=755623](https://t.me/c/2941121338/755623)

## Период 08–20.07.2026 — Remnawave 2.8.1, Bedolaga v3.62–3.64, Cabinet 1.61

- **Web-админка Bedolaga** (входит в бот/кабинет): `/admin/coupons` (мастер партии оптовых купонов: тариф, дни, кол-во, оптовая цена, срок) [id=862046](https://t.me/c/2941121338/862046); `/admin/users/:id` → вкладка «Активность» [id=867446](https://t.me/c/2941121338/867446); `/recurrent-payments` — документ «Рекуррентные платежи» во вкладке админ-редактора [id=862046](https://t.me/c/2941121338/862046); дерево настроек платежей с узлом `payments_cispay` [id=916051](https://t.me/c/2941121338/916051); «Админ → Тарифы» — там создаются тарифы при `SALES_MODE=tariffs` [id=838156](https://t.me/c/2941121338/838156); «Админка → Система → Настройки → опции интерфейса» — гифт-опции [id=838809, 838824](https://t.me/c/2941121338/838809); `Настройки → Шаблоны XRAY` [id=915262](https://t.me/c/2941121338/915262); `Настройки → Подписка → happ routing` [id=915216](https://t.me/c/2941121338/915216); «Управление → нода → коэффициент трафика» [id=879142](https://t.me/c/2941121338/879142); «Аналитика → Расход трафика» [id=905398](https://t.me/c/2941121338/905398). Публичная страница купона: `/coupon/:token`, активация в кабинете (для email-юзеров без телеги) [id=862046](https://t.me/c/2941121338/862046). Рекурренты в кабинете (ЛК): «у вас теперь тоже рекуррентки появились» [id=885849|16.07.2026](https://t.me/c/2941121338/885849).
- **REMNA-ADMIN** (сторонняя панель-помощник, продаётся): 1 499 ₽ (в чате также звучит «1 599 ₽» как цена панели) [id=873126, 873187|15.07.2026](https://t.me/c/2941121338/873126). Заявленный функционал: установка Remnawave на VPS, подключение/импорт нод, VLESS Reality, gRPC+Reality, Hysteria2, Trojan TLS, SS-2022, оптимизация VPS, авто-открытие портов, Yandex CDN для xHTTP, каскадные схемы, автообновление из GitHub Releases.
- **node-diagnostic** (Case211) — bash-тулкит диагностики/тюнинга/защиты Linux-ноды под Remnawave: `https://github.com/Case211/node-diagnostic` [id=923728|20.07.2026](https://t.me/c/2941121338/923728):
  - Диагностика: 27 проверок — живая скорость 1/4-flow + мульти-CDN (ловит троттлинг по ASN), CPU steal (оверселл VPS), PSI, UDP-дропы (критично для QUIC/Hysteria2/TUIC), реально ли работает BBR, MSS-коллапс на потере, переполнение accept-queue, PMTU, loss/latency, туннели (WG/NetBird), репутация IP, блокировки популярных сервисов, открытые порты; компактный дашборд + вердикт «пригодна для видео или нет».
  - Оптимизация: sysctl-тюнинг (буферы по RAM, BBR+cake, FD-лимиты, RPS/RFS/XPS, irqbalance, NIC-offloads, MSS clamp, netdev_budget, zram), всё namespaced — откат одной командой.
  - Защита: только генерация без риска лок-аута — готовый firewall (nft/ufw) под Remnawave, fail2ban, SSH-хардненинг + `APPLY.txt` с авто-откатом правил через таймер.
  - Шейпер трафика на eBPF/EDT: per-IP лимиты полосы, whitelist для доверенных, штраф абузеру.
  - Ядро XanMod с BBRv3/BBRv1, установка с проверкой GPG-ключа, подбором сборки под CPU, без автоперезагрузки.
  - Установка ноды Remnawave / Selfsteal / NetBird / полный мониторинг (cAdvisor + node_exporter + vmagent → VictoriaMetrics) из меню.
  - Ubuntu/Debian/RHEL/Alpine, зависимости ставит сам, CI на живых дистрибутивах.
- **bedolagam.ru / docs**: `docs.bedolagam.ru` — документация (лежала 19.07) [id=916972..916982](https://t.me/c/2941121338/916972); бот поддержки/анонсов экосистемы — `BedolagamNaPivoBot` [id=835847, 902763](https://t.me/c/2941121338/835847).
- **«Кабина» в боте** — раздел, где mini app = кабинет [id=864868](https://t.me/c/2941121338/864868).
- Прочее: «ВСкай панель» + API хостера = «5 минут АФК на ноду» при массовом изменении SSH-портов/рутов на флоте [id=848824|11.07.2026](https://t.me/c/2941121338/848824). Упоминание сторонней панели: `SteathNet panel (StealthNet_sup)` — в чате к ней относятся скептически [id=861071, 861091|13.07.2026](https://t.me/c/2941121338/861071).
- Мониторинг-эталон для панели/бот-инфра: Prometheus + Grafana + cAdvisor + node-exporter на дедике; «бесзель»-мониторинг меньше потребляет; шаблон для ремны лежит на github [id=850467, 850518, 850519|11.07.2026](https://t.me/c/2941121338/850467).

---

## Период 20–31.07.2026 — Bedolaga v3.66/3.67 + Cabinet 1.64 (рекурренты Platega/Lava)

- Админка Bedolaga: статус СБП-автооплаты в карточке юзера [id=962143](https://t.me/c/2941121338/962143).
- Веб-кабинет Bedolaga: «дрочишь там оплата впн» [id=992427](https://t.me/c/2941121338/992427); «квоты» не в приоритете [id=939420](https://t.me/c/2941121338/939420); `/api` на 8080 [id=998867](https://t.me/c/2941121338/998867).
- Кабинет от DDoS: «под КФ + ОВХ неубиваемо» [id=1003152|bypara](https://t.me/c/2941121338/1003152); «яша-кф-овх» [id=1003170](https://t.me/c/2941121338/1003170); «через наш сдн» [id=1003206](https://t.me/c/2941121338/1003206); Яша отлетит при DDoS [id=1003217](https://t.me/c/2941121338/1003217).
- v2board [v2board/v2board](https://github.com/v2board/v2board) и Xboard [cedar2025/Xboard](https://github.com/cedar2025/Xboard) [id=994291|徹夜 高橋|29.07.2026](https://t.me/c/2941121338/994291).
- Лимитер [syvlech/remnawave-limiter](https://github.com/syvlech/remnawave-limiter) [id=992162, 992463](https://t.me/c/2941121338/992162); HWID обходится кражей подписки [id=992235](https://t.me/c/2941121338/992235).
- Грейс-доступ [zavul0nn/remnawave-grace-access](https://github.com/zavul0nn/remnawave-grace-access) [id=994349|徹夜 高橋|29.07.2026](https://t.me/c/2941121338/994349).
### Защита панели
- Не держать на `panel` [id=964242 (п.9), 968820](https://t.me/c/2941121338/964242); отдельный домен 10$ [id=964242 (п.12)](https://t.me/c/2941121338/964242); поддомен `ghy7654edfvghjiuytrdfvghu7y6t5rdc.levyidomain.com` с клиентским сертификатом [id=995389](https://t.me/c/2941121338/995389); пример `pelmeni.домен.com` [id=995384](https://t.me/c/2941121338/995384).
- Доступ к API только с двух IP [id=995408, 996813](https://t.me/c/2941121338/995408); белый список IP для API [id=995407](https://t.me/c/2941121338/995407); 2222 порт [id=995417](https://t.me/c/2941121338/995417).
- Нет rate limit на auth/login [id=996830, 996834](https://t.me/c/2941121338/996830).
- «защищен буквально каждый endpoint»; «единственное наружу — канал панель-нода, и то mTLS» [id=996787, 996810](https://t.me/c/2941121338/996787).
- Атаки на сабки, панель важнее (БД) [id=959720](https://t.me/c/2941121338/959720).
- SQLi sub.madvpn.cc — дамп users/nodes/hosts/snippets [id=950403-950406|—|23.07.2026](https://t.me/c/2941121338/950403).
- Anti-DDoS панели: «берёте ВАФ/ДДосГуард/Mitelis/Turbo, закрываете порты кроме IP ВАФ; меняете сервера ремны и сабки, SSL в ВАФ» [id=965653|STEALTHNET Support|25.07.2026](https://t.me/c/2941121338/965653); «на ноды анти-ddos бесполезно» [id=993786](https://t.me/c/2941121338/993786).
- «Renmonade» — фейк-письмо [id=997813, 997795](https://t.me/c/2941121338/997813).

## Период 31.07–09.08.2026 — Remnawave 3.0.0 (ломающий), Bedolaga v4.0.0, Cabinet 1.65

### REMNA-ADMIN [id=1033967](https://t.me/c/2941121338/1033967)
Панель управления Remnawave-инфраструктурой, 2999₽: установка панели, подключение/импорт нод, управление протоколами (VLESS Reality, VLESS gRPC+Reality, Hysteria2, Trojan TLS, SS-2022), рестарт нод, логи, диагностика, оптимизация VPS, защита, Yandex CDN для xHTTP, каскадные схемы, автообновление из GitHub Releases, русскоязычный интерфейс.

### bedolaga-support (автоответчик тикетов) [id=1064918, id=1084107](https://t.me/c/2941121338/1064918)
- [AirP0WeR/bedolaga-support](https://github.com/AirP0WeR/bedolaga-support)
- MIT, Python, один контейнер, любой OpenAI-совместимый провайдер. v0.2.1, неофициальный.

### Радар блокировок (плагин Remnawave) [id=1062871, id=1069403](https://t.me/c/2941121338/1062871)
```text
🧩 Первый плагин — «Радар блокировок». Ловит блокировки по фоновому
шуму активности (оператор × хостер × транспорт). В версии 0.4.0 —
рейтинг хостеров. Пробный период 14 дней.
```

### bedolaga-cabinet: переделка ссылок [id=1007274](https://t.me/c/2941121338/1007274)
PR: [BEDOLAGA-DEV/bedolaga-cabinet#532](https://github.com/BEDOLAGA-DEV/bedolaga-cabinet/pull/532)

## Период 09–20.08.2026 — Remnawave 3.2.3/3.3.0, Bedolaga v4.1.0 (GeoCheck)

- Web-админка: Пробный [id=1101022](https://t.me/c/2941121338/1101022); выбор сквада [id=1104830](https://t.me/c/2941121338/1104830); Кнопки [id=1142053](https://t.me/c/2941121338/1142053); GeoCheck 3.3.0+ [id=1152077](https://t.me/c/2941121338/1152077)
- Case211 skill: /plugin marketplace add Case211/skill-remnawave-xray [id=1094452](https://t.me/c/2941121338/1094452) [id=1094476](https://t.me/c/2941121338/1094476)
- BEDOLAGA-DEV repos [id=1130369](https://t.me/c/2941121338/1130369); BedolagamNaPivoBot [id=1092560](https://t.me/c/2941121338/1092560); Asnumbers [id=1112197](https://t.me/c/2941121338/1112197); Vpnutka [id=1094473](https://t.me/c/2941121338/1094473); п2го панель [id=1116065](https://t.me/c/2941121338/1116065); фирстбайт [id=1086608](https://t.me/c/2941121338/1086608); CDN панели dashboard.* [id=1096190](https://t.me/c/2941121338/1096190)
- spofyltd DNS каркас [id=1084401](https://t.me/c/2941121338/1084401)

## Период 20–23.08.2026 — совместимость 2.8.x/3.2.2, GHCR, пин-борда

- **Админ-функционал Bedolaga-бота**: ручная смена типа подписки Trial→Paid через бота; **массовые действия** (повторная выдача подписки как фикс); карточка подписки в Cabinet как точка управления (запрошены: смена типа, автопродление) [id=1157934|20.08](https://t.me/c/2941121338/1157934), [id=1158091|21.08](https://t.me/c/2941121338/1158091).
- **`ADMIN_IDS`** — переменная `.env` бота для списка админов [id=1177374|23.08](https://t.me/c/2941121338/1177374).
- **Bedolaga Web Cabinet как админка** — карточка юзера/подписки + массовые действия; feature-requests: автопродление из кабинета, раздельная настройка для новых/существующих, дата сброса трафика, QR рефералок [id=1158091|21.08](https://t.me/c/2941121338/1158091), [id=1169196|22.08](https://t.me/c/2941121338/1169196).
- **Смежные сторонние админ-панели/шопы Remnawave** (из официальной пин-борды): `eGamesAPI/remnawave-reverse-proxy`, `Jolymmiels/remnawave-telegram-shop`, `machka-pasla/remnawave-tg-shop`, `DigneZzZ/remnawave-scripts`, `legiz-ru/my-remnawave`, `maposia/remnawave-telegram-sub-mini-app`, `kutovoys/xray-checker`, `dotX12/traffic-guard` [id=1173179, id=1173186|23.08](https://t.me/c/2941121338/1173179).
- **remnawave-admin (Case211)** — в заметках 169–172 не упоминается.
- **bedolagam.ru** — как домен/панель в заметках 169–172 не упоминается (упоминается только бот `@BedolagamNaPivoBot` с маркет-функциями: публикация объявления в обход лимита 24 часа, покупка закреплённого сообщения, покупка персонального тэга) [id=1169140|22.08](https://t.me/c/2941121338/1169140).
- **Сторонняя панель с API-интеграцией**: проект `shape` — добавлена поддержка панели Remnawave через API и API Shaper, `https://github.com/SkunkBG/shape` [id=1176773|23.08](https://t.me/c/2941121338/1176773).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🛠 01. Панели](README.md) › **Admin-панели**

◀ [Ошибки → фиксы](ошибки-фиксы.md) · [Кейсы и разборы](кейсы.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
