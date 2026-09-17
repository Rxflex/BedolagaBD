# Заметки из chunk_021 (id 115081..123677, 18.12.2025 .. 21.12.2025)

## Bedolaga: релиз v2.9.2 (совместимость с Remnawave API 2.4.0+, конструктор меню, конкурсы, НалогоГО)
- **[id=121296|Egor|21.12.2025]** релиз v2.9.2: совместимость с Remnawave API 2.4.0+ by fringg — новый путь статистики /api/bandwidth-stats/nodes/{uuid}/users/legacy, требует Remnawave v2.4.0+; Конструктор меню (@pedzeo) — асинхронная сборка клавиатуры, плейсхолдеры username/дни/трафик/рефералы, история изменений с откатом, Web API роутер /menu-layout; аналитика кликов по кнопкам; система конкурсов (@Gy9vin) — реферальные конкурсы, лидерборд, призы продлением; интеграция НалогоГО — авто-чеки при пополнении через YooKassa, автоаутентификация токена API, graceful fallback; расширенные рассылки: expiring/expired/canceled, autopay_failed, low_balance (баланс < 100 руб), inactive_30d/60d/90d. Обновление: cd /root/remnawave-bedolaga-telegram-bot && git pull origin main && make reload (или make reload-follow с логами).
  - новые настройки: MENU_LAYOUT_ENABLED=false, CONTESTS_ENABLED=false, CONTESTS_BUTTON_VISIBLE=false, ENABLE_AUTOPAY=false, NALOGO_ENABLED=false, NALOGO_INN=, NALOGO_PASSWORD=, NALOGO_DEVICE_ID=, NALOGO_STORAGE_PATH=./nalogo_tokens.json, TIMEZONE=Europe/Moscow. Требуются миграции БД для конструктора меню и конкурсов.
- **[id=121318|Egor|21.12.2025]** клавиатуру в новой версии менять пока только по API; **[id=121319|—|21.12.2025]** скоро откроют правку менюшки в админке без тарифа.
- **[id=119177|R0xTaDDy|20.12.2025]** фича-реквест в 3.0: рулетка в миниаппке, создающая промики по API с настраиваемыми шансами.
- **[id=115149|—|18.12.2025]** разработчик ебашит Bedolaga 3.0.0. **[id=115340|Евген|18.12.2025]** реквест: поддержка WireGuard (AmneziaWG), выбор протокола Vless/Trojan/WireGuard при подключении.

## Платёжка Platega: env и нюансы
- **[id=115154|Й Цукен|18.12.2025]** env:
```
# PLATEGA
PLATEGA_ENABLED=true
PLATEGA_MERCHANT_ID=немногосимволов
PLATEGA_SECRET=многасимволов
#PLATEGA_BASE_URL=https://app.platega.io
PLATEGA_RETURN_URL=https://t.me/мойбот
PLATEGA_FAILED_URL=https://t.me/мойбот
PLATEGA_CURRENCY=RUB
# Список ID активных методов из кабинета Platega (через запятую)
PLATEGA_ACTIVE_METHODS=2
PLATEGA_MIN_AMOUNT_KOPEKS=100
#PLATEGA_MAX_AMOUNT_KOPEKS=100000000
PLATEGA_WEBHOOK_PATH=/platega-webhook
PLATEGA_WEBHOOK_HOST=0.0.0.0
PLATEGA_WEBHOOK_PORT=8086
```
- **[id=115236|—|18.12.2025]** PLATEGA_RETURN_URL/FAILED_URL — домен (не ссылка бота): https://your-domain.com/payments/success и /payments/failed.
- **[id=115239|—|18.12.2025]** после смены env нужна ПОЛНАЯ пересборка: make reload/docker compose, простой рестарт скриптом не подхватывает.
- **[id=121146|Агент поддержки|21.12.2025]** Platega: пока кнопку «проверить платеж» не нажмёшь — не зачисляется; **[id=121162|—|21.12.2025]** после добавления Platega бота надо ребутнуть, иначе webhook даёт 404.
- **[id=121211|—|21.12.2025]** Platega без сабдомена в хуках работала раньше мистическим образом; hooks надо дописать.
- **[id=117920|Й Цукен|19.12.2025]** надпись кнопки Platega (СБП+карта) не меняется в боте — только правкой исходника.
- **[id=122920|17|21.12.2025]** у Platega с оборотом от 5к можно у merchant-менеджера снизить комиссию без особых проблем.
- **[id=117980|—|19.12.2025]** 50 выводов с Platega — ни одного отлёта карт; **[id=117983|Никита|19.12.2025]** если карту и блокнут по 115-ФЗ — звонок в банк разблокирует.

