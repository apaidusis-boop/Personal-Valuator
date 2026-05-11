"""Overnight job 2: Run batch of strategic RAG queries; save answers to markdown.

Output: obsidian_vault/briefings/overnight_research_YYYY-MM-DD/*.md
  - One .md per query with answer + citations
  - index.md aggregating all

Questions cover:
  - Damodaran valuation for holdings we care about
  - Dalio macro regime checks for BR + US
  - Cross-book strategic questions
"""
from __future__ import annotations

import re
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from library.rag import ask, query_index

OUT_DIR = ROOT / "obsidian_vault" / "briefings" / f"overnight_research_{date.today().isoformat()}"


QUESTIONS = [
    # --- Dalio macro (BR + US) ---
    ("dalio_br_capital_flow", "Quais sinais Dalio usaria para antecipar crise de fluxo de capital no Brasil com Selic alta e dólar volátil?", "principles"),
    ("dalio_us_late_cycle", "Como Dalio identifica que US está em late cycle vs expansion? Indicadores concretos.", "principles"),
    ("dalio_currency_depreciation", "Quando Dalio sugere currency depreciation como policy response? Trade-offs e riscos.", "principles"),
    ("dalio_beautiful_deleveraging", "O que é Beautiful Deleveraging segundo o Dalio e como identificar quando está a ocorrer?", "principles"),
    ("dalio_bubble_detection_quantitative", "Métricas quantitativas específicas que Dalio usa para identificar bubble (não só os 4 critérios conceituais).", "principles"),
    # --- Damodaran valuation ---
    ("damodaran_high_growth_firms", "Como Damodaran valua firmas high-growth sem histórico longo de lucros? Adjustments ao DCF.", "investment_valuation"),
    ("damodaran_country_risk_br", "Como Damodaran incorpora country risk em valuation de empresa brasileira? Fórmula + exemplo.", "investment_valuation"),
    ("damodaran_banks_valuation", "Método de Damodaran para valuation de bancos (não-firm DCF clássico). Equity DCF + book value growth.", "investment_valuation"),
    ("damodaran_commodity_cyclical", "Como valuation de commodity cyclical firms (VALE-like) segundo Damodaran? Normalize earnings approach.", "investment_valuation"),
    ("damodaran_relative_valuation", "Relative valuation — quando Damodaran prefere múltiplos vs DCF? PEG ratio explained.", "investment_valuation"),
    ("damodaran_option_pricing", "Black-Scholes e real options em valuation — quando Damodaran sugere usar?", "investment_valuation"),
    ("damodaran_wacc_emerging", "Cost of Capital em emerging markets — ajustes Damodaran para BR/LATAM firms.", "investment_valuation"),
    # --- Cross-book strategic ---
    ("cross_bubble_defensive", "Se Dalio sinalizar bubble, que ajustes Damodaran faz em cost of equity para valuation defensiva?", None),
    ("cross_debt_valuation", "Como Dalio debt cycle + Damodaran valuation convergem para determinar quando empresa é over-leveraged?", None),
    ("cross_regime_risk_premium", "Regime macro do Dalio afecta equity risk premium de Damodaran? Empirical evidence.", None),
    # --- Applied to holdings specifically ---
    ("apply_br_banks_itsa4", "ITSA4 é holding de Itaú. Que framework Damodaran + Dalio sugerem para avaliar quality desta holding BR?", None),
    ("apply_tech_aapl", "AAPL com PE 33, PB 44 — Damodaran + Dalio: é bubble territory ou justified growth? Frameworks para decidir.", None),
    ("apply_commodity_vale3", "VALE3 tem PE 27 e CAGR lucros -12% 5y. Damodaran sobre commodity cyclicals: é hora de acumular ou evitar?", None),
    # --- Portfolio construction ---
    ("portfolio_drip_compound", "Para investidor DRIP long-term BR+US, que methods Dalio+Damodaran são mais relevantes para stock picking?", None),
    ("portfolio_macro_overlay", "Como combinar stock-picking value (Graham/Damodaran) com macro overlay (Dalio)? Practical weight suggestions.", None),
]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", s.lower())[:50]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = [
        "---",
        f"type: research_batch_index",
        f"date: {date.today().isoformat()}",
        f"tags: [overnight, rag, research]",
        "---",
        "",
        f"# 🔬 Overnight RAG Research Batch — {date.today().isoformat()}",
        "",
        f"**{len(QUESTIONS)} strategic queries** contra 4 livros (1704 chunks), 100% Ollama local.",
        "",
        "## Questions + answers",
        "",
    ]

    t0 = time.time()
    for qid, question, book_filter in QUESTIONS:
        t_q = time.time()
        print(f"[{qid}] {question[:70]}...")
        try:
            answer = ask(question, k=8, book_filter=book_filter)
        except Exception as e:
            answer = f"(error: {e})"
        elapsed = time.time() - t_q

        # Write to individual md
        md = [
            "---",
            f"type: rag_research",
            f"qid: {qid}",
            f"date: {date.today().isoformat()}",
            f"book_filter: {book_filter or 'all'}",
            "tags: [rag, research, overnight]",
            "---",
            "",
            f"# {qid}",
            "",
            f"**Question**: {question}",
            "",
            f"**Book filter**: `{book_filter or 'all'}`",
            f"**Generated in**: {elapsed:.1f}s by Qwen 14B + nomic-embed (100% local, 0 Claude tokens)",
            "",
            "## Answer",
            "",
            answer,
        ]
        (OUT_DIR / f"{qid}.md").write_text("\n".join(md), encoding="utf-8")

        index_lines.append(f"### [[{qid}]]")
        index_lines.append(f"{question}")
        index_lines.append("")

    total = time.time() - t0
    index_lines.append(f"\n---\n\n**Total**: {len(QUESTIONS)} queries in {total/60:.1f} min. Zero Claude tokens.\n")
    (OUT_DIR / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"\nDone. Batch saved to {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
