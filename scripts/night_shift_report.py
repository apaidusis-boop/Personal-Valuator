"""Night Shift Report generator — reads logs/night_shift_progress_<DATE>.jsonl
and produces a consolidated MD in obsidian_vault/Bibliotheca/.

Output sections:
  - Sumário executivo (count, time, stances breakdown)
  - Tabela completa: ticker | stance | confidence | seats | flags | evidence | elapsed
  - Stance changes vs prior snapshot (from delta MDs)
  - Top pre-publication flags by ticker
  - Specialists most-convocated this night
  - Errors & retries needed
  - Tomorrow's priorities
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
DOSSIERS_DIR = ROOT / "obsidian_vault" / "dossiers"
BIBLIOTHECA_DIR = ROOT / "obsidian_vault" / "Bibliotheca"


def load_progress(target_date: date) -> list[dict]:
    p = LOG_DIR / f"night_shift_progress_{target_date.isoformat()}.jsonl"
    if not p.exists():
        return []
    out: list[dict] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def load_delta_mds(target_date: date) -> list[Path]:
    return sorted(DOSSIERS_DIR.glob(f"*_DELTA_{target_date.isoformat()}.md"))


def parse_delta(p: Path) -> dict:
    """Extract key facts from a delta MD frontmatter."""
    text = p.read_text(encoding="utf-8")
    out = {"path": str(p.relative_to(ROOT))}
    if text.startswith("---"):
        try:
            front_end = text.index("---", 3)
            for line in text[3:front_end].split("\n"):
                if ":" in line:
                    k, _, v = line.partition(":")
                    out[k.strip()] = v.strip()
        except ValueError:
            pass
    # Detect stance flip
    if "STANCE FLIP" in text:
        out["has_flip"] = True
    return out


def build_report(target_date: date) -> str:
    progress = load_progress(target_date)
    deltas = [parse_delta(p) for p in load_delta_mds(target_date)]

    if not progress:
        return f"# Night Shift Report — {target_date.isoformat()}\n\n_(Sem dados de progresso. Verificar `logs/night_shift_progress_{target_date.isoformat()}.jsonl`.)_\n"

    # Aggregations
    total = len(progress)
    successes = [r for r in progress if r.get("exit_code") == 0]
    failures = [r for r in progress if r.get("exit_code") != 0]
    elapsed_total = sum(r.get("elapsed_sec", 0) for r in progress)
    elapsed_avg = elapsed_total / max(total, 1)

    stance_counts = Counter()
    confidence_counts = Counter()
    seats_used = Counter()
    flags_total = 0
    evidence_total = 0
    pre_pub_flags_by_ticker: dict[str, list[str]] = {}
    flips: list[dict] = []

    for r in successes:
        snap = r.get("snapshot") or {}
        stance = snap.get("council_stance", "?")
        stance_counts[stance] += 1
        confidence_counts[snap.get("council_confidence", "?")] += 1
        for s in (snap.get("council_seats") or []):
            seats_used[s] += 1
        flags = snap.get("pre_publication_flags") or []
        flags_total += len(flags)
        evidence_total += snap.get("evidence_count", 0) or 0
        if flags:
            pre_pub_flags_by_ticker[r["ticker"]] = flags

    # Stance flips from delta MDs
    for d in deltas:
        if d.get("has_flip"):
            flips.append(d)

    # ─── Build markdown ────────────────────────────────────────────
    lines = [
        "---",
        "type: night_shift_report",
        f"date: {target_date.isoformat()}",
        f"tickers_total: {total}",
        f"tickers_success: {len(successes)}",
        f"tickers_failed: {len(failures)}",
        f"elapsed_total_min: {elapsed_total/60:.1f}",
        "tags: [night_shift, batch, council, audit]",
        "---",
        "",
        f"# 🌙 Night Shift Report — {target_date.isoformat()}",
        "",
        f"_Gerado: {datetime.now(timezone.utc).isoformat(timespec='seconds')}_",
        "",
        "## Sumário executivo",
        "",
        f"- **{total} tickers processados** ({len(successes)} ok / {len(failures)} falhas)",
        f"- **Tempo total**: {elapsed_total/60:.1f} min · Média por ticker: {elapsed_avg:.0f}s",
        f"- **Evidence entries criadas**: {evidence_total} (média {evidence_total/max(len(successes),1):.0f}/ticker)",
        f"- **Pre-publication flags emitidas**: {flags_total} (em {len(pre_pub_flags_by_ticker)} tickers)",
        f"- **Stance flips vs último run**: {len(flips)}",
        "",
        "## Distribuição de stances",
        "",
        "| Stance | Count | % |",
        "|---|---|---|",
    ]
    for stance in ("BUY", "HOLD", "AVOID", "NEEDS_DATA", "?"):
        n = stance_counts.get(stance, 0)
        if n:
            pct = n / max(len(successes), 1) * 100
            lines.append(f"| {stance} | {n} | {pct:.0f}% |")
    lines.append("")

    lines.append("| Confiança | Count |")
    lines.append("|---|---|")
    for conf in ("high", "medium", "low", "?"):
        n = confidence_counts.get(conf, 0)
        if n:
            lines.append(f"| {conf} | {n} |")
    lines.append("")

    # Per-ticker table
    lines.append("## Tabela completa")
    lines.append("")
    lines.append("| Ticker | Mkt | Stance | Conf | Seats | Flags | Evidence | Elapsed |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in sorted(progress, key=lambda x: (x.get("market", ""), x.get("ticker", ""))):
        snap = r.get("snapshot") or {}
        ticker = r.get("ticker", "?")
        market = (r.get("market") or "?").upper()
        stance = snap.get("council_stance", "?")
        emoji = {"BUY": "🟢", "HOLD": "🟡", "AVOID": "🔴", "NEEDS_DATA": "⚪"}.get(stance, "?")
        conf = snap.get("council_confidence", "?")
        seats = len(snap.get("council_seats") or [])
        flags = len(snap.get("pre_publication_flags") or [])
        evidence = snap.get("evidence_count", 0)
        elapsed = r.get("elapsed_sec", 0)
        link = f"[[{ticker}_STORY\\|{ticker}]]"
        lines.append(f"| {link} | {market} | {emoji} {stance} | {conf} | {seats} | {flags} | {evidence} | {elapsed:.0f}s |")
    lines.append("")

    # Stance flips
    if flips:
        lines.append("## ⚠️ Stance flips detectadas (vs último snapshot)")
        lines.append("")
        for f in flips:
            ticker = f.get("ticker", "?")
            prior_d = f.get("prior_date", "?")
            cur_d = f.get("current_date", "?")
            lines.append(f"- **{ticker}**: ver [[{ticker}_DELTA_{cur_d}|delta]] (prior: {prior_d})")
        lines.append("")

    # Pre-publication flags
    if pre_pub_flags_by_ticker:
        lines.append("## 🚨 Pre-publication flags por ticker")
        lines.append("")
        for tk, flags in sorted(pre_pub_flags_by_ticker.items()):
            lines.append(f"### [[{tk}_STORY|{tk}]]")
            for fl in flags:
                lines.append(f"- ⚠️ {fl}")
            lines.append("")

    # Specialists most active this night
    lines.append("## 👥 Especialistas mais convocados")
    lines.append("")
    lines.append("| Especialista | Convocações |")
    lines.append("|---|---|")
    for name, n in seats_used.most_common(15):
        lines.append(f"| [[{name}]] | {n} |")
    lines.append("")

    # Failures
    if failures:
        lines.append("## ❌ Falhas (precisam retry)")
        lines.append("")
        for r in failures:
            ticker = r.get("ticker", "?")
            err = r.get("error") or r.get("stderr_preview", "")[:200]
            lines.append(f"- **{ticker}** ({r.get('market','?').upper()}): exit={r.get('exit_code')} · {err}")
        lines.append("")

    # Tomorrow's priorities heuristic
    lines.append("## 📋 Prioridades para amanhã")
    lines.append("")
    avoid_tickers = [r["ticker"] for r in successes if (r.get("snapshot") or {}).get("council_stance") == "AVOID"]
    high_flag_tickers = [(tk, len(fl)) for tk, fl in pre_pub_flags_by_ticker.items() if len(fl) >= 2]
    high_flag_tickers.sort(key=lambda x: -x[1])

    if avoid_tickers:
        lines.append(f"### AVOID (revisar tese)")
        for tk in avoid_tickers:
            lines.append(f"- **[[{tk}_STORY|{tk}]]** — council recomendou AVOID; ler dossier e considerar trim")
        lines.append("")

    if high_flag_tickers:
        lines.append(f"### Tickers com 2+ pre-pub flags (atenção primeiro)")
        for tk, n in high_flag_tickers[:10]:
            lines.append(f"- **[[{tk}_STORY|{tk}]]** ({n} flags)")
        lines.append("")

    if failures:
        lines.append(f"### Re-run failures")
        for r in failures:
            lines.append(f"- `python -m agents.council.story {r['ticker']} --market {r.get('market','br')}`")
        lines.append("")

    # Cost summary
    lines.append("## 💰 Custos")
    lines.append("")
    lines.append(f"- **Claude tokens**: 0 (100% Ollama local)")
    lines.append(f"- **Tavily API calls**: ~{len(successes)*3} estimado (cache 7d, real menor)")
    lines.append(f"- **Hardware time**: {elapsed_total/60:.1f}min @ Ollama qwen2.5:14b RTX 5090")
    lines.append("")

    lines.append("## Documentos relacionados")
    lines.append("")
    lines.append(f"- [[../_HUB|🏛️ HUB principal]]")
    lines.append(f"- [[../agents/_MOC|👥 Empresa sintética]]")
    lines.append(f"- Storytellings em `dossiers/<TICKER>_STORY.md`")
    lines.append(f"- Snapshots JSON em `data/dossier_snapshots/<TICKER>/{target_date.isoformat()}.json`")
    lines.append("")
    lines.append("---")
    lines.append("*Night Shift autónomo · STORYT_3.0 · zero Claude tokens*")

    return "\n".join(lines)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    target_date = date.today()
    if len(sys.argv) > 1:
        target_date = date.fromisoformat(sys.argv[1])

    BIBLIOTHECA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BIBLIOTHECA_DIR / f"Night_Shift_{target_date.isoformat()}.md"
    body = build_report(target_date)
    out_path.write_text(body, encoding="utf-8")
    print(f"Night Shift Report: {out_path}")
    print(f"Length: {len(body)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
