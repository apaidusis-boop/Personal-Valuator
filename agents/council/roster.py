"""Council roster — maps Modo×Jurisdiction to a named specialist persona.

The council is no longer made of anonymous "sector_specialist" / "risk_officer"
roles. Each role is filled by a NAMED employee from `config/agents.yaml`,
with their own persona MD in `obsidian_vault/agents/personas/<name>.md`.

This file is the single source of truth for who shows up in the room.

Routing:
  Modo A-BR  → Tião Galpão (Industrials BR)
  Modo A-US  → Charlie Compounder (Buffett-frame US)
  Modo B-BR  → Diego Bancário (Banks BR)
  Modo B-US  → Hank Tier-One (Banks US)
  Modo C-BR  → Aderbaldo Cíclico (Commodities BR)
  Modo D-BR  → Lourdes Aluguel (FIIs BR)
  Modo D-US  → Walter Triple-Net (REITs US)

Cross-cutting (added to every council where macro pesa):
  Mariana Macro (Macro Strategist)

Functional (always in the room):
  Valentina Prudente (Risk Officer — existing CRO)
  Pedro Alocação    (Capital Allocator)

Special case — holdings with mixed exposure:
  Modo=A but sector="Holding" with banking parent (e.g. ITSA4 → Itaú) → adds
  Diego Bancário as a *second* sector specialist alongside Tião Galpão.
"""
from __future__ import annotations

from dataclasses import dataclass

from agents.council.dossier import CouncilDossier


@dataclass(frozen=True)
class CouncilSeat:
    """One seat at the council table."""
    role: str                  # "sector_specialist" | "risk_officer" | "portfolio_officer" | "macro_strategist" | "sector_specialist_secondary"
    employee_name: str         # human name — used in transcript and wikilinks
    agent_slug: str            # agents.yaml name — used to load full persona
    title: str                 # for transcript heading
    framework_brief: str       # short rule set the prompt embeds


# ─────────────────────────────────────────────────────────────────────
# Framework briefs (concise — full bio stays in vault persona MDs)
# ─────────────────────────────────────────────────────────────────────

FRAMEWORKS = {
    # keyed by agent_slug (matches config/agents.yaml `name` field)
    "industrials_br_specialist": """Modo A-BR Industrials/Consumer.
Graham clássico ajustado: P/E vs mediana setorial, FCF Yield, ROE > Ke (Selic+4.5%≈18%),
ND/EBITDA < 3x, CCC, margem EBITDA, dividend streak ≥ 5y.
VETO: P/TBV em industrial, DCF sem WACC ajustado a Selic, peer comp sem ajuste de jurisdição.
Macro local importa: Selic encarece capex, câmbio afecta exportadoras.""",

    "banks_br_specialist": """Modo B-BR Bancos.
P/E ≤ 10, P/B ≤ 1.5, DY ≥ 6%, ROE ≥ 12% (Selic-era), streak ≥ 5y.
NIM, cobertura, Basileia, eficiência são 2ª natureza.
VETO: Graham Number, EV/EBITDA, ND/EBITDA aplicados a banco.""",

    "banks_us_specialist": """Modo B-US Banks.
P/E ≤ 12, P/TBV ≤ 1.8 (TBV não BV), ROTCE ≥ 15%, CET1 ≥ 11%, Efficiency ≤ 60%, streak pós-2009 ≥ 10y.
VETO: P/B simples (sobrestima banco com goodwill), streak pré-GFC.""",

    "industrials_us_specialist": """Modo A-US Industrials/Consumer (Buffett frame).
P/E ≤ 20, P/B ≤ 3, DY ≥ 2.5%, ROE ≥ 15% sustentado, Aristocrat ou ≥ 10y streak.
Shareholder Yield (Div + Buyback) > Yield isolado. Moat antes de múltiplo.
VETO: yield sem layer de buyback, valuation sem histórico de ROIC.""",

    "commodities_br_specialist": """Modo C-BR Commodities.
Regra do ciclo PRIMEIRO. Mid-cycle EBITDA não trailing. Lifting cost, reservas, posição no ciclo.
VETO: P/E spot sem fase do ciclo declarada, valuation no peak earnings.""",

    "fiis_br_specialist": """Modo D-BR FIIs.
Cap Rate vs NTN-B real, P/VP ≤ 1.0, vacância física + financeira separadas, LTV ≤ 50% (tijolo) / 65% (papel),
DSCR ≥ 1.5×. Distribuição 95% do resultado caixa.
VETO: Piotroski/Altman aplicados a FII, DY sobre lucro contábil em vez de FFO.""",

    "reits_us_specialist": """Modo D-US REITs.
P/AFFO > P/FFO (AFFO exclui capex de manutenção). Cap Rate vs Treasury 10Y spread ≥ 2.5%.
LTV ≤ 40% IG. Tenant concentration top ≤ 10%. Distribuição 90% lucro tributável.
VETO: FFO sem ajuste para AFFO, concentração tenant > 20% sem warning.""",

    "macro_strategist": """Macro cross-jurisdição.
NÃO escolho ações. NÃO dou rating. NÃO faço DCF.
Descrevo regime: Selic/Fed, câmbio, ciclo, yield curve. Identifico triggers macro
que mudam tese (Selic ≤ X, Brent ≥ Y, câmbio ≤ Z).
Convocada quando Macro Exposure ou Dependency ≥ 4.""",

    "risk_auditor": """Chief Risk Officer (existing CRO, no veto power on method but on flags).
Pre-Mortem rigoroso. Distress: Altman zona cinzenta/distress, Piotroski ≤ 4, Beneish ≥ -1.78.
Surfaces gatilhos OBSERVÁVEIS específicos do sector+jurisdição.
"Risk is permanent loss of capital, not volatility" — só sinaliza o que é permanente.""",

    "capital_allocator": """Capital Allocator.
NÃO decide se a empresa é boa. Decide se cabe NESTA carteira AGORA.
Sizing (1.5-3% inicial / 3-7% maduro / 10% teto), correlação > 0.7 = warning,
currency isolation (BRL/USD não misturam).
VETO: peso > 10% sem tese de concentração; BUY sem cash deployable.""",
}


