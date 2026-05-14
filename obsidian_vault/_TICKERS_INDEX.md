---
type: index
generated: 2026-05-14
tags: [hub, master_index, holdings]
parent: "[[CONSTITUTION_Pessoal]]"
related: "[[_LEITURA_DA_MANHA]]"
---

# 🗂️ Tickers Index — porta de entrada matinal

> Um link por holding. Clica para abrir o **hub consolidado** do ticker (panorama, histórico cronológico, todos os artefactos). Substitui o atropelo de DOSSIE / STORY / COUNCIL / FILING / OVERNIGHT espalhados.

**Filosofia**: cada nome é uma porta. Atrás dela está tudo (e ordenado).

## 🇧🇷 Brasil (12)

| Ticker | Nome | Sector | Posição | Verdict | Score | Último deepdive |
|---|---|---|---:|---|---:|---|
| [[hubs/BBDC4\|BBDC4]] | Bradesco | Banks | 1837 | `WATCH` | 6.58 | — |
| [[hubs/BTLG11\|BTLG11]] | BTG Logística | Logística | 166 | `HOLD` | 5.10 | — |
| [[hubs/ITSA4\|ITSA4]] | Itaúsa | Holding | 2485 | `ADD` | 7.55 | — |
| [[hubs/IVVB11\|IVVB11]] | iShares S&P 500 (BRL hedged) | ETF-US | 11 | `SELL` | 2.97 | — |
| [[hubs/KLBN11\|KLBN11]] | KLBN11 | Materials | 1059 | `SELL` | 3.02 | — |
| [[hubs/KNHF11\|KNHF11]] | Kinea Hedge Fund FII | Híbrido | 175 | `SKIP` | 5.10 | — |
| [[hubs/LFTB11\|LFTB11]] | iShares Tesouro Selic ETF | ETF-RF | 873 | `SELL` | 2.97 | — |
| [[hubs/PRIO3\|PRIO3]] | PRIO3 | Oil & Gas | 503 | `AVOID` | 3.13 | — |
| [[hubs/PVBI11\|PVBI11]] | VBI Prime Properties | Corporativo | 217 | `SELL` | 3.73 | — |
| [[hubs/VALE3\|VALE3]] | VALE3 | Mining | 501 | `HOLD` | 6.13 | 2026-05-09 |
| [[hubs/VGIR11\|VGIR11]] | Valora CRI | Papel (CRI) | 1776 | `HOLD` | 5.97 | — |
| [[hubs/XPML11\|XPML11]] | XP Malls | Shopping | 159 | `HOLD` | 5.70 | — |

## 🇺🇸 EUA (21)

| Ticker | Nome | Sector | Posição | Verdict | Score | Último deepdive |
|---|---|---|---:|---|---:|---|
| [[hubs/AAPL\|AAPL]] | Apple | Technology | 5 | `HOLD` | 6.62 | — |
| [[hubs/ABBV\|ABBV]] | AbbVie | Healthcare | 7 | `SKIP` | 4.95 | — |
| [[hubs/ACN\|ACN]] | Accenture | Technology | 4 | `WATCH` | 6.62 | — |
| [[hubs/BLK\|BLK]] | BlackRock | Financials | 2 | `HOLD` | 4.87 | — |
| [[hubs/BN\|BN]] | Brookfield Corp | Financials | 7 | `SELL` | 3.52 | — |
| [[hubs/BRK-B\|BRK-B]] | Berkshire Hathaway B | Holding | 1 | `HOLD` | 4.42 | — |
| [[hubs/GREK\|GREK]] | Global X MSCI Greece ETF | ETF | 5 | `WATCH` | 7.00 | — |
| [[hubs/GS\|GS]] | Goldman Sachs | Financials | 1 | `HOLD` | 5.92 | — |
| [[hubs/HD\|HD]] | Home Depot | Consumer Disc. | 1 | `HOLD` | 5.95 | — |
| [[hubs/JNJ\|JNJ]] | Johnson & Johnson | Healthcare | 10 | `HOLD` | 5.68 | 2026-05-13 |
| [[hubs/JPM\|JPM]] | JPMorgan Chase | Financials | 7 | `HOLD` | 5.98 | 2026-05-09 |
| [[hubs/KO\|KO]] | Coca-Cola | Consumer Staples | 11 | `HOLD` | 6.90 | — |
| [[hubs/NU\|NU]] | Nu Holdings | Financials | 13 | `SELL` | 3.27 | — |
| [[hubs/O\|O]] | Realty Income | REIT | 30 | `WATCH` | 6.27 | — |
| [[hubs/PG\|PG]] | Procter & Gamble | Consumer Staples | 10 | `WATCH` | 6.97 | — |
| [[hubs/PLD\|PLD]] | Prologis | REIT | 2 | `HOLD` | 6.13 | — |
| [[hubs/PLTR\|PLTR]] | Palantir | Technology | 2 | `HOLD` | 5.23 | — |
| [[hubs/TEN\|TEN]] | Tsakos Energy Navig. | Energy | 35 | `AVOID` | 4.18 | — |
| [[hubs/TSLA\|TSLA]] | Tesla | Consumer Disc. | 3 | `HOLD` | 4.16 | — |
| [[hubs/TSM\|TSM]] | Taiwan Semiconductor | Technology | 5 | `HOLD` | 6.39 | — |
| [[hubs/XP\|XP]] | XP Inc | Financials | 20 | `HOLD` | 4.47 | — |

