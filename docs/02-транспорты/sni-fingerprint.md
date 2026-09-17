# SNI-подбор и fingerprint

<!-- KB:HEAD -->
[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **SNI и fingerprint**

◀ [Selfsteal](selfsteal.md) · [gRPC](grpc.md) ▶

> подбор SNI, uTLS-отпечатки, что горело по датам

---
<!-- /KB:HEAD -->

- Критерии SNI (выдержка от Гемини [id=328197|MeinCain|06.04.2026]): домен должен поддерживать TLS 1.3 и HTTP/2, быть доступен с РФ-IP, не принадлежать конкурентам/блок-листам; «а вообще говорят, что еще лучше — selfsni» [id=328214].
- «Ставишь SNI РКН — и тебя не трогают» [id=328127|06.04.2026]; «меняй target на какой-нибудь github.com:443 и тестируй» [id=328135|Weelx|06.04.2026].
- Fingerprint-практика: chrome [note_014, note_057], firefox [id=699075], random [note_017], randomized (vless ws tls — «заведётся любая нода») [id=651697|pkhat|07.06.2026]. По fingerprint РКН вырезал всё: «редирект reality в браузере есть, в curl пусто, и ни один fingerprint не работает» [id=759521|27.06.2026].
- Билайн/Мегафон новые белые списки: проверка SNI + ASN (и вроде IP); в Татарстане (Мегафон) подтверждено, единственный рабочий метод — VK-туннель [id=15017|24.09.2025].

<!-- KB:FOOT -->
---

[⌂](../../README.md) › [🔌 02. Транспорты](README.md) › **SNI и fingerprint**

◀ [Selfsteal](selfsteal.md) · [gRPC](grpc.md) ▶

[⌂ База знаний](../../README.md) · [🗺 Карта](../../MAP.md) · Индексы: [релизы](../../indexes/релизы.md) · [ошибки](../../indexes/ошибки.md) · [env](../../indexes/env.md) · [термины](../../indexes/термины.md) · [ссылки](../../indexes/ссылки.md)
<!-- /KB:FOOT -->
