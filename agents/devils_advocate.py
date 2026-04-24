"""DevilsAdvocateAgent — anti-confirmation-bias agent.

Para cada holding onde o sentimento agregado dos analyst_insights recentes
é majoritariamente positivo (>= 60% bull ou neutral-bull), este agent:

  1. Busca bear insights existentes no DB (stance='bear' OR kind='risk')
     — muitas vezes já foram ingeridos mas ficaram soterrados sob o bull noise.
  2. Se não há bear insights suficientes, pede ao Ollama para gerar uma
     "bear thesis" contrafactual baseada em:
       - Current fundamentals (high P/E, debt/ebitda, drawdown position)
       - Wiki sector context (se aplicável)
       - Known weaknesses (via sector/cycle wiki notes)
  3. Injecta secção "## ⚠️ Bear case (Devil's Advocate)" em
     wiki/holdings/<TICKER>.md — idempotent (replaces se já existe).

Esta versão NÃO faz web search (TOS grey + infra não existe). Usa só:
  - DB analyst_insights que já temos
  - Ollama para síntese contrafactual local
  - Wiki thesis existente para contextualização
"""
from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta, timezone

from ._base import AgentContext, AgentResult, BaseAgent
from ._llm import llm_summarise


BEAR_SECTION_TITLE = "## ⚠️ Bear case (Devil's Advocate)"
BEGIN_MARKER = "<!-- DEVILS_ADVOCATE:BEGIN -->"
END_MARKER = "<!-- DEVILS_ADVOCATE:END -->"


class DevilsAdvocateAgent(BaseAgent):
    name = "devils_advocate"
    description = "Injecta bear case em holdings com sentimento muito positivo"
    default_schedule = "weekly:wed:10:00"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        written: list[str] = []
        skipped: list[str] = []

        # 1. Find holdings com sentiment bullish nos últimos 60 dias
        candidates = self._bullish_holdings(root, days=60, min_insights=3, bull_ratio=0.6)
        if not candidates:
            return AgentResult(
                agent=self.name, status="no_action",
                summary="Nenhuma holding com sentimento positivo suficiente para devil's advocate.",
                started_at="", finished_at="", duration_sec=0,
            )

        vault = Path(ctx.config.get("vault") or (root / "obsidian_vault"))
        holdings_dir = vault / "wiki" / "holdings"

        for ticker, meta in candidates.items():
            thesis_path = holdings_dir / f"{ticker}.md"
            if not thesis_path.exists():
                skipped.append(f"{ticker} (no thesis note)")
                continue

            # 2. Existing bear insights
            bears = self._existing_bears(root, ticker, days=90)
            # 3. Fundamentals context
            fund_ctx = self._fundamentals_context(root, ticker)
            # 4. Ollama generates bear case
            bear_md = self._generate_bear_case(ticker, meta, bears, fund_ctx)
            if not bear_md:
                skipped.append(f"{ticker} (Ollama failed)")
                continue

            # 5. Inject/replace section in thesis note
            if not ctx.dry_run:
                self._inject_section(thesis_path, bear_md)
                written.append(ticker)
            actions.append(f"bear case gerado para {ticker} ({meta['bull']}/{meta['total']} bull)")

        return AgentResult(
            agent=self.name,
            status="ok" if written else "no_action",
            summary=f"{len(written)} bear cases injectados "
                    f"({len(candidates)} candidatos, {len(skipped)} skipped).",
            started_at="", finished_at="", duration_sec=0,
            actions=actions,
            data={"written": written, "skipped": skipped, "candidates": list(candidates.keys())},
        )

    # ─── Helpers ─────────────────────────────────────────────────────────

    def _bullish_holdings(
        self, root: Path, days: int, min_insights: int, bull_ratio: float,
    ) -> dict[str, dict]:
        """Returns {ticker: {bull, bear, neutral, total, claims}}."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")
        tickers: dict[str, dict] = {}
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                # apenas holdings
                rows = c.execute("""
                    SELECT i.ticker, i.stance, i.claim
                    FROM analyst_insights i
                    JOIN companies co ON co.ticker = i.ticker
                    JOIN portfolio_positions p ON p.ticker = i.ticker AND p.active = 1
                    WHERE i.created_at >= ?
                """, (cutoff,)).fetchall()
                for r in rows:
                    t = r["ticker"]
                    tickers.setdefault(t, {"bull": 0, "bear": 0, "neutral": 0, "total": 0, "claims": []})
                    tickers[t]["total"] += 1
                    stance = (r["stance"] or "").lower()
                    if stance in ("bull", "bear", "neutral"):
                        tickers[t][stance] += 1
                    tickers[t]["claims"].append(r["claim"][:200])
        # Filter: min insights + bull_ratio
        return {
            t: m for t, m in tickers.items()
            if m["total"] >= min_insights and (m["bull"] / m["total"]) >= bull_ratio
        }

    def _existing_bears(self, root: Path, ticker: str, days: int = 90) -> list[dict]:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")
        out: list[dict] = []
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                try:
                    rows = c.execute("""
                        SELECT r.source, i.claim, i.kind, i.confidence
                        FROM analyst_insights i JOIN analyst_reports r ON r.id = i.report_id
                        WHERE i.ticker = ? AND (i.stance = 'bear' OR i.kind = 'risk')
                          AND i.created_at >= ?
                        ORDER BY i.confidence DESC LIMIT 5
                    """, (ticker, cutoff)).fetchall()
                    out.extend(dict(r) for r in rows)
                except sqlite3.OperationalError:
                    pass
        return out

    def _fundamentals_context(self, root: Path, ticker: str) -> dict:
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                row = c.execute("""
                    SELECT pe, pb, dy, roe, net_debt_ebitda, dividend_streak_years
                    FROM fundamentals WHERE ticker = ?
                    ORDER BY period_end DESC LIMIT 1
                """, (ticker,)).fetchone()
                if row:
                    return dict(row)
        return {}

    def _generate_bear_case(
        self, ticker: str, meta: dict, bears: list[dict], fund: dict,
    ) -> str | None:
        # Materializa contexto
        bear_ctx = "\n".join(
            f"- [{b['source']}] ({b.get('kind', 'risk')}): {b['claim'][:250]}"
            for b in bears
        ) or "- (nenhum bear insight recente no DB)"

        fund_ctx = (
            f"P/E: {fund.get('pe')} · P/B: {fund.get('pb')} · "
            f"DY: {fund.get('dy')} · ROE: {fund.get('roe')} · "
            f"ND/EBITDA: {fund.get('net_debt_ebitda')} · "
            f"Streak: {fund.get('dividend_streak_years')} years"
        ) if fund else "(sem fundamentals recentes)"

        system = (
            "És o 'Devil's Advocate' — um analista bearish que procura sistematicamente "
            "os riscos que o consensus está a ignorar. Tom: sóbrio, jornalístico, SEM alarmismo. "
            "Produz em PT BR. Nunca inventes números; usa só o que está nos dados."
        )
        prompt = f"""Ticker: {ticker}
