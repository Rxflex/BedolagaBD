# Заметки из chunk_029 (id 173628..179725, период 16.01.2026 .. 18.01.2026)

## Bedolaga: релизы v3.1.0 (18.01) и веб-кабинет v1.1.0
- **[id=178078|Egor|18.01]** **#v3_1_0 «Новые типы промокодов и бонусов РК, улучшенный мониторинг, багфиксы»**:
  1. **Улучшенный мониторинг по нодам by @Gy9vin** — env-блок полностью (пересказ с переменными):
```
# ===== МОНИТОРИНГ ТРАФИКА =====
TRAFFIC_FAST_CHECK_ENABLED=false
TRAFFIC_FAST_CHECK_INTERVAL_MINUTES=10
TRAFFIC_FAST_CHECK_THRESHOLD_GB=5.0
TRAFFIC_DAILY_CHECK_ENABLED=false
TRAFFIC_DAILY_CHECK_TIME=00:00
TRAFFIC_DAILY_THRESHOLD_GB=50.0
SUSPICIOUS_NOTIFICATIONS_TOPIC_ID=14
TRAFFIC_MONITORED_NODES=
TRAFFIC_IGNORED_NODES=
TRAFFIC_EXCLUDED_USER_UUIDS=
TRAFFIC_CHECK_BATCH_SIZE=1000
TRAFFIC_CHECK_CONCURRENCY=10
TRAFFIC_NOTIFICATION_COOLDOWN_MINUTES=60
TRAFFIC_SNAPSHOT_TTL_HOURS=24
```
  Логика: при запуске создаётся snapshot трафика всех юзеров; через интервал проверяется дельта; превышение порога → уведомление админам [id=174290|Gy9vin: 12 ГБ за 10 минут на инсте].
  2. **Промокод на разовую скидку** @libkit.
  3. **РК без бонусов и с бонусом на тариф**.
  Множественные багфиксы. Обновление: `cd /root/remnawave-bedolaga-telegram-bot && git pull origin main && make reload` / `make reload-follow` / веб-админка bedolagam.ru.
- **[id=178082|Egor|18.01]** **Web Cabinet #v1_1_0**: Все HTTP запросы через Axios; CSRF защита; DOMPurify санитизация; валидация deep links; защита от open redirect; безопасная обработка токенов; Admin Route защита; runtime-валидация ответов API; валидация URL для buttonLink; Debounce/throttle; рейтлимиты; правки платежек; новые разделы в админке: Рассылки, Промокоды, Промопредложения, Кампании, Пользователи, Платежи, Remnawave. **🚨 Необходимо предварительное обновление бота до версии v3.1.0!**
- **[id=173476..173487|16.01]** (из предыдущего чанка, повтор) 3.0.0: веб-кабинет, суточные тарифы, умная докупка трафика (каждый пакет живёт свои 30 дней), лимиты докупки; CABINET_ENABLED/CABINET_JWT_SECRET/CABINET_ALLOWED_ORIGINS; старая /miniapp/ будет удалена в ближайшие дни.
- **[id=177569..177570, 177584|17.01]** Егор тестил кабинет на базе 100k+ юзеров; 3.0.1 на подходе; «Юра Кастов прости и не бей за RemnaWave, я поправлю».
- **[id=177804|BedolagamNaPivoBot|17.01]** В посты добавлен второй репозиторий: BEDOLAGA-DEV/bedolaga-cabinet.
- **[id=178690|Pedzeo|18.01]** «Miniapp будет удален из репозитория бота в ближ время».
- **[id=178529..178532, 178739|18.01]** Кабинет: обучение для «совсем даунов» при первом запуске; админка из кабинета.

