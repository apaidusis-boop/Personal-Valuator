
/============================================================================\
|   DRIP SCENARIO — JNJ             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:             10
  Entry price.........: US$      238.28
  Cost basis..........: US$    2,382.80
  Price now...........: US$      227.50
  Market value now....: US$    2,275.00  [-4.5% nao-realizado]
  DY t12m.............: 2.29%  (R$/US$ 5.2000/share)
  DY vs own 10y.......: P 2 [EXPENSIVE]  (actual 2.29% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=65  hist_g_5y=0.052  hist_g_raw=0.052  gordon_g=0.105  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +4.72%  |   -1.00% |   +6.00%       |
  | base         |   +7.86%  |   +0.00% |  +10.15%       |
  | optimista    |  +10.61%  |   +1.00% |  +13.90%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     25       |       27       |       13       |
  | base         |     20       |       31       |        8       |
  | optimista    |     17       |       37       |        6       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      3,067 | US$      3,719 | US$      4,399 |
  |  10y  | US$      4,158 | US$      6,078 | US$      8,464 |
  |  15y  | US$      5,671 | US$      9,935 | US$     16,213 |
  --------------------------------------------------------------------------
