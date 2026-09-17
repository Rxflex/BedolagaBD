# Заметки из chunk_096 (id 644636..653221, 05.06.2026 .. 07.06.2026)

## Обновления Bedolaga (05.06)
- **[644694|c0mrade|05.06]** Bedolaga Bot: 50 коммитов, +5833/−1166 строк, ~2550 строк тестов, 1 миграция (обратно совместима). Безопасность: нельзя молча утащить аккаунт через Google/Discord/Яндекс/почту; вход через Telegram одноразовый и ограничен по времени (есть время жизни, как у токена, не выкинет [644820/644826|c0mrade]); объединение аккаунтов по почте только с кодом из письма; приватные вложения в тикетах подписаны и истекают; права админов нельзя выдать выше своих. Платежи: Tribute/Telegram Stars без двойных списаний, оплата Pal24 выбранным способом, автопродление возвращает списанное на баланс. Колесо Фортуны честное. Языки RU/EN/UA/FA/ZH выровнены.
- **[644698|c0mrade|05.06]** Bedolaga Cabinet: 36 коммитов, +2726/−1560, без миграций. Новый хедер-«капсула» на десктопе; мобильная вёрстка; подписанные ссылки на вложения тикетов; закрыта уязвимость с подменой ссылки в мини-аппе; Happ TV работает на Apple TV; пересобрана статистика лендингов.

## Волна блокировок 05–07.06 и механика детекта
- **[646031|—|05.06]** В бегете «частичные проблемы» из-за ТСПУ (официальное сообщение Бегета, SpaceWeb, Datacheap, Timeweb о возможной блокировке их сетей — массовый бан российского облака, см. [645556]).
- **[646160|—|06.06]** Эксперимент Сергея: с обычным SNI серверы банят почти сразу (IP на выброс), с селфстилом не трогают; при этом селфстил не панацея — США ноду перевёл с SNI на селфстил и через день улетела, пришлось менять IP [646481].
- **[646466|—|06.06]** РКН к утру заблокирует домен наглухо (со SNI).
- **[648042|⁯|06.06]** Yandex Cloud: хорошо настроенный XHTTP живёт дольше, чем TCP+Reality; банки не частые.
- **[647601|YungCayde|06.06]** WAF CDN-ки (Билайн) 403 и закрывает соединение, если видит UUID в заголовке/path/query; у grpc нет uuid в открытом виде — поэтому пускает; websocket в билайне не пускает.
- **[647529|pon arķ|06.06]** На СДН возможен grpc reality; xhttp тоже.
- **[647523|Pavel K.|06.06]** Роскомвпн-список можно в шаблон xray; ссылка не подтягивается в JSON-клиенты.
- **[647534|—|06.06]** XHTTP можно за nginx прятать.
- **[643295|Данил|05.06]** (переносится из 095) ТСПУ спуфит TLS: подсовывает настоящий сертификат маскировочного сайта → Xray рвёт соединение.
- **[643462|compact disc|05.06]** В Xray убрали allowInsecure; см. verifyPeerByCertName — серт должен совпадать с SNI.
- **[648525|Руслан И.|06.06]** Озон начал детектить VPN; фикс — рулинг в direct для доменов озона:
  ```json
  { "domain": ["ozonusercontent.com","ozon-credit.ru","ozoncard.ru","o-courier.ru","ocourier.ru"], "outboundTag": "direct" }
  ```
- **[650495|—|07.06]** Список ASN/подсетей «плохих» (VPN-провайдеры): https://github.com/C24Be/AS_Network_List; из него блоклист v4.
- **[650492|ClearedToLand|07.06]** Использование всего списка для блокировки входящих невозможно, но может забанить клиентов; автор ведёт исходящий трафик на ВК/Мейл, живущий в списках: https://github.com/AndreyTimoschuk/nonorkn
- **[649835|사악한 주장|07.06]** Рейтинг хостингов по тестам двух чатов: https://github.com/evi1argument/bedolaga-vps-rating