## Bedolaga/Cabinet: установка и настройка (16–18.01)
- **Установка кабинета** — вручную, из отдельного репо (github BEDOLAGA-DEV/bedolaga-cabinet):
```
git clone https://github.com/BEDOLAGA-DEV/bedolaga-cabinet.git
cd bedolaga-cabinet
cp .env.example .env (настроить)
nano .env
docker compose up -d --build
```
[id=173909|torro xD, 174501..174510]
- **Docker-образ не пуллится** («pull access denied», «error from registry: unauthorized», 403 Forbidden) — приватный репо, собирайте сами: `docker compose build`; либо `docker pull fr1ngg/bedolaga-cabinet:latest` (авторский образ) [id=173702..173706, 173838..173847, 174501..174510|zyko/hdhdh/torro xD/Евген].
- **Cabinet docker-compose** (внутри только фронтенд, без открытых портов, только в docker-сети) [id=174488..174494|xexe]:
```
services:
  cabinet-frontend:
    image: ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
    container_name: cabinet_frontend
    restart: unless-stopped
    networks:
      - bot_network
networks:
  bot_network:
    external: true
    name: remnawave-bedolaga-telegram-bot_bot_network
```
- **Nginx-конфиг для кабинета** (cabinet.domain.com) [id=174773, 175058, 178315..178353|xexe/financetroubles]:
```
location /api/ {
    rewrite ^/api/(.*) /$1 break;
    proxy_pass http://remnawave_bot_unified;   # или backend_bot:8080
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
location / {
    proxy_pass http://cabinet_frontend:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_intercept_errors on;
    error_page 404 = @fallback;
}
location @fallback {
    rewrite ^ /index.html break;
    proxy_pass http://cabinet_frontend:80;
    proxy_set_header Host $host;
}
```
- **Caddy для кабинета** (из README) [id=173966, 174526..174529|torro xD]:
```
handle /api/* {
    uri strip_prefix /api
    reverse_proxy название_контейнера_бота:8080
}
```
- **Порты кабинета**: фронтенд слушает 80 внутри контейнера; для хоста — `${CABINET_PORT:-3000}:80` или на другой порт (3020) [id=174230..174231, 178843..178890].
- **Бэкенд (API) бота** — порт 8080 (WEB_API); кабинет через `http://backend_bot:8080` (docker-сеть) или `VITE_API_URL=https://bot.example.com/api` [id=173966..173976, 174508..174510, 178901..178904].
- **Авторизация в кабинете через ТГ** — нужен **домен в BotFather** (Bot settings → Domain) [id=175067..175078|wsq22, 175813..175814|Miya]. Домен должен совпадать с тем, что указан в .env кабинета [id=174429|xexe].
- **env кабинета**: VITE_TELEGRAM_BOT_USERNAME, VITE_API_URL, CABINET_ALLOWED_ORIGINS, VITE_TELEGRAM_BOT_USERNAME [id=176391..176394].
- **SMTP/email**:
```
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=VPN Service
SMTP_USE_TLS=true
```
[id=177862..177866|zyko]. Gmail: SMTP не с логином-паролем, а отдельный пароль приложения [id=176514|Sam]. CABINET_EMAIL_VERIFICATION_ENABLED=false — вериф не отключается (баг) [id=178275|xexe]. Ссылка верификации идёт с example.com → фиксовали (в auth.py/search по example.com; редирект должен идти на /cabinet/auth/verify-email? не /cabinet/verify-email?) [id=175896, 177872, 178331..178345].
- **Перенос домена/замена ссылок**: в БД replace старый домен → новый (sql update или dump → редактировать → залить) [id=178922..178960|denis/Zavulon].
- **Обновление кабинета**: `git pull origin main && docker compose down && docker compose up -d` (или `up -d --build`) [id=178111..178112, 179017..179018]. Версию кабинета в самом кабинете не посмотреть — только git tag / сравнение админки [id=179167..179169, 178190..178207].
- **Авторизация через сайт 404** — сначала `/login` в адресной строке удалить (просто домен), потом логин [id=178361..178364, 178416..178420|xexe/zyko].
- **VITE-переменные** кладутся в env кабинета, НЕ бота [id=178503|stormie].

