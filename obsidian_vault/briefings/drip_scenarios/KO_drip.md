
/============================================================================\
|   DRIP SCENARIO — KO              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:             11
  Entry price.........: US$       75.92
  Cost basis..........: US$      832.90
  Price now...........: US$       76.63
  Market value now....: US$      840.72  [+0.9% nao-realizado]
  DY t12m.............: 2.69%  (R$/US$ 2.0600/share)
  DY vs own 10y.......: P 6 [EXPENSIVE]  (actual 2.69% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=65  hist_g_5y=0.050  hist_g_raw=0.050  gordon_g=0.140  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +5.68%  |   -1.00% |   +7.37%       |
  | base         |   +9.47%  |   +0.00% |  +12.16%       |
  | optimista    |  +12.78%  |   +1.00% |  +16.47%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     20       |       24       |       10       |
  | base         |     16       |       27       |        6       |
  | optimista    |     14       |       30       |        5       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,211 | US$      1,509 | US$      1,825 |
  |  10y  | US$      1,757 | US$      2,709 | US$      3,938 |
  |  15y  | US$      2,565 | US$      4,863 | US$      8,456 |
  --------------------------------------------------------------------------
