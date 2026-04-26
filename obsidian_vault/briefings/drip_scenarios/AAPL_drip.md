
/============================================================================\
|   DRIP SCENARIO — AAPL            moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              5
  Entry price.........: US$      121.89
  Cost basis..........: US$      609.45
  Price now...........: US$      271.06
  Market value now....: US$    1,355.30  [+122.4% nao-realizado]
  DY t12m.............: 0.38%  (R$/US$ 1.0400/share)
  DY vs own 10y.......: P 2 [EXPENSIVE]  (actual 0.38% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=15  hist_g_5y=0.045  hist_g_raw=0.045  gordon_g=1.320  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -1.00% |  +10.18%       |
  | base         |  +18.00%  |   +0.00% |  +18.38%       |
  | optimista    |  +22.00%  |   +1.00% |  +23.38%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     25       |      >40       |        1       |
  | base         |     18       |      >40       |        1       |
  | optimista    |     16       |      >40       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      2,206 | US$      3,161 | US$      3,888 |
  |  10y  | US$      3,594 | US$      7,370 | US$     11,143 |
  |  15y  | US$      5,860 | US$     17,187 | US$     31,915 |
  --------------------------------------------------------------------------
