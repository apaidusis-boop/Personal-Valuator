"""Camada 6 — Narrative Engine (chunked, deterministic-numbers).

Strategy: split the 8-act narrative into 4 chunks (2 acts each). Each chunk
gets a focused prompt with all the deterministic numbers already computed
(financial evolution table, philosophy scores, DCF). The LLM only writes the
*prose* around the numbers — never invents them.

Chunks:
  C1: Atos 1+2 — Identidade + Contexto
  C2: Atos 3+4 — Evolução Financeira + Balanço
  C3: Atos 5+6 — Múltiplos + Quality Scores
  C4: Atos 7+8 — Moat/Gestão + Veredito (DCF + Pre-Mortem + Rating)

Hard rules embedded in prompts:
  - Each Act minimum 250 words of prose (not just bullet lists)
  - Tables required where indicated
  - Cite numbers from injected data; never invent
  - Preserve council dissent in Acto 8
  - Honor pre-publication flags
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from agents._llm import ollama_call
from agents.council.coordinator import CouncilRun
from agents.council.dossier import CouncilDossier
from agents.council.evidence import EvidenceLedger, build_ledger_from_dossier
from agents.council.peer_engine import compute_ticker_fcf_yield
from agents.council.philosophy import PhilosophyScores, compute as compute_philosophy
from agents.council.valuation import (
    DCFResult,
    FinancialRow,
    compute_dcf,
    compute_net_debt,
    fetch_annual_evolution,
    get_shares_outstanding,
    render_dcf_table,
    render_evolution_table,
)

ROOT = Path(__file__).resolve().parents[2]
DOSSIERS_DIR = ROOT / "obsidian_vault" / "dossiers"

MODEL = "qwen2.5:14b-instruct-q4_K_M"
PT_MONTHS = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


# ─────────────────────────────────────────────────────────────────────
# Deterministic data prep
# ─────────────────────────────────────────────────────────────────────


def _dividend_history_annual(ticker: str, market: str, years: int = 6) -> list[dict]:
    import sqlite3
    db = ROOT / "data" / f"{market}_investments.db"
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        try:
            rows = c.execute("""
                SELECT strftime('%Y', ex_date) AS year, SUM(amount) AS total
                FROM dividends WHERE ticker = ? AND ex_date >= date('now', ?)
                GROUP BY year ORDER BY year ASC
            """, (ticker, f"-{years} years")).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []


def _compute_dgr_clean(div_hist: list[dict]) -> tuple[float | None, str]:
    """DGR removing extraordinary spikes. Returns (dgr, note).
    A year >3× median is considered to have an extraordinary — replaced by median for CAGR."""
    if len(div_hist) < 3:
        return None, "histórico insuficiente"
    full = div_hist[:-1] if len(div_hist) > 1 else div_hist
    if len(full) < 2:
        return None, "histórico insuficiente"
    amounts = [r["total"] for r in full]
    sorted_a = sorted(amounts)
    median = sorted_a[len(sorted_a) // 2]
    cleaned = [median if (median > 0 and a > 3 * median) else a for a in amounts]
    extraordinary = any(a > 3 * median for a in amounts) and median > 0
    first, last = cleaned[0], cleaned[-1]
    n = len(cleaned) - 1
    if first <= 0 or last <= 0 or n == 0:
        return None, "valores inválidos"
    try:
        dgr = (last / first) ** (1 / n) - 1
        note = "DGR limpo de extraordinária" if extraordinary else "DGR sem extraordinárias detectadas"
        return dgr, note
    except (ValueError, ZeroDivisionError):
        return None, "erro cálculo"


def _format_div_table(div_hist: list[dict]) -> str:
    if not div_hist:
        return "(sem histórico)"
    lines = ["| Ano | Total proventos (R$/ação) |", "|---|---|"]
    for r in div_hist:
        lines.append(f"| {r['year']} | {r['total']:.3f} |")
    return "\n".join(lines)


def _council_block(run: CouncilRun) -> str:
    lines = ["=== COUNCIL DEBATE (Camada 5.5) ==="]
    if run.seats:
        lines.append("Especialistas convocados (cita-os PELO NOME na narrativa):")
        for seat in run.seats:
            lines.append(f"  - {seat.employee_name} ({seat.title})")
    if run.synthesis:
        s = run.synthesis
        lines.append(f"\nVote: {s.final_stance} ({s.confidence})")
        if s.consensus_points:
            lines.append("Consensus:")
            for p in s.consensus_points:
                lines.append(f"  - {p}")
        if s.dissent_points:
            lines.append("DISSENT (preserve em Acto 8 — ATRIBUI A QUEM):")
            for p in s.dissent_points:
                lines.append(f"  - {p}")
        if s.pre_publication_flags:
            lines.append("PRE-PUB FLAGS (must surface):")
            for p in s.pre_publication_flags:
                lines.append(f"  - {p}")

    # Per-seat R1+R2 stances (so narrative can attribute)
    if run.openings or run.responses:
        lines.append("\nStances por especialista:")
        for rk, op in run.openings.items():
            seat = run.seat_by_role.get(rk)
            resp = run.responses.get(rk)
            if not seat:
                continue
            r1 = op.stance
            r2 = resp.revised_stance if resp else "—"
            lines.append(f"  - {seat.employee_name}: R1={r1} R2={r2}")
            if op.veto_signals:
                lines.append(f"    veto: {' | '.join(op.veto_signals[:2])}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Chunk prompts — each one is focused, deep, with required numbers
# ─────────────────────────────────────────────────────────────────────


SYSTEM_BASE = """És o Narrative Engine do framework STORYT_1 v5.0.