---

## Como usar

1. **Manhã**: abre este índice → clica no ticker que queres rever → hub mostra **Hoje** (1 linha de verdict) e **Histórico** (jornal cronológico).
2. **Refresh**: cada hub tem um bloco `bash` com os 5 comandos canónicos (`ii panorama`, `ii deepdive`, `ii verdict`, `ii fv`, `fair_value_forward`).
3. **Regenerar tudo**: `python scripts/build_ticker_hubs.py` reescreve os 33 hubs. `python scripts/build_tickers_index.py` reescreve este índice.

## Hubs disponíveis (filesystem)

- [[hubs/AAPL]] · `US` · `Technology`
- [[hubs/ABBV]] · `US` · `Healthcare`
- [[hubs/ACN]] · `US` · `Technology`
- [[hubs/BBDC4]] · `BR` · `Banks`
- [[hubs/BLK]] · `US` · `Financials`
- [[hubs/BN]] · `US` · `Financials`
- [[hubs/BRK-B]] · `US` · `Holding`
- [[hubs/BTLG11]] · `BR` · `Logística`
- [[hubs/GREK]] · `US` · `ETF`
- [[hubs/GS]] · `US` · `Financials`
- [[hubs/HD]] · `US` · `Consumer Disc.`
- [[hubs/ITSA4]] · `BR` · `Holding`
- [[hubs/IVVB11]] · `BR` · `ETF-US`
- [[hubs/JNJ]] · `US` · `Healthcare`
- [[hubs/JPM]] · `US` · `Financials`
- [[hubs/KLBN11]] · `BR` · `Materials`
- [[hubs/KNHF11]] · `BR` · `Híbrido`
- [[hubs/KO]] · `US` · `Consumer Staples`
- [[hubs/LFTB11]] · `BR` · `ETF-RF`
- [[hubs/NU]] · `US` · `Financials`
- [[hubs/O]] · `US` · `REIT`
- [[hubs/PG]] · `US` · `Consumer Staples`
- [[hubs/PLD]] · `US` · `REIT`
- [[hubs/PLTR]] · `US` · `Technology`
- [[hubs/PRIO3]] · `BR` · `Oil & Gas`
- [[hubs/PVBI11]] · `BR` · `Corporativo`
- [[hubs/TEN]] · `US` · `Energy`
- [[hubs/TSLA]] · `US` · `Consumer Disc.`
- [[hubs/TSM]] · `US` · `Technology`
- [[hubs/VALE3]] · `BR` · `Mining`
- [[hubs/VGIR11]] · `BR` · `Papel (CRI)`
- [[hubs/XP]] · `US` · `Financials`
- [[hubs/XPML11]] · `BR` · `Shopping`

---

_Gerado por `scripts/build_tickers_index.py`._
