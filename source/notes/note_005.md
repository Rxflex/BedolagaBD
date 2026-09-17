# Заметки из chunk_005 (id 19809..24244, 01.10.2025 .. 09.10.2025)

## MiniApp подписки (v2.4.2+) — полная настройка (большая тема недели)
- **[id=19813..19957|Egor|01.10]** Новый встроенный MiniApp: подписка работает через **WebAPI бота** (порт 8080), не через панель ремны. Шаги установки: 1) reverse-proxy на новый домен миниапки (nginx/caddy) + серты; 2) `WEB_API_DEFAULT_TOKEN=` — придумать самому в .env (6–20 символов); 3) смонтировать в докер бота папки `./miniapp:/app/miniapp:ro` и `./app-config.json:/app/app-config.json:ro` (в корне бота создать и закинуть app-config.json + index.html); 4) в настройках бота указать домен миниапки, включить API бота; 5) в BotFather указать ссылку на миниапку (кнопка «Подключиться»).
- **[id=19971|BURJUY]** Проверка API: `{"status":"ok","api_version":"1.0.0","bot_version":"v2.4.2","features":{"monitoring":true,...}}`. Браузер выдаёт `{"detail":"Method Not Allowed"}` — норм: запрос без ключа; из ТГ по ссылке работает.
- **[id=20034..20037|Egor]** Режимы кнопки «Подключиться» (env):
  ```env
  # guide - открывает гайд подключения (режим 1)
  # miniapp_subscription - открывает ссылку подписки в мини-приложении (режим 2)
  # miniapp_custom - открывает заданную ссылку в мини-приложении (режим 3)
  # link - открывает ссылку напрямую в браузере (режим 4)
  CONNECT_BUTTON_MODE=miniapp_custom
  ```
- **[id=20132..20141]** Ошибка `inline keyboard button Web App URL '' is invalid: URL host is empty` = включён `CONNECT_BUTTON_MODE=miniapp_custom`, но пуст `MINIAPP_CUSTOM_URL`. Обязателен при этом режиме.
- **[id=20203..20309|maks]** Полный рабочий docker-compose бота v2.4.2: postgres15-alpine (healthcheck pg_isready), redis7-alpine (`--maxmemory 256mb --maxmemory-policy allkeys-lru`), бот с volumes logs/data/locales/app-config.json/timezone/vpn_logo.png, ports `"127.0.0.1:${WEB_API_PORT:-8080}:8080"`, `"${TRIBUTE_WEBHOOK_PORT:-8081}:8081"`, `"${YOOKASSA_WEBHOOK_PORT:-8082}:8082"`, network bot_network 172.20.0.0/16.
- **[id=20346..20353]** Лого: `chmod +r vpn_logo.png` в корне бота (права на чтение — иначе «нет эмодзи»/логотип).
- **[id=20391]** Канонический рестарт: `docker compose down && docker compose up -d && docker compose logs -f`.
- **[id=20394]** docker cp файлы в контейнер nginx: `docker cp 91e33556b0d3:/app/miniapp /tmp/remnawave-miniapp` → `docker cp /tmp/remnawave-miniapp remnawave-nginx:/var/www/remnawave-miniapp` (если не монтировать volume).
- **[id=20376..20378|ViToS]** Рабочий nginx для миниапки (два разных компоуза в одной докер-сети):
  ```nginx
  server {
      listen 80; listen 443 ssl http2;
      server_name newpodpiska.domain.com;
      ssl_certificate "/etc/nginx/ssl/fullchain.pem";
      ssl_certificate_key "/etc/nginx/ssl/privkey.key";
      root /var/www/remnawave-miniapp; index index.html;
      location = /miniapp/app-config.json { add_header Access-Control-Allow-Origin "*"; try_files $uri =404; }
      location / { try_files $uri /index.html =404; }
      location /miniapp/ {
          proxy_pass http://remnawave_bot:8080/miniapp/;   # имя контейнера, не 127.0.0.1!
          proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  ```
  volume nginx: `- /opt/.../miniapp:/var/www/remnawave-miniapp:ro`. Ключевая ошибка многих: nginx и бот не в одной докер-сети → `host not found in upstream "remnawave_bot"`. 90% сетей: `remnawave_network`.
