# Заметки из chunk_033 (id 196682..201322, 26.01–31.01.2026)

## Релизы Bedolaga: бот v3.2.0 + кабинет v1.4.0 (27.01)
- **[id=197164|Egor|27.01]** #v3_2_0 Bedolaga Bot Update:
  - Email регистрация юзеров в веб-кабинете без привязки тг; фиксы Wata, Kassa ai, Cloudpayments; расширение API кабинета (Email шаблоны, настройка платёжных методов, yandex.metrika, google ads счётчики); багфиксы расчётов/продлений; **старый Miniapp удалён!**
  - Для email-регистрации нужен кабинет v1.4.0 + новая переменная `.env` бота:
  ```env
  # URL кабинета для ссылок в email (например: https://cabinet.example.com)
  CABINET_URL=
  ```
- **[id=197165]** #v1_4_0 Cabinet: полноценная email-рега, редактируемые email-шаблоны, отдельный раздел «Платёжные методы» (последовательность, условия вывода), Tribute вывод, пункт «Аналитика» (Я.Метрика), усиление безопасности, правки почтового сервера. Кабинет бесплатный ([id=197245]).
- В кабинете по дефолту все платежки ОФНУТЫ, активируются в админке кабинета → «Платёжные методы» [id=199649, 198107]. После обновлений у многих «пропадает» платежка — причина: не активирована в кабинете / старая статика [id=197819].
- **[id=200535|30.01]** На бою: смена почты, обновлённый websocket (уведы при пополнении/покупке/продлении by @c0mrade_ton), запоминание корзины, автопокупка после пополнения из кабинета, доработка раздела «Платёжные методы».
- **[id=200538|c0mrade]** ГЛАВНОЕ УСЛОВИЕ по сокетам: должны быть включены ТАРИФЫ (SALES_MODE=tariffs).

## Обновление/пересборка — стандартные команды
- **[id=199663]** Универсальная команда обновления бота:
```bash
cd /opt/remnawave-bedolaga-telegram-bot && git pull origin main && docker compose down && docker compose up -d --build && docker compose logs -f
# кабинет (сборка через npm):
cd /opt/bedolaga-cabinet && git pull origin main && npm run build && cd /opt/caddy && docker compose down && docker compose up -d --build && docker compose logs -f
```
- Пулл-релизный чеклист: `docker compose pull && docker compose down && docker compose up -d` или `docker compose down && git pull origin main && docker compose up -d --build && docker compose logs -f` [id=198036..198038].
- **Фикс «чёрный экран» кабинета**: пересборка с `--no-cache` (два дефиса!) бота и кабинета, рестарт реверс-прокси, чистка кеша браузера/Telegram [id=198960, 199560, 199963]. `docker compose build --no-cache` — обязательно два дефиса.
- **[id=199932|𝐢𝐠𝐨𝐫 𝐥𝐢𝐨𝐧]** Проблему чёрного экрана решил: `cabinet-dist/html:/srv/cabinet` (монтаж дистрибутива статики).
- **[id=199620|Egor]** В docker-compose кабинета заменить `image: cabinet_frontend` на `build: .` — иначе «pull access denied for cabinet_frontend» [id=200967].
- **[id=200990|Egor]** Альтернатива: собирать статику без докера:
```bash
# В папке с кабинетом:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
npm install
npm run build
```
- Caddy-конфиг кабинета (дословно):
```caddy
https://cabinet.example.com {
    encode gzip zstd
    handle /api/* {
        uri strip_prefix /api
        reverse_proxy remnawave_bot:8080 {
        }
    }
    handle {
        root * /srv/cabinet
        try_files {path} /index.html
        file_server
        @static path *.js *.css *.woff *.woff2 *.ttf *.ico *.png *.jpg *.jpeg *.svg *.webp *.gif
        header @static Cache-Control "public, max-age=31536000, immutable"
        @html path *.html /
        header @html Cache-Control "no-cache, must-revalidate"
    }
}
# в docker caddy монтируем: - /opt/bedolaga-cabinet/dist:/srv/cabinet:ro
```
- «Статика старая» — главный источник 80% багов после апдейтов; «три точки → перезагрузить страницу» в ТГ.

