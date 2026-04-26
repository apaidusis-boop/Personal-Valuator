
/============================================================================\
|   DRIP SCENARIO — ACN             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              4
  Entry price.........: US$      213.71
  Cost basis..........: US$      920.03
  Price now...........: US$      178.36
  Market value now....: US$      767.85  [-16.5% nao-realizado]
  DY t12m.............: 1.74%  (R$/US$ 3.1100/share)
  DY vs own 10y.......: P71 [fair-cheap]  (actual 1.74% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=22  hist_g_5y=0.053  hist_g_raw=0.053  gordon_g=0.185  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +7.13%  |   -1.00% |   +7.87%       |
  | base         |  +11.88%  |   +0.00% |  +13.62%       |
  | optimista    |  +16.04%  |   +1.00% |  +18.78%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     25       |       34       |       12       |
  | base         |     19       |      >40       |        7       |
  | optimista    |     16       |      >40       |        6       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,130 | US$      1,468 | US$      1,834 |
  |  10y  | US$      1,670 | US$      2,805 | US$      4,367 |
  |  15y  | US$      2,478 | US$      5,360 | US$     10,362 |
  --------------------------------------------------------------------------
