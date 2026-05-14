
/============================================================================\
|   DRIP SCENARIO — VALE3           moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:            500
  Entry price.........: R$       61.81
  Cost basis..........: R$   30,905.00
  Price now...........: R$       85.87
  Market value now....: R$   42,935.00  [+38.9% nao-realizado]
  DY t12m.............: 6.38%  (R$/US$ 5.4772/share)
  DY vs own 10y.......: P50 [fair-rich]  (actual 6.38% em 115 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=18  hist_g_5y=0.221  hist_g_raw=0.221  gordon_g=0.000  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +6.63%  |   -1.00% |  +12.01%       |
  | base         |  +11.06%  |   +0.00% |  +17.43%       |
  | optimista    |  +14.92%  |   +1.00% |  +22.30%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |      9       |       11       |        4       |
  | base         |      8       |       12       |        3       |
  | optimista    |      7       |       12       |        2       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     77,593 | R$     98,805 | R$    121,515 |
  |  10y  | R$    142,324 | R$    227,378 | R$    339,667 |
  |  15y  | R$    265,132 | R$    523,258 | R$    938,212 |
  --------------------------------------------------------------------------