## Приоритет настроек: .env > бот > БД
- **[id=196777]** Поля не меняются, потому что приоритетные данные в `.env`; закомментить их и менять через бота.
- **[id=198858|vsevolodezz]** Настройки из бота применяются сразу, если их нет в .env; если в .env — удалить из env либо править env и рестарт.
- **[id=199871..199897]** Пример кривого env: `SALES_MODE=simple` не существует (только classic/tariffs); фиксированные пакеты трафика — только в classic; совет автора: **снести настройки цен из env и настраивать всё в боте**.
- **[id=200443|Джа]** Ловушка с устройствами: `DEFAULT_DEVICE_LIMIT=3` + `MAX_DEVICES_LIMIT=5` → кабинет считает 5-3=2 как «доп устройства» к подписке. Вернул `DEFAULT_DEVICE_LIMIT=5` — цены вернулись.
- **[id=200907]** `PLATEGA_MIN_AMOUNT_KOPEKS` сохранена в БД, но не применена (задаётся через env): удалить из env — меняется через бота без рестарта. **[id=200912|Egor]**: любые изменения в env → рестарт; через бота без рестарта меняется 98% настроек.
- **[id=200433|art vs]** Периоды, не используемые (значение 0) — раскомментировать/выставить через настройки бота: закомментированные тянут дефолт из БД.
- Env для кабинета (дословно):
```env
# ===== ЛИЧНЫЙ КАБИНЕТ (CABINET) =====
CABINET_ENABLED=false
CABINET_URL=
# Секретный ключ для JWT токенов (если не указан, используется BOT_TOKEN)
CABINET_JWT_SECRET=0
CABINET_ACCESS_TOKEN_EXPIRE_MINUTES=15
CABINET_REFRESH_TOKEN_EXPIRE_DAYS=7
CABINET_ALLOWED_ORIGINS=
CABINET_EMAIL_VERIFICATION_ENABLED=false
CABINET_EMAIL_AUTH_ENABLED=true
```

## Миграция на другой сервер
- **[id=196712..196739|Данил Уваров|26.01]** Перенос бота: поставил бедолагу, перенёс .env, восстановил бэкап, webhooks → ошибка 401; заменил токен Remnawave — ошибки ушли, но бот не отвечает на /start. Причина: **не был сделан сертификат на новом сервере**; при смене DNS на новый IP сертификат старого сервера становится невалидным.
- **[id=197413|/dev/null]** Без проблем переехал с марзбана; **[id=197706|R0xTaDDy]** синк с ремной простой, балансы придётся выдать скриптом. **[id=197349]** Бедолага работает только с Remnawave.
- Резервный домен/переезд: домен меняется в env панели и бота + реверс-прокси, всё [id=201227].

## Timezone: вечная -3 часа
- **[id=197817..197848]** Бот сравнивает end_date и никогда не укорачивает подписку; RemnaWave хранит в UTC, бот в UTC+3 → ровно 3 часа разницы. В docker-compose:
```yaml
services:
    remnawave:
      environment:
        - TZ=Europe/Moscow
      volumes:
        - /etc/timezone:/etc/timezone:ro
        - /etc/localtime:/etc/localtime:ro
```
- **[id=199139..199155|Egor]** Бот живёт на `datetime.utcnow`; совет: удалить из docker-компоcа бота `/etc/timezone` и `/etc/localtime`, поставить зону свою, `timedatectl set-timezone Europe/Moscow`, пустить синк — на 3 ботах время выровнялось. Синк сквадов по UUID [id=199174], название сквада отдельно редактируемое вручную.
- **[id=199168]** В админке бота время отображается в UTC всегда.

## Ошибки и фиксы
- **[id=198818|Миша ту-ту]** Email-регистрация: точка в почте → 400 от панели `Username can only contain letters, numbers, underscores and dashes` — убирать запрещённые символы перед регистрацией в панели.
- **[id=198244|kifchan]** `LOG_ROTATION_TOPIC_ID` пустой → бот не поднимается (int parsing), хотя в комментах указан fallback на BACKUP_SEND_TOPIC_ID.
- **[id=197802|SUPPORT]** `Unclosed client session / Connector is closed` в aiohttp после бэкапа — баг, присылали автору.
- **[id=200510|nikita]** Миграция: `integer out of range` в `button_click_logs.user_id TYPE INTEGER` (большие user_id).
- **[id=198619|данч]** Бедолага экспортирует юзеров в ремну на -3 часа (datetime.utcnow).
- **[id=198851]** Локали бота лежат в `remnawave-bedolaga-telegram-bot/data/backups`... правильный путь: `https://github.com/BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot/tree/main/app/localization/locales` [id=198782]; текст тестовой подписки в `./app/localization/locales/ru.json` + `./app/services/monitoring_service.py` [id=200585].
- **[id=200823]** `<br>` в текстах → краш бота `Unsupported start tag "br"`; ТГ не работает с `<br>` — использовать `\n`.
- **[id=201086]** Кнопка guide: `BUTTON_URL_INVALID` на guide_android — задать `HAPP_CRYPTOLINK_REDIRECT_TEMPLATE` (редирект-страницу). Ссылки `happ://` ТГ не поддерживает, нужна редирект-страница:
  ```env
  # Пример: https://sub.domain.sub/redirect-page/?redirect_to=
  HAPP_CRYPTOLINK_REDIRECT_TEMPLATE=
  ```
