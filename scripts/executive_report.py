"""Relatório executivo mensal da carteira BR — estilo equity research.

Layout landscape, multi-página, desenhado para abrir no browser e
exportar para PDF via Ctrl+P (usa @page CSS e page-break-after).

Páginas:
  1. Capa — resumo da carteira (posições, rating, fair value, DY)
  2. Desempenho — tabela por ticker (retorno desde entrada, mês, YTD)
                  + indicadores (Sharpe, vol, beta) + chart vs IBOV
  3. Gráfico — curva acumulada portfolio vs Ibovespa em grande
  4. Comentários — por ticker, auto-gerado a partir dos dados
  5. Disclaimer

Nunca toca na rede *exceto* para descarregar a série do Ibovespa via
yfinance (necessária para o comparativo). Toda a outra data vem da DB.

Uso:
    python scripts/executive_report.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from fetchers.cache_policy import fmt_date_br  # noqa: E402

ROOT = _ROOT
DB_PATH = ROOT / "data" / "br_investments.db"
REPORTS = ROOT / "reports"

IBOV = "^BVSP"


# ---------- formatters ----------

def fmt_money(x, sym="R$"):
    if x is None or not isinstance(x, (int, float)):
        return "—"
    s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sym} {s}"


def fmt_pct(x, nd=1, signed=False):
    if x is None or not isinstance(x, (int, float)):
        return "—"
    fmt = f"{{:+.{nd}f}}%" if signed else f"{{:.{nd}f}}%"
    return fmt.format(x * 100)


def fmt_num(x, nd=2):
    if x is None or not isinstance(x, (int, float)):
        return "—"
    return f"{x:.{nd}f}"


# ---------- data loading ----------

def load_portfolio() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            """SELECT p.ticker, p.weight, p.entry_date, p.entry_price,
                      c.name, c.sector
               FROM portfolio_positions p
               JOIN companies c USING (ticker)
               WHERE p.active=1
               ORDER BY p.ticker""",
            conn,
        )
    return df


def load_prices_wide() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            "SELECT ticker, date, close FROM prices ORDER BY date ASC",
            conn,
        )
    return df.pivot(index="date", columns="ticker", values="close")


def load_fundamentals() -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """SELECT ticker, eps, bvps, roe, pe, pb, dy,
                      net_debt_ebitda, dividend_streak_years
               FROM fundamentals f
               WHERE period_end = (
                 SELECT MAX(period_end) FROM fundamentals WHERE ticker=f.ticker
               )"""
        ).fetchall()
    keys = ["eps", "bvps", "roe", "pe", "pb", "dy", "net_debt_ebitda", "streak"]
    return {r[0]: dict(zip(keys, r[1:])) for r in rows}


def load_scores() -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """SELECT ticker, score, passes_screen, details_json
               FROM scores s WHERE run_date = (
                 SELECT MAX(run_date) FROM scores WHERE ticker=s.ticker
               )"""
        ).fetchall()
    return {
        r[0]: {
            "score": r[1], "passes": bool(r[2]),
            "details": json.loads(r[3]) if r[3] else {},
        } for r in rows
    }


def load_valuations() -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """SELECT ticker, fair_value, entry_price, details_json
               FROM valuations v WHERE run_date = (
                 SELECT MAX(run_date) FROM valuations WHERE ticker=v.ticker
               )"""
        ).fetchall()
    out = {}
    for ticker, fv, ep, details in rows:
        det = json.loads(details) if details else {}
        out[ticker] = {"fair_value": fv, "entry_price": ep, "details": det}
    return out


# ---------- analytics ----------

def is_ddm_reliable(ticker: str, fund: dict, val: dict) -> bool:
    """DDM só faz sentido para pagadoras consistentes.
    Regras:
      - DY ≥ 3%
      - streak de dividendos ≥ 5 anos
      - fair value entre 0.3× e 5× o preço actual (sanity bound)
    """
    f = fund.get(ticker, {})
    v = val.get(ticker, {})
    if not f or not v:
        return False
    dy = f.get("dy") or 0
    streak = f.get("streak") or 0
    fv = v.get("fair_value") or 0
    current = (v.get("details") or {}).get("outputs", {}).get("current_price")
    if dy < 0.03 or streak < 5:
        return False
    if fv <= 0 or current is None or current == 0:
        return False
    ratio = fv / current
    return 0.3 <= ratio <= 5.0


def rating_for(ticker: str, scores: dict, val: dict, fund: dict) -> tuple[str, str]:
    """Devolve (rating, fonte).
    Lógica:
      - Se o screen passa → BUY
      - Caso contrário, usa o veredicto do DDM quando fiável
      - Fallback: NEUTRO
    """
    s = scores.get(ticker, {})
    if s.get("passes"):
        return "COMPRA", "screen"

    if is_ddm_reliable(ticker, fund, val):
        verdict = (val[ticker]["details"].get("outputs") or {}).get("verdict")
        if verdict == "BUY":
            return "COMPRA", "DDM"
        if verdict == "HOLD":
            return "NEUTRO", "DDM"
        if verdict == "OVERVALUED":
            return "VENDA", "DDM"

    return "NEUTRO", "fallback"


def compute_returns(prices_wide: pd.DataFrame, ticker: str, entry_date: str, entry_price: float) -> dict:
    if ticker not in prices_wide.columns:
        return {}
    s = prices_wide[ticker].dropna()
    if len(s) == 0:
        return {}
    current = float(s.iloc[-1])
    current_date = s.index[-1]

    # retorno desde entrada
    since_entry = current / entry_price - 1

    # retorno no mês (últimos ~21 dias)
    month_start = s[s.index < current_date].iloc[-21] if len(s) > 21 else s.iloc[0]
    month_ret = current / float(month_start) - 1

    # YTD
    current_year = str(current_date)[:4]
    ytd_base = s[s.index.str.startswith(current_year)]
    ytd_ret = current / float(ytd_base.iloc[0]) - 1 if len(ytd_base) > 0 else None

    return {
        "current_price": current,
        "current_date": str(current_date),
        "since_entry": since_entry,
        "month": month_ret,
        "ytd": ytd_ret,
    }


def build_portfolio_series(prices_wide: pd.DataFrame, portfolio: pd.DataFrame,
                           start_date: str) -> pd.Series:
    """Série do valor acumulado da carteira, base 100 na data de entrada
    mais antiga. Pondera pelos pesos do portfolio."""
    prices = prices_wide.copy()
    prices.index = pd.to_datetime(prices.index)

    start = pd.to_datetime(start_date)
    prices = prices[prices.index >= start]

    tickers = portfolio["ticker"].tolist()
    available = [t for t in tickers if t in prices.columns]
    prices = prices[available].ffill().dropna(how="all")

    weights = portfolio.set_index("ticker").loc[available, "weight"]
    weights = weights / weights.sum()  # renormalizar se algum faltar

    # base 100 para cada ticker na data de início dele
    base = prices.iloc[0]
    normed = prices.divide(base, axis=1) * 100

    portfolio_series = (normed * weights).sum(axis=1)
    return portfolio_series


def fetch_ibov_series(start_date: str) -> pd.Series:
    ibov = yf.download(IBOV, start=start_date, auto_adjust=True, progress=False)
    if isinstance(ibov.columns, pd.MultiIndex):
        close = ibov[("Close", IBOV)] if ("Close", IBOV) in ibov.columns else ibov["Close"]
    else:
        close = ibov["Close"]
    close = close.dropna()
    close.index = pd.to_datetime(close.index)
    return close / close.iloc[0] * 100


def portfolio_metrics(port: pd.Series, bench: pd.Series) -> dict:
    # alinha em datas comuns, diário
    port = port.copy()
    port.index = pd.to_datetime(port.index)
    aligned = pd.concat([port.rename("p"), bench.rename("b")], axis=1).dropna()
    if len(aligned) < 30:
        return {}
    ret_p = aligned["p"].pct_change().dropna()
    ret_b = aligned["b"].pct_change().dropna()
    ret_p, ret_b = ret_p.align(ret_b, join="inner")
    vol_p = float(ret_p.std() * (252 ** 0.5))
    vol_b = float(ret_b.std() * (252 ** 0.5))
    ann_p = float(ret_p.mean() * 252)
    sharpe_p = ann_p / vol_p if vol_p > 0 else 0
    sharpe_b = float(ret_b.mean() * 252 / vol_b) if vol_b > 0 else 0
    cov = float(ret_p.cov(ret_b))
    var_b = float(ret_b.var())
    beta = cov / var_b if var_b > 0 else 0
    total_p = float(aligned["p"].iloc[-1] / aligned["p"].iloc[0] - 1)
    total_b = float(aligned["b"].iloc[-1] / aligned["b"].iloc[0] - 1)
    return {
        "sharpe_p": sharpe_p, "sharpe_b": sharpe_b,
        "vol_p": vol_p, "vol_b": vol_b,
        "beta": beta,
        "total_p": total_p, "total_b": total_b,
    }


# ---------- commentary (auto-gerado) ----------

def commentary_for(ticker: str, name: str, rating: str, rating_src: str,
                   returns: dict, fund: dict, val: dict, scores: dict) -> str:
    f = fund.get(ticker, {})
    s = scores.get(ticker, {})
    v = val.get(ticker, {})
    det_v = (v.get("details") or {}).get("outputs", {}) if v else {}
    reliable = is_ddm_reliable(ticker, fund, val)

    parts: list[str] = []

    # Leitura de rating
    if rating == "COMPRA" and rating_src == "screen":
        parts.append(
            f"Passa o screen Graham/Buffett com score <strong>{s.get('score', 0):.2f}</strong> "
            f"(DY {fmt_pct(f.get('dy'))}, ROE {fmt_pct(f.get('roe'))}, "
            f"streak de dividendos {f.get('streak') or '—'} anos)."
        )
    elif rating == "COMPRA" and rating_src == "DDM":
        parts.append(
            f"DDM sugere fair value de <strong>{fmt_money(v.get('fair_value'))}</strong>, "
            f"acima do preço actual — upside de {fmt_pct(det_v.get('upside'), signed=True)}."
        )
    elif rating == "VENDA":
        parts.append(
            f"DDM indica preço actual acima do fair value estimado "
            f"(<strong>{fmt_money(v.get('fair_value'))}</strong>)."
        )
    else:
        parts.append("Não passa no screen primário.")

    # Desempenho recente
    if returns:
        parts.append(
            f"Retorno desde entrada (2025-04) de {fmt_pct(returns.get('since_entry'), signed=True)}, "
            f"{fmt_pct(returns.get('month'), signed=True)} no mês e "
            f"{fmt_pct(returns.get('ytd'), signed=True)} no ano."
        )

    # Notas qualitativas
    if reliable and det_v.get("entry_price"):
        parts.append(
            f"Preço de entrada sugerido (margem de segurança 25%): "
            f"<strong>{fmt_money(det_v.get('entry_price'))}</strong>."
        )
    dy_val = f.get("dy") or 0
    if not reliable and dy_val < 0.03:
        parts.append(
            "DDM não é adequado — empresa de crescimento/commodities "
            "sem histórico de dividendos relevante."
        )
    roe_val = f.get("roe")
    if roe_val is not None and roe_val < 0.10:
        parts.append("Atenção: ROE abaixo de 10%.")

    return " ".join(parts)


# ---------- HTML building ----------

CSS = """
@page { size: 297mm 210mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  font-family: "Segoe UI", -apple-system, system-ui, sans-serif;
  color: #0f172a;
  background: #e2e8f0;
  font-size: 12px;
  line-height: 1.45;
}
.page {
  width: 297mm; min-height: 210mm;
  padding: 12mm 14mm;
  background: #ffffff;
  page-break-after: always;
  margin: 0 auto 12px auto;
  position: relative;
  box-shadow: 0 2px 8px rgba(0,0,0,.08);
}
.page:last-child { page-break-after: auto; }

