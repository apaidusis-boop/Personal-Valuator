
/============================================================================\
|   DRIP SCENARIO — BLK             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              2
  Entry price.........: US$      897.70
  Cost basis..........: US$    1,795.39
  Price now...........: US$    1,044.97
  Market value now....: US$    2,089.94  [+16.4% nao-realizado]
  DY t12m.............: 2.04%  (R$/US$ 21.3600/share)
  DY vs own 10y.......: P28 [fair-rich]  (actual 2.04% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=24  hist_g_5y=0.060  hist_g_raw=0.060  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +3.59%  |   -1.00% |   +4.63%       |
  | base         |   +5.98%  |   +0.00% |   +8.02%       |
  | optimista    |   +8.07%  |   +1.00% |  +11.12%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     26       |       30       |       12       |
  | base         |     21       |       35       |        7       |
  | optimista    |     19       |      >40       |        6       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      2,635 | US$      3,092 | US$      3,560 |
  |  10y  | US$      3,340 | US$      4,573 | US$      6,038 |
  |  15y  | US$      4,256 | US$      6,765 | US$     10,197 |
  --------------------------------------------------------------------------
