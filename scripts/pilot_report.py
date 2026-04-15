"""Relatório HTML do piloto — protótipo do futuro weekly_report.py.

Lê tudo da DB (nunca toca na rede), gera:
  - reports/pilot_<ticker>.md    (fonte canónica em markdown)
  - reports/pilot_<ticker>.html  (apresentação: CSS + Plotly embutido)

Secções:
  1. Tese & Preços            (verdict, fair value, entry, thesis break)
  2. Gráfico preço + dividendos anuais (Plotly interativo)
  3. Fundamentos              (tabela)
  4. Scoring                  (pass/fail/n/a por critério)
  5. Eventos CVM recentes     (fatos relevantes + comunicados)

Uso:
    python scripts/pilot_report.py            # ITSA4
    python scripts/pilot_report.py PRIO3
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from fetchers.cache_policy import fmt_date_br  # noqa: E402

ROOT = _ROOT
DB_PATH = ROOT / "data" / "br_investments.db"
REPORTS = ROOT / "reports"

VERDICT_ICON = {"pass": "✅", "fail": "❌", "n/a": "➖"}
VERDICT_BADGE_CLASS = {"pass": "badge-pass", "fail": "badge-fail", "n/a": "badge-na"}
RECO_BADGE_CLASS = {"BUY": "reco-buy", "HOLD": "reco-hold", "OVERVALUED": "reco-sell"}


# ---------- helpers ----------

def fmt_pct(x, nd=2):
    return f"{x*100:.{nd}f}%" if isinstance(x, (int, float)) else "—"


def fmt_num(x, nd=2):
    return f"{x:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(x, (int, float)) else "—"


def fmt_money(x, currency="R$", nd=2):
    if not isinstance(x, (int, float)):
        return "—"
    return f"{currency} {fmt_num(x, nd)}"


# ---------- leitura ----------

def load_all(ticker: str) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        co = conn.execute(
            "SELECT ticker, name, sector, is_holding, currency FROM companies WHERE ticker=?",
            (ticker,),
        ).fetchone()
        if not co:
            raise SystemExit(f"{ticker} não está em companies")
        fund = conn.execute(
            """SELECT period_end, eps, bvps, roe, pe, pb, dy,
                      net_debt_ebitda, dividend_streak_years
               FROM fundamentals WHERE ticker=?
               ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        price_series = conn.execute(
            "SELECT date, close FROM prices WHERE ticker=? ORDER BY date ASC",
            (ticker,),
        ).fetchall()
        divs_annual = conn.execute(
            "SELECT year, amount FROM dividends_annual WHERE ticker=? ORDER BY year ASC",
            (ticker,),
        ).fetchall()
        score = conn.execute(
            """SELECT run_date, score, passes_screen, details_json
               FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        valuation = conn.execute(
            """SELECT run_date, model, fair_value, entry_price, details_json
               FROM valuations WHERE ticker=? ORDER BY run_date DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        events = conn.execute(
            """SELECT event_date, kind, summary, url FROM events
               WHERE ticker=? AND source='cvm' ORDER BY event_date DESC LIMIT 10""",
            (ticker,),
        ).fetchall()
    return {
        "company": co,
        "fundamentals": fund,
        "prices": price_series,
        "dividends_annual": divs_annual,
        "score": score,
        "valuation": valuation,
        "events": events,
    }


# ---------- gráfico Plotly ----------

def build_chart(data: dict, ticker: str, currency: str) -> str:
    prices = data["prices"]
    divs = data["dividends_annual"]

    fig = go.Figure()

    if prices:
        dates = [p[0] for p in prices]
        closes = [p[1] for p in prices]
        fig.add_trace(go.Scatter(
            x=dates, y=closes, name="Preço",
            mode="lines", line=dict(color="#2563eb", width=2),
            yaxis="y1",
        ))

    if divs:
        years = [str(d[0]) for d in divs]
        amounts = [d[1] for d in divs]
        fig.add_trace(go.Bar(
            x=years, y=amounts, name="Dividendos anuais",
            marker=dict(color="#10b981"),
            yaxis="y2", opacity=0.7,
        ))

    # Linhas de fair value e entry
    val = data["valuation"]
    if val and prices:
        det = json.loads(val[4]) if val[4] else {}
        fv = det.get("outputs", {}).get("fair_value")
        ep = det.get("outputs", {}).get("entry_price")
        if fv:
            fig.add_hline(y=fv, line=dict(color="#16a34a", dash="dash"),
                          annotation_text=f"Fair value {fmt_money(fv, currency)}",
                          annotation_position="top left", yref="y1")
        if ep:
            fig.add_hline(y=ep, line=dict(color="#ca8a04", dash="dot"),
                          annotation_text=f"Entry {fmt_money(ep, currency)}",
                          annotation_position="bottom left", yref="y1")

    fig.update_layout(
        title=f"{ticker} — Preço diário & Dividendos anuais",
        xaxis=dict(title="Data / Ano"),
        yaxis=dict(title=f"Preço ({currency})", side="left"),
        yaxis2=dict(title=f"Dividendo ({currency}/ação)", overlaying="y",
                    side="right", showgrid=False),
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=40, r=40, t=60, b=40),
        height=480,
        template="plotly_white",
    )
    return fig.to_html(include_plotlyjs="cdn", full_html=False)


