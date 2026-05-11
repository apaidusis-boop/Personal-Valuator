# Midnight Work 2026-05-09 — Data Fortification Report

_Generated: 2026-05-09T08:59:25_

## Mission recap

Fortify data quality, audit provenance, prove firmness — **no new recommendations**. Tomorrow re-test: same questions as today, do answers cite DB rows or extrapolate?

## Phase results — quick scan

- Live log: `logs\midnight_2026-05-09.log`
- Live status: `obsidian_vault\Midnight_Work_2026-05-09.md`
- Inventory snapshot: `data\midnight_inventory_2026-05-09.json`
- Provenance scorecard: `data\provenance_scorecard_2026-05-09.json`
- Dividend CAGRs: `data\dividend_cagrs_2026-05-09.json`

## Inventory snapshot (start of night)

### US

- Tickers known: **109**
- Tickers with no fundamentals at all: **1**
- Tickers with stale fundamentals (>120d): **0**
- Tickers with stale dividend history (>180d): **7**
- Fundamentals nulls per field:
  - `pe`: 4 tickers null
  - `pb`: 5 tickers null
  - `dy`: 5 tickers null
  - `roe`: 15 tickers null
  - `eps`: 1 tickers null
  - `bvps`: 1 tickers null
  - `dividend_streak_years`: 5 tickers null

### BR

- Tickers known: **81**
- Tickers with no fundamentals at all: **2**
- Tickers with stale fundamentals (>120d): **0**
- Tickers with stale dividend history (>180d): **10**
- Fundamentals nulls per field:
  - `pe`: 12 tickers null
  - `pb`: 20 tickers null
  - `dy`: 7 tickers null
  - `roe`: 23 tickers null
  - `eps`: 7 tickers null
  - `bvps`: 20 tickers null
  - `dividend_streak_years`: 4 tickers null

## Provenance scorecard (end of night)

### US

- fair_value confidence distribution: `{'cross_validated': 13, 'disputed': 1, 'single_source': 10}`
- data_confidence distribution: `no_table`
- provenance table rows: `16`
- fundamentals non-null counts:
  - `pe`: 1388
  - `pb`: 1393
  - `dy`: 1341
  - `roe`: 1319
  - `eps`: 1409
  - `bvps`: 1409
  - `dividend_streak_years`: 1411
- events total: 4599  (last 90d: 168)
- dividend streak stats: median=40y max=65y count_>=25y=1162

### BR

- fair_value confidence distribution: `{'null': 1, 'cross_validated': 11, 'disputed': 3, 'single_source': 11}`
- data_confidence distribution: `no_table`
- provenance table rows: `1`
- fundamentals non-null counts:
  - `pe`: 906
  - `pb`: 816
  - `dy`: 986
  - `roe`: 797
  - `eps`: 967
  - `bvps`: 816
  - `dividend_streak_years`: 1021
- events total: 357  (last 90d: 279)
- dividend streak stats: median=6y max=20y count_>=25y=0

## Dividend CAGRs (computed from DB, NOT extrapolated)

