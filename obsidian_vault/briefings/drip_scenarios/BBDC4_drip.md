
/============================================================================\
|   DRIP SCENARIO — BBDC4           moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:          1.828
  Entry price.........: R$       16.08
  Cost basis..........: R$   29,394.24
  Price now...........: R$       19.92
  Market value now....: R$   36,413.76  [+23.9% nao-realizado]
  DY t12m.............: 7.56%  (R$/US$ 1.5057/share)
  DY vs own 10y.......: P76 [CHEAP]  (actual 7.56% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=19  hist_g_5y=0.120  hist_g_raw=0.169  gordon_g=0.040  is_quality=True  capped=True

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +4.81%  |   -1.00% |  +11.37%       |
  | base         |   +8.02%  |   +0.00% |  +15.57%       |
  | optimista    |  +10.82%  |   +1.00% |  +19.38%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |      9       |       10       |        5       |
  | base         |      8       |       10       |        4       |
  | optimista    |      7       |       10       |        3       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     63,846 | R$     77,077 | R$     90,795 |
  |  10y  | R$    113,944 | R$    163,150 | R$    223,004 |
  |  15y  | R$    207,145 | R$    345,340 | R$    539,865 |
  --------------------------------------------------------------------------
