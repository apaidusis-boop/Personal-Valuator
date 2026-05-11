---
type: org_chart
tags: [agents, organization, hierarchy]
---

# 📊 Organograma — A Empresa Sintética

```
                          ┌────────────────────────┐
                          │      FOUNDER (Tu)      │
                          │     Decisões finais    │
                          │   Capital allocation   │
                          └───────────┬────────────┘
                                      │
        ┌────────────────┬────────────┼────────────┬────────────────┐
        │                │            │            │                │
 ┌──────▼──────┐  ┌──────▼──────┐  ┌──▼──────┐  ┌──▼───────┐  ┌────▼────────┐
 │  Aurora     │  │  Valentina  │  │ Ulisses │  │Aristóteles│  │    Regina   │
 │  Matina     │  │  Prudente   │  │Navegador│  │ Backtest  │  │    Ordem    │
 │(Morning     │  │(Chief Risk) │  │(Head of │  │(Head of   │  │(Compliance) │
 │ Analyst)    │  │             │  │Research)│  │Performance)│  │             │
 └──────┬──────┘  └──────┬──────┘  └────┬────┘  └──────┬─────┘  └─────────────┘
        │                │              │               │             ▲
        │                │              │               │             │ audita
        ▼                ▼              │               │             │
 ┌──────────────┐  ┌──────────────┐    ├───────────────┘              │ TODOS
 │   Wilson     │  │    Diabo     │    │                              │
 │    Vigil     │  │    Silva     │    │                              │
 │(Floor Trader)│  │(Contrarian)  │    │                              │
 └──────────────┘  └──────────────┘    │                              │
                                       │                              │
                                ┌──────┴──────┐                       │
                                │             │                       │
                          ┌─────▼─────┐ ┌─────▼──────┐                │
                          │  Teresa   │ │   Sofia    │                │
                          │   Tese    │ │ Clippings  │                │
                          │ (Research │ │ (Research  │                │
                          │   Coord)  │ │   Intern)  │                │
                          └───────────┘ └────────────┘                │
                                                                      │
                                                              ┌───────┴──────┐
                                                              │              │
                                                       ┌──────▼─────┐ ┌─────▼─────┐
                                                       │   Clara    │ │   Noé     │
                                                       │    Fit     │ │Arquivista │
                                                       │ (Portfolio │ │ (Data     │
                                                       │  Analyst)  │ │ Steward)  │
                                                       └────────────┘ └───────────┘

                          ┌────────────────────────┐
                          │    Zé Mensageiro       │  ←→ Telegram
                          │   (Telegram Desk)      │    Founder mobile
                          │  Reports directo ao    │
                          │       Founder          │
                          └────────────────────────┘
```

## Níveis hierárquicos

### L0 — Founder (tu)
- Único que decide capital real
- Recebe outputs; nunca gera outputs operacionais
- Aprova acções via Telegram (`/approve <id>`)

### L1 — Heads of Department (reports_to: founder)
- **Aurora Matina** (Operations)
- **Valentina Prudente** (Risk)
- **Ulisses Navegador** (Research)
- **Aristóteles Backtest** (Performance)
- **Regina Ordem** (Compliance) — audita todos L0-L2
- **Zé Mensageiro** (Desk/Contact) — reporta directo ao founder

### L2 — Specialists (reports_to: L1)
- **Wilson Vigil** (Aurora Matina)
- **Teresa Tese** (Ulisses Navegador)
- **Sofia Clippings** (Ulisses Navegador)
- **Diabo Silva** (Valentina Prudente)
- **Clara Fit** (self-supervising, Performance)
- **Noé Arquivista** (Regina Ordem)

## Departamentos × Horários

| Dept | Funcionários | Cadência agregada |
|---|---|---|
| 🏛 Operations | Aurora, Wilson, Noé | 07:00 diário + 15min contínuo + sábado 03:00 |
| 🔍 Research | Ulisses, Teresa, Sofia | 08:30 daily + sun 22:00 + mon 09:00 |
| 🛡 Risk | Valentina, Diabo | 21:00 daily + wed 10:00 |
| ⚖️ Compliance | Regina | 23:00 daily |
| 📈 Performance | Aristóteles, Clara | fri 20:00 + 30min contínuo |
| 📞 Desk | Zé | 2min poll contínuo |

## Salários (hardware + Ollama tokens)

Todos **$0/mês** — é o milagre da disciplina de tokens. Só o CEO (Founder, Claude on-demand) custa algo, mas ≤ $5/dia com budget cap.

## Recrutamento

Ver [[_MOC|MOC]] secção "Como contratar novo funcionário" — cargos em aberto (backlog):
- **Chief Economist** (macro regime changer) — vagamos
- **Press Officer** (news digest curator) — vagamos
- **Treasury Officer** (cash_reminder) — vagamos
- **QA Engineer** (data_quality_guardian) — vagamos
- **Portfolio Risk** (concentration_auditor) — vagamos

---

*Para hierarquia live/dataview, ver [[_dashboard]].*