- **[id=20408..20429|Генадий]** Вебхуки через nginx (случай «всё на 443»): `listen 443 ssl`, location `/tribute-webhook`→127.0.0.1:8081, `/cryptobot-webhook`→8081, `/mulenpay-webhook`→8081, `/pal24-webhook`→8084, `/yookassa-webhook`→8082, `/health`→8081/health. Смена YOOKASSA_WEBHOOK_PORT на 443 — НЕ надо. 405 на /cryptobot-webhook — норм (Method not allowed = слушает).
- **[id=20681]** Ошибка пути вебхука: `ValueError: path should be started with / or be empty` — слеш убрать в webhook path env.
- **[id=20775..20776|Garry]** Время в боте -3ч от панели: подписки привязываются к UTC; TZ в докере `Europe/Moscow`; позже фикс — «сделайте синк с ремной, пропадёт разница» [id=23467].
- **[id=20793]** Синхронизация серверов: бот → Админ панель → Подписки → Управление серверами → Синхронизация (без неё пользователи не видят страны).
- **[id=20888..20912]** Ошибка `ERR_UNKNOWN_URL_SCHEME` при открытии `happ://` из миниапп ТГ, если приложение не установлено (десктоп): нужен **редирект-шаблон** `HAPP_CRYPTOLINK_REDIRECT_TEMPLATE=` (страница-редирект в репо `miniapp/redirect`), формат `https://miniapp.domain.com/redirect/?redirect_to=happ://...` [id=22561]. С пк прямой импорт в приложение из миниапки ТГ не работает в принципе [id=22532|Egor].
- **[id=20911..20912]** UX-решение: после попытки открыть happ:// показываем кнопку «Не получилось?» (успех — уйдёт, провал — увидит инструкцию установки).
- **[id=21371..21374]** «Subscription Not Found» в nginx-миниапке: у proxied location `proxy_set_header X-API-Key "КЛЮЧ-WEBAPI"` (контейнер `remnawave_bot_api`) — рабочий конфиг:
  ```nginx
  server { listen 80; listen 443 ssl http2; server_name miniapp.example.com;
    root /var/www/remnawave-miniapp; index index.html;
    location = /app-config.json { add_header Access-Control-Allow-Origin "*"; try_files $uri =404; }
    location / { try_files $uri /index.html =404; }
    location /miniapp/ { proxy_pass http://remnawave_bot_api/miniapp/; proxy_set_header X-API-Key "КЛЮЧ-WEBAPI"; ... }
  }
  ```
- **[id=23803..23806|Egor]** TG кеширует миниапку на уровне бота+юзера на своих серверах. Обход кеша: в BotFather указать `https://miniapp.domain.com/?v={time.time()}`.
- **[id=20244|BURJUY]** Автоинкремент PG после восстановления бекапа — лечится setval всех sequences (см. баг-раздел).

