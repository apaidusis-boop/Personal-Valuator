
/============================================================================\
|   DRIP SCENARIO — TSM             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              5
  Entry price.........: US$      102.47
  Cost basis..........: US$      512.35
  Price now...........: US$      402.46
  Market value now....: US$    2,012.30  [+292.8% nao-realizado]
  DY t12m.............: 0.84%  (R$/US$ 3.3930/share)
  DY vs own 10y.......: P 1 [EXPENSIVE]  (actual 0.84% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=23  hist_g_5y=0.133  hist_g_raw=0.133  gordon_g=0.257  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -1.00% |  +10.64%       |
  | base         |  +18.00%  |   +0.00% |  +18.84%       |
  | optimista    |  +22.00%  |   +1.00% |  +23.84%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     14       |      >40       |        1       |
  | base         |     11       |      >40       |        1       |
  | optimista    |     10       |      >40       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      3,353 | US$      4,801 | US$      5,902 |
  |  10y  | US$      5,598 | US$     11,454 | US$     17,283 |
  |  15y  | US$      9,366 | US$     27,328 | US$     50,530 |
  --------------------------------------------------------------------------