Tu transformas dados crus em prosa jornalístico-analítica densa e culta em
português europeu. Tom: sóbrio, sem hype, sem emoji.

REGRAS NÃO-NEGOCIÁVEIS:
1. NUNCA inventes números. Cada métrica TEM que vir dos dados injectados.
   Se um facto não está disponível, declara "dado não disponível" e segue.
2. Cada Acto tem MÍNIMO 250 palavras de prosa, não apenas bullets.
3. Onde for indicado, INCLUI a tabela markdown que te é entregue.
4. Mantém a estrutura `## Ato N — Título` exactamente.
"""


def _chunk1_prompt(d: CouncilDossier, web_facts: str, research_brief_text: str, macro_block: str) -> str:
    """Atos 1 (Identidade) + 2 (Contexto)."""
    return f"""{SYSTEM_BASE}

DADOS PARA ATO 1 (Identidade):
- Nome: {d.name or d.ticker}
- Ticker: {d.ticker}
- Sector: {d.sector or '?'}
- Modo: {d.modo}-{d.market.upper()}
- Held by user: {'Sim' if d.is_holding else 'Não'}

RESEARCH BRIEFING (Ulisses Navegador puxou da casa — APENAS factos que aparecem aqui ou em web facts):
{research_brief_text or '(research brief vazio)'}

WEB FACTS:
{web_facts or '(nenhum facto via Tavily)'}

GUARDRAIL ANTI-HALUCINAÇÃO:
- Se "Marcopolo" e "1949" não aparecem nem na research brief nem nos web facts, NÃO escrevas "Marcopolo, fundada em 1949"
- Se a sede da empresa NÃO está nas fontes, escreve "informação geográfica não disponível nesta análise"
- Se um analista (BTG, XP, Suno) é citado nas research brief hits, podes referenciá-lo PELO NOME e CITAR O QUE ELE DISSE textualmente
- NÃO inventes ano de fundação, cidade de sede, número de mercados, ou família controladora

CONTEXTO MACRO (Ato 2):
{macro_block}

TAREFA:
Escreve **Ato 1 — A Identidade** (250-350 palavras) e **Ato 2 — O Contexto** (250-350 palavras).

Ato 1 deve:
- Começar com a frase "Esta análise opera no Modo {d.modo}-{d.market.upper()} sob a Jurisdição {d.market.upper()}."
- Descrever o que a empresa FAZ (não inventar). Se web facts dão modelo de negócio, use.
- Identificar a "armadilha" típica que o investidor cai ao falar deste tipo de empresa
  (ex: confundir produto com negócio, marca com diferencial)
- Posicionamento competitivo se houver dados

Ato 2 deve:
- Pano de fundo macro (Selic, câmbio, ciclo) baseado em macro_block
- Como esse macro afecta especificamente este sector + esta empresa
- Mencionar qualquer mudança regulatória ou estrutural se nas web facts

