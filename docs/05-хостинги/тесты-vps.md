# Инструменты проверки локаций и подсетей

<!-- KB:HEAD -->
[⌂](../../README.md) › [🌍 05. Хостинги](README.md) › **Тесты VPS**

◀ [Ёмкость нод](ёмкость-нод.md) · [Боты и сервисы](боты-сервисы.md) ▶

> канонический набор проверок сервера — дословно

---
<!-- /KB:HEAD -->

## Канонический набор тестов VPS (закреп Egor, дословно) [id=199900](https://t.me/c/2941121338/199900)

```bash
IP region
bash <(wget -qO- https://ipregion.vrnt.xyz)
Censorcheck для проверки геоблока
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode geoblock
Censorcheck для серверов РФ
bash <(wget -qO- https://github.com/vernette/censorcheck/raw/master/censorcheck.sh) --mode dpi
Тест до российских iPerf3 серверов
bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh)
YABS
curl -sL yabs.sh | bash -s -- -4
Проверка IP сервера на блокировки зарубежными сервисами
bash <(curl -Ls IP.Check.Place) -l en
Параметры сервера и проверка скорости к зарубежным провайдерам
wget -qO- bench.sh | bash
IPQuality
bash <(curl -Ls https://Check.Place) -EI
Тест на процессор (какой % cpu выделили)
sysbench cpu run --threads=1
```

**Multitest (saveksme) — обновлённый метод (09.05):**
```bash
curl -sL https://raw.githubusercontent.com/saveksme/multitest/master/multitest.sh -o /usr/local/bin/multitest && chmod +x /usr/local/bin/multitest && echo "Установлено! Запуск: multitest"
```
[id=480497,495478](https://t.me/c/2941121338/480497)

**Прочие команды:**
```bash
# Проверка скорости до РФ
bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh)
# BGP-трассировка
curl nxtrace.org/nt | bash; nexttrace 8.8.8.8
# Скорость до api.telegram.org
curl -o /dev/null -s -w 'Connect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n' https://api.telegram.org
```
[id=184554,87774](https://t.me/c/2941121338/184554)

**Чекер ТСПУ/операторов (по операторам ICMP/TCP/TLS):**
```bash
wget -qO- censorcheck.tlab.pw | bash
```
[id=845579](https://t.me/c/2941121338/845579)

**Censorcheck с альтернативным портом 8443:**
```bash
curl -sSL -A "Wget/1.21.3" censorcheck.tlab.pw | sed 's/":443"/":8443"/g; s/"port": 443/"port": 8443/g' | bash
```
[id=935719](https://t.me/c/2941121338/935719)

**dpi-detector:**
```bash
docker run --rm -it --pull=always ghcr.io/runnin4ik/dpi-detector:latest
```
[id=934724](https://t.me/c/2941121338/934724)

**TrafficGuard (blockguard) установка:**
```bash
apt install ipset iptables-persistent netfilter-persistent -y
ipset create autoban hash:net maxelem 65536
wget https://raw.githubusercontent.com/tread-lightly/CyberOK_Skipa_ips/refs/heads/main/lists/skipa_cidr.txt
while read subnet; do ipset add autoban $subnet; done < skipa_cidr.txt
iptables -I INPUT -m set --match-set autoban src -j DROP
iptables -I FORWARD -m set --match-set autoban src -j DROP
ipset save > /etc/ipset.conf
iptables-save > /etc/iptables/rules.v4
```
[id=469137](https://t.me/c/2941121338/469137)

**Закрытие почтовых портов (анти-спам):**
```bash
ufw deny out 25/tcp && ufw deny out 465/tcp && ufw deny out 587/tcp && ufw deny out 110/tcp && ufw deny out 995/tcp && ufw deny out 143/tcp && ufw deny out 993/tcp && ufw deny in 25/tcp && ufw deny in 465/tcp && ufw deny in 587/tcp && ufw deny in 110/tcp && ufw deny in 995/tcp && ufw deny in 143/tcp && ufw deny in 993/tcp
```
[id=265309](https://t.me/c/2941121338/265309)

**Обход ТСПУ через iptables (hashlimit на 443):**
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
[id=776723](https://t.me/c/2941121338/776723)

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🌍 05. Хостинги](README.md) › **Тесты VPS**

◀ [Ёмкость нод](ёмкость-нод.md) · [Боты и сервисы](боты-сервисы.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
