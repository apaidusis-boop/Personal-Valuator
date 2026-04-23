"""verdict — motor de decisão agregado "buy/hold/sell/watch".

Dado um ticker, produz um verdicto escorado em 4 dimensões:
  - Quality    (35%) — Altman + Piotroski + DivSafety
  - Valuation  (30%) — Screen score + DY percentile
  - Momentum   (20%) — 1d / 30d / YTD price action
  - Narrativa  (15%) — User notes + YouTube insights + peer divergence

Acção recomendada: AVOID | SELL | HOLD | WATCH | ADD | BUY

Output: markdown block (pode ser injectado no topo do ticker note em Obsidian)
        + JSON strict para consumo programático (--json).

Usa Qwen local (14B) opcional para narrativa humanizada (--narrate).

Uso:
    python scripts/verdict.py ACN                # verdict só
    python scripts/verdict.py ACN --narrate      # + prose local LLM
    python scripts/verdict.py ACN --write        # escreve no vault
    python scripts/verdict.py --all-holdings --write   # batch
    python scripts/verdict.py --json ACN
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
VAULT = ROOT / "obsidian_vault"


@dataclass
class Verdict:
    ticker: str
    market: str
    action: str             # AVOID|SELL|HOLD|WATCH|ADD|BUY
    total_score: float      # 0-10
    confidence_pct: int
    quality_score: float    # 0-10 weighted 35%
    valuation_score: float  # 0-10 weighted 30%
    momentum_score: float   # 0-10 weighted 20%
    narrative_score: float  # 0-10 weighted 15%
    quality_detail: dict
    valuation_detail: dict
    momentum_detail: dict
    narrative_detail: dict
    reasons: list[str]
    generated_at: str


# ------------------------- Scoring helpers ----------------------------------

def _altman_pts(z: float | None, applicable: bool) -> float:
    if not applicable or z is None:
        return 5.0  # N/A neutral
    if z >= 3.0: return 10.0
    if z >= 1.81: return 5.0
    return 0.0


def _piotroski_pts(f: int | None, applicable: bool) -> float:
    if not applicable or f is None:
        return 5.0
    if f >= 7: return 10.0
    if f >= 5: return 6.0
    if f >= 3: return 3.0
    return 0.0


def _safety_pts(s: float | None) -> float:
    if s is None:
        return 5.0
    if s >= 80: return 10.0
    if s >= 60: return 6.0
    if s >= 40: return 3.0
    return 0.0


def _pct_tier_pts(pct: float | None, tiers: list[tuple[float, float]]) -> float:
    """tiers: [(threshold, pts), ...] sorted DESC. pct=None → neutral 5.0."""
    if pct is None:
        return 5.0
    for thr, pts in tiers:
        if pct >= thr:
            return pts
    return 0.0


_MOMENTUM_TIERS = [(3.0, 8.0), (0.0, 6.0), (-3.0, 4.0), (-10.0, 2.0)]
_MOMENTUM_YTD_TIERS = [(10.0, 8.0), (0.0, 6.0), (-10.0, 4.0), (-25.0, 2.0)]


def _price_history(conn: sqlite3.Connection, ticker: str) -> list[tuple]:
    return list(conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 300",
        (ticker,),
    ))


def _momentum(conn: sqlite3.Connection, ticker: str) -> dict:
    rows = _price_history(conn, ticker)
    if len(rows) < 2:
        return {"score": 5.0, "reasons": ["insuficiente histórico"]}
    latest_d, latest = rows[0]
    prev = rows[1][1]
    d30_idx = min(20, len(rows) - 1)
    d30 = rows[d30_idx][1] if d30_idx < len(rows) else None
    # YTD: procura primeiro preço do ano actual
    year_start = date.fromisoformat(latest_d).replace(month=1, day=1).isoformat()
    ytd_price = None
    for d, c in reversed(rows):
        if d >= year_start:
            ytd_price = c
            break

    chg_1d = ((latest / prev - 1) * 100) if prev else None
    chg_30d = ((latest / d30 - 1) * 100) if d30 else None
    chg_ytd = ((latest / ytd_price - 1) * 100) if ytd_price else None

    s1 = _pct_tier_pts(chg_1d, _MOMENTUM_TIERS)
    s30 = _pct_tier_pts(chg_30d, _MOMENTUM_TIERS)
    sy = _pct_tier_pts(chg_ytd, _MOMENTUM_YTD_TIERS)
    score = (s1 + s30 + sy) / 3
    return {
        "score": round(score, 2),
        "change_1d_pct": round(chg_1d, 2) if chg_1d is not None else None,
        "change_30d_pct": round(chg_30d, 2) if chg_30d is not None else None,
        "change_ytd_pct": round(chg_ytd, 2) if chg_ytd is not None else None,
        "price_latest": latest,
        "price_date": latest_d,
    }


def _narrative(ticker: str, market: str) -> dict:
    notes_exist = False
    notes_tags = []
    try:
        from scripts.notes_cli import read_note
        n = read_note(ticker)
        if n:
            fm, body = n
            notes_exist = bool(body and body.strip())
            if fm.get("tags"):
                notes_tags = [t.strip() for t in fm["tags"].split(",") if t.strip()]
    except Exception:  # noqa: BLE001
        pass

    yt_recent = 0
    cutoff = (date.today() - timedelta(days=60)).isoformat()
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                r = c.execute(
                    """SELECT COUNT(*) FROM video_insights
                       WHERE ticker=? AND created_at >= ?""",
                    (ticker, cutoff),
                ).fetchone()
                yt_recent += r[0] or 0
            except sqlite3.OperationalError:
                pass

    score = 4.0  # base
    reasons = []
    if notes_exist:
        score += 3.0
        reasons.append("user note presente")
    if yt_recent >= 3:
        score += 3.0
        reasons.append(f"{yt_recent} YT insights recentes")
    elif yt_recent >= 1:
        score += 1.5
        reasons.append(f"{yt_recent} YT insight recente")
    else:
        reasons.append("zero cobertura YouTube")

    return {
        "score": min(score, 10.0),
        "user_note": notes_exist,
        "tags": notes_tags,
        "yt_insights_60d": yt_recent,
        "reasons": reasons,
    }


# ------------------------- Main aggregate -----------------------------------

def compute_verdict(ticker: str) -> Verdict:
    from scripts.research import evaluate, _detect_market
    market = _detect_market(ticker)
    if not market:
        raise ValueError(f"{ticker} não encontrado em nenhum DB")

    ev = evaluate(ticker, market)
    if "error" in ev:
        raise ValueError(ev["error"])

    # Quality
    altman_apl = ev.get("altman_z") is not None
    altman_pts = _altman_pts(ev.get("altman_z"), altman_apl)
    piot_apl = ev.get("piotroski_f") is not None
    piot_pts = _piotroski_pts(ev.get("piotroski_f"), piot_apl)
    safety_pts = _safety_pts(ev.get("safety"))
    quality_score = (altman_pts + piot_pts + safety_pts) / 3
    quality_detail = {
        "altman_z": ev.get("altman_z"),
        "altman_zone": ev.get("altman_zone"),
        "altman_pts": altman_pts,
        "piotroski_f": ev.get("piotroski_f"),
        "piotroski_label": ev.get("piotroski_label"),
        "piotroski_pts": piot_pts,
        "div_safety": ev.get("safety"),
        "safety_pts": safety_pts,
    }

    # Valuation
    screen = ev.get("screen_score", 0) or 0
    screen_pts = screen * 10
    dy_pctl = ev.get("dy_pctl_value")
    dy_adj = 0
    if dy_pctl is not None:
        if dy_pctl >= 75: dy_adj = 2
        elif dy_pctl <= 25: dy_adj = -2
    valuation_score = max(0, min(10, screen_pts + dy_adj))
    valuation_detail = {
        "screen_score": screen,
        "screen_pts": screen_pts,
        "dy_percentile": dy_pctl,
        "dy_label": ev.get("dy_pctl_label"),
        "dy_adjustment": dy_adj,
    }

    # Momentum
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        momentum = _momentum(c, ticker)
    momentum_score = momentum["score"]

    # Narrativa
    narr = _narrative(ticker, market)
    narrative_score = narr["score"]

    # Total
    total = (quality_score * 0.35 + valuation_score * 0.30
             + momentum_score * 0.20 + narrative_score * 0.15)

    # Action mapping
    reasons: list[str] = []
    altman_z = ev.get("altman_z")
    piot_f = ev.get("piotroski_f")

    # Vetos
    if altman_apl and altman_z is not None and altman_z < 1.81:
        action = "AVOID"
        reasons.append(f"Altman {altman_z:.2f} < 1.81 (distress veto)")
    elif piot_apl and piot_f is not None and piot_f <= 3:
        action = "AVOID"
        reasons.append(f"Piotroski {piot_f}/9 ≤ 3 (quality veto)")
    elif ev.get("is_holding") and total < 4:
        action = "SELL"
        reasons.append(f"holding + total {total:.1f} < 4")
    elif total >= 7.5:
        action = "BUY" if not ev.get("is_holding") else "ADD"
        reasons.append(f"total {total:.1f} ≥ 7.5")
    elif total >= 6.0 and valuation_score >= 7:
        action = "WATCH"
        reasons.append("valuation atractiva mas quality ou momentum fraco")
    else:
        action = "HOLD" if ev.get("is_holding") else "SKIP"
        reasons.append(f"total {total:.1f} na zona neutra")

    # Enriquecer reasons
    if quality_score >= 8: reasons.append("quality forte")
    elif quality_score < 4: reasons.append("quality frágil")
    if valuation_score >= 8: reasons.append("valuation barato")
    elif valuation_score < 4: reasons.append("valuation caro")
    if momentum["change_1d_pct"] is not None and momentum["change_1d_pct"] <= -5:
        reasons.append(f"queda 1d {momentum['change_1d_pct']:.1f}%")
    if dy_pctl is not None and dy_pctl >= 75:
        reasons.append(f"DY percentil P{dy_pctl:.0f} (historicamente CHEAP)")

    # Confidence heurístico
    conf = 50
    if altman_apl: conf += 10
    if piot_apl: conf += 10
    if narr["yt_insights_60d"] >= 3: conf += 10
    if narr["user_note"]: conf += 10
    if total <= 2 or total >= 8: conf += 10  # extremos = mais confiança
    conf = min(conf, 95)

    return Verdict(
        ticker=ticker, market=market, action=action,
        total_score=round(total, 2),
        confidence_pct=conf,
        quality_score=round(quality_score, 2),
        valuation_score=round(valuation_score, 2),
        momentum_score=round(momentum_score, 2),
        narrative_score=round(narrative_score, 2),
        quality_detail=quality_detail,
        valuation_detail=valuation_detail,
        momentum_detail=momentum,
        narrative_detail=narr,
        reasons=reasons,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


# ------------------------- Render markdown ----------------------------------

ACTION_ICONS = {
    "BUY": "🟢", "ADD": "🟢", "WATCH": "🟡",
    "HOLD": "🟠", "SELL": "🔴", "AVOID": "⛔", "SKIP": "⚪",
}


def _bar(score: float, width: int = 10) -> str:
    filled = int(round(score / 10 * width))
    return "█" * filled + "░" * (width - filled)


def render_markdown(v: Verdict, narrate: str | None = None) -> str:
    icon = ACTION_ICONS.get(v.action, "•")
    lines = []
    lines.append(f"## 🎯 Verdict — {icon} {v.action}\n")
    lines.append(f"> **Score**: {v.total_score:.1f}/10  |  **Confiança**: {v.confidence_pct}%  |  _{v.generated_at}_\n")

    lines.append("| Dimensão | Score | Peso | Bar |")
    lines.append("|---|---:|---:|---|")
    lines.append(f"| Quality    | {v.quality_score:.1f}/10 | 35% | `{_bar(v.quality_score)}` |")
    lines.append(f"| Valuation  | {v.valuation_score:.1f}/10 | 30% | `{_bar(v.valuation_score)}` |")
    lines.append(f"| Momentum   | {v.momentum_score:.1f}/10 | 20% | `{_bar(v.momentum_score)}` |")
    lines.append(f"| Narrativa  | {v.narrative_score:.1f}/10 | 15% | `{_bar(v.narrative_score)}` |")
    lines.append("")

    lines.append("### Detalhes\n")
    qd = v.quality_detail
    lines.append(
        f"- **Quality**: Altman Z {qd['altman_z']} ({qd['altman_zone']}), "
        f"Piotroski {qd['piotroski_f']}/9 ({qd['piotroski_label']}), "
        f"DivSafety {qd['div_safety']}/100"
    )
    vd = v.valuation_detail
    dy_p = vd.get("dy_percentile")
    dy_s = f"P{dy_p:.0f}" if dy_p is not None else "-"
    lines.append(
        f"- **Valuation**: Screen {vd['screen_score']:.2f}, "
        f"DY percentil {dy_s} ({vd['dy_label'] or '-'})"
    )
    md = v.momentum_detail
    lines.append(
        f"- **Momentum**: 1d {md.get('change_1d_pct')}%, "
        f"30d {md.get('change_30d_pct')}%, "
        f"YTD {md.get('change_ytd_pct')}%"
    )
    nd = v.narrative_detail
    lines.append(
        f"- **Narrativa**: user_note={nd['user_note']}, YT insights 60d={nd['yt_insights_60d']}"
    )
    lines.append("")

    lines.append("### Razões\n")
    for r in v.reasons:
        lines.append(f"- {r}")
    lines.append("")

    if narrate:
        lines.append("### Síntese (Qwen local)\n")
        lines.append(narrate)
        lines.append("")

    return "\n".join(lines)


def synthesize_narrative(v: Verdict) -> str:
    """Chama Qwen 14B para gerar prose explicativa."""
    import requests
    system = """Você é analista quant Buffett-Graham. Dados estruturados abaixo.