# ---------- markdown builder (mantido para auditoria) ----------

def build_md(data: dict, ticker: str, currency: str) -> str:
    co = data["company"]
    name = co[1]; sector = co[2]; in_portfolio = bool(co[3])
    fund = data["fundamentals"]
    prices = data["prices"]
    score = data["score"]
    val = data["valuation"]

    lines = []
    lines.append(f"# {ticker} — {name}")
    lines.append("")
    lines.append(f"> Gerado em {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
                 f"Sector *{sector}* · {'Na carteira' if in_portfolio else 'Watchlist'}")
    lines.append("")

    # Tese & Preços
    lines.append("## Tese & Preços")
    if val:
        det = json.loads(val[4]) if val[4] else {}
        out = det.get("outputs", {})
        inp = det.get("inputs", {})
        lines.append(f"- **Veredicto:** {out.get('verdict') or '—'}")
        lines.append(f"- **Fair value (Gordon DDM):** {fmt_money(out.get('fair_value'), currency)}")
        lines.append(f"- **Preço de entrada:** {fmt_money(out.get('entry_price'), currency)} "
                     f"(margem de segurança {fmt_pct(inp.get('margin_of_safety'))})")
        lines.append(f"- **Preço actual:** {fmt_money(out.get('current_price'), currency)}")
        if out.get("upside") is not None:
            lines.append(f"- **Upside ao fair value:** {fmt_pct(out['upside'])}")
        lines.append("")
        lines.append(f"**Premissas do modelo:** D₀={fmt_num(inp.get('d0'))}, "
                     f"g={fmt_pct(inp.get('g'))} (CAGR cru {fmt_pct(inp.get('g_raw'))}), "
                     f"r={fmt_pct(inp.get('r'))}")
        notes = det.get("notes") or []
        for n in notes:
            lines.append(f"- _Nota:_ {n}")
        lines.append("")
        lines.append("**Quando vender (thesis break):**")
        for cond in det.get("thesis_break", []):
            lines.append(f"- {cond['label']}")
    else:
        lines.append("_Sem valuation calculada._")
    lines.append("")

    # Preço / histórico
    lines.append("## Preço")
    if prices:
        latest = prices[-1]
        closes = [p[1] for p in prices]
        lines.append(f"- **Último fechamento:** {fmt_money(latest[1], currency)} ({fmt_date_br(latest[0])})")
        lines.append(f"- **Janela na DB:** {fmt_date_br(prices[0][0])} → {fmt_date_br(prices[-1][0])} ({len(prices)} dias)")
        lines.append(f"- **Min / Max:** {fmt_money(min(closes), currency)} / {fmt_money(max(closes), currency)}")
    lines.append("")

    # Fundamentos
    lines.append("## Fundamentos")
    if fund:
        lines.append("| Campo | Valor |")
        lines.append("|---|---|")
        lines.append(f"| Período | {fund[0]} |")
        lines.append(f"| EPS (LPA) | {fmt_num(fund[1])} |")
        lines.append(f"| BVPS (VPA) | {fmt_num(fund[2])} |")
        lines.append(f"| ROE | {fmt_pct(fund[3])} |")
        lines.append(f"| P/E | {fmt_num(fund[4])} |")
        lines.append(f"| P/B | {fmt_num(fund[5])} |")
        lines.append(f"| Dividend Yield | {fmt_pct(fund[6])} |")
        lines.append(f"| Dív. líq / EBITDA | {fmt_num(fund[7])} |")
        lines.append(f"| Dividend streak (anos) | {fund[8] if fund[8] is not None else '—'} |")
    lines.append("")

    # Scoring
    lines.append("## Scoring")
    if score:
        lines.append(f"- **Score:** {score[1]:.2f}")
        lines.append(f"- **Passes screen:** {'sim' if score[2] else 'não'}")
        lines.append("")
        details = json.loads(score[3]) if score[3] else {}
        lines.append("| Critério | Valor | Threshold | Veredicto |")
        lines.append("|---|---|---|---|")
        for k, d in details.items():
            icon = VERDICT_ICON.get(d.get("verdict"), "?")
            reason = f" _({d['reason']})_" if d.get("reason") else ""
            lines.append(f"| `{k}` | {d.get('value')} | {d.get('threshold')} | {icon} {d.get('verdict')}{reason} |")
    lines.append("")

    # Eventos
    lines.append("## Eventos recentes (CVM)")
    for ev_date, kind, summary, url in data["events"]:
        tag = "🔴" if kind == "fato_relevante" else "🔵"
        summary = (summary or "").replace("|", "·")
        link = f" · [PDF]({url})" if url else ""
        lines.append(f"- {tag} **{fmt_date_br(ev_date)}** — _{kind}_ — {summary}{link}")
    lines.append("")
    lines.append("---")
    lines.append("_Fontes: brapi.dev + Status Invest + CVM Dados Abertos. Valuation: Gordon DDM._")
    return "\n".join(lines) + "\n"


