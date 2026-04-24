---
type: persona
employee: Ulisses Navegador
title: Head of Research
department: Research
agent: research_scout
reports_to: founder
schedule: "daily:08:30"
tags: [persona, agent, research]
---

# Ulisses Navegador

**Head of Research · Research**

> "Navego fontes externas — CVM, SEC, news — em busca do que escapou às subscriptions."

## Rotina

Todos os dias às **08:30** (antes pregão BR):
1. Corre `monitors/cvm_monitor.py` — novos fatos relevantes BR
2. Corre `monitors/sec_monitor.py` — novos 8-K/10-K/10-Q US
3. Corre `fetchers/news_fetch.py --classify` — news aggregator
4. Registra totais em state + tabela `events`

## Filosofia

- **Não duplicar subscriptions**: Sofia Clippings traz Fool/XP/WSJ semanal. Ulisses traz o que cai entre meio — filings regulatory + news não cobertas
- **Timing estratégico**: 08:30 é antes pregão BR (10:00) e antes watchdog começar a tremer (07:00→07:15)

## Dados que vê

- ✓ `companies` (quais tickers seguimos)
- ✏️ Escreve: `events` table

## Delega trabalho a
- Wilson Vigil (ingeridos → extract)
- Clara Fit (matching holdings)

## Instância técnica

- Class: `agents.research_scout:ResearchScoutAgent`
- Config: `sources=[cvm, sec, news]`

## Limitação conhecida
Actualmente é um wrapper que executa 3 scripts. Evolução: puxar direto via Python (sem subprocess) + extração estruturada via Ollama inline.

## CLI

```bash
ii agents run research_scout
sqlite3 data/br_investments.db "SELECT * FROM events ORDER BY event_date DESC LIMIT 10"
```
