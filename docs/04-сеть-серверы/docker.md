# Docker-сети и compose

<!-- KB:HEAD -->
[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **Docker**

◀ [DNS](dns.md) · [Мониторинг](мониторинг.md) ▶

> сети, compose, изоляция компонентов

---
<!-- /KB:HEAD -->

- Сеть панели эталон [id=44928](https://t.me/c/2941121338/44928):
```yaml
networks:
  remnawave-network:
    external: true
    driver: bridge
    ipam:
      config:
        - subnet: 172.30.0.0/16
          gateway: 172.30.0.1
```
- Имя сети бота при автопрефиксе compose — `remnawave-bedolaga-telegram-bot_bot_network` (не `bot_network`) [id=32068..32079](https://t.me/c/2941121338/32068):
```yaml
networks:
  remnawave-bedolaga-telegram-bot_bot_network:
    external: true
    name: remnawave-bedolaga-telegram-bot_bot_network
```
- Caddy и бот в разных сетях → `host not found`; возвращение в одну сеть чинит Tribute+YooKassa [id=7817, 20376..20378](https://t.me/c/2941121338/7817); `docker network connect remnawave-network remnawave_bot` — временное решение [id=134695, 115532](https://t.me/c/2941121338/134695); лучше прописать в compose [id=44812](https://t.me/c/2941121338/44812).
- «Pool overlaps with other one on this address space» — заменить subnet 172.20.0.0/16 на свободный (172.30.0.0/16) [id=3093, 212293](https://t.me/c/2941121338/3093); диагностика:
```bash
docker network inspect $(docker network ls -q) -f '{{.Name}} {{range .IPAM.Config}}{{.Subnet}}{{end}}'
```
[id=3093..3341](https://t.me/c/2941121338/3093).
- MTU: docker compose MTU 1350 [id=259226, 615201](https://t.me/c/2941121338/259226); Happ-домашний NAT: docker-подсеть попала в 192.168.0.0/24/10.0.0.0/8/100.64.0.0/10 → менять пул IP [id=54484](https://t.me/c/2941121338/54484).
- Права на каталоги бота (бекап Permission denied) [id=137718, 402523](https://t.me/c/2941121338/137718):
```bash
mkdir -p ./logs ./data ./data/backups ./data/referral_qr
chmod -R 755 ./logs ./data
sudo chown -R 1000:1000 ./logs ./data
mkdir -p uploads/images uploads/videos uploads/thumbnails
sudo chown -R 1000:1000 uploads/
```
- Dockerhub-зеркала (get.docker.com/dockerhub недоступны из РФ) [id=589903](https://t.me/c/2941121338/589903):
```bash
cat << EOF | sudo tee -a /etc/docker/daemon.json
{ "registry-mirrors" : [ "https://dockerhub.timeweb.cloud", "https://huecker.io", "https://mirror.gcr.io", "https://c.163.com", "https://registry.docker-cn.com", "https://daocloud.io" ] }
EOF
```
- docker-proxy маппинги панели (посмотреть, что торчит) [id=433912](https://t.me/c/2941121338/433912):
```
/usr/bin/docker-proxy -proto tcp -host-ip 127.0.0.1 -host-port 3000 -container-ip 172.18.0.4 -container-port 3000 -use-listen-fd
```
- localhost в nginx при IPv4-only контейнере ловит ipv6 → запросы не доходят; менять на `127.0.0.1` [id=192781](https://t.me/c/2941121338/192781).
- Порядок запуска стека: панель → сабка → бот → кабинет → nginx/angie; остановка наоборот [id=502278](https://t.me/c/2941121338/502278).

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🖧 04. Сеть и серверы](README.md) › **Docker**

◀ [DNS](dns.md) · [Мониторинг](мониторинг.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
