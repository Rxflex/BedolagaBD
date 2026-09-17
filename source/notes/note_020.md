# Заметка по chunk_020 (id 109852..115079, 15.12..18.12.2025)

## Selфsteal-гайд (полный, для тупых) [id=110027-110040, Egor + 17, 15.12]
Скрипт: https://github.com/DigneZzZ/remnawave-scripts#-caddy-selfsteal-for-reality
1. Caddy selfsteal ставится НА НОДЫ (не на панель/бот).
2. Направляешь поддомен на сервер с нодой, запускаешь скрипт, вводишь домен.
3. На ноде: `docker exec <ID контейнера ремнаноде> xray x25519 && openssl rand -hex 8` (privateKey первый, shortId последний короткий).
4. Профиль ноды в Remnawave:
```json
{"inbounds":[{"tag":"NODA1_VPN_VLESS","port":443,"protocol":"vless","settings":{"clients":[],"decryption":"none"},"sniffing":{"enabled":true,"destOverride":["http","tls","quic"]},"streamSettings":{"network":"raw","security":"reality","realitySettings":{"show":false,"xver":1,"target":"127.0.0.1:9443","spiderX":"","shortIds":["XXXX"],"privateKey":"XXXX","serverNames":["noda.example.com"]}}}],
"outbounds":[{"tag":"DIRECT","protocol":"freedom"},{"tag":"BLOCK","protocol":"blackhole"}],
"routing":{"rules":[{"type":"field","domain":["domain:youtube.com","domain:youtubei.googleapis.com","domain:ggpht.com","domain:ytimg.com","domain:googleapis.com"],"outboundTag":"DIRECT"},{"type":"field","domain":["domain:googlesyndication.com","domain:googleadservices.com","domain:doubleclick.net","domain:googleads.g.doubleclick.net","domain:pagead2.googlesyndication.com","domain:partnerad.l.doubleclick.net","domain:ads.youtube.com","regexp:.*pagead.*","regexp:.*doubleclick.*"],"outboundTag":"BLOCK"},{"ip":["geoip:private"],"type":"field","outboundTag":"BLOCK"},{"type":"field","domain":["geosite:private"],"outboundTag":"BLOCK"},{"type":"field","protocol":["bittorrent"],"outboundTag":"BLOCK"}]}}
```
5. Создаешь хост в Remnawave, адрес = поддомен ноды = serverNames.
6. Ютуб без рекламы: маршрут ютуб-доменов DIRECT + реклама BLOCK — работает на ру-нодах (ну или сервер, где IP в геобазах ютуба как ру).
Проверка гео IP: `bash <(wget -qO- https://github.com/Davoyan/ipregion/raw/main/ipregion.sh)` [id=112881].

## Лимит скорости на ноде (tc) [id=111693-...+ script snippet, Zavulon, 16.12]
Скрипт vps-limit.sh (в «полезностях»): apply/clear/status через tc qdisc, автоопределение интерфейса, egress limit 10mbit по умолчанию. Применение: `sudo ./script.sh apply 20mbit`. Без дропа пакетов, на fq. Zavulon: на нодах с СНИ ВК нет nginx. Альтернатива в nginx:
```
location / {
    limit_rate_after 10m;
    limit_rate 500k;
}
```
Ставится на панель/ноду с nginx [id=112693, 112697]. Мотивация: Zavulon ставит 10-20 Мбит на ноду белых списков, чтобы юзеры с ПК не съедали трафик.

## BBR и вместимость нод [id=112903, Ivan-стата]
- 1/2: BBR1 15-25 активных, BBR3 20-35
- 2/4: BBR1 40-60, BBR3 60-90
- 4/8: BBR1 ~100, BBR3 120-180
- 8/16: BBR1 200-250, BBR3 300-400
- BBR3 требует изменения ядра (модуль), скрипты с ним (SawGoD, от Ивана) пока не переключают; показывают всё равно BBR1. Пока ббр не работает: скрипт ставит оптимальные TCP-настройки.
- Панель+бот на 5к пользователей: запас x4.