| Ticker | Mkt | 5y CAGR | 10y CAGR | 25y CAGR | yrs in DB |
|---|---|---:|---:|---:|---:|
| AAPL | us | +5.0% | +7.3% | — | 24 |
| ABBV | us | +6.8% | +12.5% | — | 14 |
| ABCB4 | br | +33.1% | +20.1% | — | 16 |
| ABEV3 | br | +19.2% | -4.5% | — | 19 |
| ABM | us | +13.8% | +8.2% | +5.0% | 43 |
| ABT | us | +10.4% | +9.4% | +8.2% | 44 |
| ACN | us | +6.2% | +7.7% | — | 22 |
| ADM | us | +7.2% | +6.2% | +10.1% | 44 |
| ADP | us | +11.5% | +12.2% | +13.1% | 44 |
| AFL | us | +15.7% | +11.4% | +14.3% | 43 |
| ALB | us | +1.0% | +3.4% | +8.1% | 33 |
| ALOS3 | br | — | — | — | 6 |
| ALUP11 | br | +16.0% | +3.4% | — | 13 |
| AOS | us | +7.1% | +13.8% | +11.9% | 41 |
| APD | us | +5.9% | +9.1% | +9.8% | 44 |
| ATO | us | +9.0% | +8.6% | +4.7% | 38 |
| AWR | us | +8.7% | +8.3% | +6.2% | 40 |
| B3SA3 | br | -15.4% | +0.4% | — | 19 |
| BBAS3 | br | +9.9% | +1.4% | — | 19 |
| BBDC4 | br | +24.7% | +10.2% | — | 19 |
| BBSE3 | br | +0.6% | +9.8% | — | 14 |
| BDX | us | +6.0% | +5.7% | +10.2% | 45 |
| BEN | us | +3.4% | +7.4% | +11.7% | 42 |
| BF-B | us | +5.4% | +5.9% | +8.0% | 42 |
| BKH | us | +4.5% | +5.3% | +3.7% | 40 |
| BLK | us | +7.5% | +9.1% | — | 24 |
| BN | us | -1.4% | +3.7% | +5.8% | 40 |
| BPAC11 | br | +35.8% | — | — | 9 |
| BRBI11 | br | — | — | — | 4 |
| BRCO11 | br | — | — | — | 5 |
| BRKM5 | br | +6.2% | +10.9% | — | 14 |
| BRO | us | +12.1% | +10.5% | +12.3% | 40 |
| BTLG11 | br | — | — | — | 6 |
| CAT | us | +7.2% | +7.1% | +9.1% | 53 |
| CB | us | -9.5% | -3.4% | +5.4% | 34 |
| CBSH | us | +4.1% | +5.1% | +6.1% | 40 |
| CHD | us | +4.2% | +5.8% | +13.8% | 37 |
| CHRW | us | +4.1% | +4.7% | +14.5% | 30 |
| CINF | us | +7.7% | +4.2% | +6.7% | 41 |
| CL | us | +3.3% | +3.2% | +7.8% | 54 |
| CLX | us | +2.5% | +5.0% | +7.4% | 45 |
| CMIG4 | br | +56.7% | +22.2% | — | 17 |
| CPLE3 | br | +8.3% | +6.0% | — | 20 |
| CSMG3 | br | -3.9% | +54.7% | — | 17 |
| CTAS | us | +13.9% | +20.4% | +15.4% | 40 |
| CVX | us | +5.8% | +4.8% | +6.9% | 58 |
| CWT | us | +7.8% | +6.3% | +3.3% | 40 |
| DOV | us | +1.0% | +4.6% | +7.7% | 45 |
| ECL | us | +7.2% | +7.2% | +10.0% | 41 |
| ED | us | +2.1% | +2.7% | +1.8% | 65 |
| EGIE3 | br | +1.8% | +6.8% | — | 20 |
| EMR | us | +1.3% | +1.3% | +4.4% | 55 |
| ENGI11 | br | +43.1% | +20.1% | — | 16 |
| EQTL3 | br | +49.5% | +30.6% | — | 18 |
| ERIE | us | -1.4% | +4.7% | +9.7% | 31 |
| ES | us | +5.8% | +6.1% | +8.4% | 43 |
| EXPD | us | +8.2% | +7.9% | +16.3% | 33 |
| EZTC3 | br | +39.5% | +6.7% | — | 18 |
| FAST | us | +4.6% | +12.1% | +26.4% | 36 |
| FDS | us | +7.5% | +9.8% | +17.9% | 28 |
| FRT | us | +1.0% | +2.0% | +3.6% | 40 |
| FUL | us | +7.4% | +6.2% | +6.2% | 40 |
| GARE11 | br | — | — | — | 3 |
| GD | us | +6.5% | +8.2% | +10.3% | 55 |
| GPC | us | +5.5% | +5.3% | +5.4% | 44 |
| GRC | us | +4.8% | +6.3% | +5.3% | 40 |
| GREK | us | +27.9% | +20.2% | — | 15 |
| GRND3 | br | +59.0% | +19.4% | — | 19 |
| GS | us | +22.9% | +18.6% | +14.4% | 28 |
| GWW | us | +8.2% | +6.8% | +10.9% | 42 |
| HD | us | +8.9% | +14.6% | +17.6% | 40 |
| HGLG11 | br | — | — | — | 6 |
| HGRU11 | br | — | — | — | 5 |
| HRL | us | +4.5% | +8.8% | +10.9% | 40 |
| IBM | us | +1.5% | +3.5% | +11.1% | 65 |
| ISAE4 | br | +9.9% | +2.1% | — | 25 |
| ITSA4 | br | +28.5% | +20.0% | — | 20 |
| ITUB4 | br | +31.1% | +18.7% | — | 19 |
| ITW | us | +7.1% | +11.6% | +11.8% | 40 |
| JKHY | us | +6.2% | +8.8% | +13.4% | 36 |
| JNJ | us | +5.2% | +5.7% | +8.8% | 65 |
| JPM | us | +9.0% | +12.7% | +6.2% | 43 |
| KLBN11 | br | +143.5% | +13.6% | — | 12 |
| KLBN4 | br | +143.5% | +16.3% | — | 16 |
| KMB | us | +3.3% | +3.6% | +6.5% | 42 |
| KNCR11 | br | — | — | — | 6 |
| KNHF11 | br | — | — | — | 4 |
| KNRI11 | br | — | — | — | 6 |
| KO | us | +4.5% | +4.5% | +7.4% | 65 |
| LEG | us | -34.0% | -16.8% | -2.9% | 40 |
| LIN | us | +9.3% | +7.7% | +12.6% | 35 |
| LOW | us | +15.9% | +16.5% | +21.6% | 42 |
| MCCI11 | br | — | — | — | 5 |
| MCD | us | +7.3% | +7.6% | +15.1% | 52 |
| MCRE11 | br | — | — | — | 6 |
| MDT | us | +4.4% | +7.0% | +11.6% | 45 |
| MGEE | us | +5.0% | +4.8% | +3.0% | 40 |
| MKC | us | +7.6% | +8.4% | +9.4% | 41 |
| MO | us | +4.1% | +6.7% | +2.9% | 65 |
| MSA | us | +4.2% | +5.2% | +11.7% | 37 |
| MSEX | us | +5.8% | +5.9% | +3.3% | 40 |
| MSFT | us | +10.2% | +10.2% | — | 24 |
| MULT3 | br | +18.8% | +12.7% | — | 18 |
| NDSN | us | +20.9% | +15.8% | +11.4% | 41 |
| NEE | us | +10.1% | +11.4% | +8.9% | 45 |
| NFG | us | +3.7% | +3.0% | +3.2% | 40 |
| NUE | us | +6.5% | +4.0% | +11.4% | 44 |
| NWN | us | +0.5% | +0.5% | +1.8% | 37 |
| O | us | +5.1% | +4.7% | +4.9% | 33 |
| PEP | us | +6.9% | +7.4% | +9.7% | 55 |
| PETR4 | br | +489.5% | — | — | 19 |
| PG | us | +6.0% | +4.7% | +7.6% | 65 |
| PGMN3 | br | — | — | — | 3 |
| PH | us | +14.8% | +10.8% | +11.6% | 42 |
| PLD | us | +11.7% | +10.3% | +4.1% | 30 |
| PLPL3 | br | — | — | — | 5 |
| PMLL11 | br | — | — | — | 5 |
| PNR | us | +5.6% | +1.5% | +6.3% | 37 |
| PNVL3 | br | +53.8% | +5.1% | — | 19 |
| POMO3 | br | +74.7% | +51.1% | — | 19 |
| POMO4 | br | +74.7% | +41.1% | — | 18 |
| PPG | us | +5.8% | +7.0% | +5.1% | 44 |
| PSSA3 | br | +14.0% | +13.2% | — | 18 |
| PVBI11 | br | +33.3% | — | — | 7 |
| RAPT4 | br | -28.0% | +1.8% | — | 15 |
| RBRX11 | br | — | — | — | 5 |
| RBRY11 | br | — | — | — | 5 |
| RDOR3 | br | — | — | — | 6 |
| RECR11 | br | — | — | — | 5 |
| RENT3 | br | +42.0% | +25.8% | — | 20 |
| RLI | us | +21.9% | +6.7% | +15.4% | 40 |
| ROP | us | +10.0% | +12.7% | +13.5% | 35 |
| RPM | us | +7.2% | +7.0% | +5.9% | 40 |
| SANB11 | br | -7.7% | +6.2% | — | 17 |
| SAPR11 | br | +16.5% | — | — | 9 |
| SCL | us | +6.5% | +7.8% | +6.4% | 40 |
| SEER3 | br | -5.6% | +13.2% | — | 10 |
| SHW | us | +12.1% | +13.5% | +12.1% | 42 |
| SIMH3 | br | — | — | — | 4 |
| SJM | us | +4.1% | +5.2% | +14.1% | 27 |
| SLCE3 | br | +42.8% | +38.0% | — | 16 |
| SPGI | us | +7.5% | +11.3% | +8.8% | 42 |
| SUZB3 | br | — | +17.0% | — | 15 |
| SWK | us | +3.5% | +4.4% | +5.3% | 42 |
| SYY | us | +3.1% | +8.8% | +9.1% | 40 |
| TAEE11 | br | +0.1% | +5.1% | — | 19 |
| TDS | us | -25.1% | -11.8% | -1.5% | 40 |
| TEN | us | +3.7% | -6.7% | — | 24 |
| TFC | us | +2.9% | +7.1% | +3.6% | 40 |
| TGT | us | +11.0% | +7.7% | +13.1% | 44 |
| TIMS3 | br | +35.5% | +32.4% | — | 17 |
| TNC | us | +6.1% | +4.1% | +4.6% | 40 |
| TR | us | +2.8% | +2.6% | +3.5% | 41 |
| TROW | us | +7.1% | +2.2% | +12.5% | 41 |
| TRXF11 | br | — | — | — | 5 |
| TSM | us | +12.8% | +15.7% | — | 23 |
| TTEN3 | br | — | — | — | 5 |
| TUPY3 | br | — | +6.5% | — | 17 |
| UNIP6 | br | +65.4% | +54.5% | — | 14 |
| UVV | us | +1.3% | +4.6% | +3.9% | 41 |
| V | us | +14.9% | +17.2% | — | 19 |
| VALE3 | br | +25.9% | +22.8% | — | 18 |
| VAMO3 | br | — | — | — | 5 |
| VGIP11 | br | — | — | — | 5 |
| VGIR11 | br | — | — | — | 5 |
| VISC11 | br | — | — | — | 6 |
| VIVA3 | br | +66.6% | — | — | 7 |
| VIVT3 | br | -4.8% | +2.0% | — | 18 |
| VRTA11 | br | — | — | — | 6 |
| WIZC3 | br | -3.3% | +9.4% | — | 12 |
| WMT | us | +5.5% | +3.7% | +10.4% | 53 |
| WST | us | +5.5% | +6.6% | +6.6% | 40 |
| XOM | us | +2.8% | +3.3% | +6.2% | 65 |
| XP | us | — | — | — | 3 |
| XPLG11 | br | — | — | — | 5 |
| XPML11 | br | — | — | — | 5 |

## How to consume tomorrow

1. Read THIS file (`Bibliotheca/Midnight_Work_2026-05-09.md`) — executive summary
2. Read live status (`Midnight_Work_2026-05-09.md`) — chronological progress for any failures
3. Re-ask yesterday's questions (PG/JNJ/KO bands; JPM deep dive; "onde investir $1.5k"). Each numerical claim should now cite a DB source or be flagged `extrapolation:true`.
4. Compare CAGR table above with my earlier extrapolations: "PG 5–7%/yr", "JPM ~10%/yr". Real numbers are above.
5. Items NOT closed tonight (engineering follow-ups for design conversation tomorrow):
   - CET1/Tier 1/leverage parser for US banks
   - Brand/intangible premium estimator for staples
   - Litigation overhang flags (10-K Item 3 parsing)
   - Fair-value intermediate "add zones" engine
   - REIT-aware dividend safety calibration audit (O still WATCH 60)
