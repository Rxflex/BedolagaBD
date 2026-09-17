# DNS

<!-- KB:HEAD -->
[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **DNS**

◀ [Сертификаты](сертификаты.md) · [Docker](docker.md) ▶

> зоны, резолверы, ускорение

---
<!-- /KB:HEAD -->

- Проверка DNS у хостера: `curl https://lknpd.nalog.ru/` — Could not resolve host = проблема DNS у хостера [id=142113].
- РФ-серверы и DNS SERVFAIL: lknpd.nalog.ru и api.yookassa.ru через 1.1.1.1/8.8.8.8 не резолвятся с многих серверов; фикс /etc/hosts: `213.24.64.181 lknpd.nalog.ru` + restart systemd-resolved, либо DNS яндекса [id=278984].
- Полный гайд NaloGo через Яндекс DNS (дословно) [id=306223|Andrew]:
```
mkdir -p /etc/systemd/resolved.conf.d
cat <<EOF > /etc/systemd/resolved.conf.d/ru-dns.conf
[Resolve]
DNS=77.88.8.8 77.88.8.1
Domains=~nalog.ru ~yookassa.ru ~yoomoney.ru
EOF
systemctl restart systemd-resolved
resolvectl query lknpd.nalog.ru
```
и systemd-юнит с Yandex DNS для ~nalog.ru/~yookassa.ru [id=279702].
- Налоговая (lknpd.nalog.ru) с 9.02.2026 с РУ серверов недоступна — лечится сменой DNS на яндекс 77.88.8.8 через netplan [id=225273].
- Cloudflare забанен в РФ: сабка за CF DNS не открывается; альтернатива — Yandex Cloud DNS [id=474485, 474507|08.05.2026]; при этом оранжевое облако КФ включать не стоит (CF в бане у операторов) [id=129655, 796612].
- DNS в Xray JSON (серверный, дословно) [id=723051|19.06.2026]:
```json
"dns": {
  "hosts": {
    "dns.google": ["8.8.8.8", "8.8.4.4"],
    "common.dot.dns.yandex.net": ["77.88.8.8", "77.88.8.1"],
    "unfiltered.adguard-dns.com": ["94.140.14.140", "94.140.14.141"]
  },
  "servers": [
    { "address": "https://dns.google/dns-query", "timeoutMs": 5000 },
    { "address": "https://unfiltered.adguard-dns.com/dns-query", "timeoutMs": 5000 },
    { "address": "https://common.dot.dns.yandex.net/dns-query", "timeoutMs": 5000, "disableFallbackIfMatch": true }
  ],
  "serveStale": true, "queryStrategy": "UseIP", "serveExpiredTTL": 43200, "enableParallelQuery": true
}
```
- DoH через https+local (в сабке) [id=722462]:
```json
"dns": { "servers": [
  { "address": "https+local://8.8.8.8/dns-query", "skipFallback": false },
  { "address": "https+local://1.1.1.1/dns-query", "skipFallback": false }
], "queryStrategy": "UseIPv4" }
```
- DNS split: yandex/vk/mail/ok/госуслуги → 77.88.8.8, остальное → 1.1.1.1 DoH (полный клиентский конфиг) [id=576494|24.05.2026].
- DNS hosts прямо в клиентском json (обход сабки по старым записям) [id=758741|27.06.2026]:
```json
{ "dns": { "hosts": { "lkfl2.nalog.ru": "213.24.64.175", "lknpd.nalog.ru": "213.24.64.181" },
  "servers": ["https://77.88.8.8/dns-query", "8.8.8.8", "localhost"] }, ... }
```
- Свой DNS (AdGuard Home) в xray, чтобы dnsleaktest показывал только его [id=587799]:
```json
"dns": { "servers": [
  {"address": "https://мойднс.com"},
  {"address": "162.159.36.1"},
  {"address": "162.159.46.1", "finalQuery": true}
], "queryStrategy": "UseIPv4" }
```
- Реклама YouTube DNS'ом не режется (AdGuard не убирает ютуб-рекламу) [id=636387]; блокировка рекламы через `geosite:category-ads-all → block` или DNS AdGuard для прочего [id=469649].
- DNS на ноде без разруливания: прописать в конфиг ноды `"dns": { "servers": [ "1.1.1.1", "8.8.8.8" ] }` — иначе при включённой ноде «хана ДНС» [id=1000827|30.07.2026].
- Яндекс+AdGuard в parallel-режиме «дико сосет» — ядро закрывает соединение с Яндекс DNS (unexpected EOF) [id=723788]; xdns на 26.3.27/26.6.27 «раскурили, всё норм», но скорость режет до 5 Мбит/с [id=830683, 861904].
- DNS-балансировка: round-robin, не переключает по нагрузке [id=92863, 134753, 234888]; TTL лучше 1–2 минуты; скрипт xray-checker → CF API убирает IP упавшей ноды из DNS-записи [id=140610]; «DNS-балансировка хуйня полная; хрей-балансировка сложнее, но универсальнее» [id=118204]; клиентский leastLoad предпочтительнее DNS [id=188369]; DNS-рулетка xray-core: xraycore.org/ru/misc/dns_roulette [id=141765]; истекший TTL убивает игровые сессии [id=165648].
- Скрипт мониторинга → Cloudflare DNS: remnawave-cloudflare-nodes (hteppl) — мониторит API панели и правит A-записи [id=235271].
- Своя ASN: в РФ ~1000₽ регистрация + ~1000₽/мес [id=1058107]; UK LTD + ASN + /24 ~100+120 CHF/мес [id=1057296]; /24 в аренду 75€ [id=1058345]; подсеть OVH из 16-20 блока выводится на свою ASN через BGP [id=1031265].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **DNS**

◀ [Сертификаты](сертификаты.md) · [Docker](docker.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