- **[id=198067]** Мониторинг трафика готовится: будет «по сраке лупить» абъюзеров, мультиаккеров, любителей сидеть под БС нодами.
- **[id=198824]** Wata: `WATA API error 429: Use webhook – polling is blocked` при проверке сразу после создания платежа.
- **[id=200660|Gy9vin]** Баг: при обязательной подписке на группу система блокировки/бан не работает (реактивация после подписки на канал обходит бан).
- **[id=200383]** После переключения tariffs→classic: `greenlet_spawn has not been called` в middlewares (лечится восстановлением с бэкапа).
- **[id=200940]** Промокод «использований 0» = максимум через админку ставится тупо 0 использований.

## Домены и Telegram Login Widget
- **[id=200642..200665]** ТГ НЕ поддерживает зоны **.xyz, .top, .pro** для Telegram Login Widget («Telegram does not support .xyz domains for authentication»). Работают: **.com, .ru, .net, .biz, .online, .ink, .ovh** (овх дешёвая альтернатива). Хуки/webhooks/ноды/панель можно оставить на старых дешёвых зонах, кабинет — на доверенной.
- Кнопка подключения mode=link открывает просто ссылку страницы подписки [id=197278].

## Мультипротокольная нода (VLESS Reality + xhttp) — конфиг
- **[id=198540..198554|Кирилл/R0xTaDDy]** Несколько инбаундов в одном конфиге, порты разные; api_inbound (dokodemo-door) удалить — не нужен. Полный конфиг Xray с VLESS_REALITY_MAIN (8443) + xhttp (8442), shortId ≤16 симв., routing блокирует торренты (порты 6881-6889, 6969, 27015, домены openbittorrent.com, rarbg.to, piratebay.org, 1337x.to, yts.mx, eztv.io, kickasstorrents.to, nyaa.si), geosite:private/geoip:private → BLOCK:
```json
{
  "log": {"loglevel": "info"},
  "inbounds": [
    {"tag": "VLESS_REALITY_MAIN", "port": 8443, "listen": "::", "protocol": "vless",
     "settings": {"clients": [], "decryption": "none"},
     "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
     "streamSettings": {"network": "tcp", "security": "reality",
       "realitySettings": {"show": false, "xver": 0, "target": "domain:443",
         "shortIds": ["1A2B3C4D5E6F7890"], "serverNames": ["domain.com"]}}},
    {"tag": "xhttp", "port": 8442, "listen": "::", "protocol": "vless",
     "streamSettings": {"network": "xhttp", "security": "reality",
       "xhttpSettings": {"host": "", "mode": "auto", "path": ""},
       "realitySettings": {"xver": 0, "target": "hotmc.ru:443", "shortIds": ["1A2B3C445D5E6F7890"], "serverNames": ["hotmc.ru"]}}}
  ],
  "outbounds": [{"tag": "DIRECT", "protocol": "freedom"}, {"tag": "BLOCK", "protocol": "blackhole"}],
  "routing": {"rules": [{"type":"field","inboundTag":["VLESS_REALITY_MAIN","xhttp"],"outboundTag":"DIRECT"}]}
}
```
- Генератор инбаундов: https://azavaxhuman.github.io/DDS-Xray-Inbound-Generator/ ; примеры: https://github.com/XTLS/Xray-examples ; дока: https://xtls.github.io/ru/config/dns.html
- Selfsteal на ноду руками: гайдов нет, поставить скрипт dignezzz/egames и посмотреть конфиг [id=198609]. Скрипт нод автоустановки: https://github.com/nerioff1337/remnawave-node-auto [id=200267], https://github.com/Case211/remnanode-install [id=200376].
- Логи ноды: в конфиг `"log": {"error": "/var/log/remnanode/error.log", "access": "...", "loglevel": "warning"}` — нужны существующие файлы/тома [id=197855].
- Ограничение скорости 20 мбит на юзера — на нодах, не в панели; через tc:
```bash
tc qdisc del dev eth0 root 2>/dev/null
tc qdisc add dev eth0 root handle 1: htb default 10
tc class add dev eth0 parent 1: classid 1:10 htb rate 20mbit ceil 20mbit
tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip dport 443 0xffff flowid 1:10
tc -s qdisc show dev eth0
```
[id=200780]

