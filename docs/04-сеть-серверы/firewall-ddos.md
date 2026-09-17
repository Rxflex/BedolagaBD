# iptables / nftables / XDP / анти-DDoS

<!-- KB:HEAD -->
[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **Firewall и анти-DDoS**

◀ [Шейпинг](шейпинг.md) · [Реверс-прокси](reverse-proxy.md) ▶

> iptables/nftables, hashlimit, ipset, XDP, fail2ban

<details>
<summary>📑 <b>На этой странице</b> — 5 разделов</summary>

- [3.1 hashlimit + xt_recent (лимитируем подключения к 443) — дословно [id=776723|Evi|30.06.2026](https://t.me/c/2941121338/776723)](#31-hashlimit--xt_recent-лимитируем-подключения-к-443--дословно-id776723evi30062026)
- [3.2 Geo-block на ipset — дословно [id=487828|Frist|10.05.2026](https://t.me/c/2941121338/487828)](#32-geo-block-на-ipset--дословно-id487828frist10052026)
- [3.3 Анти-скан скрипт (ban сканеров nmap/zmap) — дословно [id=469137|DarkDragonFlame|07.05.2026](https://t.me/c/2941121338/469137)](#33-анти-скан-скрипт-ban-сканеров-nmapzmap--дословно-id469137darkdragonflame07052026)
- [3.4 XDP](#34-xdp)
- [3.5 fail2ban / crowdsec / traffic-guard / анти-DDoS-продукты](#35-fail2ban--crowdsec--traffic-guard--анти-ddos-продукты)

</details>

---
<!-- /KB:HEAD -->

## 3.1 hashlimit + xt_recent (лимитируем подключения к 443) — дословно [id=776723|Evi|30.06.2026](https://t.me/c/2941121338/776723)
```bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y iptables-persistent
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m recent --name blocked --rcheck --seconds 600 -j DROP
iptables -A INPUT -p tcp --dport 443 -m state --state NEW -m hashlimit \
  --hashlimit-upto 10/minute --hashlimit-burst 60 \
  --hashlimit-mode srcip --hashlimit-name mtproto_limit -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m state --state NEW -m recent --name blocked --set -j DROP
netfilter-persistent save
```
Вайтлист: `iptables -I INPUT 1 -s 1.1.1.1 -p tcp --dport 443 -j ACCEPT` [id=776731](https://t.me/c/2941121338/776731); чек банов `cat /proc/net/xt_recent/blocked`; сброс `echo / > /proc/net/xt_recent/blocked`; время бана — в `--rcheck --seconds` [id=776732..776742](https://t.me/c/2941121338/776732).

## 3.2 Geo-block на ipset — дословно [id=487828|Frist|10.05.2026](https://t.me/c/2941121338/487828)
```bash
#!/bin/bash
apt update
apt install -y ipset curl
command -v ipset >/dev/null 2>&1 || { echo "ipset не установлен!"; exit 1; }
ipset create geo_block hash:net maxelem 200000 -exist
MY_IP="YOUR_IP"
iptables -I INPUT -s $MY_IP -j ACCEPT
ipset flush geo_block
COUNTRIES="br za mx bd in ar co cn ve ec pk uz tn"
for country in $COUNTRIES; do
    curl -s https://www.ipdeny.com/ipblocks/data/countries/${country}.zone | while read ip; do
        ipset add geo_block $ip -exist
    done
done
iptables -I INPUT -m set --match-set geo_block src -j DROP
```
- Геоблок на ноду «только мобильные операторы» через UFW+ipset: ASN список мобильных РФ/БГ/КЗ в заметке [id=264566|Max R](https://t.me/c/2941121338/264566).
- Дефолт анти-DDoS: геоблок — «сразу блекхоллить не РФ»; при этом selectel/timeweb/yandex к ноде не могут подключиться — аккуратно [id=996712](https://t.me/c/2941121338/996712); геоблок не спасает от спуфа src [id=997013](https://t.me/c/2941121338/997013).
- Ограничение ноды только мобильными: дроп Wi-Fi с allowlist мобильных ASN, блоклист по traffic-guard, мягкая блокировка с задержкой 30 сек [id=488912|Евгений П.|10.05.2026](https://t.me/c/2941121338/488912).

## 3.3 Анти-скан скрипт (ban сканеров nmap/zmap) — дословно [id=469137|DarkDragonFlame|07.05.2026](https://t.me/c/2941121338/469137)
```bash
apt install ipset iptables-persistent netfilter-persistent -y
ipset create autoban hash:net maxelem 65536
wget https://raw.githubusercontent.com/tread-lightly/CyberOK_Skipa_ips/refs/heads/main/lists/skipa_cidr.txt
while read subnet; do
     ipset add autoban $subnet
done < skipa_cidr.txt
iptables -I INPUT -m set --match-set autoban src -j DROP
iptables -I FORWARD -m set --match-set autoban src -j DROP
ipset save > /etc/ipset.conf
iptables-save > /etc/iptables/rules.v4
```
- Сканеры РКН/ГРЧЦ: censys ASN долбит вебхуки [id=20913..20924](https://t.me/c/2941121338/20913); топ сканеров — CMU_GRCHC (AS61280), GIR_SER-NET (AS207713) [id=240273](https://t.me/c/2941121338/240273); traffic-guard банит подсети ГРЧЦ/РКН («Атак отбито: 26023 за полтора суток») [id=238585, 276623](https://t.me/c/2941121338/238585); список IP сканеров: github.com/tread-lightly/CyberOK_Skipa_ips [id=335336](https://t.me/c/2941121338/335336).
- UFW-закрытие почтовых портов на нодах (спам через ноду, IP в блэклистах) [id=265309](https://t.me/c/2941121338/265309):
```bash
ufw deny out 25/tcp && ufw deny out 465/tcp && ufw deny out 587/tcp && ufw deny out 110/tcp && ufw deny out 995/tcp && ufw deny out 143/tcp && ufw deny out 993/tcp && ufw deny in 25/tcp && ufw deny in 465/tcp && ufw deny in 587/tcp && ufw deny in 110/tcp && ufw deny in 995/tcp && ufw deny in 143/tcp && ufw deny in 993/tcp
```
- Дроп POST (осторожно: POST встречается в VLESS Reality) [id=576015](https://t.me/c/2941121338/576015):
```bash
sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -m string --algo bm --string "POST" -j DROP
```
- Блок QUIC/UDP 443 (правило xray) [id=788164|02.07.2026](https://t.me/c/2941121338/788164):
```json
{ "port": 443, "type": "field", "network": "udp", "outboundTag": "block" }
```
«Браузеры лезут по QUIC; заблокируешь QUIC → откат на TCP/HTTP2: стабильнее, роутинг точнее. Минус: отключается HTTP/3» [id=788164](https://t.me/c/2941121338/788164); контраргумент: по UDP ютуб быстрее [id=788179](https://t.me/c/2941121338/788179).
- youtubeUnblock на ру-ноде [id=59776|10.11.2025](https://t.me/c/2941121338/59776):
```bash
cd /opt && git clone https://github.com/Waujito/youtubeUnblock.git && cd /opt/youtubeUnblock
sudo apt install autoconf automake autotools-dev libtool pkg-config
sudo modprobe nfnetlink_queue
sudo iptables -t mangle -N YOUTUBEUNBLOCK
sudo iptables -t mangle -A YOUTUBEUNBLOCK -p tcp --dport 443 -m connbytes --connbytes-dir original --connbytes-mode packets --connbytes 0:19 -j NFQUEUE --queue-num 537 --queue-bypass
sudo iptables -t mangle -A YOUTUBEUNBLOCK -p udp -m connbytes --connbytes-dir original --connbytes-mode packets --connbytes 0:8 -j NFQUEUE --queue-num 537 --queue-bypass
sudo iptables -t mangle -A POSTROUTING -j YOUTUBEUNBLOCK
sudo iptables -I OUTPUT -m mark --mark 32768/32768 -j ACCEPT
make && sudo systemctl start youtubeUnblock
```

## 3.4 XDP
- XDP-фильтр на ноде: все порты кроме 443/22/1488 DROP; 443 — только RU ISP; 22 — только свой IP; 1488 (порт нода-панель) — только IP панели. Режим native лучший, generic лучше nftables/iptables; зависит от ядра и сетевухи. Для UDP — SYN cookies; против спуфинга source IP XDP особо не помог [id=991903|徹夜 高橋|29.07.2026](https://t.me/c/2941121338/991903).
- Массовая классификация ASN (AS1–AS216475, 4 млрд IP отсканировано): правило «из РФ ISP/MOB — ALLOW, остальное DROP»; для экспатов — обратная логика на отдельных нодах [id=992197|29.07.2026](https://t.me/c/2941121338/992197).
- На ноды анти-DDoS бесполезен — «достаточно панели (и кабинета) с анти-DDoS» [id=993786, 991903](https://t.me/c/2941121338/993786); DROP не-РФ XDP бесполезен против залива/спуфа [id=1178614](https://t.me/c/2941121338/1178614).
- Спуфинг: TCP SYN не требует своего IP в source; провайдер без BCP 38 позволяет подмену; сервер никогда не установит соединение со спуф-IP; XDP «все РФ ESTABLISH, остальное DROP» валится от спуфа [id=1025001, 1083206, 1025082](https://t.me/c/2941121338/1025001). Амплитудные атаки зарезаны провайдерами: NTP monlist, DNS ANY, SNMP, Chargen/QOTD/SSDP, Memcached — остались прямые SYN/ACK/RST спуфинг и UDP флуд [id=1096563|11.08.2026](https://t.me/c/2941121338/1096563).

## 3.5 fail2ban / crowdsec / traffic-guard / анти-DDoS-продукты
- fail2ban: «за 6 часов забанил 100 айпишников» — норм для панели; SSH-порт менять, вход по ключу [id=172019, 49116](https://t.me/c/2941121338/172019). Решала v3.045 Fail2Ban 2.0: дерево статуса, синхронизация с UFW, Geo-Block ipset в before.rules (экономия CPU) [id=512705](https://t.me/c/2941121338/512705).
- CrowdSec: `apt crowdsec + firewall-bouncer-iptables`, вайтлист `/etc/crowdsec/parsers/s02-enrich/whitelist.yaml`, занимает 8080 (менять) [id=110951](https://t.me/c/2941121338/110951); CrowdSec > fail2ban, но панель некрасивая [id=166984](https://t.me/c/2941121338/166984); CrowdSec на всех серверах [id=254377](https://t.me/c/2941121338/254377); multi-server конфиги: github.com/thegrayfoxxx/configs (crowdsec, Traffic Guard списки через `cscli decisions import`) [id=627172, 690898](https://t.me/c/2941121338/627172).
- TrafficGuard (dotX12): блокировка IP сканеров на уровне iptables до сервисов; авто-инсталлер DonMatteoVPN/TrafficGuard-auto → команда `rknpidor` [id=197089, 235475](https://t.me/c/2941121338/197089); списки github.com/shadow-netlab/traffic-guard-lists [id=235935](https://t.me/c/2941121338/235935).
- nDPI + Suricata скрипт (закрытый код!): L1 nDPI режет P2P, L2 Suricata ловит трекеры; 12 нод, DROP ~1 млрд пакетов за 2 недели [id=950368](https://t.me/c/2941121338/950368); критика — зашифрованный shell [id=950649](https://t.me/c/2941121338/950649).
- Цены защиты (дословно) [id=1060389|Саргон|07.08.2026](https://t.me/c/2941121338/1060389):
```
Ddos-Guard - от 48к руб/мес
Stormwall - от 80$
Mitelis - от 25$
Turtle - от 10$
Alibaba - free
```
Механика защиты mitelis.net: SYN-auth, атака 143k RPS → пик 5.78M RPS, TCP RST challenge + adaptive defense (включается через 15 сек) [id=509103, 509262](https://t.me/c/2941121338/509103); TCP RST challenge работает до HTTP, у юзеров сайт открывается со второй попытки [id=509262](https://t.me/c/2941121338/509262).
- DDoS-факты: SYN-flood фаерволом не отразить, если пакетов больше, чем канал — только транзитная скрабка [id=574884, 574941](https://t.me/c/2941121338/574884); средняя атака ~10 Гбит при 17к онлайне [id=833885](https://t.me/c/2941121338/833885); «Иван» 31.07: 2×50 Гбит на UDP 443, спуфинг с миллионами IP [id=1004675, 1004596](https://t.me/c/2941121338/1004675); выше 100 Гбит/с не выстоять, какая бы защита ни была [id=1004732](https://t.me/c/2941121338/1004732); ботнет 20 Гбит TCP SYN flood с 220k адресов [id=562885](https://t.me/c/2941121338/562885); типовая ёмкость ботнет-защиты сабки до 8 Тб, pletx приняла L7 на 1.5 Тбит/с [id=1005651](https://t.me/c/2941121338/1005651); «дедик+защита от хостера+миксование впсок» — рабочая защита; дефолт-метод атаки TCP SYN flood [id=1124594](https://t.me/c/2941121338/1124594).
- Механика атаки через сим-пулы (Т2): авиарежим → новый IP, 2 запроса с IP, релоуд; ~200k pps; сбор IP не завершающих handshake + жалоба в abuse оператора (бан симок) [id=780152..780606](https://t.me/c/2941121338/780152).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **Firewall и анти-DDoS**

◀ [Шейпинг](шейпинг.md) · [Реверс-прокси](reverse-proxy.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