# ─────────────────────────────────────────────────────────────────────
# Routing — Modo×Jurisdiction → Sector Specialist
# ─────────────────────────────────────────────────────────────────────

SECTOR_SPECIALIST_ROUTE: dict[str, tuple[str, str, str]] = {
    # key: f"{modo}_{jurisdiction.upper()}"
    # value: (employee_name, agent_slug, title)
    "A_BR": ("Tião Galpão", "industrials_br_specialist", "Industrials & Consumer BR Specialist"),
    "A_US": ("Charlie Compounder", "industrials_us_specialist", "Industrials & Consumer US Specialist (Buffett frame)"),
    "B_BR": ("Diego Bancário", "banks_br_specialist", "Banks BR Specialist"),
    "B_US": ("Hank Tier-One", "banks_us_specialist", "Banks US Specialist"),
    "C_BR": ("Aderbaldo Cíclico", "commodities_br_specialist", "Commodities BR Specialist"),
    "D_BR": ("Lourdes Aluguel", "fiis_br_specialist", "FIIs BR Specialist"),
    "D_US": ("Walter Triple-Net", "reits_us_specialist", "REITs US Specialist"),
}


HOLDING_KEYWORDS_BANK = ("itaú", "itau", "bradesco", "banco")  # detect financial holdings


def _detect_secondary_specialist(d: CouncilDossier) -> tuple[str, str, str] | None:
    """Holdings with significant banking exposure (e.g. ITSA4 → Itaú) get
    a SECOND sector specialist (Banks BR) alongside the primary Industrials BR.
    Detection: thesis text mentions Itaú/Bradesco AND modo is A AND sector is Holding."""
    if d.modo != "A" or (d.sector or "").lower() != "holding":
        return None
    blob = (d.thesis_text or "").lower() + " " + (d.name or "").lower()
    if any(kw in blob for kw in HOLDING_KEYWORDS_BANK):
        return SECTOR_SPECIALIST_ROUTE.get(f"B_{d.market.upper()}")
    return None


def _macro_belongs_in_room(d: CouncilDossier) -> bool:
    """Mariana Macro joins when:
    - Modo C (commodities — macro is the driver)
    - Modo B (banks — Selic/Fed defines NIM)
    - Industrials with material FX exposure (heuristic: large debt + market BR)
    - Always for now while we validate; can tighten later."""
    if d.modo in ("B", "C"):
        return True
    return True  # default ON during prototype; tighten with score-based later


def assemble_council(d: CouncilDossier) -> list[CouncilSeat]:
    """Return ordered list of seats for this dossier's debate."""
    seats: list[CouncilSeat] = []

    # 1. Primary sector specialist (always)
    key = f"{d.modo}_{d.market.upper()}"
    primary = SECTOR_SPECIALIST_ROUTE.get(key) or SECTOR_SPECIALIST_ROUTE["A_BR"]
    employee, slug, title = primary
    seats.append(CouncilSeat(
        role="sector_specialist",
        employee_name=employee,
        agent_slug=slug,
        title=title,
        framework_brief=FRAMEWORKS.get(slug, FRAMEWORKS["industrials_br_specialist"]),
    ))

    # 2. Secondary sector specialist (if holding has cross-modo exposure)
    secondary = _detect_secondary_specialist(d)
    if secondary:
        e2, s2, t2 = secondary
        seats.append(CouncilSeat(
            role="sector_specialist_secondary",
            employee_name=e2,
            agent_slug=s2,
            title=t2,
            framework_brief=FRAMEWORKS.get(s2, ""),
        ))

    # 3. Macro Strategist if relevant
    if _macro_belongs_in_room(d):
        seats.append(CouncilSeat(
            role="macro_strategist",
            employee_name="Mariana Macro",
            agent_slug="macro_strategist",
            title="Chief Macro Strategist",
            framework_brief=FRAMEWORKS["macro_strategist"],
        ))

    # 4. Risk Officer (always)
    seats.append(CouncilSeat(
        role="risk_officer",
        employee_name="Valentina Prudente",
        agent_slug="risk_auditor",
        title="Chief Risk Officer",
        framework_brief=FRAMEWORKS["risk_auditor"],
    ))

    # 5. Capital Allocator (always)
    seats.append(CouncilSeat(
        role="portfolio_officer",
        employee_name="Pedro Alocação",
        agent_slug="capital_allocator",
        title="Capital Allocator",
        framework_brief=FRAMEWORKS["capital_allocator"],
    ))

    return seats


def get_framework(slug: str) -> str:
    """Lookup helper used by personas.py during prompt assembly."""
    return FRAMEWORKS.get(slug, "")
