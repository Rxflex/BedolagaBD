# Заметки из chunk_042 (id 241921..247086, 25.02–28.02.2026)

## Remnawave Bedolaga Bot — релизы 25–28.02
- **[id=242001|Egor|25.02]** Bedolaga Bot v3.20.0: Freekassa раздельные методы (СБП/QR payment_system_id=44, Карты РФ i=36); валидация API фонов; фиксы auto-sync 404, FK при удалении юзера, DEVICES_SELECTION_DISABLED_AMOUNT=0, import structlog.
- **[id=242005|Egor|25.02]** Cabinet v1.22.0: 14 анимированных фонов (Aceternity UI), редизайн дашборда, светлая тема, Google Fonts preconnect, dashboard eagerly.
- **[id=242437|Egor|25.02]** Bot v3.20.1: суточные подписки не продлевались (race condition MonitoringService/DailySubscriptionService), идемпотентные миграции 0010/0011, HTML-escape.
- **[id=244332|Egor|27.02]** Дока переехала на docs.bedolagam.ru (актуализируется вместе с релизами); quickstart на пуле за минуту.
- **[id=243451|Дмитрий|26.02]** Remnawave Panel v2.6.2+: просмотр/удаление пользовательских сессий с нод; для NET_ADMIN-функций в docker-compose ноды: `cap_add: [NET_ADMIN]` (Remnawave Node 2.6.0+); при превышении лимита трафика юзер удаляется из Xray, но старые сессии висят — NET_ADMIN решает (сессии последних 20 секунд).
- **[id=242926|Max R|25.02]** Panel v2.6.4 hotfix: Mihomo + hidden hosts, Xray-Json Advanced addVirtualHostAsOutbound.

## Bedolaga: настройка/эксплуатация (команды)
- **[id=245593|Egor|28.02]** Бэкап/восстановление БД бота:
  ```bash
  docker exec remnawave_bot_db pg_dump -Fc -U postgres remnawave_bot > backup_$(date +%Y%m%d_%H%M%S).dump
  docker exec -i postgres pg_restore -U postgres -d remnawave_bot --clean --if-exists < backup_XXXXXXXX_XXXXXX.dump
  ```
- **[id=244878|Egor|27.02]** Права для томов бота:
  ```bash
  mkdir -p ./logs ./data ./data/backups ./data/referral_qr
  chmod -R 755 ./logs ./data
  sudo chown -R 1000:1000 ./logs ./data
  ```
- **[id=243644|Дмитрий|26.02]** Полная пересборка кабинета без кеша:
  ```bash
  docker builder prune -a -f && docker compose down && docker compose build --no-cache && docker compose up -d && docker compose logs -f
  ```