## Конфиги/гайды (дословно)

### Hysteria2 в Remnawave + certbot (полный гайд) [647736|𝓓𝓮𝓪𝓽𝓱 𝓘𝓼 𝓝𝓸 𝓜𝓸𝓻𝓮|06.06]
```
mkdir -p /opt/certbot && cd /opt/certbot && nano docker-compose.yml
```
```yaml
services:
  certbot:
    container_name: certbot
    image: certbot/certbot
    network_mode: host
    volumes:
      - ./certs:/etc/letsencrypt
```
Первичное получение (порт 80 свободен):
```
docker run --rm \
  -v $(pwd)/certs:/etc/letsencrypt \
  -v $(pwd)/var-lib-letsencrypt:/var/lib/letsencrypt \
  --network host \
  certbot/certbot certonly --standalone \
  --non-interactive --agree-tos \
  --email admin@your-domain.com \
  -d your-domain.com
```
Проброс в Remnawave (в docker-compose ноды):
```yaml
    volumes:
      - '/opt/certbot/certs:/etc/letsencrypt:ro'
```
Профиль Hysteria2 (BBR):
```json
{
  "log": { "loglevel": "none" },
  "inbounds": [
    {
      "tag": "HYSTERIA-BBR",
      "port": 443,
      "listen": "0.0.0.0",
      "protocol": "hysteria",
      "settings": { "clients": [], "version": 2 },
      "streamSettings": {
        "network": "hysteria",
        "security": "tls",
        "finalmask": { "quicParams": { "debug": false, "congestion": "bbr" } },
        "tlsSettings": {
          "alpn": ["h3"],
          "certificates": [
            {
              "keyFile": "/etc/letsencrypt/live/your-domain.com/privkey.pem",
              "certificateFile": "/etc/letsencrypt/live/your-domain.com/fullchain.pem"
            }
          ]
        },
        "hysteriaSettings": { "version": 2 }
      }
    }
  ],
  "outbounds": [
    { "tag": "DIRECT", "protocol": "freedom" },
    { "tag": "BLOCK", "protocol": "blackhole" }
  ],
  "routing": {
    "rules": [
      { "ip": ["geoip:private"], "outboundTag": "BLOCK" },
      { "domain": ["geosite:private"], "outboundTag": "BLOCK" },
      { "protocol": ["bittorrent"], "outboundTag": "BLOCK" }
    ]
  }
}
```
Cron (обновление раз в месяц, 28-го числа):
```
0 0 28 * * cd /opt/certbot && docker compose run --rm certbot renew
```

