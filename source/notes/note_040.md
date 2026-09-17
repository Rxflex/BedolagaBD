# Заметки из chunk_040 (id 231865..237420, 18-22.02.2026)

Период: релизы Bedolaga Bot v3.17.0 и Cabinet v1.19.0, анти-стресс вокруг миграций, массовое обрушение связей Яндекса/ВК/операторов, длинные разборы миграций/балансировки/мостов, обязательный троллинг «Семёна» (продолжение).

## Релизы Bedolaga Bot
- **v3.17.0 (19.02, id 232625, Egor)**: 🚀 Реферальный код во всех методах авторизации кабинета (?ref=CODE в Telegram Mini App/Widget, OAuth Google/Yandex/VK, email login; защита от самореферала); миграция Alembic для таблицы email_templates (notification_type, language, subject, body_html). Фиксы: «caption is too long» в режиме логотипа (>900 символов → send_message вместо send_photo); фильтрация заблокированных в триальных уведомлениях (SQL-фильтр + pre-send проверка, экономия рейт-лимитов; убрана автоблокировка при рассылках); import shadowing UserStatus.
- **Cabinet v1.19.0 (19.02, id 232644, Egor)**: реферальный код во всех методах авторизации (?ref=CODE в localStorage TTL 24ч, one-time read-and-delete по pattern campaign.ts; код в deep link Telegram Widget; OAuth сохранение до редиректа). Фикс: redirect loop при отключенном email auth и наличии реферального кода.
- Во время отпуска Егора (до 23.02) фиксы копились в dev-ветке (id 232214/232272/234702).

## Ошибки после релизов 19-22.02
- Ошибка BUTTON_DATA_INVALID при выборе серверов для нового тарифа (id 235678/235689, Егор) — «новые тарифы не позволяют выбрать сервера», «в старых все норм»; после переустановки /root/remnawave ошибка не устранилась, меню исчезает. Лечение по комментариям Егора (id 236263): снести и накатить заново бэкапы панели distillium + бота на чистом сервере; создание нового тарифа решает проблему выбора серверов.
- Не обновляемый файл (id 231868-231871, Евгений/Егор) — ругань на docker-compose.yml (для цветных логов FORCE_COLOR).
- «Пишет лимит доменов достигнут» при попытке создать новый домен бота (id 233123/233126, Константин).
- «Error response from daemon: invalid pool request: Pool overlaps with other one on this address space» (id 233130/233131, Alex).
- Плавающая ругань на ссылку «cabinet» в кнопке «Подключиться» при CONNECT_BUTTON_MODE=miniapp_subscription — открывает страницу подписки Remnawave вместо миниаппки; запрос на разделение параметров (id 235746/235747, Андрей).
- После обновы на 3.17: ошибка при создании бэкапа и при восстановлении database.json (восстановление не запускается, логов нет) (id 235092, {name: Popugtop!}); импорт .env выдает ошибку (id 235092).
- «Telegram server says - Bad Request: chat not found» — стартовый уведомитель/глобальный error handler (id 235419, 236239) — проверять ADMIN_NOTIFICATIONS_CHAT_ID.
- Ошибка при подписке «Сообщение слишком длинное» (id 231931/231991) — локализация с сообщением «caption is too long», искать через поиск IDE (id 231997).
- «Работа с кнопками из ботфазера: emoji отключены» (id 232628, tgshtt) — подписку покупают в клиенте.
- Ошибка «Failed to create network remnawave-bedolaga-telegram-bot_bot_network: Pool overlaps» (id 233130/233131) — (см. выше).
- Как поднять кабинет из образа: `docker pull ghcr.io/bedolaga-dev/bedolaga-cabinet:latest; docker create --name tmp_cabinet ghcr.io/bedolaga-dev/bedolaga-cabinet:latest; docker cp tmp_cabinet:/usr/share/nginx/html ./cabinet-dist; docker rm tmp_cabinet` (id 233021/233023, —) — так вытащили фронт статики кабинета на целевой сервер.

