---
type: flow_diagram
tags: [agents, flow, information, pipeline]
---

# 🔀 Fluxo de Informação — Como os sinais viajam

```
┌─────────────────────────────────────────────────────────────────┐
│ EXTERNAL SOURCES (world)                                        │
│   brapi · yfinance · SEC · CVM · FRED · Fool · XP · WSJ · YT    │
└────────┬────────────────────────┬───────────────┬───────────────┘
         │                        │               │
         ▼                        ▼               ▼
 ┌───────────────┐        ┌────────────────┐  ┌─────────────┐
 │   FETCHERS    │        │   SCRAPERS     │  │  MONITORS   │
 │   (cron)      │        │ (weekly+manual)│  │  (daily)    │
 └───────┬───────┘        └────────┬───────┘  └──────┬──────┘
         │                         │                 │
         └──────────┬──────────────┴─────────────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │    SQLite 2 DBs     │  ← single source of truth
         │   (BR + US isolated)│
         └──┬───────────────┬──┘
            │               │
            │               └──────────────────┐
            ▼                                  ▼
   ┌────────────────┐             ┌─────────────────────────┐
   │ Sofia Clippings│             │ Ulisses Navegador       │
   │ (segunda 09h)  │             │ (daily 08:30)           │
   │ Weekly fetch   │             │ CVM/SEC/news scout      │
   └───────┬────────┘             └───────────┬─────────────┘
           │                                  │
           └───────────┬──────────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │ analyst_reports table │
           │  (raw + extracted)    │
           └───────────┬───────────┘
                       │
           ┌───────────┼──────────────┐
           │                          │
           ▼                          ▼
   ┌──────────────┐          ┌────────────────┐
   │ Wilson Vigil │          │  Clara Fit     │
   │ (15m auto-   │          │  (30m recent   │
   │  extract     │          │   insights →   │
   │  Ollama)     │          │   fit holdings)│
   └──────┬───────┘          └────────┬───────┘
          │                           │
          │                           ▼
          │              ┌──────────────────────┐
          │              │  watchlist_actions   │ ◄── triggers.yaml
          │              │  (decision journal)  │ ◄── risk_auditor
          │              └──────────┬───────────┘ ◄── portfolio_matcher
          │                         │
          │                         ▼
          │               ┌────────────────────┐
          │               │   Aurora Matina    │
          │               │  (07:00 synthesis) │
          │               └─────────┬──────────┘
          │                         │
          ├─────────────────────────┼──────────────────┐
          │                         │                  │
          ▼                         ▼                  ▼
   ┌──────────────┐         ┌──────────────┐   ┌──────────────┐
   │  Valentina   │         │    Diabo     │   │   Teresa     │
   │  Prudente    │         │    Silva     │   │    Tese      │
   │ (21h daily   │         │ (wed 10h     │   │ (sun 22h     │
   │  drift)      │         │  bear cases) │   │  snapshots)  │
   └──────┬───────┘         └──────┬───────┘   └──────┬───────┘
          │                        │                   │
          └──────────┬─────────────┴───────────────────┘
                     │
                     ▼
        ┌─────────────────────────────┐
        │   Obsidian Vault            │
        │   (wiki + holdings + agents)│
        └────────────┬────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │ Aristóteles      │
           │ Backtest         │         ┌──────────────────────┐
           │ (fri 20h)        ├────────►│ predictions table    │
           │ Mede accuracy    │         │ → source credibility │
           └──────────────────┘         └──────────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │  Regina Ordem    │
           │  (23h — audita   │
           │   tudo + disable │
           │   failing)       │
           └────────┬─────────┘
                    │
                    ▼
           ┌──────────────────┐
           │     Founder      │
           │   (Telegram via  │
           │  Zé Mensageiro)  │
           └──────────────────┘
```

## 📬 Canais de comunicação

### Inbound (agents aprendem do mundo)
- **Fetchers** — brapi, yfinance, FRED → scheduled cron
- **Scrapers** — Fool/XP/WSJ via Sofia Clippings + Playwright persistent
- **Monitors** — CVM/SEC via Ulisses Navegador
- **YouTube** — on-demand `ii ingest <url>`

### Internal (agents falam entre si via DB)
- `analyst_reports` (extracção Wilson) → `analyst_insights`
- `analyst_insights` → Clara Fit → `watchlist_actions`
- `watchlist_actions` → Aurora Matina resume → briefing
- `analyst_insights` → Aristóteles Backtest → `predictions` → credibility
- `agents/*.json` state → Regina Ordem → dashboard
- `predictions` → Clara Fit weight adjustment

### Outbound (agents falam ao founder)
- **Telegram push** — Aurora (daily), Wilson (alerts), Valentina (risk), Regina (cohort unhealthy)
- **Obsidian vault** — persona status pages, dashboards, briefings, wiki updates
- **Telegram pull (two-way)** — Zé Mensageiro recebe /status /run /approve

### Return path (founder → sistema)
- Telegram `/approve <id>` → Zé Mensageiro → `UPDATE watchlist_actions`
- Manual edits em wiki/holdings/*.md → próxima run de Teresa Tese preserva entre markers

## 🚦 Criticidade dos fluxos

| Fluxo | Se falhar | Severity |
|---|---|---|
| brapi/yfinance fetch | Dados stale → decisões com info antiga | 🔴 Alta |
| Sofia Clippings | Weekly reports atrasados | 🟡 Média |
| Wilson auto-extract | Insights pending acumulam | 🟡 Média |
| Aurora briefing | Founder acorda sem sinopse | 🟢 Baixa (pode correr manual) |
| Valentina drift | Holding drift não detectado | 🔴 Alta |
| Regina Ordem | Agents failing sem auto-disable | 🟡 Média |
| Zé Mensageiro | Founder perde canal remote | 🟡 Média |

## 🔁 Ciclos de feedback

1. **Curto (30 min)**: Clara Fit → flagga high-relevance → Aurora menciona no próximo briefing
2. **Diário**: Valentina/Ulisses produzem sinais → Aurora consolida manhã seguinte
3. **Semanal**: Aristóteles avalia predictions → Clara ajusta weights → qualidade flags sobe
4. **Mensal implícito**: Regina audita padrões → founder revisita agents.yaml

---

*Para estado live dos fluxos, ver [[_dashboard]].*
