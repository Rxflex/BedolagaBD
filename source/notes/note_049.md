# Заметки из chunk_049 (id 273684..278178, 16.03.2026 .. 18.03.2026)

## Блокировка oauth.telegram.org / авторизация в кабинете (веха 16.03.2026)
- **[id=274237|Djingle|16.03.2026](https://t.me/c/2941121338/274237)** В РФ заблокирован oauth.telegram.org — страница авторизации кабинета висит в pending. Кабину ставят на EU VPS — не помогает, т.к. обращения идут на серверы Telegram с клиента. Решения: прокси telegram-web-app.js, deep link auth (см. v3.33.0).
- **[id=274193|Djingle|16.03.2026](https://t.me/c/2941121338/274193)** Фикс загрузки кабинета без VPN — проксирование telegram-web-app.js через Caddy (дословно):
  ```
  # качаешь себе на vps файл https://telegram.org/js/telegram-web-app.js
  # добавляешь в caddyfile блок для проксирования:
  # Прокси для заблокированных в РФ ресурсов
      handle /proxy/telegram-web-app.js {
          reverse_proxy https://telegram.org {
              header_up Host telegram.org
              rewrite /js/telegram-web-app.js
          }
      }
  # Пересобираем Caddy. Вносим изменения в index:
  sed -i 's|https://telegram.org/js/telegram-web-app.js|/proxy/telegram-web-app.js|g' /opt/bedolaga-cabinet/cabinet-dist/index.html
  ```
  Кнопка авторизации в ТГ становится активна через 10–30 сек после открытия страницы.
- **[id=275223|Alexy|16.03.2026](https://t.me/c/2941121338/275223)** Самостоятельный selfhost-зеркало tg-js: редактирование tg js + fallback предзагрузки снимает зависший pending (задержки с 800мс/3сек упали до 20–100мс), но этап подтверждения авторизации клиентом в ТГ не фиксится никак — нужен альтернативный вход (OIDC google/yandex).
- **[id=277027|Egor|18.03.2026](https://t.me/c/2941121338/277027)** Bedolaga Bot v3.33.0 (дословно, ключевые пункты):
  - RioPay в кабинете — пополнение, лендинги, подарки; KassaAI суб-опции СБП/Карта;
  - Deep link авторизация — вход в кабинет через Telegram-бота, когда oauth.telegram.org заблокирован; одноразовая ссылка;
  - Fix: конверсия в статистике (0% при оплативших), фантомные пользователи при покупке с лендинга (мерж при /start), уязвимость выбора серверов из чужих промо-групп, Caddy перепутанные заголовки api_key/caddy_token, MissingGreenlet после покупки подписки/изменения устройств на CLASSIC, синхронизация сквадов при покупке/смене тарифа, плашка верификации email скрыта при CABINET_EMAIL_VERIFICATION_ENABLED=false, Tribute webhook миграция user_id → trb_user_id, NameError в продлении.
  - Bedolaga Cabinet v1.35.0: Deep link auth (fallback через бота; таймаут 8 сек на виджет, затем polling каждые 2.5 сек).

## Обновление бота/кабины (пути миграций)
- **[id=274071|tgshtt|16.03.2026](https://t.me/c/2941121338/274071)** Старые версии (<3.15.1) обновлять сначала до 3.15.1 (там прошла миграция БД на Alembic), потом на ласт. Пропущенные миграции 3.0.0–3.15.1 ломают БД.
- **[id=276660|tgshtt|17.03.2026](https://t.me/c/2941121338/276660)** Команды обновления:
  ```
  cd /root/remnawave-bedolaga-telegram-bot
  git pull origin main          # до последней версии (main ветка)
  git fetch --tags && git checkout v2.7.0   # до конкретной версии
  make reload
  ```
- **[id=277955|Konstantin|18.03.2026](https://t.me/c/2941121338/277955)** Обновление кабинета:
  ```
  cd /opt/bedolaga-cabinet && git pull origin main && docker compose down && docker compose up -d --build
  ```
- **[id=274406|Николай|16.03.2026](https://t.me/c/2941121338/274406)** Полный набор команд обновления кабинета (дословно):
  ```
  rm -rf /root/bot/bedolaga-cabinet/cabinet-dist && rm -rf /opt/remnawave/nginx/cabinet && cd /root/bot/bedolaga-cabinet/ && git pull && docker compose build && docker create --name tmp_cabinet bedolaga-cabinet-cabinet-frontend && docker cp tmp_cabinet:/usr/share/nginx/html ./cabinet-dist && docker rm tmp_cabinet && cp -r /root/bot/bedolaga-cabinet/cabinet-dist/ /opt/remnawave/nginx/cabinet
  ```
- **[id=276112|.da|17.03.2026](https://t.me/c/2941121338/276112)** Все docker-compose (ремна/бот/кабина/nginx) должны иметь одну и ту же docker-сеть; порядок запуска: панель → сабка → бот → nginx.
- **[id=276169|Super U.|17.03.2026](https://t.me/c/2941121338/276169)** Баг бота с Caddy-авторизацией панели (docs.rw caddy-with-custom-path): REMNAWAVE_AUTH_TYPE=caddy + CADDY_TOKEN из 2FA → 401; в коде бота Authorization/X-Api-Key перепутаны местами (починено в 3.33.0).
- **[id=275679|Конфликт портов](https://t.me/c/2941121338/275679)** Панель+бот+кабинет на одном сервере: ремна занимает 443, кабинету брать 8443; панель не ставить туда же где нода — при неверном xray-конфиге пропадёт доступ к панели.

## Ошибки Bedolaga и фиксы
- **[id=274166+|MissingGreenlet](https://t.me/c/2941121338/274166)** Много жалоб (16–17.03): `MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here` в app.middlewares.auth при покупке/продлении/докупке устройств (v3.32.x, CLASSIC). Починено в 3.33.0.
- **[id=274184|Maxdep|16.03.2026](https://t.me/c/2941121338/274184)** `[error] select_tariff_extend_period NameError("name 'group_pct' is not defined")` + `TelegramBadRequest: message to delete not found` при оплате через Platega — тоже фикс в 3.33.0.
- **[id=275860|Бехзод Ю.|16.03.2026](https://t.me/c/2941121338/275860)** Баг: при MAIN_MENU_MODE=cabinet кнопки в уведомлениях не конвертируются в WebApp (InlineKeyboardButton вместо build_miniapp_or_callback_button в subscription_auto_purchase_service.py, payment/yookassa.py, payment/stars.py, daily_subscription_service.py — 26 мест). Фикс: заменить на build_miniapp_or_callback_button из app.utils.miniapp_buttons.
- **[id=275973|Бехзод|16.03.2026](https://t.me/c/2941121338/275973)** Меню не берётся из БД: в .env надо `MENU_LAYOUT_ENABLED=true` + рестарт; иначе бот берёт дефолтную раскладку из кода.
- **[id=276994|Egor N.|18.03.2026](https://t.me/c/2941121338/276994)** Триал не выдаёт сквад по промокоду: trial использует только сквады с `is_trial_eligible = true` в БД (при is_available=true, is_trial_eligible=false сквад не выбирается).
- **[id=274260|tgshtt|16.03.2026](https://t.me/c/2941121338/274260)** Ошибка "бот не может узнать errorlog" — бесконечные падения при несуществующем errorlog.
- **[id=274997|Пустой|17.03.2026](https://t.me/c/2941121338/274997)** Nalogo curl 200, но чеки не приходят — забыли перезапустить контейнер после обновы.
- **[id=277219|18.03.2026](https://t.me/c/2941121338/277219)** Platega минималка: `PLATEGA_MIN_AMOUNT_KOPEKS=10000` (100 ₽) в .env режет пополнения от 1–9 ₽ с ошибкой react-валидации.
- **[id=277401|Васян|18.03.2026](https://t.me/c/2941121338/277401)** PLATEGA_RETURN_URL: ставь либо на бот, либо на кабинет — иначе web-клиенты после оплаты редиректятся в ТГ на пустой акк.

## Каскады, сквады, балансировка
- **[id=275514|Sergey|16.03.2026](https://t.me/c/2941121338/275514)** Роутинг «RU→EU через прокси»: отдельный шаблон xray json, в хостах присваиваешь шаблон нужному хосту. Пример routing-шаблона (полный трафик через прокси, кроме geoip:ru direct... фактически приведён шаблон: private→direct, geoip:ru→proxy, остальное direct).
- **[id=276022|Неизв.|16.03.2026](https://t.me/c/2941121338/276022)** Блокировка рекламы YouTube: в routing добавить `domainStrategy: UseIPv4` + домены youtube.com, ytimg.com, yting.com, ggpht.com, googlevideo.com, youtubekids.com, youtu.be, yt.be, youtube-nocookie.com, wide-youtube.l.google.com, ytimg.l.google.com, youtubei.googleapis.com, youtubeembeddedplayer.googleapis.com, youtube-ui.l.google.com, yt-video-upload.l.google.com, jnn-pa.googleapis.com, returnyoutubedislikeapi.com, yt3.googleusercontent.com. Тикток — через geosite:tiktok (github.com/hydraponique/roscomvpn-geosite).
- **[id=275133|Мультитысячник|16.03.2026](https://t.me/c/2941121338/275133)** Весь Google на RU-сервер: `geosite:google, geosite:youtube, geoip:google → RU` — ютуб работает, минус: не работает Gemini (лечится WARP).
- **[id=276618|tgshtt|17.03.2026](https://t.me/c/2941121338/276618)** Автовыбор ноды в ремне работает по стратегии leastping (клиентский xray json) — подключение на меньший пинг; есть leastload, но работает не супер; «самый норм балансер — xray json клиентский».
- **[id=274045|Ramil M.|16.03.2026](https://t.me/c/2941121338/274045)** Схема сквадов: хост-balancer (авто) с тегами выдаёт инбаунды только тех сквадов, что у пользователя; балансировка между сквадами с общим тегом — только при наличии обоих сквадов у юзера.
- **[id=276768|Valerii B.|17.03.2026](https://t.me/c/2941121338/276768)** Собственный CLI: WireGuard (туннель, 10.66.64.0/21) + Xray dokodemo-door (порт 12345, REDIRECT для TCP, TPROXY для UDP) + per-client VLESS/REALITY outbounds из squads.json; remna_mapping.json — реестр (username, UUID, squad_id, IP, pubkey); горячая перезагрузка Xray сигналом SIGUSR1 без разрыва соединений; wg show опрос каждые 2 сек; Remnawave через API только для списка юзеров/UUID; трафик считается по кэфу нод.

## БС (белые списки) и хостинги
- **[id=276066|yng dev Zover|17.03.2026](https://t.me/c/2941121338/276066)** Яндекс-клад быстрый метод бс-теста: сни `www.vk.com` на IP 84.201.166.166 (публичный с парсинга ключей).
- **[id=276306|PinkHead|17.03.2026](https://t.me/c/2941121338/276306)** Подсети Yandex Cloud (AS200350): 51.250.0.0/17 (Билайн, ТМоб, МТС, Yota, Мегафон, Т2), 84.201.128.0/18 (T2, ТМоб), 158.160.0.0/16 (T2), 5.255.193.0-3. На практике почти везде работает только 51.250 (id=277890). Проверять надо конкретный IP, а не AS.
- **[id=276316|Hidden|17.03.2026](https://t.me/c/2941121338/276316)** Чекер на БС: https://hyperion-cs.github.io/dpi-checkers/ru/ipv4-whitelisted-subnets/ (Cache через обычный интернет, Check через мобильный). Мануал: https://hyperion-cs.github.io/dpi-checkers/
- **[id=277076|Александр Kus Karas'|18.03.2026](https://t.me/c/2941121338/277076)** Списки БС на GitHub: https://github.com/hxehex/russia-mobile-internet-whitelist ; https://github.com/zieng2/wl/blob/main/vless_universal.txt (обновляется каждый час); https://github.com/igareck/vpn-configs-for-russia
- **[id=276100|R0xTaDDy|17.03.2026](https://t.me/c/2941121338/276100)** Продавец БС-IP: majordomo (выкуплены 2 подсети); selectel — дедики, не все операторы; yandex/vk — бесплатно.
- **[id=274086|Djingle|16.03.2026](https://t.me/c/2941121338/274086)** Кабинет/авторизация полдня грузится на RU VPS → переносят на EU (Германия/Нидерланды), но реальная причина — блокировки ТГ-скриптов.
- **[id=276824|276828|Reyды VK Cloud 18.03](https://t.me/c/2941121338/276824)** VK Cloud ночью 18.03: floating IP снесены без уведомлений, массово отбирают БС-IP и аккаунты физлиц (пункт 6.2 ToS, ГРЧЦ жалобы), закрыли регистрацию для физлиц; причины «подозрительная активность по перебору IP-адресов». Yandex: таскер перегружен, IP бить по 500 траев, регистрацию тоже ограничили (юрлицо). 84.201 в БС частично.
- **[id=276868|yng dev Zover|17.03.2026](https://t.me/c/2941121338/276868)** Местоположение Ютуб-гео зависит от аккаунтов, сидевших с ноды: много UA-акков → Google отдал UA-гео.
- **[id=274837|V M|16.03.2026](https://t.me/c/2941121338/274837)** AdminVPS Германия (185.237.x.x) штормит 16–17.03; 4vps ру разобрали; p2go аварии 3 за сутки, поддержка игнорирует (ddos).
- **[id=276548|Popugtop|17.03.2026](https://t.me/c/2941121338/276548)** Реселл Hetzner @vibehost_bot (Финляндия): 2vCPU/4GB/40GB NVMe, $4.95/мес, диск 1.2–1.3 GB/s, 5 Gbit; минус — подсеть забанена в РФ, нода только мостом.
- **[id=275968|Димeнтий|17.03.2026](https://t.me/c/2941121338/275968)** it-garage.pro Финляндия 1vCPU/2GB/1Gbit 3.6€/мес.
- **[id=274890|Влад|17.03.2026](https://t.me/c/2941121338/274890)** hostvds USA (Канзас) Burstable-2: $1.99/мес 1CPU/2GB/20GB NVMe/1Gbit/1TB.
- **[id=275135|Фамиль|16.03.2026](https://t.me/c/2941121338/275135)** intezio.net Польша Ubuntu 24.04, 2×Ryzen 9 5950X, 4GB, 64GB NVMe — 550₽. (intezio в т.ч. Эстония 2 дня лежит 18.03 id=277320.)
- **[id=276003|yng dev Zover|17.03.2026](https://t.me/c/2941121338/276003)** freckhosting: 4.5€ 3 ядра/4GB/100GB SSD, 10Gbit канал (реально 2–5); узел мигрируют при проблемах. Аеза СПб: 7€ 1 ядро/4GB, 25 Гбит, стабильна.
- **[id=277620|18.03.2026](https://t.me/c/2941121338/277620)** Массовые магистральные сбои 16–18.03 в Европе: финка/шведы/Германия/Нидерланды прыгают у всех хостеров (play2go, frikhosting, adminvps) — потери на немецком хабе; mtr показывает маршрут.

## Анти-скан / ТСПУ-зашита
- **[id=276623|277810](https://t.me/c/2941121338/276623)** TrafficGuard (https://github.com/dotX12/traffic-guard, авто-инсталлер https://github.com/DonMatteoVPN/TrafficGuard-auto) — банит подсети ГРЧЦ/РКН; тони: работает по сканам гос.подсетей, ставят и на ноды, и на панель.
- **[id=277955|277960](https://t.me/c/2941121338/277955)** Crowdsec (https://www.crowdsec.net/), beszel (https://beszel.dev/) — мониторинг/защита.
- **[id=274950|Zavulon|16.03.2026](https://t.me/c/2941121338/274950)** Сканеры не блочит — вк/яндекс сносят итак; у вк отбирают даже неиспользованные IP по жалобам ГРЧЦ (см. выше).

## Инструменты/ссылки
- **[id=273969|BedolagamNaPivoBot](https://t.me/c/2941121338/273969)** Репозитории: remnawave/panel, BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot, BEDOLAGA-DEV/bedolaga-cabinet, kutovoys/xray-checker, eGamesAPI/remnawave-reverse-proxy, Jolymmiels/remnawave-telegram-shop, machka-pasla/remnawave-tg-shop, DigneZzZ/remnawave-scripts, distillium/remnawave-backup-restore, maposia/remnawave-telegram-sub-mini-app, legiz-ru/my-remnawave, dotX12/traffic-guard.
- **[id=277195|MAKS|17.03.2026](https://t.me/c/2941121338/277195)** Бэкап бота: скрипт «капибары» (DigneZzZ/remnawave-scripts) — бекап/восстановление; distillium/remnawave-backup-restore для панели (id=277330|Egor).
- **[id=274368|Max R|16.03.2026](https://t.me/c/2941121338/274368)** Репозиторий ID нежелательных юзеров для VPN с интеграцией в Бедолагу: https://raw.githubusercontent.com/Blin4ickUSE/ban-vpn/refs/heads/main/blacklist.txt (обновлять раз в 60 минут).
- **[id=277925|Case211|18.03.2026](https://t.me/c/2941121338/277925)** remnawave-admin v2.7.4: фактический трафик без множителей нод, вкл/выкл ноды, аналитика по нодам. github.com/Case211/remnawave-admin.
- **[id=277974|Egor|18.03.2026](https://t.me/c/2941121338/277974)** Changelog v3.34 (скоро): интеграция SeverPay (API с HMAC-SHA256, вебхуки, гостевые покупки), поиск платежей по 13 провайдерам с ILIKE; RioPay/SeverPay добавлены в REAL_PAYMENT_METHODS; кнопка устройств disabled при достижении лимита.
- **[id=277830|Max R|17.03.2026](https://t.me/c/2941121338/277830)** Официальное партнёрство Бедолаги с WATA (платёжка): промокод bedolaga → бесплатное подключение.

## Разное
- **[id=273974|Max R|16.03.2026](https://t.me/c/2941121338/273974)** Tribute Webhook API: поле `user_id` deprecated, удалено 14.04.2026 → использовать `trb_user_id`.
- **[id=274411|Alexy|16.03.2026](https://t.me/c/2941121338/274411)** Кабина: смена кнопок в главном меню — нужна настройка темы в кабинете, но не всех кнопок в рассылке (локаль).
- **[id=275390|16.03.2026](https://t.me/c/2941121338/275390)** Прокси для ТГ без VPN: MTProto (mtg) накручивается на отдельный промо-сервер, чистится админкой, режет соединение после 24ч юза. R0xTaDDy раздал mtproxy всем бесплатно.
- **[id=275340|Мультитысячник|16.03.2026](https://t.me/c/2941121338/275340)** socks-прокси ТГ одним кликом: `https://t.me/socks?server=IP&port=PORT&user=user&pass=pass` в кнопку index.html лендинга.
- **[id=274548|Popugtop|16.03.2026](https://t.me/c/2941121338/274548)** Фейк-гео ЮТуб на РУ-сервере: если с РУ-сервера идёшь на евро, оставить трафик ютуба на РУ (не реклама), остальное в европу (правила в xray json).
- **[id=276558|Николай|17.03.2026](https://t.me/c/2941121338/276558)** Трафик и кэф: кэф 0.0 в ремне — БС-нода без лимита юзера; трафик учитывается только с нод кэф >0 (только в статистику ноды). Дропать старый трафик при переключении на БС.
- **[id=277927|Кирилл "Lucifer"|18.03.2026](https://t.me/c/2941121338/277927)** Продление тарифа: +30 дней от даты продления, а не истечения подписки — запрос фичи.
- **[id=277625|Аезовская интригушечка](https://t.me/c/2941121338/277625)** РКН-жалобы и массовые отборы IP на ВК/Яндексе при переборе подсетей: сильно фродят новые рега, акки банили за "подозрительную активность" (5к верификационный платёж, привязку карты).
- **[id=277682|Миша ту-ту|17.03.2026](https://t.me/c/2941121338/277682)** «Бурст» на 50 юзерах: юзеры с 200₽/мес безлимитом под БС — экономика минус (2₽/ГБ Яндекса); рекомендация — лимит 30–40 ГБ, докупка.
- **[id=278013|18.03.2026](https://t.me/c/2941121338/278013)** Телега замедляется по гео даже через ВПН (ру-впс хосты) — скорее сам Дуров под ТСПУ нагружается мусорными запросами (спекуляция, не подтверждено).