Output em markdown puro, começa com "## Ato 1 — A Identidade", inclui Ato 2 a seguir.
NÃO inventes ano de fundação ou cidade de sede se não estão acima."""


def _chunk2_prompt(
    d: CouncilDossier,
    evolution_table: str,
    div_table: str,
    dgr: float | None,
    dgr_note: str,
    net_debt: float | None,
    fundamentals_view: str,
) -> str:
    """Atos 3 (Evolução Financeira) + 4 (Balanço)."""
    dgr_str = f"{dgr*100:.1f}% a.a. ({dgr_note})" if dgr is not None else f"insuficiente ({dgr_note})"
    nd_str = f"R$ {net_debt/1e9:.2f} bi (estimativa: total_debt × 0.5 — caixa não disponível directamente)" if net_debt else "não computável"

    return f"""{SYSTEM_BASE}

DADOS PARA ATO 3 (Evolução Financeira):

Tabela anual (USA EXACTAMENTE COMO ESTÁ NO ATO 3):
{evolution_table}

Histórico de dividendos:
{div_table}

DGR computado (limpo de extraordinárias): {dgr_str}

DADOS PARA ATO 4 (Balanço):
{fundamentals_view}
Net Debt estimado: {nd_str}
Custo de capital próprio (Ke) Brasil: ~18.25% (Selic 13.75% + 4.5% prémio de risco equity)

TAREFA:
Escreve **Ato 3 — A Evolução Financeira** (350-500 palavras + a tabela) e **Ato 4 — O Balanço** (300-400 palavras).

Ato 3 deve:
- Inserir a tabela anual TAL COMO TE FOI DADA (não a re-formates)
- Comentar a trajectória: receita CAGR, expansão de margens, comportamento do FCF
- Distinguir DY total reportado vs DY estrutural se há sinal de extraordinária
- Inserir tabela de dividendos
- Comentar DGR e o que isso significa para tese DRIP
- Frase obrigatória: "Lucro contábil pode esconder provisões e ajustes; FCF, não."

Ato 4 deve:
- Estrutura de capital, Net Debt/EBITDA (calcula! ND_estimado / EBITDA mais recente da tabela)
- Current Ratio + interpretação
- ROE vs Ke explícito ("ROE de X% supera o Ke de ~18% — a empresa cria valor")
- Se há ponto de atenção (despesa financeira crescente, alavancagem subindo), declara

Output markdown puro, começa com "## Ato 3 — A Evolução Financeira"."""


def _chunk3_prompt(
    d: CouncilDossier,
    fundamentals_view: str,
    peer_table: str,
    peer_source_note: str,
    quality_block: str,
) -> str:
    """Atos 5 (Múltiplos) + 6 (Quality Scores)."""
    return f"""{SYSTEM_BASE}

DADOS PARA ATO 5 (Múltiplos):
{fundamentals_view}

TABELA DE COMPARAÇÃO (USA EXACTAMENTE COMO ESTÁ):
{peer_table}

{peer_source_note}

DADOS PARA ATO 6 (Quality Scores):
{quality_block}

TAREFA:
Escreve **Ato 5 — Os Múltiplos** (350-450 palavras + a tabela acima) e **Ato 6 — Os Quality Scores** (300-400 palavras).

Ato 5 deve:
- Inserir a tabela acima TAL COMO TE FOI DADA
- Aplicar a regra das três âncoras (histórico próprio se conhecido, peers, índice)
- Distinguir DY reportado de DY estrutural (DY pode incluir extraordinária)
- Comentar sell-side recomendações se aparecem na research brief (cita por nome, não inventes)

Ato 6 deve:
- Piotroski: explicar SCORE/9, listar critérios aprovados/reprovados se temos breakdown
- Altman: declarar Z conservador E Z ajustado se temos os dois (BR), interpretar zona
- Beneish: M-Score + interpretação (clean/grey/risk)
- Ressalva técnica X2 do Altman para BR se aplicável
- Cada score com 1-2 frases de contextualização — não apenas listar