## Bedolaga/Cabinet: баги и решения 16–18.01
- **«Telegram бот не настроен»** на сайте кабинета — домен в BotFather не задан (или не совпадает) [id=175813..175814|Miya].
- **404 при auth/telegram/callback** — прокси /api/ не на backend, или domain в BotFather не тот [id=174748..174757, 175025, 175839..175843].
- **«Missing API key»** — кабинет не настроен: API URL / X-API-Key (VITE_API_URL) в env кабинета [id=175025, 174508..174510].
- **«Bot domain invalid»** — юзернейм бота в env кабинета неверно; имя бота на странице авторизации кэшируется (нужен rebuild/кэш) [id=178369..178372, 178276..178278].
- **Утечка пользователей в заблокированные** — если бот перенесён/восстановлен, часть юзеров получила status='deleted'; фикс: в БД (users.status) перевести в active; связано не с Remna, а с ботом [id=174884, 174894..174900|Сергей/Илья].
- **Double списание при пополнении в 3.0.0** — авто-продление после пополнения баланса (не из корзины) на максимальный баланс — «задумано» (DEFAULT_AUTOPAY_ENABLED в env) [id=177634..177659|zyko/libkit].
- **Двойной учет дохода в веб-админке** — «при покупке доступа за 200 получился входящий оборот на 400» — баг, «допилим» [id=177453|Борис Бритва, 177470|Egor].
- **Monetization: «Мони из кабинета не учитываются»** — при покупке подписки через кабинет в Remna не фиксируются как оплата [id=178349..178350].
- **Локальные IP** — подписка берётся из localadmin (баланс, купоны) [id=178300..178309].
- **invalid total amount** при оплате через кабинет (напр., в Юкасса) — бот: «Логи бро, и на гх закинь» [id=177080..177082].
- **YooKassa создание платежа в кабинете** — платёж создаётся в ЮК, но не сохраняется в боте (не пополняется баланс) [id=176983..176984, 177017].
- **Кабинет не открывает банковские приложения при оплате** — «кнопка просто не жмётся» (редирект в bank) — баг, фиксят [id=177131..177135, 177826..177832|ALIEN].
- **F5 на вкладках кабинета → 404 / редирект на главную** — «React Router basename» (похоже на фикс) [id=177921..177923, 175984|𝖆𝖓𝖒𝖇𝖇/Evgeny].
- **emailed: домен с example.com в письме** — «Поиск по слову example.com» [id=178340|zyko].
- **Ссылка «подключиться» на обнову, добавление приложения в HAPP/Clash** — парсинг app-config.json, т.е. в Remna; в кабинете; happ://crypt4 через хедеры / редирект URL [id=175497..175509, 178649..178656|—].
- **«Настройка не применяется» / prices из env или из tariff** — цены кабинета с окружения env если заданы, иначе из DB кабинета [id=178090..178091|—].
- **Смена tariff / payment / подключение** — кнопки в тарифах/классике работают; оплата по бонусу/промо/промоцоде (отличаются) [id=178326..178357|—].
- **«Invalid total amount» / «Amount not set» в кабинет** — по мере добавления сумм; fixed-цены — фиксы [id=177131..177180].
- **«Сейчас платят с промо» / «начнутся обновления в 3.1»** [id=178000..178079].
- **Auto-подписание через кабинет** — «срабатывает автосписание и продление подписки. На максимальный допустимый баланс» — задумано (DEFAULT_AUTOPAY_ENABLED в env) [id=177634..177659].
- **Обновление с 2.9.x до 3.0** — миграция данных (users/subscriptions): при рестарте/обновлении у части пользователей слетает статус → в БД set active [id=174884..174900, 174921..174930|Сергей/Илья].

## Bedolaga/Cabinet: фичи 3.x (новые)
- **Веб-кабинет (3.0+)**: JWT-авторизация, TLS, CORS, React-Router с basename, админка (но создается отдельный кабинет), отображение лого/цветов, юридические тексты, сведения юзера, тема/поддержка, «деньги»/продукт, приобретение подписок (classic/tariffs), WhatsApp/TG-уведомления, банковские приложения (в кабинете не работает — баг) [id=173476..173540, 175834..175863].
- **Кабинет (новый)**: миниапка — не открывается через сайт (требуется Telegram-авторизация); банковские приложения не перенаправляют [id=177131..177152, 177826..177832|—].
- **Cabinet 1.1.0**: ручки Telegram-bot, JWT, конфиг React-Router + auth-ROUTES, mail/credit rate, ответы API, app config; «CABINET_ENABLED» [id=178082..178084].
- **Бан, вход через кабинет и HTTPS** — JWT, почтовая авторизация, «Signature» в кабинете (не для тг бота), отдельная админка (create/user через кабинет) [id=175736..175834|—].
- **База данных/обновления 2.9.x→3.0** — с миграцией юзеров; авто-миграция; статус 'deleted' у некоторых юзеров [id=174884..174934, 174921..174950].
- **Cabinet 3.0 + Remna (classic) не всегда** — юзеры в 3.0 могут «работать без личных кабинетов», «выплачен баланс» [id=177892..177900].

