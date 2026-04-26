
/============================================================================\
|   DRIP SCENARIO — XPML11          moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:            159
  Entry price.........: R$      108.73
  Cost basis..........: R$   17,288.07
  Price now...........: R$      111.00
  Market value now....: R$   17,649.00  [+2.1% nao-realizado]
  DY t12m.............: 9.94%  (R$/US$ 11.0386/share)
  DY vs own 10y.......: P62 [fair-cheap]  (actual 9.94% em 50 obs mensais) — entry-timing, NAO stock-picker

  kind=fii  streak=5  hist_g=-0.282  ipca_anchor=0.035

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +0.00%  |   -1.00% |   +8.94%       |
  | base         |   +0.00%  |   +0.00% |   +9.94%       |
  | optimista    |   +0.00%  |   +1.00% |  +10.94%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     10       |        8       |        8       |
  | base         |     10       |        8       |        8       |
  | optimista    |     10       |        8       |        7       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     27,339 | R$     28,352 | R$     29,406 |
  |  10y  | R$     43,375 | R$     45,547 | R$     47,956 |
  |  15y  | R$     70,558 | R$     73,170 | R$     76,625 |
  --------------------------------------------------------------------------
