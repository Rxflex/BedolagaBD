# Заметки из chunk_089 (id 574737..585946, 24.05–26.05.2026)

## Веха: массовый отвал VLESS TCP Reality по fingerprint (25–26.05.2026)
- **[id=581441..585946|общий|25–26.05.2026]** ТСПУ начала отбрасывать VLESS TCP Reality с фингерпринтом **chrome**: «пинг есть, но не работает», сначала Сибирь/ДВ (Новосибирск, Кемерово, Ростов, Якутск, Крым), потом шире. Частичный отвал ws/grpc.
  - Фиксы по данным чата: смена fingerprint в Remnawave → Хосты → расширенные (chrome → **firefox / safari / qq / android / ios / random / randomized**); gRPC-транспорт работает; переход на mihomo-клиенты (FlClashX, Koala Clash, Hiddify, Prizrak Box, RabbitHole на iOS) — на них проблемы не проявлялись; полный сброс приложения после смены fp; у части не помог ничего (Краснодар — ни один fp).
  - «График юзеров фф после 25.05.2026: 📈» [id=581937]; qq fp для РФ «максимально палевный» [id=582124]; «рандомайзед пашет вроде везде» [id=585579].
  - Возможная причина привязана к патчу ядра Xray: https://github.com/XTLS/Xray-core/pull/6181 [id=582273]. Связь подтверждали, точной уверенности нет.
  - gRPC менее подвержен убийству, т.к. это h2 [id=582276].
  - Нюанс: клиент Happ на iOS со старым ядром — подобные TCP-блокировки на Apple-устройствах не срабатывают [id=585657].
  - Контекст: ТСПУ «вышли на новый уровень» — блок по объёму пакетов с одного IP (шортс/YouTube тупит при большом числе соединений) [id=584006].

### Массовая смена fingerprint через Remnawave API (легиз/ALERT AI)
- **[id=582144|legiz|25.05.2026]** Ответ на issue panel#463: bulk-редактирование fp через REST API. PATCH `/api/hosts` принимает `{uuid, fingerprint}`, меняет только переданные поля. bash-версия:
```bash
API_URL="https://YOUR_PANEL_URL"
TOKEN="YOUR_TOKEN"
NEW_FP="firefox"   # chrome | firefox | safari | ios | android | edge | qq | random | randomized
UUIDS=$(curl -s -X GET "$API_URL/api/hosts" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "import sys,json; [print(h['uuid']) for h in json.load(sys.stdin)['response']]")
for UUID in $UUIDS; do
  curl -s -X PATCH "$API_URL/api/hosts" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"uuid\": \"$UUID\", \"fingerprint\": \"$NEW_FP\"}"
done
```
  - PowerShell-версия (fp только у хостов с chrome):
```powershell
$API_URL = "https://YOUR_PANEL_URL"; $TOKEN = "YOUR_TOKEN"
$OLD_FP = "chrome"; $NEW_FP = "firefox"
$headers = @{ "Authorization" = "Bearer $TOKEN"; "Content-Type" = "application/json" }
$hosts   = (Invoke-RestMethod -Uri "$API_URL/api/hosts" -Method GET -Headers $headers).response
$targets = $hosts | Where-Object { $_.fingerprint -eq $OLD_FP }
foreach ($h in $targets) {
    $body = @{ uuid = $h.uuid; fingerprint = $NEW_FP } | ConvertTo-Json
    Invoke-RestMethod -Uri "$API_URL/api/hosts" -Method PATCH -Headers $headers -Body $body | Out-Null
}
```
  - Значения fp: chrome, firefox, safari, ios, android, edge, qq, random, randomized. Тем же патчем можно менять sni, alpn, allowInsecure, port, path и др.

