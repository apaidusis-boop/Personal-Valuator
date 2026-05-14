
/============================================================================\
|   DRIP SCENARIO — JPM             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              7
  Entry price.........: US$      306.56
  Cost basis..........: US$    2,145.89
  Price now...........: US$      308.28
  Market value now....: US$    2,157.96  [+0.6% nao-realizado]
  DY t12m.............: 1.91%  (R$/US$ 5.9000/share)
  DY vs own 10y.......: P12 [EXPENSIVE]  (actual 1.91% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=43  hist_g_5y=0.107  hist_g_raw=0.107  gordon_g=0.118  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +6.75%  |   -1.00% |   +7.66%       |
  | base         |  +11.24%  |   +0.00% |  +13.16%       |
  | optimista    |  +15.18%  |   +1.00% |  +18.09%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     23       |       32       |       10       |
  | base         |     18       |       37       |        6       |
  | optimista    |     15       |      >40       |        5       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      3,146 | US$      4,042 | US$      5,009 |
  |  10y  | US$      4,606 | US$      7,570 | US$     11,583 |
  |  15y  | US$      6,779 | US$     14,178 | US$     26,685 |
  --------------------------------------------------------------------------