Output markdown puro, começa com "## Ato 5 — Os Múltiplos"."""


def _chunk4_prompt(
    d: CouncilDossier,
    web_facts: str,
    council_block: str,
    philosophy: PhilosophyScores,
    dcf: DCFResult,
    dcf_table: str,
) -> str:
    """Atos 7 (Moat + Gestão) + 8 (Veredito completo)."""
    phil_decl = philosophy.declare()
    phil_breakdown = ""
    for lens in ("value", "growth", "dividend", "buffett"):
        items = philosophy.breakdown.get(lens, [])
        if items:
            phil_breakdown += f"\n  {lens.upper()} score breakdown:\n"
            for item in items:
                phil_breakdown += f"    {item}\n"

    final_stance = (
        d.market and "?" or "?"
    )  # filled below from council
    council_stance = "HOLD"
    if "Vote:" in council_block:
        for line in council_block.splitlines():
            if line.strip().startswith("Vote:"):
                council_stance = line.split(":", 1)[1].strip().split(" ")[0]
                break

    rating_map = {"BUY": "Buy", "AVOID": "Sell", "HOLD": "Hold", "NEEDS_DATA": "Hold"}
    rating = rating_map.get(council_stance, "Hold")

    return f"""{SYSTEM_BASE}

DADOS PARA ATO 7 (Moat + Gestão):
WEB FACTS (use só se referem moat/gestão/insider):
{web_facts or '(sem dados web sobre insider ownership ou moat — escreve sobre moat com base só no que sabemos: histórico de dividendos {int(d.fundamentals.get("dividend_streak_years", 0))} anos, sector {d.sector}.)'}

DADOS PARA ATO 8 (Veredito):

PERFIL FILOSÓFICO COMPUTADO:
{phil_decl}
{phil_breakdown}

DCF COMPUTADO (USA EXACTAMENTE):
{dcf_table}

CONSELHO (Camada 5.5):
{council_block}

Rating final mapeado: **{rating}**

TAREFA:
Escreve **Ato 7 — O Moat e a Gestão** (300-400 palavras) e **Ato 8 — O Veredito** (500-700 palavras).

Ato 7 deve:
- Classificar moat como Wide / Narrow / None e justificar
- 5 formas de moat: custo/escala, switching costs, network effects, intangíveis, eficiência
- Insider ownership SE está nas web facts; senão declara "dado não disponível"
- Insider trades últimos 6 meses SE web facts mencionam

Ato 8 deve TER OBRIGATORIAMENTE estas secções (com sub-headers):
  ### Perfil Filosófico
  → cita as scores tal como acima
  ### O que o preço desconta
  → 1-2 parágrafos
  ### O que os fundamentos sugerem
  → 1-2 parágrafos
  ### DCF — A âncora do valor
  → INCLUI a tabela DCF tal como está acima
  ### Margem de segurança
  → cita o número computado
  ### Rating final
  → "RATING: {rating}"
  ### Pre-Mortem — Se esta tese falhar
  → mecanismo causal específico (não genérico) + gatilho observável + impacto
  → INCORPORA dissent points e pre-publication flags do council se houver
  → Atribui PELO NOME quem flagou (ex: "Valentina Prudente sinalizou que...")
  ### Horizonte
  → 24-36 meses ou faixa explícita
  ### Nota divergente do Council
  → SE houver dissent_points em council_block, transcreve aqui ATRIBUINDO POR NOME
  → Formato: "Foi este o ponto onde Mariana Macro divergiu de Diego Bancário: ..."