## DDoS-защита: реальность и скам
- **[id=574884|Wyatt Haley|24.05.2026]** Ключевой тезис: фаервол-уровень «защита» не спасает от SYN-flood — каждый SYN обязан быть обработан системой; если трафик превышает канал, поможет только промежуточная транзитная скрабка (анти-DDoS хостинг); ноды защитить нельзя, панель — за Cloudflare.
- **[id=575138|825hp|24.05.2026]** Его Rust-аналог TrafficGuard работает на L2-L3 (nftables, блок CIDR до conntrack, радикс-деревья, синк списков) — сообщество считает это не защитой от L4-атак, а фильтрацией подсетей.
- **[id=576226|. (спуфи/spfowner)|24.05.2026]** Скандал: продавец скрипта «защиты от DDOS за 40$» (кастомное ядро XanMod, MSS clamping) — сообщество: «любая нейронка раскурит», скрипт «не спасёт при нормальном L4-вливе», при атаке превышающей канал «канал забит до того, как его сервер вообще увидит трафик» [id=576386]. Покупатель Chara Freedom: скрипт не детектит атаку («соворис»), 0 результата [id=574846, 575964]. Продавать такие скрипты как «защиту» = скам [id=574975].
- **[id=576015|—|24.05.2026]** Команда от Gemini для дропа POST-запросов (проверить применимость, во VLESS Reality «POST» встречается):
```
sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -m string --algo bm --string "POST" -j DROP
```
- **[id=575330|DAUNAMORAL|24.05.2026]** «В целом это и fail2ban отфильтрует» — ирония над продажей «лучших методов».
- **[id=574933|Wyatt Haley|24.05.2026]** Cloudflare для панели: включить проксирование (облачко) рядом с доменом, reverse-proxy в ремне должен подстроиться; при проблемах — дёргать настройки SSL в CF. Кэширование отрубить [id=575054].
- **[id=574977|Денис|24.05.2026]** CF на панели ок, но на субдоменах нод/подписки — ноды становятся недоступны; на ноды CF не вешать, сабку — на отдельный сервер под CDN крупного RU-провайдера [id=574982]. «CF тоже в РФ заблокирован» [id=583364].

