# Заметки из chunk_018 (id 96617..103377, 09.12–12.12.2025)

## Юкасса: вебхук 403 и обход блокировки зарубежных IP
- **[id=96999|Серёжа|09.12](https://t.me/c/2941121338/96999)** `POST /yookassa-webhook -> 403 Forbidden` — только автопроверка платежа работает.
- **[id=97013|ム|09.12](https://t.me/c/2941121338/97013)** Юкасса с 1 декабря 2025 заблокировала запросы не с RU-серверов (ответ вебхука).
- **[id=97017..97018|09.12](https://t.me/c/2941121338/97017)** Фиксы: просить поддержку Юкассы занести IP сервера в белый список; либо звонить на горячую линию (через email ответы очень долгие).
- **[id=102457|Genik|11.12](https://t.me/c/2941121338/102457)** ГАЙД: обход блокировки Юкассы через Shadowsocks + Privoxy (перехват только api.yookassa.ru, остальное напрямую). Дословно:
```yaml
services:
  bot:
    image: your-bot-image
    environment:
      HTTP_PROXY: http://privoxy:8118
      HTTPS_PROXY: http://privoxy:8118
    networks:
      - remnawave-network
  ss_tunnel:
    image: shadowsocks/shadowsocks-libev:latest
    container_name: ss_tunnel
    restart: unless-stopped
    command: >
      ss-local
      -s SS_SERVER_IP
      -p SS_SERVER_PORT
      -k "SS_PASSWORD"
      -m aes-256-gcm
      -l 1081
    networks:
      - remnawave-network
  privoxy:
    image: caligari/privoxy:latest
    container_name: privoxy
    restart: unless-stopped
    volumes:
      - ./privoxy.conf:/etc/privoxy/config:ro
    networks:
      - remnawave-network
networks:
  bot_network:
    driver: bridge
  remnawave-network:
    external: true
```
`privoxy.conf`:
```
listen-address 0.0.0.0:8118
toggle 1
enable-remote-toggle 0
enable-remote-http-toggle 0
allow 172.0.0.0/8
# Только api.yookassa.ru → через Shadowsocks
forward-socks5t /api.yookassa.ru/ ss_tunnel:1081 .
```
Проверка: `docker run --rm -it --network remnawave-network curlimages/curl curl -x http://privoxy_yookassa:8118 -I https://api.yookassa.ru/v3/payments --max-time 20` → HTTP/2 401 = работает. Менять код бота не нужно; достаточно, чтобы запрос создания платежа исходил из РФ.
- **[id=100779|Ivan|11.12](https://t.me/c/2941121338/100779)** Юкасса с 29 декабря отключает автоотправку чеков для самозанятых.
- **[id=102315|Inpereon|11.12](https://t.me/c/2941121338/102315)** Письмо от Юкассы о прекращении передачи чеков в налоговую — придется вручную.

## Bedolaga: env vs бот (приоритет env)
- **[id=96682..96684|09.12](https://t.me/c/2941121338/96682)** Всё, что хочешь менять через бота — закомментировать в .env (env имеет приоритет).
- **[id=98621|Пал П.|10.12](https://t.me/c/2941121338/98621)** Скрипт комментирования цен:
```
sed -i 's|^PRICE_30_DAYS=|#PRICE_30_DAYS=|' .env
sed -i 's|^PRICE_90_DAYS=|#PRICE_90_DAYS=|' .env
sed -i 's|^PRICE_180_DAYS=|#PRICE_180_DAYS=|' .env
docker compose restart bot
```
- **[id=98473|c0mrade|10.12](https://t.me/c/2941121338/98473)** PostgreSQL (не SQLite для прода):
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=remnawave_bot
POSTGRES_USER=remnawave_user
POSTGRES_PASSWORD=secure_password_123
```
Клиенты: pgAdmin, DBeaver.
- **[id=100248..100251|10.12](https://t.me/c/2941121338/100248)** `WEBHOOK_SECRET_TOKEN` генерировать: `openssl rand -hex 32`.
- **[id=98652..98707|10.12](https://t.me/c/2941121338/98652)** Уведомления в группу с топиками: `ADMIN_NOTIFICATIONS_CHAT_ID=-1003455753691`, `ADMIN_NOTIFICATIONS_TOPIC_ID=<id_топика>`; ошибка "message thread not found" — неверный ID топика; ID топиков проверять ботом (напр. @GetIDcnBot) или Swiftgram.
- **[id=98559|Oleg|10.12](https://t.me/c/2941121338/98559)** Подключение бота к ремне: `REMNAWAVE_API_URL=https://panel...` — путь до API (панель remnawave 2.3.2, API-токен в настройках). 404 при подключении = не тот URL/токен.
- **[id=98604..98607|10.12](https://t.me/c/2941121338/98604)** Требования CPU/RAM под бот+панель на одной VPS: минимум 2/4, идеально 4/8 (id 102878: «Минимум 2/4, идеально 4/8»).
- **[id=102878|Egor|12.12](https://t.me/c/2941121338/102878)** Требования к VPS для бота+панели: минимум 2/4, идеально 4/8.
- **[id=102529|qwex|12.12](https://t.me/c/2941121338/102529)** HWID лимит не работает после обновления: настройка переехала в панель.
- **[id=102564|Egor|12.12](https://t.me/c/2941121338/102564)** Бекап БД в боте: восстановление — «очистить и восстановить» на новом боте, потом рестарт бота (миграции догрузятся).

## Bedolaga v2.9.1 (11.12.2025) — релиз
- **[id=103051|Egor|12.12](https://t.me/c/2941121338/103051)** Черный список (загрузка из GitHub по raw URL, автообновление, проверка по telegram_id/username, интеграция во все потоки, админ-панель) — by @Gy9vin. Массовая блокировка (парсинг ID, уведомления, кнопка «🛑 Массовый бан»). Мониторинг трафика (порог ГБ/день, детализация по нодам, уведомления, scheduler). Шифрование happ-ссылок: `encrypt_happ_crypto_link` через API Remnawave, автообогащение `happ_crypto_link`. Фильтр «Готовы к продлению» (подписка истекла + баланс ≥ порог).
```env
BLACKLIST_CHECK_ENABLED=false
BLACKLIST_GITHUB_URL=https://raw.githubusercontent.com/.../blacklist.txt
BLACKLIST_UPDATE_INTERVAL_HOURS=1
BLACKLIST_IGNORE_ADMINS=true
TRAFFIC_MONITORING_ENABLED=false
TRAFFIC_THRESHOLD_GB_PER_DAY=50
TRAFFIC_MONITORING_INTERVAL_HOURS=6
SUSPICIOUS_NOTIFICATIONS_TOPIC_ID=0
SUBSCRIPTION_RENEWAL_BALANCE_THRESHOLD_KOPEKS=20000
```
- **[id=103366|Egor|12.12](https://t.me/c/2941121338/103366)** У кого не выдало крипто-ссылки юзерам: после апдейта ничего не делать — она подгрузится автоматически при открытии подписки в боте (триггер на check).
- **[id=103054|12.12](https://t.me/c/2941121338/103054)** «Фича»: при покупке нового сервера списывает за весь месяц, даже если осталось пару дней.
- **[id=100281|17|10.12](https://t.me/c/2941121338/100281)** Триал: два сквада в триал нельзя — выдает рандомно (создать отдельный сквад под триал и не включать для продажи).

## Конфиги Xray
- **[id=99195|valera.|10.12](https://t.me/c/2941121338/99195)** VLESS xhttp+reality инбаунд (дословно):
```json
{
  "tag": "VLESS_XHTTP_REALITY1",
  "port": 5446,
  "listen": "0.0.0.0",
  "protocol": "vless",
  "settings": {"clients": [], "decryption": "none"},
  "sniffing": {"enabled": true, "routeOnly": true, "destOverride": ["http","tls","quic"]},
  "streamSettings": {
    "network": "xhttp",
    "security": "reality",
    "realitySettings": {
      "dest": "vk.com:443",
      "show": false,
      "xver": 0,
      "shortIds": [""],
      "privateKey": "",
      "serverNames": ["vk.com"]
    }
  }
}
```
Outbounds: DIRECT (freedom), BLOCK (blackhole), TORRENT (blackhole). Routing: BLOCK на geoip:private, geosite:private; bittorrent → TORRENT.
- Ссылки от Vladimir Karin (id 99196): https://github.com/XTLS/Xray-examples/ , https://github.com/legiz-ru/my-remnawave (remnawave xhttp inbound tls via nginx / stream separation).
- **[id=101596|Ваня|11.12](https://t.me/c/2941121338/101596)** VLESS-TLS-WS инбаунд на 443 (path /ray, tlsSettings с ключами) — «не пингуется»: проверить tlsSettings (путь серта).
- **[id=102124|EE|11.12](https://t.me/c/2941121338/102124)** Фикс некорректного гео (NL показывает Украину): отключение IPv6:
```
nano /etc/sysctl.d/99-disable-ipv6.conf
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
sudo sysctl --system
```

## Bedolaga: сеть Docker (бот на сервере с панелью)
- **[id=101833..101846|c0mrade|11.12](https://t.me/c/2941121338/101833)** bot_network vs remnawave-network:
```
remnawave-network:
    name: remnawave-network
    external: true  # Используем существующую сеть панели
```
external прописывать в docker-compose бота (внизу и в каждом сервисе). В .env бота: `REMNAWAVE_API_URL=http://remnawave:3000` (внутри Docker-сети) — если панель и бот в докере.
- **[id=98367|sc4rbby|10.12](https://t.me/c/2941121338/98367)** Компози для страницы подписки (отдельный сервис):
```yaml
services:
    remnawave-subscription-page:
        image: remnawave/subscription-page:latest
        container_name: remnawave-subscription-page
        hostname: remnawave-subscription-page
        restart: always
        env_file:
            - .env
        ports:
            - '127.0.0.1:3010:3010'
        networks:
            - remnawave-network
networks:
    remnawave-network:
        driver: bridge
        external: true
```
- **[id=98412|10.12](https://t.me/c/2941121338/98412)** Пример nginx-конфига для бота: https://github.com/BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot#8-пример-nginx-конфига
- **[id=101409|stormie|11.12](https://t.me/c/2941121338/101409)** Конфиг nginx не туда: "events" directive is not allowed here — events/http в конфиге, который include'ится. Основной nginx:
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;
events { worker_connections 1024; }
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    upstream remnawave_bot { server 127.0.0.1:8080; }
    include /etc/nginx/conf.d/*.conf;
}
```
Отдельные server-блоки — в conf.d/.
- **[id=101662..101653|11.12](https://t.me/c/2941121338/101662)** После правки nginx: `docker container restart remnawave-nginx` (перезапуск контейнера nginx).
- **[id=102899|12.12](https://t.me/c/2941121338/102899)** Если прокси на том же сервере: замените `remnawave_bot:8080` на `localhost:8080`.
- **[id=102916|12.12](https://t.me/c/2941121338/102916)** «network with name remnawave-network already exists» — сеть уже есть, external: true.

## Обратка (webhook) Bedolaga
- **[id=102421..102454|11.12](https://t.me/c/2941121338/102421)** Бот отправляет служебные, но не реагирует на /start: служебное по API, старт — через хук. Прозвонить хук через Postman (502 = прокси не настроен). Если GET работает, а POST нет — проверять обратку. `docker network ls` — убедиться, что бот в одной сети с прокси.
- **[id=102424|11.12](https://t.me/c/2941121338/102424)** Бот молчит при webhook: проверить правильность обратки; сессии/логи бота в /opt/remnawave-bot/.
- **[id=102613|Daniil|11.12](https://t.me/c/2941121338/102613)** Обратка через чат: `docker network ls` и проверить сеть.
- **[id=102448|11.12](https://t.me/c/2941121338/102448)** Если обратка настроена, а сети разные — докера не достучатся.
- **[id=97693|17|09.12](https://t.me/c/2941121338/97693)** Первая кнопка в боте думает 5 сек, потом быстро — проблема с коннектом между сервами (пинг/отклик панели).
- **[id=97634|Egor|09.12](https://t.me/c/2941121338/97634)** «Отклик с кнопок ремны должен быть ~0.1 сек». Если 5-7 сек — чекать коннект между серверами.
- **[id=97651|С|09.12](https://t.me/c/2941121338/97651)** Совет: связать серверы teilscale/netbird (приватная сеть) для уменьшения влияния DNS.

## Установка Bedolaga + панель (по инструкции)
- **[id=97924|Евген|09.12](https://t.me/c/2941121338/97924)** Порядок: панель → wildcard-сертификат → сервер под ноду → remnanode на ноду → домен (panel.домен, huy.домен для ноды).
- **[id=101800..101823|11.12](https://t.me/c/2941121338/101800)** docker-compose.yml бота (стил от DigneZzZ):
```yaml
services:
  postgres:
    image: postgres:15-alpine
    container_name: remnawave_bot_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-remnawave_bot}
      POSTGRES_USER: ${POSTGRES_USER:-remnawave_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secure_password_123}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"
    volumes: [postgres_data:/var/lib/postgresql/data]
    networks: [bot_network]
  redis:
    image: redis:7-alpine
    container_name: remnawave_bot_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes: [redis_data:/data]
    networks: [bot_network]
  bot:
    build: .
    container_name: remnawave_bot
    restart: unless-stopped
    depends_on: {postgres: {condition: service_healthy}, redis: {condition: service_healthy}}
    env_file: [.env]
    environment:
      DOCKER_ENV: "true"
      DATABASE_MODE: "auto"
      POSTGRES_HOST: "postgres"
      POSTGRES_PORT: "5432"
      REDIS_URL: "redis://redis:6379/0"
      TZ: "Europe/Moscow"
    volumes:
      - ./logs:/app/logs:rw
      - ./data:/app/data:rw
      - ./locales:/app/locales:rw
      - ./vpn_logo.png:/app/vpn_logo.png:ro
    ports:
      - "${WEB_API_PORT:-8080}:8080"
    networks: [bot_network]
networks:
  bot_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```
- **[id=101846|11.12](https://t.me/c/2941121338/101846)** В docker-compose бота — external network (внизу + в каждом сервисе) для связи с панелью.
- **[id=102594|12.12](https://t.me/c/2941121338/102594)** Ошибка ValidationError: `ADMIN_REPORTS_TOPIC_ID` — поле должно быть числом, а в .env.example комментарий («# ID топика для отчетов»). Не копировать целиком `.env.example`, создавать свой.
- **[id=101849|12.12](https://t.me/c/2941121338/101849)** Ошибка 401 Unauthorized на /health — это нормально (нет токена).

## Bedolaga: скрипты и репозитории
- **[id=97750|c0mrade|09.12](https://t.me/c/2941121338/97750)** Автоустановщики ремны:
  - https://github.com/DigneZzZ/remnawave-scripts
  - https://github.com/Capybara-z/RemnaSetup
  - https://github.com/xxphantom/remnawave-installer
  - eGamesAPI/remnawave-reverse-proxy (устанавливает всё, 3 мин с нодой)
- **[id=97817|09.12](https://t.me/c/2941121338/97817)** Прайс на установку от команды Бедолаги (Egor):
  - Установка бота: базовая 3500₽, полная «под ключ» 6500₽ (2-3 платежки, webhook+reverse proxy, SSL, MiniApp, брендирование), Premium 10000₽
  - Remnawave панель: базовая 4000₽ (панель+1 нода), полная 8000₽ (до 5 нод, рутинги, сабка), пакет «под ключ» 16000₽
  - Миграция от 3000₽, восстановление от 2000₽, консультации 3500₽/час
  - Разработка мобильного VPN-приложения (XRay) с гарантией модерации Google Play/App Store — от 200 000 ₽
  - Кейсы: 20+ проектов спасены с 3x-ui, 15+ с Marzban, максимум 800 000 юзеров миграция, средняя миграция 4-5 ч, 5 приложений в сторах.

## Конвертация и тарифы
- **[id=97200|09.12](https://t.me/c/2941121338/97200)** 200р = 2 месяца (пробник 7 дней).
- **[id=97209|09.12](https://t.me/c/2941121338/97209)** Без БС 100-150₽/мес, с БС 250-350₽/мес.
- **[id=97239|09.12](https://t.me/c/2941121338/97239)** В среднем по рынку 150-200р.
- **[id=97331|Товарищ|09.12](https://t.me/c/2941121338/97331)** Сенко NL тариф: 2.65€/мес, 1 vCPU AMD EPYC 9004, 1 GiB DDR5 ECC, 15 GB NVMe, 250 Mbps (shared, Fair Use). Опла: СБП/карты/крипта.
- **[id=98013|Genik|09.12](https://t.me/c/2941121338/98013)** hip.hosting рефералка: https://hip.hosting/?code=37d25ad0b3b05ca581f0 . Пишет 100 Мбит/с, фактическая скорость выше (Германия/Швеция — более 100%).
- **[id=96908..96949|09.12](https://t.me/c/2941121338/96908)** dhost.nl / 1cent / vdpsina — хосты для нод.

## Хостинги
- **Билл (Bill.ru?)**: у Ильи тестовый сервер недоступен (09.12, id 96668). «Задал вопрос по памяти — не могут расширить» → съехал с Билл (id 100671..100689).
- **hostkey.com / hostkey.ru**: хорошие сервера, поддержка, SSH ок (id 96669, 102478 KRUZ: «Hostkey.ru хороший хостинг»).
- **dhost**: отвалы начались (11.12, id 101261) — «РКН что-то мутит, смена ip не помогла».
- **hip.hosting**: финка 200 Мбит/с как и заявлено (id 101875, 102263). Германия и Швеция норм, США/Финляндия/Латвия херня, РФ упала (id 102313).
- **senko**: Нидерланды 2.65€, NL-EP-0 250 Мбит. Хвалят.
- **play2go**: стабильно хуёво (id 100542). 100 Мбит → 2000 ГБ на локацию, дальше 100 Мбит/с.
- **1cent**: отвалы (id 96909).
- **Ishosting** — «испортились» (id 98400), **edisglobal** — подороже.
- **infomaniak** (Швейцария) — верификация легко.
- **serva.one** — кто-то есть (id 102347).
- **globalcloudnetwork.ru** — использовали/пытались (id 101183, 101147).
- **cloudcore.ru / cloudcore.plus** — новый хостинг, .plus ИП, .ru ООО (id 96684..96697). Переименован из rocketcloud (id 97367).
- **4vps.su** (id 100557) — рефералка.
- **hostoff.link/invite/NEWYEAR** — почасовая оплата, Нидерланды (id 101167).
- **Beget** — не годится для нод, 200 Мбит на выход.
- **4vps** (Япония) — «сразу минус» (id 98396).
- **hostvds** — Латвия 10 Гбит (id 90243).
- **Waicore** — нет серверов.
- **hip.hosting** — проблемы с IP-регионами (УКР гео) (id 101354, 97134).

## Инциденты/фиксы
- **[id=96007|09.12](https://t.me/c/2941121338/96007)** Remnawave: после обновления GET /api/users/{uuid} нет happ.cryptoLink; теперь новый эндпоинт `POST /api/system/tools/happ/encrypt` → `{"response": {"encryptedLink": "string"}}` (id 100240). Обновление включено в общий релиз.
- **[id=98496| stormie|09.12](https://t.me/c/2941121338/98496)** Ошибка `Ошибки при поднятии контейнера` — игнорировать, "warnings".
- **[id=98200..98205|09.12](https://t.me/c/2941121338/98200)** 3x-ui → Remnawave: гайд https://github.com/evoll/xui2remnawave-migrate ; напрямую не переехать, нужно поднимать ремну/ноды на новых серверах, скрипт миграции через нейронку.
- **[id=98403|Egor|10.12](https://t.me/c/2941121338/98403)** Прокси обратное: меняешь патч → меняешь конфиг вебсервера.
- **[id=98579|10.12](https://t.me/c/2941121338/98579)** Если не меняется ничего: в панель, копируешь uuid сквада, в .env бота → `make reload` (bot 2.9.0, панель 2.3.1).
- **[id=98603..98605|10.12](https://t.me/c/2941121338/98603)** ВК лауд пул адресов уже исчерпан (vk cloud белый адрес кончился, id 98601).
- **[id=102450|11.12](https://t.me/c/2941121338/102450)** Бот не отвечает на /start — прозвонить хук через Postman, 502 = прокси криво.

## Прочее
- **[id=97353|Илья|09.12](https://t.me/c/2941121338/97353)** Теле2/Мегафон: VPN не работает на мобильном интернете, работает на Wi-Fi. Причины: лочат reality, lочат tls, lочат reality+tls, lочат reality+443, или подсети хостера в бане у оператора.
- **[id=97395..97400|09.12](https://t.me/c/2941121338/97395)** Google-гос сервисы определяют RU (укр гео) — актуально для поиска под это.
- **[id=97293|Haxonate|09.12](https://t.me/c/2941121338/97293)** ipregion скрипт для гео:
```
bash <(wget -qO- https://github.com/Davoyan/ipregion/raw/main/ipregion.sh)
```
- **[id=97443|Pavel|09.12](https://t.me/c/2941121338/97443)** Уведомления не приходят: бот должен быть админом, бот сам темы не создаёт; 3 топика: General-1, Reports-2, Тикеты-3, Backup-4.
- **[id=97605|Egoist|09.12](https://t.me/c/2941121338/97605)** Ошибка `Бот не имеет прав для отправки в чат -1003307738688` — чат ID не совпадает, бот не админ.
- **[id=102771|12.12](https://t.me/c/2941121338/102771)** Скрипт Билла — облако 51.250 (Яндекс), IP-статика и фаервол по умолчанию открыты (id 100846).
- **[id=100917|Миша|11.12](https://t.me/c/2941121338/100917)** Remnawave subscription-page: ошибка `[AxiosService]` — кривой env.
- **[id=101593|EE|11.12](https://t.me/c/2941121338/101593)** Также проверка «это переменные окружения» — если не применяется, поменяй в .env.
- **[id=102868|Васян|12.12](https://t.me/c/2941121338/102868)** Хостить панель и бота на RU VPS — платежки работают, плюсы.
- **[id=102877|12.12](https://t.me/c/2941121338/102877)** Требования под бот+панель: минимум 2/4, идеально 4/8.
- **[id=102878|Egor|12.12](https://t.me/c/2941121338/102878)** (уже выше)

## Цены и продажи
- **[id=100193|10.12](https://t.me/c/2941121338/100193)** Домены: reg.ru дорого продление (~6к/год за .com?), в ботах дешевле.
- **[id=100225|10.12](https://t.me/c/2941121338/100225)** Yandex Cloud 1.6 ₽/гиг трафика.
- **[id=100222|10.12](https://t.me/c/2941121338/100222)** «2500 нода и 100 гигоф фри, дальше за гиги плата» (VK Cloud).
- **[id=100219|10.12](https://t.me/c/2941121338/100219)** Обход БС стоит «минимум 2к в месяц».
