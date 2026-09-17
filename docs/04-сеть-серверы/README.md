<div align="center">

<img src="../../assets/sections/04.svg" alt="Сеть и серверы" width="860">

</div>

# 🖧 04 · Сеть и серверы

> sysctl/BBR, шейпинг, firewall и анти-DDoS, реверс-прокси, сертификаты, бэкапы

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)

`12 документов` · `912 строк` · `319 пруфов` · `59 блоков кода`

---

## Документы раздела

| # | Документ | О чём | Строк | Пруфов |
|---|---|---|---:|---:|
| 1 | **[sysctl, BBR, MTU](sysctl-bbr-mtu.md)** | полные наборы тюнинга ядра для нод | 63 | 32 |
| 2 | **[Шейпинг](шейпинг.md)** | ограничение скорости, tc, честная раздача | 23 | 13 |
| 3 | **[Firewall и анти-DDoS](firewall-ddos.md)** | iptables/nftables, hashlimit, ipset, XDP, fail2ban | 105 | 46 |
| 4 | **[Реверс-прокси](reverse-proxy.md)** | Caddy, Nginx, HAProxy, Traefik — конфиги дословно | 383 | 49 |
| 5 | **[Сертификаты](сертификаты.md)** | acme.sh, выпуск, продление, подводные камни | 55 | 16 |
| 6 | **[DNS](dns.md)** | зоны, резолверы, ускорение | 60 | 28 |
| 7 | **[Docker](docker.md)** | сети, compose, изоляция компонентов | 46 | 14 |
| 8 | **[Мониторинг](мониторинг.md)** | алерты, метрики трафика, health-чеки | 62 | 18 |
| 9 | **[Бэкапы и restore](бэкапы.md)** | что бэкапить, как восстанавливать | 21 | 26 |
| 10 | **[SSH и доступ](ssh-доступ.md)** | порты, ключи, гигиена доступа | 15 | 20 |
| 11 | **[ТСПУ: серверная часть](тспу-серверное.md)** | что видно со стороны сервера | 52 | 33 |
| 12 | **[Вехи](вехи.md)** | сетевые события года | 27 | 24 |

---

## Что внутри документов

<details>
<summary><b>sysctl, BBR, MTU</b> — 4 разделов</summary>

- [1.1 BBR / congestion control](sysctl-bbr-mtu.md#11-bbr--congestion-control)
- [1.2 Полные sysctl-наборы для нод](sysctl-bbr-mtu.md#12-полные-sysctl-наборы-для-нод)
- [1.3 Отключение IPv6](sysctl-bbr-mtu.md#13-отключение-ipv6)
- [1.4 MTU](sysctl-bbr-mtu.md#14-mtu)

</details>

<details>
<summary><b>Firewall и анти-DDoS</b> — 5 разделов</summary>

- [3.1 hashlimit + xt_recent (лимитируем подключения к 443) — дословно [id=776723|Evi|30.06.2026](https://t.me/c/2941121338/776723)](firewall-ddos.md#31-hashlimit--xt_recent-лимитируем-подключения-к-443--дословно-id776723evi30062026)
- [3.2 Geo-block на ipset — дословно [id=487828|Frist|10.05.2026](https://t.me/c/2941121338/487828)](firewall-ddos.md#32-geo-block-на-ipset--дословно-id487828frist10052026)
- [3.3 Анти-скан скрипт (ban сканеров nmap/zmap) — дословно [id=469137|DarkDragonFlame|07.05.2026](https://t.me/c/2941121338/469137)](firewall-ddos.md#33-анти-скан-скрипт-ban-сканеров-nmapzmap--дословно-id469137darkdragonflame07052026)
- [3.4 XDP](firewall-ddos.md#34-xdp)
- [3.5 fail2ban / crowdsec / traffic-guard / анти-DDoS-продукты](firewall-ddos.md#35-fail2ban--crowdsec--traffic-guard--анти-ddos-продукты)

</details>

<details>
<summary><b>Реверс-прокси</b> — 4 разделов</summary>

- [4.1 Caddy](reverse-proxy.md#41-caddy)
- [4.2 Nginx](reverse-proxy.md#42-nginx)
- [4.3 HAProxy](reverse-proxy.md#43-haproxy)
- [4.4 Traefik](reverse-proxy.md#44-traefik)

</details>

---

◀ [🛡 03. Обход ТСПУ](../03-обход-тспу/README.md) · [🌍 05. Хостинги](../05-хостинги/README.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