Sentimento consensus (últimos 60d): {meta['bull']} bull / {meta['bear']} bear / {meta['neutral']} neutral ({meta['total']} insights).

Fundamentals actuais:
{fund_ctx}

Bear insights existentes no DB:
{bear_ctx}

Escreve uma secção "Bear case" estruturada em markdown com:
- **Risco estrutural** (1 parágrafo curto — o maior risco que o consensus não está a precificar)
- **Invalidation signals** (3-5 bullets — o que teria que acontecer para a tese bull quebrar)
- **Peer / sector headwinds** (2-3 bullets — vento contra macro/sectorial)
- **Sizing suggestion** (1 frase — se reduzir, por quanto, porquê)

Limite: ~250 palavras. Factual, não speculative. Se os dados não sustentam bear case forte, diz isso explicitamente no final."""

        response = llm_summarise(prompt, system=system, max_tokens=800, temperature=0.4)
        if not response or response.startswith("[LLM FAILED"):
            return None
        return response.strip()

    def _inject_section(self, path: Path, bear_md: str) -> None:
        """Replace/insert bear section idempotente entre markers."""
        text = path.read_text(encoding="utf-8")
        stamp = f"_Gerado: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
        block = f"{BEGIN_MARKER}\n{BEAR_SECTION_TITLE}\n\n{stamp}{bear_md}\n{END_MARKER}"
        pattern = re.compile(
            re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER),
            re.DOTALL,
        )
        if pattern.search(text):
            new = pattern.sub(block, text)
        else:
            # inserir ANTES de "## Related" OR "<!-- LIVE_SNAPSHOT" OR EOF
            for anchor in ["<!-- LIVE_SNAPSHOT:BEGIN -->", "\n## Related", "\n## Memory refs"]:
                idx = text.find(anchor)
                if idx >= 0:
                    new = text[:idx] + "\n" + block + "\n\n" + text[idx:]
                    break
            else:
                new = text.rstrip() + "\n\n" + block + "\n"
        path.write_text(new, encoding="utf-8")
