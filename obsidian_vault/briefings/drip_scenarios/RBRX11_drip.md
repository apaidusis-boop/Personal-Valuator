
/============================================================================\
|   DRIP SCENARIO — RBRX11          moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:          2.000
  Entry price.........: R$        8.48
  Cost basis..........: R$   16,960.00
  Price now...........: R$        8.82
  Market value now....: R$   17,640.00  [+4.0% nao-realizado]
  DY t12m.............: 12.31%  (R$/US$ 1.0862/share)
  DY vs own 10y.......: P18 [EXPENSIVE]  (actual 12.31% em 44 obs mensais) — entry-timing, NAO stock-picker

  kind=fii  streak=5  hist_g=-0.339  ipca_anchor=0.035

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +0.00%  |   -1.00% |  +11.31%       |
  | base         |   +0.00%  |   +0.00% |  +12.31%       |
  | optimista    |   +0.00%  |   +1.00% |  +13.31%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |      8       |        6       |        6       |
  | base         |      8       |        6       |        6       |
  | optimista    |      8       |        7       |        6       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     30,490 | R$     31,527 | R$     32,606 |
  |  10y  | R$     54,248 | R$     56,347 | R$     58,724 |
  |  15y  | R$     99,483 | R$    100,706 | R$    103,168 |
  --------------------------------------------------------------------------