### VLESS WS + nginx (masquerade «decoy») [651979|Wyatt H.|07.06]
```json
{
  "log": { "loglevel": "warning" },
  "inbounds": [
    {
      "port": 12345,
      "listen": "127.0.0.1",
      "protocol": "vless",
      "settings": { "clients": [ { "id": "ВАШ_ГЕНЕРИРОВАННЫЙ_UUID", "level": 0 } ], "decryption": "none" },
      "streamSettings": { "network": "ws", "wsSettings": { "path": "/ray" } }
    }
  ],
  "outbounds": [ { "protocol": "freedom" } ]
}
```
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/private.key;

    location / {
        root /var/www/html;
        index index.html;
    }

    location /ray {
        if ($http_upgrade != "websocket") { return 404; }
        proxy_redirect off;
        proxy_pass http://127.0.0.1:12345;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### XHTTP за Caddy (без селфстила) [651359|Михаил|07.06]
```
yourdomain.com {
    handle /api* {
        reverse_proxy 127.0.0.1:8443 {
                flush_interval -1
                transport http {
                        versions h2c 1.1
                }
        }
    }
    respond "OK" 200
}
```
- Для xhttp вообще не обязателен селфстил: Caddy занимает TLS, Xray только прокси без шифрования.

### Outbound моста на DE-ноду (xhttp) [649022|x1roko -|06.06]
```json
{
  "protocol": "vless",
  "settings": {
    "vnext": [
      {
        "address": "",
        "port": 443,
        "users": [ { "encryption": "none", "flow": "", "id": "ed7b27b3-ee08-422d-bcb1-7b480e6867c1" } ]
      }
    ]
  },
  "streamSettings": {
    "network": "xhttp",
    "realitySettings": {
      "fingerprint": "firefox",
      "publicKey": "tRm6TvXbOEIUcnp4oiINmqQG4wrmCOzvH97dcvE1U3U",
      "serverName": "rutube.ru",
      "shortId": "af23bc45de678901"
    },
    "security": "reality",
    "xhttpSettings": { "host": "", "mode": "auto", "path": "/xh" }
  },
  "tag": "proxy"
}
```
- Способ получения: пользователь bridge → ключи подключения → скопировать ключ в happ → из happ скопировать секцию outbound сервера и вставить в профиль на серваке [649030].

### VLESS_TCP_REALITY2 (пример из чата, НЕ селфстил — так делать не надо) [646208|lonely|06.06]
```json
{
  "log": { "loglevel": "none" },
  "inbounds": [
    {
      "tag": "VLESS_TCP_REALITY2",
      "port": 443,
      "listen": "0.0.0.0",
      "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "raw",
        "security": "reality",
        "realitySettings": {
          "target": "www.google.com:443",
          "shortIds": [""],
          "privateKey": "<приватный ключ Reality>",
          "serverNames": ["www.google.com"]
        }
      }
    }
  ],
  "outbounds": [ { "tag": "DIRECT", "protocol": "freedom" }, { "tag": "BLOCK", "protocol": "blackhole" } ],
  "routing": {
    "rules": [
      { "ip": ["geoip:private"], "outboundTag": "BLOCK" },
      { "domain": ["geosite:private"], "outboundTag": "BLOCK" },
      { "protocol": ["bittorrent"], "outboundTag": "BLOCK" }
    ]
  }
}
```
- Контекст: у пользователя с SNI (google) ноды отлетают; **[646210|Сергей|06.06]** «фикс» — не конфиг, а селфстил; **[646481]** даже селфстил не всегда панацея.

### JSON с «fingerprint» в realitySettings (невалидный пример — с кавычками-ёлочками) [651024|lonely|07.06]
- Пользователь получил invalid JSON, потому что поставил кавычки “ ” вместо " ":
```json
"realitySettings": { “fingerprint”: “firefox”, ... }
```
- Правильно: fingerprint в realitySettings обычными кавычками; либо указать fingerprint в хосте [651033|$LamCool].

## Обходы/инструменты
- **[644838|Аркадий|05.06]** VPN на телеке Samsung: на новых смарт-ТВ было приложение из магазина, на старых нет; сейчас только через роутер или DNS.
- **[648662|—|06.06]** Проверка, что домен жив/в бане: bschekbot, netprobe.ru/dashboard [650514].
- **[645004|—|05.06]** Ревизия (снятие) IPv6-флуда: ipv6 disable [648437].
- **[646068|Nikita M.|06.06]** Обновление бота: `git pull && make reload`.
- **[647650|YungCayde|06.06]** Ссылка на issue Xray-core: https://github.com/XTLS/Xray-core/issues/6264 (детект по UUID/паттерну).
- **[645537|no content|05.06]** Проверка ЖД (как на SSR...): `df -i` — на самом деле это [651077] df -i/free -h/dmesg для диагностики I/O error (isq).
- **[647703|Коала|06.06]** Чекер подписок (мульти-SNI, ICMP/TCP, ASN/хостинг в мульти-проверках, МТС tcp(tls) с zombie-детектом, багбаунти): bot @Jeremy0x1 — бот «Коала» (in-bin).
- **[644698|c0mrade|05.06]** CABINET — всё тоже.
- **[651077|isq|07.06]** Диагностика падения диска:
  ```
  df -i
  free -h
  dmesg | tail -40 | grep -iE 'error|fail|oom|bus|I/O'
  ```
- **[652307|Илья|07.06]** Статистика по ноде (трафик по годам и инбаундам) — в ремне учитывается только по инбаундам; для статистики использовать Grafana.
- **[652472|—|07.06]** ufw открыть порт ноды:
  ```
  sudo ufw allow 2222/tcp
  sudo ufw reload
  ```

## Роутинг/транспорт/фиксы
- **[644837|Леш Л.|05.06]** Каждые 5–6 минут обрыв (fp firefox, h3 alpn, selfsteal); причина не в fp; похоже на баг балансира (obs: Happ-логи ругаются на ошибку пинга из burst-observatory) [645016].
- **[645056|—|05.06]** CDN в BBR, alpn.
- **[645079|—|05.06]** «Дедик выдаёт 10гбит где вкусные есть» — OVH, senko (онли дедики), spacecore [644756].
- **[645336|Don’t care|05.06]** «Конфиги влессвлесс каскад для бс» — не найдено в чанке.
- **[646080|Илья|06.06]** На iOS шаблон x-ray json балансера «затирает» конфиги одиночных хостов — проблема в hapе.
- **[647695|Pavel K.|06.06]** Перейдите на grpc; xhttp не особо рекомендую, но на запас можно.
- **[647624|YungCayde|06.06]** Греп на 443/не; за Nginx прятать.
- **[647736|—|06.06]** (см. выше гайд hysteria)
- **[651697|pkhat|07.06]** Vless websocket tls с fp randomized — заведётся любая нода.
- **[651628|okala|07.06]** В хаппе можно отключить лимит для xhttp, чтобы не дропало постоянно соединение — в dev settings; настройка в хаппе не воркает → переезд на tcp.
- **[652993|Stanislav T.|07.06]** В dev-ветке хаппа проблем с xhttp нет; сидит 16 часов на XHTTP Reality Auto на iOS.
- **[652389|—|07.06]** Балансир в JSON работает, но роутинг из JSON не подтягивается клиентам; если отключить роутинг в клиенте — балансир сломается.

## Хостеры/опыт (ключевое)
- **[646069|Даня|06.06]** TimeWeb SPB 2 CPU / 2 ГБ / 40 ГБ NVMe — 980 руб/мес (с IP); вторая ру-нода (под мост) для подстраховки Beget.
- **[646263|isq|06.06]** Бегет: учёт канала по всем ВМ в сумме на акке; бан за утилизацию трафика.
- **[647031|—|06.06]** Hostoff (hostoff.net): целый день серверы не работают; ТП ссылается на «через терминал пингуется — всё нормально» [646211].
- **[647413|—|06.06]** ufo.hosting Москву взял на тесты — IP «выебан похлеще хетзнера», на уровне ovh, по SSH не зайти.
- **[647413|undr|06.06]** UFO ворк и vless tcp reality прокинул.
- **[649835|—|07.06]** Рейтинг: https://github.com/evi1argument/bedolaga-vps-rating
- **[650021|—|07.06]**(netcup) — оплата через KYC не пройдёт с VPN (KYC).
- **[648914|isq|07.06]** Хостинг Vyrex.co (Германия, 1 vCPU Ryzen 9 9950X, 1 ГБ RAM, 15 GB NVMe, до 1 Gbps, без моста, AES-NI по запросу, steal 0).
- **[648914|—|07.06]** Вайкор дорогой; ua.
- **[650338|Nikita M.|07.06]** Cloudrux (Spain): awg.
- **[649096|Evil|07.06]** MVPS для Нидерландов/Швеции/Германии.
- **[650203|—|07.06]**Clouvider (ref) — Нидерланды: AMD EPYC 7313 (1 vCPU), 2GB RAM, 50GB NVMe, 5ТБ трафика (считают в обе стороны), 4.05 EUR/мес; канал 10 гбит (в пике ~7.5), до РФ 3–4; стил 0.0–0.7.
- **[651419|—|07.06]** Аеза МСК/СПБ - сканы.
- **[652019|—|07.06]** Опыт с нодхостом (Польша): «лучшая польша из всех, 10 гбит» (Ня абузерша), но **[652990|Хочу руль|07.06]** Польша Nodehost сутки лежит; Германия умирает каждые 30 минут; Финка — норм.
- **[652411|—|07.06]** Упрут:
- **[652404|yng dev Zover|07.06]** Селектел (гбит) - Питер ускраше.
- **[653089|yng dev Zover|07.06]** Nodehost: Швеция — не берите; Германия — не берите; Польша — заебись; Нидерланды — мало тестил.
- **[653096|yng dev Zover|07.06]** У большинства лоукостеров 1–2 локи норм, остальное мусор.
- **[652978|—|07.06]** Осторожно с неткупом: **[652938|Дима╰‿╯|07.06]** шейпят трафик: занимаешь 75 мбит на час → следующий час скорость 30.
- **[653038|Karnetto|07.06]** netcup 6.60: порт 2.5 гбит, лимита на трафик нет, но если больше 2 ТБ за 24ч — режут канал до 200 мбит до следующего суток.
- **[653092|undr|07.06]** 2 ТБ = на вход (там) ; докуп: 2ТБ 1.20$, 4ТБ 2.51$, 8ТБ 5.45$ (hostingturkiye).
- **[653013|undr|07.06]** Эпик 7534P (2 vCPU), 2 ГБ DDR4, 40 ГБ NVMe, 20ТБ (в обе стороны), до 100 мбит срежут — Austria без мостов, 5.22$.
- **[651308|—|07.06]** Epid, IP ящик.

## Хостеры - прочее
- **[645268|—|05.06]** ВДСина: 3 сервера в дауне, остальные работают; ЛК не пускает; «Датацентр 3 полностью находится в процессе переезда с 4 по 7 июня 2026» [650691].
- **[646041|—|06.06]** Vdsina «не работает — дорогая».
- **[646041|Zoomov|07.06]** П2Г: заменить IP бесплатно.
- **[646336|Zoomov|06.06]** Раз.
- **[646336|—|06.06]** Пользователь.

## Платежки
- **[648007|—|07.06]** Платега (Platega): взлом менеджера, аккаунт заморожен, вебхуки не прилетают [649376|Ак Б.|06.06], платежи «ожидает оплаты», зачислений нет; ТП работает 9–21 Мск.
- **[652003|—|07.06]** РоллиPay: «Ролли вполне» (saveks), 3–4 мес без проблем по крупным суммам.
- **[648474|—|07.06]** AuraPay: вывод на карту моментально.
- **[648760|Максим|06.08]** Платёжки с СБП: лава, вата.
- **[652654|—|07.06]** Юкасса: вывод на расчётный счёт (не на карту).
- **[648223|Виктор|06.06]** Юкасса принимает VPNщиков, не видно отказа; high-risk платёжки без KYC ~10% коми [648229|vedma].

## ИИ/боты
- **[648562|darkfox|06.06]** MCP для ремны (форк с cookie-авторизацией для панели от eGames): https://github.com/dzhokhar1/mcp-remnawave
- **[651800|—|07.06]** Ддос-скрипт (вайбкодный, тест): https://github.com/kenshiro-pixel/vps-shield — вайбкодный ддос-щит; в чате спорили [652195/652208].
- **[651786|omae|07.06]** Оставить vps-shield на проде не рекомендуют (Uff: не нужно).

## Прочее
- **[645363|Анархия|05.06]** Ловится «VPN - на Я.Клауде» - списание яндекс клауд на карты.
- **[644698|—|05.06]** Бедолага-кабина.
- **[651691|—|07.06]** Прикольно из чата.
- **[651816|wrongdeath|07.06]** fail2ban + динамический IP клиента — в white list не получится.

(флуд: срачи со «спуфи», ддрары, продажа акков/гайдов/криптокарт, скам-истории, дроп-темы — опущено)