## YooKassa: чеки самозанятых закрываются, НалогоГО
- **[id=118343|_-_ LeX _-_|19.12.2025]** официальная рассылка ЮKassa: с 29 декабря 2025 сервис «Чеки для самозанятых» завершает работу; чеки регистрировать через приложение «Мой налог», приём платежей через ЮKassa без изменений.
- **[id=118345|Egor|19.12.2025]** интеграция с НалогоГО уже тестируется; **[id=118348|Egor]** и под ставку 22% тоже.
- **[id=119229|Egor|20.12.2025]** фикс под апишку готовлю; **[id=121296|Egor|21.12.2025]** в 2.9.2 авто-чеки через НалогоГО при пополнении YooKassa.
- **[id=119953|Евген|20.12.2025]** раньше при оплате в юкассе надо было вводить чек, сейчас не надо.
- **[id=119225|Ivan|20.12.2025]** самозанятому чек — на каждое оказание услуги отдельный (нельзя одним чеком на сумму/ежедневную выплату кассы); ходят слухи, что самозанятость прикроют (id=119670|Ivan).
- **[id=121996|SUPPORT|21.12.2025]** миграции БД (конструктор меню/конкурсы) — вопрос остался открытым в чанке; **[id=119229|Egor|20.12.2025]** патч апишки под 2.4.1 готовился.
- **[id=118005|Никита|19.12.2025]** Tribut — ~10% комса с понижением при большем обороте, у ЮKassa ~7-8% в сумме; ЮKassa белая, Platega — не белая (можно работать по-белому с чеками, id=118005/118000: в описании проекта для одобрения писал «интернет услуги»).
- **[id=119864|—|20.12.2025]** Wata в коде бота не найдена (на гите написано, что есть, по факту нет; id=122882..122884|🛡️/—); оплата Wata — только СБП (id=120380|Deleted Account вопрос без ответа).
- **[id=122749|Й Цукен|21.12.2025]** автоплатёж с карты есть в Tribut; в боте автосписание списывает только с баланса бота (id=122756).
- **[id=118424|Агент поддержки|19.12.2025]** Lava — «помойка», вывод 200к занял неделю (id=122436..122439|🛡️).

## Обновление Remnawave 2.4.x и совместимость
- **[id=119290|—|20.12.2025]** вышла новая ремна: страницу подписки теперь настраиваешь прямо с панели.
- **[id=119227|legiz|20.12.2025]** Orion пока не совместим с обновлением — фиксировать версию пейджа на 6-й.
- **[id=119236|—|20.12.2025]** после апишки обновляться можно, текущий бот воркает; **[id=121069|Egor|21.12.2025]** при 2.4.2 в некоторых местах бота отвалится инфа по нодам — вышел патч.
- **[id=119822|—|20.12.2025]** ласт панель = ласт нода, только так работает (ошибка создания ноды из-за версии).
- **[id=122642|anmbl|21.12.2025]** вопрос «Remnawave 2.4.0 совместима с remnanode 2.3.2?» — следуя вышеприведённому, нужен ласт remnanode.
- **[id=120124|Й Цукен|20.12.2025]** скрипт eGames и субы работают с новыми версиями, страницу подписки можно менять через браузер.
- **[id=119681|Васян|20.12.2025]** ( Remnawave Reverse Proxy v2.3.0 от eGames) : генерация сертификатов Gcore; реальные IP для subscription page — в nginx.conf proxy_set_header X-Real-IP $proxy_protocol_addr и X-Forwarded-For; server_names_hash_bucket_size 64 (фикс «could not build the server_names_hash»); @redirect return 444 вместо 404; REMNAWAVE_API_TOKEN=ваш_токен в docker-compose сервиса subscription-page (старая установка — создать токен в панели вручную); SUBSCRIPTION_UI_DISPLAY_RAW_KEYS=true — показывает сырые vless:// ссылки при отключённом HWID.

## Скрипты автоустановки
- **[id=118077|Й Цукен|19.12.2025]** автоустановка бота Bedolaga (eGames-скрипт): Docker, SSL, база, webhook, miniapp, подключение к панели; работает панель+бот на одном сервере или на разных; пока только с nginx.
- **[id=118048|Евген|19.12.2025]** «решала-скрипт» оценивает сколько юзеров потянет сервер: https://github.com/DonMatteoVPN/Reshala-Remnawave-Bedolaga
- **[id=118320|—|19.12.2025]** скрипт установки бота: https://github.com/wrx861/bedolaga_auto_install (панель-ссылка/лог-пас вводятся, но были проблемы с коннектом).

## YooKassa webhook: trusted proxy и проверка
- **[id=120591|Александр|20.12.2025]** решение для вебхуков ЮKassa: YOOKASSA_TRUSTED_PROXY_NETWORKS=subnet: 172.20.0.0/16 (подсеть из докера); бот сначала проверяет локальный IP, потом из заголовка; **[id=120633|Александр|20.12.2025]** без этого вебхуки работать не будут, нужно в README.
- **[id=118419|—|19.12.2025]** рабочий хук по полному пути в браузере отвечает: {"status":"ok","service":"yookassa_webhook","enabled":true}.
- **[id=120647|Александр|20.12.2025]** тест-команда вебхука:
```
curl -X POST http://localhost:8080/yookassa-webhook \
  -H "Content-Type: application/json" \
  -H "X-Forwarded-For: 77.75.153.78" \
  -d '{ "event": "payment.succeeded", "object": { "id": "test-payment-id" } }'
```
- **[id=121818|libkit|21.12.2025]** CryptoBot webhook 401 «Неверная подпись» → в криптобота надо загрузить .rem-сертификат от домена хуков (hook.yourdomain.com.rem) (id=121835..121839|—/романтика.com).
- **[id=122822|libkit|21.12.2025]** после оплаты heleket в консоли WARNING: Invalid HTTP request received — фикса в чанке нет.

## Бэкапы и восстановление
- **[id=118111|Haxonate|19.12.2025]** ручной бэкап бота — во вкладке «Бэкапы» бота; восстановление: нажать восстановить и очистить (id=118153).
- **[id=118118..118131|Whiteness/Й Цукен/—|19.12.2025]** восстановление ремны из rw-backup на новой установке не встаёт — решалось одной командой: снести redis (нет компонента — нет проблемы).
- **[id=119673|Евген|20.12.2025]** (важный мантр-пост) бэкапы 3-2-1, безопасность серверов, порт связи ноды с панелью открывать только для IP панели.

