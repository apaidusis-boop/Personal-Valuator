"""Bibliotheca Knowledge Cards — synth respostas conceptuais via RAG.

Para cada pergunta-chave da filosofia de investimento, corre `library.rag ask`
e salva como nota persistente em `obsidian_vault/Bibliotheca/Knowledge/<slug>.md`.

Cada card vira referência durável (não regenera todos os dias) que pode ser
linkada de Glossary + dossiers para deep-context.

Uso:
    python scripts/build_knowledge_cards.py            # gera todos os cards faltantes
    python scripts/build_knowledge_cards.py --force    # regenera tudo
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "obsidian_vault" / "Bibliotheca" / "Knowledge"

# Curated conceptual questions — cada uma vira um card persistente.
CARDS: list[dict] = [
    {
        "slug": "buffett_moat_detection",
        "title": "Buffett Moat: como detectar vantagem competitiva sustentável",
        "category": "philosophy",
        "question": "Como o Buffett define moat e quais são os 5 sinais práticos para detectar uma empresa com wide moat?",
        "k": 6,
    },
    {
        "slug": "graham_margin_of_safety",
        "title": "Graham Margem de Segurança: princípio fundamental",
        "category": "philosophy",
        "question": "Qual o princípio da margem de segurança segundo Graham? Como aplicar quantitativamente vs qualitativamente?",
        "k": 6,
    },
    {
        "slug": "drip_vs_cash_dividends",
        "title": "DRIP vs Cash Dividend: quando cada faz sentido",
        "category": "strategy",
        "question": "Quando reinvestir dividendos via DRIP é superior a receber em cash? Liste 4 critérios práticos com exemplos.",
        "k": 6,
    },
    {
        "slug": "dalio_bubble_framework",
        "title": "Dalio Bubble Framework: 4 critérios para identificar bolha",
        "category": "macro",
        "question": "Quais os 4 critérios do Dalio para identificar uma bolha de mercado? Como aplicar à equity actual?",
        "k": 8,
    },
    {
        "slug": "dalio_debt_crisis_signals",
        "title": "Dalio Debt Crisis: sinais precoces antes de uma crise de dívida",
        "category": "macro",
        "question": "Quais sinais antecedem uma crise de dívida segundo o framework do Dalio em 'Big Debt Crises'? Liste 5 indicadores observáveis.",
        "k": 8,
    },
    {
        "slug": "dcf_practical_pitfalls",
        "title": "DCF prático: quando faz sentido e quando engana",
        "category": "valuation",
        "question": "Quando um DCF é robusto vs quando é apenas teatro de assumptions? Quais empresas merecem DCF e quais devem usar outro método?",
        "k": 6,
    },
    {
        "slug": "bank_screening_checklist",
        "title": "Bank Screening: checklist antes de comprar um banco",
        "category": "sector",
        "question": "Quais os 6 sinais críticos para avaliar um banco antes de comprar (Basel/CET1/NPL/ROE/payout/franchise)? Por que P/E e P/B isolados são insuficientes?",
        "k": 6,
    },
    {
        "slug": "fii_paper_vs_brick",
        "title": "FII Papel vs Tijolo: quando preferir cada",
        "category": "fii",
        "question": "Diferenças estruturais entre FIIs de papel (CRI) e tijolo (imóveis físicos)? Quando preferir cada num ciclo de Selic alta vs queda?",
        "k": 6,
    },
    {
        "slug": "aristocrat_quality_signal",
        "title": "Dividend Aristocrat: o que sustenta o status durante 25y+",
        "category": "income",
        "question": "Quais características operacionais permitem a uma empresa manter status de Dividend Aristocrat por 25 anos? Como detectar erosão antes do corte?",
        "k": 6,
    },
    {
        "slug": "variant_perception_edge",
        "title": "Variant Perception: como identificar onde divergimos do consenso com edge real",
        "category": "process",
        "question": "Como aplicar variant perception scanning de forma rigorosa? Como distinguir edge real de viés contrarian sem evidência?",
        "k": 6,
    },
    {
        "slug": "value_trap_signals",
        "title": "Value Trap: como evitar comprar barato pelas razões erradas",
        "category": "process",
        "question": "Quais sinais distinguem uma empresa value (barata por razão temporária) de uma value trap (barata por declínio estrutural)? Liste 5 critérios discriminantes.",
        "k": 6,
    },
    {
        "slug": "drip_compounding_math",
        "title": "DRIP Compounding: a matemática real ao longo de 10-20 anos",
        "category": "strategy",
        "question": "Como o DRIP compounding funciona matematicamente em 10-20 anos? Que premissas são fundamentais e que sensibilidades quebram a tese?",
        "k": 6,
    },
]


def card_exists(slug: str) -> bool:
    return (KNOWLEDGE / f"{slug}.md").exists()


def gen_card(card: dict, timeout: int = 180) -> str | None:
    """Calls library.rag ask + builds frontmatter + body."""
    import subprocess
    cmd = [sys.executable, "-m", "library.rag", "ask",
           card["question"], "--k", str(card["k"])]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8")
        if r.returncode != 0:
            return None
        # Output has chunks listed + final answer. We want clean version.
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"  err: {e}")
        return None


def render_card(card: dict, raw_output: str) -> str:
    """Build markdown with frontmatter + question + answer + raw context."""
    lines = [
        "---",
        f"type: knowledge_card",
        f"slug: {card['slug']}",
        f"title: {card['title']}",
        f"category: {card['category']}",
        f"date: {date.today().isoformat()}",
        f"source: library.rag (Ollama Qwen 14B + nomic-embed)",
        "tags: [bibliotheca, knowledge_card, " + card["category"] + "]",
        "---",
        "",
        f"# 🧠 {card['title']}",
        "",
        f"> Categoria: **{card['category']}**. Synth via RAG sobre books + clippings. "
        f"Cross-links: [[Bibliotheca/_Index]] · [[Glossary/_Index]]",
        "",
        "## Pergunta",
        "",
        f"_{card['question']}_",
        "",
        "## Resposta (synth Ollama Qwen 14B)",
        "",
        raw_output,
        "",
        "---",
        f"*Auto-build via `scripts/build_knowledge_cards.py` em "
        f"{date.today().isoformat()}. Para regenerar: `--force`.*",
    ]
    return "\n".join(lines) + "\n"


def render_index(cards: list[dict]) -> str:
    by_cat: dict[str, list[dict]] = {}
    for c in cards:
        if card_exists(c["slug"]):
            by_cat.setdefault(c["category"], []).append(c)

    lines = [
        "---",
        "type: knowledge_index",
        f"date: {date.today().isoformat()}",
        f"cards: {sum(len(v) for v in by_cat.values())}",
        "tags: [bibliotheca, knowledge_index]",
        "---",
        "",
        "# 🧠 Bibliotheca Knowledge — Índice",
        "",
        "> Cards conceptuais sintetizados via RAG sobre books + clippings (Ollama local). "
        "Cada card é resposta durável a uma pergunta-chave da filosofia investimento.",
        "",
    ]
    for cat in sorted(by_cat):
        lines += [f"## {cat}", ""]
        for c in by_cat[cat]:
            lines.append(f"- [[Bibliotheca/Knowledge/{c['slug']}|{c['title']}]]")
        lines.append("")
    lines += [
        "## Como expandir",
        "",
        "1. Editar `scripts/build_knowledge_cards.py` `CARDS` list",
        "2. `python scripts/build_knowledge_cards.py` (gera só os faltantes)",
        "3. `--force` regenera todos (custo: ~30s × N cards via Ollama)",
        "",
        "---",
        f"*Auto-build em {date.today().isoformat()}.*",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="regenerar tudo")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    KNOWLEDGE.mkdir(parents=True, exist_ok=True)

    skipped = generated = errors = 0
    for card in CARDS:
        if not args.force and card_exists(card["slug"]):
            skipped += 1
            if not args.quiet:
                print(f"  skip   {card['slug']} (exists)")
            continue
        if not args.quiet:
            print(f"  gen    {card['slug']} ... ", end="", flush=True)
        out = gen_card(card)
        if not out:
            errors += 1
            if not args.quiet:
                print("FAIL")
            continue
        md = render_card(card, out)
        (KNOWLEDGE / f"{card['slug']}.md").write_text(md, encoding="utf-8")
        generated += 1
        if not args.quiet:
            print(f"OK ({len(out)} chars)")

    # Index
    idx_md = render_index(CARDS)
    (KNOWLEDGE / "_Index.md").write_text(idx_md, encoding="utf-8")

    print(f"\n[summary] generated={generated} skipped={skipped} errors={errors} of {len(CARDS)}")


if __name__ == "__main__":
    main()