Output markdown puro, começa com "## Ato 7 — O Moat e a Gestão"."""


# ─────────────────────────────────────────────────────────────────────
# Macro block (deterministic, BR-only for now)
# ─────────────────────────────────────────────────────────────────────


def _macro_block(market: str) -> str:
    if market == "br":
        return (
            "Selic actual: 13.75% (Abril 2026). BCB sinalizou início de afrouxamento "
            "no 2H/2026 contingente a IPCA + contas públicas. Câmbio BRL/USD na "
            "faixa R$ 5.80-6.00. Custo de capital próprio (Ke) ~18% (Selic + 4.5% prémio). "
            "Tesouro IPCA+ 2035 oferece juro real ~6-7%."
        )
    return (
        "Fed Funds 4.25-4.50%. Treasury 10Y ~4.2%. Custo de capital próprio (Ke) ~10%. "
        "Cycle: late expansion / early softening."
    )


# ─────────────────────────────────────────────────────────────────────
# Main entry — chunked rendering
# ─────────────────────────────────────────────────────────────────────


@dataclass
class NarrativeResult:
    ticker: str
    market: str
    body_md: str
    md_path: Path
    elapsed_sec: float


def _ollama_chunk(prompt: str, max_tokens: int = 2200) -> str:
    raw = ollama_call(
        prompt,
        model=MODEL,
        max_tokens=max_tokens,
        temperature=0.3,
        seed=42,
        timeout=300,
    )
    if not raw or raw.startswith("[LLM FAILED"):
        raise RuntimeError(f"Narrative chunk failed: {raw[:200]}")
    return raw.strip()


def _format_web_facts(web_context: list[dict]) -> str:
    if not web_context:
        return ""
    lines = []
    for h in web_context:
        title = (h.get("title") or "")[:200]
        pub = h.get("published") or ""
        content = (h.get("content") or "")[:400]
        line = f"- [{pub[:10]}] {title}"
        if content:
            line += f"\n  {content}"
        lines.append(line)
    return "\n".join(lines)


def _format_fundamentals_view(d: CouncilDossier, ev: list[FinancialRow]) -> str:
    f = d.fundamentals or {}
    lines = []
    for k, lbl in [
        ("pe", "P/E"), ("pb", "P/B"), ("dy", "DY"), ("roe", "ROE"),
        ("net_debt_ebitda", "ND/EBITDA"), ("dividend_streak_years", "DivStreak"),
    ]:
        v = f.get(k)
        if v is None:
            continue
        if k in ("dy", "roe") and isinstance(v, (int, float)) and abs(v) < 5:
            lines.append(f"- {lbl}: {v*100:.2f}%")
        elif isinstance(v, (int, float)):
            lines.append(f"- {lbl}: {v:.2f}")
    if d.last_price:
        lines.append(f"- Preço actual: R$ {d.last_price:.2f} ({d.last_price_date})")
    if ev:
        latest = ev[0]
        if latest.ebitda_estimate:
            lines.append(f"- EBITDA estimado (último ano): R$ {latest.ebitda_estimate/1e9:.2f} bi")
        if latest.fcf:
            lines.append(f"- FCF (último ano): R$ {latest.fcf/1e9:.2f} bi")
        if latest.revenue:
            lines.append(f"- Receita (último ano): R$ {latest.revenue/1e9:.2f} bi")
    return "\n".join(lines)


def _format_quality_block(d: CouncilDossier) -> str:
    qs = d.quality_scores or {}
    lines = []
    if "piotroski" in qs:
        p = qs["piotroski"]
        lines.append(f"Piotroski F-Score: {p.get('f_score')}/9 ({p.get('period_end','?')})")
    if "altman" in qs:
        a = qs["altman"]
        lines.append(f"Altman Z-Score: {a.get('z'):.2f}  zona: {a.get('zone')}  conf: {a.get('confidence')}")
        if a.get("notes"):
            lines.append(f"  ressalva: {' | '.join(a['notes'][:1])}")
    if "beneish" in qs:
        b = qs["beneish"]
        lines.append(f"Beneish M-Score: {b.get('m'):.2f}  zona: {b.get('zone')}  conf: {b.get('confidence')}")
    return "\n".join(lines) or "(scores não computados — declarar inaplicabilidade)"


def render_story(run: CouncilRun, *, verbose: bool = True) -> NarrativeResult:
    import time
    t0 = time.time()

    d = run.dossier

    # ── Deterministic data prep ──────────────────────────────────
    ev = fetch_annual_evolution(d.ticker, d.market, n=5)
    div_hist = _dividend_history_annual(d.ticker, d.market, years=6)
    dgr, dgr_note = _compute_dgr_clean(div_hist)

    shares_out = get_shares_outstanding(d.ticker, d.market)
    dcf = compute_dcf(ev, d.last_price, shares_out, market=d.market)
    dcf_table = render_dcf_table(dcf)

    net_debt = compute_net_debt(d.fundamentals, ev)

    philosophy = compute_philosophy(
        {
            "fundamentals": d.fundamentals,
            "quality_scores": d.quality_scores,
            "sector": d.sector,
            "market": d.market,
            "is_holding": d.is_holding,
        },
        annual_evolution=[
            {
                "period_end": r.period_end,
                "total_revenue": r.revenue,
                "ebit": r.ebit,
                "net_income": r.net_income,
                "free_cash_flow": r.fcf,
            }
            for r in ev
        ],
        dcf={"margin_of_safety_pct": dcf.margin_of_safety_pct or 0.0},
    )

    evolution_table = render_evolution_table(ev) if ev else "| Sem dados anuais |\n|---|"
    div_table = _format_div_table(div_hist)
    web_facts = _format_web_facts(d.web_context)
    fundamentals_view = _format_fundamentals_view(d, ev)
    quality_block = _format_quality_block(d)
    macro_block = _macro_block(d.market)
    council_block = _council_block(run)

    if verbose:
        print(f"\n=== Narrative Engine (chunked): {d.market.upper()}:{d.ticker} ===")
        print(f"  Annual rows: {len(ev)} | Div years: {len(div_hist)} | DGR: {dgr_note}")
        print(f"  Philosophy: {philosophy.primary} | {philosophy.secondary}")
        if dcf.base_value:
            print(f"  DCF base: R$ {dcf.base_value:.2f}  MoS vs preço: {(dcf.margin_of_safety_pct or 0)*100:+.0f}%")

    # ── Chunk LLM calls ──────────────────────────────────────────
    chunks: list[str] = []

    # Project research brief for chunk1 (needs facts for Identidade)
    research_brief_text = ""
    if d.research_brief is not None:
        try:
            research_brief_text = d.research_brief.render_for_council(max_per_section=4)
        except Exception:
            research_brief_text = ""

    if verbose: print("  Chunk 1/4 (Atos 1-2 Identidade+Contexto)...", end=" ", flush=True)
    chunks.append(_ollama_chunk(_chunk1_prompt(d, web_facts, research_brief_text, macro_block), max_tokens=1800))
    if verbose: print("ok")

    if verbose: print("  Chunk 2/4 (Atos 3-4 Evolução+Balanço)...", end=" ", flush=True)
    chunks.append(_ollama_chunk(
        _chunk2_prompt(d, evolution_table, div_table, dgr, dgr_note, net_debt, fundamentals_view),
        max_tokens=2400,
    ))
    if verbose: print("ok")

    # Peer comparison table — REAL numbers from DB
    ticker_fcf_yield = compute_ticker_fcf_yield(d.ticker, d.market)
    ticker_metrics_for_peer = {
        "pe": (d.fundamentals or {}).get("pe"),
        "pb": (d.fundamentals or {}).get("pb"),
        "dy": (d.fundamentals or {}).get("dy"),
        "roe": (d.fundamentals or {}).get("roe"),
        "net_debt_ebitda": (d.fundamentals or {}).get("net_debt_ebitda"),
        "fcf_yield": ticker_fcf_yield,
    }
    if d.peer_benchmark is not None:
        peer_table = d.peer_benchmark.render_comparison_table(d.ticker, ticker_metrics_for_peer)
        if d.peer_benchmark.source == "db":
            peer_source_note = f"_Mediana setorial computada de {d.peer_benchmark.n_peers} peers em DB ({', '.join(d.peer_benchmark.peers_used[:6])}{'...' if len(d.peer_benchmark.peers_used) > 6 else ''})._"
        elif d.peer_benchmark.source == "mixed":
            peer_source_note = f"_Mediana parcial: {d.peer_benchmark.n_peers} peers em DB + fallback para mediana publicada onde DB é insuficiente._"
        else:
            peer_source_note = "_Sem peers suficientes em DB — usando mediana publicada para o sector como fallback._"
    else:
        peer_table = "| (peer benchmark não disponível) |\n|---|"
        peer_source_note = ""

    if verbose: print("  Chunk 3/4 (Atos 5-6 Múltiplos+Quality)...", end=" ", flush=True)
    chunks.append(_ollama_chunk(
        _chunk3_prompt(d, fundamentals_view, peer_table, peer_source_note, quality_block),
        max_tokens=2200,
    ))
    if verbose: print("ok")

    if verbose: print("  Chunk 4/4 (Atos 7-8 Moat+Veredito)...", end=" ", flush=True)
    chunks.append(_ollama_chunk(
        _chunk4_prompt(d, web_facts, council_block, philosophy, dcf, dcf_table),
        max_tokens=3000,
    ))
    if verbose: print("ok")

    # ── Assemble final document ──────────────────────────────────
    today = date.today()
    today_pt = f"{today.day} de {PT_MONTHS[today.month]} de {today.year}"

    # Specialists block — with wikilinks
    specialists_lines = []
    for seat in run.seats:
        specialists_lines.append(f"- [[{seat.employee_name}]] — _{seat.title}_")
    specialists_block = "\n".join(specialists_lines) if specialists_lines else "_(sem especialistas convocados — pipeline degraded)_"

    council_summary_table = "| Camada | Resultado |\n|---|---|\n"
    council_summary_table += f"| **1 — Data Ingestion** | yfinance ({len(ev)} anos), brapi (preço), CVM, Tavily ({len(d.web_context)} hits) |\n"
    if ev:
        latest = ev[0]
        council_summary_table += f"| **2 — Metric Engine** | Receita R$ {(latest.revenue or 0)/1e9:.1f} bi · "
        if latest.ebitda_estimate:
            council_summary_table += f"EBITDA est. R$ {latest.ebitda_estimate/1e9:.2f} bi · "
        if latest.fcf:
            council_summary_table += f"FCF R$ {latest.fcf/1e9:.2f} bi · "
        f = d.fundamentals or {}
        if f.get("roe"):
            council_summary_table += f"ROE {f['roe']*100:.0f}% · "
        if dgr is not None:
            council_summary_table += f"DGR {dgr*100:.1f}% a.a. ({dgr_note}) "
        council_summary_table += "|\n"
    council_summary_table += f"| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |\n"
    council_summary_table += f"| **4 — Scoring Engine** | "
    if d.quality_scores:
        qs_bits = []
        if "piotroski" in d.quality_scores:
            qs_bits.append(f"Piotroski {d.quality_scores['piotroski'].get('f_score')}/9")
        if "altman" in d.quality_scores:
            qs_bits.append(f"Altman Z={d.quality_scores['altman'].get('z'):.2f} ({d.quality_scores['altman'].get('zone')})")
        if "beneish" in d.quality_scores:
            qs_bits.append(f"Beneish M={d.quality_scores['beneish'].get('m'):.2f} ({d.quality_scores['beneish'].get('zone')})")
        council_summary_table += " · ".join(qs_bits)
    council_summary_table += " |\n"
    council_summary_table += f"| **5 — Classification** | Modo {d.modo}-{d.market.upper()} · {philosophy.primary}"
    if philosophy.secondary:
        council_summary_table += f" · {philosophy.secondary}"
    council_summary_table += " |\n"
    if run.synthesis:
        council_summary_table += f"| **5.5 — Council Debate** | {run.synthesis.final_stance} ({run.synthesis.confidence}) · {len(run.synthesis.dissent_points)} dissent · {len(run.synthesis.pre_publication_flags)} pre-pub flags |\n"

    header = f"""# {d.name or d.ticker} — {d.ticker}