## Remna: платежи, операции, «простые» фичи
- **Установка кабинета — Независимая от Remna** [id=174499..174510|xexe].
- **Remna без VPN (miniapp/cabinet)** — «юзаешь, пока можно» [id=175755..175780].
- **Remna «чистая БД» и цены** [id=178295..178313].
- **«UnboundLocalError: cannot access local variable 'settings'» в YooKassa** — выгрузка окружения: удалите строчку из `/app/app/services/payment/yookassa.py`: `from app.config import settings` на стр. 667 (это дубликат) [id=176421..176422, 178197..178199, 178476|xexe/Айдар].
- **Errors /topics: pydantic «Input should be a valid integer, unable to parse string as an integer»** [id=179584] — в env строковые комментарии; исправить как `ADMIN_REPORTS_TOPIC_ID=0`, `MULENPAY_SHOP_ID=0`, `FREEKASSA_SHOP_ID=0`, `FREEKASSA_PAYMENT_SYSTEM_ID=0`, `LOG_ROTATION_TOPIC_ID=0`.
- **Мониторинг трафика**: конфиг для мониторинга шардинга/дельты по нодам; пример лога «12 гиг за 10 минут на инсте» [id=174290, 174236..174261].
- **Список/подписки** — можно смотреть «Подписки» в кабинете: `cabinet/admin/tickets` и т.д. [id=175984..175986].
- **Auto-подписание через кабинет (двойной списание)** — «Донат не засчитается епт» — DEFAULT_AUTOPAY_ENABLED в env [id=177694..177700|—].
- **Remna «Директ»** — если подписка в_remna (классик) [id=178349..178353].
- **Оплаты с «ЮKassa/Platega» при кабинетах** — банковские приложения не работают (баг) [id=177131..177180].

## Remna/Bedolaga: интеграции, SMTP, Telegram
- **Кабинет/сайт поддерживает в кабинете: mail, bot username, JWT, SMTP** [id=177862..177866].
- **Мини-апка (miniapp)** — не работает на кабинете (кабинет требует авторизацию TG через BotFather) [id=174748..174757, 174785..174843].
- **Uptime Kuma** — «h», «cabinet» [id=174972..174974].
- **SwiftServer** (панель мониторинга) [id=176727..176731|libkit/xrmqd]; все на мак, 3 сервиса; «макс. 3 сервера» [id=176733].
- **Xray-checker** — проверка трафика (типа «обход бс», «снятие скринов») [id=174994..175002].
- **Iperf3 / Censorcheck / IP.Check.Place / bench.sh / yabs.sh** — тестовые команды (с itdog) [id=179704..179711|Haxonate]:
```
bash <(wget -qO- https://ipregion.vrnt.xyz)
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode geoblock
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode dpi
bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh)
curl -sL yabs.sh | bash -s -- -4
bash <(curl -Ls IP.Check.Place) -l en
wget -qO- bench.sh | bash
bash <(curl -Ls https://Check.Place) -EI
sysbench cpu run --threads=1
```

## Remna/Bedolaga: трафик и хостинги (16–18.01)
- **Хостинги (личный опыт)**:
  - **1cent** — «падает часто, цену подняли, тп считай нет» [id=175520|stayinit]; «за старую цену вполне нормально» [id=175521|libkit]; «падения» [id=175505..175512|—].
  - **4vps.su** — «норм» [id=169665..169666].
  - **serv.host** — «тот же бро» [id=171053].
  - **wecere.com** — «2,5-3кк+ машиноместо на паркинге в мск» [id=177861..177862, 174499..174510|xexe].
  - **cloudcore.ru** — только РФ, лимитный трафик, чисто ради сабпейджа [id=177773..177775|—].
  - **Deevo** — «на нём же дешевые сервера по 448₽ (1/2/20, 10 Гбит)» [id=172106..172108|—]; «Нидерланды/Германия» [id=171346..171347].
  - **VDS-инка** — «физическая локация в Нидерландах, 10 Гбит» [id=171346..171347].
  - **VeSpree** — «4 месяца всё норм» [id=175545..175555].
  - **waicore** — «Германия стоит стабильно, и скорости приемлемые» [id=175693..175700]; «2/4 — 220 юзеров» [id=175451..175467|Whiteness]; «ни снэпшотов, ни бекапов» [id=179134..179139|V M]; «скорость канала: ребут нужен» [id=179565..179573|—].
  - **Adman** — «1/2 может 110 юзеров» [id=170470..170492].
  - **VPSina** — «до 100к юзеров» [id=178803..178804].
  - **Ahelio Host** — «да можно» (Europe/SF) [id=165582..165593].
  - **crazy** — «у них сервера хуёвые, сразу поддержу 4 сервера» [id=175519..175521].
  - **дедик ( dedi)** — «реально тариф» [id=172106..172108|—].
  - **litehost** — «мало, но у меня все сервера там, 1цент» [id=175505..175521].
