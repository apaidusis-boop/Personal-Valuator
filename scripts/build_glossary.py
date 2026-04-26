"""Build vault Glossary — one note per métrica usada nos dossiers.

Cada entry tem: definição, fórmula, leitura (good/bad), thresholds BR vs US,
contraméricas (quando falha), fontes (clippings + books no library/), e
back-links para os dossiers que usam a métrica.

Uso:
    python scripts/build_glossary.py            # gera/actualiza Glossary/
    python scripts/build_glossary.py --backlinks  # inclui who-uses-this
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "obsidian_vault" / "Glossary"
DOSSIE_DIR = ROOT / "obsidian_vault" / "tickers"
CLIPPINGS = ROOT / "obsidian_vault" / "Clippings"

# Curated entries — anchored to CLAUDE.md screens + clippings já no vault.
ENTRIES: dict[str, dict] = {
    "PE": {
        "title": "P/E — Price / Earnings",
        "category": "valuation",
        "formula": "Preço da acção ÷ Lucro por acção (EPS, últimos 12m)",
        "leitura": (
            "Múltiplo do que o mercado paga por cada R$1 de lucro anual. "
            "Mais baixo = mais barato (cheaper), assumindo qualidade comparável."
        ),
        "thresholds": {
            "br_equity": "≤ 22.5 (via Graham, em conjunto com P/B)",
            "br_banks":  "≤ 10",
            "us":        "≤ 20 (Buffett quality threshold)",
        },
        "good_bad": (
            "**P/E baixo** pode indicar barato OU empresa em decadência. **P/E alto** "
            "pode indicar growth premium OU bolha. Sozinho, P/E é insuficiente — "
            "combinar com ROE (qualidade) e Graham/P-B (margem de segurança)."
        ),
        "counter": (
            "❌ Empresas com EPS volátil ou negativo (start-ups, cyclicals em "
            "trough) tornam P/E inútil. Para essas, usar EV/EBITDA ou P/Sales.\n"
            "❌ EPS GAAP pode ser inflado por items não-recorrentes — comparar "
            "com EPS adjusted/ongoing (ABBV é exemplo onde GAAP P/E ilude)."
        ),
        "sources": [
            "[[Clippings/Fundamental Analysis Principles, Types, and How to Use It]]",
            "[[Clippings/Warren Buffett's Value Investing Strategy Explained]]",
        ],
    },
    "PB": {
        "title": "P/B (P/VP) — Price / Book Value",
        "category": "valuation",
        "formula": "Preço da acção ÷ Patrimônio líquido por acção (BVPS)",
        "leitura": (
            "Quanto o mercado paga por cada R$1 de patrimônio líquido contábil. "
            "P/B = 1 → preço = book value; P/B < 1 → desconto sobre book."
        ),
        "thresholds": {
            "br_equity": "Componente do Graham (preço ≤ √(22.5 × EPS × BVPS))",
            "br_banks":  "≤ 1.5 (margem de segurança sobre o equity)",
            "us":        "≤ 3 (Buffett quality)",
        },
        "good_bad": (
            "**P/B < 1** sugere desconto, mas pode reflectir activos não-líquidos, "
            "goodwill inflado, ou ROE baixo. **P/B alto** justificável só se ROE "
            "for elevado (ex: ITUB4 P/B 2.4 com ROE 21%)."
        ),
        "counter": (
            "❌ Empresas asset-light (software, consultoria, marcas) têm book value "
            "subestimado — P/B perde significado. Comparar com peers do mesmo modelo.\n"
            "❌ Bancos com goodwill grande de M&A (ex: pós-aquisição) inflam book "
            "artificialmente — usar P/Tangible-B em vez de P/B."
        ),
        "sources": [
            "[[Clippings/Warren Buffett's Value Investing Strategy Explained]]",
        ],
    },
    "DY": {
        "title": "DY — Dividend Yield",
        "category": "income",
        "formula": "Dividendos pagos nos últimos 12m ÷ Preço actual da acção",
        "leitura": (
            "Yield anualizado de dividendos. **A nossa estratégia DRIP usa DY "
            "como proxy de income inicial e potencial de compounding via reinvestimento.**"
        ),
        "thresholds": {
            "br_equity": "≥ 6% (filosofia DRIP local; Selic alta = barra alta)",
            "br_banks":  "≥ 6%",
            "us":        "≥ 2.5% (Buffett tolera DY mais baixo se aristocrat)",
            "fii":       "≥ 8% (FIIs típicos; CRI papers podem chegar a 12-15%)",
        },
        "good_bad": (
            "**DY alto** atractivo, mas verificar **payout ratio** (>100% insustentável) "
            "e **dividend streak** (5y+ idealmente). **DY anormalmente alto** (>15%) "
            "frequentemente sinaliza distress — value trap em curso."
        ),
        "counter": (
            "❌ DY pode estar inflado por dividendo extraordinário one-off (ex: RDOR3 "
            "11% pós-Sul América). Olhar histórico pré-evento.\n"
            "❌ FIIs pagam de capital se imóveis vendidos — não é renda recorrente.\n"
            "❌ FIIs CRI papel: DY baseado em IPCA/CDI; cai com disinflation/Selic cut."
        ),
        "sources": [
            "[[Clippings/DRIP Investment How Dividend Reinvestment Plans Boost Your Portfolio]]",
        ],
    },
    "ROE": {
        "title": "ROE — Return on Equity",
        "category": "quality",
        "formula": "Lucro líquido ÷ Patrimônio líquido médio (anualizado)",
        "leitura": (
            "Taxa de retorno que a empresa gera sobre o capital dos accionistas. "
            "**Métrica chave de qualidade Buffett — \"empresas que geram >15% "
            "ROE de forma sustentada são compounders.\"**"
        ),
        "thresholds": {
            "br_equity": "≥ 15% (Graham clássico ajustado a juros locais)",
            "br_banks":  "≥ 12% (relaxado para era Selic alta; ITUB4 historicamente 21%)",
            "us":        "≥ 15% (Buffett standard)",
        },
        "good_bad": (
            "**ROE alto sustentado** = vantagem competitiva (moat). **ROE volátil** "
            "= cyclicality. **ROE alto via leverage** (alta D/E) é falso sinal — "
            "decompor via DuPont (margem × turnover × leverage)."
        ),
        "counter": (
            "❌ Empresas com book negativo geram ROE matemático mas sem significado.\n"
            "❌ Bancos: ROE depende fortemente do ciclo de crédito (NPL spike = ROE "
            "drop temporário).\n"
            "❌ Empresas asset-light com book pequeno (consultorias, software) "
            "inflam ROE por divisor pequeno — comparar com peers."
        ),
        "sources": [
            "[[Clippings/Warren Buffett's Value Investing Strategy How Patience and Discipline Built a Trillion-Dollar Empire]]",
        ],
    },
    "Graham_Number": {
        "title": "Graham Number — Margem de Segurança Quantitativa",
        "category": "valuation",
        "formula": "√(22.5 × EPS × BVPS)",
        "leitura": (
            "Preço-tecto que combina P/E ≤ 15 com P/B ≤ 1.5 (15 × 1.5 = 22.5). "
            "Se Preço Actual ≤ Graham Number, a acção tem margem de segurança."
        ),
        "thresholds": {
            "br_equity": "Preço ≤ Graham Number (factor 22.5; CLAUDE.md screen)",
            "br_banks":  "NÃO se aplica (estrutura de capital diferente)",
            "us":        "Conservador; Buffett tolera múltiplos mais altos para qualidade",
        },
        "good_bad": (
            "**Pass** = barato segundo Graham; **fail** = caro vs fundamentais. "
            "Não substitui análise qualitativa do moat, só dá entry-screen."
        ),
        "counter": (
            "❌ Falha em empresas asset-light (BVPS subestimado).\n"
            "❌ Falha em cyclicals em trough (EPS deprimido inflate Graham).\n"
            "❌ Não considera dívida — adicionar Net Debt/EBITDA como complemento."
        ),
        "sources": [
            "[[Clippings/Warren Buffett's Value Investing Strategy Explained]]",
        ],
    },
    "EPS": {
        "title": "EPS — Earnings per Share",
        "category": "fundamentals",
        "formula": "Lucro líquido (12m) ÷ Número de acções outstanding",
        "leitura": (
            "Lucro líquido normalizado por acção. Base para P/E e DCF. "
            "**Crescimento de EPS sustentável é o motor real de retorno de longo prazo.**"
        ),
        "thresholds": {
            "growth": "EPS YoY ≥ 10% sustentado = candidato compounder",
            "value":  "EPS estável + DY = candidato DRIP",
        },
        "good_bad": (
            "**EPS crescente** (3-5y CAGR) = qualidade. **EPS estagnado** = ex-growth. "
            "**EPS volátil** = cyclical (PRIO3, VALE3 são exemplo)."
        ),
        "counter": (
            "❌ EPS pode ser manipulado via buybacks (reduz denominador).\n"
            "❌ EPS GAAP vs Adjusted/Ongoing pode divergir muito (ABBV: GAAP P/E inflado "
            "por amortização de M&A; Ongoing EPS é o real).\n"
            "❌ Em bancos, EPS volátil reflecte provisões — usar PPNR (pre-provision) "
            "para tendência estrutural."
        ),
        "sources": [
            "[[Clippings/Fundamental Analysis Principles, Types, and How to Use It]]",
        ],
    },
    "BVPS": {
        "title": "BVPS — Book Value per Share",
        "category": "fundamentals",
        "formula": "Patrimônio líquido contábil ÷ Acções outstanding",
        "leitura": "Equity contábil por acção. Componente do P/B e Graham.",
        "thresholds": {
            "growth": "BVPS subestimado em asset-light → P/B perde significado",
            "banks":  "BVPS é altamente confiável (regulação contábil rígida)",
        },
        "good_bad": (
            "**BVPS crescente YoY** = retenção de lucros funciona. **BVPS estagnado** "
            "com DY alto = distribuição agressiva (sustentável só se ROE > custo capital)."
        ),
        "counter": (
            "❌ Goodwill inflado por M&A esticado mascara BVPS real — preferir "
            "Tangible Book Value para bancos pós-aquisição.\n"
            "❌ Asset-light: BVPS pequeno → P/B alto não é sinal de overvalue."
        ),
        "sources": [],
    },
    "Net_Debt_EBITDA": {
        "title": "Net Debt / EBITDA — Alavancagem",
        "category": "balance_sheet",
        "formula": "(Dívida bruta − Caixa) ÷ EBITDA (12m)",
        "leitura": (
            "Quantos anos de EBITDA seriam necessários para pagar a dívida líquida. "
            "**Maior = mais alavancado = mais frágil em downturns.**"
        ),
        "thresholds": {
            "br_equity": "< 3.0× (CLAUDE.md screen)",
            "br_banks":  "NÃO se aplica (banks gerem balance sheet diferente)",
            "us":        "< 2.5× típico investment-grade; > 4× = high yield risk",
        },
        "good_bad": (
            "**< 1×** ultra-conservador (cash-rich); **1-3×** saudável; **3-5×** "
            "alavancado (cuidado em downturn); **> 5×** distress potencial."
        ),
        "counter": (
            "❌ EBITDA pode ser inflado por items não-recorrentes ou ajustes contabeis.\n"
            "❌ REITs/utilities operam com leverage alto por design — comparar dentro "
            "do sector, não cross-sector.\n"
            "❌ Capital leases pós-IFRS 16 inflam dívida nominal — verificar se "
            "EBITDA também foi ajustado."
        ),
        "sources": [],
    },
    "Dividend_Streak": {
        "title": "Dividend Streak — Anos Consecutivos a Pagar",
        "category": "income",
        "formula": "Anos seguidos sem corte de dividendo (qualquer valor, inclusive nominal-only)",
        "leitura": (
            "Sinaliza disciplina de distribuição + capacidade de gerar caixa em "
            "ciclos completos. **Dividend Aristocrat (US) = 25y+; King = 50y+.**"
        ),
        "thresholds": {
            "br":  "≥ 5y (CLAUDE.md screen mínimo para tese DRIP)",
            "us":  "≥ 10y consecutivos OU Aristocrat (25y+)",
            "kings": "50y+ — JNJ (62y), PG (68y), KO (62y) são Kings classics",
        },
        "good_bad": (
            "**Streak longo** = compromisso da gestão + caixa robusto através de "
            "recessões. **Streak interrompido** (cut) = sinal vermelho de credibilidade — "
            "raramente recupera o status premium."
        ),
        "counter": (
            "❌ Streak nominal pode mascarar redução real (ex: split sem ajuste de "
            "dividendo proporcional = corte disfarçado).\n"
            "❌ Empresas que pagam dividendo simbólico para manter streak (US gov-related) "
            "não são DRIP-quality.\n"
            "❌ FIIs raramente medem streak em anos (distribuições mensais variáveis)."
        ),
        "sources": [
            "[[Clippings/DRIP Investment How Dividend Reinvestment Plans Boost Your Portfolio]]",
        ],
    },
    "Basel_Ratio": {
        "title": "Basel Ratio — Capital Regulatório de Bancos",
        "category": "banks_regulatory",
        "formula": "Capital regulatório total ÷ RWA (Risk-Weighted Assets)",
        "leitura": (
            "Cushion mínimo de capital exigido por reguladores (BCB, Fed, ECB) "
            "para absorver perdas. **Define quanto banco pode crescer/distribuir.**"
        ),
        "thresholds": {
            "min_regulatorio_br": "8.0% (BCB) + buffers = ~10.5% efectivo",
            "saudavel":            "≥ 14% (cushion confortável)",
            "premium":             "≥ 16% (capital excess → buyback/extraordinary div)",
        },
        "good_bad": (
            "**Trend ascendente** = banco a reconstruir cushion (geralmente pós-ciclo). "
            "**Trend descendente** = crescimento agressivo OU perdas a comer capital."
        ),
        "counter": (
            "❌ Basel total é menos preditivo que CET1 (capital high-quality).\n"
            "❌ Bancos podem inflar Basel via debt subordinado (Tier 2) que não absorve "
            "perdas em going-concern.\n"
            "❌ Comparar dentro do peer set (small-cap vs incumbent)."
        ),
        "sources": [],
    },
    "CET1": {
        "title": "CET1 — Common Equity Tier 1",
        "category": "banks_regulatory",
        "formula": "Equity comum ajustado ÷ RWA",
        "leitura": (
            "Capital de **maior qualidade** — equity puro, sem hybrids. Métrica "
            "principal para Basel III e stress tests."
        ),
        "thresholds": {
            "min_regulatorio": "4.5% Pillar 1 + 2.5% buffer = 7%; cíclico até 9.5%",
            "saudavel":         "≥ 11% (peer BR médio)",
            "premium":          "≥ 13% (ITUB4 historicamente)",
        },
        "good_bad": (
            "**CET1 leadership** (vs peers) = capacidade de pagar dividendos extraordinários "
            "OU resistir a cycle peak. **CET1 fraco** + NPL a subir = double risk."
        ),
        "counter": (
            "❌ DTAs (deferred tax assets) inflam CET1 sem caixa real.\n"
            "❌ Dividendos propostos não-pagos podem inflar CET1 momentaneamente.\n"
            "❌ Bancos pequenos têm CET1 maior por modelo (fewer RWA-dense activities)."
        ),
        "sources": [],
    },
    "NPL": {
        "title": "NPL — Non-Performing Loans (E-H)",
        "category": "banks_credit",
        "formula": "Saldo da carteira em rating E até H ÷ Carteira total (BACEN)",
        "leitura": (
            "% da carteira de crédito em deterioração ou inadimplência (90+ dias). "
            "**Sinal lagging do ciclo de crédito — peak ~6m após Selic peak.**"
        ),
        "thresholds": {
            "saudavel": "< 3% pré-pandémico",
            "stress":   "3-5% (ciclo elevado, ainda manageable)",
            "alarme":   "> 5% (provisões a comer lucro; ROE drop)",
        },
        "good_bad": (
            "**NPL a cair** = ciclo virou (e provisões diminuem → ROE expansion). "
            "**NPL a subir** = pressão sobre lucros próximos 2-3 trimestres."
        ),
        "counter": (
            "❌ NPL E-H é apenas a parte severa — H mostra perda; E ainda recuperável.\n"
            "❌ Banks podem 'esconder' NPL via renegociação massiva (relaxar critérios).\n"
            "❌ Ciclo de crédito é regional + segmento — corporate vs consumer divergem."
        ),
        "sources": [],
    },
    "DRIP": {
        "title": "DRIP — Dividend Reinvestment Plan",
        "category": "concept",
        "formula": "Reinvestir dividendos automaticamente em mais acções (zero corretagem ideal)",
        "leitura": (
            "Estratégia de compounding: cada distribuição compra mais acções, que "
            "geram mais dividendos no próximo ciclo. **A nossa estratégia core "
            "para BR e US holdings income-focused.**"
        ),
        "thresholds": {
            "candidato": "DY ≥ 6% (BR) ou ≥ 2.5% (US) + streak ≥ 5y + ROE ≥ 12%",
            "default":   "Activar DRIP em JNJ, KO, PG, O, JPM, BLK, BBDC4, ITSA4, FIIs",
            "exclui":    "Growth picks (XP, PLTR, TSLA, BRK-B, TTD), tactical (GREK, TEN)",
        },
        "good_bad": (
            "**Funciona** quando empresa mantém DY + cresce dividendo + acção não "
            "está esticada. **Falha** quando se aplica a growth/tactical (compra-se "
            "alto sem catalyst de income)."
        ),
        "counter": (
            "❌ DRIP em GREK falha porque dividendos são irregulares e tactical.\n"
            "❌ DRIP em TEN falha porque empresa está em distress signal.\n"
            "❌ DRIP em valuation esticado compra alto — combinar com floor de PE/DY."
        ),
        "sources": [
            "[[Clippings/DRIP Investment How Dividend Reinvestment Plans Boost Your Portfolio]]",
        ],
    },
    "Aristocrat": {
        "title": "Dividend Aristocrat / King",
        "category": "concept",
        "formula": (
            "Aristocrat = 25y+ de aumentos consecutivos no dividendo (S&P 500 member). "
            "King = 50y+ de aumentos."
        ),
        "leitura": (
            "Categorias formais (S&P) que sinalizam **disciplina extrema** de "
            "distribuição. Nas nossas holdings: JNJ, KO, PG, HD, PEP, MCD são Kings/Aristocrats."
        ),
        "thresholds": {
            "aristocrat": "25y+ aumentos contínuos",
            "king":       "50y+ aumentos contínuos",
            "config":     "config/kings_aristocrats.yaml (87 tickers, fonte canónica)",
        },
        "good_bad": (
            "**Membership = sinal forte** de gestão pró-dividendo + caixa robusto. "
            "**Loss of status** (corte) = sinal de credibilidade severo, raramente recupera."
        ),
        "counter": (
            "❌ Aristocrat status pode ser mantido com aumentos simbólicos ($0.01) "
            "que não acompanham inflação — verificar dividend growth real.\n"
            "❌ Maturidade extrema correlaciona com low growth — bom para income, "
            "fraco para total return.\n"
            "❌ Inclusão depende de S&P 500 membership — drop-out automático."
        ),
        "sources": [
            "[[Clippings/Warren Buffett's Value Investing Strategy How Patience and Discipline Built a Trillion-Dollar Empire]]",
        ],
    },
    "Margin_of_Safety": {
        "title": "Margin of Safety — Margem de Segurança (Graham/Buffett)",
        "category": "concept",
        "formula": "(Preço Justo Estimado − Preço Actual) ÷ Preço Justo Estimado",
        "leitura": (
            "**Princípio fundacional do value investing** (Graham, depois Buffett): "
            "comprar significativamente abaixo do valor intrínseco para proteger "
            "contra erros de análise + eventos adversos."
        ),
        "thresholds": {
            "graham":  "≥ 33% desconto sobre intrinsic estimate",
            "buffett": "≥ 25% para qualidade comprovada (compounders)",
            "screen":  "Graham Number ≤ Preço Actual (proxy quantitativo BR)",
        },
        "good_bad": (
            "**Margem ampla** (40-50%+) = colchão grande para análise errada. "
            "**Margem fina** = exigir alta certeza no fair value."
        ),
        "counter": (
            "❌ Cálculo de fair value depende de assumptions (growth, discount rate) "
            "— sensitivity analysis é obrigatório.\n"
            "❌ Margin of safety em value trap = não margem (empresa em decadência "
            "não justifica preço actual).\n"
            "❌ Cíclicas em peak parecem ter margem mas estão a usar earnings inflados."
        ),
        "sources": [
            "[[Clippings/Warren Buffett's Value Investing Strategy Explained]]",
            "[[Clippings/Warren Buffett's Value Investing Strategy How Patience and Discipline Built a Trillion-Dollar Empire]]",
        ],
    },
    "Moat": {
        "title": "Moat — Vantagem Competitiva Sustentável (Buffett)",
        "category": "concept",
        "formula": "Conceito qualitativo. Sources: brand, network effect, scale, switching cost, regulatory.",
        "leitura": (
            "**Pilar 1 da framework Buffett**: empresa com moat tem ROE alto sustentado, "
            "pricing power e protege market share contra new entrants."
        ),
        "thresholds": {
            "wide":   "ROE > 20% sustentado 10y+ (KO, JNJ, V)",
            "narrow": "ROE 12-20% com algum moat identificável (ACN, HD)",
            "none":   "Commoditized; competir só em preço (cyclicals, energy)",
        },
        "good_bad": (
            "**Wide moat** + preço razoável = compounder. **No moat** = comprar só "
            "com margem de segurança massiva (cigar butt strategy)."
        ),
        "counter": (
            "❌ Moats erodem com tecnologia/regulação (Kodak, Blockbuster).\n"
            "❌ Moat percebido pode ser apenas inertia do consumidor — testar com "
            "novos entrants (fintechs vs bancos tradicionais).\n"
            "❌ Brand moat depende de marketing contínuo — cortes geram declínio gradual."
        ),
        "sources": [
            "[[Clippings/Buffett's Moat Google's Competitive Advantage]]",
        ],
    },
}


def render_entry(slug: str, data: dict) -> str:
    lines = [
        "---",
        "type: glossary",
        f"slug: {slug}",
        f"title: {data['title']}",
        f"category: {data['category']}",
        f"date: {date.today().isoformat()}",
        "tags: [glossary, tutor, " + data["category"] + "]",
        "---",
        "",
        f"# 📖 {data['title']}",
        "",
        f"> Categoria: **{data['category']}**. "
        f"Cross-links: [[CONSTITUTION]] · [[Glossary/_Index]]",
        "",
        "## Fórmula",
        "",
        f"`{data['formula']}`",
        "",
        "## Leitura",
        "",
        data["leitura"],
        "",
        "## Thresholds",
        "",
    ]
    for k, v in data["thresholds"].items():
        lines.append(f"- **{k}**: {v}")
    lines += [
        "",
        "## Bom vs Mau",
        "",
        data["good_bad"],
        "",
        "## Contraméricas (quando o sinal falha)",
        "",
        data["counter"],
        "",
    ]
    if data.get("sources"):
        lines += ["## Fontes", ""]
        for s in data["sources"]:
            lines.append(f"- {s}")
        lines.append("")
    lines += ["---", f"*Auto-build via `scripts/build_glossary.py` em {date.today().isoformat()}.*"]
    return "\n".join(lines) + "\n"


def find_dossier_users(slug: str) -> list[str]:
    """Find dossiers that mention this metric."""
    pattern_map = {
        "PE": ["P/E", "Price/Earnings"],
        "PB": ["P/B", "P/VP", "Price/Book"],
        "DY": ["DY", "Dividend Yield"],
        "ROE": ["ROE", "Return on Equity"],
        "Graham_Number": ["Graham"],
        "EPS": ["EPS"],
        "BVPS": ["BVPS"],
        "Net_Debt_EBITDA": ["Net Debt", "ND/EBITDA", "Dívida Líq"],
        "Dividend_Streak": ["Streak div", "dividend streak"],
        "Basel_Ratio": ["Basel"],
        "CET1": ["CET1"],
        "NPL": ["NPL"],
        "DRIP": ["DRIP"],
        "Aristocrat": ["Aristocrat", "King"],
        "Margin_of_Safety": ["margem de segurança", "margin of safety"],
        "Moat": ["moat"],
    }
    needles = pattern_map.get(slug, [])
    if not needles:
        return []
    users = []
    for p in DOSSIE_DIR.glob("*_DOSSIE.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if any(n.lower() in text.lower() for n in needles):
            users.append(p.stem.replace("_DOSSIE", ""))
    return sorted(users)


def render_index(entries: list[tuple[str, dict]]) -> str:
    by_cat: dict[str, list[tuple[str, dict]]] = {}
    for slug, data in entries:
        by_cat.setdefault(data["category"], []).append((slug, data))

    lines = [
        "---",
        "type: glossary_index",
        f"date: {date.today().isoformat()}",
        f"entries: {len(entries)}",
        "tags: [glossary, tutor, index]",
        "---",
        "",
        "# 📚 Glossary — Índice",
        "",
        f"> {len(entries)} entradas. Cada uma explica **fórmula + leitura + "
        "thresholds BR/US + contraméricas + fontes**. Use [[Glossary/<slug>]] "
        "para hover-preview em qualquer dossier.",
        "",
    ]
    for cat in sorted(by_cat):
        lines += [f"## {cat}", ""]
        for slug, data in sorted(by_cat[cat]):
            lines.append(f"- [[Glossary/{slug}|{data['title']}]]")
        lines.append("")
    lines += [
        "## Como usar (Tutor mode)",
        "",
        "1. Em qualquer dossier `*_DOSSIE.md`, hover sobre uma métrica para "
        "preview da entrada Glossary correspondente (Obsidian nativo).",
        "2. Cada entrada cita as Clippings de origem (Investopedia, Suno, etc.).",
        "3. As contraméricas listam **quando NÃO confiar** na métrica isolada — "
        "é nessas que está a alpha real.",
        "4. Para deep-dive conceitual, usar `python -m library.rag ask "
        "\"<pergunta>\" --k 6` — RAG inclui clippings + 4 books.",
        "",
        "---",
        f"*Build: `python scripts/build_glossary.py`*",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--backlinks", action="store_true",
                    help="Include who-uses-this scan (slow)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    GLOSSARY.mkdir(parents=True, exist_ok=True)

    entries = list(ENTRIES.items())
    for slug, data in entries:
        md = render_entry(slug, data)
        if args.backlinks:
            users = find_dossier_users(slug)
            if users:
                md = md.replace("---\n*Auto-build", "## Usado em\n\n" +
                                "\n".join(f"- [[{u}_DOSSIE]]" for u in users) +
                                "\n\n---\n*Auto-build")
        out = GLOSSARY / f"{slug}.md"
        out.write_text(md, encoding="utf-8")
        if not args.quiet:
            print(f"  ✓ {out.relative_to(ROOT)}")

    # Index
    idx = GLOSSARY / "_Index.md"
    idx.write_text(render_index(entries), encoding="utf-8")
    if not args.quiet:
        print(f"\n  ✓ {idx.relative_to(ROOT)}")
        print(f"\n[summary] {len(entries)} entries + index → {GLOSSARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