## Bedolaga релизы v2.4.x
- **[id=21791|Egor|04.10|v2_4_3]** Улучшенная архитектура, автоустановщик install_bot.sh (5 мин, интерактивное меню: мониторинг/контейнеры/логи/автообновление/бекапы/чистка/Caddy/.env с маскировкой), StartupTimeline, автосинк PG sequences после восстановления, retry при создании юзеров, MulenPay детальное логирование (by @Legacyyy777), MiniApp desktop-редиректы (isDesktopPlatform/getDesktopRedirectLink), REST: is_configured/configuration_error. Установка: `curl -fsSL https://raw.githubusercontent.com/Fr1ngg/remnawave-bedolaga-telegram-bot/main/install_bot.sh -o install_bot.sh && chmod +x ./install_bot.sh && ./install_bot.sh`.
- **[id=22764|Egor|06.10|v2_4_4]** Система промо-предложений: скидки автоматом при оплате/автопродлении; тестовые доступы к сквадам через акции (временная выдача); модели PromoOfferTemplate/PromoOfferLog/SubscriptionTemporaryAccess; скидка хранится в promo_offer_discount_percent и сбрасывается после использования; таймеры и прогресс-бары; рассылка промо по сегментам; логирование всех операций. KeyError 'amount' баг — фикшено.
- **[id=23024|Egor|07.10|v2_4_5]** Персональные промо-предложения (отправка конкретному юзеру, поиск по имени/username/ID); REST /promo-offers (GET/POST/{id}/logs/templates); /pages — CRUD для политики конфиденциальности, оферты, FAQ, правил (многоязычно RU/EN, автопагинация); TRIBUTE_WEBHOOK_HOST и YOOKASSA_WEBHOOK_HOST для кастомного bind; таблицы privacy_policies, public_offers, faq_settings, faq_pages; раздел «Инфо» в главном меню (правила/статус/FAQ).
- **[id=23465|Egor|08.10|v2_4_6]** Скидочные уровни за траты (раздел в инфо, прогресс до следующего уровня); продление/сокращение подписки админом (-365..+365, быстрые ±7/±30); триальные серверы: is_trial_eligible, случайный выбор из пула; зачёркнутая старая цена при скидке; включение/отключение пакетов трафика (минимум 1 активен); TZ-обработка с fallback UTC; `DEFAULT_AUTOPAY_ENABLED` в .env (true = автосписание включено по умолчанию для новых).
- **[id=23779|Egor|09.10|v2_4_7]** Расширение MiniApp API: промо-оферы/промокоды/промогруппы, реферальная система (MiniAppReferral*), FAQ + юридические документы, удаление устройств; MiniAppSubscriptionResponse + promo_offers/promo_group/auto_assign_promo_groups/total_spent/faq/legal_documents/referral_info.

## Платежки (подробный опыт)
- **[id=21968|Egor]** MulenPay: по дефолту **не шлёт подпись в хуках**; @Legacyyy777 ковырял — работает, но без подписи можно фейк-хуками пополнять баланс (спуфинг платежей). В v2_4_3 [id=21791] добавлено детальное логирование хуков; после мержа Мулен получает 200 и не спамит 3 раза [id=21793, 23524].
- **[id=22344..22347|legiz]** Гей-платежки: палыч = 10% [id=23441 «по сбп 9% +50 руб дерут как трибут 10%»]; **URLPay** — «зеркало/дочька Мулена», хук `/urlpay-webhook` не ловится ботом (ловится `/mulenpay-webhook`), авто-подтверждения нет, нужен ручной «проверить платеж» [id=23519..23533]; у кого-то заработало без доп. правок [id=23538]. Мулен переходит на URLPay: юрлицам — Мулен, физикам — URLPay [id=22414].
- **[id=22840|Egor]** Pal24 (Палыч): webhook secret не нужен, можно любой токен для теста хука:
  ```bash
  SIGNATURE=$(python - <<'PY'
  import hashlib, os
  token = os.environ.get('PAL24_SIGNATURE_TOKEN', 'test_token')
  print(hashlib.md5(f"100.00:test-order-1:{token}".encode()).hexdigest().upper())
  PY
  )
  curl -X POST https://your-domain.com/pal24-webhook -H "Content-Type: application/json" \
    -d '{"InvId": "test-order-1", "OutSum": "100.00", "Status": "SUCCESS", "SignatureValue": "'$SIGNATURE'"}'
  ```
