
/============================================================================\
|   DRIP SCENARIO — XP              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:             20
  Entry price.........: US$       17.36
  Cost basis..........: US$      347.10
  Price now...........: US$       19.74
  Market value now....: US$      394.80  [+13.7% nao-realizado]
  DY t12m.............: 0.91%  (R$/US$ 0.1800/share)
  DY vs own 10y.......: P 3 [EXPENSIVE]  (actual 0.91% em 32 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=8  hist_g_5y=-0.629  hist_g_raw=-0.629  gordon_g=0.215  is_quality=False  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -2.00% |   +9.71%       |
  | base         |  +18.00%  |   +0.00% |  +18.91%       |
  | optimista    |  +22.00%  |   +1.00% |  +23.91%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     23       |      >40       |        7       |
  | base         |     17       |      >40       |        4       |
  | optimista    |     15       |      >40       |        3       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$        631 | US$        945 | US$      1,162 |
  |  10y  | US$      1,015 | US$      2,263 | US$      3,413 |
  |  15y  | US$      1,638 | US$      5,417 | US$     10,009 |
  --------------------------------------------------------------------------