- **[id=242786|mah1cul|25.02]** Обновление бота: «make down → git pull origin main → make up-follow»; порядок миграций: с 2.9.3 → 3.14 → 3.15.1 (миграция на Alembic) → ласт; с 3.7.0 на 3.18 лезть нельзя.
- **[id=244963|Prokurátura|27.02]** Версии с алембиком: 3.11/2.9.3 → обновляться поэтапно (3.14 → 3.15.1 → ласт), иначе «снежинки» БД.
- **[id=242911|Mah1cul|25.02]** `.env.example` — это просто шаблон, не трогать; все важное в `.env`.
- **[id=244061|tgshtt|27.02]** Приоритет переменных: `.env` > админка. Если настройку нужно редактировать в админке — удалить её из `.env`.
- **[id=244801|—|26.02]** ЛК-редактирование не конфликтует с `.env`, пока настройка не прописана в env.
- **[id=244013|tgshtt|25.02]** Реф-ссылки в кабинете через Telegram id+username; в чёрный список «id+username в топик черный список» (бот репорты).
- **[id=243586|Whiteness|25.02]** 4vps раскупили (завоз), армения/албания — «не особо».
- **[id=242716|Whiteness|25.02]** Weasel.cloud (1cent) — Польша 4$/мес 2/2/30/100Mbit (гарант 100). Под ноды из-за гаранта низкого не рекомендую, под бота/сабку ок.
- **[id=243574|tgshtt|25.02]** MHost GB 4€ (2/2/30/3Gbit) — «канал вроде бодрый, под ноду пойдёт», гео-айпи солянка.
- **[id=244445|tgshtt|27.02]** MHost GB 4€ (1/2/30/3Gbit) — «AES-NI выключен (включают по тп), гео-айпи пизда, под ютуб норм, в остальном сомнительно».
- **[id=242317|—|25.02]** u1host.com NL-5950X-1 429₽ (1/2/30 NVMe), IPv6 выкл, BBR вкл.
- **[id=242642|Prokurátura|25.02]** qwins.co EE 5$ (1/2/30/1Gbit) — «думайте сами».
- **[id=242766|MAKS|25.02]** YeezyHost SE 3.6$ (1/2/30) — «под ноду пойдёт».
- **[id=242970|Whiteness|26.02]** Midas_Hosting NL Амстердам 5€ (1/2 DDR5/30/5Gbit) — «работает очень хорошо», поддержка оперативная.
- **[id=243090|MAKS|26.02]** YeezyHost NL 3.6$ (1/2/30 NVMe 1Gbps), оплата крипта/LZT, AES-NI выключен (включают через тп).
- **[id=243097|MAKS|26.02]** AEZA опустила цены после блоков; x10 на нодах.
- **[id=243188|MAKS|26.02]** c0mrade: AEZA = «куклы» (после бана с блоченными айпишниками).
- **[id=243230|Михаил|26.02]** hyper.hosting «Яша ворует трафик» — депосит 4к.
- **[id=243679|Max R|26.02]** 4vps AES-NI «включается по тп», на 4vps РКН банит ноды.
- **[id=244070|Max R|26.02]** «4vps на 4vps МСК 3 день».
- **[id=244070|MAKS|26.02]** «в 4vps раскупили всё, орвис».
- **[id=244070|Whiteness|26.02]** Midas/4vps — из минусов у мидасов «AES-NI».
- **[id=244072|MAKS|26.02]** asdhere ФИ Хельсинки 8€ (1/2 DDR5/30/10Gbit), промо GREE№ — 50% на 1 сервер.
- **[id=244120|Max R|26.02]** Макс сказал «точно так».
- **[id=244290|Prokurátura|27.02]** ASHRC (whitelist сканеров).
- **[id=244290|MAKS|27.02]** doubleservers 10,26€ CA Beauharnois (4/8/75GB NVME) — «во всех геобазах отображается как нужно».
- **[id=244311|tgshtt|26.02]** Waicore letters о повышении цен (на продление тоже), 6€ вместо 4€.
- **[id=244400|MAKS|27.02]** hshp.host FI-RZ-1 350₽ (1/2/32 NVMe 500mb port) — «вроде норм но хз».
- **[id=244438|MAKS|27.02]** 4vps AU Австралия 770₽ (2/4/25/2Gbit) — «айпишник грязноват», ютуб бьётся как РФ (фикс варпом), канал 1 гбит.
- **[id=244430|MAKS|27.02]** Warpx 250₽ (Старт), «скорости чуть меньше гига, айпи чистый, steal 0».
- **[id=244450|MAKS|27.02]** AlexHost MD/NL/BG/CH/FR/GB/RO 10€ (2/4/40/1Gbit) — «более года, нареканий нет».
- **[id=244457|Nick|27.02]** U1host.com NL 429₽ (1/2/30 NVMe), AES-NI выключен.
- **[id=245056|MAKS|27.02]** doubleservers DE Нюрнберг 8.37€ (2/4 DDR5/40/10Gbit) — «мега стабильный Hetzner», «нужен мост».
- **[id=246003|ssshhh|28.02]** doubleservers FI Хельсинки 47.57€ (16/32 DDR4/320 SSD) — «канал отличный».