## Конфиг Xray с RU-DIRECT (Кирилл, полный)
- **[id=576494|Кирилл|24.05.2026]** Рабочий Xray JSON: DNS split (yandex/vk/mail/ok/госуслуги → 77.88.8.8, остальное → 1.1.1.1 DoH), inbounds VLESS_Reality_443 (dest vk.com:443, serverNames vk.com/mail.ru/ok.ru/ya.ru) + Shadowsocks_8388, outbounds DIRECT/BLOCK, routing: category-ads-all → BLOCK, большой список RU-доменов → DIRECT, geoip:ru + private → DIRECT.
```json
{
  "log": {"loglevel": "warning"},
  "dns": {
    "queryStrategy": "UseIPv4",
    "servers": [
      {"address": "https://1.1.1.1/dns-query", "domains": ["geosite:geolocation-!cn"], "queryStrategy": "UseIPv4"},
      {"address": "https://77.88.8.8/dns-query", "domains": [
        "domain:yandex.ru","domain:yandex.com","domain:ya.ru","domain:yandex.net",
        "domain:vk.com","domain:vk.me","domain:vkontakte.ru",
        "domain:mail.ru","domain:ok.ru","domain:gosuslugi.ru",
        "domain:sberbank.ru","domain:mos.ru"
      ], "queryStrategy": "UseIPv4"},
      "1.1.1.1", "77.88.8.8"
    ]
  },
  "inbounds": [
    {
      "tag": "VLESS_Reality_443", "port": 443, "protocol": "vless",
      "settings": {"clients": [], "decryption": "none"},
      "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
      "streamSettings": {
        "network": "tcp", "security": "reality",
        "realitySettings": {
          "dest": "vk.com:443", "show": false, "xver": 0,
          "shortIds": ["","9c","0a3dc0","5869"],
          "privateKey": "...",
          "serverNames": ["vk.com","mail.ru","ok.ru","ya.ru"]
        }
      }
    },
    {
      "tag": "Shadowsocks_8388", "port": 8388, "protocol": "shadowsocks",
      "settings": {"clients": [], "method": "chacha20-ietf-poly1305", "network": "tcp,udp"},
      "sniffing": {"enabled": true, "destOverride": ["http","tls"]}
    }
  ],
  "outbounds": [
    {"tag": "DIRECT", "protocol": "freedom", "settings": {"domainStrategy": "UseIPv4"}},
    {"tag": "BLOCK",  "protocol": "blackhole", "settings": {"response": {"type": "http"}}}
  ],
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      {"type": "field", "outboundTag": "BLOCK", "domain": [
        "geosite:category-ads-all",
        "domain:adnxs.com","domain:googlesyndication.com","domain:doubleclick.net",
        "domain:googleadservices.com","domain:moatads.com","domain:amazon-adsystem.com"
      ]},
      {"type": "field", "outboundTag": "DIRECT", "domain": [
        "domain:yandex.ru","domain:yandex.com","domain:ya.ru","domain:yandex.net",
        "domain:yandex.kz","domain:yandex.by",
        "domain:vk.com","domain:vkontakte.ru","domain:vk.me","domain:userapi.com",
        "domain:mail.ru","domain:bk.ru","domain:inbox.ru","domain:list.ru",
        "domain:ok.ru","domain:odnoklassniki.ru",
        "domain:gosuslugi.ru","domain:esia.gosuslugi.ru",
        "domain:sberbank.ru","domain:online.sberbank.ru","domain:sbbol.ru",
        "domain:tinkoff.ru","domain:alfabank.ru","domain:vtb.ru",
        "domain:gazprombank.ru","domain:raiffeisen.ru","domain:rshb.ru",
        "domain:mts.ru","domain:megafon.ru","domain:beeline.ru","domain:tele2.ru",
        "domain:ozon.ru","domain:wildberries.ru","domain:avito.ru",
        "domain:auto.ru","domain:drom.ru","domain:hh.ru","domain:headhunter.ru",
        "domain:kinopoisk.ru","domain:rutube.ru","domain:ivi.ru","domain:okko.tv",
        "domain:2gis.ru","domain:2gis.com",
        "domain:dns-shop.ru","domain:mvideo.ru","domain:eldorado.ru",
        "domain:lamoda.ru","domain:samokat.ru","domain:magnit.ru",
        "domain:dzen.ru","domain:mos.ru","domain:kremlin.ru",
        "domain:gosuslugi.ru","domain:pfr.gov.ru","domain:nalog.ru",
        "domain:cdnvideo.ru","domain:ngenix.net","domain:mts-cloud.ru",
        "domain:rt.ru","domain:russianpost.ru"
      ]},
      {"type": "field", "outboundTag": "DIRECT", "ip": [
        "geoip:ru","geoip:private",
        "127.0.0.0/8","10.0.0.0/8","172.16.0.0/12","192.168.0.0/16"
      ]}
    ]
  }
}
```

## Список RU-доменов для блокировки/байпаса (MA, на XRAY + Happ Direct)
- **[id=576511..576691|MA|24.05.2026]** Цель — не отлететь в бан: некоторые RU-сервисы шлют данные о пользователе и «штампик что у него впн» (озон с впн не ворк). На иностранных нодах эти домены — BLOCK, для клиентов — Happ Routing Direct. Достаточно `domain:max.ru` (поддомены наследуются) [id=576459, 576781].

## Роутинг по геосайту в Remnawave (Свят Камаев)
- **[id=576771|Свят Камаев|24.05.2026]** Доработанный конфиг с антифильтром: RU-домены (.ru/.su/.рф, субдомены явные на всякий) → direct; Frist: «я так же на домейн переписал все» [id=576774]. Оценка: «хороший кфг» [id=576777].

