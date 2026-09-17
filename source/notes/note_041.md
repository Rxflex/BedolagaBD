# Заметки из chunk_041 (id 237421..241920, 22.02–25.02.2026)

## БС (белые списки) и Я.Клауд / ВК — состояние на 22–25.02.2026
- **[id=237439..237460|Yaroslav/Илья Захаров/—|22.02](https://t.me/c/2941121338/237439)** Я.Клауд 51.250: БС отвалился, новый IP тоже не работает без моста; выбиваются IP «на изи» (с 35-й, потом с 15-й попытки). Работает только чистый (мост отрублен) RU-IP напрямую на Россию; мосты на иностранку перестали работать ~неделю назад («у 5 разных провайдеров не работает, трафик идёт но не открывается», порты >6000).
- **[id=237459|—|22.02](https://t.me/c/2941121338/237459)** Гипотеза: РФ-IP не могут подключаться к иностранным на Я.Клауд (внедряют фичу). Фикс-идея: RU-ноунейм сервер → мост → иностранка (потери по скорости/пингу, не проверено).
- **[id=237519..237521|tgshtt|22.02](https://t.me/c/2941121338/237519)** Яшу «легко выбивается» руками, но трафик платный — 1.6₽ за 1ГБ.
- **[id=238748|Сергей Комаров|23.02](https://t.me/c/2941121338/238748)** Массовый бан подсетей 23.02: весь Waicore (109.172, 185.75), 4vps финка (81.177), hostvds (ФР и США). К вечеру «отпустило обратно» [id=238789](https://t.me/c/2941121338/238789). Мелкие хостеры продолжали работать стабильно.
- **[id=240086..240102|Lywome|24.02](https://t.me/c/2941121338/240086)** ВК: «в какие-то моменты хост может стать недоступным», ноды отключаются по кд, финка живёт. Я.Клауд гранты 4к₽, обход (обход Yandex BGP-тулзой, "bgp tools") Ижевск/Краснодар/МГТС.
- **[id=240196|valera.|24.02](https://t.me/c/2941121338/240196)** valera на Я.Клауд: 700+ онлайн, конфиг 6/6, ~45к₽/мес за трафик — «задался вопросом, зачем платить за ГБ».
- **[id=241232|Zavulon|24.02](https://t.me/c/2941121338/241232)** ВК: трафик бесплатный (не 0.5₽/ГБ — «барыжат нагло»), 2/2 тянет ~100 юзеров на БС-ноде, IP 200₽. 3 «пула» где ВК-обход работает на всех операторах.
- **[id=241491|DonkyBoss|25.02](https://t.me/c/2941121338/241491)** Мегафон отвал (с 24.02): смена SNI/транспортов (gRPC/xHTTP/TCP/WS) не помогает; без ВПН в БС открывается ~50 доменов из 700 (2гис, ВТБ, макс, госуслуги). Банится либо IP, либо подсети 51.250/84.201/212.233.
- **[id=239298|MAKS|23.02](https://t.me/c/2941121338/239298)** p2go DE HI-LOAD — «айпишники норм видны с LTE» (vs 4vps).

## Обход ДПИ / чекеры / white-list
- **[id=239781|мысли|24.02](https://t.me/c/2941121338/239781)** Чекер TCP 16-20 (белые списки): https://hyperion-cs.github.io/dpi-checkers/ru/tcp-16-20/
- **[id=239877|Vlad Kulik|25.02](https://t.me/c/2941121338/239877)** https://github.com/hxehex/russia-mobile-internet-whitelist — рус. мобильные IP вайтухе (обновлялся, но R0xTaDDy считает «не очень актуальным»).
- **[id=240404|—|24.02](https://t.me/c/2941121338/240404)** Прописать свой IP-прокси/VPN IP в правило direct в роутинге, чтобы не конфликтовали MTProto и VPN.
- **[id=239753|Сергей|23.02](https://t.me/c/2941121338/239753)** Роутинг по Simple-RU (geosite/geoip через happ): https://utils.docs.rw/happ-rb — шаблон конфига для Happ.
- **[id=239995|Max R|23.02](https://t.me/c/2941121338/239995)** Готовый конфиг Happ `happ://routing/onadd/<base64 JSON>` (Simple-RU-routing), geosite/geoip ссылки frayZV/simple-ru-geoip, simple-ru-geosite, DNS DoU 1.1.1.1/1.0.0.1, GlobalProxy true, RemoteDNS 1.1.1.1, DnsHosts, DirectSites (geosite:private, geosite:category-ru, ...).
- **[id=239001|—|22.02](https://t.me/c/2941121338/239001)** Google Copilot (https://github.com/copilot) — «кинул ссылку на репо бота, попросил убрать кнопку из меню — схавал весь гит и выдал базу».

## Anti-DDoS / анти-скан / Firewall
- **[id=238585|—|23.02](https://t.me/c/2941121338/238585)** TrafficGuard-auto (ДонМаттео): https://github.com/DonMatteoVPN/TrafficGuard-auto — «Атак отбито: 26023 за полтора суток», банит IP ркн/грчц (десятки тысяч IP в бане).
- **[id=239587|—|24.02](https://t.me/c/2941121338/239587)** FFXBan (для Remnawave): https://github.com/Nurmaga095/FFXBan-remnawave
- **[id=238824|—|23.02](https://t.me/c/2941121338/238824)** Установка решалы (f2b + ufw + bbr + шейпер на каждую ноду):
  ```bash
  wget -O install.sh https://raw.githubusercontent.com/DonMatteoVPN/Reshala-Remnawave-Bedolaga/main/install.sh \
    && bash install.sh \
    && reshala
  ```
- **[id=238548|/dev/null|24.02](https://t.me/c/2941121338/238548)** РКН/ГРЧЦ сканят все VPS. Уфом + f2b «китайцы дудосят не с российских айпи». Закрытие всего мира кроме РФ — и п2г, и DDoS-Guard не спасают от L7 скана сабки по `sub/{randomString(32)}` с миллионом разных subID.
- **[id=240273|—|23.02](https://t.me/c/2941121338/240273)** Топ-20 сканеров (реальный лог):
  ```
  v4|212.192.158.75|AS61280|CMU_GRCHC|31|2026-02-22T21:59
  v4|212.192.158.176|AS61280|CMU_GRCHC|31|...
  v4|212.192.158.167|AS61280|CMU_GRCHC|31|...
  v4|212.192.158.74|AS61280|CMU_GRCHC|29|...
  v4|212.192.14.234|AS207713|GIR_SER-NET|24|...
  v4|212.192.14.224|AS207713|GIR_SER-NET|20|...
  v4|62.76.140.68|AS60747|MODUS|5|...
  v4|212.193.51.212|AS201848|COMFORTEL|1|...
  ```
- **[id=240669|Данч|24.02](https://t.me/c/2941121338/240669)** Комиссии/порты у платеги: 0,4% СБП, 3,5% карты, 1.6% за чек (юркасса) — по памяти Rambal Cochet.

## Тюнинг / шейдер / torrents / routing
- **[id=239991|Александр|24.02](https://t.me/c/2941121338/239991)** Блок торрентов: https://github.com/kutovoys/xray-torrent-blocker (тблокер) — по логам ремны, порт → ufw блок → коннтрек-обрыв. Не ловит в 3xui.
- **[id=240019|Zavulon|24.02](https://t.me/c/2941121338/240019)** Правило в xray для блока торрентов (routing):
  ```json
  "routing": {
    "rules": [
      { "ip": ["geoip:private"], "type": "field", "outboundTag": "BLOCK" },
      { "type": "field", "protocol": ["bittorrent"], "outboundTag": "TORRENT" },
      { "type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK" }
    ]
  }
  ```
- **[id=240287|tgshtt|24.02](https://t.me/c/2941121338/240287)** Шейдер/шейпер из решалы.
- **[id=240299|Никита|24.02](https://t.me/c/2941121338/240299)** Разбирает «на 2 устройства одновременно скорость проседает» — «ты спидтестом канал забиваешь»; и наоборот.
- **[id=239817|—|23.02](https://t.me/c/2941121338/239817)** Скорость и канал — смотри `bench.sh` / `bench.openode.xyz`.
- **[id=239841|Никита|24.02](https://t.me/c/2941121338/239841)** У юзера нода на 25 Гбит (на п2г выдавал ~19 гигабит).

## Схема 51.250 / bridge
- **[id=237928|Nick|23.02](https://t.me/c/2941121338/237928)** Caddy reverse proxy на дешёвом ВПС (перенос сабки за ТСПУ) + рабочий вариант:
  ```caddy
  {
      email admin@domen.com
  }
  https://domen.com {
      encode gzip
      reverse_proxy http://remnawave:3000
  }
  https://sub.domen.com {
      encode gzip
      # 1️⃣ Redirect handler (для HAPP_CRYPTOLINK_REDIRECT_TEMPLATE)
      handle /redirect/* {
          @hasQuery query redirect_to=*
          redir @hasQuery {http.request.uri.query.redirect_to} 302
          respond "Missing redirect_to parameter" 400
      }
      # 2️⃣ Subscription pages
      handle {
          reverse_proxy http://remnawave-subscription-page:3010
      }
  }
  :443 {
      tls internal
      respond 204
  }
  ```
- **[id=238701|—|23.02](https://t.me/c/2941121338/238701)** Caddyfile редирект для «connect?url={{HAPP_CRYPT4_LINK}}» (через поддомен редиректа).
- **[id=237605|Vladislav|22.02](https://t.me/c/2941121338/237605)** Fix крипто-ссылок в кабинете (DeepLinkRedirect.tsx):
  ```tsx
  const getRawParam = (key: string) => {
    const params = new URLSearchParams(window.location.search);
    const raw = params.get(key);
    if (!raw) return '';
    return decodeURIComponent(raw.replace(/ /g, '+'));
  };
  const deepLink = getRawParam('url') || getRawParam('deeplink') || '';
  ```
- **[id=237835|—|22.02](https://t.me/c/2941121338/237835)** В HAPP кнопка: `happ://add/{{SUBSCRIPTION_LINK}}` (И) и `happ://add/{{HAPP_CRYPT4_LINK}}` (Андрей).
- **[id=238127|RuVPN Поддержка|23.02](https://t.me/c/2941121338/238127)** `HAPP_CRYPTOLINK_REDIRECT_TEMPLATE=https://sub.domen.com/redirect/?redirect_to=`
- **[id=237629|—|23.02](https://t.me/c/2941121338/237629)** Ошибка 404 вебхука из панели — хук в Remnawave panel не нужен (это от Telegram; «в бедолаге нет интеграции с хуком в панель, удаляй это в панели и проблем не будет»).

## Remnawave / Bedolaga обновления и баги
- **[id=239703|Egor|24.02](https://t.me/c/2941121338/239703)** Bedolaga Bot v3.17.1 — int32 overflow guard, защита self-referral, кросс-валидация Telegram-идентичности, целостность БД.
- **[id=239395|Egor|23.02](https://t.me/c/2941121338/239395)** Cabinet v1.19.1 — deep linking fix (double-decode URL в крипто-ссылках), скидки, email auth, устранение leak.
- **[id=239866|Egor|24.02](https://t.me/c/2941121338/239866)** Bedolaga Bot v3.18.0 — мульти-канальная обязательная подписка (ChatMemberUpdated, 3-уровневый кеш Redis→PostgreSQL→Telegram API, per-user rate limit 5с), гайд подключения через Remnawave API с TTL, фильтр групповых сообщений; удалена legacy app-config.json.
- **[id=239883|Egor|24.02](https://t.me/c/2941121338/239883)** Cabinet v1.20.0 — мульти-канальная подписка, управление каналами.
- **[id=241545|Egor|25.02](https://t.me/c/2941121338/241545)** Bedolaga Bot v3.19.0 — RBAC+ABAC (AdminRole/UserRole/AccessPolicy/AdminAuditLog, 26 секций/78 разрешений, wildcard-matching, ABAC по времени/IP/weekdays, аудит-лог CSV), per-channel `disable_trial_on_leave`/`disable_paid_on_leave`; фикс: `subscription_url`/`crypto_link` исчезали после sync (update_user), синхронизация crypto_link в webhook user_modified.
- **[id=241546|Egor|25.02](https://t.me/c/2941121338/241546)** Cabinet v1.21.0 — RBAC в админке (Permission store, PermissionRoute, PermissionGate, ABAC по time/IP/weekdays, аудит-лог).
- **[id=240880|Max R|25.02](https://t.me/c/2941121338/240880)** Remnawave Panel v2.6.2 релиз (24.02) и v2.6.3 (25.02) hotfix.
- **[id=238125|RuVPN Поддержка|23.02](https://t.me/c/2941121338/238125)** Env-переменные Remnawave webhook (в панели):
  ```
  WEBHOOK_ENABLED=true
  WEBHOOK_URL=https://panel.XXX.ru/remnawave-webhook
  WEBHOOK_SECRET_HEADER=XXX
  ```
  В боте:
  ```
  REMNAWAVE_WEBHOOK_ENABLED=true
  REMNAWAVE_WEBHOOK_PATH=/remnawave-webhook
  REMNAWAVE_WEBHOOK_SECRET=XXX  # openssl rand -hex 32
  ```
  Из доки бота «в панели хук не нужен».
- **[id=239068|—|23.02](https://t.me/c/2941121338/239068)** Обновление бота командой (без пересборки):
  ```bash
  cd /opt/remnawave-bedolaga-telegram-bot && git pull origin main && docker compose down && docker compose up -d --build && docker compose logs -f
  ```
  (Егор советует сначала убрать `cd /opt/...` в команде).
- **[id=240608|Артём|24.02](https://t.me/c/2941121338/240608)** docker-compose.override.yml для кастомных правок (не трогать основной compose).
- **[id=240339|Данил|24.02](https://t.me/c/2941121338/240339)** Команды обновления кабинета: `cd /root/remnawave-bedolaga-telegram-bot/bedolaga-cabinet && git pull origin main && docker compose down && docker compose up -d --build && docker compose logs -f`
- **[id=240611|/dev/null|24.02](https://t.me/c/2941121338/240611)** В Remnawave 3.x синхронизация хостов: «в боте нажми определить».
- **[id=240516|MRX|24.02](https://t.me/c/2941121338/240516)** Ошибка `column subscriptions.last_webhook_update_at does not exist` — нужно обновляться поэтапно: сначала до v3.15.1, потом v3.16.0, потом на ласт.
- **[id=240534|—|24.02](https://t.me/c/2941121338/240534)** Миграция с 3.7.0 на 3.18 слетели тарифы/баланс/подписки. Решил: бэкап + восстановление.
- **[id=240345|tgshtt|24.02](https://t.me/c/2941121338/240345)** Bedolaga «обновиться но не слетели локали/кнопки» — бэкап и восстановление.
- **[id=240662|Владимир|24.02](https://t.me/c/2941121338/240662)** TrafficGuard-auto (ДонМаттео): https://github.com/DonMatteoVPN/TrafficGuard-auto/tree/main
- **[id=240254|—|24.02](https://t.me/c/2941121338/240254)** Vless-json vs обычный vless (tgshtt): «обычный — инфа о подписке в base64, просто список серверов; json — балансеры, роутинг, хуёутинг».
- **[id=240432|—|24.02](https://t.me/c/2941121338/240432)** `TZ=UTC` в .env (база бота переехала на UTC).
- **[id=240356|—|24.02](https://t.me/c/2941121338/240356)** `LOG_LEVEL=DEBUG` для расширенного дебага.
- **[id=240354|—|24.02](https://t.me/c/2941121338/240354)** `DEBUG=true` в env ботa.
- **[id=239287|Valerii Bezkorovainyi|23.02](https://t.me/c/2941121338/239287)** Reshala поставил (f2b/ufw/bbr/шейпер) на каждую ноду.

## Bedolaga баги/фичи конкретных версий (выборочно)
- **[id=239473|SligStorm|23.02](https://t.me/c/2941121338/239473)** Кабинет при инкогнито у нового юзера — кнопка «Добавить подписку» с HAPP_CRYPT4_LINK не отображается если юзер импортирован из другого проекта; появляется если берёт триал/тариф.
- **[id=239555|Whiteness|23.02](https://t.me/c/2941121338/239555)** `VPN logo` после обновы — не отображается из-за активной промо-группы со скидкой. Сброс промо-группы — всё оживает.
- **[id=239715|—|23.02](https://t.me/c/2941121338/239715)** Реф-ссылка из бота (Cabinet): DeepLinkRedirect.tsx — параметр `url` или `deeplink` (см. фикс выше).
- **[id=239587|—|24.02](https://t.me/c/2941121338/239587)** В кабинете после обновления кнопка «Подключиться» ломалась: URL вида `https://cabinet.xx.xx/login` — решение «убрать login» [id=240641|Андрей|24.02](https://t.me/c/2941121338/240641).
- **[id=239402|—|24.02](https://t.me/c/2941121338/239402)** Кабинет отдельно не обновляется (проверил, есть разница).
- **[id=239485|юкасса|Rambal Cochet|24.02](https://t.me/c/2941121338/239485)** С января юкасса перестала слать чеки; НДС на комиссию платежных систем по новому закону (не «чек»). `0,2%/0,6%` — самозанятый налог / НДС на комиссию.
- **[id=240572|—|24.02](https://t.me/c/2941121338/240572)** Выплаты ЮKassa «недоучли» 3 из 14 платежей в одну выплату.
- **[id=240397|DonkyBoss|24.02](https://t.me/c/2941121338/240397)** Юкасса при отключении чеков «остаются деньги».
- **[id=239738|/dev/null|24.02](https://t.me/c/2941121338/239738)** Пересобирай кабинет: `docker compose build --no-cache`.
- **[id=239876|e|23.02](https://t.me/c/2941121338/239876)** Команда удаления из `.env` не подхватывается если не `docker compose build --no-cache`.
- **[id=239921|Egor|23.02](https://t.me/c/2941121338/239921)** Планировщик бэкапов: `backup_interval_hours`/`backup_time` в env, «each 3 hours у меня».
- **[id=240298|Vlad|25.02](https://t.me/c/2941121338/240298)** «No hosts found» — надо назначить сервер в боте.

## Хостинги (отзывы/факты)
- **[id=238516|MAKS|23.02](https://t.me/c/2941121338/238516)** nodehost NL 1/2/15GB 10Gbit 2.85$ — «не советую. часто слетает, скорость не соответствует».
- **[id=238517|Whiteness|23.02](https://t.me/c/2941121338/238517)** 1cent.host EE Таллин 180₽ (1/1/10GB/1Gbit) — #неплохо.
- **[id=238519|Whiteness|23.02](https://t.me/c/2941121338/238519)** play2go DE-1 340₽ (1/2/80GB/1Gbit) — #неплохо.
- **[id=238523|Whiteness|23.02](https://t.me/c/2941121338/238523)** dhostVPS DE 3€ (1/1/10GB/10Gbit) — « Youtube как RU - Рекламы нет».
- **[id=238528|Whiteness|23.02](https://t.me/c/2941121338/238528)** Midas_Hosting GB Лондон 4€ (2/2/30GB/3Gbit) — #неплохо.
- **[id=238531|Whiteness|23.02](https://t.me/c/2941121338/238531)** nodehost DE 2.2$ (1/1/10GB/10Gbit) — #неплохо (позже MAKS спорит).
- **[id=238393|MAKS|23.02](https://t.me/c/2941121338/238393)** p2g HI-LOAD-1 DE 450₽ (1 vCPU 9950X, 2GB DDR5, 80GB NVMe, 10 Gbit, мощная L3-L4 DDoS защита) — «впечатления положительные».
- **[id=238538|Сергей|23.02](https://t.me/c/2941121338/238538)** p2g PROMO-2 159₽ (2 ядра AMD EPYC 7351P, 4GB RAM 15GB NVMe, 100Мб/с) — «работает шустро, оверсела нету».
- **[id=238565|MAKS|23.02](https://t.me/c/2941121338/238565)** Mhost Швейцария/Цюрих 5€ (1 vCPU | 2GB DDR5 | 30GB NVMe).
- **[id=239331|Миша|23.02](https://t.me/c/2941121338/239331)** hyper.hosting Micro 4$ МСК 1Гбит — «50-60 Мбит реала, не рекомендую».
- **[id=238456|Spaghetti Support|23.02](https://t.me/c/2941121338/238456)** justhost — «не советую, аптайм конченый», «неделя проблем с сетью МСК VPS».
- **[id=238401|Whiteness|23.02](https://t.me/c/2941121338/238401)** hip hosting — «сервер подняли вторые сутки»; weasel.cloud — «продают локации даже когда закончились» (ddddd, mah1cul). hiphosting=weasel.cloud (одна компания, разный бренд, один юрлицо) [id=238409|tgshtt](https://t.me/c/2941121338/238409).
- **[id=239605|Fabel|23.02](https://t.me/c/2941121338/239605)** hosting-vds.com 4/8/80 — 370₽ МСК (У меня панель+бот) — «панель/сабка/бот».
- **[id=239672|MAKS|23.02](https://t.me/c/2941121338/239672)** freakhosting DE Budget VPS-1 2.49€ (1/1/25GB NVME 10Gbps) — «не советую, скорости странные».
- **[id=239683|Aleksey Ermakov|23.02](https://t.me/c/2941121338/239683)** Freakhosting DE 2.49€ — «не советую, IPQuality многое говорит».
- **[id=239716|ALIEN|24.02](https://t.me/c/2941121338/239716)** YeezyHost SE Швеция 5950x 3.6$ (1/2/30GB).
- **[id=239674|Xenomorph|24.02](https://t.me/c/2941121338/239674)** aeza.ru — «норм для моста».
- **[id=239678|Prokurátura|24.02](https://t.me/c/2941121338/239678)** beget — 1 гигабит, ТСПУ нет (под мост для RU).
- **[id=239686|MAKS|24.02](https://t.me/c/2941121338/239686)** asdhere (my.asdhere.net) — 25 Гбит, «макс выбивал ~19 гигов на нидерландах», «асд не разу не падал».
- **[id=239690|Кamil|24.02](https://t.me/c/2941121338/239690)** asdhere — пинг 900+ у одного.
- **[id=239695|Whiteness|24.02](https://t.me/c/2941121338/239695)** «LC не советую. Очень нестабильные», «1cent падох» [id=237498|9|22.02](https://t.me/c/2941121338/237498).
- **[id=239794|Vlad|24.02](https://t.me/c/2941121338/239794)** aeza — «отваливаются постоянно».
- **[id=239840|Whiteness|24.02](https://t.me/c/2941121338/239840)** «4vps финка нахуй, hostvds нахуй» (бан подсетей 23.02).
- **[id=239847|Whiteness|24.02](https://t.me/c/2941121338/239847)** «Ovh» (Zavulon) — «прямо нода для прокси с 500+».
- **[id=240028|—|24.02](https://t.me/c/2941121338/240028)** Нидерланды/Германия на p2go — «PROMO-2 взял за 159р» (2 ядра).
- **[id=240101|Alex T|24.02](https://t.me/c/2941121338/240101)** «Оракл и амазон» — `s.yorksik.mooo.com` — «ключ, что я скидывал, не работает в нужных регионах РФ» (AWS/Oracle ноды).
- **[id=240096|Vlad Kulik|24.02](https://t.me/c/2941121338/240096)** «не поверишь - тоже самое» (Hetzner и OVH не работают напрямую из РФ).
- **[id=239715|Whiteness|23.02](https://t.me/c/2941121338/239715)** Hetzner — «у меня там 4-5 серверов, нет проблем» (Prokurátura).
- **[id=240754|Bulat|24.02](https://t.me/c/2941121338/240754)** 1cent.host (1/1/10GB/1Gbit, 180₽) — «падох», «у моего инет так скажем не очень».
- **[id=238853|Сергей|23.02](https://t.me/c/2941121338/238853)** CloudCore Burstable-2 — steal 75–85% CPU.
- **[id=241322|MAKS|24.02](https://t.me/c/2941121338/241322)** p2go NL HI-LOAD — «вечером отваливается раз в день на 5 минут» (ddddd).
- **[id=239073|MAKS|24.02](https://t.me/c/2941121338/239073)** play2go SWE (ЛК или ХЛ) — «гигабитка».
- **[id=240754|Kamil|24.02](https://t.me/c/2941121338/240754)** p2go «на некоторых локах норм, на некоторых пиздец».
- **[id=238738|MAKS|23.02](https://t.me/c/2941121338/238738)** 4vps Finland R9 5950x — 4.3$ (2/2/45GB).
- **[id=239082|MAKS|24.02](https://t.me/c/2941121338/239082)** YeezyHost SE R9 5950x — 3.6$ (1/2/30GB).
- **[id=239087|—|24.02](https://t.me/c/2941121338/239087)** asdhere — 25 Гбит, 9950x3d, NL, 19 гигов.
- **[id=241702|MAKS|23.02](https://t.me/c/2941121338/241702)** Mhost CH Цюрих 5€ (1/2/30GB NVMe) — снова рекомендуют.
- **[id=239666|Kamil|24.02](https://t.me/c/2941121338/239666)** p2go — «на некоторых локах норм, на некоторых пиздец», «у меня там 6 впсок».
- **[id=239591|—|23.02](https://t.me/c/2941121338/239591)** beget.com (Rawi) — «ежедневная тарификация».
- **[id=239092|MAKS|23.02](https://t.me/c/2941121338/239092)** Mhost CH 5€ — «0,4 сбп, 3,5 картами» (это про платегу).
- **[id=239568|Whiteness|23.02](https://t.me/c/2941121338/239568)** doubleservers CA Beauharnois 10,26€ (4/8/75GB NVME) — «во всех геобазах отображается как нужно».
- **[id=239591|saveks|23.02](https://t.me/c/2941121338/239591)** Midas_Hosting NL Амстердам 5€ (1/2 DDR5/30GB/5Gbit) — «работает очень хорошо».
- **[id=239590|Djingle|23.02](https://t.me/c/2941121338/239590)** hostvds — «не советую» (ип без кешей).
- **[id=239655|bypara|23.02](https://t.me/c/2941121338/239655)** nodehost выкидывай — «с 1 марта режут скорость сильно всем» (Евген).
- **[id=239655|tgshtt|25.02](https://t.me/c/2941121338/239655)** hiphosting 4/8 370₽, «норм цены по конфигу», «4/8 у меня норм пашет», «под ноды хипхост не рекомендую» (100 Мбит гарант).
- **[id=239655|Евген|25.02](https://t.me/c/2941121338/239655)** dhost и nodehost — «с 1 марта режут скорость сильно всем».
- **[id=238853|MAKS|23.02](https://t.me/c/2941121338/238853)** nodehost NL 1/2/15GB 10Gbit 2.85$ — «не советую. Часто слетает и мало людей сидят на нём, также скорость не соответствует заявленной».
- **[id=240717|—|24.02](https://t.me/c/2941121338/240717)** Doubleservers DE Нюрнберг 6.64€ (2/4/40GB SSD) — «Забанен» (MAKS).
- **[id=240717|/dev/null|24.02](https://t.me/c/2941121338/240717)** Пропажа dhost 10 Гбит — «режут».
- **[id=240535|17|23.02](https://t.me/c/2941121338/240535)** Ovh и Hetzner — «прямо нода для прокси с 500+».
- **[id=239752|MAKS|23.02](https://t.me/c/2941121338/239752)** hetzner «у половины провайдеров не работает» — «мост делать».
- **[id=240128|—|24.02](https://t.me/c/2941121338/240128)** serva.one — «крайне не рекомендую» (Евген, комиссия огромная, мин тариф 5€).
- **[id=238963|DonkyBoss|25.02](https://t.me/c/2941121338/238963)** aeza — «массовая блокировка всех российских серверов на всех аккаунтах, без предупреждения и без возможности снять бекапы» (3301, 25.02). «Тут только ленивый не сказал какие аеза куколды» (Name Lastname).
- **[id=240128|MAKS|25.02](https://t.me/c/2941121338/240128)** asdhere (my.asdhere.net) — «асд не разу не падал» (Zavulon).
- **[id=240128|Mah1cul|25.02](https://t.me/c/2941121338/240128)** the.hosting (KZ, кириллический хостер) — «>60-70% кз билось, мост через рф».
- **[id=240112|Валера|25.02](https://t.me/c/2941121338/240112)** «шкаф с хостингом на профи». Ilyas — «500 рублей эстонка ee-1 интезио», «интезио 10 гбит шаред, ретн апстрим как у 1cent», «мы на RETN пинг оч маленький».
- **[id=239683|Dzhokhar|23.02](https://t.me/c/2941121338/239683)** «Яшин обход - 51.250, 84.201, 212.233 — работает на изи, у него в пуле всего 254 адресов» (шардинг p2g, dhost, nodehost).
- **[id=240048|Dzholo|23.02](https://t.me/c/2941121338/240048)** «opdnodе.xyz bench».
- **[id=240046|—|24.02](https://t.me/c/2941121338/240046)** «bench.sh».
- **[id=239059|/dev/null|24.02](https://t.me/c/2941121338/239059)** Под «RU-серваки для моста» — «бери практически что угодно», «adman».

## Прочее
- **[id=237919|MAKS|23.02](https://t.me/c/2941121338/237919)** Оркестратор Веб-админка (Case211/remnawave-admin) v2.3.2 — Fleet (скрипты из UI/GitHub), удалённое обновление агента, IP-аналитика, HWID кросс-аккаунт детекция, биллинг нод.
- **[id=239443|Илья|23.02](https://t.me/c/2941121338/239443)** Remnawave Admin v2.4.0 — Fleet Management (Web Terminal xterm.js), External API v3, anti-abuse per-user, RBAC, бэкапы; `AGENT_COLLECTOR_URL` → web-backend :8081.
- **[id=240062|Zavulon|24.02](https://t.me/c/2941121338/240062)** Ссылка на прессу про Яндекс 3к₽ — «на Яндексе 3к почти отдаю только за сервер» (Forward).
- **[id=239402|/.|23.02](https://t.me/c/2941121338/239402)** xraycore.org/ru/misc/dns_roulette/ — DNS round robin для балансировки нод.
- **[id=239683|/dev/null|24.02](https://t.me/c/2941121338/239683)** `docker logs -f cabinet_frontend` — проверить, что нет ошибок.
- **[id=239365|—|23.02](https://t.me/c/2941121338/239365)** «минимальная рыночная цена за трафик 0.15 евро/мбит» (zoomov, оценка).
- **[id=239820|—|23.02](https://t.me/c/2941121338/239820)** «Кто-то уже скидывал» ссылку на прессу.
- **[id=239279|MAKS|23.02](https://t.me/c/2941121338/239279)** «Проблемы с сервером — надо спрашивать у поддержки».
- **[id=239872|Whiteness|23.02](https://t.me/c/2941121338/239872)** «2ip.ru США показывает для свежевзятых IP» — геобазы обновляются не сразу.
- **[id=239711|bypara|23.02](https://t.me/c/2941121338/239711)** «Реф-ссылки в тестах впс — просите вердикт, не только рефку» (Name Lastname).
- **[id=239706|Jolymmiels|23.02](https://t.me/c/2941121338/239706)** Repl Bot's petka (Bedolaga) v3.17.0 + Cabinet v1.19.1.
- **[id=240655|/dev/null|24.02](https://t.me/c/2941121338/240655)** «anti-сканеры — топик чата».
- **[id=240655|Влад|25.02](https://t.me/c/2941121338/240655)** «bash <(wget -qO- https://dignezzz.github.io/server/dashboard.sh) --force» — MOTD dashboard.
- **[id=240655|tgshtt|25.02](https://t.me/c/2941121338/240655)** «anti-сканеры» — ссылка на чат.
- **[id=239279|SligStorm|23.02](https://t.me/c/2941121338/239279)** «Не открывается сабка на домашнем интернетe (я)».
- **[id=239753|/.|24.02](https://t.me/c/2941121338/239753)** Дороговизна «не дублировать в боте управление панелью».
- **[id=239588|Laz|25.02](https://t.me/c/2941121338/239588)** «Поиск по чату» — «99% ответов там» (Лис).
- **[id=239706|Alex|25.02](https://t.me/c/2941121338/239706)** «У меня в РФ стоит на одной машине всё (panel+bot)» (Евген).
- **[id=240754|MAKS|23.02](https://t.me/c/2941121338/240754)** «YeezyHost: Швеция 5950x» — «пинг от меня до швеции самый низкий» (ALIEN).
- **[id=239713|MAKS|23.02](https://t.me/c/2941121338/239713)** «По пингу: Эстония/Латвия дают меньше пинг нежели Швеция и Финка» (Prokurátura).
- **[id=239716|Prokurátura|23.02](https://t.me/c/2941121338/239716)** «овх и хетзнер напрямую нет» (. | 24.02).
- **[id=239753|MAKS|24.02](https://t.me/c/2941121338/239753)** Кассир «OVH» — «барыжат нагло» (Zavulon).

## Полезные ссылки из чанка
- https://docs.rw/docs/learn/server-routing/
- https://docs.rw/docs/install/subscription-page/separate-server/
- https://docs.rw/docs/install/remnawave-node
- https://utils.docs.rw/happ-rb
- https://docs.bedolagam.ru/bot/channel-subscription
- https://bedolagadev.mintlify.app/bot/subscriptions
- https://bedolagadev.mintlify.app/bot/subscriptions#%D0%B4%D0%BE%D0%BA%D1%83%D0%BF%D0%BA%D0%B0-%D1%82%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%B0
- https://xraycore.org/ru/misc/dns_roulette/
- https://github.com/DonMatteoVPN/TrafficGuard-auto
- https://github.com/DonMatteoVPN/Reshala-Remnawave-Bedolaga
- https://github.com/Nurmaga095/FFXBan-remnawave
- https://github.com/kutovoys/xray-torrent-blocker
- https://github.com/BEDOLAGA-DEV/bedolaga-cabinet
- https://github.com/BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot
- https://github.com/hxehex/russia-mobile-internet-whitelist
- https://hyperion-cs.github.io/dpi-checkers/ru/tcp-16-20/
- https://github.com/Case211/remnawave-admin
- https://docs.rw/docs/learn/xray-json-advanced
- https://neonode.cc/ru/blog/motd_dashboard/