## Bedolaga 2.9.x: вебхуки юкассы 403 forbidden_ip [id=113611, 113881-113978]
- Проверка IP — хардкод YOOKASSA_ALLOWED_IP_NETWORKS: 185.71.76.0/27, 185.71.77.0/27, 77.75.153.0/25, 77.75.154.128/25, 77.75.156.11/32, 77.75.156.35/32, 2a02:5180::/32; через env не настраивается.
- Бот должен видеть реальный IP юкассы через X-Forwarded-For; nginx/caddy должны передавать заголовки. Если нет — 403.
- Временный фикс (Maxim, 17.12): отключить проверку в app/external/yookassa_webhook.py:
```python
def is_yookassa_ip_allowed(ip_object: IPAddress) -> bool:
    return True
```
и `docker compose build`. Причина — nginx/caddy не передают IP.
- Юкасса с проверкой IP — оставить автопроверку оплат раз в минуту вместо вебхуков (Egor) [id=110850].
- После настройки юкассы в боте — рестарт, иначе хук не поднимется [id=111158].
- Egor планирует переменную для отключения проверки / добавления разрешённых IP в env.

## Bedolaga .env минимальный (2.9.x) [id=112179, 114099]
```
BOT_TOKEN=1234567890:AABBCCdd...
ADMIN_IDS=123456789,987654321
BOT_RUN_MODE=webhook
WEBHOOK_URL=https://hooks.domain.com
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET_TOKEN=super-secret-token
WEB_API_ENABLED=true
WEB_API_PORT=8080
WEB_API_ALLOWED_ORIGINS=https://miniapp.domain.com
WEB_API_DEFAULT_TOKEN=super-secret-token
REMNAWAVE_API_URL=https://your-panel.com
REMNAWAVE_API_KEY=your_api_key
```
- REMNAWAVE_API_URL должен быть с /api на конце для внешнего API-доступа (eGames): https://panel.vpn.ru/api [id=114508, 114515].
- BOT_RUN_MODE=polling — fallback для простого запуска [id=114100].
- Docker compose: у бедолаги есть docker-compose.local.yml (бот+панель на одном сервере); бото-кадди/нжинкс из доков бедолаги (аддон caddy конфиг в репо) [id=113541, 114090, 114099].
- docker-compose.yml с ошибкой: networks.remnawave-subscription-page с image/volumes (нельзя в network section) [id=111377].
- Аккаунт не запускается: env-приоритет (env настройки над DB). Всё что хочешь настраивать в боте — комментируй в env [id=113401, 113404].
- Ошибка "Не найдена директория модулей /tmp/lib" у скрипта от dignez — не наш, у eGames свой скрипт.
- При обновлении у бота слетают права на папку с бекапами — make reload [id=113390].
- Отчеты (стата) после раскатки бекапа не работали [id=114120].

## Bedolaga 3.0 (75%+ готовности) [id=114978, 114988]
- Тарифы (безлимит на устройства / оплата за трафик) будут [id=114961, 114980, 114982].
- Разные картинки на разные менюшки/разные локали [id=115006, 115008].
- Промогруппы/рефактор.
- Научный отчет: c0mrade открыл опенсурс тикеты для бедолаги (в разработке) [id=114166].
- «BedolagaKYC» шутка от Ивана.
- Bedolaga в web-админке (eGames скрипт) — не дает ошибок API [id=112262].

## Bedolaga баги/фичи
- Disable у юзеров после истечения подписки [id=112783].
- Купон на 1 день даёт 100 дней триала (баг, кибер-промо) [id=114545, 114554].
- disable юзеры (нельзя сбросить) [id=112783].
- Рефка промо: при неверном промокоде на этапе рефки не возвращает в меню и кнопки нет; после рестарта так же [id=113426].
- Telegram лимиты: chat manager 50 сообщений; боты не могут тегать всех в чате.
- disable_web_page_preview — просили переменную в env [id=114220].
- Дизейбл юзеров на ~1000; авто-подключение инбаундов при обновлении [id=113532].

## Ошибки нод
- nginx: could not build server_names_hash → в http добавить `server_names_hash_bucket_size 64;` [id=114513, 114521].
- Xray: `Failed to start: failed to listen TCP on 9999... address already in use` — порт 9999 занят чем-то (на ноде, контейнер, сс слушает?); в другой ВПС все 9999 один и тот же. [id=114755-114770]
- ss-конфиг: не сработал; shadowsocks недостает.
- Бекап-бот: бекапы 1 раз в час [id=113451].
- Разнобой версий: если update до 2.9.1 не работает кнопка подключения в happ — фикс в 2.9.1 [id=113446-113449].

## Конкурсы (Gy9vin)
- В боте появился раздел конкурсы; отключать кнопку пока нельзя (через код), функционал будет [id=110425].
- Бот-недостаток: вывода на карту и кнопки купить [id=114595].