## Базовый шаблон VLESS Reality inbound (Jordan)
- **[id=576687|Jordan|24.05.2026]** Минимальный Xray inbound для ноды (заполнить target, privateKey, serverNames):
```json
{
  "log": {"loglevel": "none"},
  "inbounds": [{
    "tag": "VLESS_TCP_REALITY", "port": 443, "listen": "0.0.0.0",
    "protocol": "vless",
    "settings": {"clients": [], "decryption": "none"},
    "sniffing": {"enabled": true, "destOverride": ["http","tls","quic"]},
    "streamSettings": {
      "network": "raw", "security": "reality",
      "realitySettings": {
        "target": "#REPLACE_WITH_YOUR_DEST, EXAMPLE: example.com:443",
        "shortIds": [""],
        "privateKey": "#REPLACE_WITH_YOUR_PRIVATE_KEY",
        "serverNames": ["#REPLACE_WITH_YOUR_SERVER_NAMES, EXAMPLE: example.com"]
      }
    }
  }],
  "outbounds": [
    {"protocol": "freedom", "tag": "DIRECT"},
    {"protocol": "blackhole", "tag": "BLOCK"}
  ],
  "routing": {"rules": [
    {"ip": ["geoip:private"], "outboundTag": "BLOCK"},
    {"domain": ["geosite:private"], "outboundTag": "BLOCK"},
    {"protocol": ["bittorrent"], "outboundTag": "BLOCK"}
  ]}
}
```
  - Генерация ключей на ноде: `xray x25519` [id=576608]; либо взять готовый из панели.

## RU-сервер как мост (relay) к нодам по странам (Xanta)
- **[id=579794|Xanta|25.05.2026]** Схема: пользователь → RU inbound (отдельный под страну) → RU outbound → зарубежная нода → интернет. Routing по inboundTag:
```json
"routing": {
  "rules": [
    {"type": "field", "inboundTag": ["germany-in"],    "outboundTag": "germany-out"},
    {"type": "field", "inboundTag": ["netherlands-in"],"outboundTag": "netherlands-out"}
  ]
}
```
  - Отдельный inbound/порт/path/SNI под каждую страну — иначе на RU сервере не понять, куда хотел попасть клиент.

## Балансировка нод (leastLoad + fallback)
- **[id=584231|art vs|25.05.2026]** `fallbackTag` — один outbound tag, не список. Резервные хосты задаются высоким cost:
```json
"balancers": [{
  "tag": "Super_Balancer",
  "selector": ["proxy","fallback"],
  "strategy": {"type": "leastLoad", "settings": {
    "costs": [{"match": "fallback", "value": 9999, "regexp": false}],
    "maxRTT": "1s", "expected": 2, "baselines": ["1s"], "tolerance": 0.01
  }}
}],
"domainStrategy": "IPIfNonMatch"
```
  - Альтернатива: лупбэк + группа БС [id=584513].
  - Конфиг gRPC+Reality inbound (Ак Барс, не заработал через CDN) [id=578984]:
```json
{
  "log": {"loglevel": "debug"},
  "inbounds": [{
    "tag": "grpc-cdn", "port": 10445, "protocol": "vless",
    "settings": {"clients": [], "decryption": "none"},
    "streamSettings": {
      "network": "grpc", "security": "none",
      "grpcSettings": {
        "multiMode": true,
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0.0.0 Safari/537.36",
        "idleTimeout": 15, "serviceName": "/api", "healthCheckTimeout": 12,
        "initialWindowsSize": 0, "permitWithoutStream": false
      }
    }
  }],
  "outbounds": [{"protocol": "freedom"}]
}
```
  - grpc+reality у Tesla (работает) [id=578834]: `network: grpc, security: reality, grpcSettings: {mode:false, serviceName:"service"}, target: 127.0.0.1:9443`, xver:1.
  - При авто-выборе (балансер) — периодические обрывы [id=585235], по-видимому конфликт Happ.

