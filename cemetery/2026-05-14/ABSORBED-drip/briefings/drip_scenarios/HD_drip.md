
/============================================================================\
|   DRIP SCENARIO — HD              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              1
  Entry price.........: US$      292.02
  Cost basis..........: US$      292.02
  Price now...........: US$      335.89
  Market value now....: US$      335.89  [+15.0% nao-realizado]
  DY t12m.............: 2.75%  (R$/US$ 9.2300/share)
  DY vs own 10y.......: P94 [CHEAP]  (actual 2.75% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=40  hist_g_5y=0.087  hist_g_raw=0.087  gordon_g=0.512  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -1.00% |  +12.55%       |
  | base         |  +18.00%  |   +0.00% |  +20.75%       |
  | optimista    |  +22.00%  |   +1.00% |  +25.75%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     14       |       23       |        5       |
  | base         |     11       |       26       |        3       |
  | optimista    |     10       |       29       |        3       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$        616 | US$        880 | US$      1,079 |
  |  10y  | US$      1,137 | US$      2,305 | US$      3,451 |
  |  15y  | US$      2,114 | US$      6,040 | US$     10,976 |
  --------------------------------------------------------------------------
