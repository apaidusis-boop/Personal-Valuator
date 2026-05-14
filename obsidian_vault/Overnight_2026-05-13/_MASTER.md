# Pilot Deep Dive — Master Report (2026-05-12)

**Phase MCP-5 validation** — does our new Playwright + markitdown pipeline add real value over yesterday's CVM/SEC monitors?

Pilot: **67 tickers** chosen for diversity (BR/US, sector, RI provider).

## Sumário executivo

- Scrapes bem-sucedidos: **0/67**
- Scrapes falhados: ['ABCB4', 'ABEV3', 'ALOS3', 'ALUP11', 'AXIA7', 'B3SA3', 'BBAS3', 'BBSE3', 'BPAC11', 'BRBI11', 'BRCO11', 'BRKM5', 'CMIG4', 'CPLE3', 'CSMG3', 'EGIE3', 'ENGI11', 'EQTL3', 'EZTC3', 'GARE11', 'GMAT3', 'GRND3', 'HGLG11', 'HGRU11', 'ISAE4', 'ITUB4', 'KLBN4', 'KNCR11', 'KNHF11', 'KNRI11', 'MCCI11', 'MCRE11', 'MOTV3', 'MULT3', 'PETR4', 'PGMN3', 'PLPL3', 'PMLL11', 'PNVL3', 'POMO3', 'POMO4', 'PSSA3', 'RAPT4', 'RBRY11', 'RDOR3', 'RECR11', 'RENT3', 'SANB11', 'SAPR11', 'SEER3', 'SIMH3', 'SLCE3', 'SUZB3', 'TAEE11', 'TIMS3', 'TRXF11', 'TTEN3', 'TUPY3', 'UNIP6', 'VAMO3', 'VGIP11', 'VISC11', 'VIVA3', 'VIVT3', 'VRTA11', 'WIZC3', 'XPLG11']
- **Filings novos descobertos** (vs DB): **0**
- **Eventos de calendário descobertos** (não tínhamos): **0**
- **Apresentações/releases acessíveis**: **0**
- **Audio/video accessível** (era cego): **0**
- Tempo médio scrape Playwright: **1.2s/ticker**
- Estimativa scaling 200 tickers: **~4min** (~0.1h)

## Tabela comparativa global