## Набор тестов VPS (закреп от Egor, дословно) [id=199900]
```bash
IP region
bash <(wget -qO- https://ipregion.vrnt.xyz)
Censorcheck для проверки геоблока
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode geoblock
Censorcheck для серверов РФ
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode dpi
Тест до российских iPerf3 серверов
bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh)
YABS
curl -sL yabs.sh | bash -s -- -4
Проверка IP сервера на блокировки зарубежными сервисами
bash <(curl -Ls IP.Check.Place) -l en
Параметры сервера и проверка скорости к зарубежным провайдерам
wget -qO- bench.sh | bash
IPQuality
bash <(curl -Ls https://Check.Place) -EI
Тест на процессор (какой % cpu выделили)
sysbench cpu run --threads=1
```

## Хостинги (опыт, конец января 2026)
- **[id=197319|V M]** #Poland #AdminVPS: 1 ядро/2ГБ/15ГБ/до1Гбит(лимит 5ТБ) — 499₽/мес; Польша работает лучше НЛ/Германии у этого хостера, 3 снэпшота.
- **[id=199002|wsq22]** #USA #UNESTY: 4 ядра/1ГБ/25ГБ/до 10Гбит — 500₽ (потом тот же 249₽).
- **[id=200122..200227]** #play2go DE: 6 vCPU Ryzen 9 5950X/16GB/200GB/1Гбит — но «2 из 2 серваков режет скорость, пинги высокие» (Anton ES SL); NL норм у одного, у другого нет. DNS-амплификация открыта на play2go и Senko [id=199678|Prokurátura].
- **[id=200083]** serv.host Москва Epyc-7502-1: 1vCPU/1GB/10GB/250Мбит (burst 1Гбит) — 150₽/мес.
- **[id=200628]** #elenahost Томск: 2vCPU/2GB/15GB/200Мбит — 144₽/мес; SMTP порты заблокированы; 40ТБ/мес потом режут.
- **[id=201048..201050|Павел]** Hip-Hosting Финляндия 3.2$/мес 2vCPU/2GB/20GB/100Мбит+ — стабильно; РУ Москва 2.4$/мес 1vCPU/1GB/10GB/100+Мбит — YouTube рабочий; Beget РУ 7₽/день 1vCPU/1GB/10GB/250Мбит — ютуб рабочий.
- **[id=200694]** #1cent Germany: 1 ядро/1ГБ/10ГБ, 1Гбит — 150₽, неровные падения на пару часов; ещё Эстония, Финляндия.
- **[id=200763]** Vultr Индия (Мумбаи): 12$/мес 1vCPU/2GB/50GB/10Гбит/5ТБ — 100% гео-совпадение, почасовая оплата, ровный аптайм.
- **[id=198839|V M]** adminVPS: 77-я подсеть без рекламы, 93-я — с рекламой (рандом).
- **[id=198842|xrmqd]** u1host НЛ: геобазы обновились — реклама пропала, физически сервер в Германии.
- **[id=198532|tgshtt]** weasel.cloud Польша — IP чистый рандом (у него IP «только гугл видит как РУ»).
- **[id=200183|นิโคลัส]** u1host: 209₽/мес, фины/немцы/голландцы.
- **[id=196880|xexe]** Аеза: «все жалуются, но я 2 года пользуюсь — все гуд», но для нод дорогая (500₽+), для панели на старт хватит; **не ставь ноду на сервер с панелью** [id=196882]; панель/бот/кабинет можно на одном сервере.
- **[id=201097]** adminvps Нидерланды: купил, панель упала на 1.5ч, реинсталл не помогает.
- **[id=200411|Anton Khakin]** hshp.host — прошлый опыт: не дали сервер после покупки, возврат только после жалобы на Lolz.
- **[id=200294]** таймвеб: скорость режут со временем при большом потоке; за айпишник ещё 200₽.
- **[id=201058|Popugtop]** the.hosting: франция/швейцария — ютуб иногда как РУ определяется рандомно; финка/турция проседают, турция падает на 10 минут раз в несколько дней.
- Play2go NL: «переехал с p2g — 2 из 2 серверов режут скорость, пинги высокие» → купил у другого хоста с тем же конфигом — всё летает [id=197995].