# ---------- HTML builder (sem dependência de markdown lib) ----------

CSS = """
:root {
  --bg: #0f172a; --fg: #e2e8f0; --muted: #94a3b8;
  --card: #1e293b; --border: #334155;
  --accent: #3b82f6; --pass: #10b981; --fail: #ef4444; --na: #6b7280;
  --warn: #f59e0b;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #f8fafc; --fg: #0f172a; --muted: #64748b;
    --card: #ffffff; --border: #e2e8f0;
  }
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", system-ui, "Inter", sans-serif;
  background: var(--bg); color: var(--fg);
  max-width: 1080px; margin: 0 auto; padding: 2rem 1.5rem;
  line-height: 1.6;
}
h1 { font-size: 2rem; margin: 0 0 .25rem 0; }
h2 { font-size: 1.25rem; margin: 2.5rem 0 1rem 0;
     padding-bottom: .4rem; border-bottom: 1px solid var(--border); }
.subtitle { color: var(--muted); margin-bottom: 2rem; }
.card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 1.25rem 1.5rem; margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
.metric { background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem 1.25rem; }
.metric .label { color: var(--muted); font-size: .8rem;
  text-transform: uppercase; letter-spacing: .05em; margin-bottom: .35rem; }
.metric .value { font-size: 1.4rem; font-weight: 600; }
.metric .sub { color: var(--muted); font-size: .85rem; margin-top: .25rem; }
.reco {
  display: inline-block; padding: .4rem .9rem; border-radius: 999px;
  font-weight: 700; font-size: 1rem; letter-spacing: .03em;
}
.reco-buy   { background: #10b98122; color: #10b981; border: 1px solid #10b98166; }
.reco-hold  { background: #f59e0b22; color: #f59e0b; border: 1px solid #f59e0b66; }
.reco-sell  { background: #ef444422; color: #ef4444; border: 1px solid #ef444466; }
.badge { display: inline-block; padding: .15rem .55rem;
  border-radius: 999px; font-size: .8rem; font-weight: 600; }
.badge-pass { background: #10b98122; color: #10b981; }
.badge-fail { background: #ef444422; color: #ef4444; }
.badge-na   { background: #6b728022; color: #94a3b8; }
table { width: 100%; border-collapse: collapse; margin: .75rem 0; }
th, td { text-align: left; padding: .55rem .75rem;
  border-bottom: 1px solid var(--border); font-size: .92rem; }
th { color: var(--muted); font-weight: 600; text-transform: uppercase;
  font-size: .75rem; letter-spacing: .05em; }
tr:last-child td { border-bottom: none; }
code { background: var(--border); padding: .1rem .4rem; border-radius: 4px;
  font-size: .85em; }
.event { padding: .7rem 0; border-bottom: 1px dashed var(--border); }
.event:last-child { border-bottom: none; }
.event .dot { display: inline-block; width: .6rem; height: .6rem;
  border-radius: 50%; margin-right: .5rem; vertical-align: middle; }
.event.fato .dot { background: #ef4444; }
.event.comunicado .dot { background: #3b82f6; }
.event .date { color: var(--muted); font-size: .85rem; margin-right: .5rem; }
.event a { color: var(--accent); text-decoration: none; margin-left: .3rem; }
.event a:hover { text-decoration: underline; }
ul.thesis { padding-left: 1.1rem; margin: .3rem 0; }
ul.thesis li { margin: .2rem 0; }
.note { color: var(--muted); font-style: italic; font-size: .88rem; }
footer { color: var(--muted); font-size: .8rem; margin-top: 3rem;
  padding-top: 1rem; border-top: 1px solid var(--border); text-align: center; }
"""