/* Header / footer */
.header {
  display: flex; justify-content: space-between; align-items: baseline;
  border-bottom: 3px solid #1e3a8a; padding-bottom: 6px; margin-bottom: 14px;
}
.header h1 { color: #1e3a8a; font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
.header .kicker { color: #64748b; font-size: 11px; text-transform: uppercase;
  letter-spacing: .08em; }
.footer {
  position: absolute; bottom: 8mm; left: 14mm; right: 14mm;
  display: flex; justify-content: space-between;
  color: #64748b; font-size: 10px;
  border-top: 1px solid #e2e8f0; padding-top: 6px;
}

/* Cover */
.cover-title {
  color: #1e3a8a; font-size: 42px; font-weight: 800;
  letter-spacing: -0.03em; line-height: 1.05; margin-top: 10mm;
}
.cover-sub {
  color: #d97706; font-size: 20px; font-weight: 600; margin-top: 4px;
}
.cover-meta {
  color: #64748b; font-size: 13px; margin-top: 6px;
}
.cover-lede {
  font-size: 13px; color: #334155; margin: 18px 0 14px 0; max-width: 230mm;
  border-left: 3px solid #d97706; padding-left: 10px;
}

/* Tables */
table { width: 100%; border-collapse: collapse; }
th {
  background: #1e3a8a; color: #ffffff; font-weight: 600;
  text-align: left; padding: 7px 9px; font-size: 11px;
  text-transform: uppercase; letter-spacing: .04em;
}
td {
  padding: 7px 9px; border-bottom: 1px solid #e2e8f0; font-size: 12px;
}
tr:nth-child(even) td { background: #f8fafc; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
td.center { text-align: center; }

/* Rating pills */
.pill {
  display: inline-block; padding: 2px 10px; border-radius: 999px;
  font-size: 10px; font-weight: 700; letter-spacing: .05em;
}
.pill.buy     { background: #dcfce7; color: #166534; }
.pill.hold    { background: #fef3c7; color: #92400e; }
.pill.sell    { background: #fee2e2; color: #991b1b; }
.pill.up      { color: #16a34a; font-weight: 600; }
.pill.down    { color: #dc2626; font-weight: 600; }

/* Metric cards */
.metric-grid {
  display: grid; gap: 10px;
  grid-template-columns: repeat(4, 1fr); margin: 10px 0 14px 0;
}
.metric {
  border: 1px solid #e2e8f0; border-left: 4px solid #1e3a8a;
  padding: 10px 14px; background: #ffffff;
}
.metric .k { color: #64748b; font-size: 10px; text-transform: uppercase;
  letter-spacing: .06em; }
.metric .v { color: #0f172a; font-size: 22px; font-weight: 700; margin-top: 2px; }
.metric .s { color: #64748b; font-size: 11px; margin-top: 2px; }
.metric.alpha { border-left-color: #d97706; }

/* Commentary */
.comment-block {
  border-left: 3px solid #1e3a8a; padding: 8px 14px;
  margin-bottom: 12px; background: #f8fafc;
}
.comment-block .ch {
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 4px;
}
.comment-block .name { font-weight: 700; font-size: 13px; color: #0f172a; }
.comment-block .ticker { color: #64748b; font-size: 11px;
  font-family: "Consolas", monospace; margin-left: 6px; }
.comment-block p { font-size: 11.5px; color: #334155; }

/* Disclaimer */
.disclaimer p { font-size: 10px; color: #64748b; margin-bottom: 6px;
  text-align: justify; }

/* Section headline */
h2.section {
  color: #1e3a8a; font-size: 16px; margin: 8px 0 8px 0;
  padding-bottom: 3px; border-bottom: 1px solid #e2e8f0;
}
p.note { color: #64748b; font-size: 10px; margin-top: 4px; font-style: italic; }

/* Screen display niceties */
@media screen {
  body { padding: 20px 0; }
}
"""


def page_header(title: str, kicker: str) -> str:
    return (
        f'<div class="header">'
        f'<h1>{title}</h1>'
        f'<div class="kicker">{kicker}</div>'
        f'</div>'
    )


def page_footer(page_num: int, total: int) -> str:
    now = datetime.now().strftime("%d/%m/%Y")
    return (
        f'<div class="footer">'
        f'<span>Investment Intelligence · Relatório executivo · {now}</span>'
        f'<span>página {page_num} de {total}</span>'
        f'</div>'
    )


def build_cover(portfolio: pd.DataFrame, fund: dict, scores: dict, val: dict,
                prices_wide: pd.DataFrame) -> str:
    month_pt = datetime.now().strftime("%B %Y").replace(
        "January", "Janeiro").replace("February", "Fevereiro").replace("March", "Março") \
        .replace("April", "Abril").replace("May", "Maio").replace("June", "Junho") \
        .replace("July", "Julho").replace("August", "Agosto").replace("September", "Setembro") \
        .replace("October", "Outubro").replace("November", "Novembro").replace("December", "Dezembro")

    rows_html = []
    for _, row in portfolio.iterrows():
        ticker = row["ticker"]
        rating, _ = rating_for(ticker, scores, val, fund)
        pill_cls = {"COMPRA": "buy", "NEUTRO": "hold", "VENDA": "sell"}[rating]
        f = fund.get(ticker, {})
        v = val.get(ticker, {})
        reliable = is_ddm_reliable(ticker, fund, val)
        fv_cell = fmt_money(v.get("fair_value")) if reliable else "—"
        current = (v.get("details") or {}).get("outputs", {}).get("current_price")
        if current is None and ticker in prices_wide.columns:
            s = prices_wide[ticker].dropna()
            current = float(s.iloc[-1]) if len(s) else None
        rows_html.append(
            f"<tr>"
            f"<td>{row['sector']}</td>"
            f"<td>{row['name']}</td>"
            f"<td><code>{ticker}</code></td>"
            f"<td class='num'>{fmt_pct(row['weight'], nd=1)}</td>"
            f"<td class='center'><span class='pill {pill_cls}'>{rating}</span></td>"
            f"<td class='num'>{fmt_money(current)}</td>"
            f"<td class='num'>{fv_cell}</td>"
            f"<td class='num'>{fmt_pct(f.get('dy'))}</td>"
            f"</tr>"
        )
    table_html = (
        "<table><thead><tr>"
        "<th>Setor</th><th>Companhia</th><th>Ticker</th>"
        "<th class='num'>Peso</th><th class='center'>Rating</th>"
        "<th class='num'>Preço</th><th class='num'>Fair value</th>"
        "<th class='num'>DY</th>"
        "</tr></thead><tbody>" + "".join(rows_html) + "</tbody></table>"
    )

    passes = sum(1 for t in portfolio["ticker"] if scores.get(t, {}).get("passes"))
    lede = (
        f"Carteira equal-weight composta por {len(portfolio)} ações brasileiras "
        f"selecionadas pelo screen Graham/Buffett adaptado. "
        f"<strong>{passes} de {len(portfolio)}</strong> passa(m) no screen primário este mês. "
        f"Fontes: brapi.dev, Status Invest, CVM Dados Abertos, Yahoo Finance. "
        f"Valuation por Gordon DDM onde aplicável."
    )

    return (
        '<div class="page">'
        + page_header("Investment Intelligence BR", f"Carteira · {month_pt}")
        + '<div class="cover-title">Carteira Dividendos BR</div>'
        + '<div class="cover-sub">Screen Graham/Buffett adaptado</div>'
        + f'<div class="cover-meta">Relatório mensal · {fmt_date_br(datetime.now().strftime("%Y-%m-%d"))}</div>'
        + f'<div class="cover-lede">{lede}</div>'
        + '<h2 class="section">Composição e recomendação</h2>'
        + table_html
        + '<p class="note">Preços de fechamento do último pregão disponível na DB. '
          'Fair value por Gordon DDM (r=14%, g capado). "—" indica que o DDM não é '
          'adequado ao perfil da empresa (crescimento/commodities).</p>'
        + page_footer(1, 5)
        + '</div>'
    )


def build_performance(portfolio: pd.DataFrame, prices_wide: pd.DataFrame,
                      port_series: pd.Series, ibov_series: pd.Series) -> str:
    # tabela por ticker
    rows = []
    for _, row in portfolio.iterrows():
        t = row["ticker"]
        r = compute_returns(prices_wide, t, row["entry_date"], row["entry_price"])
        if not r:
            continue
        def cls(v): return "pill up" if v and v >= 0 else "pill down"
        rows.append(
            f"<tr>"
            f"<td>{row['name']}</td><td><code>{t}</code></td>"
            f"<td>{row['sector']}</td>"
            f"<td class='num'>{fmt_pct(row['weight'], nd=1)}</td>"
            f"<td class='num'>{fmt_date_br(row['entry_date'])}</td>"
            f"<td class='num'>{fmt_money(row['entry_price'])}</td>"
            f"<td class='num'>{fmt_money(r['current_price'])}</td>"
            f"<td class='num'><span class='{cls(r['since_entry'])}'>{fmt_pct(r['since_entry'], signed=True)}</span></td>"
            f"<td class='num'><span class='{cls(r['month'])}'>{fmt_pct(r['month'], signed=True)}</span></td>"
            f"<td class='num'><span class='{cls(r['ytd'])}'>{fmt_pct(r['ytd'], signed=True)}</span></td>"
            f"</tr>"
        )
    table = (
        "<table><thead><tr>"
        "<th>Companhia</th><th>Ticker</th><th>Setor</th>"
        "<th class='num'>Peso</th><th class='num'>Entrada</th>"
        "<th class='num'>Preço entrada</th><th class='num'>Preço actual</th>"
        "<th class='num'>Desde entrada</th><th class='num'>Mês</th>"
        "<th class='num'>YTD</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )

    m = portfolio_metrics(port_series, ibov_series)
    metrics_html = ""
    if m:
        metrics_html = (
            '<div class="metric-grid">'
            f'<div class="metric"><div class="k">Retorno total</div>'
            f'<div class="v">{fmt_pct(m["total_p"], signed=True)}</div>'
            f'<div class="s">IBOV {fmt_pct(m["total_b"], signed=True)}</div></div>'
            f'<div class="metric alpha"><div class="k">Alpha vs IBOV</div>'
            f'<div class="v">{fmt_pct(m["total_p"] - m["total_b"], signed=True)}</div>'
            f'<div class="s">desde entrada da carteira</div></div>'
            f'<div class="metric"><div class="k">Volatilidade anual</div>'
            f'<div class="v">{fmt_pct(m["vol_p"])}</div>'
            f'<div class="s">IBOV {fmt_pct(m["vol_b"])}</div></div>'
            f'<div class="metric"><div class="k">Beta</div>'
            f'<div class="v">{fmt_num(m["beta"])}</div>'
            f'<div class="s">sensibilidade vs IBOV</div></div>'
            '</div>'
        )

    return (
        '<div class="page">'
        + page_header("Desempenho por ativo", "Página 2")
        + metrics_html
        + '<h2 class="section">Retorno por posição</h2>'
        + table
        + '<p class="note">Retornos calculados a partir de preços ajustados (splits + dividendos). '
          '"Mês" = últimos 21 pregões. Métricas de Sharpe/vol/beta computadas em base diária anualizada.</p>'
        + page_footer(2, 5)
        + '</div>'
    )


def build_chart_page(port_series: pd.Series, ibov_series: pd.Series) -> str:
    port_series = port_series.copy()
    port_series.index = pd.to_datetime(port_series.index)
    aligned = pd.concat(
        [port_series.rename("port"), ibov_series.rename("ibov")], axis=1
    ).dropna()
    if len(aligned) == 0:
        return ('<div class="page">' + page_header("Retorno acumulado", "Página 3")
                + '<p class="note">Sem dados suficientes.</p>'
                + page_footer(3, 5) + '</div>')

    # rebase ambas a 100 no primeiro ponto comum
    aligned["port"] = aligned["port"] / aligned["port"].iloc[0] * 100
    aligned["ibov"] = aligned["ibov"] / aligned["ibov"].iloc[0] * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=aligned.index, y=aligned["port"], name="Carteira",
        line=dict(color="#1e3a8a", width=2.8),
    ))
    fig.add_trace(go.Scatter(
        x=aligned.index, y=aligned["ibov"], name="Ibovespa",
        line=dict(color="#94a3b8", width=2, dash="dot"),
    ))
    fig.add_hline(y=100, line=dict(color="#cbd5e1", width=1),
                  annotation_text="base 100", annotation_position="right")
    fig.update_layout(
        title=dict(text="Retorno acumulado (base 100)",
                   font=dict(color="#1e3a8a", size=18)),
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", y=-0.15),
        margin=dict(l=50, r=30, t=60, b=40),
        font=dict(family="Segoe UI", size=12),
    )
    chart = fig.to_html(include_plotlyjs="cdn", full_html=False,
                        config={"displayModeBar": False})

    return (
        '<div class="page">'
        + page_header("Retorno acumulado", "Carteira vs Ibovespa")
        + '<h2 class="section">Trajetória desde a entrada da carteira</h2>'
        + '<div style="margin-top:10px;">' + chart + '</div>'
        + '<p class="note">Rebase 100 na primeira data com ambas as séries disponíveis. '
          'Carteira ponderada pelos pesos actuais; dividendos reinvestidos via auto_adjust do Yahoo Finance.</p>'
        + page_footer(3, 5)
        + '</div>'
    )


def build_commentary(portfolio: pd.DataFrame, prices_wide: pd.DataFrame,
                     fund: dict, scores: dict, val: dict) -> str:
    blocks = []
    for _, row in portfolio.iterrows():
        t = row["ticker"]
        rating, src = rating_for(t, scores, val, fund)
        pill_cls = {"COMPRA": "buy", "NEUTRO": "hold", "VENDA": "sell"}[rating]
        r = compute_returns(prices_wide, t, row["entry_date"], row["entry_price"])
        text = commentary_for(t, row["name"], rating, src, r, fund, val, scores)
        blocks.append(
            f'<div class="comment-block">'
            f'<div class="ch">'
            f'<div><span class="name">{row["name"]}</span>'
            f'<span class="ticker">{t} · {row["sector"]}</span></div>'
            f'<span class="pill {pill_cls}">{rating}</span>'
            f'</div>'
            f'<p>{text}</p>'
            f'</div>'
        )
    return (
        '<div class="page">'
        + page_header("Comentários por posição", "Página 4")
        + "".join(blocks)
        + '<p class="note">Comentários auto-gerados a partir da DB. '
          'Rating "COMPRA" prioriza screen primário; se não passa, usa veredicto do DDM '
          'quando o modelo é adequado (empresa pagadora consistente).</p>'
        + page_footer(4, 5)
        + '</div>'
    )


def build_disclaimer() -> str:
    return (
        '<div class="page disclaimer">'
        + page_header("Disclaimer", "Informação importante")
        + "<p>1) Este relatório foi gerado automaticamente por um sistema pessoal "
          "de inteligência de investimentos. NÃO constitui recomendação profissional "
          "de investimento, nem foi produzido por analista credenciado pela CVM.</p>"
          "<p>2) Os screens Graham/Buffett utilizados são simplificações didácticas "
          "dos critérios clássicos de valor e qualidade. O veredicto 'COMPRA' "
          "significa apenas que o ativo cumpre os critérios mecânicos definidos, "
          "não que seja necessariamente uma boa decisão de investimento no contexto "
          "macroeconómico e individual do investidor.</p>"
          "<p>3) O modelo Gordon DDM utilizado assume crescimento perpétuo constante "
          "de dividendos, o que é uma aproximação grosseira. O valor justo calculado "
          "deve ser interpretado como ordem de grandeza, não como preço-alvo preciso. "
          "Para empresas que não pagam dividendos consistentes (commodities, growth), "
          "o DDM é propositadamente omitido.</p>"
          "<p>4) Fontes de dados: brapi.dev (cotações BR), Status Invest (fundamentals BR "
          "por web scraping), CVM Dados Abertos (fatos relevantes), Yahoo Finance (histórico "
          "longo e dividendos). A qualidade dos dados não é garantida. Discrepâncias entre "
          "fontes foram observadas em séries de dividendos e não estão totalmente reconciliadas.</p>"
          "<p>5) Desempenho passado não garante resultados futuros. Os retornos apresentados "
          "usam preços ajustados para splits e dividendos; retornos reais após impostos, "
          "custos de transacção e câmbio serão diferentes.</p>"
          "<p>6) Este relatório é privado e gerado para uso pessoal do autor. "
          "Não deve ser redistribuído ou usado como base para decisões de investimento "
          "por terceiros.</p>"
        + page_footer(5, 5)
        + '</div>'
    )


# ---------- main ----------

def main() -> None:
    REPORTS.mkdir(exist_ok=True)

    portfolio = load_portfolio()
    if portfolio.empty:
        raise SystemExit("portfolio_positions vazio — corre scripts/seed_portfolio.py")

    fund = load_fundamentals()
    scores = load_scores()
    val = load_valuations()
    prices_wide = load_prices_wide()

    earliest_entry = portfolio["entry_date"].min()
    port_series = build_portfolio_series(prices_wide, portfolio, earliest_entry)
    ibov_series = fetch_ibov_series(earliest_entry)

    pages = [
        build_cover(portfolio, fund, scores, val, prices_wide),
        build_performance(portfolio, prices_wide, port_series, ibov_series),
        build_chart_page(port_series, ibov_series),
        build_commentary(portfolio, prices_wide, fund, scores, val),
        build_disclaimer(),
    ]

    html = (
        '<!doctype html><html lang="pt-br"><head><meta charset="utf-8">'
        '<title>Carteira BR · Relatório Executivo</title>'
        f'<style>{CSS}</style></head><body>'
        + "".join(pages) +
        '</body></html>'
    )

    month_tag = datetime.now().strftime("%Y%m")
    out = REPORTS / f"executive_br_{month_tag}.html"
    out.write_text(html, encoding="utf-8")
    print(f"[ok] {out}")
    webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()
