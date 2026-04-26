
/============================================================================\
|   DRIP SCENARIO — ABBV            moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              7
  Entry price.........: US$      200.91
  Cost basis..........: US$    1,500.00
  Price now...........: US$      198.71
  Market value now....: US$    1,483.57  [-1.1% nao-realizado]
  DY t12m.............: 3.39%  (R$/US$ 6.7400/share)
  DY vs own 10y.......: P26 [fair-rich]  (actual 3.39% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=14  hist_g_5y=0.060  hist_g_raw=0.060  gordon_g=0.000  is_quality=False  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +1.79%  |   -2.00% |   +3.19%       |
  | base         |   +2.99%  |   +0.00% |   +6.38%       |
  | optimista    |   +4.04%  |   +1.00% |   +8.43%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     24       |       18       |       19       |
  | base         |     22       |       21       |       12       |
  | optimista    |     20       |       24       |        9       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,753 | US$      2,031 | US$      2,231 |
  |  10y  | US$      2,108 | US$      2,781 | US$      3,329 |
  |  15y  | US$      2,587 | US$      3,807 | US$      4,933 |
  --------------------------------------------------------------------------
