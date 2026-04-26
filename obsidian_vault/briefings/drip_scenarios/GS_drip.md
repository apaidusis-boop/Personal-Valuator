
/============================================================================\
|   DRIP SCENARIO — GS              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              1
  Entry price.........: US$      318.83
  Cost basis..........: US$      318.83
  Price now...........: US$      926.91
  Market value now....: US$      926.91  [+190.7% nao-realizado]
  DY t12m.............: 1.67%  (R$/US$ 15.5000/share)
  DY vs own 10y.......: P46 [fair-rich]  (actual 1.67% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=28  hist_g_5y=0.209  hist_g_raw=0.211  gordon_g=0.105  is_quality=True  capped=True

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +9.42%  |   -1.00% |  +10.09%       |
  | base         |  +15.69%  |   +0.00% |  +17.37%       |
  | optimista    |  +21.19%  |   +1.00% |  +23.86%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     12       |       36       |        1       |
  | base         |     10       |      >40       |        1       |
  | optimista    |      8       |      >40       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,512 | US$      2,087 | US$      2,737 |
  |  10y  | US$      2,476 | US$      4,701 | US$      8,057 |
  |  15y  | US$      4,071 | US$     10,586 | US$     23,641 |
  --------------------------------------------------------------------------