def build_html(data: dict, ticker: str) -> str:
    co = data["company"]
    name = co[1]; sector = co[2]; in_portfolio = bool(co[3]); currency = co[4]
    sym = "R$" if currency == "BRL" else "$"
    fund = data["fundamentals"]
    prices = data["prices"]
    score = data["score"]
    val = data["valuation"]

    parts: list[str] = []
    parts.append(f'<h1>{ticker} — {name}</h1>')
    parts.append(
        f'<div class="subtitle">Gerado em {datetime.now().strftime("%Y-%m-%d %H:%M")} · '
        f'Sector <strong>{sector}</strong> · {"Na carteira" if in_portfolio else "Watchlist"}</div>'
    )

    # === Tese & Preços ===
    parts.append("<h2>Tese &amp; Preços</h2>")
    if val:
        det = json.loads(val[4]) if val[4] else {}
        out = det.get("outputs", {})
        inp = det.get("inputs", {})
        verdict = out.get("verdict") or "—"
        reco_cls = RECO_BADGE_CLASS.get(verdict, "reco-hold")

        parts.append('<div class="card">')
        parts.append(f'<p><span class="reco {reco_cls}">{verdict}</span></p>')
        parts.append('<div class="grid">')
        parts.append(
            f'<div class="metric"><div class="label">Preço actual</div>'
            f'<div class="value">{fmt_money(out.get("current_price"), sym)}</div>'
            f'<div class="sub">{fmt_date_br(prices[-1][0]) if prices else ""}</div></div>'
        )
        parts.append(
            f'<div class="metric"><div class="label">Fair value (DDM)</div>'
            f'<div class="value">{fmt_money(out.get("fair_value"), sym)}</div>'
            f'<div class="sub">Gordon Growth Model</div></div>'
        )
        parts.append(
            f'<div class="metric"><div class="label">Preço de entrada</div>'
            f'<div class="value">{fmt_money(out.get("entry_price"), sym)}</div>'
            f'<div class="sub">margem de segurança {fmt_pct(inp.get("margin_of_safety"))}</div></div>'
        )
        ups = out.get("upside")
        ups_str = fmt_pct(ups) if ups is not None else "—"
        parts.append(
            f'<div class="metric"><div class="label">Upside</div>'
            f'<div class="value">{ups_str}</div>'
            f'<div class="sub">vs fair value</div></div>'
        )
        parts.append("</div>")  # grid

        parts.append(
            f'<p class="note">Premissas: D₀ = {fmt_num(inp.get("d0"))}, '
            f'g = {fmt_pct(inp.get("g"))} (CAGR cru {fmt_pct(inp.get("g_raw"))}, '
            f'{inp.get("g_years_window")} anos desde {inp.get("g_start_year")}), '
            f'r = {fmt_pct(inp.get("r"))}</p>'
        )
        for n in det.get("notes") or []:
            parts.append(f'<p class="note">· {n}</p>')

        parts.append("<p><strong>Quando vender (thesis break):</strong></p><ul class='thesis'>")
        for cond in det.get("thesis_break", []):
            parts.append(f"<li>{cond['label']}</li>")
        parts.append("</ul>")
        parts.append("</div>")  # card
    else:
        parts.append('<div class="card"><p class="note">Sem valuation calculada.</p></div>')

    # === Gráfico ===
    parts.append("<h2>Gráfico</h2>")
    parts.append('<div class="card">')
    parts.append(build_chart(data, ticker, sym))
    parts.append("</div>")

    # === Fundamentos ===
    parts.append("<h2>Fundamentos</h2>")
    if fund:
        rows = [
            ("Período", fund[0]),
            ("EPS (LPA)", fmt_num(fund[1])),
            ("BVPS (VPA)", fmt_num(fund[2])),
            ("ROE", fmt_pct(fund[3])),
            ("P/E", fmt_num(fund[4])),
            ("P/B", fmt_num(fund[5])),
            ("Dividend Yield", fmt_pct(fund[6])),
            ("Dív. líq / EBITDA", fmt_num(fund[7])),
            ("Dividend streak (anos)", fund[8] if fund[8] is not None else "—"),
        ]
        parts.append('<div class="card"><table><thead><tr><th>Campo</th><th>Valor</th></tr></thead><tbody>')
        for k, v in rows:
            parts.append(f"<tr><td>{k}</td><td>{v}</td></tr>")
        parts.append("</tbody></table></div>")

    # === Scoring ===
    parts.append("<h2>Scoring</h2>")
    if score:
        details = json.loads(score[3]) if score[3] else {}
        passes = "PASSA" if score[2] else "NÃO PASSA"
        parts.append(
            f'<div class="card"><p>Score <strong>{score[1]:.2f}</strong> · '
            f'<strong>{passes}</strong> o screen · run {score[0]}</p>'
        )
        parts.append('<table><thead><tr><th>Critério</th><th>Valor</th><th>Threshold</th><th>Veredicto</th></tr></thead><tbody>')
        for k, d in details.items():
            v = d.get("value")
            v_str = fmt_num(v, 4) if isinstance(v, float) else str(v)
            t = d.get("threshold")
            verdict = d.get("verdict")
            cls = VERDICT_BADGE_CLASS.get(verdict, "badge-na")
            reason = d.get("reason") or ""
            reason_html = f' <span class="note">({reason})</span>' if reason else ""
            parts.append(
                f'<tr><td><code>{k}</code></td><td>{v_str}</td><td>{t}</td>'
                f'<td><span class="badge {cls}">{verdict}</span>{reason_html}</td></tr>'
            )
        parts.append("</tbody></table></div>")

    # === Eventos ===
    parts.append("<h2>Eventos recentes (CVM)</h2>")
    parts.append('<div class="card">')
    if data["events"]:
        for ev_date, kind, summary, url in data["events"]:
            cls = "fato" if kind == "fato_relevante" else "comunicado"
            summary = (summary or "").replace("|", "·")
            link = f' <a href="{url}" target="_blank">PDF ↗</a>' if url else ""
            parts.append(
                f'<div class="event {cls}"><span class="dot"></span>'
                f'<span class="date">{fmt_date_br(ev_date)}</span>'
                f'<strong>{kind}</strong> — {summary}{link}</div>'
            )
    else:
        parts.append('<p class="note">Sem eventos CVM.</p>')
    parts.append("</div>")

    parts.append(
        '<footer>Fontes: brapi.dev · Status Invest · CVM Dados Abertos. '
        'Valuation por Gordon DDM. Este relatório é informativo, não constitui recomendação de investimento.</footer>'
    )

    return (
        '<!doctype html><html lang="pt-br"><head><meta charset="utf-8">'
        f'<title>{ticker} — {name}</title>'
        f'<style>{CSS}</style></head><body>'
        + "\n".join(parts)
        + "</body></html>"
    )


# ---------- main ----------

def main() -> None:
    ticker = sys.argv[1] if len(sys.argv) > 1 else "ITSA4"
    REPORTS.mkdir(exist_ok=True)
    data = load_all(ticker)
    currency = data["company"][4]
    sym = "R$" if currency == "BRL" else "$"

    md_text = build_md(data, ticker, sym)
    html_text = build_html(data, ticker)

    md_path = REPORTS / f"pilot_{ticker.lower()}.md"
    html_path = REPORTS / f"pilot_{ticker.lower()}.html"
    md_path.write_text(md_text, encoding="utf-8")
    html_path.write_text(html_text, encoding="utf-8")
    print(f"[ok] {md_path}")
    print(f"[ok] {html_path}")


if __name__ == "__main__":
    main()
