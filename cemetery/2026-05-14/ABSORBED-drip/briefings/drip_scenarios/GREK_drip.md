
/============================================================================\
|   DRIP SCENARIO — GREK            moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              5
  Entry price.........: US$       50.30
  Cost basis..........: US$      251.50
  Price now...........: US$       70.20
  Market value now....: US$      351.00  [+39.6% nao-realizado]
  DY t12m.............: 3.25%  (R$/US$ 2.2840/share)
  DY vs own 10y.......: P81 [CHEAP]  (actual 3.25% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=15  hist_g_5y=0.281  hist_g_raw=0.281  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -1.00% |  +13.05%       |
  | base         |  +18.00%  |   +0.00% |  +21.25%       |
  | optimista    |  +22.00%  |   +1.00% |  +26.25%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     12       |       20       |        3       |
  | base         |      9       |       22       |        2       |
  | optimista    |      9       |       24       |        2       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$        660 | US$        942 | US$      1,155 |
  |  10y  | US$      1,251 | US$      2,530 | US$      3,779 |
  |  15y  | US$      2,391 | US$      6,794 | US$     12,291 |
  --------------------------------------------------------------------------
