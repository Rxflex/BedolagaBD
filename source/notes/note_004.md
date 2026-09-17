# Заметки из chunk_004 (id 14616..19808, 24.09–01.10.2025)

## Bedolaga релизы (Egor/@fringg)
- **[id=15132|Egor|24.09.2025](https://t.me/c/2941121338/15132)** #v2_3_9: система поддержки/модерации (SLA-таймеры тикетов, аудит действий, роли модераторов, пагинация тикетов); платежки PayPalych (Pal24, СБП+карты) и Mulen Pay (СБП); промогруппы с видимостью серверов, автовыдачей по порогу пополнений, JSON-карта скидок; умное пополнение (автопредложение суммы); напоминания (триалам через 1ч/24ч без трафика, подписчикам через 1–3 дня после истечения с нарастающими скидками); режим external_link_miniapp для мониторинга.
- **[id=16115|Egor|25.09.2025](https://t.me/c/2941121338/16115)** #v2_4_0: все настройки в БД (таблица bot_config), в ENV для запуска только BOT_TOKEN= и ADMIN_IDS=; режим happ_cryptolink (HTTPS-редирект для happ:// ссылок); умные триалы (мгновенное отключение при отписке от канала, восстановление кнопкой «Я подписался», платные подписки защищены); скидки промогрупп на докупку (флаг addon_discounts_enabled); миграция ENV→БД автоматически при запуске.
- **[id=18904|Egor|30.09.2025](https://t.me/c/2941121338/18904)** #v2_4_1: полноценное Web API (REST, токены, управление подписками/промокодами/рассылками, интеграция с Remnawave); Swagger (/docs, /redoc); полная мультиязычность (выбор языка при первом запуске, RU/EN); сохранение дней триала при покупке платной; автосброс трафика при продлении; перед обновлением бэкап БД.
  - Дока API: https://github.com/Fr1ngg/remnawave-bedolaga-telegram-bot/blob/main/docs/web-admin-integration.md [18909]
- **[id=19736|Egor|01.10.2025](https://t.me/c/2941121338/19736)** #v2_4_2: Telegram Mini App (просмотр подписки, брендинг через env); PayPalych — раздельные кнопки СБП/карта; уведомление для триала при отписке от канала; админ-панель: 6 новых сортировок (Gy9vin), раздел логов бота, модераторы и SLA (Pedzeo); 250+ ключей локализации; app-config.json актуализация (SantaSpeen) — macOS, Android TV, Apple TV.
  - env для Mini App: MINIAPP_SERVICE_NAME_EN/RU, MINIAPP_SERVICE_DESCRIPTION_EN/RU, MINIAPP_PURCHASE_URL.
  - Для миграции веб-API нужен в env WEB_API_DEFAULT_TOKEN=токен_какой_нибудь [19740-19742].
- **[id=16511|Edward Forix|26.09.2025](https://t.me/c/2941121338/16511)** Docker-тег 2.3.9 недоступен: manifest for fr1ngg/remnawave-bedolaga-telegram-bot:2.3.9 not found. Откат невозможен; Egor советует залить бэкап в 2.4.0 [16514].
- Стандартное обновление: `docker compose down && docker compose pull && docker compose up -d && docker compose logs -f` [18904, 19802].

## Настройки в БД vs ENV (v2.4.0+)
- **[id=15951|Egor|25.09.2025](https://t.me/c/2941121338/15951)** В БД живут все настройки кроме BOT_TOKEN и ADMIN_IDS; для первичного запуска нужны поля Remnawave + триал-сквад (потом убрали). При конфликте приоритет у значений из БД [15952]. ENV можно не трогать/оставить как есть [16492-16494]; удалять env нельзя, пока не отредактированы дефолты — затрутся [15935-15937].
- Менять настройки можно из админки бота без перезапуска [15924, 15944].
- BURJUY критикует: платежку в env настроил один раз и менять на лету не надо [16522-16523]; Egor: вебадминка планируется платной (~1000р/мес), бот и лайт-версия админки бесплатные [18799-18800, 18547].

## Ошибки и фиксы Bedolaga
- **[id=16262|叶丹尼|26.09.2025](https://t.me/c/2941121338/16262)** Обновление до 2.4.0: не прошли миграции БД (issue 481). Ручной фикс от Ильи [16273-16283]:
  ```sql
  docker exec -it remnawave_bot_db psql -U remnawave_user -d remnawave_bot
  ALTER TABLE users ADD COLUMN IF NOT EXISTS auto_promo_group_assigned BOOLEAN DEFAULT false;
  ALTER TABLE users ADD COLUMN IF NOT EXISTS auto_promo_group_threshold_kopeks INTEGER DEFAULT 0;
  UPDATE users SET auto_promo_group_assigned = false WHERE auto_promo_group_assigned IS NULL;
  UPDATE users SET auto_promo_group_threshold_kopeks = 0 WHERE auto_promo_group_threshold_kopeks IS NULL;
  ALTER TABLE promo_groups ADD COLUMN IF NOT EXISTS apply_discounts_to_addons BOOLEAN DEFAULT false;
  UPDATE promo_groups SET apply_discounts_to_addons = false WHERE apply_discounts_to_addons IS NULL;
  ALTER TABLE promo_groups ALTER COLUMN apply_discounts_to_addons SET NOT NULL;
  DELETE FROM promo_groups WHERE name = 'Базовый юзер' AND apply_discounts_to_addons IS NULL;
  INSERT INTO promo_groups (name, server_discount_percent, traffic_discount_percent, device_discount_percent, apply_discounts_to_addons, is_default)
  SELECT 'Базовый юзер', 0, 0, 0, false, true WHERE NOT EXISTS (SELECT 1 FROM promo_groups WHERE is_default = true);
  ```
  Плюс недостающее: `ALTER TABLE users ADD COLUMN promo_group_id BIGINT;` [16283]. Если в логах ошибки промогрупп / ProgrammingError — прогонять эти скрипты [16619-16620]. Помогло и с 2.3.2 [16720].
- **[id=16328|Николай Ditrix|26.09.2025](https://t.me/c/2941121338/16328)** pydantic ValidationError: MULENPAY_SHOP_ID «Input should be a valid integer» — в env остались плейсхолдеры. Фикс: закомментировать в .env неиспользуемые платежные переменные (MULENPAY_SHOP_ID, ADMIN_REPORTS_TOPIC_ID='# ID топика для отчетов' и т.п.), затем `docker compose down/up` [16425-16441, 16832, 16839-16841]. Egor обещал починить [16330].
- **[id=16413|Евгений|26.09.2025](https://t.me/c/2941121338/16413)** Купил 2 устройства, а подключает 3 — HWID не включен в панели Remna. Включи HWID на панели — контроль заработает [16414-16415].
- **[id=15325|—|25.09.2025](https://t.me/c/2941121338/15325)** Бот подвязан на hwid контроль; дорабатывают работу без него [15326]. При сбросе HWID удаляется только список устройств, старые ключи продолжают работать — предложение ревокать подписку при полном сбросе вынесено [17570-17575].
- **[id=19626|Edward Forix|30.09.2025](https://t.me/c/2941121338/19626)** WARNING Failed to copy default locale ... Permission denied: sudo chown -R 1000:1000 ./locales && chmod -R u+rwX,go-rwx ./locales [19629].
- **[id=16810|—|26.09.2025](https://t.me/c/2941121338/16810)** Redis в контейнере бота: WARNING Memory overcommit must be enabled — фикс: `sysctl vm.overcommit_memory=1` (в /etc/sysctl.conf), затем рестарт [16813].
- **[id=16933|—|26.09.2025](https://t.me/c/2941121338/16933)** Бот «ломается» на юзерах с символами < > в нике (Telegram HTML-парсинг). Лечится экранированием/санитайзингом; в 2.4.1 пофикшено — «бот больше не вызывает проблем у пользователей с символами <>» [19021].
- **[id=16144|Дмитрий|25.09.2025](https://t.me/c/2941121338/16144)** Ошибка «can't parse entities: Unsupported start tag "html"» в разделе обновлений (получение информации о версиях) — репорт ошибка парсинга changelog.
- **[id=17892|Deleted Account|28.09.2025](https://t.me/c/2941121338/17892)** После правки текста главной страницы бот перестал отвечать: TelegramBadRequest «Unexpected end tag» на старте. Фикс — вернуть прежний текст [17958-17960]. Восстановление: запустить чистого бота с нуля, положить файл бэкапа в ту же папку и восстановить [17966-17967].
- **[id=17596|Ко|27.09.2025](https://t.me/c/2941121338/17596)** CryptoBot webhook «Неверная подпись» — включить вебхуки в самом криптоботе, закомментировать подпись в env, рестарт, заново «старт» в боте [17604-17609]. Изменения в env требуют именно down/up, рестарт контейнера не помогает [17610].
- **[id=17724|Haxonate|27.09.2025](https://t.me/c/2941121338/17724)** YooKassa: предупреждение «Подпись не совпала, но продолжаем обработку (режим отладки)» — не баг. Фикс для чистоты: оставить `YOOKASSA_WEBHOOK_SECRET=` пустым [17730-17731]; Egor просил проверить, что webhook secret выключен в настройках [17727].
- **[id=17693|Андрей|27.09.2025](https://t.me/c/2941121338/17693)** YooKassa refund.succeeded игнорируется ботом (нормально).
- **[id=19517|И҉л҉ь҉я҉с҉|30.09.2025](https://t.me/c/2941121338/19517)** Mulen Pay: бот не ловит автоматические уведомления (callback фиксирует как «отсутствует подпись»), деньги приходят только после кнопки «Проверить статус» — Egor допилил, фикс в 2.4.2 [19695-19699].
- **[id=18027|Дмитрий|28.09.2025](https://t.me/c/2941121338/18027)** Время подписки в боте на 3 часа меньше, чем в панели — TZ в docker; в docker-compose бота TZ=UTC, в панели eGames своя. Свести таймзоны к одной и синхронизировать [18032-18036, 18048].
- **[id=17357|Skrimp|26.09.2025](https://t.me/c/2941121338/17357)** «Фантомный» сервер не удаляется из бота после удаления в панели Remna: оставалась запись в БД; в 2.4.1 фиксед — синк серверов теперь принудительно удаляет неактивные сервера/сквады [19027]. Причина дублей: юзер, созданный ботом, был привязан к серверу — удалить юзера, потом сервер [17411].
- **[id=18308|Дмитрий|29.09.2025](https://t.me/c/2941121338/18308)** В отчетах «Всего поступлений» суммирует пополнения И траты (двойной учет: пополнил 700, потратил 575 — показывает 1276). Репорт в issues, пообещали поправить [18984 не было; см. 18076].
- **[id=15366|4 0 4|25.09.2025](https://t.me/c/2941121338/15366)** Ошибка «количество устройств» в рекламной кампании: максимум устройств в env поставить >0 (например 50) — уйдет [15376].
- **[id=17599|Ко|27.09.2025](https://t.me/c/2941121338/17599)** Вблизи сап-домен юкaccы: достаточно key+shop id+webhook; главный момент — добавить ссылку вебхука https://webhook.domain.com/yookassa-webhook и настроить прокси [17520-17531].
- **[id=19507|Дмитрий|30.09.2025](https://t.me/c/2941121338/19507)** После выбора языка остается лого в чате — фикс в start.py [19514].
- **[id=16976|Ко|26.09.2025](https://t.me/c/2941121338/16976)** У Туркмении бот не работает (чужой тестовый юзер).
- **[id=15648|Андрей|25.09.2025](https://t.me/c/2941121338/15648)** Happ роутинг «не работает» при верном DirectSites/ProxySites — у одного клиента в Москве; на другом телефоне ок. Проблема на стороне клиента/региона, не конфига.
- **[id=15616|—|25.09.2025](https://t.me/c/2941121338/15616)** На Android в Happ не качаются гео-файлы (это не работает после обновления Happ; старый APK работал) [15644-15645].
- **[id=17858|Иван Болгов|26.09.2025](https://t.me/c/2941121338/17858)** Хост/нода: путаница в терминах Remna — есть хост, нода, сквад и профиль. Панель отвечает за менеджмент, сквады агрегируют хосты/ноды. В боте список серверов = список сквадов панели [15385-15396, 17801-17835].
- **[id=16369|Николай Ditrix|26.09.2025](https://t.me/c/2941121338/16369)** Remna не балансирует сама — балансировка через DNS (или HAProxy/CF/балансировщик) [16371-16374]. Все поддомены нод нужно указать в serverNames профиля [16374]. Ссылка на доку профилей/сквадов: https://remna.st/blog/misc/new-profiles-and-squads/explaining-new-profile-and-squads-system [16376].
- **[id=18102|—|28.09.2025](https://t.me/c/2941121338/18102)** eGames почему-то работает без открытия IP (наблюдение).
- **[id=17679|PEpeSan|27.09.2025](https://t.me/c/2941121338/17679)** Cron-проверка nginx: важный момент — вебхук-поддомен и health.
- **[id=18381|Egor|29.09.2025](https://t.me/c/2941121338/18381)** Промокод BEDOLAGA на 30% первый месяц для @dhostVPS_bot (коллаба, сам пользуется 3 месяца, NL 10 гбит).
- **[id=16176|Дмитрий|26.09.2025](https://t.me/c/2941121338/16176)** Гайд по балансировке в mihomo + скрытие серверов одной локации: https://t.me/c/2409638119/239695 (детали в следующем пункте).

## Конфиги
### Caddy: вебхуки бота (R0xTaDDy) [id=16788](https://t.me/c/2941121338/16788)
```
https://webhook.domain.com {
        handle /tribute-webhook* {
                reverse_proxy http://remnawave_bot:8081
        }
        handle /cryptobot-webhook* {
                reverse_proxy http://remnawave_bot:8081
        }
        handle /health {
                reverse_proxy http://remnawave_bot:8081
        }
}
```
Важно: localhost в reverse_proxy заменять на имя docker-контейнера бота и держать Caddy и контейнеры бота в одной docker-сети [16791].
Ошибочный вариант Ко с `localhost:8081` не работает [16786-16790]. Полный перечень портов: Tribute/CryptoBot/MulenPay/health = 8081, YooKassa = 8082, Pal24 = 8084 [17866].
### Nginx: вебхуки (Gy9vin) [id=17866](https://t.me/c/2941121338/17866) (сокращенно, все блоки с proxy_set_header Host $host; X-Real-IP; X-Forwarded-For; X-Forwarded-Proto)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    location /tribute-webhook  { proxy_pass http://127.0.0.1:8081; }
    location /cryptobot-webhook { proxy_pass http://127.0.0.1:8081; }
    location /mulenpay-webhook { proxy_pass http://127.0.0.1:8081; }
    location /pal24-webhook    { proxy_pass http://127.0.0.1:8084; }
    location /yookassa-webhook { proxy_pass http://127.0.0.1:8082; }
    location /health           { proxy_pass http://127.0.0.1:8081/health; }
}
```
Проверка Pal24 из чанка (Gy9vin): сгенерировать test POST и ждать `{"status":"ok"}`; signature = md5(OutSum:InvId:token) upper-case. [17866]
### YooKassa: настройка (Gy9vin) [id=17846](https://t.me/c/2941121338/17846)
- env: YOOKASSA_ENABLED=true, YOOKASSA_SHOP_ID=<shop_id>, YOOKASSA_SECRET_KEY=<secret_key>, YOOKASSA_RETURN_URL=https://t.me/<имя_бота>, YOOKASSA_DEFAULT_RECEIPT_EMAIL=<email>;
- опционально YOOKASSA_SBP_ENABLED, YOOKASSA_VAT_CODE, YOOKASSA_PAYMENT_MODE, YOOKASSA_PAYMENT_SUBJECT;
- в кабинете YooKassa HTTP-уведомление → https://<домен>/yookassa-webhook; порты/путь бота: YOOKASSA_WEBHOOK_PORT, YOOKASSA_WEBHOOK_PATH; при YOOKASSA_WEBHOOK_SECRET включается HMAC.
- Возврат: RETURN_URL — это просто ссылка на бота после оплаты, не внутренний юрл Юкассы [17813-17829].
- Мин/макс суммы: YOOKASSA_MIN_AMOUNT_KOPEKS / YOOKASSA_MAX_AMOUNT_KOPEKS.
- Андрею помогло: `YOOKASSA_RETURN_URL=https://domain/yookassa-webhook` (без лишнего поддомена) [17686].
### Caddy с DNS-challenge Cloudflare (Danila Tsaplin) [id=17404](https://t.me/c/2941121338/17404) — полностью
```dockerfile
# Создаем Dockerfile в папке Caddy
FROM caddy:2.9.1-builder AS builder
RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```
```bash
docker build -t caddy-cf .
```
```caddy
{
    email {$EMAIL}
    acme_dns cloudflare {$CF_API_TOKEN}
    https_port {$SELF_STEAL_PORT}
    default_bind 127.0.0.1
    servers {
        listener_wrappers {
            proxy_protocol {
                allow 127.0.0.1/32
            }
            tls
        }
    }
    auto_https disable_redirects
    log {
        output file /var/log/caddy/access.log {
            roll_size 10MB
            roll_keep 5
            roll_keep_for 720h
            roll_compression gzip
        }
        level ERROR
        format json
    }
}
http://{$SELF_STEAL_DOMAIN} {
    bind 0.0.0.0
    redir https://{$SELF_STEAL_DOMAIN}{uri} permanent
    log {
        output file /var/log/caddy/redirect.log {
            roll_size 5MB
            roll_keep 3
            roll_keep_for 168h
        }
    }
}
https://{$SELF_STEAL_DOMAIN} {
    root * /var/www/html
    try_files {path} /index.html
    file_server
    log {
        output file /var/log/caddy/access.log {
            roll_size 10MB
            roll_keep 5
            roll_keep_for 720h
            roll_compression gzip
        }
        level ERROR
    }
}
:{$SELF_STEAL_PORT} {
    tls internal
    respond 204
    log off
}
:80 {
    bind 0.0.0.0
    respond 204
    log off
}
```
.env:
```
SELF_STEAL_DOMAIN=your.domain.sample
SELF_STEAL_PORT=9443
CF_API_TOKEN=API KEY CLOUDFLARE FOR YOURS DNS ZONE
EMAIL=YOURS@EMAIL.Sample
```
docker-compose: image caddy-cf, контейнер caddy-selfsteal, volumes Caddyfile + /opt/caddy/html + logs + caddy_data/caddy_config, env_file .env, network_mode host. Смысл: не перетасовывать сертификаты, всё обновляется само (DNS challenge).

### Редирект-страница для импорта подписки (Максимка) [id=17888](https://t.me/c/2941121338/17888)
```caddy
sub.some.site {
    reverse_proxy * http://127.0.0.1:3010
    @redir query u=*
    redir @redir {query.u} 302
}
```
Пример кода кнопки импорта подписки с encodeURIComponent:
```python
target = f"{app.get('urlScheme', '')}{subscription_url}"
sso_url = f"https://sub.some.site/?u={quote(target, safe='')}"
```
Скрытие криптолинка Happ в expandable blockquote:
```python
if settings.is_happ_cryptolink_mode():
    redirect_link = get_happ_cryptolink_redirect_link(subscription_link)
    happ_message = textwrap.dedent(f"""\
    🔗 <b>Подключение через Happ</b>
    💡 Если ссылка не открывается автоматически, скопируйте её вручную:
    <blockquote expandable><code>{subscription_link}</code></blockquote>""")
```
### Цены/тарифы в .env (PEpeSan) [id=17630](https://t.me/c/2941121338/17630)
```env
BASE_SUBSCRIPTION_PRICE=0
PRICE_14_DAYS=7000
PRICE_30_DAYS=9900
PRICE_60_DAYS=25900
PRICE_90_DAYS=36900
PRICE_180_DAYS=69900
PRICE_360_DAYS=109900
BASE_PROMO_GROUP_PERIOD_DISCOUNTS_ENABLED=false
BASE_PROMO_GROUP_PERIOD_DISCOUNTS=60:10,90:20,180:40,360:70
TRAFFIC_PACKAGES_CONFIG="5:2000:false,10:3500:false,25:7000:false,50:11000:true,100:15000:true,250:17000:false,500:19000:false,1000:19500:true,0:20000:true"
PRICE_PER_DEVICE=5000
AVAILABLE_SUBSCRIPTION_PERIODS=30,90,180
AVAILABLE_RENEWAL_PERIODS=30,90,180
```
Чтобы не было выбора допов: один сервер (не позволять выбирать), режим fixed для трафика, дефолт устройств = максимум [15311].
### Xray Reality нода (Илья/Дмитрий) [id=18305, 18311](https://t.me/c/2941121338/18305)
Конфиг с dest /dev/shm/nginx.sock (xver 1), либо target 127.0.0.1:9443 для selfsteal:
```json
{
  "log": {"loglevel": "warning"},
  "dns": {"servers": [{"address": "https://dns.google/dns-query", "skipFallback": false}], "queryStrategy": "ForceIPv4"},
  "inbounds": [{
    "tag": "ИМЯ_ВАШЕЙ_НОДЫ", "port": 443, "protocol": "vless",
    "settings": {"clients": [], "decryption": "none"},
    "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
    "streamSettings": {
      "network": "tcp", "security": "reality",
      "realitySettings": {
        "dest": "/dev/shm/nginx.sock", "show": false, "xver": 1, "spiderX": "",
        "shortIds": ["СЮДА_ВАШ_SHORT_ID"],
        "privateKey": "СЮДА_ВАШ_ПРИВАТНЫЙ_КЛЮЧ",
        "serverNames": ["ВАШ.ДОМЕН.COM"]
      }
    }
  }],
  "outbounds": [{"tag": "DIRECT","protocol": "freedom"},{"tag": "BLOCK","protocol": "blackhole"}],
  "routing": {"rules": [
    {"ip": ["geoip:private"], "type": "field", "outboundTag": "BLOCK"},
    {"type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK"}
  ]}
}
```
Спор про shortIds: Илья считает, что для каждого юзера он не нужен (UUID уникален, актуально для SS); Дмитрий — что shortId в Client Hello отличает клиента Reality от обычного HTTPS и сокращает handshake [18313-18324].
- **[id=18302|-|29.09.2025](https://t.me/c/2941121338/18302)** У некоторых клиентов отключалось: совет ИИ — network поменяен с raw на tcp/tls, target → dest, стало лучше.
- **[id=15648|Андрей|25.09.2025](https://t.me/c/2941121338/15648)** Happ routing DirectSites/ProxySites (geosite: CATEGORY-GOV-RU, CATEGORY-MEDIA-RU, YOUTUBE, OPENAI, INSTAGRAM; DirectIp: private ranges + geoip:RU; DomainStrategy IPIfNonMatch, FakeDNS false).
### Роутинг Happ через base64-конфиг (maks) [id=16323-16325](https://t.me/c/2941121338/16323)
happ://routing/add/<base64 JSON> с RemoteDNS DoH cloudflare-dns.com, DomesticDNS DoH dns.yandex.ru (77.88.8.8), geoiр/геосайт с github.com/runetfreedom/russia-v2ray-rules-data. Примечание: JSON выключить, тогда работает.
### Happ роутинг (Максимка/Dмитрий) [id=17840-17854](https://t.me/c/2941121338/17840)
Балансировка mihomo: создать группу балансировки из серверов одной локации, скрыть её, прописать группу в selectors — клиент видит 1 сервер вместо 2+. Дебри: https://t.me/c/2409638119/239695 [16176].

## Оплата/платежки — опыт
- **[id=16741|R0xTaDDy|26.09.2025](https://t.me/c/2941121338/16741)** Mulen Pay: комиссия 7% по СБП, карты через 1-2 недели после запуска СБП, выплата в USDT, T+1. Сравнение: Tribute ~10%, YooKassa ~8% со всем (с налогом/чеками), Vata 8%+ [16747-16748, 16758].
- **[id=16689|Pedzeo|26.09.2025](https://t.me/c/2941121338/16689)** Условия эквайринга Mulen (LOWRISK): вход СБП 7%, settlement T+1, лимит до 300.000 руб/транзакция, H2H (при PCI) или их форма, холд 1 сутки, выплаты USDT T+1 с проверкой по AML, вывод 0%, выплаты пн-пт.
- **[id=15783|R0xTaDDy|25.09.2025](https://t.me/c/2941121338/15783)** PayPalych: без нормального оборота не добавят (известен случай отказа хостеру). Mulen: регистрация через менеджера, вывод в крипту — без KYC (только почта и телефон на сайте) [15798-15823]; при создании магазина просит ИНН [16656].
- **[id=16536|Maxim|26.09.2025](https://t.me/c/2941121338/16536)** Tribute заблокировал прием платежей: продавать VPN через донат нельзя — нужно создавать цифровые товары и отправлять клиентов по ссылкам на оплату; 7к заморожены, обещают вернуть [16536-16575]. У Ильи трибьют работает нормально, две выплаты прошли [17483-17485].
- **[id=19061|BURJUY|30.09.2025](https://t.me/c/2941121338/19061)** urlpay.io — API для Mulen (https://urlpay.io/docs/api). Кто не одобрили на Mulen — отправляют на urlpay [19062-19067]. Вывод: urlpay = mulenpay = onlipay (одно и то же, хайриск) [19109]; Egor добавил URLPay как тот же API [19240-19247].
- **[id=16690|Pedzeo|26.09.2025](https://t.me/c/2941121338/16690)** Юзеры просят: правила и политику — телеграф-ссылкой (влезает 1200 символов в админку, больше — ошибка сохранения [16695]). Пример политики: https://telegra.ph/POLITIKA-KONFIDENCIALNOSTI-PO-RABOTE-S-PERSONALNYMI-DANNYMI-POLZOVATELEJ-03-30; оферты: https://telegra.ph/Polzovatelskoe-soglashenie-Publichnaya-oferta-07-15
- **[id=18471|R0xTaDDy|29.09.2025](https://t.me/c/2941121338/18471)** Юмани: переводы на карту 7%, СБП до 3500р/день без комиссии, снятие 15к бесплатно далее 3-5% [18470].
- **[id=15936|Maxim|26.09.2025](https://t.me/c/2941121338/15936)** Трибьют: «у меня макс по деньгам вообще ноль платных не возвращают» (жалоба).
- **[id=15761|—|25.09.2025](https://t.me/c/2941121338/15761)** Свой хостинг-бизнес (белые ВПС, оверселл): оккупация меньше года, но там свои риски.

## ТСПУ / белые списки / обходы
- **[id=15017|свэгги|24.09.2025](https://t.me/c/2941121338/15017)** Билайн и Мегафон внедрили новые белые списки: проверка SNI + ASN, вроде и IP. В Татарстане (Мегафон) — подтверждено [15044]. Единственный рабочий метод там — VK-туннель [15022-15023]; «мобильный интернет оффнули, работает только вк туннель».
- **[id=15038|свэгги|24.09.2025](https://t.me/c/2941121338/15038)** SNI ozon.ru снова работает на Мегафоне — но это грузит ноды Remna (сеть Ильи задыхается, алерты) [15046].
- **[id=14994|Дмитрий|24.09.2025](https://t.me/c/2941121338/14994)** Роутинг РУ→один сервер, НЕ-РУ→другой: средствами Xray нельзя переразрулить на другой сервер; это делается в mihomo (гайд: https://remna.st/docs/guides/templates/mihomo). Белые списки — это не маршрутизация, туннелирование не поможет, если работает только белое [15002-15031].
- **[id=18864|maks|29.09.2025](https://t.me/c/2941121338/18864)** Тормоза на Мегафон/Йота: обход во время отключений (whitelistbypass) https://t.me/whitelistbypass/31 [18871]; Ростовская область — перманентно без мобильного интернета кроме разрешенных сервисов [18363-18364].
- **[id=17245|—|26.09.2025](https://t.me/c/2941121338/17245)** В РФ в половине регионов CDN (CF, Fastly) заблокирован.

## Инструменты, ссылки, репозитории
- **[id=16246|Илья|26.09.2025](https://t.me/c/2941121338/16246)** Смена ядра Xray в Remna: скрипты DigneZzZ https://github.com/DigneZzZ/remnawave-scripts (либо eGames). В Marzban это было проще (ключ в окружениях). Понизить ядро — тоже там [16237-16262]. Илья: смена ядра не решила проблемы с Google-сервисами [16265], понизил до 25.6.8 — стало лучше [16318].
- **[id=17373|BURJUY|26.09.2025](https://t.me/c/2941121338/17373)** Torrenты: настраивать роутинг DIRECT для торрентов + torrent blocker: https://github.com/kutovoys/xray-torrent-blocker [17409]; примеры правил mihomo: https://github.com/legiz-ru/mihomo-rule-sets/tree/main/examples [17408]. У BURJUY в подписке два клиента с правильным конфигом — торренты в директ, юзерам не даёт выбор клиента [17452].
- **[id=17773|Nunya Business|27.09.2025](https://t.me/c/2941121338/17773)** Автоустановка ноды Remna с selfsteal: https://github.com/eGamesAPI/remnawave-reverse-proxy (одна команда, минус — nginx socket в конфиге).
- **[id=17810|R0xTaDDy|27.09.2025](https://t.me/c/2941121338/17810)** Ansible-установка ноды: https://github.com/iphizic/remna-node [17810-17812].
- **[id=15989|Egor|25.09.2025](https://t.me/c/2941121338/15989)** Страница подписки (саб-пейдж) от автора бота: https://github.com/Fr1ngg/remnawave-multistep-xraychecker-subpage-adaptive (подключить файл в докер вместо своей index) [15996-15998].
- **[id=17023|R0xTaDDy|26.09.2025](https://t.me/c/2941121338/17023)** Бот от мачки: https://github.com/machka-pasla/remnawave-tg-shop — ставится и настраивается проще, функционала меньше, работает на вебхуках (запускается даже с ошибками в env) [17105-17113]; разборы на Boosty у Богдана Соловьева (2 видео, через расширение More Boosty для Chrome качается) [17157].
- **[id=19061|BURJUY|30.09.2025](https://t.me/c/2941121338/19061)** URLPay docs: https://urlpay.io/docs/api; Mulen docs: https://mulenpay.ru/docs/api [19069].
- **[id=18910|Egor|30.09.2025](https://t.me/c/2941121338/18910)** Bedolaga на 1-й странице GitHub по лайкам (после 100-го лайка).
- **[id=18552|PEpeSan|29.09.2025](https://t.me/c/2941121338/18552)** easy-vk-tunnel (туннель через VK): https://github.com/nebesniy/easy-vk-tunnel/ — один пользователь спрашивал про inbound для Remna [19804].
- **[id=18006|Egor|28.09.2025](https://t.me/c/2941121338/18006)** @zarub_robot — штука для оплаты, «кто юзал, нормикс?» (обсуждение).
- **[id=16673|Aleksey Vist|26.09.2025](https://t.me/c/2941121338/16673)** whitebird.io — опыт у R0xTaDDy: «норм тема» [16679].
- **[id=17417|свэгги|27.09.2025](https://t.me/c/2941121338/17417)** Замечание о панели Remna: тикеты/саб-страничка.
- **[id=17408|BURJUY|27.09.2025](https://t.me/c/2941121338/17408)** App-config: сток app-config.json прямо из панели.
- **[id=16005|R0xTaDDy|25.09.2025](https://t.me/c/2941121338/16005)** Lovable.dev / Bolt.new — лучший генератор фронта (по опыту R0xTaDDy). Codex Claude — популярный для кода [16166]; Perplexity Pro 250₽/год ключом с plati.market [16029].
- **[id=18105|PEpeSan|28.09.2025](https://t.me/c/2941121338/18105)** Termius — андроид-мониторинг серверов (ssh): https://termius.com [18110-18113].
- **[id=17804|R0xTaDDy|27.09.2025](https://t.me/c/2941121338/17804)** Ответ «для массового управления — Ansible» [17807].
- **[id=18512|R0xTaDDy|29.09.2025](https://t.me/c/2941121338/18512)** Мониторинг нод в веб-морде бота — не задача; ставь beszel и мониторь.
- **[id=18663|Максимка|29.09.2025](https://t.me/c/2941121338/18663)** «Как перейти с nginx на Caddy»: apt remove nginx; apt install caddy (шутка-совет в чате).
- **[id=19061|BURJUY|30.09.2025](https://t.me/c/2941121338/19061)** Сравнение мулена и urlpay: у обоих одинаковые API.

## Remna specifics
- **[id=15385|Bedolaga Cash|25.09.2025](https://t.me/c/2941121338/15385)** Сервера в боте = сквады в панели; UUID не совпадают — это норм, автоопределение стран корявое, менять руками [15388-15396].
- **[id=16376|BURJUY|26.09.2025](https://t.me/c/2941121338/16376)** Дока: https://remna.st/blog/misc/new-profiles-and-squads/explaining-new-profile-and-squads-system
- **[id=16100|R0xTaDDy|25.09.2025](https://t.me/c/2941121338/16100)** Продажа стран по отдельности — идея плохая: юзеры тыкают на верхнюю и грузят локацию; со всеми серверами балансировка лучше [16103]. Хак Egor: рассылка «топ по скорости» меняет баланс [16107].
- **[id=16373|Pedzeo|26.09.2025](https://t.me/c/2941121338/16373)** Панель не балансирует сама — через DNS.
- **[id=16374|Илья|26.09.2025](https://t.me/c/2941121338/16374)** В serverNames профиля указывать все поддомены нод.
- **[id=16474|Иван Болгов|26.09.2025](https://t.me/c/2941121338/16474)** REMNAWAVE_API_URL= можно писать с портом (remna:8000) — для внутренней docker-сети; все типы аутентификации работают [16481-16485].
- **[id=17801|Alex|27.09.2025](https://t.me/c/2941121338/17801)** REMNAWAVE_SECRET_KEY: в панели DigneZzZ/remnawave-scripts — из URL входа, всё после `?` с `=` замененным на `:` [16559]; для eGames — из панели (cookie), у DigneZzZ тоже это работает.

## Хостинги/локации — опыт
- **[id=18760|Илья|29.09.2025](https://t.me/c/2941121338/18760)** freakhosting.com (бюджет VPS) — обсуждают, но кто-то сканировал с их IP и активно брутил SSH [18780-18784]; Илья собирался пробовать самый дешман с мониторингом.
- **[id=17990|—|28.09.2025](https://t.me/c/2941121338/17990)** Панель перенесена на h2.nexus (Польша 8/16) — полет нормальный.
- **[id=18520|—|29.09.2025](https://t.me/c/2941121338/18520)** Турция: плохо, разве что ishosting дает IP, но ограничения так себе [18523].
- **[id=18386|Edward Forix|29.09.2025](https://t.me/c/2941121338/18386)** Нидерланды от Aeza — советуют сменить [18387].
- **[id=17395|Danila Tsaplin|27.09.2025](https://t.me/c/2941121338/17395)** ihc.ru — 4 месяца ютуб без рекламы и затыков; cloud.ru — хорошо, но github-страницы скриптов установки панелей забанены; сервер, купленный для теста — ютуб с «затыками» каждые 5 минут.
- **[id=19562|Глеб|30.09.2025](https://t.me/c/2941121338/19562)** Хосты на VMm6 — все «кал» (aеза, veykor, h2nexus, xcent), ретном только в Финке и Эстонии; melbicom.net рекомендован (long uptime, looking glass) [19532-19567]; YottaSrc — не слышал.
- **[id=19567|PEpeSan|30.09.2025](https://t.me/c/2941121338/19567)** edisglobal.com — «хорошие сервера», перекупы (ASN чужие).
- **[id=17215|Haxonate|26.09.2025](https://t.me/c/2941121338/17215)** В РФ для VPN-прод — Hosting Russia.

## Бедолага-мелочи и бизнес-контекст
- **[id=14640|—|24.09.2025](https://t.me/c/2941121338/14640)** Тикет-система обновлена @pedzeo: автовыдача промогрупп за общие траты + скидка на период; +2 платежки (MulenPay, PayPalych); external_link_miniapp для мониторинга; фикс удаления юзера, бэкапы/восстановление; обновленное меню промогрупп.
- **[id=14666|Дмитрий|24.09.2025](https://t.me/c/2941121338/14666)** Баг: повторное нажатие на выбранный пункт устройств при оформлении подписки выдает «подпишитесь на канал» (при включенной обязательной подписке).
- **[id=14753|Alex|24.09.2025](https://t.me/c/2941121338/14753)** Цены в USD — возможность отсутствует (обсуждение).
- **[id=14754|—|24.09.2025](https://t.me/c/2941121338/14754)** Готовые тарифы из админки против «конструктора»: наклепать тарифы списком, отключить конструктор — короче путь [14786, 18218]. Мнения: люди не читают, «тариф 50 рублей, а по итогу 400» [14780].
- **[id=14696|—|24.09.2025](https://t.me/c/2941121338/14696)** DEFAULT_AUTOPAY_DAYS_BEFORE=3 — Илья не понимает зачем; лучше просто дефолт автопродление вкл [14691-14698].
- **[id=14830|—|24.09.2025](https://t.me/c/2941121338/14830)** Триал не плюсуется с подпиской (был вопрос) [16440].
- **[id=17407|BURJUY|27.09.2025](https://t.me/c/2941121338/17407)** Торренты: router DIRECT + torrent blocker.
- **[id=17413|Gy9vin|27.09.2025](https://t.me/c/2941121338/17413)** Идея: тарифы «сколько гигабайт» — ограничение по гигам на отдельных серверах.
- **[id=17702|Haxonate|28.09.2025](https://t.me/c/2941121338/17702)** HWID работает только с Remna (у Happ есть передача HWID в панель).
- **[id=17931|—|28.09.2025](https://t.me/c/2941121338/17931)** ✈️ Передача HWID в панель — работает только с Remnawave.
- **[id=17233|Gy9vin|26.09.2025](https://t.me/c/2941121338/17233)** 500+ активных пользователей → ~8 ТБ трафика/мес (при R0xTaDDy 250 юзеров и подписке 200₽ тоже 8 ТБ). 26 активных → 1.2 ТБ.
- **[id=18627|Ко|29.09.2025](https://t.me/c/2941121338/18627)** Купил кинокбот за 32 000₽ (модуль рекламы 5500₽) — коммент про ценообразование сторонних ботов.
- **[id=18799|Egor|29.09.2025](https://t.me/c/2941121338/18799)** Монетизация Bedolaga — только вебадминка (планируется ~1000₽/мес, лайт-версия бесплатно, топ-донатерам бесплатно); бот, саб-страница, API остаются бесплатными.
- **[id=18830|Egor|29.09.2025](https://t.me/c/2941121338/18830)** Проект (веб-админка) делает сторонняя команда (не он в верстке).
- **[id=19192|Pangur Ban|30.09.2025](https://t.me/c/2941121338/19192)** Скидка на доп.услуги в промогруппах (за период) применялась только к базовому периоду, не ко всему заказу — репорт; Egor: перенесет настройки скидок в раздел промогрупп [19232-19238].
- **[id=19153|R0xTaDDy|30.09.2025](https://t.me/c/2941121338/19153)** Запрос: бонус на баланс при пополнении от суммы N (реализовано: бонус только на первое пополнение) [19190].
- **[id=19282|Gy9vin|30.09.2025](https://t.me/c/2941121338/19282)** Подписки отключаются в DISABLE при том, что срок не истек и трафик есть — предложено сравнить даты окончания в боте/панели (баг рапортован).
- **[id=19027|—|30.09.2025](https://t.me/c/2941121338/19027)** Синк серверов теперь удаляет неактивные сервера (сквады) из бота.
- **[id=19196|—|30.09.2025](https://t.me/c/2941121338/19196)** В серверах теперь можно смотреть подключенных юзеров.
- **[id=19292|R0xTaDDy|30.09.2025](https://t.me/c/2941121338/19292)** Уведомление о пополнении светит имя администратора — решение: выдать деньги с саппорт-аккаунта (добавить его в админы) [19294-19304].
- **[id=19767|BURJUY|01.10.2025](https://t.me/c/2941121338/19767)** WEB_API_HOST=0.0.0.0 наружу не светит — API на 8080, доступ только с самого сервера (Caddy/nginx проксирует нужное) [19773].
- **[id=17941|—|28.09.2025](https://t.me/c/2941121338/17941)** Идея «сделать одну большую кнопку» — редукция UI для слабых пользователей.
- **[id=18000|Egor|28.09.2025](https://t.me/c/2941121338/18000)** Промик BEDOLAGA -30% первый месяц у @dhostVPS_bot (см. выше).
- **[id=15985|Иван Болгов|25.09.2025](https://t.me/c/2941121338/15985)** Вопрос «у тебя ещё страничка подписки есть?» — да, ремнавейв-саб пейдж.
- **[id=17366|BURJUY|26.09.2025](https://t.me/c/2941121338/17366)** Донат-ссылки автора (карточка/tribute/USDT TRC20) — по ссылке: https://t.me/tribute/app?startapp=duUO.
- **[id=19565|Максимка|30.09.2025](https://t.me/c/2941121338/19565)** Скрипт установки ноды (доработанный Edward Forix): https://gist.github.com/SantaSpeen/e52938ca39b8f4007b4dff669561a9f2
- **[id=19565|Максимка|30.09.2025](https://t.me/c/2941121338/19565)** Установка ноды Remna одной командой:
```bash
bash <(curl -fsSL https://cc.watchcats.ru/install-remnanode.sh)
```
(обновляет пакеты, ставит докер/зависимости, чистит мусор, спрашивает APP_PORT и SSL_CERT, запускает ноду).
- **[id=17417|свэгги|27.09.2025](https://t.me/c/2941121338/17417)** (рефакторинг) — BB-код тарифов «мой код»: подробности у автора.

## Мусор/офтоп
- (флуд) Дискуссии про AiE, ВОВ, донаты, шаурму, BURJUY vs мачка, «возраст», доту, Оренбург, ltsc/Windows, Minecraft, сериалы и пр. — без знаний.