- **Beget** — «для бекапов: S3, гиг 7₽; aws + cron для копирования бекапов» [id=179241..179246|—].
- **CDN-виртуалки** — «CDN-video, VK, Yandex, RKN» [id=169033..169096|—].
- **ВК / vk_cloud** — бонусы (студенты) [id=174188..174204|—]; «бесплатные айпишники vk cloud» — «Секрет..» [id=174463..174464|—].
- **Google Cloud** — «500 $ + бесплатный» [id=174501..174510|—]; «на 50-90д» [id=174497..174500].
- **DigitalOcean GitHub Student Pack** — «200 $» (и после проверки карты 11 $) [id=174188..174204|—].
- **Hetzner — реселлеры** (не Hetzner напрямую) [id=178288..178289|—].
- **Zix** — «Локация редкая, только у 2-х провайдеров» [id=178888..178889].
- **AEZA** — «два года сервер там живет» [id=179333..179338].

## Безопасность / законы / планы (16–18.01)
- **«281 ФЗ»** — регламент рекламы в России, но не всегда [id=175030].
- **ВК ads** — рекламные посты; 12/1 = «12 часов, 1 час пауз» [id=173921..173924].
- **Telegram группы** — реклама ~3000₽ за 12/1 [id=173916..173924].
- **Критично: «Реклама ВПН в инсте»** — «сам факт рекламы в инсте уже нарушает закон» (1 сентября 2025) [id=175721..175762|—]; штрафы: физлица 50-80 тыс. руб., должностные 80-150 тыс., юрлица 200-500 тыс. руб.; повышение до 1 млн руб. [id=175754..175763].
- **«Как купить IP VK/Yandex»** — «секрет» (выкуп/блокировка) [id=174463..174464, 174959..174962].
- **VPN-Blacklist** (свой скрипт) — github BEDOLAGA-DEV/VPN-BLACKLIST (blacklist.txt) [id=179523|Сергей].
- **NaloGO**: env-конфиг целиком в чанке [id=179492]; «можно не настраивать, чеки вручную» [id=179493..179500].
- **Auto-deduction: recurring payments** — «Сделать «списывать» авто» — «Не делают, все Платега юзают» [id=179585..179605].
- **Remna/Cabinet обновления: ежечасная/раз-в-3-часа БД-бекапы** (не из кабинета) [id=177848..177864|—].
- **SMTP-свой сервер**: SPF, TLS, 25 порт, кнопка отписки [id=179879..179011].
- **Waicore (бекапы)** — «снэпшотов нет» [id=179134..179139|V M].
- **Kassa AI (модуль)** — «запилил модуль для Касса Аи» (не в main) [id=177010..177055|—].
- **«Haxe/AI: Whois» / «ipregion»** — ИП/регион [id=177955..178022].
- **«Мой налог» / NaloGO env** — [id=179492..179497].
- **Remna API-ключ** — «дей вызывается /api/system/stats» — «Не верный ключ, пересоздать» [id=177013..177017|кирилл].
- **Bedolaga/v3: «Дампы» для кабинета, независимый (не Remna)** — «дампы» в кабинете — отдельные, «база данных» бота/Remna — «двойные» [id=177848..177854].

## Прочее (16–18.01)
- **Google Cloud free $200** [id=174500..174503|—]; **DigitalOcean student pack 200$** [id=174188..174204|—].
- **Xray + Hysteria2** [id=179252..179255|—].
- **vless Golang / JARM** — «VLESS определяется по Golang-шифрованию (JARM)» [id=179230..179239|—].
- **Amnezia** — «блочат»; «Мой to-ту» [id=179234..179235].
- **Hysteria2 в Remna** — «HY2 ждём» [id=179253..179259|—].
- **Bedolaga auto install (wrx861)** — «работает?» [id=171662].
- **Скрипты автоустановки**: «баш <(curl -sL ...) @ install» [id=179875..179876].
- **Remnawave scripts (DigneZzZ)** — обновление/бекапы/установка [id=179447..179478].
- **Bedolaga cabinet (v1.0.0/v1.1.0)** — бекап/восстановление/`git pull`, `up -d --build` [id=177843..177863].
- **Аппка (не знает размер) / «Хуёвые показания»** [id=179214..179217|—].
- **VLESS Golang / JARM detection** [id=179230..179239|—].
- **Hysteria2 в Xray** (outbound; «HY2 ждём») [id=179252..179259|—].

## Флуд/мемы
- (флуд) Дискуссии про «какой клиент выбрать», «юмор про пиво/работу», «донаты BedolagamNaPivoBot», «Батя/снеговик» (обливают розжигом), «Яшка/ВК/каналы», «драки в чате», «рассылка в чатах по vpn 3000 ₽/мес», «еду на озеро» и т.п.
