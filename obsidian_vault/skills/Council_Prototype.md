---
type: phase_note
phase: council_v1
date: 2026-04-30
status: prototype_validated
related: [STORYT_1, STORYT_2.0, synthetic_ic, variant_perception, V10_deepdive]
tags: [council, storyt2, multi_agent, debate, prototype]
---

# Council Prototype — STORYT_2.0 Camada 5.5

> Pre-publication multi-voice debate inserted between STORYT_1's Classification (5) and Narrative (6) layers. Three voices argue across two rounds before the narrative engine ships.

## Why this exists

**The gap STORYT_1 v5.0 leaves**: Camadas 1-5 are silent; only Camada 6 writes. That protects the narrative from technical contamination but ALSO prevents specialist voices from disagreeing visibly. The user's complaint — "que se comuniquem antes de me apresentar algo que eu terei que ir depois e mudar tudo" — is a request for *pre-flight review*.

**The gap existing agents leave**: `synthetic_ic.py` runs *after* the dossier exists; `variant_perception.py` runs *after* a thesis is written. Both arbitrate finished output. None of them shape the dossier construction itself.

**The Council fills both gaps**: deliberation BEFORE the narrative engine fires.

## Architecture

```
agents/council/
├── __init__.py            # exports run_council, build_dossier
├── dossier.py             # CouncilDossier — factual layer (no opinions)
├── personas.py            # 3 role frames + Round 1/2 prompts
├── coordinator.py         # 2-round orchestration + deterministic vote synthesis
├── render.py              # Markdown + JSON output
└── __main__.py            # CLI: python -m agents.council ITSA4 [--market br]
```

### The three voices (Modo A-BR prototype)

| Role | Function | Veto power |
|---|---|---|
| **Sector Specialist** | Defends method-correct framing for the asset's Modo. Routed by `dossier.modo` (A/B/C/D × BR/US). Currently A_BR is fleshed out; B/C/D have stub frames. | P/TBV in industrial, DCF without Selic-adjusted WACC, peer comp without jurisdiction adjustment |
| **Risk Officer** | Pre-Mortem rigour + distress flags + observable triggers. Pulls Piotroski/Altman/Beneish concerns. Anchors on disconfirmation triggers from vault thesis when present. | Material data missing, distress trigger active without mitigation, CCC deteriorating >30% YoY |
| **Portfolio Officer** | Fit vs current portfolio, sizing, correlation, currency isolation (BRL→BR / USD→US per memory rule). | Correlation > 0.7 with existing position, weight > 10% without explicit concentration thesis |

### Two rounds of debate

- **Round 1** (blind): each voice writes opening statement seeing only the dossier, not peers
- **Round 2** (responsive): each voice reads the other two's R1 and can challenge / agree / revise stance
- **Synthesis**: deterministic majority vote on R2 stances → confidence (high if unanimous, medium if 2/3, low if split or any `NEEDS_DATA`); LLM writes consensus_points + dissent_points + pre_publication_flags around the locked vote

The synthesis intentionally **preserves dissent** — the user sees disagreement explicitly rather than the council flattening it into a single voice.

## Test runs

### ITSA4 (held, high-conviction, with full vault thesis)

```
=== Council: BR:ITSA4 ===
  Modo (auto): A | Sector: Holding | Held: True
  Round 1: sector=HOLD risk=HOLD portfolio=HOLD
  Round 2: sector=HOLD risk=HOLD portfolio=HOLD
  Synthesis: HOLD (high)  53.1s
  Pre-publication flag: NAV discount >25% sem catalisador deve ser mencionado antes da publicação
```

**What worked**: Risk Officer pulled "Itaú ROE < 12% em 2 quarters consecutivos" directly from the vault thesis disconfirmation triggers — surfacing the exact tripwire the user wrote into thesis and would otherwise be buried.

Portfolio Officer surfaced concentration concern: "atual posição já está em 9.5%, e um TRIM pode ser necessário". This is signal the user would otherwise have to fish out manually.

### MOTV3 (watchlist, no vault thesis, weaker fundamentals)

```
=== Council: BR:MOTV3 ===
  Modo (auto): A | Sector: Industrials | Held: False
  Round 1: sector=HOLD risk=AVOID portfolio=HOLD
  Round 2: sector=HOLD risk=AVOID portfolio=HOLD
  Synthesis: HOLD (medium)  40.1s
  Pre-publication flags:
    - CCC deteriorando >30% YoY sem explicação
    - dividend yield baixo e ND/EBITDA acima de 3x
```

**What worked**: genuine disagreement (Risk=AVOID, others=HOLD) → confidence dropped to **medium** correctly. Risk Officer caught DivStreak=2.00 which fails the Modo A-BR Graham screen requirement (≥5 anos) — exactly the kind of veto signal that would otherwise pass into a narrative unchallenged.

## What's NOT built yet (deferred to Sprint 2+)

1. **Sector Specialists for B/C/D modes** — frames exist as stubs in `personas.py::SECTOR_FRAMES`. Banks (BR + US), Commodities, FIIs/REITs need their own dedicated frames promoted from method YAML.
2. **Synthetic IC integration** — currently runs separately; could be invoked as a 4th voice for high-conviction or large-position decisions.
3. **`ii council` CLI wiring** — currently runs via `python -m agents.council <TICKER>`. Wire into `ii.bat` once UX validated.
4. **Council perpetuum** — daily/weekly batch run for top conviction holdings, output digest in Captain's Log Telegram brief.
5. **Mission Control front-end** — surface council transcripts in `/ticker/<TK>` page next to the existing dossier.
6. **Override flags** — `--sector-frame B_BR` to test whether a holding like ITSA4 should be reframed as a bank specialist's responsibility.

## Decision points for the user

After validating the prototype, three branches:

**A — Iterate on Modo A-BR before expanding modes**
Run council on 5-10 more tickers (mix holdings + watchlist, mix high/low conviction). Measure: does dissent surface in the right cases? Are pre-publication flags actionable? Refine the role frames based on what comes out.

**B — Promote and expand modes**
Treat the Modo A-BR prototype as proven; build out Banks (B_BR + B_US), Commodities (C_BR), FIIs (D_BR), REITs (D_US). Each mode gets its own Sector Specialist prompt with sector-specific veto rules.

**C — Integrate with existing pipeline**
Wire council into `ii deepdive` so the V10 deepdive runs council BEFORE the Strategist writes the dossier. Currently V10 is single-pass; council would gate it.

Recommended order: **A → B → C**. Validate the architecture surfaces useful signal across more tickers in the same Modo before adding complexity.

## Cost (everything runs on Ollama Qwen 2.5 14B local)

- ITSA4 run: 53.1s end-to-end (3 R1 + 3 R2 + 1 synthesis = 7 Ollama calls, ~7-8s each)
- MOTV3 run: 40.1s
- Zero Claude tokens
- Compatible with overnight/perpetuum batch use

## Outputs

- `obsidian_vault/dossiers/<TICKER>_COUNCIL.md` — full transcript with rounds visible
- `obsidian_vault/dossiers/<TICKER>_COUNCIL.json` — sidecar for programmatic consumption (Mission Control, etc.)
- This file (`Council_Prototype.md`) — architectural notes