## Remnawave: настройка + решения (сборка)
- **[id=242299|tgshtt|25.02]** «Синхронизация пользователей из панели» в кабинете: Настройки → Remnawave → синхронизация.
- **[id=242437|Egor|25.02]** Remna v2.6.4: Xray-Json Advanced, удаление user-сессий.
- **[id=242475|Egor|25.02]** «В прилы зайди в админке конфиг выбери» — конфигурация приложений в кабинете.
- **[id=242439|Александр|25.02]** Тесты с конфигами: vless+reality / xhttp+reality / xhttp+cloudflare / xhttp+nginx на Waicore Фин+ASD Германия — при скорости >200 Мбит ТСПУ рвёт; vless+reality не рвёт. «Под массовое использование xhttp не подходит, ТСПУ видит огромный трафик сразу режет».
- **[id=242801|tgshtt|25.02]** «IPv6+BBR» как настройка нод.
- **[id=242879|Aero|25.02]** VLESS+REALITY порт 7443 (инбаунд):
  ```json
  {
    "log": { "loglevel": "none" },
    "inbounds": [{
      "tag": "VLESS_TCP_REALITY7443",
      "port": 7443, "listen": "0.0.0.0", "protocol": "vless",
      "settings": { "clients": [], "decryption": "none" },
      "sniffing": { "enabled": true, "destOverride": ["http","tls","quic"] },
      "streamSettings": {
        "network": "raw", "security": "reality",
        "realitySettings": {
          "show": false, "xver": 0,
          "target": "yandex.ru:7443",
          "shortIds": [""],
          "privateKey": "-",
          "serverNames": ["yandex.ru", "www.yandex.ru"]
        }
      }
    }],
    "outbounds": [
      { "tag": "DIRECT", "protocol": "freedom" },
      { "tag": "BLOCK", "protocol": "blackhole" }
    ],
    "routing": { "rules": [
      { "ip": ["geoip:private"], "type": "field", "outboundTag": "BLOCK" },
      { "type": "field", "domain": ["geosite:private"], "outboundTag": "BLOCK" },
      { "type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK" }
    ]}
  }
  ```
  Разбор ошибки (Aero|25.02): «домен надо оставлять 443, а везде заменил на 7443» — в конфиге target указывают SNI (yandex.ru:7443) + ufw allow 7443.
- **[id=244007|Tatoxa|25.02]** Xray-конфиг (клиентский, socks 10808/http 10809, queryStrategy UseIPv4, routing IPIfNonMatch):
  ```json
  {
    "dns": { "servers": ["77.88.8.8","1.1.1.1","1.0.0.1"], "queryStrategy": "UseIPv4" },
    "log": { "loglevel": "warning" },
    "routing": { "rules": [
      { "type": "field", "protocol": ["bittorrent","quic"], "outboundTag": "direct" },
      { "type": "field", "network": "tcp,udp", "outboundTag": "proxy" }
    ], "domainStrategy": "IPIfNonMatch" },
    "inbounds": [ socks 10808 / http 10809 ],
    "outbounds": [ direct/freedom, block/blackhole ]
  }
  ```
- **[id=244529|Name Lastname|27.02]** SelfSteal (Caddy на той же ноде):
  ```caddy
  {
      https_port {$SELF_STEAL_PORT}
      default_bind 127.0.0.1
      servers { listener_wrappers { proxy_protocol { allow 127.0.0.1/32 } tls } }
      auto_https disable_redirects
  }
  http://{$SELF_STEAL_DOMAIN} { bind 0.0.0.0; redir https://{$SELF_STEAL_DOMAIN}{uri} permanent }
  https://{$SELF_STEAL_DOMAIN} { root * /var/www/html; try_files {path} /index.html; file_server }
  :{$SELF_STEAL_PORT} { tls internal; respond 204 }
  :80 { bind 0.0.0.0; respond 204 }
  ```
  .env: `SELF_STEAL_DOMAIN=subdomen.domen.ru`, `SELF_STEAL_PORT=9443`; docker-compose с `network_mode: "host"`, volume `../html:/var/www/html`.
