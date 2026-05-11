"""daily_synthesizer — agrega tudo que mudou nas últimas 24-48h e produz
o "What changed today" focado no portfolio do user.

Pipeline:
  1. gather()      — SQL puro: insights + themes + analyst + events +
                     verdict deltas + price moves + triggers das ÚLTIMAS 24h.
                     Filtrado/ranqueado por relevância às holdings.
  2. synthesize()  — Ollama (Qwen 14B) gera narrativa PT-BR top items.
  3. write_vault() — `obsidian_vault/Bibliotheca/Daily_Synthesis_<DATE>.md`.
  4. push_telegram() — opcional, formato compactado mobile.

Uso:
    python -m agents.daily_synthesizer
    python -m agents.daily_synthesizer --hours 48 --no-llm --dry-run
    python -m agents.daily_synthesizer --push-telegram

Cron: wired no daily_run.bat antes do TELEGRAM-BRIEF (07:00 brief consome).
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
VAULT_OUT = ROOT / "obsidian_vault" / "Bibliotheca"
LOG_FILE = ROOT / "logs" / "daily_synthesizer.log"


@dataclass
class TickerEvent:
    ticker: str
    market: str
    kind: str          # "insight_yt" | "insight_analyst" | "filing" | "verdict_change" | "price_move" | "trigger" | "theme"
    source: str        # channel / publisher / engine
    timestamp: str
    summary: str
    significance: float = 0.5  # 0-1 score
    extra: dict = field(default_factory=dict)


def _log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {msg}\n")


def _holdings(market: str) -> dict[str, dict]:
    """Returns {ticker: {qty, market_value, entry_price, ...}} for active positions."""
    db = DB_BR if market == "br" else DB_US
    out: dict[str, dict] = {}
    if not db.exists():
        return out
    try:
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            for r in c.execute("""
                SELECT ticker, quantity, entry_price
                FROM portfolio_positions WHERE active=1
            """).fetchall():
                out[r["ticker"]] = {
                    "qty": r["quantity"] or 0,
                    "entry_price": r["entry_price"] or 0,
                    "market": market,
                }
    except sqlite3.OperationalError:
        pass
    return out


def _fetch_video_insights(market: str, since_iso: str) -> list[TickerEvent]:
    db = DB_BR if market == "br" else DB_US
    out: list[TickerEvent] = []
    if not db.exists():
        return out
    try:
        with sqlite3.connect(db) as c:
            # Filter by processed_at (when WE ingested) — surfaces stale-published
            # but newly-ingested content. Fall back to created_at then published_at.
            for row in c.execute("""
                SELECT v.published_at, v.processed_at, v.channel, v.title, v.video_id,
                       i.ticker, i.kind, i.claim, i.confidence
                FROM video_insights i
                LEFT JOIN videos v ON i.video_id = v.video_id
                WHERE COALESCE(v.processed_at, i.created_at, v.published_at) >= ?
                ORDER BY COALESCE(v.processed_at, i.created_at, v.published_at) DESC
            """, (since_iso,)).fetchall():
                pub, proc, ch, title, vid, ticker, kind, claim, conf = row
                ts = (proc or pub or "")[:19]
                out.append(TickerEvent(
                    ticker=ticker,
                    market=market,
                    kind="insight_yt",
                    source=ch or "?",
                    timestamp=ts,
                    summary=(claim or "").strip(),
                    significance=float(conf or 0.5),
                    extra={"video_id": vid, "video_title": (title or "")[:100],
                           "kind_detail": kind, "published": pub, "ingested": proc},
                ))
    except sqlite3.OperationalError:
        pass
    return out


def _fetch_analyst_insights(market: str, since_iso: str) -> list[TickerEvent]:
    db = DB_BR if market == "br" else DB_US
    out: list[TickerEvent] = []
    if not db.exists():
        return out
    try:
        with sqlite3.connect(db) as c:
            for row in c.execute("""
                SELECT r.published_at, r.source, r.title,
                       ai.ticker, ai.kind, ai.stance, ai.claim, ai.price_target, ai.confidence
                FROM analyst_insights ai
                JOIN analyst_reports r ON ai.report_id = r.id
                WHERE r.published_at >= ?
                ORDER BY r.published_at DESC
            """, (since_iso,)).fetchall():
                pub, src, title, ticker, kind, stance, claim, pt, conf = row
                out.append(TickerEvent(
                    ticker=ticker,
                    market=market,
                    kind="insight_analyst",
                    source=(src or "?").upper(),
                    timestamp=(pub or "")[:19],
                    summary=(claim or "").strip(),
                    significance=float(conf or 0.6),
                    extra={"stance": stance, "price_target": pt, "report": (title or "")[:80], "kind_detail": kind},
                ))
    except sqlite3.OperationalError:
        pass
    return out


def _fetch_filings(market: str, since_iso: str) -> list[TickerEvent]:
    db = DB_BR if market == "br" else DB_US
    out: list[TickerEvent] = []
    if not db.exists():
        return out
    try:
        with sqlite3.connect(db) as c:
            for row in c.execute("""
                SELECT ticker, event_date, source, kind, summary, url
                FROM events
                WHERE event_date >= ?
                ORDER BY event_date DESC
            """, (since_iso[:10],)).fetchall():
                ticker, ed, src, kind, summ, url = row
                out.append(TickerEvent(
                    ticker=ticker,
                    market=market,
                    kind="filing",
                    source=(src or "?").upper(),
                    timestamp=ed or "",
                    summary=(summ or "")[:300],
                    significance=0.7 if kind == "fato_relevante" else 0.5,
                    extra={"filing_kind": kind, "url": url},
                ))
    except sqlite3.OperationalError:
        pass
    return out


def _fetch_verdict_changes(market: str, since_iso: str) -> list[TickerEvent]:
    db = DB_BR if market == "br" else DB_US
    out: list[TickerEvent] = []
    if not db.exists():
        return out
    try:
        with sqlite3.connect(db) as c:
            for row in c.execute("""
                SELECT ticker, run_date, score, action, previous_action, delta_score
                FROM verdict_history
                WHERE run_date >= ?
                  AND (previous_action IS NULL OR previous_action <> action)
                ORDER BY run_date DESC
            """, (since_iso[:10],)).fetchall():
                ticker, rd, score, action, prev, delta = row
                if not prev:
                    summary = f"Novo verdict: {action} (score {score})"
                    sig = 0.6
                else:
                    summary = f"Verdict mudou: {prev} → {action} (Δscore {delta:+.2f})"
                    sig = 0.85
                out.append(TickerEvent(
                    ticker=ticker, market=market, kind="verdict_change",
                    source="verdict_engine", timestamp=rd or "",
                    summary=summary, significance=sig,
                    extra={"score": score, "from": prev, "to": action, "delta": delta},
                ))
    except sqlite3.OperationalError:
        pass
    return out


def _fetch_triggers(market: str, since_iso: str) -> list[TickerEvent]:
    db = DB_BR if market == "br" else DB_US
    out: list[TickerEvent] = []
    if not db.exists():
        return out
    try:
        with sqlite3.connect(db) as c:
            for row in c.execute("""
                SELECT ticker, kind, action_hint, note, created_at
                FROM watchlist_actions
                WHERE status='open' AND created_at >= ?
                ORDER BY created_at DESC
            """, (since_iso,)).fetchall():
                ticker, kind, ah, note, ca = row
                out.append(TickerEvent(
                    ticker=ticker, market=market, kind="trigger",
                    source="trigger_engine", timestamp=(ca or "")[:19],
                    summary=f"{kind}: {ah}" + (f" — {note[:120]}" if note else ""),
                    significance=0.75,
                    extra={"trigger_kind": kind, "action": ah},
                ))
    except sqlite3.OperationalError:
        pass
    return out


def _fetch_themes(market: str, since_iso: str, limit: int = 12) -> list[TickerEvent]:
    """Macro themes are not per-ticker — surfaced as separate signal."""
    db = DB_BR if market == "br" else DB_US
    out: list[TickerEvent] = []
    if not db.exists():
        return out
    try:
        with sqlite3.connect(db) as c:
            for row in c.execute("""
                SELECT v.processed_at, v.published_at, v.channel,
                       t.theme, t.stance, t.summary, t.confidence
                FROM video_themes t
                LEFT JOIN videos v ON t.video_id = v.video_id
                WHERE COALESCE(v.processed_at, v.published_at) >= ?
                ORDER BY COALESCE(v.processed_at, v.published_at) DESC,
                         t.confidence DESC NULLS LAST
                LIMIT ?
            """, (since_iso, limit)).fetchall():
                proc, pub, ch, theme, stance, summary, conf = row
                # Higher conf themes get more weight; bullish/bearish > neutral
                stance_mult = 1.0 if stance in ("bullish", "bearish") else 0.7
                out.append(TickerEvent(
                    ticker="—",  # macro theme has no ticker
                    market=market,
                    kind="theme",
                    source=ch or "?",
                    timestamp=(proc or pub or "")[:19],
                    summary=(summary or "").strip(),
                    significance=float(conf or 0.5) * stance_mult,
                    extra={"theme": theme, "stance": stance or "neutral"},
                ))
    except sqlite3.OperationalError:
        pass
    return out


def _fetch_price_moves(market: str, since_iso: str, holdings: set[str], threshold_pct: float = 3.0) -> list[TickerEvent]:
    """Holdings with abs price move > threshold_pct in window."""
    db = DB_BR if market == "br" else DB_US
    out: list[TickerEvent] = []
    if not db.exists() or not holdings:
        return out
    placeholders = ",".join("?" * len(holdings))
    try:
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            for ticker in holdings:
                rows = c.execute(f"""
                    SELECT date, close FROM prices
                    WHERE ticker=? AND date >= ?
                    ORDER BY date DESC LIMIT 2
                """, (ticker, since_iso[:10])).fetchall()
                if len(rows) < 2:
                    continue
                latest, prior = rows[0]["close"], rows[1]["close"]
                if not prior or prior == 0:
                    continue
                pct = (latest - prior) / prior * 100
                if abs(pct) >= threshold_pct:
                    direction = "↑" if pct > 0 else "↓"
                    out.append(TickerEvent(
                        ticker=ticker, market=market, kind="price_move",
                        source="prices", timestamp=rows[0]["date"],
                        summary=f"{direction} {pct:+.2f}% ({prior:.2f} → {latest:.2f})",
                        significance=min(0.9, 0.4 + abs(pct) / 20),
                        extra={"pct": pct, "from": prior, "to": latest},
                    ))
    except sqlite3.OperationalError:
        pass
    return out


def gather(hours: int = 24) -> dict:
    """Pure SQL aggregation. Returns dict keyed by market with events list."""
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat(timespec="seconds")
    out: dict = {"cutoff": cutoff, "hours": hours, "br": {}, "us": {}, "totals": {}}

    for market in ("br", "us"):
        holdings = _holdings(market)
        events: list[TickerEvent] = []
        events += _fetch_video_insights(market, cutoff)
        events += _fetch_analyst_insights(market, cutoff)
        events += _fetch_filings(market, cutoff)
        events += _fetch_verdict_changes(market, cutoff)
        events += _fetch_triggers(market, cutoff)
        events += _fetch_price_moves(market, cutoff, set(holdings.keys()))
        events += _fetch_themes(market, cutoff)

        # Boost significance for events on holdings (skin in the game)
        for e in events:
            if e.ticker in holdings:
                e.significance = min(1.0, e.significance + 0.15)
                e.extra["is_holding"] = True

        events.sort(key=lambda e: (e.significance, e.timestamp), reverse=True)
        out[market] = {
            "holdings": holdings,
            "events": events,
            "n_events": len(events),
            "n_on_holdings": sum(1 for e in events if e.extra.get("is_holding")),
        }
    out["totals"] = {
        "all_events": len(out["br"]["events"]) + len(out["us"]["events"]),
        "on_holdings": out["br"]["n_on_holdings"] + out["us"]["n_on_holdings"],
    }
    return out


def _format_event_row(e: TickerEvent) -> str:
    holding_mark = " 💼" if e.extra.get("is_holding") else ""
    icon = {
        "insight_yt": "🎙️",
        "insight_analyst": "📰",
        "filing": "📜",
        "verdict_change": "🎯",
        "trigger": "⚡",
        "price_move": "📈",
        "theme": "🌐",
    }.get(e.kind, "•")
    summ = e.summary[:200].replace("|", "\\|").replace("\n", " ")
    return f"| {icon} | **{e.ticker}**{holding_mark} | {e.source[:18]} | {summ} |"


def synthesize(snapshot: dict, *, max_top: int = 8, no_llm: bool = False) -> str:
    """Compose markdown. Optional Ollama narrative for top items."""
    cutoff = snapshot["cutoff"]
    hours = snapshot["hours"]
    today = datetime.now(timezone.utc).date().isoformat()

    lines = [
        f"# Daily Synthesis — {today}",
        "",
        f"_Window: últimas {hours}h (desde `{cutoff[:16]}`). "
        f"{snapshot['totals']['all_events']} eventos, "
        f"{snapshot['totals']['on_holdings']} sobre holdings._",
        "",
    ]

    # Top picks across markets — those with highest significance, holdings preferred
    all_events: list[TickerEvent] = (
        snapshot["br"]["events"] + snapshot["us"]["events"]
    )
    if not all_events:
        lines.append("_Sem novidades materiais nas últimas 24h._")
        return "\n".join(lines)

    top = all_events[:max_top]

    lines.append("## 🎯 Top moves (ranked by significance × holding-fit)")
    lines.append("")
    lines.append("| | Ticker | Fonte | Resumo |")
    lines.append("|---|---|---|---|")
    for e in top:
        lines.append(_format_event_row(e))
    lines.append("")

    # LLM narrative if enabled
    if not no_llm and top:
        narrative = _llm_narrative(top, snapshot)
        if narrative:
            lines.append("## 📝 What it means (Qwen 14B narrative)")
            lines.append("")
            lines.append(narrative)
            lines.append("")

    # Per-bucket detail
    for market in ("br", "us"):
        ev = snapshot[market]["events"]
        if not ev:
            continue
        flag = "🇧🇷" if market == "br" else "🇺🇸"
        lines.append(f"## {flag} {market.upper()} — todos os eventos ({len(ev)})")
        lines.append("")

        # Group by kind
        from collections import defaultdict
        groups = defaultdict(list)
        for e in ev:
            groups[e.kind].append(e)

        for kind in ("verdict_change", "trigger", "filing", "price_move",
                     "insight_analyst", "insight_yt"):
            items = groups.get(kind, [])
            if not items:
                continue
            label = {
                "insight_yt": "🎙️ YouTube + Podcast insights",
                "insight_analyst": "📰 Analyst insights",
                "filing": "📜 Filings (CVM/SEC)",
                "verdict_change": "🎯 Verdict changes",
                "trigger": "⚡ Triggers",
                "price_move": "📈 Price moves >3%",
            }[kind]
            lines.append(f"### {label} ({len(items)})")
            lines.append("")
            for e in items[:15]:  # cap per group
                hold = " 💼" if e.extra.get("is_holding") else ""
                lines.append(
                    f"- `{e.timestamp[:10]}` **{e.ticker}**{hold} "
                    f"({e.source[:20]}): {e.summary[:200]}"
                )
            lines.append("")

    return "\n".join(lines)


def _llm_narrative(top: list[TickerEvent], snapshot: dict) -> str:
    """Call Ollama for short PT-BR narrative on top events."""
    try:
        from agents._llm import llm_summarise
    except ImportError:
        return ""

    brief_lines = []
    for e in top:
        hold = " 💼" if e.extra.get("is_holding") else ""
        extra_bits = []
        if e.kind == "insight_analyst" and e.extra.get("price_target"):
            extra_bits.append(f"PT={e.extra['price_target']}")
        if e.kind == "insight_analyst" and e.extra.get("stance"):
            extra_bits.append(f"stance={e.extra['stance']}")
        if e.kind == "verdict_change":
            extra_bits.append(f"{e.extra.get('from')}→{e.extra.get('to')}")
        if e.kind == "price_move":
            extra_bits.append(f"{e.extra.get('pct'):+.2f}%")
        if e.kind == "theme":
            extra_bits.append(f"theme={e.extra.get('theme')} stance={e.extra.get('stance')}")
        meta = f" ({', '.join(extra_bits)})" if extra_bits else ""
        brief_lines.append(
            f"- {e.ticker}{hold} [{e.kind}{meta}] from {e.source}: {e.summary[:220]}"
        )

    # Build allowed_tickers set: events tickers + holdings only.
    # LLM is forbidden from mentioning tickers outside this set.
    allowed = set()
    for e in top:
        if e.ticker and e.ticker != "—":
            allowed.add(e.ticker)
    allowed.update(snapshot["br"]["holdings"].keys())
    allowed.update(snapshot["us"]["holdings"].keys())
    allowed_str = ", ".join(sorted(allowed)) if allowed else "(nenhum)"

    holdings_summary = ", ".join(
        sorted(snapshot["br"]["holdings"].keys())[:8] +
        sorted(snapshot["us"]["holdings"].keys())[:8]
    )

    prompt = (
        f"Tu és analista pessoal sénior do investidor abaixo (estratégia DRIP, "
        f"BR+US, Buffett/Graham). Olha os eventos das últimas {snapshot['hours']}h "
        f"e produz uma síntese em PT-BR de 3-5 parágrafos curtos com:\n\n"
        f"1. **Tema central**: 1 parágrafo nomeando o tema dominante (ex: "
        f"'Selic elevada pressiona FIIs', 'Earnings season tech mista'). Cita "
        f"≥2 fontes específicas.\n"
        f"2. **Holdings impactadas**: 1 parágrafo SÓ sobre holdings (ver lista). "
        f"Para cada uma: TICKER + facto observável + número (PT, %, $) + fonte.\n"
        f"3. **Sinais conflitantes**: 1 parágrafo se houver — ex: "
        f"'2 fontes recomendam X, mas Y emitiu trigger contrário'.\n"
        f"4. **Acção hoje**: 1 parágrafo. Se houver verdict_change ou trigger "
        f"sobre holding, AGE — diz qual review fazer. Senão: 'Dia calmo'.\n\n"
        f"REGRAS DURAS:\n"
        f"- NUNCA inventes números, datas, ou price targets. Só os listados nos eventos.\n"
        f"- TICKERS PERMITIDOS — mencione APENAS estes; qualquer outro = hallucination:\n"
        f"  {allowed_str}\n"
        f"- Refere o ticker tal e qual (ex: BBDC4, ITSA4) — NÃO traduzas para nome de empresa.\n"
        f"  Se quiseres ser claro, escreve só `BBDC4` sem parênteses.\n"
        f"- Cita o NOME da fonte (BTG, Genial, FT, etc.) em cada claim — não 'analistas'.\n"
        f"- Prefere holdings > watchlist > universe. Sem holding mencionada = falha.\n"
        f"- Não recomendes BUY/SELL sem ≥2 fontes concordantes (excepto trigger explícito).\n"
        f"- Se há evento crítico (verdict_change, content_trigger), trata como prioritário.\n"
        f"- Sem markdown headers (## etc). Sem emojis. Texto corrido.\n\n"
        f"HOLDINGS DO INVESTIDOR: {holdings_summary}\n\n"
        f"EVENTOS RANQUEADOS:\n" + "\n".join(brief_lines)
    )

    try:
        out = llm_summarise(
            prompt,
            prefer="ollama",
            system="És analista pessoal sénior. Conciso, sem emojis, sem markdown headers.",
            max_tokens=600,
            temperature=0.3,
        )
        if out and not out.startswith("[LLM"):
            return out.strip()
    except Exception as e:
        _log(f"narrative LLM fail: {type(e).__name__}: {e}")
    return ""


def write_vault(content: str, *, dry_run: bool) -> Path:
    today = datetime.now(timezone.utc).date().isoformat()
    out_path = VAULT_OUT / f"Daily_Synthesis_{today}.md"
    if dry_run:
        return out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path


def push_telegram(snapshot: dict, narrative: str = "") -> bool:
    """Compact Telegram summary."""
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            try:
                from dotenv import load_dotenv
                load_dotenv(ROOT / ".env")
                token = os.environ.get("TELEGRAM_BOT_TOKEN")
                chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            except ImportError:
                pass
        if not token or not chat_id:
            return False

        all_events = snapshot["br"]["events"] + snapshot["us"]["events"]
        on_holdings = [e for e in all_events if e.extra.get("is_holding")]

        text_parts = [
            f"🌅 *Daily Synthesis* — {datetime.now(timezone.utc).date().isoformat()}",
            f"_{snapshot['totals']['all_events']} eventos · "
            f"{snapshot['totals']['on_holdings']} sobre holdings_",
            "",
        ]
        if on_holdings:
            text_parts.append("*Top sobre tuas posições:*")
            for e in on_holdings[:5]:
                icon = {
                    "verdict_change": "🎯", "trigger": "⚡",
                    "filing": "📜", "price_move": "📈",
                    "insight_analyst": "📰", "insight_yt": "🎙️",
                }.get(e.kind, "•")
                text_parts.append(f"{icon} *{e.ticker}* — {e.summary[:90]}")
            text_parts.append("")

        if narrative:
            text_parts.append("*Tema do dia:*")
            text_parts.append(narrative[:600])
            text_parts.append("")

        text_parts.append("Ver dossier completo em `Bibliotheca/Daily_Synthesis_<date>.md`")

        import urllib.parse, urllib.request
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": "\n".join(text_parts)[:4000],
            "parse_mode": "Markdown",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data, method="POST",
        )
        urllib.request.urlopen(req, timeout=10).read()
        return True
    except Exception as e:
        _log(f"telegram push fail: {type(e).__name__}: {e}")
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--max-top", type=int, default=8)
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--push-telegram", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    snapshot = gather(args.hours)
    content = synthesize(snapshot, max_top=args.max_top, no_llm=args.no_llm)

    out_path = write_vault(content, dry_run=args.dry_run)

    # Extract narrative again for telegram (already in content if LLM ran)
    narrative = ""
    if "## 📝 What it means" in content:
        chunks = content.split("## 📝 What it means")
        if len(chunks) > 1:
            block = chunks[1].split("##", 1)[0].strip()
            narrative = block.split("\n", 2)[-1].strip() if "\n" in block else ""

    if args.push_telegram and not args.dry_run:
        ok = push_telegram(snapshot, narrative)
        if not args.quiet:
            print(f"  telegram: {'pushed' if ok else 'skipped/failed'}")

    if not args.quiet:
        print(f"daily_synthesis: {snapshot['totals']['all_events']} events, "
              f"{snapshot['totals']['on_holdings']} on holdings")
        if args.dry_run:
            print(f"DRY-RUN — would write {out_path}")
            print()
            print(content[:2000])
            if len(content) > 2000:
                print(f"\n... (+{len(content)-2000} chars)")
        else:
            print(f"wrote {out_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
