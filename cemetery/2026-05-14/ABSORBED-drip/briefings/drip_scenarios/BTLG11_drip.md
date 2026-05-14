
/============================================================================\
|   DRIP SCENARIO — BTLG11          moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:            166
  Entry price.........: R$      103.30
  Cost basis..........: R$   17,147.80
  Price now...........: R$      103.18
  Market value now....: R$   17,127.88  [-0.1% nao-realizado]
  DY t12m.............: 9.19%  (R$/US$ 9.4801/share)
  DY vs own 10y.......: P71 [fair-cheap]  (actual 9.19% em 62 obs mensais) — entry-timing, NAO stock-picker

  kind=fii  streak=5  hist_g=-0.290  ipca_anchor=0.035

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +0.00%  |   -1.00% |   +8.19%       |
  | base         |   +0.00%  |   +0.00% |   +9.19%       |
  | optimista    |   +0.00%  |   +1.00% |  +10.19%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     11       |        8       |        9       |
  | base         |     11       |        8       |        8       |
  | optimista    |     11       |        9       |        8       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     25,607 | R$     26,581 | R$     27,594 |
  |  10y  | R$     39,144 | R$     41,252 | R$     43,580 |
  |  15y  | R$     61,248 | R$     64,021 | R$     67,530 |
  --------------------------------------------------------------------------
