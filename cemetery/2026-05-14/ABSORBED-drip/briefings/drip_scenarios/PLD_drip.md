
/============================================================================\
|   DRIP SCENARIO — PLD             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              2
  Entry price.........: US$      109.22
  Cost basis..........: US$      218.44
  Price now...........: US$      142.10
  Market value now....: US$      284.20  [+30.1% nao-realizado]
  DY t12m.............: 2.89%  (R$/US$ 4.1000/share)
  DY vs own 10y.......: P63 [fair-cheap]  (actual 2.89% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=30  hist_g_5y=0.125  hist_g_raw=0.125  gordon_g=0.000  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +3.76%  |   -1.00% |   +5.64%       |
  | base         |   +6.26%  |   +0.00% |   +9.15%       |
  | optimista    |   +8.45%  |   +1.00% |  +12.34%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     19       |       22       |        8       |
  | base         |     16       |       25       |        5       |
  | optimista    |     14       |       28       |        4       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$        377 | US$        444 | US$        513 |
  |  10y  | US$        503 | US$        693 | US$        919 |
  |  15y  | US$        678 | US$      1,083 | US$      1,639 |
  --------------------------------------------------------------------------