- **[id=244534|—|27.02]** SelfSteal: «IP в DNS для адреса SNI совпадает с IP сервера, сертификат валидный».
- **[id=244902|Tatoxa|28.02]** Мост (мск↔еу): «через мост idre...»
- **[id=244557|Prokurátura|26.02]** «ДаблVPN» (RU-сервер → ЕУ-нода).
- **[id=244549|Чар|27.02]** МСК + ЕУ мост (retzor) — «через Retzor».
- **[id=244919|MAKS|27.02]** «Дешёвый РФ хостинг под мост: Apexnodes, One dash».
- **[id=244921|—|27.02]** Дешёвые RU под мост: 4vps, beget.com (1 Гбит, нет ТСПУ).
- **[id=243451|Дмитрий|26.02]** Remna v2.6.2+: Node NET_ADMIN (`cap_add: [NET_ADMIN]`) — обрыв сессий юзеров.

## ТСПУ / хосты (морские хосты с ТСПУ)
- **[id=243066|tgshtt|25.02]** «Z4R есть на сервере?» — вопрос «запрет на сервер поставил?»
- **[id=243069|tgshtt|25.02]** Zapret4rocket (ДонМаттео): https://github.com/IndeecFOX/zapret4rocket
- **[id=243082|—|25.02]** Сканеры 24/7 от РКН; eGames Reverse Proxy как маскировка:
  **[id=246222|makdren|28.02]** https://github.com/eGamesAPI/remnawave-reverse-proxy
- **[id=243084|MAKS|25.02]** «Ovh» (защита «Хетцнер в РФ»).
- **[id=243548|Whiteness|26.02]** netcup — «тспу страшно душит».
- **[id=243083|tgshtt|25.02]** «Xray-конфиги + скрытие».

## ТСПУ / zapret / ДПИ-обход (мет. работы)
- **[id=242716|Дмитрий|26.02]** Zapret4rocket на ноду (РКН обходит).
- **[id=243059|Whiteness|26.02]** «Youtube Premium NO» = «нет рекламы».
- **[id=243987|Max R|28.02]** GitHub: DanielLavrushin/tspu-docs (читабельная доки по ТСПУ).
- **[id=242716|Max R|26.02]** «Написал ру сервер, в приложении ок, в браузере вообще не грузит» (Владимир). «На ноду уеби zapret4rocket» (tgshtt).
- **[id=243082|tgshtt|25.02]** «z4r — запрет на сервере, 8 раз Enter».

## РКН-белые IP (VK)
- **[id=243074|Владимир|25.02]** «Ловлю белые ip, если кому надо, в ВК Клауде» (валера/Владимир).
- **[id=243077|Владимир|25.02]** «На ВК клауде ВМ, с утра умирает а днем все збс» (Don’t care).

## Remnawave: панель/ноды/фичи (новое)
- **[id=242771|Дмитрий|26.02]** Remnawave Panel v2.6.2+ Node NET_ADMIN.
- **[id=244075|Prokurátura|26.02]** «Remnawave Node 2.6.2».
- **[id=244085|tgshtt|26.02]** «отключить из меню приветственного триала».
- **[id=244100|Дмитрий|26.02]** Netcup «тспу страшно душит».
- **[id=244077|MAKS|26.02]** midas/vps+use « AES-NI выключен по умолчанию».
- **[id=244088|Whiteness|26.02]** «1cent.host EE 180₽ (1/1/10GB/1Gbit), IPv6 вкл, BBR вкл» — дубль.
- **[id=244545|MAKS|27.02]** «YeezyHost».