## Белые списки / БС-серверы / обходы
- **[id=199845|R0xTaDDy]** Выбить БС-айпи на ВК — «очень проблематично»; на таймвебе половина операторов не работает; Яндекс — «точно всё просто», скриптом 5-10 минут сейчас (раньше 3 мин); 158.160 — «шляпа»; 84-я подсеть — не работают все операторы кроме Ростелекома и t-мобайл, 51-я — работает на всех [id=199809]. Яндекс ~1.65–2₽/ГБ. Есть места с бесплатным трафиком (не ВК, не таймвеб) — «уже нет».
- **[id=199141]** Пролив 70ТБ трафика на БС — «до первых проблем».
- **[id=200704]** Абьюзер 186ГБ за 4 дня с белых списков → бан.
- **[id=200069]** Роутинг ютуба на РУ сервер/сервер с IP в геобазах как РУ → ютуб без рекламы (секция routing в ремне; отдельный РУ VPS под ютуб) [id=199771]. Twitch: маршрут geosite:twitch напрямую — лаги (1080 макс); через прокси — 1440 летает [id=198139..198166].
- **[id=198872|V M]** sprintbox СПб: нет ТСПУ на ютуб и инсту, скорость до 200 Мбит, безлимит.
- **[id=198301]** «109.120.x / 109.120.180/188» — ценятся для БС.
- Роутинг серверный настраивается в панели: подписка → настройки, внизу строка про роутинг [id=198430].
- WG/Amnezia блокируют из РФ во внешку [id=199921]; NetBird на WG — «легко заблокировать», между нодами не блокируют [id=199912].

## Платежи
- **[id=198210..198226]** Платега — рекомендация №1; юкасса — когда нужны чеки. Platega из кабинета: методы указывать номерами (2, 11; 11=карты, 13/5%=крипта) в `PLATEGA_ACTIVE_METHODS`; PLATEGA_SECRET = my.platega.io/dashboard/settings.
- **[id=197742|Kabeba]** Прикол с портом: в nginx проксирование `127.0.0.1:808` (опечатка) — юкасса не завелась, случайно заметил 8080.
- **[id=199259]** `YOOKASSA_RETURN_URL` — куда перекидывает после оплаты («вернуться в магазин»); не указан — сайт юмани.
- **[id=197634|V M]** Tribute поднял комиссию с 3% до 10%; отзыв [id=200212|R0xTaDDy]: «хуйня, 10% комса, только карты, выёбываются при выводе»; мин вывод ~200$ (другой говорит от 3к₽).
- Криптобот: API + webhook, закомментить 8081, testnet пробовать; **[id=200409]** «криптобот как mega scam» — саппорт 2 модератора; комиссии большие (3%).
- **[id=200435]** Налоговая: сказал в лоб «продаю VPN» под «Интернет-сервис» — ответ: если прилетит, не от нас; чеки автоматически идут из юкассы в nalogo с подписью «Интернет-сервис» [id=199520]. nalogo: lkfl.nalog.ru через ЕСИА [id=196757].
- **[id=200950]** Platega 31.01 outage — платежи висят 10+ мин, поддержка молчит, у кого 30+ пополнений со скидкой не подтверждались; плatega «не принимает ВПН без лицензии РКН» [id=200951|Zavulon].
- **[id=199467]** Юкасса пропускает VPN-магазин (указывают реального бота) [id=200194..200200]; самозанятым cloudpayments не работает, юкасса — да.
- **[id=199891]** Вывод с платеги: Trust Wallet (некастодиальный), тг-кошелёк любят банить; tronlink gasfree — комиссия 1 USDT.
- **[id=201270]** Альфабанк API — сказали что лицензий не надо, только прикрутить API.