## Análise de Investimento · Modo FULL · Jurisdição {d.market.upper()}

*{today_pt} · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo {d.modo}-{d.market.upper()} sob a Jurisdição {d.market.upper()}.**

---

## Quem analisou este ticker

{specialists_block}

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/{d.ticker}_{today.isoformat()}.md`._

---

## Camadas Silenciosas — Sumário de Execução

{council_summary_table}

---

"""

    body = "\n\n---\n\n".join(chunks)

    # Evidence ledger — Sprint 3
    ledger = build_ledger_from_dossier(d, research_brief=d.research_brief, peer_benchmark=d.peer_benchmark)
    evidence_md = ledger.render_md()
    stats = ledger.stats()
    evidence_section = f"""

---

## Evidence Ledger — fontes de cada métrica e claim

> {stats['total']} entradas · {stats['with_url']} com URL · confiança: {dict(stats['by_confidence'])}

{evidence_md}

_Cada número e claim qualitativo no storytelling acima tem origem nesta tabela. Se vires um facto sem entrada correspondente, é halucinação — flag com Tetris ou abre issue._
"""

    disclaimer = """

---

## Disclaimer

*Esta análise é instrumental de pesquisa e educação. Não constitui recomendação de investimento, não substitui consultoria profissional (CNPI, assessor regulamentado) e pode conter imprecisões nos dados. Performance passada não garante retornos futuros. O investidor é integralmente responsável por suas próprias decisões.*

---

*Framework STORYT_3.0 · Camada 6 Narrative Engine (chunked) + Camada 5.5 Council + Camada 1 Research Brief + Evidence Ledger*
"""

    elapsed = time.time() - t0

    DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = DOSSIERS_DIR / f"{d.ticker}_STORY.md"

    front = [
        "---",
        "type: storyt2_narrative",
        f"ticker: {d.ticker}",
        f"market: {d.market}",
        f"modo: {d.modo}",
        f"date: {today.isoformat()}",
        f"council_stance: {run.synthesis.final_stance if run.synthesis else 'NEEDS_DATA'}",
        f"council_confidence: {run.synthesis.confidence if run.synthesis else 'low'}",
        f"philosophy_primary: \"{philosophy.primary}\"",
        f"philosophy_secondary: \"{philosophy.secondary}\"",
        f"dcf_base: {dcf.base_value:.2f}" if dcf.base_value else "dcf_base: null",
        f"margin_of_safety: {(dcf.margin_of_safety_pct or 0):.3f}",
        f"narrative_elapsed_sec: {elapsed:.1f}",
        "tags: [storyt2, narrative, council]",
        "---",
        "",
    ]

    full = "\n".join(front) + header + body + evidence_section + disclaimer
    md_path.write_text(full, encoding="utf-8")

    # ── STORYT_3.0 Sprint 4 — versioning + delta ─────────────────
    try:
        from agents.council.versioning import (
            DossierSnapshot, archive_storytelling, emit_delta_if_prior, save_snapshot,
        )
        # Determine period_end of latest fundamentals
        period_end = (d.fundamentals or {}).get("period_end", "") or today.isoformat()
        snapshot = DossierSnapshot(
            ticker=d.ticker,
            market=d.market,
            date=today.isoformat(),
            period_end=str(period_end),
            fundamentals={k: v for k, v in (d.fundamentals or {}).items() if not isinstance(v, (dict, list))},
            quality_scores={k: dict(v) if isinstance(v, dict) else v for k, v in (d.quality_scores or {}).items()},
            philosophy={"primary": philosophy.primary, "secondary": philosophy.secondary,
                        "value": philosophy.value, "growth": philosophy.growth,
                        "dividend": philosophy.dividend, "buffett": philosophy.buffett,
                        "macro_exposure": philosophy.macro_exposure,
                        "macro_dependency": philosophy.macro_dependency},
            dcf={"base_value": dcf.base_value, "pessimistic_value": dcf.pessimistic_value,
                 "optimistic_value": dcf.optimistic_value,
                 "margin_of_safety_pct": dcf.margin_of_safety_pct,
                 "current_price": dcf.current_price},
            council_stance=run.synthesis.final_stance if run.synthesis else "NEEDS_DATA",
            council_confidence=run.synthesis.confidence if run.synthesis else "low",
            council_seats=[s.employee_name for s in run.seats],
            pre_publication_flags=list((run.synthesis.pre_publication_flags if run.synthesis else []) or []),
            consensus_points=list((run.synthesis.consensus_points if run.synthesis else []) or []),
            dissent_points=list((run.synthesis.dissent_points if run.synthesis else []) or []),
            evidence_count=stats["total"],
            research_hits_total=(d.research_brief.total_hits if d.research_brief is not None else 0),
        )
        save_snapshot(snapshot)

        # Archive the just-written latest as a versioned copy
        archive_storytelling(md_path, today)

        # Emit delta vs prior snapshot if exists
        delta_path = emit_delta_if_prior(snapshot, run_date=today)
        if delta_path and verbose:
            print(f"  Δ Delta: {delta_path.name}")
    except Exception as e:
        if verbose:
            print(f"  (versioning failed: {type(e).__name__}: {e})")

    if verbose:
        print(f"  Written: {md_path.name}  ({len(full)} chars, {elapsed:.1f}s)")

    return NarrativeResult(
        ticker=d.ticker,
        market=d.market,
        body_md=full,
        md_path=md_path,
        elapsed_sec=elapsed,
    )
