---
type: phase_ff_finding
date: 2026-05-06
phase: FF Bloco 1 (Decision Quality)
severity: high (was hidden before this session)
tags: [phase-ff, calibration, bloco1, root-cause, finding]
---

# Phase FF Bloco 1 — Real unblock (the prices were not the issue)

> **TL;DR**: A memória dizia "Phase FF Bloco 1 bloqueada — SPY/BOVA11 prices zero rows". Verificação 2026-05-06 mostrou que **prices estão lá** (501/499 rows desde 2024). O bloqueador real era diferente: **`vh record` nunca foi adicionado ao `daily_run.bat`**, então `verdict_history` tinha apenas 31 rows de uma única data (2026-04-23). A "calibration curve" não era uma curva — era um snapshot single-day. Wiring corrigido neste commit.

## Estado verificado (2026-05-06 14:xx)

```
prices.SPY      US: 501 rows (2024-05-06 → 2026-05-05) ✅
prices.BOVA11   BR: 499 rows (2024-05-06 → 2026-05-05) ✅
verdict_history US: 20 rows ALL from 2026-04-23      ❌
verdict_history BR: 11 rows ALL from 2026-04-23      ❌
```

**Diagnóstico**: `daily_run.bat` chamava `analytics.decision_quality update --window 30 --market both` (que **fecha** verdicts antigos contra forward returns), mas **nunca chamava** `scripts/verdict_history.py record` (que **cria** os verdicts diários). Sem feed, `update` não tem nada a fechar.

`vh record` foi corrido manualmente uma vez em 2026-04-23 (talvez durante setup da Phase FF). Depois nada.

## Calibration "curve" pré-fix (snapshot single-day, ENGANADORA)

```
US (n=20, todos 2026-04-23, fechados após +13d):
  40-60 conv → 42.9% bench-hit (n=7)
  60-80     → 25.0%             (n=12)   ← inversão suspeita
  80-100    → 100%              (n=1)

BR (n=9):
  40-60 → 0.0%     (n=5)
  60-80 → 0.0%     (n=1)
  80-100 → 33.3%   (n=3)
```

Os dados acima **não são curva de calibração**. São o resultado de UMA passagem do verdict engine em 2026-04-23, cruzada com 13 dias de mercado. Não há diversidade temporal — todos os verdicts foram gerados sob as mesmas condições macro/regime/mood.

A inversão (60-80 < 40-60) que a `decision_quality calibration` reportou pode ser real ou artefacto de single-day — impossível distinguir até termos 20+ datas. **Não agir baseado nesta inversão.**

## Fix aplicado

Commit `e0823c5`:
```bat
echo [VH-RECORD] verdict_history record  (Phase FF: snapshot today's verdicts) >> "%LOG%"
"%PY%" scripts\verdict_history.py record >> "%LOG%" 2>&1
```

Inserido entre `[BENCHMARKS]` (que actualiza SPY/BOVA11/sector ETFs) e `[DECISION-QUALITY] update` (que fecha verdicts ≥30d).

Order rationale:
1. Benchmarks fresh primeiro → preço de hoje disponível.
2. **vh record** → grava verdicts de hoje contra preço fresco.
3. update → fecha verdicts de há 30+ dias contra preço actual.

`vh record` é idempotente per (ticker, date) — re-run no mesmo dia é no-op.

## Estado pós-fix (2026-05-06)

Manual run inseriu hoje:
```
US verdict_history: 20 → 41  (+21 verdicts holdings)
BR verdict_history: 11 → 23  (+12 verdicts holdings)
1 erro: BTLG12 KeyError 'change_1d_pct' — residual position 48 shares @ R$0.09, no prices in yfinance, error caught and skipped (cosmético)
```

Verdicts de hoje têm `outcome_price=NULL` — vão fechar gradualmente conforme `decision_quality update` corre nos próximos 30 dias.

## Quando esperar calibração genuína

| Data | n esperado (holdings) | Observação |
|---|---|---|
| 2026-06-06 | ~62 (US) + ~36 (BR) | Primeiros verdicts de 2026-05-06 fecham (+30d window) |
| 2026-07-06 | ~125 + ~70 | 2 meses de feed contínuo, 5 datas distintas fechadas |
| 2026-08-06 | ~190 + ~108 | **Limiar mínimo para conviction calibration ser meaningful** (n≥30 por bin) |
| 2026-08-06 | — | Bloco 1 efectivamente concluído (calibration curve com n adequado) |

Phase GG (Capital Deployment) prerequisite era "≥90 dias de validated verdicts". Pré-fix esse contador era ~13 dias e congelado. Pós-fix começa a contar de 2026-05-06.

## Lição

Memória `phase_ff_calibration_loop.md` foi escrita com diagnóstico errado (prices, não feed). Verificação independente apanhou-o.

**Aplicação retrospectiva da regra 7 (verification-before-completion, adoptada hoje)**: a memória dizia "Bloqueador imediato — SPY/BOVA11 zero rows" sem ter executado o query. Se tivesse aplicado a regra na sessão original, o erro de diagnóstico tinha sido apanhado.

## Próximos checkpoints

- [ ] 2026-05-13: confirm `daily_run.bat` está a correr `vh record` (verificar last log + verdict_history MAX(date))
- [ ] 2026-06-06: primeiros verdicts de hoje fecham via `decision_quality update`. Re-run `calibration` — se mantém inversão 60-80 < 40-60 com sample maior, é sinal genuíno
- [ ] 2026-08-06: Bloco 1 done quando calibration curve tem n≥30 por bin

## Sources

- Memory original: `phase_ff_calibration_loop.md` (atualizada 2026-05-06 com correcção)
- Constitution: secção "Phase FF — Calibration Loop"
- Code: `scripts/verdict_history.py`, `analytics/decision_quality.py`, `scripts/daily_run.bat:57-61`