## Платежки
- ЮKassa: webhook юкассы — надо указать URL в ЛК юкассы (POST /yookassa-webhook). URL: `https://hook.domain.com/yookassa-webhook` [id=111150, 113612].
- После настройки юкассы — рестарт бота.
- Платега: вывод через манагера в рубли на карту (п2п) — приходят как пополнение от юрлица, не перевод [id=113430, 113473].
- Робокасса: 1.8% СБП для юрлиц (3.5% самозанятые, чеки включены) [id=109933, 109935-109947].
- Юкасса: чеки НЕ включены (требуют налогового API), ФНС гайд через `pypi.org/project/nalogo/` [id=109975].
- Юкасса запрещает слово «впн» и т.п. — «заувалированно»: меняем на «защищенное подключение» и т.п. [id=110446, 110260?].
- Иные: Telegram Stars, Tribute, CryptoBot, Heleket, YooKassa, MulenPay, PayPalych, Platega, WATA.
- У каждого свой мин. чек.

## Бедолага 2.x→3.x: веб-админка (частично упоминалась) 
- «Доп услуги» — скидка на доп. услуги (не сказано что именно).
- «Купи подписку» — у бедолаги 2.9.x убирается выбор типа серверов: "Можно так же, но это...".
- Продажа двух серверов с разным тарифом — решение через промогруппы (100% скидка на трафик) или два бота (чистый vs БС) [id=114940, 115011-115028].
- «Хочу пейворл как у hit vpn» — простая большая кнопка «ВКЛ» [id=114595-114650].

## Хостинги (новое)
- Bill (promoted) — сотрудник удалил все серверы; обещают 24ч и компенсацию; вывод баланса не всегда; Egor у них panel; многие уехали на dhost [id=112629, 113145, 114936?]. Bill — promocloud? [id=112678].
- beget.com — ру/каз, 220р 1/1/10, 660р 2/2/30, 664.5 2/4/20, бесплатные бекапы, 250 мбит, под панели ок; Казахстан (Kaz) тоже ок; Норвегия дешевле и стабильная [id=112830].
- hostkey.ru — дешевые VPS, много стран, но касса (касс-зал?) [id=110168, 110086].
- AdminVPS — ненадежный: уничтожил сервер после техработ, 499р/1/2/30, дропы [id=112905].
- qwins.co — дропы, в Польше вышково (не Варшава) [id=112905].
- dhost — топ, панель восстановил туда [id=113492]; Германия у них сыровата, NL лучше; хостинг раздатчик (наливка).
- play2go — иногда падает [id=114084].
- 4vps — ру, дешево, но всё разобрали, остался Питер [id=111995].
- hostvds.com (ref) — руки Фина на 1 долар, доп. оплата анлим; их DNS-геобазы плохо обновляются [id=114435].
- Procloud — Польша/США/Каз/Беларусь, Польша норм [id=113393, 113410].
- Kyonix, 1centhost, DHost — Германия [id=113490].
- Senko — «пока классная Германия» [id=115048].
- XorekCloud — много трафика [id=115044].
- hostoff.net?ref=CHAT — 20% скидон, WG работает [id=112572].
- weasel.cloud — привет [id=113154].
- hostkey.ru — и нидерланды дешевле [id=110168].
- Serva.one — USA скорость говна [id=112263, 113503].
- Terr: все хосты в dhost, DHOST Admin [id=110349].

## Bedolaga панель (бот-скрипты)
- eGames https://wiki.egam.es/configuration/external-api/ — внешний API доступ [id=114512].
- wrx861/bedolaga_auto_install — авто-установщик бота (github) [id=113551].
- «BezSel» (bbr-control script) — упоминания: bbr не работает.
- Скрипты DigneZ — проблемы при рестарте бота с API ремня (черный докер — net) [id=112924].