| Ticker | Mkt | Sector | Scrape | Time | DB events | RI filings | Novel | Events | Pres. | A/V |
|---|---|---|---|---|---|---|---|---|---|---|
| ABCB4 | BR | Banks | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| ABEV3 | BR | Consumer Stapl | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| ALOS3 | BR | Real Estate | ❌ | 0.5s | 11 | 0 | 0 | 0 | 0 | 0 |
| ALUP11 | BR | Utilities | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| AXIA7 | BR | Utilities | ❌ | 1.0s | 33 | 0 | 0 | 0 | 0 | 0 |
| B3SA3 | BR | Financials | ❌ | 0.5s | 13 | 0 | 0 | 0 | 0 | 0 |
| BBAS3 | BR | Banks | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| BBSE3 | BR | Insurance | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| BPAC11 | BR | Banks | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| BRBI11 | BR | Financials | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| BRCO11 | BR | Logística | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| BRKM5 | BR | Materials | ❌ | 12.6s | 0 | 0 | 0 | 0 | 0 | 0 |
| CMIG4 | BR | Utilities | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| CPLE3 | BR | Utilities | ❌ | 0.5s | 13 | 0 | 0 | 0 | 0 | 0 |
| CSMG3 | BR | Utilities | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| EGIE3 | BR | Utilities | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| ENGI11 | BR | Utilities | ❌ | 0.5s | 21 | 0 | 0 | 0 | 0 | 0 |
| EQTL3 | BR | Utilities | ❌ | 0.5s | 24 | 0 | 0 | 0 | 0 | 0 |
| EZTC3 | BR | Real Estate | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| GARE11 | BR | Híbrido | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| GMAT3 | BR | Consumer Stapl | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| GRND3 | BR | Consumer Disc. | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| HGLG11 | BR | Logística | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| HGRU11 | BR | Híbrido | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| ISAE4 | BR | Utilities | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| ITUB4 | BR | Banks | ❌ | 0.5s | 7 | 0 | 0 | 0 | 0 | 0 |
| KLBN4 | BR | Materials | ❌ | 0.6s | 0 | 0 | 0 | 0 | 0 | 0 |
| KNCR11 | BR | Papel (CRI) | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| KNHF11 | BR | Híbrido | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| KNRI11 | BR | Híbrido | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| MCCI11 | BR | Papel (CRI) | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| MCRE11 | BR | Tijolo | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| MOTV3 | BR | Industrials | ❌ | 0.5s | 15 | 0 | 0 | 0 | 0 | 0 |
| MULT3 | BR | Real Estate | ❌ | 0.5s | 13 | 0 | 0 | 0 | 0 | 0 |
| PETR4 | BR | Oil & Gas | ❌ | 13.1s | 49 | 0 | 0 | 0 | 0 | 0 |
| PGMN3 | BR | Consumer Stapl | ❌ | 0.5s | 9 | 0 | 0 | 0 | 0 | 0 |
| PLPL3 | BR | Consumer Disc. | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| PMLL11 | BR | Shopping | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| PNVL3 | BR | Consumer Stapl | ❌ | 1.0s | 0 | 0 | 0 | 0 | 0 | 0 |
| POMO3 | BR | Industrials | ❌ | 1.5s | 7 | 0 | 0 | 0 | 0 | 0 |
| POMO4 | BR | Industrials | ❌ | 1.0s | 7 | 0 | 0 | 0 | 0 | 0 |
| PSSA3 | BR | Insurance | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| RAPT4 | BR | Industrials | ❌ | 0.5s | 7 | 0 | 0 | 0 | 0 | 0 |
| RBRY11 | BR | Papel (CRI) | ❌ | 1.0s | 0 | 0 | 0 | 0 | 0 | 0 |
| RDOR3 | BR | Healthcare | ❌ | 0.5s | 5 | 0 | 0 | 0 | 0 | 0 |
| RECR11 | BR | Papel (CRI) | ❌ | 1.0s | 0 | 0 | 0 | 0 | 0 | 0 |
| RENT3 | BR | Industrials | ❌ | 3.2s | 14 | 0 | 0 | 0 | 0 | 0 |
| SANB11 | BR | Banks | ❌ | 1.0s | 0 | 0 | 0 | 0 | 0 | 0 |
| SAPR11 | BR | Utilities | ❌ | 0.6s | 0 | 0 | 0 | 0 | 0 | 0 |
| SEER3 | BR | Consumer Disc. | ❌ | 13.1s | 0 | 0 | 0 | 0 | 0 | 0 |
| SIMH3 | BR | Industrials | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| SLCE3 | BR | Consumer Stapl | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| SUZB3 | BR | Materials | ❌ | 0.5s | 11 | 0 | 0 | 0 | 0 | 0 |
| TAEE11 | BR | Utilities | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| TIMS3 | BR | Telecom | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| TRXF11 | BR | Híbrido | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| TTEN3 | BR | Consumer Stapl | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| TUPY3 | BR | Industrials | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| UNIP6 | BR | Materials | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| VAMO3 | BR | Industrials | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| VGIP11 | BR | Papel (CRI) | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| VISC11 | BR | Shopping | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| VIVA3 | BR | Consumer Disc. | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| VIVT3 | BR | Telecom | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| VRTA11 | BR | Papel (CRI) | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |
| WIZC3 | BR | Insurance | ❌ | 1.0s | 0 | 0 | 0 | 0 | 0 | 0 |
| XPLG11 | BR | Logística | ❌ | 0.5s | 0 | 0 | 0 | 0 | 0 | 0 |

## Dossiers individuais

