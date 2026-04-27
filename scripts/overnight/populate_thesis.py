"""Overnight job 3: Populate ## Thesis em holdings que não têm.

Strategy:
  1. Lista holdings sem ## Thesis no vault
  2. Para cada, assemble context: fundamentals + peers + sector + perpetuum state
  3. Ask Ollama Qwen 32B (maior qualidade) to generate structured thesis:
     - Core thesis (1 para)
     - Key assumptions (3-4)
     - Disconfirmation triggers (3-4)
     - Intent (DRIP/Growth/Compounder)
  4. Insert into ticker note ANTES de "Gerado por obsidian_bridge" line

Safety:
  - Only writes if vault note exists
  - Always preserves trailer footer
  - Dry-run flag available
  - Logs ALL writes to data/overnight/thesis_populated.log
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
TICKERS = ROOT / "obsidian_vault" / "tickers"
LOG = ROOT / "data" / "overnight" / "thesis_populated.log"

OLLAMA = "http://localhost:11434/api/generate"
MODEL_14B = "qwen2.5:14b-instruct-q4_K_M"
MODEL_32B = "qwen2.5:32b-instruct-q4_K_M"

THESIS_PROMPT = """You are a senior investment analyst writing a concise thesis for a long-term DRIP/value investor.

CONTEXT about the ticker:
{context}

Write a ## Thesis section in PORTUGUESE, following this EXACT structure:

## Thesis

**Core thesis ({today})**: <1 parágrafo (4-6 linhas) que explica por que esta empresa é uma boa posição long-term para um investidor Buffett/Graham. Cita números reais do contexto.>

**Key assumptions**:
1. <premissa 1 verificável>
2. <premissa 2 verificável>
3. <premissa 3 verificável>
4. <premissa 4 verificável>

**Disconfirmation triggers**:
- <red flag quantitativo 1>
- <red flag quantitativo 2>
- <red flag quantitativo 3>
- <red flag qualitativo 1>

**Intent**: <DRIP compounder|Growth|Value deep|Tactical|Defensive> — <justificação 1 linha>

RULES:
- Only Portuguese PT
- Cite actual numbers from context (DY, PE, ROE, etc.)
- Specific, not generic ("DY 8.91%" not "good DY")
- Disconfirmation triggers MUST be quantitative with thresholds
- No hedging ("talvez", "possivelmente")
- Max 300 words total

Output ONLY the ## Thesis section (no prose before/after):"""


def holdings_without_thesis() -> list[tuple[str, str, Path]]:
    """Returns [(ticker, market, path)] for holdings missing thesis."""
    out = []
    for db_name, market in [("br_investments.db", "br"), ("us_investments.db", "us")]:
        db = ROOT / "data" / db_name
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            tickers = [r[0] for r in c.execute(
                "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
            ).fetchall()]
        for t in tickers:
            path = TICKERS / f"{t}.md"
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
            if "## Thesis" in content:
                continue
            out.append((t, market, path))
    return out


def build_context(ticker: str, market: str, path: Path) -> str:
    """Aggregate fundamentals + vault frontmatter + peer stats."""
    lines = [f"Ticker: {ticker}", f"Market: {market.upper()}"]

    # Frontmatter from note (has name, sector, price, PE, etc.)
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                lines.append("VAULT METADATA:")
                for line in fm.strip().split("\n")[:25]:
                    lines.append(f"  {line.strip()}")
    except Exception:
        pass

    # Fundamentals
    db = ROOT / "data" / f"{market}_investments.db"
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        row = c.execute(
            "SELECT * FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if row:
            lines.append("\nLATEST FUNDAMENTALS:")
            for k in ("period_end", "eps", "bvps", "roe", "pe", "pb", "dy",
                     "net_debt_ebitda", "dividend_streak_years", "is_aristocrat",
                     "market_cap_usd", "current_ratio", "beta_levered", "peg_ratio"):
                v = row[k] if k in row.keys() else None
                if v is not None:
                    lines.append(f"  {k}: {v}")

        # Company info
        row_c = c.execute(
            "SELECT name, sector FROM companies WHERE ticker=?", (ticker,)
        ).fetchone()
        if row_c:
            lines.append(f"\nCOMPANY: {row_c['name']}  Sector: {row_c['sector']}")

        # Thesis_health if any
        row_t = c.execute(
            "SELECT thesis_score, run_date FROM thesis_health "
            "WHERE ticker=? AND thesis_score>=0 ORDER BY run_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if row_t:
            lines.append(f"\nPREVIOUS THESIS HEALTH: {row_t[0]}/100 on {row_t[1]}")

    return "\n".join(lines)


def generate_thesis(ctx: str, model: str = MODEL_14B) -> str | None:
    prompt = THESIS_PROMPT.replace("{context}", ctx[:3000]).replace("{today}", date.today().isoformat())
    try:
        r = requests.post(
            OLLAMA,
            json={"model": model, "prompt": prompt, "stream": False,
                  "options": {"temperature": 0.3, "num_predict": 700}},
            timeout=180,
        )
        r.raise_for_status()
        text = r.json().get("response", "").strip()
        # Ensure starts with ## Thesis
        if "## Thesis" not in text:
            return None
        # Strip anything before ## Thesis
        idx = text.find("## Thesis")
        text = text[idx:].strip()
        return text
    except Exception as e:
        return None


def insert_thesis(path: Path, thesis: str, dry_run: bool) -> bool:
    content = path.read_text(encoding="utf-8")
    marker = "*Gerado por obsidian_bridge"
    if marker in content:
        idx = content.find("---\n" + marker) if "---\n" + marker in content else content.find(marker)
        if idx < 0:
            return False
        new = content[:idx].rstrip() + "\n\n" + thesis + "\n\n" + content[idx:]
    else:
        new = content.rstrip() + "\n\n" + thesis + "\n"
    if dry_run:
        return True
    path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Limit N holdings (0=all)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default=MODEL_14B)
    args = ap.parse_args()

    LOG.parent.mkdir(parents=True, exist_ok=True)
    log = [f"=== populate_thesis run {date.today().isoformat()} (model={args.model}, dry_run={args.dry_run}) ===\n"]

    missing = holdings_without_thesis()
    if args.limit:
        missing = missing[:args.limit]

    log.append(f"holdings without thesis: {len(missing)}\n")

    ok = fail = 0
    for ticker, market, path in missing:
        ctx = build_context(ticker, market, path)
        log.append(f"\n--- {market}:{ticker}  ctx_chars={len(ctx)}")
        t0 = time.time()
        thesis = generate_thesis(ctx, model=args.model)
        elapsed = time.time() - t0
        if not thesis:
            log.append(f"  FAIL ({elapsed:.1f}s)")
            fail += 1
            continue
        if insert_thesis(path, thesis, args.dry_run):
            log.append(f"  OK ({elapsed:.1f}s, {len(thesis)} chars)")
            ok += 1
        else:
            log.append(f"  INSERT_FAIL")
            fail += 1

    log.append(f"\n=== done: ok={ok} fail={fail} ===")
    LOG.write_text("\n".join(log), encoding="utf-8")
    print(f"ok={ok} fail={fail}  log={LOG}")


if __name__ == "__main__":
    main()