Gere 2-3 frases em PT explicando o verdict, mencionando o ticker e números exactos.
NÃO invente dados. Foque na lógica de decisão e acção imediata."""
    user = f"""TICKER: {v.ticker} ({v.market.upper()})
ACTION: {v.action}
TOTAL: {v.total_score:.1f}/10 (conf {v.confidence_pct}%)
QUALITY: {v.quality_score:.1f}/10 — {v.quality_detail}
VALUATION: {v.valuation_score:.1f}/10 — {v.valuation_detail}
MOMENTUM: {v.momentum_score:.1f}/10 — {v.momentum_detail}
NARRATIVE: {v.narrative_score:.1f}/10 — {v.narrative_detail}
REASONS: {v.reasons}
"""
    try:
        r = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:14b-instruct-q4_K_M",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "options": {"temperature": 0.2, "num_ctx": 4096},
                "stream": False,
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
    except Exception as e:  # noqa: BLE001
        return f"_(Qwen indisponível: {e})_"


# ------------------------- Write into vault ---------------------------------

def write_into_vault(v: Verdict, verdict_md: str) -> Path:
    """Injecta a secção Verdict no topo de tickers/<TICKER>.md (abaixo do frontmatter)."""
    path = VAULT / "tickers" / f"{v.ticker}.md"
    if not path.exists():
        raise FileNotFoundError(f"{path} — corre obsidian_bridge primeiro")
    text = path.read_text(encoding="utf-8")
    # Split frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        fm = text[: end + 3]
        body = text[end + 3 :]
    else:
        fm = ""
        body = text

    # Remove bloco verdict anterior se existir
    import re
    body = re.sub(
        r"\n## 🎯 Verdict.*?(?=\n## |\Z)", "", body, count=1, flags=re.DOTALL
    )

    new = fm + "\n\n" + verdict_md + "\n" + body.lstrip("\n")
    path.write_text(new, encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=False)
    g.add_argument("ticker", nargs="?")
    g.add_argument("--all-holdings", action="store_true")
    ap.add_argument("--narrate", action="store_true", help="Qwen 14B prose")
    ap.add_argument("--write", action="store_true", help="Inject no vault ticker note")
    ap.add_argument("--json", action="store_true", help="Raw JSON")
    args = ap.parse_args()

    if args.all_holdings:
        for market, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                holdings = [r[0] for r in c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1 ORDER BY ticker"
                )]
            for tk in holdings:
                try:
                    v = compute_verdict(tk)
                    narrate = synthesize_narrative(v) if args.narrate else None
                    md = render_markdown(v, narrate)
                    print(f"\n=== {tk} ({v.action}) ===")
                    print(f"score={v.total_score:.1f}/10 conf={v.confidence_pct}%")
                    if args.write:
                        p = write_into_vault(v, md)
                        print(f"  wrote {p}")
                except Exception as e:  # noqa: BLE001
                    print(f"  {tk}: ERROR — {e}")
        return 0

    if not args.ticker:
        ap.print_help()
        return 1
    tk = args.ticker.upper()
    v = compute_verdict(tk)
    if args.json:
        print(json.dumps(asdict(v), ensure_ascii=False, indent=2))
        return 0
    narrate = synthesize_narrative(v) if args.narrate else None
    md = render_markdown(v, narrate)
    print(md)
    if args.write:
        p = write_into_vault(v, md)
        print(f"\n[wrote] {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
