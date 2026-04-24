---
type: moc
name: 🏢 A Empresa Sintética
tags: [moc, agents, company, organization]
---

# 🏢 A Empresa Sintética

> Uma analyst-CFO boutique de 12 funcionários que opera 24/7 enquanto o **Founder** decide só o estratégico. Todos os empregados são agentes Python herdando de `BaseAgent`; cada um tem nome, cargo, departamento e horário.

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
