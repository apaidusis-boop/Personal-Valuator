
/============================================================================\
|   DRIP SCENARIO — BN              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              7
  Entry price.........: US$       25.56
  Cost basis..........: US$      178.93
  Price now...........: US$       45.48
  Market value now....: US$      318.36  [+77.9% nao-realizado]
  DY t12m.............: 0.55%  (R$/US$ 0.2500/share)
  DY vs own 10y.......: P11 [EXPENSIVE]  (actual 0.55% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=40  hist_g_5y=-0.037  hist_g_raw=-0.037  gordon_g=0.010  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   -0.83%  |   -1.00% |   -1.28%       |
  | base         |   -1.38%  |   +0.00% |   -0.83%       |
  | optimista    |   -1.86%  |   +1.00% |   -0.31%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |    >40       |      >40       |      >40       |
  | base         |    >40       |      >40       |      >40       |
  | optimista    |    >40       |      >40       |      >40       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$        299 | US$        305 | US$        313 |
  |  10y  | US$        281 | US$        293 | US$        307 |
  |  15y  | US$        264 | US$        281 | US$        302 |
  --------------------------------------------------------------------------