## Оптимизация
- **[id=576459, 576516, 576524|MA/DarkDragonFlame|24.05.2026]** RU-домены можно не блокировать, а «отправить в директ» у клиента (роутинг прилетает с подпиской); у MA сделано «заблочены на всех иностранных нодах кроме РФ + роутинг правила для Happ с директом».
- **[id=574786|825hp|24.05.2026]** nftables: блокирование CIDR ещё до conntrack, инкрементальные обновления, радикс-деревья — быстро и легко.

## Домены
- **[id=574941|—|24.05.2026]** «каждый syn пакет для отражения должен быть минимально обработан системой» — если пакетов больше, чем канал, ничего не поможет.
- **[id=579837|Andrey Petrov|25.05.2026]** Домены .рф по 200 руб./год (продление столько же).

## Полезные инструменты и ссылки (официальный пост бота + обсуждения)
- **[id=575790|BedolagamNaPivoBot|24.05.2026]** Список GitHub-проектов экосистемы:
  - remnawave/panel
  - BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot
  - BEDOLAGA-DEV/bedolaga-cabinet
  - kutovoys/xray-checker
  - eGamesAPI/remnawave-reverse-proxy
  - Jolymmiels/remnawave-telegram-shop
  - machka-pasla/remnawave-tg-shop
  - DigneZzZ/remnawave-scripts
  - distillium/remnawave-backup-restore
  - maposia/remnawave-telegram-sub-mini-app
  - legiz-ru/my-remnawave
  - dotX12/traffic-guard
  - Партнёрства: Platega (менеджер @ArstanPlatega) и RollyPay (rollypay.io, менеджеры @sasha_rollypay / @rollypay_manager) — СБП QR, RU/зарубежные карты, крипта (USDT, TON, ETH, CryptoBot, XRocket), ЕРИП/Беларусь.
- **[id=578021|Vladimir Goncharov|24.05.2026]** MTProto-прокси: панель не имеет официальной поддержки, сторонняя есть только на старую версию; скрипт https://github.com/ivan-yurich/mtproxy/tree/main — быстрый, но выдача проксей ручная. QQ Support: «mtg-multi лучше всех работает» [id=582334].
- **[id=578074|fullinside|24.05.2026]** Selectel IP Parser — бот для выбива нужного IP в облаке Selectel: OpenStack Keystone v3 + Neutron, режимы (обычная охота с AIMD-лимитером: старт 1 rpm, на успех растёт, на 429 ×0.5 + cooldown 20 мин, circuit breaker при 2+ 429 подряд; точный поиск по подсетям JSON, 2 rpm, 409 → пропустить), регионы ru-1/2/3/7/8/9, форматы: точный IP/CIDR/префикс/wildcard, стек Python 3.11 + aiogram 3 + aiohttp + aiosqlite + Docker.
- **[id=578074|fullinside|24.05.2026]** Reg.ru IP Hunter — бот для выбива IP в Reg.ru CloudVPS: API доп. IP не работает в OpenStack-регионах, поэтому «создать VPS → получить случайный IP → проверить → удалить → повторить», ждёт 404 перед следующей попыткой; adaptive rate ×0.5 на 429; квота-семафор (1 без верификации / 5 с верификацией); регионы openstack-msk1/msk2/spb1/sam1/fz1, msk1.
- **[id=577586, 583947|MultiRoller|24-25.05.2026]** Парсер белых IP (Yandex Cloud, Selectel до 1000 IP/час, VK Cloud, Reg.ru, Timeweb, RUVDS, скоро Beget) — сам проверяет IP на доступность, веб-панель, ТГ-уведомления, ротация прокси.
- **[id=578008|theflyke|24.05.2026]** «Способ обхода белых списков, не Яндекс и не VK, 0.8 ₽/ГБ, первые 4500 ГБ бесплатно (можно пересоздавать аккаунты)» — как способ (без деталей).
- **[id=578295|Wyatt Haley|24.05.2026]** Днр: у Ирана «все подсети CF в полном блоке, но в ТСПУ прописан белый список SNI, которые открываются даже на забаненных подсетях» — пример: random 193.232.123.0/24 со SNI yahoo.com — отвал, со SNI google.com — пропустит (не на всех подсетях); TG полностью в нуле. Миф про wg из РФ: «из РФ стучаться до RU-сервера по WG обычно работает» [id=578370], «у нас vless на стандартных настройках сочит, ss мертв у многих (до европы), хиста тоже; до RU и wireguard робит» [id=578358].
- **[id=578008, 575475|DAUNAMORAL/Wyatt|24.05.2026]** Селектор IP для атаки: «@selectelgetbot» — бот от Wyatt Haley.