- **[id=22802]** Совет по модерации платежек: регистрировать бота как «левый бот» (не указывать прямо что ВПН).
- **[id=22982..22983]** Трибут: канал без контента → «заявка на выплату отклонена, напишите в поддержку» [id=23593]; донаты через трибут падают на счёт в самом боте [id=21877]; добавление бота трибута в админы канала не мешает [id=23609].
- **[id=23362]** Автоплатежи: списание с баланса работает если денег хватает [id=21867]; DEFAULT_AUTOPAY_ENABLED=false → всё как раньше, true → у новых автопродление по дефолту [id=23458].
- **[id=22792, 24076]** Баг конвертации звезд/крипты: пополняешь на 200, приходит 199 (округление вниз вместо вверх; курс 0.9, 222 звезды → 199.8 → округлить надо к 200).

## База данных (проблемы и фиксы)
- **[id=21506..21507|Дмитрий]** Универсальный фикс sequence после восстановления бекапа: `docker exec -it remnawave_bot_db psql -U remnawave_user -d remnawave_bot` и набор `SELECT setval(pg_get_serial_sequence('TABLE','id'), coalesce(max(id),1), max(id) IS NOT null) FROM TABLE;` для всех таблиц (users, subscriptions, transactions, promo_groups, promocodes, squads, yookassa_payments, mulenpay_payments, pal24_payments, cryptobot_payments, ticket*, broadcast_history, web_api_tokens, welcome_texts и т.д.); затем `docker restart remnawave_bot`. Ошибка была `duplicate key value violates unique constraint "users_pkey"`.
- **[id=22980|Дмитрий]** Пароль БД: в compose юзер/пароль прописаны, в env другие → 3 выхода: дефолтные данные, сменить пароль PostgreSQL командой, или снести и поставить руками с настроенным env (просто сменить пароль в env не прокатит).
- **[id=21859, 23005]** Деактивированные пользователи: есть настройка деактивировать/удалять (по дефолту удаление), но в ряде версий не работает.

## Безопасность и атаки
- **[id=20919..20924, 23238]** Сканеры: с ASN censys/денвер США долбят вебхуки; совет fail2ban; автоматические сканы — «забей».
- **[id=23773]** ТГ кеширует миниапку бота+юзера (см. выше `?v={time.time()}`).
- **[id=23840..23945]** Атака сносом ботов: тип с ником `t.me/+42` (и варианты) входит в бота → бот выводит ссылку-приглашение `t.me/...` → жертва кидает репорт → тег скрипт сносит бота как фишинговый. Защита: в PR 988 добавлена валидация ников (t.me/ → блок/рандомизация) [id=24240, 24083 «добавил доп защиту от пустых значений»], оффнуть подписку на канал, работать только по TG_ID [id=24073]. Модератор-бот Rose/фильтры, воронка по дате создания аккаунта (<3 дней), «вход платный = лучшая капча» [id=24040].
- **[id=24187]** Досье/деанон-бот @Safetyformed_Bot (пробивает телефоны/теги).

## Хостинг (опыт)
- **[id=22963|Egor]** Промокод `BEDOLAGA` на @dhostVPS_bot — 30% первый месяц, 10гбитка Нидерланды, 3 месяца без проблем.
- **[id=21443..21447]** Хостинг @biil_robot (Япония): VPS отдыхает с 29.09 неделю, поддержка молчит; с РФ-тарифом срубил после месяца («бот по ошибке выдал РФ, для тарифа нет РФ»).
- **[id=21958, 22079]** Вейкор (Germany promo): 14 евро взял, 2 месяца аптайм отличный; промка 100 мбит, остальные гбит.
- **[id=22420..22424, 22430..22431]** Дешёвые альтернативы аезы: 1cent за 150р (подсети иногда падали, починили), firstbyte (год без проблем, основной трафик), Sber VDS (полгода без обращений в саппорт).
- **[id=22153|Глеб]** IP-регион сервера serv.host 193.23.201.123: MaxMind=US/Orem, IPinfo=GB/Southend, Cloudflare=GB, RIPE=GB; ipregistry: Malicious ❌ Server ✅.
- **[id=20776..20781]** Каналы/гаранты: на ВПС 50 гбит не бывает (только выделенка $1000+); гигабит ~100–120 юзеров; у «Ко» 7 евро гарант 1 ГБ (Москва/Питер/Германия, 25 гиг).
- **[id=24057]** «норм сервер рублей 300» — с IP+NVMe.
- **[id=22312..22314]** Промо-тарифы хостеров: для тестов 1-2х людей, нагрузки не держат, помощь не оказывается, РФ могут не выдать.

