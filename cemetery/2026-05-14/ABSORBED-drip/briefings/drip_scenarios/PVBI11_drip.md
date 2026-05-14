
/============================================================================\
|   DRIP SCENARIO — PVBI11          moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:            217
  Entry price.........: R$       79.04
  Cost basis..........: R$   17,151.68
  Price now...........: R$       79.00
  Market value now....: R$   17,143.00  [-0.1% nao-realizado]
  DY t12m.............: 5.95%  (R$/US$ 4.7000/share)
  DY vs own 10y.......: P16 [EXPENSIVE]  (actual 5.95% em 67 obs mensais) — entry-timing, NAO stock-picker

  kind=fii  streak=7  hist_g=-0.496  ipca_anchor=0.035

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +0.00%  |   -1.00% |   +4.95%       |
  | base         |   +0.00%  |   +0.00% |   +5.95%       |
  | optimista    |   +0.00%  |   +1.00% |   +6.95%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     17       |       12       |       14       |
  | base         |     17       |       12       |       13       |
  | optimista    |     17       |       13       |       11       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     21,953 | R$     22,886 | R$     23,857 |
  |  10y  | R$     28,534 | R$     30,554 | R$     32,762 |
  |  15y  | R$     37,670 | R$     40,791 | R$     44,425 |
  --------------------------------------------------------------------------
