
/============================================================================\
|   DRIP SCENARIO — PG              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:             10
  Entry price.........: US$      142.76
  Cost basis..........: US$    1,427.60
  Price now...........: US$      148.18
  Market value now....: US$    1,481.80  [+3.8% nao-realizado]
  DY t12m.............: 2.87%  (R$/US$ 4.2600/share)
  DY vs own 10y.......: P69 [fair-cheap]  (actual 2.87% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=65  hist_g_5y=0.053  hist_g_raw=0.053  gordon_g=0.115  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +5.04%  |   -1.00% |   +6.91%       |
  | base         |   +8.39%  |   +0.00% |  +11.27%       |
  | optimista    |  +11.33%  |   +1.00% |  +15.21%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     20       |       22       |       10       |
  | base         |     16       |       25       |        7       |
  | optimista    |     14       |       28       |        5       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      2,089 | US$      2,555 | US$      3,042 |
  |  10y  | US$      2,967 | US$      4,405 | US$      6,210 |
  |  15y  | US$      4,244 | US$      7,594 | US$     12,602 |
  --------------------------------------------------------------------------