## Remnawave/Bedolaga: обновления 25–28.02 (сводно)
- **[id=242001/242005|Egor|25.02]** Bot v3.20.0 / Cabinet v1.22.0.
- **[id=242437|Egor|25.02]** Bot v3.20.1.
- **[id=243451|Дмитрий|26.02]** Remnawave Panel v2.6.2+, Node v2.6.0+ NET_ADMIN.
- **[id=244332|Egor|27.02]** Дока на docs.bedolagam.ru.
- **[id=244077|MAKS|26.02]** «AES-NI выключен» (midas/4vps/yeezy).
- **[id=244075|Prokurátura|26.02]** «Remnawave Node 2.6.2».

## Remnawave/Bedolaga: обновления (из прежних чанков, консолидировано)
- **[id=238585|MAKS|23.02]** nodehost NL 1/2/15GB 10Gbit 2.85$ — «не советую».
- **[id=238646|Whiteness|23.02]** 1cent EE 180₽ — дубль.
- **[id=238528|MAKS|23.02]** Midas GB 4€ — дубль.

## Панелька c URL для мини-аппки
- **[id=244875|Дмитрий|28.02]** «В ссылку ставить только домен, без ключа в ссылке и в конце не должно быть /»: `https://admin.domen.site` — REMNAWAVE_API_URL.

## Кабина (сборка)
- **[id=245525|—|28.02]** Скрипт патча юзернейма бота в статике (скрипт для «Telegram бот не настроен»):
  ```bash
  #!/bin/bash
  CONFIG_FILE="./.cabinet_config"
  if [ -f "$CONFIG_FILE" ]; then
      SAVED_USERNAME=$(cat "$CONFIG_FILE")
      echo ">>> Найден сохранённый юзернейм: $SAVED_USERNAME"
      read -p ">>> Использовать его? (Enter = да, или введи новый): " INPUT_USERNAME
      BOT_USERNAME="${INPUT_USERNAME:-$SAVED_USERNAME}"
  else
      read -p ">>> Введи юзернейм бота (без @): " BOT_USERNAME
  fi
  echo "$BOT_USERNAME" > "$CONFIG_FILE"
  if [ ! -f "./docker-compose.yml" ]; then
      cat > ./docker-compose.yml << 'COMPOSE'
  services:
    cabinet-frontend:
      image: ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
      container_name: cabinet_frontend
      restart: unless-stopped
      env_file:
        - .env
      ports:
        - '${CABINET_PORT:-3020}:80'
      volumes:
        - ./cabinet-dist:/usr/share/nginx/html:ro
      networks:
        - remnawave_bot_network
  networks:
    remnawave_bot_network:
      external: true
  COMPOSE
  fi
  if [ ! -f "./.env" ]; then echo "CABINET_PORT=3020" > ./.env; fi
  docker pull ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
  docker create --name tmp_cabinet ghcr.io/bedolaga-dev/bedolaga-cabinet:latest
  rm -rf ./cabinet-dist
  docker cp tmp_cabinet:/usr/share/nginx/html ./cabinet-dist
  docker rm tmp_cabinet
  INDEX_FILE=$(grep -rl 'botUsername:xt' ./cabinet-dist/assets/*.js 2>/dev/null | head -1)
  sed -i "s/xt=\"\"/xt=\"${BOT_USERNAME}\"/g" "$INDEX_FILE"
  docker compose down && docker compose up -d
  ```
- **[id=244065|MAKS|26.02]** «Сборка кабинета 2/2 падает, надо 4/2».

## Remnawave/Bedolaga: ТСПУ — bridge для обхода (частично)
- **[id=243594|—|26.02]** 1cent.host EE 180₽ — «IP 64.188 лежит», «83.219 работает» (Fallen).
- **[id=243547|Whiteness|26.02]** 1cent.host EE 180₽ (1/1/10GB/1Gbit, IPv6 вкл, BBR вкл) — дубль.
- **[id=244296|Whiteness|26.02]** Midas NL 5€ — дубль.
- **[id=244338|Max R|26.02]** «Vitric».