## События-вехи
- **[id=581350, 582321|KR1NGER|25.05.2026]** «У всех сибирь упала?» — массовый отвал TCP Reality по fp (см. выше). То же на РТК и других провайдерах: Rostelecom-пользователи жалуются на «пинг есть, но не подключается» [id=583395].
- **[id=580519|Никита Храмов|25.05.2026]** Remnawave на Windows: «да ремна на винде)» — запуск теста «на винде» [id=581258].
- **[id=582990|e|25.05.2026]** geo.hosting обанкротились («на сайте при входе»).
- **[id=579961|SIKAPE|25.05.2026]** Пост «Пофиксил после отбала в 26.05»: сервера перестали пинговаться после операции в OTel; решение через панель.

## Опыт хостеров (только факты)
- **[id=575853, 575867|мачка|24.05.2026]** Akenai Hosting: Германия (Frankfurt) и Италия (Equinix ML2, Tier 3), Ryzen 9 9950X, DDR5, NVMe, 10G канал; тариф 12.99$/мес (2 vCPU / 4GB DDR5 / 60GB NVMe), FUP на трафик; промокод FIRSTORDER10 (10% на первый месяц), my.akenai.host. Плюс: реалистичный биллинг, дешёвый трафик, IPv6 выключен по умолчанию, BBR выключен.
- **[id=577134|kell|24.05.2026]** play2go.cloud (Швеция): 780 RUB/мес (2 vCPU/4GB/60GB NVMe, HI-LOAD) — «цена не соответствует качеству»: сервер падал, скорость прыгала, стилтайм высокий, гео кривое [id=585696].
- **[id=581697|undr|25.05.2026]** qwins.co (Польша, Варшава): тариф 5$, «пока-что проблем не было, в целом за свою стоимость хорошая тачка». Польский IP qwins: «скорость 50 гбит а на самом деле выдавало 2-3 Гбит», «постоянно парсили трафик» [id=584104]; «Qwins — Эстония — хуйня, не коннектит; Rifty — Германия — хуйня» [id=583613].
- **[id=584104|System Fix|25.05.2026]** Steal time: норма до 5-10%, выше — требовать у поддержки или возврат; «1cent - Польша полет нормальный» [id=583695]; 1cent Эстония: стил не выше 5% [id=583644].
- **[id=584159|—|25.05.2026]** govnohost.net — хетзнер с транзитом Kyonix.
- **[id=584205|Andrey Petrov|25.05.2026]** Leaseweb: 3.6 €/мес, 4 ядра, 6 ОЗУ, 30 ТБ трафика, канал 10 Гбит.
- **[id=584204|Fedya|25.05.2026]** Aeza (Германия 25 гбит, Финляндия 1 гбит): «вроде не жалуются» [id=584166].
- **[id=576863|мачка|24.05.2026]** Финляндия Hetzner: «панель в финке — таймауты в апи», «прокси на серв п2г без отвалов» [id=580788]. Waicore финка: тормозит/лагает [id=582574, 585877].
- **[id=579560|V M|25.05.2026]** Beget.com (СПБ): «ценник чуть выше среднего, но стабильный 1 Гбит и без оверселла. Подходит для моста». Бегет платные IP [id=579332], бесплатно-платные тарифы, рабочий YouTube RU без рекламы.
- **[id=580003|—|25.05.2026]** «Панель и ноду на один сервер пизать это слишком» — но у Тимура на 10 юзеров 2/6/150 всё в одном + P2G 10 Гбит [id=580145]; не для продакшена.
- **[id=584064|—|25.05.2026]** «Экспресс» (ExpressHost): «да все скатился экспресс», «надо было в тесты их выкладывать», у mah1cul у экспресса в Рязани стил <1.5 [id=584022]. NodeHost Польша: скорость тест [id=581612].
- **[id=585634|Vladislav|26.05.2026]** «3hcloud может если без шуток» — с КЗ.
- **[id=585744|—|26.05.2026]** «Штормвалл ±170 Бачей 1 домен», Curator — «даже дешевле выходит» [id=584726].

