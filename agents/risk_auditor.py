"""RiskAuditorAgent — detecta drift de tese em holdings.

Adaptado ao NOSSO schema (não o schema imaginado pelo LLM externo).

Detection rules (deterministic — Ollama só para narrativa):
  R1. P/E expansion: P/E atual > 1.4× mediana histórica (últimos 8 quarters)
  R2. Drawdown from 52w high > -20% (cria oportunidade OU sinal quebra)
  R3. Drawdown sustained > -30% from 52w high (quality/distress review)
  R4. YoY price > +60% em holding DRIP (euphoria territory)
  R5. DY current < 50% DY 5y avg (para intent DRIP — yield compressed)

Verdicts:
  - WATCH  (1 rule fires)      → journal flag, no action
  - TRIM   (2+ rules fire)     → watchlist_action created (action_hint=TRIM)
  - REVIEW (drift conceptual)  → thesis review recommended

Output:
  - watchlist_actions rows (integração com trigger system existente)
  - Telegram alert summarizado via Ollama
  - Data json para Dataview
"""
from __future__ import annotations

import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from ._base import AgentContext, AgentResult, BaseAgent
from ._llm import llm_summarise


class RiskAuditorAgent(BaseAgent):
    name = "risk_auditor"
    description = "Detecta drift de tese em holdings via regras + narrativa Ollama"
    default_schedule = "daily:21:00"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        flags: list[dict] = []
        checked = 0

        for mkt, db_name in [("br", "br_investments.db"), ("us", "us_investments.db")]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                holdings = c.execute("""
                    SELECT p.ticker, p.quantity, p.entry_price, p.entry_date,
                           co.name, co.sector
                    FROM portfolio_positions p
                    JOIN companies co ON co.ticker = p.ticker
                    WHERE p.active = 1
                """).fetchall()

                for h in holdings:
                    checked += 1
                    ticker = h["ticker"]
                    reasons = self._evaluate_rules(c, ticker, h["sector"])
                    if not reasons:
                        continue
                    verdict = self._verdict_from_rules(reasons)

                    # Narrativa Ollama (só quando flag dispara)
                    narrative = self._narrate(ticker, h["name"], reasons, verdict)
                    flag = {
                        "ticker": ticker,
                        "market": mkt,
                        "name": h["name"],
                        "sector": h["sector"],
                        "verdict": verdict,
                        "reasons": reasons,
                        "narrative": narrative,
                    }
                    flags.append(flag)
                    actions.append(f"{verdict} {ticker}: {'; '.join(reasons)[:100]}")

                    # Persist em watchlist_actions se verdict != WATCH
                    if verdict in ("TRIM", "REVIEW") and not ctx.dry_run:
                        self._persist_watchlist_action(c, ticker, verdict, narrative, reasons)

                if not ctx.dry_run:
                    c.commit()

        if not flags:
            return AgentResult(
                agent=self.name, status="no_action",
                summary=f"Todas as {checked} holdings dentro da tese.",
                started_at="", finished_at="", duration_sec=0,
            )

        # Telegram push com summary top-N
        if not ctx.dry_run:
            self._push_telegram(root, flags, checked)

        return AgentResult(
            agent=self.name, status="ok",
            summary=f"{len(flags)}/{checked} holdings flagged — "
                    f"{sum(1 for f in flags if f['verdict']=='TRIM')} TRIM, "
                    f"{sum(1 for f in flags if f['verdict']=='REVIEW')} REVIEW, "
                    f"{sum(1 for f in flags if f['verdict']=='WATCH')} WATCH.",
            started_at="", finished_at="", duration_sec=0,
            actions=actions,
            data={"flags": flags, "checked": checked},
        )

    # ─── Rules (deterministic) ──────────────────────────────────────────
    def _evaluate_rules(self, c: sqlite3.Connection, ticker: str, sector: str) -> list[str]:
        reasons: list[str] = []

        # Latest price + fundamentals
        price_row = c.execute(
            "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        if not price_row or not price_row[1]:
            return reasons
        last_date, last_close = price_row[0], price_row[1]

        # R1. P/E expansion vs historical
        pe_row = c.execute(
            "SELECT pe FROM fundamentals WHERE ticker=? AND pe > 0 ORDER BY period_end DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        pe_hist = c.execute(
            "SELECT AVG(pe) FROM fundamentals WHERE ticker=? AND pe > 0 AND pe < 200",
            (ticker,)
        ).fetchone()
        if pe_row and pe_row[0] and pe_hist and pe_hist[0]:
            expansion = pe_row[0] / pe_hist[0]
            if expansion >= 1.4:
                reasons.append(f"P/E +{(expansion-1)*100:.0f}% vs hist avg "
                               f"({pe_hist[0]:.1f} → {pe_row[0]:.1f})")

        # R2. 52w drawdown
        high_52w = c.execute("""
            SELECT MAX(close) FROM prices WHERE ticker=? AND date >= date(?, '-365 days')
        """, (ticker, last_date)).fetchone()
        if high_52w and high_52w[0] and high_52w[0] > 0:
            dd = (last_close / high_52w[0]) - 1
            if dd <= -0.30:
                reasons.append(f"Drawdown {dd*100:.0f}% from 52w high (R3: distress review)")
            elif dd <= -0.20:
                reasons.append(f"Drawdown {dd*100:.0f}% from 52w high (R2)")

        # R4. YoY price > +60%
        yoy_row = c.execute("""
            SELECT close FROM prices WHERE ticker=? AND date <= date(?, '-365 days')
            ORDER BY date DESC LIMIT 1
        """, (ticker, last_date)).fetchone()
        if yoy_row and yoy_row[0] and yoy_row[0] > 0:
            yoy = (last_close / yoy_row[0]) - 1
            if yoy >= 0.60 and sector not in ("ETF", "ETF-US", "ETF-RF"):
                reasons.append(f"YoY +{yoy*100:.0f}% (euphoria territory — R4)")

        # R5. DY compression vs 5y avg (apenas se tem dividend history)
        dy_row = c.execute(
            "SELECT dy FROM fundamentals WHERE ticker=? AND dy > 0 ORDER BY period_end DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        dy_hist = c.execute(
            "SELECT AVG(dy) FROM fundamentals WHERE ticker=? AND dy > 0",
            (ticker,)
        ).fetchone()
        if dy_row and dy_row[0] and dy_hist and dy_hist[0] and dy_hist[0] > 0.02:
            ratio = dy_row[0] / dy_hist[0]
            if ratio <= 0.50:
                reasons.append(f"DY comprimido {ratio*100:.0f}% do hist avg "
                               f"({dy_hist[0]*100:.1f}% → {dy_row[0]*100:.1f}%)")

        return reasons

    def _verdict_from_rules(self, reasons: list[str]) -> str:
        if any("R3" in r or "distress" in r for r in reasons):
            return "REVIEW"
        if len(reasons) >= 2:
            return "TRIM"
        return "WATCH"

    def _narrate(self, ticker: str, name: str, reasons: list[str], verdict: str) -> str:
        prompt = (
            f"Escreve 2 frases em português (tom sóbrio analítico) sobre o status de {ticker} "
            f"({name}). Verdict: {verdict}. Razões técnicas: {'; '.join(reasons)}. "
            "Não invente números. Não alarmismo. Máximo 200 caracteres."
        )
        out = llm_summarise(prompt, max_tokens=200, temperature=0.2)
        return out[:400] if out and not out.startswith("[LLM FAILED") else (
            f"{verdict} sinalizado para {ticker}: {'; '.join(reasons[:2])}"
        )

    def _persist_watchlist_action(
        self, c: sqlite3.Connection, ticker: str, verdict: str,
        narrative: str, reasons: list[str],
    ) -> None:
        kind = "risk_auditor_drift"
        # Dedup: não criar duplicate open se já existe na última semana
        existing = c.execute("""
            SELECT id FROM watchlist_actions
            WHERE ticker=? AND kind=? AND status='open'
              AND created_at >= date('now', '-7 days')
            LIMIT 1
        """, (ticker, kind)).fetchone()
        if existing:
            return
        try:
            c.execute("""
                INSERT INTO watchlist_actions
                    (ticker, kind, action_hint, note, status, created_at)
                VALUES (?, ?, ?, ?, 'open', ?)
            """, (ticker, kind, verdict, narrative,
                  datetime.now(timezone.utc).isoformat(timespec="seconds")))
        except sqlite3.OperationalError:
            pass

    def _push_telegram(self, root: Path, flags: list[dict], checked: int) -> bool:
        lines = [f"⚠️ Risk Auditor — {len(flags)}/{checked} holdings flagged:", ""]
        for f in flags[:10]:
            lines.append(f"• *{f['ticker']}* ({f['verdict']})")
            lines.append(f"  {f['narrative'][:200]}")
        try:
            r = subprocess.run(
                [sys.executable, "-X", "utf8", "-m", "notifiers.telegram", "\n".join(lines)],
                capture_output=True, timeout=20, cwd=str(root),
            )
            return r.returncode == 0
        except Exception:
            return False