## Docker / nginx / miniapp / Caddy
- **[id=115232|—|18.12.2025]** ошибка бота Cannot connect to host remnawave:3000 [Name or service not known]; **[id=115532|Й Цукен|18.12.2025]** фикс:
```
docker network create remnawave_network
docker network connect remnawave_network remnawave
docker network connect remnawave_network remnawave_bot
```
- **[id=118481|Александр|19.12.2025]** набор скриптов теста сервера:
```
bash <(curl -Ls IP.Check.Place) -l en          # IP на блокировки зарубежных сервисов
wget -qO- bench.gig.ovh | bash                 # к российским провайдерам
wget -qO- bench.tlab.pw | bash
wget -qO- bench.sh | bash                      # к зарубежным
wget -qO- speed.tlab.pw | bash
bash <(curl -L -s https://bench.openode.xyz/checker_inst.sh)   # блок аудио в Instagram
curl -sL yabs.sh | bash -s -- -4               # YABS: диск, iperf3, GeekBench
bash <(wget -qO - https://github.com/vernette/ipregion/raw/master/ipregion.sh)
bash <(wget -qO- https://ipregion.xyz)
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode dpi  # DPI-блок для РФ-серверов
sysbench cpu run --threads=1                   # % выделенного CPU
```
- **[id=118298|Haxonate|19.12.2025]** проверка региона IP: bash <(wget -qO- https://github.com/Davoyan/ipregion/raw/main/ipregion.sh)
- **[id=119681|Васян|20.12.2025]** миниаппка Bedolaga за nginx (бот 127.0.0.1:8080, network_mode: host):
```
# Мини-апп (HTTPS)
server {
    listen 443 ssl http2;
    server_name mini.dom.ru;
    ssl_certificate /etc/nginx/ssl/bot_cert.pem;
    ssl_certificate_key /etc/nginx/ssl/bot_key.pem;
    root /miniapp;
    index index.html;
    location = /miniapp/app-config.json {
        add_header Access-Control-Allow-Origin "*";
        try_files $uri =404;
    }
    location / { try_files $uri /index.html =404; }
    location /miniapp/ {
        proxy_pass http://127.0.0.1:8080/miniapp/;  # важен слеш в конце!
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
  env бота: WEBHOOK_URL=https://hook.dom.ru, WEBHOOK_PATH=/webhook, BOT_RUN_MODE=webhook, WEB_API_ENABLED=true, WEB_API_HOST=0.0.0.0, WEB_API_PORT=8080, WEB_API_ALLOWED_ORIGINS=https://mini.dom.ru, WEB_API_DEFAULT_TOKEN=..., MINIAPP_STATIC_PATH=miniapp. В nginx-контейнер монтируется ./miniapp:/miniapp:ro; редактировать app-config надо на хосте и примонтировать в докер (id=120494|R0xTaDDy).
- **[id=120273|Денис|20.12.2025]** та же миниаппка на Caddy:
```
hook.my.store {
    encode gzip zstd
    @config path /app-config.json
    header @config Access-Control-Allow-Origin "*"
    reverse_proxy localhost:8080 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-Proto {scheme}
        transport http { read_buffer 0 }
    }
}
miniapp.my.store {
    encode gzip zstd
    root * /miniapp
    file_server
    @config path /app-config.json
    header @config Access-Control-Allow-Origin "*"
    reverse_proxy /miniapp/* 127.0.0.1:8080 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
    }
}
```
- **[id=119273|Дмитрий 👨‍🚒|20.12.2025]** после правок в боте пересобрать: docker compose down && docker compose up -d --build. **[id=119864|.|20.12.2025]** обновление ноды: docker-compose pull && docker-compose up -d (пуллить, не билдить; docker-compose без тире не работает с оф. страницы — id=119871|Zavulon). **[id=123378|Никита|21.12.2025]** логи: docker compose logs -f -t / docker logs remnawave-nginx -f -t.
- **[id=123309|Никита|21.12.2025]** при установке ремны скриптом eGames API к панели закрыт — открыть в конфиге nginx панели, доку: https://wiki.egam.es/configuration/external-api/ ; для бота в URL http://remnawave:3000 и api-ключ, созданный в панели (не трогать bootstrap-ключ, создать новый, id=123049/123057|Й Цукен).
- **[id=123671|Jimmy Нейтрон|21.12.2025]** панель/нода/подписка на поддоменах одного домена — хук и миниапп можно прикрутить туда же поддоменами; **[id=123676|Евген|21.12.2025]** прикручивай сколько душе угодно поддоменов.
- **[id=117114|SawGoD|19.12.2025]** хуки идут к боту, бот идёт к панели → в DNS для WEBHOOK_URL/WEB_API_ALLOWED_ORIGINS прописывать IP бота.
- **[id=121817|романтика.com|21.12.2025]** selfsteal-заглушка на Caddy (максим):
```
:9443 {
    tls internal {
        on_demand
    }
    respond 200
}
```
  target ставить 9443 — отдельная локальная заглушка под каждую ноду (она доступна только локально ноде), xray слушает 443, nginx/caddy 443 (id=121950|AIRVPN).

## Reality/selfsteal: xver, serverNames, таргеты
- **[id=120878|R0xTaDDy|21.12.2025]** в десте — fallback-адрес, в serverNames — домен(ы) ноды; **[id=120880/120885|R0xTaDDy]** xver должен быть 0.
- **[id=120801|—|20.12.2025]** в serverNames можно указать несколько selfsteal-доменов — поддомены да.
- **[id=120820|Данил|20.12.2025]** вторая нода не работала из-за того, что target селфстила указывал на первую ноду — каждой ноде свой сабдомен селфстила.
- **[id=122837|AIRVPN|21.12.2025]** профиль с 4 тегами (SNI) на 443 одной ноды работает «пока», но правильно: 1 инбаунд на 443 + dest с локальным портом (например 8080) и в тегах локальный порт.
- **[id=119788|—|20.12.2025]** xHTTP-инбаунд (TLS, свои сертификаты, только для владельцев своего домена):
```
{
  "tag": "xHTTP", "port": 443, "listen": "0.0.0.0", "protocol": "vless",
  "settings": { "clients": [], "decryption": "none" },
  "sniffing": { "enabled": true, "routeOnly": false,
    "destOverride": ["http","tls","quic"], "metadataOnly": false },
  "streamSettings": {
    "network": "xhttp", "security": "tls",
    "tlsSettings": { "alpn": ["h2","http/1.1"], "maxVersion": "1.3", "minVersion": "1.2",
      "serverName": "селфсни", "fingerprint": "chrome",
      "certificates": [{ "usage": "encipherment",
        "keyFile": "/etc/letsencrypt/live/домен/privkey.pem",
        "certificateFile": "/etc/letsencrypt/live/домен/fullchain.pem" }],
      "allowInsecure": false, "rejectUnknownSni": false, "disableSystemRoot": false,
      "enableSessionResumption": false },
    "xhttpSettings": { "host": "селфсни", "mode": "auto", "path": "/", "headers": {},
      "noSSEHeader": false, "xPaddingBytes": "100-1000",
      "scMaxBufferedPosts": 30, "scMaxEachPostBytes": 1000000,
      "scStreamUpServerSecs": "20-80" }
  }
}
```
- **[id=118728|—|19.12.2025]** селфстил с xhttp TLS пока не одолели: сайты в 400 падают, но работают (свой SNI, страничку не поднять).

## Транспорты: xhttp vs reality vs vless
- **[id=118711..118719|—/Никита|19.12.2025]** на примере недавней борьбы с ддосом цепануло reality (ограничивали TCP-трафик, сырой), а xhttp TLS проходил как реальный трафик — поэтому живёт.
- **[id=118696..118699|—|19.12.2025]** xhttp работает поверх TCP (UDP там нет вообще): vless спрятан внутри http-запросов, не детектится как сырой трафик, выглядит как реальный сайт. Разница с vless tcp: там влесс идёт поверх tcp непосредственно.
- **[id=118654|Евген|19.12.2025]** нашёл ядро mihomo с поддержкой xhttp (клиент koala clash, засунул сервер с xhttp — работало); репо: **[id=118022|—|19.12.2025]** https://github.com/vffuunnyy/mihetero ; в призрак-боксе (Ghost B) xhttp обещают, в дев-ветке есть (id=118661..118664|Никита).
- **[id=118504|Евген|19.12.2025]** засунул xhttp в коалу (clash) — «ну такое».
- **[id=118527|c0mrade|19.12.2025]** не всё, что выглядит как лаг бота — хостер: у бота есть мидлварь throttling, чтобы не улетать в лимиты API (сообщения «throttling» в логах).
- **[id=120547|SUPPORT|19.12.2025]** и ещё один юзер: после смены транспорта на xhttp пропала проблема отключения VPN при запуске TikTok; **[id=118567|R0xTaDDy|19.12.2025]** TikTok любит рвать туннель.

## Роутинг: YouTube без рекламы, Steam, RU-direct
- **[id=117184..117204|Данил/R0xTaDDy|19.12.2025]** ютуб читается как RU после маршрута на RU-ноду, но реклама остаётся — не все домены зароутил; смотреть на домены.
- **[id=118405|Рустам|19.12.2025]** список доменов YouTube для роутинга:
```
yt3.ggpht.com, yt4.ggpht.com, yt3.googleusercontent.com, googlevideo.com,
jnn-pa.googleapis.com, stable.dl2.discordapp.net, wide-youtube.l.google.com,
youtube-nocookie.com, youtube-ui.l.google.com, youtube.com,
youtubeembeddedplayer.googleapis.com, youtubekids.com, youtubei.googleapis.com,
youtu.be, yt-video-upload.l.google.com, ytimg.com, ytimg.l.google.com
```
- **[id=117221|—|19.12.2025]** правило Xray (YouTube→RU-аутбаунд + RU-ресурсы в директ):
```
"routing": { "rules": [ { "type": "field", "domain": [
  "geosite:youtube", "ggpht.cn", "ggpht.com", "full:googlevideo.com", "gvt1.com",
  "youtube.ru", "youtube-nocookie.com", "gvt2.com", "video.google.com",
  "wide-youtube.l.google.com", "withyoutube.com", "youtu.be", "youtube.com",
  "youtubeeducation.com", "youtubeembeddedplayer.googleapis.com", "youtubefanfest.com",
  "youtubegaming.com", "youtubego.co.id", "youtubego.co.in", "youtubego.com",
  "youtubego.com.br", "youtubego.id", "youtubego.in", "youtubei.googleapis.com",
  "youtubekids.com", "youtubemobilesupport.com", "yt.be", "ytimg.com",
  "2ip.io", "geoip:ru", "category-ru-gov", "kinopoisk.ru", "hd.kinopoisk.ru",
  "pochta.ru", "vkusnoitochka.ru", "auto.ru", "rzd.ru"
], "outboundTag": "SS_OUTBOUND_TO_RU" } ] }
```
- **[id=117214/117277|R0xTaDDy/Данил|19.12.2025]** после смены конфига в панеле конфиг сам подтягивается, но у Данила заработало только после полного docker compose down && docker compose up -d && docker compose logs -f -t на сервере и ноде.
- **[id=117347|Данил|19.12.2025]** правило «Steam → DIRECT» (не сработало):
```
{ "type": "field", "domain": ["geosite:steam","domain:steamcommunity.com",
"domain:steamgames.com","domain:steampowered.com","domain:steamstatic.com",
"domain:steamcdn-a.akamaihd.net","domain:steamstore-a.akamaihd.net"], "outboundTag": "DIRECT" }
```
- **[id=118490|—|19.12.2025]** расширенное (тоже не воркает — качает всё равно через впн, ограничение 100МБ не снимается):
```
{ "type": "field", "domain": ["geosite:steam","domain:steamcommunity.com","domain:steamgames.com",
"domain:steampowered.com","domain:steamstatic.com","domain:steamcdn-a.akamaihd.net",
"domain:steamstore-a.akamaihd.net","domain:steamuserimages-a.akamaihd.net",
"domain:steambroadcast.akamaized.net","domain:store.steampowered.com"], "outboundTag": "DIRECT" },
{ "type": "field", "ip": ["23.66.0.0/16","23.74.0.0/16","65.60.0.0/16","103.125.0.0/16",
"104.154.0.0/16","128.0.0.0/8","146.66.0.0/16","155.133.0.0/16","185.12.24.0/24",
"192.155.0.0/16","202.152.0.0/16","207.246.0.0/16"], "outboundTag": "DIRECT" }
```
- **[id=117414|—|19.12.2025]** в mihomo (Mihhono) можно ограничить по имени процесса.
- **[id=118032|Евген|19.12.2025]** для торрентов предлагали в каждый конфиг ноды:
```
{ "type": "field", "protocol": ["bittorrent"], "outboundTag": "DIRECT" }
```
  но **[id=118035/118041|Alexander Kazaryan]** protocol-правило на практике не работает (трафик всё равно через сервер, потому люди ставят tblocker).
- **[id=122755|Евген|21.12.2025]** скелет RU-роутинга от нейронки (vk/yandex/mailru + geoip:ru + private → direct, всё остальное → proxy) — «дальше сам копай».
- **[id=122711|Евген|21.12.2025]** RU-ресурсы лучше закручивать директом сразу на сервере — смысл пускать их через впн.
- **[id=123633|Евген|21.12.2025]** перепост с канала Happ: полностью переработанный GeoIP/Geosite — фильтрация «директа» на уровне IP, на доменном остались только исключения; починили Google Play; Twitch без ограничений качества и рекламы; .dat урезаны — 15 МБ на старте, 32-34 МБ под полной нагрузкой (айфоновский вылет на reality исключён); авторы @ristavor @PentiumB @ReverseMarv @devvoking @Razorblood @vl_matveev @md_parsa; репо antifilter.download, 1andrevich/re-filter-lists, runetfreedom, antifilter.network, MaxMind, IPLite, sapics/ip-location-db, v2fly.
- **[id=119134|Haxonate|19.12.2025]** доки роутинга xray: https://xtls.github.io/en/config/routing.html ; **[id=119135|Тимур]** https://xraycore.org/ru/misc/dns_roulette/ (DNS-«рулетка»).
- **[id=119721|—|20.12.2025]** дискуссия Xray-core по директу: https://github.com/XTLS/Xray-core/discussions/4113

## Балансировка нод
- **[id=118204|Haxonate|19.12.2025]** DNS-балансировка — хуйня полная; хрей-балансировка сложнее в настройке, но универсальнее (в конфиге); **[id=118196/118193|Haxonate/IL]** белых списков больше нет, отдали — балансировка через A-запись с IP нескольких нод работает, но просто «рандом» (id=118186|—).
- **[id=118948|Евген|19.12.2025]** при DNS/round-robin каждое подключение уходит на разную ноду, загрузка не меряется; healthcheck не даёт понимания загруженности (id=118940|Евген); с «хостом, который мониторит все сервера и отдаёт клиенту ноду с лучшим пингом» это лучший вариант, но нужен мощный сервер-балансер (id=118907|—).
- **[id=118157..118163|Тимур/Андрей|19.12.2025]** на один домен через DNS можно повесить 4+ ноды — DNS нагрузки не несёт; у кого-то каждая нода на своём домене + ограничение сквадами.
- **[id=118024|—|19.12.2025]** mihomo как балансер гибкий, можно направлять приложения, но нужен отдельный сервер (id=119110|Haxonate).

## Бот Bedolaga: поведение и настройки
- **[id=115528/115527|—|18.12.2025]** параметра BUY_TRAFFIC_BUTTON в export-env нет; вбивание руками BUY_TRAFFIC_BUTTON=ru сбрасывается после ребута; **[id=117501|—|19.12.2025]** WARNING Missing localization key 'BUY_TRAFFIC_BUTTON' for language 'ru' — лечится ручным вбиванием в .env.
- **[id=117575|Й Цукен|19.12.2025]** чтобы убрать лишние языки: DEFAULT_LANGUAGE=ru, AVAILABLE_LANGUAGES=ru, LANGUAGE_SELECTION_ENABLED=false.
- **[id=121357|Й Цукен|21.12.2025]** в env.example и в «traffic package config» значения надо в кавычках "" — иначе бот не принимает данные (вота 2 дня).
- **[id=121962|Й Цукен|21.12.2025]** env из бота vs env с гитхаба: разные имена (таймзона полностью vs TZ), HAPP_DOWNLOAD_LINK_ANDROID/IOS/MACOS/PC/WINDOWS; экспортированный и стоковый env надо мержить вручную (id=121803|Й Цукен).
- **[id=119590|🪲|20.12.2025]** настройки, сделанные внутри бота, не хранятся в docker-образе; приоритет у .env — бот не перезапишет то, что прописано в .env (id=119643|Тимур). Перенос: наклацать в боте, выгрузить env, перенести в основной (id=119573|Й Цукен).
- **[id=119941|Евген|20.12.2025]** замена дефолтной картинки бота: заменить vpn_logo.png в корне папки бота, то же имя, рестарт; нужен именно формат, в котором файл отправляется как фото (jpg, без сжатия); **[id=119943|Тимур]** кнопки сквад-картинки: в боте зайти в сквад и поменять.
- **[id=119897..119929|R0xTaDDy/Тимур/libkit|20.12.2025]** «Сервера» в боте = сквады ремны; в один сквад можно сунуть сколько надо серверов; SIMPLE_SUBSCRIPTION_SQUAD_UUID в .env — сквад для «Быстрой покупки»; при одном скваде он дефолт везде; триал-сквад включается кнопкой в настройках серверов бота; автовключение триала после /start нет (id=118083|Евген).
- **[id=118413|SUPPORT|19.12.2025]** клиенты в ремне подтянутся в бот через «синхронизацию» — да.
- **[id=115585|Александр|18.12.2025]** «Ошибка автосписание» приходит каждый час — отключается в настройках автоплатежа; логики уведомления нет.
- **[id=119899|R0xTaDDy|20.12.2025]** пользователь не попадает в default-squad — надо выдать UUID сквада, который будет выдаваться.
- **[id=120389..120397|R0xTaDDy/—|20.12.2025]** на ПК Telegram не хавает happ:// — нужен редирект-сервис: https://redirect.com/r?redirect_to=happ://add/ ; в app-config urlScheme: https://redirect.example.com/?system&redirect_to=clash://install-config?url= ; **[id=120398|anmbl]** v2raytun://add/.
- **[id=118467|Й Цукен|19.12.2025]** Telegram webhook Unauthorized — надо открыть API на сервере.
- **[id=118527|c0mrade|19.12.2025]** у бота есть мидлварь throttling (защита от лимитов Telegram API) — «медленные операции» в логах не всегда проблема хостера.
- **[id=119408/118407|Haxonate/Й Цукен|19.12.2025]** бот-экспорт env: это файл, руками в .env надо вводить всё самим.
- **[id=121311|libkit|21.12.2025]** звёзды за покупку идут на баланс бота; вывод через Fragment от 1000 звёзд.
- **[id=121677|Тимур|21.12.2025]** id канала для обязательной подписки: в настройках TG включить отображение ID; бот должен быть добавлен в группу (id=120128|Й Цукен).
- **[id=118527|c0mrade|19.12.2025]** тротлинг-мидлварь: сообщения по 5-10 сек — это не хостер.
- **[id=121616|Nekrasov|21.12.2025]** miniapp index.html менялся, а изменения не появились — файл не примонтирован в контейнер; **[id=123617|R0xTaDDy]** в docker-compose монтируешь путь на хосте в контейнер.
- **[id=121370|Мультитысячник|21.12.2025]** сообщение приглашения по партнёрке редактируется в локалях (id=123625|R0xTaDDy: «В локалях»).

## Баги бота (декабрь 2025)
- **[id=118559|Тимур|19.12.2025]** отчёты не идут: asyncpg InvalidParameterValueError «cannot get array length of a scalar» на запросе count distinct по subscriptions.connected_squads (JSONB).
- **[id=118260/119625|Товарищ|20.12.2025]** бот 2.9.1 + ремна 2.4.2: API Error 404 Cannot GET /api/nodes/usage/realtime (старый путь статистики) — реалтайм-статистика недоступна до патча.
- **[id=117493|Кирилл Т|19.12.2025]** «Критическая ошибка синхронизации пользователей: greenlet_spawn has not been called» — после восстановления базы из бэкапа.
- **[id=122869|SUPPORT|21.12.2025]** баг с истёкшими пользователями: в ремне есть, в боте нет.
- **[id=119770|valera.|20.12.2025]** при покупке подписки трафик с триала не сбрасывается.
- **[id=123160|Deleted Account|21.12.2025]** подписка продлилась как за 1 устройство при 4 устройствах юзера (простая покупка идёт по дефолту).
- **[id=121354|Gy9vin|21.12.2025]** пример бана: ID 79156181, «багюз на триале» — при лимите 5 ГБ съел 112 ГБ.
- **[id=119988|Deleted Account|20.12.2025]** фрод: @MarkWilliams_tI ддосит боты и предлагает заплатить 150$ за остановку ддоса (бан).

## Миниаппка/Happ на андроиде: баг
- **[id=120938|—|21.12.2025]** Telegram Mini App на андроидах открывается в браузере вместо миниаппа — это у всех андроидов, на iOS норм (со слов Егора). Решение в чанке: редирект-страница, кеш TG чистить не помогает.

## White lists (БС) и хостинг под БС
- **[id=118193..118198|IL/Дмитрий/Haxonate|19.12.2025]** гайдов по белым спискам нет — «Нигде», «Тебе его никто не даст»; **[id=118201|Дмитрий]** «Мы не занимаемся обходами блокировок, товарищ майор — у нас тут группа по интересам».
- **[id=118215|IL|19.12.2025]** список пулов IP, проходящих БС (обсуждение в Discord, источник не проверен):
```
RU: 51.250.0.0/17 YANDEXCLOUD; 84.201.128.0/18 YANDEXCLOUD; 158.160.0.0/16 YANDEXCLOUD;
217.16.24.0/21 VKCS; 185.39.206.0/24 TW-Cloud (тут хостится 86channel.ru);
95.163.248.0/22 VKCS (Digital Networks MSM); 91.222.239.0/24 TW-Cloud;
95.181.182.0/24 EdgeCenter CDN; 89.253.200.0/21 ASTRA CLOUD (rusonyx, Москва)
За границей: 185.177.73.0/24 MVPS (Кипр); 134.17.94.0/24 CLOUD MTS BY (Минск);
185.141.216.0/24 Rica Web Services (Монреаль); 103.111.114.0/24 Melbikomas (Мумбаи)
```
- **[id=118919/118923|AimedMaksim/—|19.12.2025]** российские VDS, входящие в БС, по их данным — ВК Клауд и Яндекс Клауд.
- **[id=121776|anmbl|21.12.2025]** на хосте с BS взял Швецию и Финляндию — IP из пула 193.68.88.0/23, геоип — Латвия (пул не соответствует стране).
- **[id=123538|хай|21.12.2025]** biill-хост: промо в Японии с любыми SNI под БС — пару дней назад взломали, всё капут; JP без промо — не все SNI работали.
- **[id=122837|AIRVPN|21.12.2025]** профиль = несколько тегов SNI на одну ноду (см. выше про 443).

## События РКН/ТСПУ (18-21.12.2025)
- **[id=116550|—|18.12.2025]** Госуслуги начали блокировать доступ за использование VPN — аккаунт блокируют на 72 часа; рост числа блокировок; развязка — подтвердить личность через госсообщения Max.
- **[id=117543..117552|stormie/—|19.12.2025]** РКН давит: ВК на работе еле грузится, сообщения в TG уходят минуты три (на бытовом интернете).
- **[id=119661|AIRVPN|20.12.2025]** Билайн днём режет скорость на VPN-хостах (Германия/финки/НЛ), ночью ок; с ip 51.* — до 500 кбит, не в зоне ограничения.
- **[id=123506..123516|Никита/Евген/Й Цукен/хай|21.12.2025]** по городам: Билайн и Yota в Сочи — «пизда»: ТСПУ пинг есть, по SNI нет; в Крыму обход по SNI до сих пор работает (Севастополь нет, «на волне» работает); на Мегафоне из ~700 SNI работало 70 (в BS без VPN на wifi все 700).
- **[id=123585|хай|21.12.2025]** не у всех BS работает даже с полным набором протоколов xray; дело в подсети (id=123529|—).
- **[id=119553|—|20.12.2025]** (РКН/бс контекст) 170 рыл юзают VPN бесплатно.

## Хостинги: опыт (18-21.12.2025)
- **[id=118422|stayinit|19.12.2025]** худшие по личному году тестов (15+ хостингов): serva.one (худший проц, сразу манибэк), qwins (проц говно, аптайм ~80%), u1host (проц норм, отвалы частые), adminvps (роуты говна; docker не ставится, id=118525|Александр), spacecore (норм, но роуты/пинги), hostvds (серв норм, гео пиздец), aeza (в 2024 — параша), pq(ufo) — обходить стороной.
- **[id=115777|Товарищ|18.12.2025]** Сенко: Германия падает периодически, Нидерланды — чуть ли не каждый день; **[id=115786|Zavulon|18.12.2025]** на firstbyte проблем небыло.
- **[id=117820|Rothschild|19.12.2025]** взял впску в Нидерландах — пул в Токио, скорость еле 40 МБ.
- **[id=117295|—|19.12.2025]** hip hosting: Финляндия 250 МБ как и написано, обещали «до 10Г»; Германия 300 МБ (id=117154|paralichevsky); нидерланды за полчаса активация (id=117143); **[id=120781|—|20.12.2025]** на hip вторая нода (Нидерланды) не заработала из-за selfsteal-конфига под первую ноду.
- **[id=119829|Й Цукен|20.12.2025]** ztv — RU-домен за 250. **[id=119826|Евген|20.12.2025]** regway — главное продление норм.
- **[id=119500|rmzn|20.12.2025]** dhost Нидерланды упали на полчаса; **[id=120141|VoidSignal|20.12.2025]** Германия на dhost не очень, отваливается часто; **[id=120180|VoidSignal]** если держать сервер на dhost постоянно >500 МБ/с — выключают, обратно через бота не включить, только в поддержку.
- **[id=120165|VoidSignal|20.12.2025]** play2go или 4vps: 4 сервера (США, Польша, Дания 25% + Эстония) — везде полёт отличный; **[id=120171|feds]** у кента на play2go сеть ложится каждые 5 минут на 10-20 сек.
- **[id=120198|—|20.12.2025]** для панели и бота с каналом 100 МБ/с — justhost: 300 МБ/с канал (до 400), 4 ядра/4 ГБ за 500 р/мес, промики до 340 р/мес (id=120202/120206).
- **[id=120218|—|20.12.2025]** Timeweb Нидерланды — заявлен 1 ГБ/с, но fair-share.
- **[id=122861|Камушек|21.12.2025]** nodehost Швеция 120 р/мес (1/1/10, 1 Gbit) — тест.
- **[id=120097|—|20.12.2025]** sraki.ovh за 170 р/мес + DDoS-защита OVH.
- **[id=117309|—|19.12.2025]** hoster russia RU 180 р/мес + 30 ТБ трафика.
- **[id=117727|Й Цукен|19.12.2025]** datacheap.ru 4/4 за 840 р (сайт открывается криво в Opera).
- **[id=118507/118517|Whiteness|19.12.2025]** centhost Эстония 1250 р — дёшево, без рекламы; 3 дня давал 200 МБит, потом 700-900.
- **[id=118295|Haxonate|19.12.2025]** на bill «Латвия» по трассировке — Германия (213 мс пинг, у Zavulon 144); **[id=122885|Камушек|21.12.2025]** после выдачи новой пачки серверов у bill нет подключения к Латвии; сбор отзывов на otzovik (id=122905).
- **[id=121128|feds|21.12.2025]** the.hosting за 1$ месяц.
- **[id=117159|Lywome|19.12.2025]** datalix Германия: тест выдал 400-600 МБ, потом анти-DDoS проредил до 50-100 Мбит; **[id=117138]** нет русской оплаты.
- **[id=119281|.|19.12.2025]** 1 цент Швеция (для теста), медленные диски (50 МБ/с, id=118558).
- **[id=116483..116504|SawGoD/—|18.12.2025]** ищут хостинг с честными 10 Гбит/с — таких не видели; 25-гбит-сервера забивают (id=116498).
- **[id=118318|Данил|19.12.2025]** «Германия» у хип — обещали «волшебные 10Г», получил 100-200.

## Инструменты и ссылки
- **[id=118118..118131|Whiteness/—|19.12.2025]** rw-backup (distillium/remnawave-backup-restore) — восстановление ремны: снести redis.
- **[id=118626|SawGoD|19.12.2025]** Netdata — мониторинг, очень много метрик; идея — прикрутить node-exporter, xray-checker, алерты; **[id=116575|—|18.12.2025]** Prometheus + Grafana + Alertmanager, либо Zabbix; **[id=120118|—|20.12.2025]** гайд по Grafana-мониторингу: https://wiki.egam.es/ru/configuration/grafana-monitoring-setup/
- **[id=116244..116306|—/Haxonate|18.12.2025]** lazydocker — TUI для docker (контейнеры/логи/сети/объёмы), lazygit для git.
- **[id=118472..118477|Васян/—|19.12.2025]** клиенты: Happ — нативный, сразу на все ОС; форк clashX (клэш) даёт работу с HWID.
- **[id=118770..118779|Рустам/Haxonate|19.12.2025]** мобильные тарифы-обманки: активация через Госуслуги, на сайтах операторов другие цифры тарифов (Озон-скидки), по факту до 1 ТБ в месяц.
- **[id=119847|Haxonate|20.12.2025]** вместо Telegram Wallet — Antarktik wallet, оплата по СБП.
- **[id=121296|Egor|21.12.2025]** Bedolaga 2.9.2 changelog (см. выше) и ссылки [Release]/[Full Changelog].
- **[id=116509|—|18.12.2025]** Prometheus/Grafana/Netdata вместо ручного htop — алерты о проблемах превентивно (id=116569|—).

## Разное поведение/баги панели
- **[id=118268|Кирилл Т|19.12.2025]** у пары новых юзеров (ремна 2.3.1 с нуля) активна подписка, но кнопка подключения не работает — логи смотреть.
- **[id=116222|IL|18.12.2025]** miniapp в Telegram Web (браузере) открывается криво — «используйте предусмотренные сервисом сценарии».
- **[id=117553|stayinit|19.12.2025]** hostvds: ipv4 показывает Гонконг, ipv6 — Иран; с ipv6 нельзя грузить файлы в дискорд.
- **[id=116767|17|18.12.2025]** серверный роутинг срабатывает после клиентского: клиентский в DIRECT (условный сайт) перекрывает серверный блок.
- **[id=121112|Рустам|21.12.2025]** «я ненавижу ремна нетворк» (docker-сети ремны — боль).
- **[id=117734|Й Цукен|19.12.2025]** рекомендуемые требования ремны — 4/4 (ядра/ГБ); **[id=123249|Фантомас|21.12.2025]** для 10-15 человек 1/1/1-гиг мало, **[id=123275|—]** 1/2 с 3xui хватит; **[id=123271|Никита]** если исходное xhttp — то 2/4.
- **[id=118467|Й Цукен|19.12.2025]** acme.sh давно не уведомляет на e-mail о скором окончании сертификатов — поднимать мониторинг с алертами в TG (id=118643|—).

## Флуд/нетехническое
- (флуд) донат-бот Bedolaga каждые 2-3 часа, десятки донатов по 100-500 р; скиды «сотки» внутри чата; дроп песен Suno; «Колумбия ВПН» скандал с пробивом юзеров (@Drekiter/@IceStormGG); продажа «БС» за 20-30к и скандал вокруг продажи белых списков;苹果/андроид споры; «Госуслуги/Max/Мос Nadzor» шутки; продажа/бронь миниапп (10к, 5к);onetimers.

(Файл охватывает id 115081..123677 полностью.)