## Разное
- CrowdSec: установка с зональными (apt crowdsec + firewall-bouncer-iptables), вайтлист в /etc/crowdsec/parsers/s02-enrich/whitelist.yaml, занимает 8080 порт по умолчанию (менять), эффективность через общую базу с пакетами [id=110951].
- Trip by каждый день: выводят каждый будний день с 21:00 до 22:00 по МСК (это про вывод?) [id=111600 — контекст про вывод, в контексте вывода средств].
- Юкасса принимает только русские IP: сервер с ботом должен быть в РФ или через SS+Privoxy/Юмани-белый список [id=110440].
- «Юкасса скоро сливается» — слух [id=109926].
- Server routing: docs.rw/docs/learn/server-routing/ — для роутинга на .ru/.gov: лучше отдельный ру-сервер (все три ноды с 1 ру-хоста скорость просядет) [id=112821]. Routing реалити+SS — базовый вариант, ру-нода грузится x2 при реалити.
- ipv6 на нодах — выключать в РФ (по дефолту выключать) [id=114142].
- Пинг в Happ ≠ реальный; реальный через ping <IP> или с ПК [id=114058-114084].
- Впс-заглушки для бесплатной подписки: hostvds $0.99 50 мбит [id=111044-111049].
- Нода и бот на одном сервере — не рекомендуется (бедолага бится с нодой за порт 80/443) [id=113235, 113297].
- 80 порт занят nginx: `systemctl stop nginx` перед установкой ноды, потом старт [id=113247].
- «Обновляйтесь вовремя» — 2.3.6 → откат на 2.3.2 [id=112790].
- Bedolaga бот в стране — бедолага-бот меняет статус: активирует подписку, юзер подписывается [id=82226-82227 из chunk15].
- Бекапы distillium: с postgres 18 не восстанавливает сам, нужно вручную [id=114571].
- Bedolaga - бекап по кнопке бот: restore «стереть и восстановить», в /data/backups [id=110336-110339].
- .env и docker compose: не перепутать POSTGRES_PASSWORD default в compose (secure_password_123) [id=113945].
- Beget 250мбит/порт; продление показывает после аренды [id=110394].
- «Осложнения» для RU: janky-BBR hostings.

## Разное
- Bedolaga бот - логика с сертификатами: порты 8088:80, 8443:443 для мinапp [id=110888].
- Bedolaga: 2.9.1→2.9.2; замена орфографии в чате.
- Обновление ремны до 2.3: после обновления подписки не работают - синхронизируй серверы [id=111369-111583].
- bedolaga api от Yandex Claude: PGC: страница Поддержка конфигурации устройства [id=113195].
- «BedolagaKYC» [id=87000].
- Ронавая: remnawave notifications - подписки при продлении (частично).
- Сни «vk» для ру-нод [id=113515].
- «Скрипт от dignez годный» - негативный отзыв: сам не привязал домены к нжинксу, ошибки в процессе [id=112271].
- Bug: Bedolaga удаляет привязку к подпискам в панели (ошибка: https://sub...) [id=114766].
- Идея: пред-фикс от РКН: репорт подсетей.
- Пинг: 1Сент.
- Bedolaga админка: показ скрытых файлов в SFTP [id=110314-110317].
- «proksi» мульти-платежка: разработкаDeleted Account (касса для всех) [id=113538].
- Проект UPGen (unblockable) — генератор протоколов, «не смогут заблочить» [id=112064, 112087]; proteus (unblockable) [id=112099].
- Bedolaga: web_api - INFO - GET /health -> 401 — норм (токен) [id=88825, 112264?].
- Работяга: I.Cent, IM и субы. Крыс.
- Telegram Bot star-based payouts: bedolaga-пиво бот (BedolagamNaPivoBot).
- ИИ-выбор: Qwen/Gemini/DeepSeek (версии и качество) [id=109908?].
- Bedolaga статистика: remnawave-nginx/redis потребление, ~370MiB RAM панель, DB 76MiB, redis 8MB, место 8.6G/118G при 40+ юзерах [id=112263].
- бесплатные: cloudflare - сканеры caddy - нет.

## Платежки юбилей
- Юкасса: если не понимаешь чеки — юкасса не даст "авто" чеки, только сам.
- Freekassa — добавление ожидается? (вопрос art vs) [id=113433].
- netlify — нет.
- Где взять urlpay - ugad.
- Bedolaga конфликт env (лучше закомментировать не нужное).

## Прочее
- Zavulon скрипт vps-limit.sh (смотри выше) — рецепт 10-20 Мбит на бс-ноду.
- «I.Cent» — самый не рекомендованный хостинг (не отвечает ТП) [id=113159].
- 1cent — ТП с 26 октября не отвечает; пакеты терялись [id=114155-114159].
- Bedolaga: полезные репы (звёзды): remnawave/panel, BEDOLAGA-DEV/..., kutovoys/xray-checker, eGamesAPI/remnawave-reverse-proxy, Jolymmiels/remnawave-telegram-shop, machka-pasla/remnawave-tg-shop, DigneZzZ/remnawave-scripts, distillium/remnawave-backup-restore, maposia/remnawave-telegram-sub-mini-app, legiz-ru/my-remnawave.
- Донация на «свитер Юре Кастову» (@tsdev, Papa Remnawave) — 20000 ₽ цель, 9650 ₽ собрано на 18.12 [id=114989].
- Bedolaga 2.9.2 ночью (Egor) — фикс статов [id=111466].
- Ремна 2.3.0: подписки не отдают ссылку юзерам — обнови бота / откат [id=111369].
- subnet listing: YOOKASSA_ALLOWED_IP_NETWORKS перечислены выше.