## Bedolaga/Remnawave (мелочи, но важные)
- **[id=575791|Артём|24.05.2026]** «Бот Бэкапы перестал слать с 14 мая» — причина: в чистом .env не указан IT-чат/топик.
- **[id=576120|—|25.05.2026]** Bedolaga поддерживает MySQL? — «нет», только PG (реально: aiomysql не помогло) [id=583379, 583376].
- **[id=580215|Максим|25.05.2026]** После изменения .env в боте: «Бота надо down-up, чтоб изменения конфига подтянулись. Рестарт не помогает».
- **[id=580254|—|25.05.2026]** Premium-эмодзи в сообщениях бота: файл `/opt/bedolaga/locales/ru.json`, HTML-разметка `<tg-emoji emoji-id="...">☺</tg-emoji>`; для кнопок — админка бота (не веб). Конструкция `=/` и экранирование кавычек `/".../"` — синтаксическая ошибка (Telegram парсер не распознаёт ID) [id=580636].
- **[id=581317|System Fix|25.05.2026]** У некоторых у пользователя лимит 20 ГБ после обновления бота/кабины, хотя в .env и админке стоит 0 — по-видимому, баг; «вышиш нулевые лимиты» нужно в ремне через панель [id=584517].
- **[id=579144|Данил Уваров|25.05.2026]** `bot.log` в `/root/remnawave-bedolaga-telegram-bot/logs/` съедает память — чистить.
- **[id=578024|Виктор|24.05.2026]** YooKassa: «ты в кошельке смотришь, а надо в бизнес кабинете лавы» (выплаты и отчёты).
- **[id=579960|Jordan|24.05.2026]** Требование в боте: ID подключать, ref-программа ТГ.
- **[id=577584|Pavel Kosyakov|24.05.2026]** В Remnawave нет фильтра пользователей по тарифу, только кол-во подписок на тарифе; поиск — в разделе «Пользователи» в фильтре [id=577584].
- **[id=578026|Денис Новосильцев|24.05.2026]** Оптимизация: «ноды защитить их же ресурсами невозможно», можно «минимизировать урон» (автоподбор нод, лимиты).
- **[id=578024|—|24.05.2026]** Улучшение реплики из ремки: ремна-админ (сайт) полезен «много чего» [id=580188].
- **[id=578088|Generating|24.05.2026]** Remna (панель) — триал-период: «Всем разрешают».
- **[id=582017|Sabina|25.05.2026]** При установке/обновлении: «внутри жёстких лимитов до 10-12 мбит, строгости хостера не встречал».

## Платежки (фрагменты)
- **[id=575891, 576069|lonely/снупс|24.05.2026]** Platega работает в боте, в кабине — ошибка при создании платежа (сейчас работает) [id=582326].
- **[id=580008|let mut !solana|25.05.2026]** Про самозанятых и чеки: «алерт» плательщикам.
- **[id=580064|—|25.05.2026]** «Мнений много» по Lavа: «не только о политике».

