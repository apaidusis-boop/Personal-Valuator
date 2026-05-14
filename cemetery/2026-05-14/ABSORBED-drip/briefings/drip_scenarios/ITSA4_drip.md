
/============================================================================\
|   DRIP SCENARIO — ITSA4           moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:          2.472
  Entry price.........: R$        7.75
  Cost basis..........: R$   19,158.00
  Price now...........: R$       14.22
  Market value now....: R$   35,151.84  [+83.5% nao-realizado]
  DY t12m.............: 8.63%  (R$/US$ 1.2276/share)
  DY vs own 10y.......: P79 [CHEAP]  (actual 8.63% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=20  hist_g_5y=0.120  hist_g_raw=0.547  gordon_g=0.030  is_quality=True  capped=True

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +4.50%  |   -1.00% |  +12.13%       |
  | base         |   +7.50%  |   +0.00% |  +16.13%       |
  | optimista    |  +10.12%  |   +1.00% |  +19.76%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |      6       |        9       |        1       |
  | base         |      6       |        9       |        1       |
  | optimista    |      5       |        9       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     63,900 | R$     76,342 | R$     89,158 |
  |  10y  | R$    118,511 | R$    165,798 | R$    222,289 |
  |  15y  | R$    224,452 | R$    360,077 | R$    545,169 |
  --------------------------------------------------------------------------
