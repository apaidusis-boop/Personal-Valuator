---
type: moc
name: 🏢 A Empresa Sintética
tags: [moc, agents, company, organization]
---

# 🏢 A Empresa Sintética

> Uma analyst-CFO boutique de **23 funcionários** que opera 24/7 enquanto o **Founder** decide só o estratégico. 14 são agentes autónomos (cron-driven) e 9 são especialistas on-demand do Council STORYT_2.0. Todos têm nome, cargo, departamento.

## Navegação rápida

- [[_org_chart|📊 Organograma]] — hierarquia + departamentos
- [[_flow_diagram|🔀 Fluxo de Informação]] — como os sinais viajam
- [[_information_levels|🧠 Níveis de Informação]] — o que cada um vê da DB
- [[_dashboard|🩺 Health Dashboard]] — estado actual (Regina Ordem atualiza)
- [[_performance_ranking|📊 Performance Ranking]] — accuracy por source (Aristóteles Backtest)

## 👥 Funcionários por departamento

### 🏛 Operations (Desk)
- [[personas/Aurora Matina|Aurora Matina]] — Morning Analyst (`morning_briefing`)
- [[personas/Wilson Vigil|Wilson Vigil]] — Floor Trader / Desk Watch (`watchdog`)
- [[personas/Noé Arquivista|Noé Arquivista]] — Data Steward (`data_janitor`)

### 🔍 Research
- [[personas/Ulisses Navegador|Ulisses Navegador]] — Head of Research (`research_scout`)
- [[personas/Teresa Tese|Teresa Tese]] — Research Coordinator (`thesis_refresh`)
- [[personas/Sofia Clippings|Sofia Clippings]] — Research Intern (`subscription_fetch`)

### 🛡 Risk
- [[personas/Valentina Prudente|Valentina Prudente]] — Chief Risk Officer (`risk_auditor`)
- [[personas/Diabo Silva|Diabo Silva]] — Chief Contrarian (`devils_advocate`)

### ⚖️ Compliance
- [[personas/Regina Ordem|Regina Ordem]] — Compliance Officer (`meta_agent`)

### 📈 Performance
- [[personas/Aristóteles Backtest|Aristóteles Backtest]] — Head of Performance (`analyst_backtest`)
- [[personas/Clara Fit|Clara Fit]] — Portfolio Analyst (`portfolio_matcher`)

### 📞 Desk (Contact)
- [[personas/Zé Mensageiro|Zé Mensageiro]] — Telegram Desk (`telegram_controller`)

### 🎓 Specialists — Council STORYT_2.0 (on-demand)

> Convocados quando o Council debate um ticker. Cada um defende framing correcto do seu Modo×Jurisdição e tem veto power sobre métricas inadequadas. Cada análise que fazem fica em `agents/<Nome>/reviews/<TICKER>_<DATE>.md`.

**Sector specialists** (routados por Modo×Jurisdição):

| Especialista | Modo×Jur | Cobre |
|---|---|---|
| [[personas/Tião Galpão\|Tião Galpão]] | A-BR | Industriais & Consumer BR (POMO3, RAPT4, RENT3, MULT3, ITSA4 industrial) |
| [[personas/Charlie Compounder\|Charlie Compounder]] | A-US | Industrials/Consumer US Buffett-frame (JNJ, PG, KO, ACN, ABBV) |
| [[personas/Diego Bancário\|Diego Bancário]] | B-BR | Bancos BR (BBDC4, ITUB4, BBAS3, ITSA4 holding bancária) |
| [[personas/Hank Tier-One\|Hank Tier-One]] | B-US | Bancos US (JPM, BAC, GS, WFC, MS) |
| [[personas/Aderbaldo Cíclico\|Aderbaldo Cíclico]] | C-BR | Commodities BR (VALE3, PRIO3, SUZB3, GGBR4) |
| [[personas/Lourdes Aluguel\|Lourdes Aluguel]] | D-BR | FIIs BR (XPML11, RBRX11, BTLG11, VGIR11, PVBI11) |
| [[personas/Walter Triple-Net\|Walter Triple-Net]] | D-US | REITs US (O, STAG, AMT, PLD) |

**Cross-cutting** (vão a todo o council):

- [[personas/Mariana Macro\|Mariana Macro]] — Chief Macro Strategist (Selic/Fed/câmbio/ciclo, NÃO escolhe ações)
- [[personas/Pedro Alocação\|Pedro Alocação]] — Capital Allocator (sizing/correlação/fit)

**Risk** (já existia, agora também integra Council):

- [[personas/Valentina Prudente\|Valentina Prudente]] — usa o seu CRO frame no Council também

## 🎯 Funções delegadas (o que o Founder não faz mais)

| Antes (fricção manual) | Agora (quem faz) |
|---|---|
| Abrir terminal para ver o que se passou durante a noite | Aurora Matina envia briefing às 07:00 via Telegram |
| Monitorar triggers a cada hora | Wilson Vigil faz 15min em 15min |
| Decidir se um holding está em drift de tese | Valentina Prudente flagga diariamente às 21:00 |
| Procurar bear cases para contrariar próprio bias | Diabo Silva gera toda quarta às 10:00 |
| Refresh manual de thesis notes com live snapshots | Teresa Tese re-injecta domingos 22:00 |
| Ingerir reports Fool / XP / WSJ | Sofia Clippings traz segunda 09:00 |
| Descobrir novos CVM/SEC filings | Ulisses Navegador scout 08:30 daily |
| Classificar insights: relevante ou ruído? | Clara Fit faz 30 em 30 min |
| Limpar DB, arquivar reports antigos | Noé Arquivista sábado 03:00 |
| Saber quem está a errar nas predictions | Aristóteles Backtest sexta 20:00 |
| Auditar os próprios agents | Regina Ordem daily 23:00 (auto-disable failures) |
| Delegar comandos remotamente | Zé Mensageiro Telegram Desk 2min poll |

## 📐 Princípios constitucionais

- 🚨 [[../wiki/playbooks/Token_discipline|Token discipline]] — todos os funcionários usam Ollama local; Claude é para o CEO apenas
- [[../wiki/playbooks/Agents_layer|Agents layer]] — arquitectura técnica
- [[../wiki/playbooks/Telegram_setup|Telegram setup]] — configurar Zé Mensageiro
- [[../wiki/playbooks/Analysis_workflow|Analysis workflow]] — como Founder consome outputs

## 🎓 Como contratar um novo funcionário

```bash
ii agents create <slug> --schedule "daily:10:00" --desc "O que faz"
# edit agents/<slug>.py — implementar execute_impl()
# edit config/agents.yaml — adicionar employee_name, title, bio, department
# criar persona card em obsidian_vault/agents/personas/<Nome>.md
```

---

*Atualização: cada run de meta_agent refresca [[_dashboard]].*