## Юридическое
- **[id=198299|Silistial]** РОССИЯНЕ СТАЛИ ПОЛУЧАТЬ ШТРАФЫ ЗА ИНФУ О VPN: Вологодское УФАС оштрафовало за ссылку на VPN-бота в WhatsApp (открытую) — «ненадлежащая реклама» от 80 000₽. Любая ссылка в открытом профиле/чате/канале может считаться рекламой. [id=199391|Alexey Golovin]: основной акцент закона — «свободное распространение рекламы»; продажа в ЛС за крипту/нал не нарушает. Формулировки: «ускоритель интернета», «стабильное подключение».
- **[id=200740]** Убийство сотрудника РКН Алексея Беляева (отвечал за блокировки) 16-летним школьником 19.01.2026 — инсайдерские каналы (ВЧК-ОГПУ), официально засекречено; споры о достоверности.
- **[id=201251]** Лицензия РКН на «телематические услуги» (не ФСТЭК) — юкасса требует; выдают список условий.
- **[id=199214]** «По запросу свыше ТГ отдаст все данные» — Дуров заявил, что IP/телефоны нарушителей передаются по юридическим запросам.
- Бот-пользователь без бэкапа залочен хостером — «дурачки думают, что бэкап никто не делает» [id=198497|Егор].

## Сервисы/инструменты
- **[id=197090..197022]** TrafficGuard (dotX12/traffic-guard) — блокировка IP сканеров на уровне iptables до сервисов; автоустановка: `curl -fsSL https://raw.githubusercontent.com/DonMatteoVPN/TrafficGuard-auto/refs/heads/main/install-trafficguard.sh | sudo bash` → команда `rknpidor` (пульт управления TrafficGuard). Решала-скрипт: https://github.com/DonMatteoVPN/reshala-script (тесты, шейпер 5 пункт показывает IP подключений и скорость/трафик).
- **[id=199450]** Блокировка торрентов: https://github.com/kutovoys/xray-torrent-blocker (DMCA-жалобы хостеру — «запретить торренты»).
- **[id=199004]** Автоустановка бедолаги: https://github.com/wrx861/bedolaga_auto_install (команду bot для панели управления).
- **[id=196803]** Список звёздочек: remnawave/panel, BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot, BEDOLAGA-DEV/bedolaga-cabinet, kutovoys/xray-checker, eGamesAPI/remnawave-reverse-proxy, Jolymmiels/remnawave-telegram-shop, machka-pasla/remnawave-tg-shop, DigneZzZ/remnawave-scripts, distillium/remnawave-backup-restore, maposia/remnawave-telegram-sub-mini-app, legiz-ru/my-remnawave, dotX12/traffic-guard.
- **[id=200763]** Чёрный список шареров/абьюзеров: https://github.com/BEDOLAGA-DEV/VPN-BLACKLIST/blob/main/blacklist.txt (автор «добавил всех», шеринг 8469354644/5267593516/7495948172/6602578716).
- **[id=201111|Илья]** remnawave-admin (Case211) v1.6: Динамические настройки (env>db>default, read-only env), Anti-Abuse система (одновременные IP, 60+ РУ-агломераций, Haversine «невозможные путешествия» город 50/страна 200/мир 800 км/ч, ASN-классификация, 30-дневный профиль, скоринг), Node Agent + Collector API, уведы NOTIFICATIONS_TOPIC_VIOLATIONS; пока режим мониторинга; после обновления «Синхронизация ASN» обязательна. https://github.com/Case211/remnawave-admin/releases/tag/1.6
- Мониторинг: начальное — beszel или uptime kuma; продвинутое — grafana/zabbix; wiki.egam.es (про графану) [id=199404..199410].
- Хэпп: скрыть конфиги серверов бесплатно — никак, платно — id провайдера на сайте хаппа [id=199218].
- Секреты безопасности: ufw на порт 2222 ноды — allow only from mainNode [id=197130|/dev/null]; изменение ssh-порта на рандомный — «сканеры засирают проц» [id=201291|Zavulon]; fail2ban на свежем сервере банит 3 IP за 8 минут (сканеры) [id=200166].
- GitActions-сборка кабинета с вшитыми VITE-переменными — редирект заработал [id=197149|art vs].

## События
- **31.01.2026** — Platega outage (платежи не подтверждаются ~1 час+).
- **[id=200407]** Уведомления-«наказания» от РКН по Telegram-каналам — «воздушные темы», «пугалки» (споры о реальности штрафов за рекламу VPN).
- **[id=200660]** Закон о запрете рекламы VPN — сформулирован под «свободный доступ к рекламе» (открытые каналы/ссылки).
- **[id=201237]** Сервис-«спамер» a9fm.site/twinkvibe.gay (ЭтоНеЯ) — ворует триальные ключи, зеркала на ютуб/гемини; на хостинге хранятся ключи других сервисов.