- ❌ [[ABCB4]] — known (watchlist)
- ❌ [[ABEV3]] — known (watchlist)
- ❌ [[ALOS3]] — heuristic (watchlist)
- ❌ [[ALUP11]] — heuristic (watchlist)
- ❌ [[AXIA7]] — known (watchlist)
- ❌ [[B3SA3]] — known (watchlist)
- ❌ [[BBAS3]] — known (watchlist)
- ❌ [[BBSE3]] — known (watchlist)
- ❌ [[BPAC11]] — known (watchlist)
- ❌ [[BRBI11]] — heuristic (watchlist)
- ❌ [[BRCO11]] — fii_heuristic (watchlist)
- ❌ [[BRKM5]] — known (watchlist)
- ❌ [[CMIG4]] — known (watchlist)
- ❌ [[CPLE3]] — known (watchlist)
- ❌ [[CSMG3]] — known (watchlist)
- ❌ [[EGIE3]] — known (watchlist)
- ❌ [[ENGI11]] — heuristic (watchlist)
- ❌ [[EQTL3]] — known (watchlist)
- ❌ [[EZTC3]] — known (watchlist)
- ❌ [[GARE11]] — fii_heuristic (watchlist)
- ❌ [[GMAT3]] — known (watchlist)
- ❌ [[GRND3]] — known (watchlist)
- ❌ [[HGLG11]] — fii_heuristic (watchlist)
- ❌ [[HGRU11]] — fii_heuristic (watchlist)
- ❌ [[ISAE4]] — tavily (watchlist)
- ❌ [[ITUB4]] — known (watchlist)
- ❌ [[KLBN4]] — known (watchlist)
- ❌ [[KNCR11]] — fii_heuristic (watchlist)
- ❌ [[KNHF11]] — fii_heuristic (watchlist)
- ❌ [[KNRI11]] — fii_heuristic (watchlist)
- ❌ [[MCCI11]] — fii_heuristic (watchlist)
- ❌ [[MCRE11]] — fii_heuristic (watchlist)
- ❌ [[MOTV3]] — known (watchlist)
- ❌ [[MULT3]] — known (watchlist)
- ❌ [[PETR4]] — known (watchlist)
- ❌ [[PGMN3]] — known (watchlist)
- ❌ [[PLPL3]] — known (watchlist)
- ❌ [[PMLL11]] — fii_heuristic (watchlist)
- ❌ [[PNVL3]] — heuristic (watchlist)
- ❌ [[POMO3]] — known (watchlist)
- ❌ [[POMO4]] — known (watchlist)
- ❌ [[PSSA3]] — known (watchlist)
- ❌ [[RAPT4]] — heuristic (watchlist)
- ❌ [[RBRY11]] — fii_heuristic (watchlist)
- ❌ [[RDOR3]] — known (watchlist)
- ❌ [[RECR11]] — fii_heuristic (watchlist)
- ❌ [[RENT3]] — known (watchlist)
- ❌ [[SANB11]] — tavily (watchlist)
- ❌ [[SAPR11]] — heuristic (watchlist)
- ❌ [[SEER3]] — heuristic (watchlist)
- ❌ [[SIMH3]] — heuristic (watchlist)
- ❌ [[SLCE3]] — heuristic (watchlist)
- ❌ [[SUZB3]] — known (watchlist)
- ❌ [[TAEE11]] — known (watchlist)
- ❌ [[TIMS3]] — known (watchlist)
- ❌ [[TRXF11]] — fii_heuristic (watchlist)
- ❌ [[TTEN3]] — heuristic (watchlist)
- ❌ [[TUPY3]] — known (watchlist)
- ❌ [[UNIP6]] — known (watchlist)
- ❌ [[VAMO3]] — heuristic (watchlist)
- ❌ [[VGIP11]] — fii_heuristic (watchlist)
- ❌ [[VISC11]] — fii_heuristic (watchlist)
- ❌ [[VIVA3]] — known (watchlist)
- ❌ [[VIVT3]] — known (watchlist)
- ❌ [[VRTA11]] — fii_heuristic (watchlist)
- ❌ [[WIZC3]] — known (watchlist)
- ❌ [[XPLG11]] — fii_heuristic (watchlist)

## Todos os filings novos descobertos (cross-ticker)

_(zero filings novos cross-ticker)_

## Próximos eventos cross-ticker (30 dias)

_(zero eventos calendário cross-ticker nos próximos 30d)_

## Validação técnica & escalabilidade

**Por ticker (tempo + estado)**:

| Ticker | Time | Status |
|---|---|---|
| ABCB4 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| ABEV3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| ALOS3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| ALUP11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| AXIA7 | 1.0s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| B3SA3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| BBAS3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| BBSE3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| BPAC11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| BRBI11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| BRCO11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| BRKM5 | 12.6s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| CMIG4 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| CPLE3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| CSMG3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| EGIE3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| ENGI11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| EQTL3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| EZTC3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| GARE11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| GMAT3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| GRND3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| HGLG11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| HGRU11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| ISAE4 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| ITUB4 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| KLBN4 | 0.6s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| KNCR11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| KNHF11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| KNRI11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| MCCI11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| MCRE11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| MOTV3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| MULT3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| PETR4 | 13.1s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| PGMN3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| PLPL3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| PMLL11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| PNVL3 | 1.0s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| POMO3 | 1.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| POMO4 | 1.0s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| PSSA3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| RAPT4 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| RBRY11 | 1.0s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| RDOR3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| RECR11 | 1.0s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| RENT3 | 3.2s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| SANB11 | 1.0s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| SAPR11 | 0.6s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| SEER3 | 13.1s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| SIMH3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| SLCE3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| SUZB3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| TAEE11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| TIMS3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| TRXF11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| TTEN3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| TUPY3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| UNIP6 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| VAMO3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| VGIP11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| VISC11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| VIVA3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| VIVT3 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| VRTA11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| WIZC3 | 1.0s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |
| XPLG11 | 0.5s | ERR: Traceback (most recent call last):   File "C:\Users\paidu\in |

**Estimativas de escala**:
- 33 holdings (BR+US): ~1min
- 100 watchlist Tier-A: ~2min
- 200 universo completo: ~4min

## Recomendação

❌ **Pipeline frágil (0/67 OK).** Não escalar. Re-investigar parser e RI URL resolution.

---
_Generated by `scripts/pilot_deep_dive.py` at 2026-05-12 02:03:57_
_Logs: `logs/pilot_deep_dive_2026-05-12.log`_