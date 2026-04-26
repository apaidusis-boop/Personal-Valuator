---
type: playbook
phase: C.2
created: 2026-04-26
last_updated: 2026-04-26
tags: [analyst, tracking, accuracy, predictions, playbook/measurement]
related:
  - "[[Index]]"
  - "[[wiki/methods/Variant_Perception]]"
---

# Analyst Tracking — Playbook (Fase C.2)

> **Princípio**: nenhum analyst é "right by default". Cada call tem que produzir outcome verificável; cada source ganha (ou perde) credibilidade ao longo do tempo. Sem track record, "consensus" é ruído.

## 🎯 Objectivo

Medir accuracy de cada source (analyst firm, YouTube channel, broker subscription) ao longo do tempo, para que `variant_perception` saiba quanto peso dar quando dizemos "we vs consensus".

## 📦 Schema (já existe — `predictions` table)

Schema vive em ambas as DBs (BR + US):

| Coluna | Tipo | Significado |
|---|---|---|
| `id` | int | autoincrement |
| `source` | text | `analyst:xp` / `analyst:fool` / `youtube:<channel>` / `analyst:btg` |
| `source_ref` | text | back-pointer (`insight:42`, `video:abc123`) |
| `ticker` | text | ticker referenciado |
| `prediction_date` | date | quando o call foi emitido |
| `price_at_pred` | float | preço no dia do call |
| `predicted_stance` | text | `bull` / `bear` / `neutral` |
| `price_target` | float | optional |
| `horizon_days` | int | 30 / 90 / 180 / 365 |
| `confidence` | float | 0-1 (extraído do tom do source) |
| `claim` | text | sentence-level summary |
| `evaluated_at` | date | NULL se ainda em janela |
| `price_at_eval` | float | preço quando expirou horizon |
| `outcome` | text | `pending` / `correct` / `wrong` / `partial` |

## 🔄 Fluxo de ingest

1. **Phase Q** (YouTube pipeline) → emite predictions de canais (`source='youtube:<canal>'`)
2. **Phase U** (Subscriptions ingest) → emite predictions de Suno/XP/WSJ/BTG (`source='analyst:<firm>'`)
3. **`predictions` row criada** com `outcome='pending'`
4. **Cron diário** (a wirar — `scripts/predictions_evaluate.py`):
   - Para cada row `outcome='pending' AND prediction_date + horizon_days <= today`
   - Pull current price + price_at_pred
   - Compute realized return
   - Match contra `predicted_stance`:
     - `bull` + return ≥ 5% → `correct`
     - `bull` + return ≤ -5% → `wrong`
     - `bull` + |return| < 5% → `partial`
     - (mirror para bear)
     - `neutral` + |return| < 5% → `correct`
   - Update `evaluated_at`, `price_at_eval`, `outcome`

## 📊 Track record (a medir após eval cron)

Métrica primária: **win_rate por source ao longo de 1y rolling**.

```sql
SELECT source,
       COUNT(*) AS calls,
       SUM(CASE WHEN outcome='correct' THEN 1 ELSE 0 END) AS correct,
       SUM(CASE WHEN outcome='wrong' THEN 1 ELSE 0 END) AS wrong,
       ROUND(100.0 * SUM(CASE WHEN outcome='correct' THEN 1 ELSE 0 END) / COUNT(*), 1) AS win_rate_pct
FROM predictions
WHERE outcome != 'pending'
  AND prediction_date >= date('now', '-365 days')
GROUP BY source
ORDER BY win_rate_pct DESC;
```

Sources já a tracker (2026-04-26):
- `analyst:xp` (87 reports), `analyst:fool` (18), `analyst:btg` (3 carteiras), `analyst:suno` (4 carteiras)
- `analyst:wsj`, `analyst:marketwatch` (~20 reports juntos)
- YouTube channels via Phase Q (`youtube:*`)

## 🎚 Calibração de variant_perception

Quando `variant_perception` diz "we are bullish vs consensus bear", o peso da divergência depende de quão accurate o consenso é:
- Source com win_rate ≥ 70% → divergir = high-conviction edge OU wrong
- Source com win_rate < 50% → consensus is noise, divergir é default

**Implementação prevista**: `agents/variant_perception.py` lê `predictions` via 1-year rolling window e ajusta `magnitude` por source-weight.

## 🚧 Estado actual / TODOs

- ✅ Schema `predictions` existe (62 BR + 10 US rows, mostly Phase U seed)
- ✅ Phase U + Phase Q emitem predictions
- ❌ `scripts/predictions_evaluate.py` ainda não existe — outcome stays `pending` para sempre (mesmo bug estrutural que paper_trade_signals tinha pré-Phase F)
- ❌ Source weighting em `variant_perception.py` não considera win_rate
- ❌ Wiki por firm (Bradesco BBI, XP, BTG, GS, JPM) — stubs separados

## 🔗 Cross-links

- [[Variant_Perception]] — onde tracking é consumido
- [[Phase_U_Subscriptions]] — pipeline de ingest analyst
- [[Phase_Q_YouTube]] — pipeline de ingest YouTube
- `scripts/paper_trade_close.py` — pattern reference (mesma estrutura de horizon eval)
