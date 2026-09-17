# Заметки из chunk_014 (id 68963..74984, 22.11.2025–26.11.2025)

## ⚡ ГЛАВНОЕ СОБЫТИЕ: массовая блокировка VLESS/Reality через FakeTLS/СКАТ (22–25.11.2025)
- **[id=69358,69362,70632,70651,70943,72004,72014,72648,74426|Valerii,Никита,InsiderКэм,Серёжа|22–25.11](https://t.me/c/2941121338/69358)** С 22.11 в ряде регионов (Урал: ЕКБ, Омск, Новосибирск, Крым, Уфа, Оренбург, Барнаул, Красноярск, Сургут, Псков) отвалился VLESS+Reality (FakeTLS): блокируют не сам протокол VLESS, а TLS1.3+ECH и TLS-in-TLS, используемые XRay; возможно последствие разворачивания белых списков. 24.11: начали снимать блокировки — «влесс заработал сам» ([id=72533,72642](https://t.me/c/2941121338/72533)); в ЕКБ на ТСПУ-тестах отвалились замедления ([id=72670](https://t.me/c/2941121338/72670)). Также сбой мог быть связан с ДДОС ботнета на магистрали ([id=73444–73457](https://t.me/c/2941121338/73444)).
- **[id=71846,72014,72425|—|23.11](https://t.me/c/2941121338/71846)** Рабочие решения текущей проблемы:
  1. меняешь fingerprint на randomized (или qq — у некоторых тоже отваливается);
  2. меняешь транспорт на grpc;
  3. меняешь транспорт на xhttp (минус: mihomo и, вероятно, iOS-клиенты).
  По порядку пробовать. `randomized` генерирует уникальный отпечаток ([id=71805](https://t.me/c/2941121338/71805)); на 3xui helped uTLS randomized ([id=71623](https://t.me/c/2941121338/71623)).
- **[id=71060,71062,71588,72100,74926|Никита,Zavulon|23.11–26.11](https://t.me/c/2941121338/71060)** xhttp+selfsni (селфстил) — главный рабочий рецепт: «воскрешает всё», «большие впн пересели на xHTTP + селфстил сни» (70к юзеров), работает на iPhone (до XR, проверено на 10 айфонах, 13-16 модели), скорость у многих даже выросла вдвое. Минусы: Mihomo/Clash-клиенты не поддерживают xhttp (там не xray core); Happ на Windows кривой, grpc там не работает; на Mac не видят серверы с xhttp (clash/hiddify) — только Happ/V2RayTun.
- **[id=70350|Zavulon|23.11](https://t.me/c/2941121338/70350)** Стратегия: на каждую зарубежную ноду — 1 российская с shadowsocks.
- **[id=72416|—|24.11](https://t.me/c/2941121338/72416)** Локальный вариант для винды: некорей поднимает сокс + ProxyFire раскидывает по доменам/приложениям.

## Конфиги xhttp (дословные)
- **[id=69397,69398|kinvsh|22.11](https://t.me/c/2941121338/69397)** Профиль xhttp+reality (один из первых рабочих, дословный):
  ```json
  {
    "log": {"loglevel": "warning"},
    "dns": {"servers": [{"address": "https://dns.google/dns-query", "skipFallback": false}], "queryStrategy": "UseIPv4"},
    "inbounds": [{
      "tag": "СВОЙ", "port": 443, "protocol": "vless",
      "settings": {"clients": [], "decryption": "none"},
      "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
      "streamSettings": {
        "network": "xhttp", "security": "reality",
        "xhttpSettings": {"host": "ДОМЕН", "mode": "stream-one", "path": "/video-stream"},
        "realitySettings": {"dest": "/dev/shm/nginx.sock", "show": false, "xver": 1, "spiderX": "",
          "shortIds": ["157b68017451de6d"], "privateKey": "СВОЙ", "serverNames": ["ДОМЕН"]}
      }
    }],
    "outbounds": [{"tag": "DIRECT", "protocol": "freedom"}, {"tag": "BLOCK", "protocol": "blackhole"},
      {"tag": "warp-out", "protocol": "freedom", "settings": {"domainStrategy": "UseIP"},
       "streamSettings": {"sockopt": {"interface": "warp", "tcpFastOpen": true}}}],
    "routing": {"rules": [
      {"ip": ["geoip:private"], "type": "field", "outboundTag": "BLOCK"},
      {"type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK"},
      {"type": "field", "domain": ["whoer.net","browserleaks.com","2ip.io","2ip.ru"], "outboundTag": "warp-out"}]}
  }
  ```
- **[id=71159,72142,72155|Камушек прямо из космоса|23.11](https://t.me/c/2941121338/71159)** Обход Reality для блокировок (кратко): `realitySettings.dest = 1.1.1.1:443`, `serverNames = [""]` — работает в Приморском крае, Иркутской обл., Новосибирской обл. Полный профиль приложен в сообщении (vless-reality-vision, port 443, sniffing routeOnly true, privateKey, DNS cloudflare/google, ad-block rules).
- **[id=71088,71131,72141,72154|Никита (ТПСУ)|23.11–24.11](https://t.me/c/2941121338/71088)** xhttp+TLS+selfsni, только для своего домена, серты letsencrypt смонтировать в докер ноды (дословный инбаунд):
  ```json
  {"tag": "xHTTP", "port": 443, "listen": "0.0.0.0", "protocol": "vless",
   "settings": {"clients": [], "decryption": "none"},
   "sniffing": {"enabled": true, "routeOnly": false, "destOverride": ["http","tls","quic"], "metadataOnly": false},
   "streamSettings": {
     "network": "xhttp", "security": "tls",
     "tlsSettings": {"alpn": ["h2","http/1.1"], "maxVersion": "1.3", "minVersion": "1.2",
       "serverName": "селфсни", "fingerprint": "chrome",
       "certificates": [{"usage": "encipherment",
         "keyFile": "/etc/letsencrypt/live/домен/privkey.pem", "oneTimeLoading": false,
         "certificateFile": "/etc/letsencrypt/live/домен/fullchain.pem"}],
       "allowInsecure": false, "rejectUnknownSni": false, "disableSystemRoot": false, "enableSessionResumption": false},
     "xhttpSettings": {"host": "селфсни", "mode": "auto", "path": "/", "headers": {}, "noSSEHeader": false,
       "xPaddingBytes": "100-1000", "scMaxBufferedPosts": 30, "scMaxEachPostBytes": 1000000, "scStreamUpServerSecs": "20-80"}
   }}
  ```
- **[id=72155|Просто Даня|24.11](https://t.me/c/2941121338/72155)** Гайд xhttp для селфстила на caddy: пути сертов
  ```
  keyFile: /certs/caddy/certificates/acme-v02.api.letsencrypt.org-directory/вашдомен/ключ.key
  certificateFile: /certs/caddy/certificates/acme-v02.api.letsencrypt.org-directory/вашдомен/серт.crt
  ```
  Монтирование в докер ноды:
  ```yaml
  services:
    remnanode:
      image: remnawave/node:latest
      network_mode: host
      volumes:
        - selfsteel_caddy_data_selfsteal:/certs:ro
  volumes:
    selfsteel_caddy_data_selfsteal:
      external: true
  ```
  После смены конфигурации Xray не забудь выбрать xhttp-профиль в сквадах/хостах/нодах; для mihomo с ручным именем прокси — убрать старый сервер.
- **[id=71604,71627,74932|Zavulon|23–26.11](https://t.me/c/2941121338/71604)** xhttp+reality для егеймса, конфиг нормальный у тех кто с блоками (дословно):
  ```json
  {"tag": "xHTTPgermany", "port": 443, "protocol": "vless",
   "settings": {"clients": [], "decryption": "none"},
   "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
   "streamSettings": {
     "network": "xhttp", "security": "reality",
     "xhttpSettings": {"mode": "auto", "path": "/germany-xhttp"},
     "realitySettings": {"dest": "/dev/shm/nginx.sock", "show": false, "xver": 1, "spiderX": "",
       "shortIds": ["4be3b5e3"], "privateKey": "9ho77A1QVREFFDhQkM", "serverNames": ["domen.life"]}
   }}
  ```
  В хосты в xHTTP extra (дословно):
  ```json
  {"xmux": {"cMaxReuseTimes": 0, "maxConcurrency": "16-32", "maxConnections": 0, "hKeepAlivePeriod": 0,
    "hMaxRequestTimes": "600-900", "hMaxReusableSecs": "1800-3000"},
   "headers": {}, "noGRPCHeader": false, "xPaddingBytes": "100-1000",
   "scMaxEachPostBytes": 1000000, "scMinPostsIntervalMs": 30, "scStreamUpServerSecs": "20-80"}
  ```
  Минус: mihomo идёт лесом; скорости на высоте, нагрузка небольшая.
- **[id=73232,73234,73266|—|-и|24.11](https://t.me/c/2941121338/73232)** Краткий рецепт: tcp→xhttp + `"xhttpSettings": {"path": "/рандомные_буквы"}`; Reality dest `127.0.0.1:8443` ([id=74673,74713](https://t.me/c/2941121338/74673)).
- **[id=72532,72529,72380|Илья,Zavulon|24.11](https://t.me/c/2941121338/72532)** gRPC работает лучше всего: `raw` это `tcp` ([id=71606](https://t.me/c/2941121338/71606)); в ремне профиль на raw не сохраняется с grpc принудительно ([id=70939](https://t.me/c/2941121338/70939)).

## Безопасность ноды (против СКАТ/бан ноды)
- **[id=71539,71557,71552,72806|SawGoD|23–24.11](https://t.me/c/2941121338/71539)** Сейв от бана ноды/домена с обновлением СКАТ (цитируемый текст): SNI на селфстил с живым сайтом и нормальными сертификатами; порт 443 (8443 не рекомендуется); TLS-отпечаток браузера (chrome/edge/safari); policy с адекватным connIdle и uplinkOnly/downlinkOnly; чувствительные сайты (госы, банки, налоговая) в директ; 1–2 аккуратных профиля вместо зоопарка; трафик максимально похож на обычный HTTPS. Не городить TLS-мутантов, когда SNI и IP не бьются; не использовать левые порты; не лепить на один IP всё подряд.
- **[id=69712–69715|Zavulon|22.11](https://t.me/c/2941121338/69712)** На ру-нодах блочить ру-сервисы: роутинг на них и хардлок, если кто-то выключит роутинг — понюхал бебру.

## Миниапка / редиректы и прочее
- **[id=71557|SawGoD|23.11](https://t.me/c/2941121338/71557)** Хосты для бота (DOMEN.life и другие).
- **[id=73336,73337,73339,73341,73342|—,IS,Илья|24.11](https://t.me/c/2941121338/73336)** По resty — феи в whitе, у Ильи 25TB/год.
- **[id=73943|Просто Даня|25.11](https://t.me/c/2941121338/73943)** Мультикнопка в боте: содержимое под кнопкой (апк, ссылка, download).
- **[id=71555|SawGoD|23.11](https://t.me/c/2941121338/71555)** Перепродажа Vless от ilovvecn (id 1330492370) — блок и переоформление.
- **[id=71515|SawGoD|23.11](https://t.me/c/2941121338/71515)** Криптопровайдеры (Crypto-Host): и запрос на VPS-хостинг от state-структуры.
- **[id=71555|SawGoD|23.11](https://t.me/c/2941121338/71555)** crypto-платежи: для реги в bbot.

## Похоже события
- **[id=69897,69915,70537,70556|Й Цукен,Илья,17|23.11](https://t.me/c/2941121338/69897)** Стоп, стоп. Стоп-стоп, пять раз. Вот профиль 3xui, который видит 24/7 своих клиентов.
- **[id=71300|—|23.11](https://t.me/c/2941121338/71300)** Скорость 30 мбит при 200 мбит от провайдера — 2 хоста (1 гигабит, 200 мбит) — «мда, реально блочат».
- **[id=70907,70908,71543,72014|—|23.11](https://t.me/c/2941121338/70907)** Глючность: 30mbit на 200mbit, «пинг на одном сервере, на другом — нет», «у меня один работает, один лежит», не один и тот же. Забой в реалити и тд.

## Клиенты (Happ, Mihomo/Clash)
- **[id=71640,71707,71713,71807|—,hdhdh4226ru|23.11](https://t.me/c/2941121338/71640)** Забирайте ваш конфиг аески, если кто чекал — и конфиг и продолжение на «XHTTP» — с реалити сни тоже работает.
- **[id=71637,71647,71648|—|23.11](https://t.me/c/2941121338/71637)** Полезный конфиг «Make sure to include this thing» в полезностях — без ПИН-текста (НЕ полезное).
- **[id=71137|—|23.11](https://t.me/c/2941121338/71137)** FlClashX = аезовский клиент, тоже перевёл.
- **[id=70981|Zavulon|23.11](https://t.me/c/2941121338/70981)** Юзер не уходит в блок, поэтому он не видит ваше с утра все сервера.
- **[id=69980|Egor|22.11](https://t.me/c/2941121338/69980)** «[Уже не надо.] [Не актуально.] [И не актуально.] [Инфу что тебе не купили] [Про хостинг] [Все работает.]»
- **[id=71143|—|23.11](https://t.me/c/2941121338/71143)** Раywall — над «комплектом».
- **[id=71141|—|23.11](https://t.me/c/2941121338/71141)** На поддомен под белыми списками беру 500 «аноним» — не знаю сколько «5 тихих».
- **[id=71137|—|23.11](https://t.me/c/2941121338/71137)** «Радует, 30-40: у меня теперь сеть работает», «не объясняй».
- **[id=70208|art vs|22.11](https://t.me/c/2941121338/70208)** Поддержку поддерживали (клиент-приложение), не смотрели hendidng.
- **[id=70242,70245|art vs,art vs|22.11](https://t.me/c/2941121338/70242)** StealthNet admin panel: регистрация выдаёт Internal Error 500 — регистрация с переменной, при регистрации с редис-версией.
- **[id=70262|art vs|23.11](https://t.me/c/2941121338/70262)** «Просто поддержали» — на егеймсе: 500 ошибок со стороны nginx, в корне беда, переподключить.
- **[id=70265|Yaroslav|23.11](https://t.me/c/2941121338/70265)** Не от администратора и не с нулевой смены — это уже мультик; подключение
- **[id=70290,70292,70293|—,Yaroslav|23.11](https://t.me/c/2941121338/70290)** Дохер/дхост/ваикор.

## Настройки и переменные бедолаги
- **[id=72495|MAKS|25.11](https://t.me/c/2941121338/72495)** REFERRAL_PROMO_CODE — фейл; PAYMENT_VERIFICATION_AUTO_CHECK_ENABLED=true, PAYMENT_VERIFICATION_AUTO_CHECK_INTERVAL_MINUTES=2, AUTO_PURCHASE_AFTER_TOPUP_ENABLED=true.
- **[id=72499|MAKS|25.11](https://t.me/c/2941121338/72499)** LOGO_FILE — подводят логотипы — «поправится при повторном включении».
- **[id=72551|MAKS|25.11](https://t.me/c/2941121338/72551)** Реклама с редиректа — выходить в чат (реклама в боте — от банка) — «откуда там». Проблемы: уходит при push от «аезы».
- **[id=72552|MAKS|25.11](https://t.me/c/2941121338/72552)** Демо-профиля нет; логотип продается отдельно.
- **[id=72498|MAKS|25.11](https://t.me/c/2941121338/72498)** MAILING_CATEGORIES — «немало рассылок»; фильтры из чата.
- **[id=72490|MAKS|25.11](https://t.me/c/2941121338/72490)** Задача оптимизировать «yookassa-webhook» — хуки.

## Разное
- **[id=71009|Haxonate|23.11](https://t.me/c/2941121338/71009)** Вопросы/настройки/ошибки (дубли): валидация вебхуков + рестарт; curl с гугл-деплоя.
- **[id=71010|Haxonate|23.11](https://t.me/c/2941121338/71010)** Проблема: «обезьяны блять, аж всплакнул 🙈» — чужой конфиг.
- **[id=71014|Haxonate|23.11](https://t.me/c/2941121338/71014)** «Дай сабку» — сравнение новой и старой сборки.
- **[id=71018|Haxonate|23.11](https://t.me/c/2941121338/71018)** Латвия, Польша, Швеция, Эстония, Литва — «все робит».
- **[id=71021|Haxonate|23.11](https://t.me/c/2941121338/71021)** «Пинг серверов не прикрепляется» — подтвердить, что есть три порта.
- **[id=71022|Haxonate|23.11](https://t.me/c/2941121338/71022)** «Перегрузка у Балалайки» — не влияет.
- **[id=71023|Haxonate|23.11](https://t.me/c/2941121338/71023)** «В ёлках не открывается» — старое.
- **[id=71024|Haxonate|23.11](https://t.me/c/2941121338/71024)** «Не может просматривать» — отслеживание, ведро.
- **[id=71025|Haxonate|23.11](https://t.me/c/2941121338/71025)** Услуги на серверах ПГ.
- **[id=71026|Haxonate|23.11](https://t.me/c/2941121338/71026)** ДэБ — надо надо, кастомный конфиг.

## Флуд
- Стим, DotA, игры, сериалы, зубы/импланты 570к, машины/Кинетик Неткрейз Ultra, хостинги «лучшие в мире», « gay bot» (13/73893%), мем-интервью, напоминания про уроки Linux/«50 нод на одном IP» — флуд, не фиксирую.
