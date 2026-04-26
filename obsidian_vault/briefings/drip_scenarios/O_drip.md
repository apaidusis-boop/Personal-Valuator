
/============================================================================\
|   DRIP SCENARIO — O               moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:             30
  Entry price.........: US$       63.56
  Cost basis..........: US$    1,906.90
  Price now...........: US$       63.33
  Market value now....: US$    1,899.90  [-0.4% nao-realizado]
  DY t12m.............: 5.11%  (R$/US$ 3.2360/share)
  DY vs own 10y.......: P77 [CHEAP]  (actual 5.11% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=33  hist_g_5y=0.059  hist_g_raw=0.059  gordon_g=0.000  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +1.77%  |   -1.00% |   +5.88%       |
  | base         |   +2.95%  |   +0.00% |   +8.06%       |
  | optimista    |   +3.98%  |   +1.00% |  +10.09%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     17       |       13       |       12       |
  | base         |     16       |       14       |        9       |
  | optimista    |     15       |       15       |        8       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      2,551 | US$      2,819 | US$      3,087 |
  |  10y  | US$      3,470 | US$      4,182 | US$      4,961 |
  |  15y  | US$      4,782 | US$      6,205 | US$      7,888 |
  --------------------------------------------------------------------------