## Настройки меню/кнопок/кабинета (v3.17+)
- Скрыть кнопку "Подключиться бесплатно": «Админка → Настройки → Интерфейс → Кнопки» (id 232068, Tatoxa; id 233573, Aleksandr).
- Кабинет и .env: параметр из .env приоритетнее кабинета; закомментить в .env и настроить в кабинете (id 235355, 🪲).
- Кнопки красятся только URL-кнопки (id 227341, eval) — (из чанка 039, не здесь).
- Меню/кнопки: «Меню настройки → cabina» (id 234699..234702) — (флуд).
- «MAIN_MENU_MODE=cabinet» + «CABINET_ENABLED=true» + «CABINET_URL» + «MINIAPP_CUSTOM_URL» + «CABINET_JWT_SECRET» + «CABINET_ALLOWED_ORIGINS» + «CABINET_BUTTON_STYLE» — набор для полного перехода на кабинет (id 235078, Андрей Сергеевич).
- Триальный тариф: TRIAL_DISABLED_FOR (id 234090, Motion) — задать «ALL» (id 234093) чтобы отключить триал для всех; либо «админка бота - настройки - конфигурация бота - пробный период - TRIAL_DISABLED_FOR» (id 234102, Роман).
- Как включить/выключить триал для отдельного юзера — админка, настройки пользователя (id 229467..229469 из чанка 039).
- Триальный тариф не выделяется (id 235136-235210, Евгений/tgshtt): чтобы заработало, нужно: в .env прописать триал (n дней/n гб/n устройств), в боте выдать триальные серверы, галка «выдавать триал» на нужных сквадах в админ-панели (id 235152..235158); сам триальный тариф при этом «без тарифа» у пользователя — по факту работает и без тарифа.
- Колесо удачи с промокодом: «ошибка сети при вращении барабана» (id 236163, Павел) — баг, без решения.
- «Приветственное сообщение» в кабинете через админ панель (id 229219 — из 039).
- Настройка «Почта - oauth - Google/Yandex» на гугле/яндексе — redirect_uri_mismatch (id 233987..233990, Илья З./—) — колбэк `https://cabinet.example.com/auth/oauth/callback` (id 233987, Sayonara) для всех oauth.
- Кабинет: почему при регистрации по email 2 аккаунта в одном клиенте телеги видят подписку с одного устройства (id 235980/235984, —/.) — (флуд).
- Кабинет: повторная активация админа в кабинете после «забанить» (id 235030, Bulat) — (флуд).
- Кабинет: «Нет тарифа» у триальных юзеров после включения TRIAL_DISABLED_FOR=ALL — отключить hidden (id 235103..235105).
- Кабинет: «Что такое реквизиты» (id 235219..235232) — (флуд).