## Мелочи, багрепорты и советы
- **[id=575023|Хоume|24.05.2026]** Много времени уходит на «халявщиков и людей которые не умеют читать».
- **[id=576470|—|24.05.2026]** Порт в inbound для xhttp — 449.
- **[id=584067|—|25.05.2026]** «Так и будет всегда» — DDoS и нагрузка.
- **[id=576873|—|24.05.2026]** Много эко-платформ: «если хочется что-то настроить».
- **[id=576847|хеуклер|24.05.2026]** Пробовать: «packet up режим» [id=578849].
- **[id=580013|Mr Alex|25.05.2026]** Кошельки: «Я использую вк для анонимности».

## Мифы, которые развенчаны в чате
- **[id=578008|—|24.05.2026]** «По-хорошему надо перейти с xray на mihomo» [id=584149].
- **[id=579918|love.you|25.05.2026]** Remnawave-шаблоны: mihomo работает лучше Xray по скорости обхода на клиентах-айфонах [id=583475].
- **[id=579905|—|25.05.2026]** «Быстро у @ponqp купил акк фрагмента с верифом» [id=579958].

## Прочие вопросы (без решения в чанке)
- «Может кто настроить cron...» [id=575916] — нет решения в чанке.
- «А есть возможность поднять кол-во устройств...» [id=585067] — решение: снеси платные устр в конфиге или с помощью Clod [id=585247].
- «Подскажите пожалуйста где дешево купить иностранный домен...» [id=585217] — нет решения.
- «Кто-нибудь сталкивался с таким что впн не работает на хаппе и все сервера пингуются, но не работает» [id=585096] — фикс fp+grpc, у части не помогло.
- «Правда что сервера из Кз поменяли» [id=584731] — нет решения.
- «Дайте норм хостинг под финку и Швецию пж» [id=585634] — нет решения.

## Скам/гаранты
- **[id=574788|анмбл|24.05.2026]** Список скамеров (@foryoouads @ruhhmen @gayaneyyan @stepnricci @dooorass @bektassvna — «скам реклама»).
- **[id=576782|.|24.05.2026]** @litlle_01 — скамер, «перевел 14 200 ₽ (200$) на номер 89289300029, кинул в блок».
- **[id=578284|murciėlago|24.05.2026]** @whitelists_shop_bot — скам-бот («вставляет в описании ссылки на форум-темы, которые никак к нему не относятся»).
- **[id=584204|Fedya|25.05.2026]** @x5med — «отряд лохов», канал t.me/warframetg, «пишет про рекламу и сливается».
- **[id=582491|Scamgod|25.05.2026]** Custodex (крипто-платежка) — «7 лет на рынке, есть лицензия», менеджер @alex_custodex; оплата комиссий/возврата.
- **[id=583382|Егор (fringg)|25.05.2026]** Предупреждение о фейковых гарантах: «чел ходит по ЛС, предлагает убер вкусные варианты, скидывая моего фейк гаранта... внимательно чекайте юзернейм, хуесос мой юзернейм втыкает в поле „О себе“. Профиль, подарки — все скопировано».
- **[id=584511|—|26.05.2026]** «отказ от гаранта = автоматический блок».
- **[id=585124|—|26.05.2026]** По китайцу: «Походу только на дальнем востоке и Сибири».

## Опыт регистрации
- **[id=574966|—|24.05.2026]** Регистрации в RU: «Привет, я тут по 25.05 прошёл регистрацию».
- **[id=585024|—|26.05.2026]** «Регистрация: vk, домены».

## Соц-факты (вне темы, но полезно)
- **[id=580193|—|25.05.2026]** «Планирую всех кто юзает подключать — новый месяц новый аккаунт» — Yandex grants.
- **[id=581353|—|25.05.2026]** «Работа через毛泽» — на личный счёт.
- **[id=580199|—|25.05.2026]** MWS — «мws всё тянет на себе» (домашний RDP).
