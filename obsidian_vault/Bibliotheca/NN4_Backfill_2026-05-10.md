---
type: backfill_execution_log
date: 2026-05-10
sprint: NN.4
started: 2026-05-10T10:20:35
finished: 2026-05-10T10:35:10
duration_min: 14.6
status: autonomous
tags: [nn4, backfill, data_coverage, autonomous_execution]
---

# NN.4 · Backfill Execution · 2026-05-10

> Orquestrador autónomo. User foi para academia, este ficheiro é o relatório.
> Zero intervenção humana; todos os fetchers são idempotentes.

## TL;DR

- Total tickers processados: **130**
- Sucessos: **129** (99%)
- Falhas: **1**
- Duração: **14.6 min**

## Plano executado

| Fase | Categoria | Tickers | Fetcher |
|---|---|---|---|
| P1 | prices_missing | 8 | yf_br_fetcher / yf_us_fetcher --period max |
| P2 | fundamentals_missing | 119 | yf_deep_fundamentals |
| P3 | partial | 3 | ambos |

## P1 · Prices

| # | Ticker | Mkt | OK | Δ prices | Δ fund | Δ deep | Tempo (s) | Tail |
|---|---|---|---|---|---|---|---|---|
| 1 | LFTB11 | br | ✅ | +1 | +1 | +0 | 2.2 | {"ts": "2026-05-10T07:20:36Z", "event": "yf_br_fetch_start", "ticker": "LFTB11", |
| 2 | RBRX11 | br | ✅ | +0 | +1 | +0 | 2.4 | {"ts": "2026-05-10T07:20:39Z", "event": "yf_br_volume_reject", "ticker": "RBRX11 |
| 3 | AXIA7 | br | ✅ | +0 | +1 | +0 | 2.2 | {"ts": "2026-05-10T07:20:40Z", "event": "yf_br_fetch_start", "ticker": "AXIA7",  |
| 4 | GARE11 | br | ✅ | +0 | +1 | +0 | 2.3 | {"ts": "2026-05-10T07:20:43Z", "event": "yf_br_fetch_start", "ticker": "GARE11", |
| 5 | KNHF11 | br | ✅ | +174 | +1 | +0 | 2.4 | {"ts": "2026-05-10T07:20:45Z", "event": "yf_br_fetch_start", "ticker": "KNHF11", |
| 6 | MCRE11 | br | ✅ | +1033 | +1 | +0 | 2.7 | {"ts": "2026-05-10T07:20:49Z", "event": "yf_br_volume_reject", "ticker": "MCRE11 |
| 7 | MOTV3 | br | ✅ | +0 | +1 | +0 | 2.3 | {"ts": "2026-05-10T07:20:50Z", "event": "yf_br_fetch_start", "ticker": "MOTV3",  |
| 8 | POMO4 | br | ✅ | +0 | +0 | +0 | 3.1 | {"ts": "2026-05-10T07:20:54Z", "event": "yf_br_volume_reject", "ticker": "POMO4" |

## P2 · Fundamentals

| # | Ticker | Mkt | OK | Δ prices | Δ fund | Δ deep | Tempo (s) | Tail |
|---|---|---|---|---|---|---|---|---|
| 1 | BBDC4 | br | ✅ | +0 | +0 | +0 | 5.8 | market: {"ts": "2026-05-10T07:20:57Z", "event": "yf_br_volume_reject", "ticker": |
| 2 | BTLG11 | br | ✅ | +0 | +1 | +0 | 5.5 | market: {"ts": "2026-05-10T07:21:03Z", "event": "yf_br_volume_reject", "ticker": |
| 3 | ITSA4 | br | ✅ | +0 | +1 | +0 | 6.0 | market: {"ts": "2026-05-10T07:21:09Z", "event": "yf_br_volume_reject", "ticker": |
| 4 | IVVB11 | br | ✅ | +8 | +1 | +0 | 5.5 | market: {"ts": "2026-05-10T07:21:14Z", "event": "yf_br_volume_reject", "ticker": |
| 5 | PVBI11 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:21:20Z", "event": "yf_br_volume_reject", "ticker": |
| 6 | VALE3 | br | ✅ | +0 | +1 | +0 | 6.2 | market: {"ts": "2026-05-10T07:21:26Z", "event": "yf_br_volume_reject", "ticker": |
| 7 | VGIR11 | br | ✅ | +0 | +1 | +0 | 6.3 | market: {"ts": "2026-05-10T07:21:32Z", "event": "yf_br_volume_reject", "ticker": |
| 8 | XPML11 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:21:38Z", "event": "yf_br_close_reject", "ticker":  |
| 9 | ALOS3 | br | ✅ | +0 | +1 | +0 | 5.6 | market: {"ts": "2026-05-10T07:21:42Z", "event": "yf_br_fetch_start", "ticker": " |
| 10 | B3SA3 | br | ✅ | +0 | +1 | +0 | 5.7 | market: {"ts": "2026-05-10T07:21:49Z", "event": "yf_br_close_reject", "ticker":  |
| 11 | BRCO11 | br | ✅ | +0 | +1 | +0 | 5.3 | market: {"ts": "2026-05-10T07:21:53Z", "event": "yf_br_fetch_start", "ticker": " |
| 12 | CPLE3 | br | ✅ | +0 | +1 | +0 | 6.0 | market: {"ts": "2026-05-10T07:22:00Z", "event": "yf_br_volume_reject", "ticker": |
| 13 | ENGI11 | br | ✅ | +0 | +1 | +0 | 6.7 | market: {"ts": "2026-05-10T07:22:07Z", "event": "yf_br_volume_reject", "ticker": |
| 14 | EQTL3 | br | ✅ | +0 | +1 | +0 | 5.8 | market: {"ts": "2026-05-10T07:22:13Z", "event": "yf_br_volume_reject", "ticker": |
| 15 | HGLG11 | br | ✅ | +0 | +1 | +0 | 5.9 | market: {"ts": "2026-05-10T07:22:18Z", "event": "yf_br_volume_reject", "ticker": |
| 16 | HGRU11 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:22:24Z", "event": "yf_br_volume_reject", "ticker": |
| 17 | ITUB4 | br | ✅ | +0 | +1 | +0 | 6.2 | market: {"ts": "2026-05-10T07:22:30Z", "event": "yf_br_volume_reject", "ticker": |
| 18 | KNCR11 | br | ✅ | +0 | +1 | +0 | 5.6 | market: {"ts": "2026-05-10T07:22:36Z", "event": "yf_br_volume_reject", "ticker": |
| 19 | KNRI11 | br | ✅ | +0 | +1 | +0 | 5.6 | market: {"ts": "2026-05-10T07:22:41Z", "event": "yf_br_volume_reject", "ticker": |
| 20 | MCCI11 | br | ✅ | +0 | +1 | +0 | 5.3 | market: {"ts": "2026-05-10T07:22:45Z", "event": "yf_br_fetch_start", "ticker": " |
| 21 | MULT3 | br | ✅ | +0 | +1 | +0 | 5.9 | market: {"ts": "2026-05-10T07:22:52Z", "event": "yf_br_volume_reject", "ticker": |
| 22 | PETR4 | br | ✅ | +0 | +1 | +0 | 6.0 | market: {"ts": "2026-05-10T07:22:58Z", "event": "yf_br_volume_reject", "ticker": |
| 23 | PGMN3 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:23:04Z", "event": "yf_br_volume_reject", "ticker": |
| 24 | PLPL3 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:23:08Z", "event": "yf_br_fetch_start", "ticker": " |
| 25 | PMLL11 | br | ✅ | +0 | +1 | +0 | 5.5 | market: {"ts": "2026-05-10T07:23:15Z", "event": "yf_br_volume_reject", "ticker": |
| 26 | POMO3 | br | ✅ | +1238 | +1 | +0 | 6.2 | market: {"ts": "2026-05-10T07:23:21Z", "event": "yf_br_volume_reject", "ticker": |
| 27 | RAPT4 | br | ✅ | +0 | +1 | +0 | 9.6 | market: {"ts": "2026-05-10T07:23:30Z", "event": "yf_br_volume_reject", "ticker": |
| 28 | RBRY11 | br | ✅ | +0 | +1 | +0 | 5.2 | market: {"ts": "2026-05-10T07:23:36Z", "event": "yf_br_volume_reject", "ticker": |
| 29 | RDOR3 | br | ✅ | +0 | +1 | +0 | 5.5 | market: {"ts": "2026-05-10T07:23:41Z", "event": "yf_br_volume_reject", "ticker": |
| 30 | RECR11 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:23:45Z", "event": "yf_br_fetch_start", "ticker": " |
| 31 | RENT3 | br | ✅ | +0 | +1 | +0 | 5.8 | market: {"ts": "2026-05-10T07:23:53Z", "event": "yf_br_volume_reject", "ticker": |
| 32 | SUZB3 | br | ✅ | +0 | +1 | +0 | 5.7 | market: {"ts": "2026-05-10T07:23:58Z", "event": "yf_br_volume_reject", "ticker": |
| 33 | TRXF11 | br | ✅ | +0 | +1 | +0 | 5.9 | market: {"ts": "2026-05-10T07:24:04Z", "event": "yf_br_volume_reject", "ticker": |
| 34 | TTEN3 | br | ✅ | +0 | +1 | +0 | 5.8 | market: {"ts": "2026-05-10T07:24:09Z", "event": "yf_br_volume_reject", "ticker": |
| 35 | VGIP11 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:24:15Z", "event": "yf_br_volume_reject", "ticker": |
| 36 | VISC11 | br | ✅ | +0 | +1 | +0 | 5.5 | market: {"ts": "2026-05-10T07:24:19Z", "event": "yf_br_fetch_start", "ticker": " |
| 37 | VRTA11 | br | ✅ | +0 | +1 | +0 | 5.5 | market: {"ts": "2026-05-10T07:24:26Z", "event": "yf_br_volume_reject", "ticker": |
| 38 | XPLG11 | br | ✅ | +0 | +1 | +0 | 5.4 | market: {"ts": "2026-05-10T07:24:30Z", "event": "yf_br_fetch_start", "ticker": " |
| 39 | ABM | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:24:39Z", "event": "yf_us_volume_reject", "ticker": |
| 40 | ABT | us | ✅ | +0 | +1 | +0 | 7.7 | market: {"ts": "2026-05-10T07:24:43Z", "event": "yf_us_fetch_start", "ticker": " |
| 41 | ADM | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:24:54Z", "event": "yf_us_volume_reject", "ticker": |
| 42 | ADP | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:25:01Z", "event": "yf_us_volume_reject", "ticker": |
| 43 | AFL | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:25:08Z", "event": "yf_us_volume_reject", "ticker": |
| 44 | ALB | us | ✅ | +0 | +1 | +0 | 7.2 | market: {"ts": "2026-05-10T07:25:15Z", "event": "yf_us_volume_reject", "ticker": |
| 45 | AOS | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:25:23Z", "event": "yf_us_volume_reject", "ticker": |
| 46 | APD | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:25:30Z", "event": "yf_us_volume_reject", "ticker": |
| 47 | ATO | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:25:38Z", "event": "yf_us_volume_reject", "ticker": |
| 48 | AWR | us | ✅ | +0 | +1 | +0 | 7.8 | market: {"ts": "2026-05-10T07:25:45Z", "event": "yf_us_volume_reject", "ticker": |
| 49 | BDX | us | ✅ | +0 | +1 | +0 | 7.9 | market: {"ts": "2026-05-10T07:25:53Z", "event": "yf_us_volume_reject", "ticker": |
| 50 | BEN | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:26:00Z", "event": "yf_us_volume_reject", "ticker": |
| 51 | BF-B | us | ✅ | +0 | +1 | +0 | 7.7 | market: {"ts": "2026-05-10T07:26:08Z", "event": "yf_us_volume_reject", "ticker": |
| 52 | BKH | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:26:16Z", "event": "yf_us_volume_reject", "ticker": |
| 53 | BRO | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:26:23Z", "event": "yf_us_volume_reject", "ticker": |
| 54 | CAT | us | ✅ | +0 | +1 | +0 | 8.0 | market: {"ts": "2026-05-10T07:26:31Z", "event": "yf_us_volume_reject", "ticker": |
| 55 | CB | us | ✅ | +0 | +1 | +0 | 7.2 | market: {"ts": "2026-05-10T07:26:38Z", "event": "yf_us_volume_reject", "ticker": |
| 56 | CBSH | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:26:46Z", "event": "yf_us_volume_reject", "ticker": |
| 57 | CHD | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:26:53Z", "event": "yf_us_volume_reject", "ticker": |
| 58 | CHRW | us | ✅ | +0 | +1 | +0 | 7.2 | market: {"ts": "2026-05-10T07:27:01Z", "event": "yf_us_volume_reject", "ticker": |
| 59 | CINF | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:27:08Z", "event": "yf_us_volume_reject", "ticker": |
| 60 | CL | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:27:16Z", "event": "yf_us_volume_reject", "ticker": |
| 61 | CLX | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:27:23Z", "event": "yf_us_pb_extreme_reject", "tick |
| 62 | CTAS | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:27:30Z", "event": "yf_us_volume_reject", "ticker": |
| 63 | CVX | us | ✅ | +0 | +1 | +0 | 7.9 | market: {"ts": "2026-05-10T07:27:38Z", "event": "yf_us_volume_reject", "ticker": |
| 64 | CWT | us | ❌ | +0 | +0 | +0 | 14.0 | market:     ) ·     ^ · sqlite3.OperationalError: database is locked · deep:   ✓ |
| 65 | DOV | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:28:00Z", "event": "yf_us_volume_reject", "ticker": |
| 66 | ECL | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:28:07Z", "event": "yf_us_volume_reject", "ticker": |
| 67 | ED | us | ✅ | +0 | +1 | +0 | 7.7 | market: {"ts": "2026-05-10T07:28:15Z", "event": "yf_us_volume_reject", "ticker": |
| 68 | EMR | us | ✅ | +0 | +1 | +0 | 7.9 | market: {"ts": "2026-05-10T07:28:20Z", "event": "yf_us_fetch_start", "ticker": " |
| 69 | ERIE | us | ✅ | +0 | +1 | +0 | 7.1 | market: {"ts": "2026-05-10T07:28:30Z", "event": "yf_us_volume_reject", "ticker": |
| 70 | ES | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:28:37Z", "event": "yf_us_volume_reject", "ticker": |
| 71 | EXPD | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:28:45Z", "event": "yf_us_volume_reject", "ticker": |
| 72 | FAST | us | ✅ | +0 | +1 | +0 | 7.2 | market: {"ts": "2026-05-10T07:28:52Z", "event": "yf_us_volume_reject", "ticker": |
| 73 | FDS | us | ✅ | +0 | +1 | +0 | 7.0 | market: {"ts": "2026-05-10T07:28:59Z", "event": "yf_us_volume_reject", "ticker": |
| 74 | FRT | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:29:06Z", "event": "yf_us_volume_reject", "ticker": |
| 75 | FUL | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:29:14Z", "event": "yf_us_volume_reject", "ticker": |
| 76 | GD | us | ✅ | +0 | +1 | +0 | 7.8 | market: {"ts": "2026-05-10T07:29:22Z", "event": "yf_us_volume_reject", "ticker": |
| 77 | GPC | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:29:26Z", "event": "yf_us_fetch_start", "ticker": " |
| 78 | GRC | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:29:37Z", "event": "yf_us_volume_reject", "ticker": |
| 79 | GWW | us | ✅ | +0 | +1 | +0 | 7.9 | market: {"ts": "2026-05-10T07:29:45Z", "event": "yf_us_volume_reject", "ticker": |
| 80 | HRL | us | ✅ | +0 | +1 | +0 | 7.2 | market: {"ts": "2026-05-10T07:29:52Z", "event": "yf_us_volume_reject", "ticker": |
| 81 | IBM | us | ✅ | +0 | +1 | +0 | 8.0 | market: {"ts": "2026-05-10T07:29:56Z", "event": "yf_us_fetch_start", "ticker": " |
| 82 | ITW | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:30:08Z", "event": "yf_us_volume_reject", "ticker": |
| 83 | JKHY | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:30:15Z", "event": "yf_us_volume_reject", "ticker": |
| 84 | KMB | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:30:22Z", "event": "yf_us_volume_reject", "ticker": |
| 85 | LEG | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:30:30Z", "event": "yf_us_volume_reject", "ticker": |
| 86 | LIN | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:30:37Z", "event": "yf_us_volume_reject", "ticker": |
| 87 | LOW | us | ✅ | +0 | +1 | +0 | 7.3 | market: {"ts": "2026-05-10T07:30:44Z", "event": "yf_us_volume_reject", "ticker": |
| 88 | MDT | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:30:52Z", "event": "yf_us_volume_reject", "ticker": |
| 89 | MGEE | us | ✅ | +0 | +1 | +0 | 7.2 | market: {"ts": "2026-05-10T07:30:59Z", "event": "yf_us_volume_reject", "ticker": |
| 90 | MKC | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:31:07Z", "event": "yf_us_volume_reject", "ticker": |
| 91 | MO | us | ✅ | +0 | +1 | +0 | 7.8 | market: {"ts": "2026-05-10T07:31:15Z", "event": "yf_us_close_reject", "ticker":  |
| 92 | MSA | us | ✅ | +0 | +1 | +0 | 7.8 | market: {"ts": "2026-05-10T07:31:22Z", "event": "yf_us_volume_reject", "ticker": |
| 93 | MSEX | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:31:30Z", "event": "yf_us_volume_reject", "ticker": |
| 94 | NDSN | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:31:37Z", "event": "yf_us_volume_reject", "ticker": |
| 95 | NEE | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:31:45Z", "event": "yf_us_volume_reject", "ticker": |
| 96 | NFG | us | ✅ | +0 | +1 | +0 | 7.7 | market: {"ts": "2026-05-10T07:31:52Z", "event": "yf_us_volume_reject", "ticker": |
| 97 | NUE | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:32:00Z", "event": "yf_us_volume_reject", "ticker": |
| 98 | NWN | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:32:07Z", "event": "yf_us_volume_reject", "ticker": |
| 99 | PH | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:32:15Z", "event": "yf_us_volume_reject", "ticker": |
| 100 | PNR | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:32:22Z", "event": "yf_us_volume_reject", "ticker": |
| 101 | PPG | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:32:30Z", "event": "yf_us_volume_reject", "ticker": |
| 102 | RLI | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:32:37Z", "event": "yf_us_volume_reject", "ticker": |
| 103 | ROP | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:32:44Z", "event": "yf_us_volume_reject", "ticker": |
| 104 | RPM | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:32:52Z", "event": "yf_us_volume_reject", "ticker": |
| 105 | SCL | us | ✅ | +0 | +1 | +0 | 7.7 | market: {"ts": "2026-05-10T07:33:00Z", "event": "yf_us_volume_reject", "ticker": |
| 106 | SHW | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:33:07Z", "event": "yf_us_volume_reject", "ticker": |
| 107 | SJM | us | ✅ | +0 | +1 | +0 | 7.1 | market: {"ts": "2026-05-10T07:33:15Z", "event": "yf_us_volume_reject", "ticker": |
| 108 | SPGI | us | ✅ | +0 | +1 | +0 | 7.5 | market: {"ts": "2026-05-10T07:33:22Z", "event": "yf_us_volume_reject", "ticker": |
| 109 | SWK | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:33:30Z", "event": "yf_us_volume_reject", "ticker": |
| 110 | SYY | us | ✅ | +0 | +1 | +0 | 7.7 | market: {"ts": "2026-05-10T07:33:37Z", "event": "yf_us_volume_reject", "ticker": |
| 111 | TDS | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:33:45Z", "event": "yf_us_volume_reject", "ticker": |
| 112 | TGT | us | ✅ | +0 | +1 | +0 | 7.9 | market: {"ts": "2026-05-10T07:33:53Z", "event": "yf_us_volume_reject", "ticker": |
| 113 | TNC | us | ✅ | +0 | +1 | +0 | 7.8 | market: {"ts": "2026-05-10T07:34:01Z", "event": "yf_us_volume_reject", "ticker": |
| 114 | TR | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:34:08Z", "event": "yf_us_volume_reject", "ticker": |
| 115 | TROW | us | ✅ | +0 | +1 | +0 | 7.4 | market: {"ts": "2026-05-10T07:34:15Z", "event": "yf_us_volume_reject", "ticker": |
| 116 | UVV | us | ✅ | +0 | +1 | +0 | 7.6 | market: {"ts": "2026-05-10T07:34:23Z", "event": "yf_us_volume_reject", "ticker": |
| 117 | WMT | us | ✅ | +0 | +1 | +0 | 7.9 | market: {"ts": "2026-05-10T07:34:31Z", "event": "yf_us_volume_reject", "ticker": |
| 118 | WST | us | ✅ | +0 | +1 | +0 | 7.1 | market: {"ts": "2026-05-10T07:34:39Z", "event": "yf_us_volume_reject", "ticker": |
| 119 | XOM | us | ✅ | +0 | +1 | +0 | 8.0 | market: {"ts": "2026-05-10T07:34:43Z", "event": "yf_us_fetch_start", "ticker": " |

## P3 · Partial

| # | Ticker | Mkt | OK | Δ prices | Δ fund | Δ deep | Tempo (s) | Tail |
|---|---|---|---|---|---|---|---|---|
| 1 | NU | us | ✅ | +0 | +1 | +0 | 6.4 | market: {"ts": "2026-05-10T07:34:53Z", "event": "yf_us_volume_reject", "ticker": |
| 2 | PLTR | us | ✅ | +0 | +1 | +0 | 6.6 | market: {"ts": "2026-05-10T07:34:57Z", "event": "yf_us_fetch_start", "ticker": " |
| 3 | XP | us | ✅ | +0 | +1 | +0 | 6.6 | market: {"ts": "2026-05-10T07:35:06Z", "event": "yf_us_volume_reject", "ticker": |

## Falhas detectadas

Tickers que NÃO completaram (provavelmente delisted, ticker errado, ou yfinance rate-limit):

- `us:CWT` — market:     )
    ^
sqlite3.OperationalError: database is locked · deep:   ✓ CWT      (us)  5 periods

Done: 1 OK, 0 bad

## Coverage diff (agregado)

- Linhas `prices` adicionadas: **+2,454**
- Linhas `fundamentals` adicionadas: **+127**
- Linhas `deep_fundamentals` adicionadas: **+0**

## Próximos passos

- [ ] Re-correr `python scripts/overnight/overnight_2026_05_09.py --block A` para gerar audit V2 com novos números
- [ ] Refresh `/stocks` e `/desk` no browser — fundamentals devem aparecer agora
- [ ] Para failures persistentes: confirmar ticker delisted ou ajustar manualmente em `config/universe.yaml`

## Log completo

`logs\nn4_backfill.log`
