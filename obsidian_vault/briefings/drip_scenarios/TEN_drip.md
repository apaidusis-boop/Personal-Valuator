
/============================================================================\
|   DRIP SCENARIO — TEN             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:             35
  Entry price.........: US$       23.93
  Cost basis..........: US$      837.48
  Price now...........: US$       39.27
  Market value now....: US$    1,374.45  [+64.1% nao-realizado]
  DY t12m.............: 1.53%  (R$/US$ 0.6000/share)
  DY vs own 10y.......: P17 [EXPENSIVE]  (actual 1.53% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=24  hist_g_5y=0.157  hist_g_raw=0.316  gordon_g=0.079  is_quality=True  capped=True

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +7.08%  |   -1.00% |   +7.60%       |
  | base         |  +11.79%  |   +0.00% |  +13.32%       |
  | optimista    |  +15.92%  |   +1.00% |  +18.45%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     19       |       38       |        3       |
  | base         |     15       |      >40       |        2       |
  | optimista    |     13       |      >40       |        2       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,996 | US$      2,589 | US$      3,233 |
  |  10y  | US$      2,908 | US$      4,877 | US$      7,584 |
  |  15y  | US$      4,255 | US$      9,186 | US$     17,734 |
  --------------------------------------------------------------------------
