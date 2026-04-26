"""Information power audit — what we know vs gaps + actionable signals."""
from __future__ import annotations
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT/"data"/"br_investments.db", "us": ROOT/"data"/"us_investments.db"}
VAULT = ROOT/"obsidian_vault"

print("="*72)
print("INFORMATION POWER AUDIT — 2026-04-26")
print("="*72)

# 1. Vault assets
print("\n[1] VAULT ASSETS")
v = VAULT/"tickers"
print(f"  dossiers (research_dossie type): {len(list(v.glob('*_DOSSIE.md')))}")
print(f"  IC debates (synthetic IC verdict): {len(list(v.glob('*_IC_DEBATE.md')))}")
print(f"  ticker wiki notes (vault thesis): {len([p for p in v.glob('*.md') if not p.stem.endswith(('_DOSSIE','_IC_DEBATE'))])}")
print(f"  sectors notes: {len(list((VAULT/'sectors').glob('*.md')))}")
print(f"  analyst reports: {len(list((VAULT/'analysts').glob('*.md')))}")

# 2. DB inventory
for mkt, db in DBS.items():
    print(f"\n[2.{mkt}] {mkt.upper()} DB SIGNALS")
    with sqlite3.connect(db) as c:
        tabs = {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        h_n = c.execute("SELECT COUNT(*) FROM companies WHERE is_holding=1").fetchone()[0]
        u_n = c.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
        print(f"  universe: {u_n} companies (holdings: {h_n})")
        if "fundamentals" in tabs:
            f_n = c.execute("SELECT COUNT(DISTINCT ticker) FROM fundamentals").fetchone()[0]
            print(f"  fundamentals: {f_n} tickers ({f_n/u_n*100:.0f}% coverage)")
        if "prices" in tabs:
            p_n = c.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
            t_n = c.execute("SELECT COUNT(DISTINCT ticker) FROM prices").fetchone()[0]
            print(f"  prices: {p_n:,} rows / {t_n} tickers")
        if "events" in tabs:
            ev30 = c.execute("SELECT COUNT(*) FROM events WHERE event_date >= date('now','-30 days')").fetchone()[0]
            print(f"  events (30d): {ev30}")
        if "paper_trade_signals" in tabs:
            po = c.execute("SELECT COUNT(*) FROM paper_trade_signals WHERE status='open'").fetchone()[0]
            pc = c.execute("SELECT COUNT(*) FROM paper_trade_signals WHERE status='closed'").fetchone()[0]
            print(f"  paper_trade: {po} open, {pc} closed")
        if "analyst_reports" in tabs:
            ar = c.execute("SELECT COUNT(*) FROM analyst_reports").fetchone()[0]
            print(f"  analyst_reports (Suno/XP/BTG): {ar}")
        if "analyst_insights" in tabs:
            ai = c.execute("SELECT COUNT(*) FROM analyst_insights").fetchone()[0]
            print(f"  analyst_insights extracted: {ai}")

# 3. Conviction (BR DB has unified BR+US)
print("\n[3] CONVICTION (BR DB unified)")
with sqlite3.connect(DBS["br"]) as c:
    rows = c.execute("SELECT ticker, composite_score FROM conviction_scores ORDER BY composite_score DESC LIMIT 15").fetchall()
    print("  top 15:")
    for t, s in rows:
        bar = "█"*(s//5)
        print(f"    {t:>7}: {s:>3} {bar}")

    n_high = c.execute("SELECT COUNT(*) FROM conviction_scores WHERE composite_score >= 75").fetchone()[0]
    n_med = c.execute("SELECT COUNT(*) FROM conviction_scores WHERE composite_score BETWEEN 50 AND 74").fetchone()[0]
    n_low = c.execute("SELECT COUNT(*) FROM conviction_scores WHERE composite_score < 50").fetchone()[0]
    print(f"  distribution: high(≥75)={n_high}, med(50-74)={n_med}, low(<50)={n_low}")

# 4. Bank-specific (BACEN)
print("\n[4] BANK BACEN COVERAGE")
with sqlite3.connect(DBS["br"]) as c:
    rows = c.execute("""
        SELECT ticker, COUNT(*) n_q, MIN(period_end) since, MAX(period_end) latest,
               (SELECT basel_ratio FROM bank_quarterly_history b2
                WHERE b2.ticker=b1.ticker AND b2.basel_ratio IS NOT NULL
                ORDER BY period_end DESC LIMIT 1) latest_basel
        FROM bank_quarterly_history b1
        WHERE basel_ratio IS NOT NULL
        GROUP BY ticker ORDER BY ticker
    """).fetchall()
    for t, n, since, latest, basel in rows:
        print(f"  {t}: {n}q from {since} to {latest}, latest Basel {basel*100:.2f}%")

# 5. CVM quarterly (Phase Y/J coverage)
print("\n[5] CVM QUARTERLY HISTORY (Phase Y)")
with sqlite3.connect(DBS["br"]) as c:
    rows = c.execute("""
        SELECT ticker, COUNT(*) n_q
        FROM quarterly_history
        GROUP BY ticker ORDER BY n_q DESC
    """).fetchall()
    print(f"  {len(rows)} tickers covered:")
    for t, n in rows[:15]:
        print(f"    {t}: {n}q")
    if len(rows) > 15:
        print(f"    ... +{len(rows)-15} more")

# 6. IC verdicts split (sample top tickers)
print("\n[6] IC VERDICTS DISTRIBUTION (sample)")
import re
verdicts = {"BUY": [], "HOLD": [], "AVOID": [], "MIXED": [], "OTHER": []}
for p in sorted(VAULT.glob("tickers/*_IC_DEBATE.md")):
    text = p.read_text(encoding="utf-8", errors="ignore")[:1000]
    m = re.search(r"committee_verdict:\s*(\w+)", text)
    if m:
        v = m.group(1).upper()
        v = v if v in verdicts else "OTHER"
        verdicts[v].append(p.stem.replace("_IC_DEBATE",""))
for v, lst in verdicts.items():
    print(f"  {v}: {len(lst)} tickers")
print(f"  AVOID picks (top 10): {verdicts['AVOID'][:10]}")
print(f"  BUY picks (top 10): {verdicts['BUY'][:10]}")

# 7. Open events / recent material news
print("\n[7] RECENT EVENTS (30d)")
for mkt, db in DBS.items():
    with sqlite3.connect(db) as c:
        rows = c.execute("""
            SELECT kind, COUNT(*) n FROM events
            WHERE event_date >= date('now','-30 days')
            GROUP BY kind ORDER BY n DESC LIMIT 5
        """).fetchall()
        if rows:
            print(f"  {mkt}: " + ", ".join(f"{k}={n}" for k,n in rows))

# 8. Gaps & flags
print("\n[8] GAPS & ACTIONABLE FLAGS")
gaps = []
with sqlite3.connect(DBS["br"]) as c:
    pc = c.execute("SELECT COUNT(*) FROM paper_trade_signals WHERE status='closed'").fetchone()[0]
    if pc == 0:
        gaps.append("BR paper_trade_close.py never ran — 780 signals stuck open")
with sqlite3.connect(DBS["us"]) as c:
    pc = c.execute("SELECT COUNT(*) FROM paper_trade_signals WHERE status='closed'").fetchone()[0]
    if pc == 0:
        gaps.append("US paper_trade_close.py never ran — 956 signals stuck open")
# Banks coverage
with sqlite3.connect(DBS["br"]) as c:
    bank_companies = c.execute("SELECT ticker FROM companies WHERE sector='Banks'").fetchall()
    bank_with_basel = c.execute("SELECT DISTINCT ticker FROM bank_quarterly_history WHERE basel_ratio IS NOT NULL").fetchall()
    missing = set(t[0] for t in bank_companies) - set(t[0] for t in bank_with_basel)
    if missing:
        gaps.append(f"Bank BACEN missing for: {sorted(missing)}")
# IC vs analyst conflict (HGRU11 case)
gaps.append("HGRU11 IC=AVOID 100% vs Suno=BUY R$140 — needs human read")
# RDOR3 sustainability flag
gaps.append("RDOR3 DY 11% likely one-off post-Sul Am — verify next earnings")
# RBRY11
gaps.append("RBRY11 DY 15% + IC MIXED low — value trap candidate")
# MCRF11 missing data
gaps.append("MCRF11 missing fundamentals → run refresh_ticker.py")
for g in gaps:
    print(f"  ▸ {g}")

print("\n"+"="*72)
print("DONE")