## Сеть/проксирование/домены
- «docker network connect bot_network remnawave_bot» — закрепленный из предыдущих чанков; здесь также «docker network connect shared_network remnawave_bot» (id 233647, Tatoxa) — своя сеть из кабинета/панели.
- Кабинет к удаленному боту: Caddy, api `/api/*` на 8080; frontend `root /srv/cabinet` (id 232936/232945, QuallS; docker-ps показан с отдельными контейнерами remnawave, subscription-page, postgres, valkey) (id 232950).
- Caddy лог-секция на hooks/miniapp домен (id 233019..233029, QuallS).
- Два домена (hooks + miniapp) — рекомендуется (id 236412/236416, Егор); «в идеале иметь три домена 2 уровня… четыре: нода/панель/сабка/кабина» (id 236632..236641, tgshtt/Egor).
- «Тг бот не привязан к домену» — после привязки в botfather чекай логи (id 236480/236481, A M/—).
- 405 Not Allowed на хук (id 233690) — сам хук пишет 405 nginx при curl.
- «Could not resolve host» на хук (id 233688, ddddd).
- Кабинет «через яндекс не работает» (id 233650, —).
- Пример nginx конфига для бота (id 236397..236399, даня): upstream remnawave_bot_unified → server remnawave_bot:8080; сервер с hooks domain и все webhook-пути, от app-config.json с CORS, client_max_body_size 32m, ssl_certificate/ssl_certificate_key, listen 80/443 ssl http2, read_timeout 120s, buffering off; miniapp domain со статикой root /var/www/remnawave-miniapp и try_files. «events {} и http {} в default.conf запрещены» (id 236005, I wasn't shot) — кидать полный upstream в основной nginx.conf, а не в conf.d; workaround: «засунь все в одну сеть и поставь localhost:8080 вместо remnawave_bot:8080» (id 236016, libkit).
- «docker compose up -d && docker compose logs -f -t» (id 236370) и «network remnawave-network declared as external, but could not be found» (id 236370, даня) — создать сеть в докере: docker network create remnawave-network (id 237146).
- SSL «decryption failed or bad record mac» на nginx 8443 — чинить по AI-инструкции (id 235700, makdren): openssl version mismatch, сертификаты/ключ, ssl_buffer_size, http2, TLSv1.2/1.3, curl -v --http2, логирование error_log debug (в 4 этапа).
- Убрать miniapp static с хоста: «засунь все в одну сеть и поставь localhost:8080» (id 236016).
- Nginx: «events {} нельзя в /etc/nginx/conf.d/default.conf» (id 236005).

## Порты/протоколы
- Порты 8443/445/9443 — альтернативы 443 (id 234774, Prokurátura).
- Aes-ni: «AES-NI отключено, это ред флаг» (id 237101, Сергей); включение просить у хостера, некоторые включают без вопросов (id 237103/237104, Zavulon/—). Пример AES-NI отключён у nodehost (id 237100..237110, Chill/Сергей).
- SSH брутфорс: на новых 4vps сразу брутят порты ssh (id 235592/235593/235595) — отключить/сменить порт.
- Скорость до нод: «большинство хомяков подключаются на первую ноду в списке» (id 237013, —); DNS-рулетка = не балансировка, 2/3 трафика на одну ноду (id 237290, V M); DNS-балансировка без healthcheck — round robin (id 234888..234891, tgshtt/R0xTaDDy); выбит IP — проверять подсеть (id 234424..234430, из чанка 039).
- Альтернативы DNS-балансировки: burstObservatory+leastLoad (id 232512, Haxonate; 3 замера с таймаутом 2с, повтор каждые 3 минуты; leastLoad исключает пинг >1с и нестабильные >30% tolerance); кастомный middleware-балансер (id 232514, —; load=usersOnline/totalRamGb, max_users_per_gb по умолчанию 20, пример лога).
- remnawave-cloudflare-nodes (id 235271, Евген): скрипт мониторит API панели Remnawave, проверяет состояние каждой ноды (online/offline, enabled, xray), добавляет/удаляет IP в DNS Cloudflare для node.example.com; репо https://github.com/hteppl/remnawave-cloudflare-nodes; теги #мониторинг #балансировка #балансировкаднс #балансировкаdns.
- Anycast (id 236300, Егор) — «юзаем anycast и не паримся».
- Статический IP не (id 237248, Тимур; id 237247, Deleted Account «для всех 1»).
- «Hostoff.net - PL Core 1 - 5€/мес, 1/2/30/ до 10 Gbps» (id 236909/236904, tgshtt/financetroubles); «hostoff - Нидерланды 1/2/30 до 10 Gbps» (id 236465?); «Рекламы по ipv4 на ютубе нет» (id 236904).

## Ошибки/разборы чатов (v3.17+)
- «Не удалось создать шаблон exc=IntegrityError ... null value in column "prize_days" of relation "contest_templates"» — contest_rotation_service (id 234596/234595, Денис/EV) — Egor должен исправить prize_days в DEFAULT_TEMPLATES.
- «column users.email_change_new does not exist» (id 235419, Sonjeffry) — миграция не прошла.
- «column users.partner_status does not exist» (id 230949 v3.16.0 → fix v3.16.1).
- «UnboundLocalError cannot access local variable 'UTC'» при докупке трафика в кабинете (id 236832/236859, Артём/...): фикш v3.15.0 + перебилд контейнера (id 236835, мысли).
- «ProgrammingError ... UndefinedColumnError users.partner_status» (id 234996) — алембик.
- Краш бот с ошибкой update email (id 234996).
- Кэш телеги: у v2rayng не обновляется подписка (id 234800) — «включи другой впн, если обновится, значит режут твой домен, надо менять» (id 234802).
- Кэш Telegram «косячил» у 2-х аккаунтов (id 235984..235990, Евгений/—) — через BotFather: дописать рандомную версию бота → кеш обновится при новом заходе у всех принудительно (id 235876, Евгений).
- «expired waves» — «botbot высрал» (id 236951) — настройки мониторинга/уведомления, отключить (id 236951, Egor).
- «Не удалось отправить отчет» спустя 24 часа (id 236940, Павел) — (не решено).
- «C 17 года закон» (id 230247) — (флуд).
- Ошибки «chat not found» из-за /admin_notifications (id 236248, Роман) — ADMIN_NOTIFICATIONS_*.
- Ошибка в подписке (id 236537/236553) — (флуд).
- «По кнопке «Подключиться» в miniapp_subscription открывает страницу подписки Remnawave вместо миниаппки» (id 235746, Андрей) — разделение параметров запрошено (id 235747).

## Хостинги (Whiteness, id 230786/230801/231180/231293/231299/231789/231849/236763/236769/237368/237394)
- 1cent.host - 🇪🇪 Эстония, Таллин: 180 руб./мес. (1 vCPU / 1 DRAM / 10GB / 1Gbit), IPv6 вкл, BBR вкл; @centhost_bot. (id 230786/230828/231849/236763/237352) — «Швеция 55-60 st» (id 234271/234266, 9/Сергей); «Шляпа, st 55-60, поддержка молчит дней пять» (id 234294/237084, Сергей).
- play2go.cloud - 🇩🇪 Германия, Франкфурт: DE-1 340 руб./мес. (1 vCPU / 2 DRAM / 80GB / 1Gbit), IPv6 выкл, BBR вкл. (id 230801/231293/236769/237359)
- @dhostVPS_bot - 🇩🇪 Германия, Франкфурт: 3 евро./мес. (1 vCPU / 1 DRAM / 10GB / 10Gbit), IPv6 выкл, BBR вкл; 💎 Ютуб как RU - Рекламы нет. (id 231299/236757/237362)
- @Midas_Hosting_bot - 🇬🇧 Великобритания, Лондон: 4 евро./мес. (2 vCPU / 2 DRAM / 30GB / 3Gbit), IPv6 выкл, BBR вкл; 💎 Ютуб - Рекламы нет. (id 231789/236763)
- @nodehost_bot - 🇩🇪 Германия, Франкфурт: 2.2$./мес. (1 vCPU / 1 DRAM / 10GB / 10Gbit), IPv6 выкл, BBR вкл. (id 231849/236766/237087/237269)
- Play2go HI-LOAD-1 Германия 450₽ (1 vCPU Ryzen 9 9950X / 2 GB DDR5 / 80 GB NVMe / 10 Gbit/s, DDoS L3-L4) — «неплохо, айпишники норм видны с LTE» (id 235659, Max R). LC-1 Финляндия 189₽ (id 234946, mah1cul) — «айпи норм но скорость такое себе».
- dhost - 🇳🇱 Нидерланды 5.5€ (1 vCPU / 2 RAM / 30GB NVMe / 10 Gbit/s, безлим. траффик) — «#неплохо» (id 236056, кумите); позже: «у дхост просто ютуб без рекламы» (id 237093).
- intezio - 🇪🇪 EE-1 500₽/мес (1× Ryzen 9 9950X3D / 2 GB DDR4 / 32 GB NVMe / 10 Gbps) (id 236102, financetroubles).
- u1host NL-5950X-2 649₽/мес (2 vCPU Ryzen 9 5950X / 4 GB / 60 ГБ NVMe / 1 Гбит/с* / 32 ТБ траф) (id 235485, Oleg).
- 62yun.ru США promo-S 219₽ (1 ядро 1GB RAM 10 Gb NVMe) — «сильно тупит, разрыв связи раз в 15-40 мин» (id 235097, Сергей).
- VPSVille RU Москва Camp 290₽/мес (1 CPU / 1 GB / 15 Gb / 10 Gbit; тарификация по дням, 300BONUS 300₽ при пополнении от 100₽, безлим FUP, поддержка 16 мин, 99% vCPU, мониторинг CPU/MEM/NET/DISK) (id 236402, Фантомас).
- vps.datacash (datacheap) 210₽/290₽ (10 Гбит) (id 236164/236167, Фантомас/—).
- hostoff.net - 🇳🇱NL / 🇵🇱PL Core 1 - 5€/мес (1/2/30/ до 10 Gbps) (id 236904/236909).
- doubleservers_bot - 🇫🇮Финляндия Хельсинки 5.98€ (2 Core / 4 GB DDR4 / 40 GB SSD) (id 236121, ssshh) — «покупка хетзнер за рубли»; еще Германия Нюрнберг 6.64€ (id 237298).
- ufo hosting - Россия, МСК Haedus 2CPU/2RAM/40GB NVMe 711р/мес, лимит трафика 232000гб, до 10гбит; на год 3625 по акции (id 236212, vsevolodezz).
- VPSPay DE i9-9900k 5GHz 2.5$ (1 vCPU / 2GB RAM / 30GB) (id 236529).
- OVHcloud 🇵🇱 VPS-2 $7.70 (6 vCPU / 12 GB / 100 GB SSD / 1 Gbit) (id 235735, 🪲).
- serv.host - Швеция Ryzen-9-5950X-0.5 285р (1 ядро 2GB RAM 25GB; st 0; канал 250-500) (id 234729/234648/234694, —/Сергей); Латвия у них тоже 500 мбит (id 237112, Сергей); «каждый вечер бот отправлял сообщение что панель не доступна на минуту» (id 237122, Chill).
- vds.selectel.ru — 200р/мес СПб/МСК (id 228358); 4vps — Москва стала доступна (id 236076, Max R); 4vps ₽ ~4.5€/мес Node Host NL 4.5$ (id 228370, tgshtt).
- 4vps: LTE местами недоступен — армения албания финка, трасса обрубается на шлюзе сотового провайдера (id 235573..235579, Max R); «сразу брутят порты ssh» (id 235592).
- Neksus — подсветок Aeza, «не годится под впн. вынюхивают впн сразу шаманят канал» (id 236550/236553, Zavulon).
- H2nexus: «отвалы начались» (id 227590, whereareyou — из чанка 039). Hostoff: «мощности закончились» (id 233929, Eugene Orefkov); новый блок IP из США — GEO первое время часто как US (id 233951, Max R).
- Bill (biil.ru) и Qwins (qwins.co): «шляпа» — сервера удалили ночью, восстановили 5%, бот валяется, компенсация 2 рубля (id 237033/237043/237056/237060/237079, Zavulon/—). Biil.ru: «в эотumn вообще удалили клиентские сервера без восстановления... компенсации дали 2 рубля... хохлы» (id 237051/237052, —).
- VPSVille: (id 236402) — «поддержка работает» (Фантомас).
- aeza: «все сервера ночью сегодня с аезы отлетели» (id 231275, —); aeza хороша как «отвалы/замедление» (id 235541..235563).
- US: netcup, ufo (id 236140/236141, Black K./A M), 62yun (id 235097).
- АИ, Билайн, Йота, Мегафон, T2: «не работает ЛК по тайм-ауту» (id 235518, Aero) — «Билайн в Ростовской области по ночам тестирует шляпу, ложатся все VPN с ЛК в вебе» (id 236902, Aero) — «Сабку и кабинет надо держать в МСК, где нет ТСПУ» (id 237226, whereareyou). «Мега сама ебланит» (id 231917).

## Инструменты/скрипты
- https://github.com/hteppl/remnawave-cloudflare-nodes (id 235271, Евген) — мониторинг+DNS.
- https://github.com/PEDZEO/remnawave-panel-backup-telegram (id 235014/235027, Pedzeo) — бэкап панели/бота/кабинета в телегу, тестеры приветствуются.
- https://github.com/wrx861/server-shield (id 233139, ALIEN) — «коряво делает авторизацию по ключу, не работает» (id 233146/233147, —); ufw/f2b руками (id 233152, Anton H.).
- https://github.com/wrx861/bedolaga_auto_install (id 237286, ewside) — «старый скрипт» (id 237348, tgshtt), «надо знать что делать перед использованием» (id 237350).
- https://github.com/DonMatteoVPN/TrafficGuard-auto — инсталлятор: `curl -fsSL https://raw.githubusercontent.com/DonMatteoVPN/TrafficGuard-auto/refs/heads/main/install-trafficguard.sh | sudo bash` (id 235475, saveks; команда «rknpidor» 🐈).
- https://github.com/shadow-netlab/traffic-guard-lists (id 235935, Max R) — списки для traffic-guard.
- https://github.com/hxehex/russia-mobile-internet-whitelist/blob/main/cidrwhitelist.txt (id 235351, —) — ЧС мобильного интернета.
- https://4domain.su/ (id 232800, Max R), reg.ru/таймвеб (id 232803, tgshtt), левые данные .com у зарубежного провайдера (id 232804).
- https://blabla.live/?v=1 (id 235891, Евген) — без сведений (id 235893).
- https://paperdraw.dev/ (id 236246, tgshtt) — симулятор проектирования систем (для теоретических проверок, «Factorio для сисадминов»).
- Гайды для проверки сервера (id 237200, из закрепа):
  - IP region: `bash <(wget -qO- https://ipregion.vrnt.xyz)`
  - Censorcheck geoblock: `bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode geoblock`
  - Censorcheck DPI: `bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode dpi`
  - Тест до российских iPerf3 серверов: `bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh)`
  - YABS: `curl -sL yabs.sh | bash -s -- -4`
  - Проверка IP на блокировки: `bash <(curl -Ls IP.Check.Place) -l en`
  - bench.sh: `wget -qO- bench.sh | bash`
  - IPQuality: `bash <(curl -Ls https://Check.Place) -EI`
  - Проверка процента CPU: `sysbench cpu run --threads=1`
- hyperion-cs.github.io/dpi-checkers/ru/tcp-16-20/ (id 237193) — не то (id 237196, Bangtott).
- ДНС айпи мегафона/билайна: id 236065 (—) - хостинг-список ip мегафона; id 236033 (Max R) — новые IP сразу блокируются v4|195.19.122.210|AS44391|ELECTROSVYAZ и v4|85.142.100.12|COMFORTEL-NET.
- «после триггера (напр http://23.251.49.123) на 10 мин блокируется все эти аснки. Лучше не брать у них впс под НОДЫ» (id 236247, Евгений П.) — список ASN: Cogent 174, IONOS 8560, M247 9009, DigitalOcean 14061, OVH 16276, VULTR 20473, GREEN FLOID 21100/204957, Zenlayer 21859, WIIT 24961, INTERKVM 25198, Baxet/JUSTHOST 26383, FDCservers 30058, velia.net 30083, UFO Hosting 33993, Layer7 Networks 35042, IDC Cube 36530, Contabo 40021, Albanian Hosting 48014, VDSINA 48282/216071, AVA HOST 48753, WorldStream 49981, Input Output Flood 53755, HOSTVDS 56971, Scalaxy 58061, CDN77/DataPacket 60068/212238, Clouvider 62240, GTHOST 62563/63023, Dedicated.com 63018, Bage Cloud 63150, HostHatch 63473, Akamai/Linode 63949, Advika 135682, GSL Networks 137409, netcup 197540, ALEXHOST 200019, WorkTitans 209847, Unesty 211301, WAIcore 213887, DePowered 214172, GLOBAL CONNECTIVITY 215540, H2NEXUS 215730, Shift Hosting 394177, Latitude.sh 396356, Global Layer 49453.
- Миграция с другого бота — «в разделе платная поддержка, там мигратор есть» (id 235018/235019, Pedzeo/—).
- Backup/restore: «Bekap каждый час... только в енв меняется» (id 235350, su -) — туда же «включение бекапов» без остальных параметров, потом в ЛК (id 235358, 🪲).
- «Как мигрировать с другого бота правильно?» (id 235016, Nikita Zimens).

## Прочее
- В. Б.: «точно перевести всех на DNS яндекс включая хостинги...» (id 230419 — из 039).
- Пинги: «вк 41мс, яндекс 800» (id 236697, .) — «бс от вк 500-2000 колеблется, у других впн бс мск 500-600» (id 236569, .).
- VPN 500₽ с 1 сервером, Яндекса бс — «конкуренты спокойно продают» (id 236929, V M).
- «РКН начали полностью закрывать VPN на протоколе VLESS» (id 235412/235413, Vlad/КиберТопор) — «Погоди) Vless В С Ё» (id 235991, Евген), «БС от вк на всех операторах работают» (id 235531/235532, Deleted Account/tgshtt).
- «Отвалились мосты с Яндекс до иностранок» (id 237402/235702, Илья З.) — «второй раз ломаются» (id 235702) — «обычная рашка Яндекса обходит бс» (id 235770, —).
- Мегафон сдох (id 235440, DonkyBoss); билайн/мегафон/йота/т2 (id 235727, Deleted Account).
- Роутинг YouTube: domain:youtube.com на ру-сервер — рекламы нет (id 235533/235534/235535, —), полный список доменов YouTube (id 234181, Фантомас): domain:youtube.com, domain:*.youtube.com, domain:googlevideo.com, domain:*.googlevideo.com, domain:ytimg.com, domain:*.ytimg.com, domain:youtubei.googleapis.com, domain:*.youtubei.googleapis.com, domain:youtube.googleapis.com, domain:*.youtube.googleapis.com.
- Роутинг/ YouTube и ru в Эстонии: «в Армении сейчас у ютуба нет монетизации поэтому рекламы не будет» (id 231706, T А).
- Steal time: «0.5 ст до 40% херачит» (id 230026 — из 039), 1cent: «st 30/55-60» (id 234266/234285/234294, Сергей); «ст 0.3 стабильно даже у firstvds» (id 234370, —). «У меня 2 ядра... украло одно с небольшим» (id 234364, Сергей).
- Скорость к серверу через iperf (id 235461, Artesian) — 700-800 по тестам, 10-20 с моего инета — «похоже ркн режет» (id 235461).
- Ирландия (id 236467..236484, . / А M) — хосты малочисленны, UK/п passports.
- IPv6-пряемые DNS 8.8.8.8 на роутере — чинить HWID/вайфай (id 234348, R0xTaDDy).
- «DNS балансировка нода через curl — приложение обновляется 24 часа» (id 235367, Сергей).
- Мосты: у «яндекса» и «вк» есть лимиты? «на ВК нет лимитов» (id 236371/236373, Forward/Илья З.); айпи у ВК: 84, 212, 37 (id 236441, .).
- Реверс-прокси: при polling→webhook бот перестает отвечать (id 235373, Filatov) — «Реверз прокси не настроил» (id 235374, Haxonate).
- HAPP модем: «выпилили, просто не обновлялись» (id 232677/232681/232684/232685, PortVPN Operator/Max R/—).
- HWID: «у пингеров IPv6 выключен» (id 234348) — (id 237247, Тимур).
- yandex, VK, «белые списки»: «парсер чс мобильного интернета» (id 235351).
- «Эстонию хорошую купить» (id 232391/232393, Йоэ) — «финка одно и то же» (id 233829, Zavulon).
- Итог (1 строка): миграции/ошибки после релизов, nginx/caddy для хука и miniapp, DNS/anycast балансировки, РКН блокирует VLESS (слухи/факты), новые хостинги, AES-NI/Steal time, ссылки на скрипты/гайды.