## Полезное из отельного (зеркальные темы)
- **[id=20737..20746|Илья/R0xTaDDy]** Мониторинг: Prometheus → Grafana; cadvisor тоже; статистика сохраняется в панельке.
- **[id=22108..22112]** Скоростные тесты в РФ: спидтесты под запретом, юзать iperf3 из скриптов:
  ```bash
  bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh)
  wget -qO- https://raw.githubusercontent.com/jomertix/server-scripts/refs/heads/master/speedtest/countries/speedtest_ru.sh | bash
  ```
- **[id=22144..22246|legiz]** Клиенты на ПК: mihomo-ядро; Prizrak-Box, Koala Clash, FlClashX — «родные» от комьюнити Remnawave; Happ на ПК — «изделие дьявола» (у кого-то чёрный экран на Win11); на iOS: v2Ray или Happ (Streisand — «кал»); для пенсионеров — большая кнопка Happ, для продвинутых sing-box/Clash Meta; криптолинк привязывает к хаппу, лучше держать как «одиночный» режим.
- **[id=22470..22475|legiz]** Роутеры для VLESS: только на filogic-процессорах (mips — «не самый сок», ax3000t — православный вариант); Keenetic Giga (KN 1011) — mips, хуже; xkeen+mihomo: https://github.com/OMchik33/Keenetic-Mihomo; на NanoPi можно openwrt, дёшево как прослойка/домашний сервер.
- **[id=22316..22325|Egor]** Сценарий докер-сети бота+nginx/caddy (общий композ бота):
  ```yaml
  services:
    caddy:
      image: caddy:2.9.1
      container_name: caddy-selfsteal
      volumes:
        - ./Caddyfile:/etc/caddy/Caddyfile
        - /opt/caddy/html:/var/www/html
        - caddy_data:/data
        - caddy_config:/config
        - /root/bot/miniapp:/var/www/remnawave-miniapp:ro
      network_mode: "host"
  networks:
    default:
      name: bot_network
      external: true
  ```
- **[id=22329|Egor]** eGames-установщик REMNAWAVE_SECRET_KEY: просто Enter; нашёл в nginx.conf; панель к себе не пускает → подключить бота к сети nginx.
- **[id=21928..21929|Haxonate]** Синхронизация юзеров из панели: бот берёт юзеров панели по их TG-ID; юзер с подпиской в панели зайдёт в бота — увидит существующую подписку.
- **[id=21099..21102|Egor]** Установка автоустановщика (install_bot.sh): клон → mkdir logs/data/backups/referral_qr → chmod 755 → chown 1000:1000 → ./install_bot.sh; пункт (8) — настроить обратный прокси (монтирует файлы, куки-ключ, серты), управляет Caddy (установит если нет, поправит докер), бекапы файлов перед правками, бекапы/восстановление данных.
- **[id=21176..21181]** nginx location для redirect-страницы:
  ```nginx
  location ^~ /redirect-page/ {
      alias /usr/share/nginx/html/redirect-page/;
      index index.html;
      try_files $uri $uri/ /index.html;
  }
  ```
