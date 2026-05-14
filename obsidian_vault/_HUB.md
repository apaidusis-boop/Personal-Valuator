---
type: hub
name: 🏛️ Investment Intelligence — HUB
tags: [hub, moc, root]
cssclasses: [hub]
---

# 🏛️ Investment Intelligence — HUB

> O ponto de entrada do vault. Todo o trabalho da empresa sintética passa por aqui.
>
> **Founder**: Antonio · **Last update**: gerado dinamicamente pelo pipeline.

---

## 📖 Storytelling — Dossiers (STORYT_3.0)

> Cada ticker tem um documento `<TICKER>_STORY.md` com 8 actos completos: Identidade · Contexto · Evolução · Balanço · Múltiplos · Quality Scores · Moat & Gestão · Veredito (DCF + Pre-Mortem + Rating + Nota divergente). Gerado pelo Council Camada 5.5 → Narrative Camada 6.

```dataview
TABLE
  market AS "Mkt",
  modo AS "Modo",
  council_stance AS "Stance",
  council_confidence AS "Conf",
  philosophy_primary AS "Filosofia",
  dcf_base AS "DCF base",
  date AS "Data"
FROM "dossiers"
WHERE type = "storyt2_narrative"
SORT date DESC
LIMIT 20
```

**Comando para gerar novo dossier**:
```bash
python -m agents.council.story <TICKER> --market br
```

→ produz:
- `dossiers/<TICKER>_STORY.md` (latest, com Evidence Ledger + Peer comparison real)
- `dossiers/archive/<TICKER>_STORY_<DATE>.md` (versionado, audit trail)
- `dossiers/<TICKER>_COUNCIL.md` (transcript do debate)
- `dossiers/<TICKER>_DELTA_<DATE>.md` (se há prior snapshot — diff vs último run)
- `data/dossier_snapshots/<TICKER>/<DATE>.json` (replicagem programática)

## 🔄 Deltas — o que mudou desde o último run

```dataview
TABLE
  prior_date AS "Anterior",
  current_date AS "Actual",
  days_apart AS "Dias"
FROM "dossiers"
WHERE type = "storyt2_delta"
SORT current_date DESC
LIMIT 10
```

---

## 🏛️ Council — Transcripts dos debates (Camada 5.5)

> Onde fica preservado o debate de 2 rondas entre os especialistas. Mostra dissenso, não consenso forçado.

```dataview
TABLE
  market AS "Mkt",
  modo AS "Modo",
  final_stance AS "Stance",
  confidence AS "Conf",
  specialists AS "Quem esteve",
  date AS "Data"
FROM "dossiers"
WHERE type = "council_dossier"
SORT date DESC
LIMIT 20
```

---

## 👥 Os Funcionários — A Empresa Sintética

→ [[agents/_MOC|👥 Empresa sintética completa]] (23 funcionários, organograma, departamentos)

### Departamentos

- 🏛 [[ops.briefing|Operations]] — desk diário (Aurora, Wilson, Noé, Zé)
- 🔍 [[research.scout|Research]] — Ulisses, Teresa, Sofia
- 🛡 [[risk.drift-audit|Risk]] — Valentina, Diabo
- ⚖️ [[risk.compliance|Compliance]] — Regina
- 📈 [[perf.backtest-analysts|Performance]] — Aristóteles, Clara
- 🎓 **Specialists (Council)** — Tião Galpão, Charlie Compounder, Diego Bancário, Hank Tier-One, Aderbaldo Cíclico, Lourdes Aluguel, Walter Triple-Net, Mariana Macro, Pedro Alocação

### Trabalho recente dos especialistas

```dataview
TABLE
  ticker AS "Ticker",
  role AS "Função",
  stance_round1 AS "R1",
  stance_round2 AS "R2",
  flipped AS "Flip?"
FROM "agents"
WHERE type = "agent_review"
SORT date DESC
LIMIT 30
```

---

## 📊 Holdings & Portfólio

- [[Holdings|📈 Holdings actuais]]
- [[Allocation|🥧 Allocation]]
- [[Rebalance|⚖️ Rebalance]]
- [[Earnings Surprise|🎯 Earnings Surprises]]

```dataview
LIST FROM "tickers" WHERE held = true
SORT file.name ASC
LIMIT 30
```

---

## 📚 Bibliotheca — Conhecimento

- [[Bibliotheca/_Index|📖 Index Bibliotheca]] — clippings, knowledge cards, glossary
- [[Glossary/_Index|🧠 Glossary]] — métricas com contraméricas
- [[Roadmap_Always_On_Workforce|🛣️ Roadmap]]

---

## 🎯 Skills & Frameworks

- [[skills/_MOC|🛠️ Skills arsenal]] — 33 skills avaliadas
- [[skills/Council_Prototype|🏛️ Council Prototype]] — STORYT_2.0 architectural notes
- [[CONSTITUTION|📜 Constitution]] — master doc vivo

---

## 🌐 Outros pontos de entrada

- [[Home|🏠 Home]] — vista do user
- [[_MOC|🗺️ MOC root]]
- [[Mega_Audit_2026-04-28|🔍 Mega Audit recente]]

---

*Para gerar novo storytelling: `python -m agents.council.story <TICKER>`. Para ver o último: navega `dossiers/` na sidebar (ou usa as Dataview tables acima).*
