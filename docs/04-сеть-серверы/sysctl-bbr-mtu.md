# Ядро: sysctl, BBR, IPv6, MTU

<!-- KB:HEAD -->
[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **sysctl, BBR, MTU**

[Шейпинг](шейпинг.md) ▶

> полные наборы тюнинга ядра для нод

<details>
<summary>📑 <b>На этой странице</b> — 4 разделов</summary>

- [1.1 BBR / congestion control](#11-bbr--congestion-control)
- [1.2 Полные sysctl-наборы для нод](#12-полные-sysctl-наборы-для-нод)
- [1.3 Отключение IPv6](#13-отключение-ipv6)
- [1.4 MTU](#14-mtu)

</details>

---
<!-- /KB:HEAD -->

## 1.1 BBR / congestion control
- Канон включения BBR:
```bash
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf && sysctl -p
```
[id=50126..50135|Дмитрий|02.11.2025](https://t.me/c/2941121338/50126), повтор [id=1066537|07.08.2026](https://t.me/c/2941121338/1066537).
- BBR-скрипт Дмитрия: включает bbr2 при наличии, fq, `tcp_fastopen=3`, большие буферы, лог `/var/log/network-optimize.log` [id=50126..50135|02.11.2025](https://t.me/c/2941121338/50126).
- Теория: BBR даёт прирост при потерях/узких местах; при скорости Wi-Fi выше тарифа разницы нет [id=50754..50765|IS|03.11.2025](https://t.me/c/2941121338/50754).
- Вместимость нод с BBR (Ivan-стата, 16.12.2025): 1/2 → BBR1 15–25 / BBR3 20–35 активных; 2/4 → 40–60/60–90; 4/8 → ~100/120–180; 8/16 → 200–250/300–400. BBR3 требует изменения ядра [id=112903](https://t.me/c/2941121338/112903).
- Внимание: кастомное ядро BBR3 не имеет TC-модулей — шейпер на BBR3 не работает, откатывайте ядро [id=138513|Дмитрий|28.12.2025](https://t.me/c/2941121338/138513).
- BBR включать при перегрузе 500+ юзеров (дедик 2 CPU/128 GB уходит в 300% CPU) [id=408005|Frist|26.04.2026](https://t.me/c/2941121338/408005).
- Ядро XanMod с BBRv3/BBRv1 — установка с проверкой GPG и подбором сборки под CPU, без автоперезагрузки (в составе node-diagnostic) [id=923728|Илья|20.07.2026](https://t.me/c/2941121338/923728).
- Некоторые хостеры дают BBR/AES-NI включёнными: Beget (BBR вкл хостингом) [id=797199](https://t.me/c/2941121338/797199), VPSPay (BBR вкл, IPv6 off) [id=206904](https://t.me/c/2941121338/206904); у других выключено — просить ТП [id=237101](https://t.me/c/2941121338/237101).

## 1.2 Полные sysctl-наборы для нод
- Вариант c0mrade (10.11.2025) [id=60218](https://t.me/c/2941121338/60218): disable IPv6, `ip_forward=0`, `rp_filter=1`, `tcp_syncookies=1`, `fin_timeout=20`, `tcp_max_tw_buckets=262144`, `tcp_fastopen=3`, `tw_reuse=1`, `tcp_max_syn_backlog=8192`, `tcp_rmem/wmem = 4096 87380/65536 16777216`, `somaxconn=4096`, `netdev_max_backlog=5000`, `default_qdisc=fq`, `congestion_control=bbr`, `fs.file-max=2097152`, `vm.swappiness=0`.
- Исправленный вариант Zavulon для VPN-ноды (дословно) [id=60229|10.11.2025](https://t.me/c/2941121338/60229):
```
# IPv6: либо полностью отключить (disable_ipv6=1), либо forwarding=1, accept_ra=0, autoconf=0, redirects=0
net.ipv4.ip_forward = 1            # на маршрутизаторе нужна переадресация
net.ipv4.conf.all.rp_filter = 2    # loose: многосетевость/Docker/VPN, strict режет легитимный трафик
net.ipv4.tcp_fastopen = 1          # только клиент; серверная TFO конфликтует через NAT/прокси
# tcp_max_tw_buckets, tcp_fack, tcp_tw_reuse — удалить (устарело)
net.ipv4.tcp_ecn = 1
net.ipv4.tcp_sack = 1
net.ipv4.tcp_keepalive_time = 600 / intvl=60 / probes=5
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.somaxconn = 4096
net.core.netdev_max_backlog = 5000
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
kernel.yama.ptrace_scope = 1
kernel.randomize_va_space = 2
fs.suid_dumpable = 0
vm.swappiness = 10
fs.file-max = 2097152
```
- Kernel hardening Решалы: `rp_filter: 2 (strict) → 0 + src_valid_mark=1` — фикс «WireGuard/WARP handshake есть, но трафик не идёт»; после апдейта переприменить (`sysctl -p /etc/sysctl.d/99-reshala-hardening.conf`) [id=495106|12.05.2026](https://t.me/c/2941121338/495106). `rp_filter = 2` (loose) сохраняет защиту от спуфинга и позволяет WG/WARP [id=467739|07.05.2026](https://t.me/c/2941121338/467739).
- eBPF-шейпер не запустится при `sysctl -w kernel.unprivileged_bpf_disabled=2` — ставить 0 [id=332326|Сергей](https://t.me/c/2941121338/332326).
- Redis в контейнере: `WARNING Memory overcommit must be enabled` → `vm.overcommit_memory = 1` в /etc/sysctl.conf [id=16810, 273062](https://t.me/c/2941121338/16810).
- Warp/WireGuard в контейнере RemnaNode: `failed to disable ipv4 rp_filter ... read-only file system` → в docker-compose `cap_add: - NET_ADMIN` [id=749423|25.06.2026](https://t.me/c/2941121338/749423); NET_ADMIN также нужен ноде 2.6.0+ для сброса сессий юзера [id=243451, 772438](https://t.me/c/2941121338/243451).
- Сборка кабинета OOM: `NODE_OPTIONS="--max-old-space-size=768"`; swap: `fallocate -l 1G /swapfile; chmod 600 /swapfile; mkswap /swapfile; swapon /swapfile` [id=258246](https://t.me/c/2941121338/258246).

## 1.3 Отключение IPv6
```
nano /etc/sysctl.d/99-disable-ipv6.conf
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
sudo sysctl --system
```
[id=102124|EE|11.12.2025](https://t.me/c/2941121338/102124); вариант без lo — [id=31307..31364|22.10.2025](https://t.me/c/2941121338/31307). Одной строкой:
```bash
echo -e "\nnet.ipv6.conf.all.disable_ipv6 = 1\nnet.ipv6.conf.default.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.conf > /dev/null && sudo sysctl -p
```
- Для чего: шортсы плохо грузятся [id=32291](https://t.me/c/2941121338/32291); некорректное гео (NL→Украина) [id=102124, 127167](https://t.me/c/2941121338/102124); у 90% хостеров кривой IPv6, warp пытается идти через него [id=791733](https://t.me/c/2941121338/791733); геометки IPv6/IPv4 расходятся — грохнуть IPv6 на ноде [id=426669](https://t.me/c/2941121338/426669). IPv6 на нодах в РФ выключать по умолчанию [id=114142|17.12.2025](https://t.me/c/2941121338/114142).

## 1.4 MTU
- Docker MTU 1350 — рабочее значение в compose бота/панели [id=259226, 281185](https://t.me/c/2941121338/259226); `driver_opts: com.docker.network.driver.mtu: 1350` [id=615203](https://t.me/c/2941121338/615203).
- Телега не работает (через раз) — пробовать MTU 1380 [id=686353](https://t.me/c/2941121338/686353); MTU 1440 на активном интерфейсе — «с мобильного ожило» [id=654354](https://t.me/c/2941121338/654354).
- Hysteria2: минимально допустимый MTU **1308**; с 1280 не заведётся, с 1420 заводится [id=868664, 868658|14.07.2026](https://t.me/c/2941121338/868664).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **sysctl, BBR, MTU**

[Шейпинг](шейпинг.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