## Система платежей (сравнение касс)
- **[id=245902|libkit|28.02]** Уведомления об оплате: https://github.com/BEDOLAGA-DEV/docs/blob/main/bot/notifications.mdx
- **[id=246297|—|28.02]** Вата (Wata): 12% карточный эквайринг РФ, 11% СБП NSPK; «могут предложить 10-15%», без КУС.
- **[id=246303|libkit|28.02]** «в вате 10% и на сбп и на карты».
- **[id=246297|tgshtt|28.02]** «Учитывая отсутствие KYC и прочих заёбов от стандартных платежек — терпимо, снижение % от оборота».
- **[id=245536|Егор|28.02]** Юкасса «маленький процент, мало негативных отзывов», у платеги «дохрена негативных отзывов».
- **[id=242673|—|25.02]** «Фрикасса, платега» (Vinchi).
- **[id=242412|Vinchi|25.02]** Фрикасса как платежка.
- **[id=243093|MAKS|26.02]** Илья Захаров: «45к в месяц обходится».
- **[id=243097|MAKS|26.02]** У юзера 45к₽/мес на Я.Клауд 6/6 700+ онлайн.
- **[id=243097|Zavulon|26.02]** ВК 2/2 тянет ~100 юзеров на БС-ноде, IP 200₽.
- **[id=243097|MAKS|26.02]** «Соберу рф хостинг под мост».
- **[id=243077|MAKS|25.02]** «Яша 1.6₽/ГБ, ВК бесплатный».
- **[id=243097|Zavulon|26.02]** «ВК у него в месяц 45» (valera).
- **[id=243097|MAKS|26.02]** valera: Я.Клауд 6/6, 700+ онлайн, 45к₽/мес.

## Прочее
- **[id=243637|Egor|26.02]** «Кабинет не слетает», реф. программы.
- **[id=243637|tgshtt|26.02]** «Приветственное сообщение».
- **[id=244074|tgshtt|26.02]** Ссылка на «Панель Баланс» (margus).
- **[id=244396|su -|27.02]** «Он мои айпи банит» (суи).
- **[id=245549|Chara Freedom|28.02]** «Юкасса работает».
- **[id=244922|Egor|28.02]** Чат бот (Bedolaga) v3.17.0/v3.18.0 «Юкасса кеша зависает».
- **[id=244072|tgshtt|26.02]** «Трейл на IP связать».
- **[id=244072|MAKS|26.02]** «Резервное копирование бота по расписанию» (3.14 → 3.15.1 → ласт).
- **[id=244072|Whiteness|26.02]** «Ветки».
- **[id=244072|tgshtt|25.02]** «Ветки dev».
- **[id=244072|tgshtt|25.02]** «Ветка dev».
- **[id=244072|MAKS|26.02]** «Ветки dev».

## Полезные ссылки из чанка
- https://docs.bedolagam.ru/ (новая база доки Bedolaga)
- https://docs.bedolagam.ru/cabinet/setup
- https://docs.bedolagam.ru/getting-started/docker-deployment
- https://docs.bedolagam.ru/getting-started/quickstart
- https://docs.bedolagam.ru/bot/channel-subscription
- https://docs.bedolagam.ru/bot/notifications.mdx
- https://docs.bedolagam.ru/getting-started/smtp-setup
- https://docs.rw/docs/learn/server-routing
- https://docs.rw/docs/learn/xray-json-advanced
- https://github.com/XTLS/RealiTLScanner
- https://github.com/IndeecFOX/zapret4rocket
- https://github.com/eGamesAPI/remnawave-reverse-proxy
- https://github.com/wrx861/server-shield
- https://github.com/DonMatteoVPN/TrafficGuard-auto
- https://github.com/DonMatteoVPN/Reshala-Remnawave-Bedolaga
- https://github.com/DanielLavrushin/tspu-docs
- https://github.com/vsys-host/shkeeper.io
- https://github.com/Case211/remnawave-admin
- https://github.com/Nurmaga095/FFXBan-remnawave
- https://www.kimsufi.com/de/