- **[id=21077..21078]** Redirect-страница от мапоши: в README репо maposia написано про редирект — «я как попугай тут про это пишу».
- **[id=22046]** «Подводные камни»: локали (mulen pay → urlpay), где менять названия кнопок/логов — монтировать `./locales:/app/locales:rw`; изменения только через `docker restart` (команда git-подтяжки локалей не сработала у многих).
- **[id=22550..22564|Egor]** Настройка nginx для редиректа (пример полный есть в README «Ручная настройка nginx в docker»); на дискуссию «криптолинк» добавил: «светим ток домен внешней страницы подписки, а на ней уже криптолинк».
- **[id=22613..22614]** Если редирект есть но не фурычит: проверить монтирование папки miniapp/redirect + пути в nginx conf.
- **[id=22628..22630]** «Кнопка подключиться» — настраиваемая (куда ведёт, можно отключить). При отсутствии подписки у юзера кнопка «купить подписку» может быть неактивна (норма).
- **[id=22856]** «Просто пользователя создать в ремне и дать ключ» — для семьи/друзей бот не обязателен.
- **[id=22877..22883|Илья]** Его админский бот remna-ad (Case211/remna-ad): апдейт UI, смена языка RU/ENG, inline-кнопки изменения параметров подписки, авторизация по токену из .env.
- **[id=21044..21045]** Xray на ноде не стартует: `XML-RPC fault: SPAWN_ERROR: xray` — сканеры долбят 127.0.0.1:61000/61001 stats; серты/пути к конфигу; решение — проверять серты/порты [id=21055].
- **[id=20671..20675]** Часовой пояс в боте: подписки привязываются к UTC, TZ env/докер на Москву не всегда достаточен — синк с ремной.
- **[id=20736..20743]** Как защититься: вводить бота только на прод-серверы, а не домашние; следить за логами (смотри `docker exec remnanode xlogs` для Xray логов юзера — только realtime).
- **[id=21197..21205|Gαɾɾყ Sσƙσʅσʋ]** Перенос сквадов/стран между серверами: дубли ID в таблицах после ручного восстановления → sequence sync (см. выше).
- **[id=23485..23494]** Продление/сокращение подписок админом: работает через админ-панель бота.
- **[id=23032]** «Проекту Bedolaga 2 месяца (с 21.08)» — темп обновлений очень быстрый.
- **[id=24046|Дмитрий]** «Теперь мой любимый михомо на FlClashX открывается на ПК» — импорт конфига mihomo из миниапки в FlClashX заработал.
- **[id=23735..23752|Egor]** FAQ/странички/партнёрку вынес в миниапку; FAQ по умолчанию свернут, содержимое редактируется, тянет из бота.
- **[id=23219..23224|Egor]** «Локали не совпадают» — en 1154 строк, ru 1118; репорт ошибках локали [id=23487..23488] — настройки с примитивными описаниями (триал 3 дн / warn 2 ч).
- **[id=23409]** Тикет-система: у бота без юзернейма у юзера тикет не открывается; у Pedzeo — своя версия админки (благодарят «200 лет за такое»), вопрос мержа [id=23752].
- **[id=23593..23597]** Трибут-донаты: на пустых каналах просят объяснение в саппорте @TributeCreatorBot (лучше иметь посты/фоловеров в канале, канал привязан к трибуту).
- **[id=23604..23605]** Названия ботов без слов VPN/VPS («VNP» вместо VPN) — чтобы платежки не банили; юкасса раньше одобряла впн-ботов [id=22895..22896].
- **[id=22875..22876]** Бот на продажу ВПН в ТГ — не запрещено напрямую; продавать можно, но на двоих парней «рублей 2000» [id=23413..23414] — «за 2000р настроил бота кому-то. полностью с хуками платегами».
- **[id=23427..23432]** «Для казуалов» хостер: 75р VDS в РФ для себя, 100р для продажи; скорость 200мбит; на фирстбайте домашний впн ок.
- **[id=23487..23492]** Идея промо-групп: порог уведомления «ещё 400р до скидки» — Egor «есть такое в планах».
- **[id=23487]** «продажа ВПН не запрещена (пока правоприменительной базы нет)» — в целом боты живут без юрлица, но есть риски.
- **[id=23787]** Сабка-страница Егора работает через API бота: подключится, добавить, оплатить подписку [id=21904..21905]; ранний вид — просто index.html.
- **[id=22710..22711]** «Разрешить Groups в BotFather» нужно отключить (Allow Groups), чтобы типы с ником `t.me/+42` не ломали ботов [id=23855..23856].
