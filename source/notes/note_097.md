# Заметки из chunk_097 (id 653222..662098, 07.06.2026..09.06.2026)

## Веха: массовая зачистка VPN «БСЫ ВСЁ» (08.06.2026)
- **[id=653866/657613/656811|—/Scamgod/PEpeSan|08.06.2026](https://t.me/c/2941121338/653866)** РКН начал беспрецедентно жёсткую зачистку VPN: перебои не только из-за ТСПУ, но и из-за DDoS-атак на сервера VPN-сервисов. Одновременно nLighten без предупреждения отключила оборудование хостинга MIRhosting в Нидерландах и Германии — посыпались десятки VPN-провайдеров. mchost, HostVDS, VDSina — жёсткие блоки; THE.Hosting закрылся из-за изъятия серверов. Фикс для MTProto оказался нерабочим — прокси Телеграма всё ещё уязвимы перед ТСПУ. Некоторые сервисы не могли оправиться третий день.
- **[id=653844/659195|—|08-09.06](https://t.me/c/2941121338/653844)** Intezio (Нидерланды) — сутки лежало, потом «не можем восстановить». В итоге пред. оценка: интезио было говном и осталось.
- **[id=657350/657365/659502|—|08-09.06](https://t.me/c/2941121338/657350)** Точечные/региональные удары РКН по IP: сервер жив (ssh, панель, логи чистые), но VPN умирает; помогает только смена IP. «На этом же IP хистерия работает — это не удар по IP».
- **[id=657478|compact disc|08.06.2026](https://t.me/c/2941121338/657478)** СМИ: РКН хочет сделать «госVPN» для российских компаний (доступ к Figma, GitHub, PyPI, нейронкам). Обсуждение: протокол — WireGuard; юмор-расшифровка «Программа Доступа к Зарубежным Ресурсам».
- **[id=660750/660750|rm -rf /|09.06](https://t.me/c/2941121338/660750)** ру-хостеры все под блоками — даже обычные сайты без VPN перестают работать.

## Selfsteal (свой SNI) — гайд и конфиг
- **[id=653860..653903|Данил/R0xTaDDy|08.06](https://t.me/c/2941121338/653860)** Скрипт: https://github.com/DigneZzZ/remnawave-scripts/blob/main/README-selfsteal.md. Важно: target/dest = `127.0.0.1:9443`, SNI = СВОЙ домен (селфстил), а не google/yahoo. У кого «сервер пингуется но выхода нет» — в хосте/host обязательно убрать поле Host (в конфиге клиента host должен быть пуст).
- **[id=657615|Shaban Ramazanow|08.06](https://t.me/c/2941121338/657615)** Пример неисправного inbound (grpc reality dest=www.microsoft.com) — контекст: после зачистки с внешними SNI начали падать; переход на селфстил — рабочий ответ:
  ```json
  "realitySettings": { "dest": "127.0.0.1:9443", "serverNames": ["свой-домен"], "xver": 1, "target": "/dev/shm/nginx.sock" }
  ```
- **[id=657198/657361|Jordan/isq|08.06](https://t.me/c/2941121338/657198)** Рабочий клиентский selfsteal vless-xhttp-reality (порт 47222, mode auto, path /, xPaddingBytes 100-1000, headers Chrome, target yahoo.com:443 пока не заменён; dns fakedns; domainStrategy IPIfNonMatch; finalmask udp noise 64-128 count 3-5; policy bufferSize 512) — «наглоспизженный конфиг» из чата, работает как xhttp+reality.
- **[id=659018/659008|ETERNAL|09.06](https://t.me/c/2941121338/659018)** Резкая критика тех, кто до сих пор ставит SNI yahoo/max/yandex/vk — «кладбище айпишников», надо уходить на selfsteal/steal one-self (свой домен). Поиск по чату по «селфстил».
- **[id=659020/659010|Тимур|09.06](https://t.me/c/2941121338/659020)** RealiTLScanner: https://github.com/XTLS/RealiTLScanner — поиск TLS/SNI под подделку.

## Hysteria2 — рабочие конфиги
- **[id=656737|Роман|08.06](https://t.me/c/2941121338/656737)** Каскад hysteria inbound → outbound VLESS reality (FIN):
  ```json
  {"tag":"HYSTERIA-BBR","port":443,"listen":"0.0.0.0","protocol":"hysteria","settings":{"clients":[],"version":2},
   "streamSettings":{"network":"hysteria","security":"tls",
     "finalmask":{"quicParams":{"debug":false,"congestion":"bbr"}},
     "tlsSettings":{"alpn":["h3"],"serverName":"","certificates":[{"keyFile":"/etc/letsencrypt/live/<домен>/privkey.pem","certificateFile":"/etc/letsencrypt/live/<домен>/fullchain.pem"}]},
     "hysteriaSettings":{"version":2}},
   ...outbounds: VLESS_FI (vless reality shortId 6b325db628f53100, fingerprint firefox, network tcp), DIRECT, BLOCK,
   routing: private+bittorrent BLOCK; {type field, domain:[soundcloud.com, geosite:youtube], inboundTag:[HYSTERIA-BBR], outboundTag:"DIRECT"}; {type field, inboundTag:[HYSTERIA-BBR], outboundTag:"VLESS_FI"}}
  ```
- **[id=658318|—|09.06](https://t.me/c/2941121338/658318)** Hysteria2 inbound с masquerade (маска под cloudflare):
  ```json
  {"tag":"HYSTERIA2-UDP-443","listen":"0.0.0.0","port":443,"protocol":"hysteria",
   "settings":{"version":2,"users":[]},
   "streamSettings":{"network":"hysteria","security":"tls",
     "tlsSettings":{"serverName":"hy2.example.com","certificates":[{"certificateFile":"/etc/letsencrypt/live/hy2.example.com/fullchain.pem","keyFile":"/etc/letsencrypt/live/hy2.example.com/privkey.pem"}]},
     "hysteriaSettings":{"version":2,"udpIdleTimeout":60,"masquerade":{"type":"proxy","url":"https://www.cloudflare.com","rewriteHost":true}}},
   "sniffing":{"enabled":true,"destOverride":["http","tls","quic"]}}
  ```
- **[id=656368/656462|Антон Кривченков|08.06](https://t.me/c/2941121338/656368)** Вопрос по hysteria inbound в логах ноды и порту 443 vs любой UDP — hysteria работает только с сертами (выпустить letsencrypt на домен), UDP порт любой.
- **[id=657759|suharik|08.06](https://t.me/c/2941121338/657759)** «какой гайд по хистерии?» — ссылку не дали, в чате разводили на 200$ (Леш Лешич).
- **[id=658371|kataomi|09.06](https://t.me/c/2941121338/658371)** Фикс «онлайн не отображается на Hysteria2» (ядро 26.3.27 не видит онлайн/трафик) — обновить Xray-core вручную:
  ```bash
  mkdir -p /opt/remnanode/custom-xray && cd /opt/remnanode/custom-xray
  apt update && apt install unzip -y
  wget https://github.com/XTLS/Xray-core/releases/download/v26.6.1/Xray-linux-64.zip
  unzip -o Xray-linux-64.zip
  nano /opt/remnanode/docker-compose.yml   # добавить в volumes:
  #   - '/opt/remnanode/custom-xray/xray:/usr/local/bin/xray:ro'
  cd /opt/remnanode && docker compose down && docker compose up -d && docker compose logs -f -t
  docker exec -it remnanode xray version
  ```
  Откат — удалить строку из volumes и пересобрать.
- **[id=660506|INCY|09.06](https://t.me/c/2941121338/660098/660506)** INCY план: AmneziaWG и olcrtc в следующей версии; поддерживает VLESS, VMess, Trojan, Shadowsocks, Hysteria2, SOCKS5, WireGuard.
- **[id=659037|c0mrade|09.06](https://t.me/c/2941121338/659037)** INCY использует DNS из вашего json профиля; Happ свой DNS не читает и юзает Cloudflare.
- **[id=660623/660625|INCY|09.06](https://t.me/c/2941121338/660098/660623)** Пинг INCY по TCP по умолчанию, Happ — HTTP; в INCY поставить HTTP-пинг — цифры будут как в Happ.

## Клиентский роутинг на РУ-сервисы (главные знания)
- **[id=653971/653977/654001|—/Руслан Иванов|08.06](https://t.me/c/2941121338/653971)** Серверный routing с leastPing балансером (RUMSK/RUNSK inbounds → balancer → fallback DIRECT):
  ```json
  "routing": {"rules":[
    {"ip":["geoip:private"],"outboundTag":"BLOCK"},
    {"protocol":["bittorrent"],"outboundTag":"BLOCK"},
    {"domain":["geosite:youtube"],"outboundTag":"DIRECT"},
    {"domain":["geosite:category-ru"],"outboundTag":"DIRECT"},
    {"ip":["geoip:ru"],"outboundTag":"DIRECT"},
    {"inboundTag":["RUMSK_VLESS_INBOUND","RUMSK_Trojan_Inbound","RUNSK_VLESS_INBOUND","RUNSK_Trojan_Inbound"],"balancerTag":"Balancer"}],
   "balancers":[{"tag":"Balancer","selector":["PROXY"],"strategy":{"type":"leastPing"},"fallbackTag":"DIRECT"}],
   "domainStrategy":"IPIfNonMatch"}
  ```
  Плюс вариант с огромным списком доменов VK/OK/Mail/Dzen/Sber/Ozon/Avito/T-Bank/WB/Yandex/VTB/Alfa/RZD/Pochta/Gosuslugi/X5/HH в outboundTag «direct» (клиентский json; правда «засерает память клиента»).
- **[id=654086/654050|Руслан Иванов|08.06](https://t.me/c/2941121338/654086)** Рекомендация: на клиенте в директ заводить не весь geosite:ru, а только те сервисы, которые реально не пускают с VPN (банки/озон/вк). Полные внешние роутинги типа RoscomVPN несовместимы/каша с серверным geosite. Клиентские конфиги не переносят жирные геофайлы — память уходит.
- **[id=653987|Руслан Иванов|08.06](https://t.me/c/2941121338/653987)** Сервисы «стучатся» из-за TUN-интерфейсов: приложения видят VPN. ВТБ палит VPN через `back.vtb.fp.f6.security` (антифрод-домен); озон/вк/макс при этом работают.
- **[id=654002/654001|Руслан Иванов|08.06](https://t.me/c/2941121338/654002)** Роутинг для ПК-клиента с запретом VPN-детекта — «Роутинг ВСЕ» — составлен в значительной мере из доменов этого чата.
- **[id=654111|Руслан Иванов|08.06](https://t.me/c/2941121338/654111)** Дока ремны: https://docs.rw/docs/learn/node-plugins (плагины для торрентов и пр.).
- **[id=655894/656803|Руслан Иванов|08.06](https://t.me/c/2941121338/655894)** Команда для проверки, куда уходит трафик на ноде (для отладки роутинга):
  ```bash
  docker exec -it remnanode tail -f /var/log/supervisor/xray.out.log | grep -- "->"
  ```
  Обязательно включить logging в json.
- **[id=656856/656853|Руслан Иванов|08.06](https://t.me/c/2941121338/656856)** Если правило не сработало — в inbound добавить:
  ```json
  "sniffing": {"enabled": true, "routeOnly": false, "destOverride": ["http","tls"]}
  ```
  (quic можно тоже). DNS-серверы для проверки: `77.88.8.8` + `1.1.1.1`, `queryStrategy: "UseIP"`, `domainStrategy: "IPIfNonMatch"`.
- **[id=656506|bypara|08.06](https://t.me/c/2941121338/656506)** Простой Xray JSON для домена платёжки в DIRECT (чтобы лаве антифрод не мешал):
  ```json
  "routing": {"rules":[{"type":"field","domain":["domain:lava.ru"],"outboundTag":"direct"}]}
  ```
  Применение: Subscription → Templates → Xray JSON → создать/в default; Хост → Advanced → Xray json RAW (получается «Host → Расширенное → шаблон xray json»).
- **[id=656539|eth|08.06](https://t.me/c/2941121338/656539)** Проверка lava.ru по операторам (мульти IP проверка): beeline/megafon/mts/tele2/t-mobile — ICMP 0/3, TCP 0/3, HTTP ✗ ( lava.ru полностью в блоке).
- **[id=656787/658217|ｈａｒａｊｕｋａ/—|08-09.06](https://t.me/c/2941121338/656787)** MAX-мессенджер: директить без впна; `max.ru` через каскад не грузится.
- **[id=658561|витяⓂ️🅱️а|09.06](https://t.me/c/2941121338/658561)** Клиентский роутинг на БС (замена geosite:ru на regexp, чтобы не тянуть тяжёлый геофайл):
  ```json
  {"type":"field","domain":["geosite:category-ru","regexp:\\.ru$","regexp:\\.xn--p1ai$","regexp:\\.su$"],"outboundTag":"DIRECT"}
  ```
- **[id=655921/655953|Тимур|08.06](https://t.me/c/2941121338/655921)** Если геофайлы/шаблон сломаны чужим «хапп роутингом»: удалить geosite:ru из xray json и написать regexp для `.ru/.su/.рф (xn--)`; `geoip:ru` тоже убрать. На ноду накатить https://github.com/dotX12/traffic-guard чтобы банить ASN чекеров и государства.
- **[id=658021/658086/658118|Scamgod|08.06](https://t.me/c/2941121338/658021)** WARP на ноду для Gemini — маршрутизация:
  ```json
  {"routing":{"rules":[{"type":"field","domain":["gemini.google.com","generativelanguage.googleapis.com","ai.google.dev","aistudio.google.com"],"outboundTag":"warp"}]}}
  ```
  есть готовый geosite: `geosite:GOOGLE-GEMINI`.
- **[id=657752|Frist|08.06](https://t.me/c/2941121338/657752)** Ютуб через ру-ноду без впн: `cdn → cloud.ru → eu` (Cloud.ru как мост).

## CDN-обход БС (мануалы, что продают — «суть»)
- **[id=653372/654417/654477/655750/655835/656048/656620/657620|—|08.06](https://t.me/c/2941121338/653372)** На рынке перепродажа гайдов «Настройка CDN» (Yandex/MWS(MТС)/CDNVideo/Selectel/Beget/Timeweb/Beeline) 15–45$, принципы во всех гайдах одинаковые: НЕ PUT и НЕ POST (CDN провайдеры режут PUT/POST автоматически), т.е. только GET/HEAD; настроить хосты, конфигурацию, прокси, CDN+DNS у двух провайдеров (основное Yandex + резерв MWS); трафик ~0.8–1₽/ГБ; гранты 4 ТБ+; настройка ~1 час; скорость до 500 Мбит/с. MWS: кабинет должен быть зарегистрирован более 4–5 дней назад (свежие кабинеты не подходят). CDNvideo нестабилен при большой выгрузке.
- **[id=655085/656876/656484|—|08.06](https://t.me/c/2941121338/655085)** Яндекс CDN методы: только GET/HEAD/OPTIONS, PUT недоступен. ЦДН провайдеры режут PUT и POST автоматически.
- **[id=654844/656844|bypara/eth|08.06](https://t.me/c/2941121338/654844)** Пример конфигурации обхода с CDN (порт, домен, серты). БС-операторы (МТС) - отдельная песня: «CDN не обходится, если на йоте/МТС — работает», «CDN → когда сети Белые/Чёрные списки».
- **[id=660372/660382|Дмитрий Шатов|09.06](https://t.me/c/2941121338/660372)** Lava добавила домен `pay.lava.ru` (запрос в тех.поддержку), плаc рекуррентные платежи в приоритете, потом иностранки и карты.
- **[id=660074/660122|—|09.06](https://t.me/c/2941121338/660074)** Рекомендация домен платежки (lava) под CDN вывести, чтобы в белые списки не попадал; домен под VPN нельзя — антифрод сработает.

## Бедолага/Remnawave: баги и фиксы
- **[id=653280|kurskyy|07.06](https://t.me/c/2941121338/653280)** `PermissionError: [Errno 13] Permission denied: '/app/data/backups'` — проверять права на `/app/data/backups` (монтируемая директория).
- **[id=654847|kurskyy|08.06](https://t.me/c/2941121338/654847)** Ошибка Platega: `Wrong input parameters ... Return/FailedUrl is not a valid absolute URL` → указать валидный абсолютный URL в кабинете (не localhost, полный https://).
- **[id=655191/655109|kurskyy/Фёдор Сирош|08.06](https://t.me/c/2941121338/655191)** Не применяются цены в периодах подписки → закомментировать прайс в `.env`, пересобрать бота, менять цены уже в кабинете/боте:
  ```bash
  docker compose down && docker compose up -d --build && docker compose logs -f
  ```
- **[id=657698|𝙠𝙞𝙣𝙜𝙥𝙞𝙣|08.06](https://t.me/c/2941121338/657698)** Миграция при апгрейде бота 3.46.1 → 3.60.0 падает: `DuplicateTableError: relation "paypear_payments" already exists` (alembic stamp не помогает).
- **[id=659376|kifchan|09.06](https://t.me/c/2941121338/659376)** После патча кнопка оплаты в боте имеет дефолтное имя, в кабинете — правильное; в кабинете одна юкасса, в боте две (баг).
- **[id=659215|буллингов|09.06](https://t.me/c/2941121338/659215)** Юкасса: оплата проходит, но бот не фиксирует.
- **[id=661994/662075|yng dev Zover|09.06](https://t.me/c/2941121338/661994)** Lava: оплата работает через бота, но НЕ работает через кабинет (файл в баги). Причина: на сабке другая `init data`/host.
- **[id=659376|kifchan|09.06](https://t.me/c/2941121338/659376)** Проблема с чекером HWID: платная подписка не активируется если платить юкассой (фича ограничения).
- **[id=654477|Андрей Ингинен|08.06](https://t.me/c/2941121338/654477)** Ползунок «Автопродление» в админке — просьба, чтобы не менять значение в БД. Вручную выданные дни на суточный тариф все равно списывают плату (баг).
- **[id=654093|Alexander|08.06](https://t.me/c/2941121338/654093)** Фича-запрос: WhiteList email адресов при регистрации в кабинете (не temp mail); лучше чёрный список с regex или проверка почтового сервера (Andrey Ингинен).
- **[id=657611|Chara Freedom|08.06](https://t.me/c/2941121338/657611)** Фича-запрос: конверсия тарифа без сохранения дней (бесплатная 0₽ может быть продлена на годы вперёд, конверсия в платный тариф всегда сохраняет дни).
- **[id=661917|Fisk|09.06](https://t.me/c/2941121338/661917)** Сделать надпись «подтвердите почту» скрытой, если проверка почты отключена.
- **[id=661898|Fisk|09.06](https://t.me/c/2941121338/661898)** Не показывать кнопку/страницу «подтверждение email», если опция выключена.
- **[id=661116| mah1cul|09.06](https://t.me/c/2941121338/661116)** В кабинете у 0001 сабку сливали по КД (слитая сабка).
- **[id=660084|Ня абузерша|09.06](https://t.me/c/2941121338/660084)** Перенос eGames панели: новый сервер, домен на новый, ставим панель с 0, восстанавливаем бэкапом, меняем на нодах доступ (2222 порт) со старого IP панели на новый. Серты на old домены подвязать. Скрипт: https://github.com/distillium/remnawave-backup-restore — фулл-бекап /opt/remnawave.
- **[id=659893|Руслан Иванов|09.06](https://t.me/c/2941121338/659893)** Правильный nginx vhost для subscription-page:
  ```nginx
  location / { proxy_pass http://remnawave-subscription-page:3010; include /etc/nginx/conf.d/proxy.conf; }
  ```
  docker-compose service с healthcheck `curl -f http://localhost:3010/`, depends_on remnawave: condition service_healthy.
- **[id=659906|Руслан Иванов|09.06](https://t.me/c/2941121338/659906)** Ошибка `Reverse proxy and HTTPS are required` от subscription-page — healthcheck был на внешний адрес, надо на localhost.
- **[id=658347|—|09.06](https://t.me/c/2941121338/658347)** Название кнопки «Публичная оферта» и др. в боте меняется в админке/в коде (не через UI).
- **[id=660090|—|09.06](https://t.me/c/2941121338/660090)** Автоматически уведомлять юзеров, не активировавших триал: локали TRIAL_INACTIVE_1H/TRIAL_INACTIVE_24H есть, настройки нет (на момент чанка).
- **[id=661136|—|09.06](https://t.me/c/2941121338/661136)** Remna API: присвоение хоста к ноде:
  ```bash
  curl -X PATCH "$REMNA_API_BASE_URL/api/hosts" \
    -H "Authorization: Bearer $REMNA_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"uuid":"<host-uuid>","nodes":["<node-uuid>"]}'
  ```
- **[id=659404|kataomi|09.06](https://t.me/c/2941121338/659404)** Виртуальный хост (виртуальный сервер) в Remna — обёртка для шаблона и метаданных (примечание/описание); реальная точка входа — инбаунд инжектнутых хостов; нужен сквад у юзера, иначе вирт.хост не отобразится в сабке; outbound-конфиги подставляются в итоговый клиентский конфиг.
- **[id=659864|aegri somnia|09.06](https://t.me/c/2941121338/659864)** Полный клиентский json — server raw reality + nginx.sock (зарубежный узел):
  ```json
  "streamSettings":{"network":"raw","sockopt":{"tcpMaxSeg":1440,"tcpNoDelay":true,"tcpFastOpen":true,"tcpcongestion":"bbr","tcpKeepAliveInterval":30},"security":"reality","realitySettings":{"xver":1,"target":"/dev/shm/nginx.sock"}}
  ```
  РУ-нода grpc reality target 127.0.0.1:8443 + `"injectHosts":{"tagPrefix":"proxy"}` (xray PR 6258 merged: https://github.com/XTLS/Xray-core/pull/6258).
- **[id=661179|—|09.06](https://t.me/c/2941121338/661179)** Ремна для одной панели может обслуживать несколько ботов/кабин (мульти-бот интеграция).
- **[id=655928|—|08.06](https://t.me/c/2941121338/655928)** «Убрать ID из ссылки подписки»: только через бек переделывать; и юзер UUID должен быть; HWID всё равно работает.
- **[id=657750|Vladislav|08.06](https://t.me/c/2941121338/657750)** «Взял flutter, написал приложение на 2 платформы» — про INCY; у него до Windows-пре-альфы в приоритете.
- **[id=660505|—|09.06](https://t.me/c/2941121338/660098/660505)** Remna не умеет передавать hysteria2 в mihomo (доклад ремна), фикс: настроить шаблоны сабок, чтобы передавались правильным ядрам (Дима, 2.8).
- **[id=661187|—|09.06](https://t.me/c/2941121338/661187)** Описание нод/заголовки под хостами — в Remna в хосте «Расширенные → Server Description».
- **[id=661895|Mah1cul|09.06](https://t.me/c/2941121338/661895)** «Мульти-тест» — скрипт saveks, лёгкий, одним снипетом; идею со скриншотами реализует.
- **[id=660560|—|09.06](https://t.me/c/2941121338/660098/660560)** INCY и Happy: дизайн и фичи; в INCY входит pin TCP/HTTP ping, поддерживает почти все протоколы; сейчас в INCY реализовано амнезия-подобное при использовании RKN: были фиксы через ДПИ.

## Инструменты и репозитории
- **[id=654142|Immanuel|08.06](https://t.me/c/2941121338/654142)** База знаний по чату (obsidian): https://github.com/immanuel1618/BedolagaSocialClub_README ; консилиум: https://github.com/immanuel1618/consiliumVPNBedolagaSocialClub
- **[id=655073/654993/658538|—|08.06](https://t.me/c/2941121338/655073)** Скрипты и доки: https://github.com/DigneZzZ/remnawave-scripts (selfsteal), https://github.com/x1roko/node-setup (скрипт), https://github.com/distillium/remnawave-backup-restore, https://github.com/Chivas600/Bedolaga-Backup-Update, https://github.com/XTLS/Xray-core/pull/6258 (injectHosts).
- **[id=655663/654580|—|08.06](https://t.me/c/2941121338/655663)** beszel — панель мониторинга (github), для онлайн/скора/нагрузки.
- **[id=654919|Бедолага|08.06](https://t.me/c/2941121338/654919)** Реклама bedolaga: remnawave/panel, BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot, BEDOLAGA-DEV/bedolaga-cabinet, kutovoys/xray-checker, eGamesAPI/remnawave-reverse-proxy, Jolymmiels/remnawave-telegram-shop, machka-pasla/remnawave-tg-shop, DigneZzZ/remnawave-scripts, distillium/remnawave-backup-restore, maposia/remnawave-telegram-sub-mini-app, legiz-ru/my-remnawave, dotX12/traffic-guard. Партнёрства: Platega (@ArstanPlatega), RollyPay (rollypay.io, @sasha_rollypay).
- **[id=658845|Allison Burgers|09.06](https://t.me/c/2941121338/658845)** chebur.me/tools — инструменты: репутация IP/URL по спискам РКН, проверка MTProto без мостов (реальный хендшейк), WhatsApp-прокси, порты почты (25/587/465, PTR, EHLO+STARTTLS), IPregion (как регион определяют ip-api/ipinfo/Cloudflare), бенчмарк (iperf3 до РФ и зарубежных), CensorCheck. Аналоги: cheburcheck.ru, check-host.net.
- **[id=658471|—|09.06](https://t.me/c/2941121338/658471)** Happ security login: https://happ-proxy.com/security/login (покупка Happ Premium ~1000₽).
- **[id=660774|Мультитысячник|09.06](https://t.me/c/2941121338/660774)** Спам-сервис «универсальный IP — 40$ Yandex + MWS CDN».
- **[id=658768|—|09.06](https://t.me/c/2941121338/658768)** INCY Releases: https://github.com/INCY-DEV/incy-platforms/releases/tag/desktop-v3.2.2 (Win пре-альфа).

## Хостинги и VPS — факты опыта
- **[id=654425/654429/654433|—|08.06](https://t.me/c/2941121338/654425)** Beget (КЗ/СПб) под панель/бота: 1150₽ за 2/4/40, дорогой но не падает; снапшоты бесплатные; недавно падал ~40-60 мин.
- **[id=654451|Vladislav|08.06](https://t.me/c/2941121338/654451)** На Timeweb: только через прокси прокинуть, цены заоблачные.
- **[id=654427|Камушек|08.06](https://t.me/c/2941121338/654427)** Под бота берут в КЗ.
- **[id=655755|undr|08.06](https://t.me/c/2941121338/655755)** Clouvider (реф) Нидерланды: AMD EPYC 7313 1vCPU, 2GB RAM, 50GB NVMe, 5ТБ (счёт в обе стороны), 4.05€/мес; порт 10Гбит (в пике ~7.5), 100% NL по гео, до РФ ~3-4 гбит, stealtime 0.0-0.7.
- **[id=657122|undr|08.06](https://t.me/c/2941121338/657122)** Alwyzon (alwyzon.com) Австрия: EPYC 7534P 2 vCPU, 2GB RAM, 40GB SSD NVMe raid10, 20ТБ (счёт в обе стороны), 4.49€/мес; 100% Австрия, до РФ ~3-5 Гбит, stealtime 0.
- **[id=656425/656415/658007|Ня абузерша/хеуклер/—|08.06](https://t.me/c/2941121338/656425)** NodeHost: Швеция/Финляндия — мусор (50 Мбит аплоад, лаги top), Польша 10 Гбит — стабильно 1 Гбит аплоад 2-3 Гбит загрузка; выбор при покупке AFRINIC или RIPE IP — лучше RIPE (+0.20$). Новые сервера хуже по скорости; «10 серверов за сутки + стрессер = IPs в блоке».
- **[id=659332/659828|—|08-09.06](https://t.me/c/2941121338/659332)** Хостап сеть у Нодхоста; Intezio — другое (не имеют своей аснки).
- **[id=655663|scruim|08.06](https://t.me/c/2941121338/655663)** NETGRID HOST LTD (Нидерланды): Xeon E5-2673 v4 1 vCPU, 1GB RAM, 10GB SSD KVM, ~290 MB/s, BBR, AES-NI, 500+ мбит до ЕС, до Москвы до 460, до СПб до 220, ping до РФ 40-80; Very Low риск, VPN/Proxy детект не сработал; ChatGPT/Gemini/TikTok/Netflix/YouTube Premium/Telegram API/Spotify/Reddit работают; Disney+ — нет; цена $2. Отзывы: нетгрид параша.
- **[id=658012|Ня абузерша|08.06](https://t.me/c/2941121338/658012)** Селектел: ~27₽/сутки, 300 Мбит, burst 1 Гбит.
- **[id=657505|Frist|08.06](https://t.me/c/2941121338/657505)** 🏷 selectel.ru Питер 250₽/мес, под мост заебись; МСК не берите — по ssh не коннектится (на МСК ТСПУ жёстко сильнее); 3ТБ ИСХОДЯЩЕГО трафика. vds.selectel.ru: анлим трафик, гарантированный 1 Гбит, 2/4/40 ~1600₽/мес; selectel.ru: 3ТБ исходящего + обновление после оплаты 300₽.
- **[id=659146|yng dev Zover|09.06](https://t.me/c/2941121338/659146)** до 12 ТБ расхода в мес выгоднее selectel.ru (при 300₽); vds.selectel.ru — тру анлим с выделенкой 1 Гбит.
- **[id=657594|Kemp|08.06](https://t.me/c/2941121338/657594)** Аккаунты с белым IP, 1 vCPU/0.8GB/100 Мбит (upgrade до 300 Мбит/16 vCores/32GB) — 800$ за штуку.
- **[id=656339|scruim|08.06](https://t.me/c/2941121338/656339)** sprinthost.ru/tariffs/vds — хост в блоке.
- **[id=658802/658803|Girlsense|08.06](https://t.me/c/2941121338/658802)** Сервхост / Клаудрикс — альтернативы; Бегет жрёт денег много (~50₽/день белого, ~27₽ на реальный).
- **[id=658100|—|08.06](https://t.me/c/2941121338/658100)** Локация «Италия» — нет.
- **[id=661240|Хочу руль|09.06](https://t.me/c/2941121338/661240)** Netcup — выдали сервер, он не работает, но в панели пишут что работает.
- **[id=661243|artem|09.06](https://t.me/c/2941121338/661243)** Пол CPU у нодхоста крадут; поддержка поебать.
- **[id=661726|MA|09.06](https://t.me/c/2941121338/661726)** Бегет МСК штормит — меняли сервер и IP.
- **[id=661202|hugo|09.06](https://t.me/c/2941121338/661202)** 💩 qwins.co: заявленные 50Гбит → в реале ~5 Гбит; fair-use 2ТБ/нед, дальше 1 Мбит на 3 дня; выделенная полоса 1 Гбит за 140$; steal ~40 стабильно. «полная hueta».
- **[id=661574|—|09.06](https://t.me/c/2941121338/661574)** Pgon и Zarub делают prepaid карточки; Zarub — 8 баксов, «проходная».
- **[id=660372|eternal|09.06](https://t.me/c/2941121338/660372)** «Селектел — 3 ип на машине, 1 в блоке, 2 ок» — парция 60к р (Majordomo уник).
- **[id=660374|—|09.06](https://t.me/c/2941121338/660374)** Локация «Италия» — нет.
- **[id=660963|деп|09.06](https://t.me/c/2941121338/660963)** Криптовалюта — лучший вариант, но для подписки — удобнее платёжка.
- **[id=660964|увед|09.06](https://t.me/c/2941121338/660964)** IHC OpenVZ (контейнер) с БС.
- **[id=661004|—|09.06](https://t.me/c/2941121338/661004)** IHC: канал 200Мбит, конфигурация 1/1, 2ТБ трафик + 300₽/100ГБ; подсети 46.254.16, 46.254.18 (35к и 45к).
- **[id=658721|—|08.06](https://t.me/c/2941121338/658721)** Информація: У меня 2 ноды конфликтуют при запуске докера — потому что из-за одной строки в env указаны обе ноды (родное поведение — docker compose down/up стартует обе).
- **[id=661991|—|09.06](https://t.me/c/2941121338/661991)** Ошибка ufw: `Chain 'ufw-user-forward' does not exist` (iptables-restore v1.8.10 nf_tables) — сбой правил.
- **[id=661566|—|09.06](https://t.me/c/2941121338/661566)** «Хетзнер криптокарту фродит» — верификация при оплате.
- **[id=660507|—|09.06](https://t.me/c/2941121338/660098/660507)** Оплатить VPS: зарубежная карта (Bybit/KuCoin/PayPal/Bybit+VISA 40$), кента 50-60$/неделя, Bybit вериф с казах номером.
- **[id=659190|Grigory|09.06](https://t.me/c/2941121338/659190)** nLighten/MIRhosting — пиздец; «хостап в бане подсетки».
- **[id=659519|Grigory|09.06](https://t.me/c/2941121338/659519)** AKENA из «Германия/Италия» — на GSL пиздов выдал, большая жопа, потом компенсации.
- **[id=661440|—|09.06](https://t.me/c/2941121338/661440)** mчost у аезы.гг был похожий баг.
- **[id=660576|—|09.06](https://t.me/c/2941121338/660098/660576)** Мст говно.
- **[id=660719|шв|09.06](https://t.me/c/2941121338/660719)** Швеция: HostUp (швеция в блоке), NetGrid (Болгария/Чехия), Rifly (Германия), Infomaniak (Швейцария), VPSpace (Финляндия) — рекомендации.
- **[id=661524|—|09.06](https://t.me/c/2941121338/661524)** Хостинги без моста: Akenai (милан падал), Nodhost.
- **[id=661625|—|09.06](https://t.me/c/2941121338/661625)** «Мониторинг онлайна/скорости/нагрузки»: панели на beszel; но кто-то предложил Vpn Control в Google Play.

## Платёжки и монетизация
- **[id=656868|Дмитрий Шатов|08.06](https://t.me/c/2941121338/656868)** Lava: у некоторых мерчантов не генерируется QR-код — антифрод режет генерацию, т.к. запросы с одного IP. Решение: домены `lava.ru` в клиентский роутинг (как сервисы Яндекса).
- **[id=656539/656481|eth|08.06](https://t.me/c/2941121338/656539)** lava.ru мульти IP проверка — все операторы полностью в блоке.
- **[id=660396|Дмитрий Шатов|09.06](https://t.me/c/2941121338/660098/660396)** Лава: сначала рекуррентные платежи, потом иностранки, потом карты.
- **[id=660572|Дмитрий Шатов|09.06](https://t.me/c/2941121338/660098/660572)** «Либо к нам на 3% по СБП и 6% по картам» (Platega).
- **[id=660398|Виктор|09.06](https://t.me/c/2941121338/660398)** Платега: 10% + 8-9% на конвертации RUB→USDT + курс рапиры (лучше ЦБ РФ).
- **[id=660847|Женя|09.06](https://t.me/c/2941121338/660847)** Платега: вывод на карту есть; вывод TRC20/ERC20.
- **[id=659192|Куvalda Manager|09.06](https://t.me/c/2941121338/659192)** Оплата Lava: подключил ключи, в кабинете нет; оплата проходит, но баланс не начисляется.
- **[id=658532|—|09.06](https://t.me/c/2941121338/658532)** СберИди — нужен для гранта Яндекс Клауд.
- **[id=655366|compact disc|08.06](https://t.me/c/2941121338/655366)** Для Японии Contabo, для Сингапура ovh/contabo; ovh лучше — без верифа и перекупов, сам беру.

## Прочие знания
- **[id=653326|Andrey|07.06](https://t.me/c/2941121338/653326)** МегаФон/Yota: в APN выставить протокол IPv4 и поймать IP из подсети 178.176.х.х — даже при ограничениях интернета доступны все ресурсы, включая БС.
- **[id=654354|—|08.06](https://t.me/c/2941121338/654354)** MTU 1440 на активном интерфейсе — фикс для «с мобильного ожило» (совет от Дмитрия).
- **[id=654418|mah1cul|08.06](https://t.me/c/2941121338/654418)** Speedtest на большом объёме (200 ТБ ≈ 300 юзеров, avg 0.8 ГБ/юзер) — «любители погонять спидтесты на гигабитном аплинке только капля в море».
- **[id=657782|Stas Vlasov|08.06](https://t.me/c/2941121338/657782)** Ufw — «антисканер» ufw.
- **[id=656828|—|08.06](https://t.me/c/2941121338/656828)** МТProto больше не работает: Telegram прокси режутся ТСПУ; вариант — свой tgws на роутере для частного использования.
- **[id=657884|—|08.06](https://t.me/c/2941121338/657884)** На «своем» VLAN ютуб режется.
- **[id=656832|darkdragon|08.06](https://t.me/c/2941121338/656832)** «happ cryptolink ломает любой бот» (спорно — Фёдор Сирош: 2 месяца работало ок).
- **[id=657786|—|08.06](https://t.me/c/2941121338/657786)** «Vpn control в google play» — для IOS.
- **[id=658506|—|09.06](https://t.me/c/2941121338/658506)** Bedolaga-bot URL trigger: TRAIL_INACTIVE_1H/TRIAL_INACTIVE_24H.
- **[id=660506|—|09.06](https://t.me/c/2941121338/660098/660506)** mihomo не умеет hy2.
- **[id=660594|—|09.06](https://t.me/c/2941121338/660594)** «Минимум скорости на айфоне» — хапп фиксы.
- **[id=661128|—|09.06](https://t.me/c/2941121338/661128)** За снос IP отвечают РКН-бановки.
- **[id=661570|—|09.06](https://t.me/c/2941121338/661570)** Контроллер нетмейна.
- **[id=661117|—|09.06](https://t.me/c/2941121338/661117)** «Швеция и Финляндия мусор» (Нодхост), «Польша у меня вроде норм».
- **[id=658051|—|08.06](https://t.me/c/2941121338/658051)** Shadowsocks с Cloud.ru напрямую не работает (SSH конфиг шаблонный).
- **[id=657911|—|08.06](https://t.me/c/2941121338/657911)** МВS: тарифы на селектеле vds анлимит.
- **[id=660010|—|09.06](https://t.me/c/2941121338/660010)** Incy приветствуется: @incydvp.
- **[id=661269|—|09.06](https://t.me/c/2941121338/661269)** Підвіска пісу.

## Пустое/мемное (не вошло)
Дом-2 с «Анастасией/inarhia/кitty_lings» и скам-схемой с твинками @rapexanny; предложения «#продам/#куплю» БС-айпов (46.182, 31.129.42, 81.163.23, 185.91.54, 37.9.4, 87.228.101, 158.160.160, 84.201 и т.д.); продавцы мануалов CDN 15-45$; споры «нексус аеза или нет»; квинс/мачка vs d3vo; троллинг эксплойтов remnawave; Etsy-проекты «продаю VPN-проект».
