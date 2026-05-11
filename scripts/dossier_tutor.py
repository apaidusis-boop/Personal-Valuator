"""Dossier Tutor — injecta secção `## Tutor` em cada DOSSIE.md.

Lê os fundamentals do dossier (PE/PB/DY/ROE/streak/Basel/etc.), aplica a
filosofia de screening do CLAUDE.md, e gera bullets que explicam:
  - cada métrica individualmente (com link [[Glossary/X]])
  - se passa o screen para o mercado/sector
  - o que isso significa em palavras simples

Idempotente: substitui qualquer "## Tutor" pré-existente.

Uso:
    python scripts/dossier_tutor.py            # processa todos os dossiers
    python scripts/dossier_tutor.py --ticker ABCB4
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOSSIE_DIR = ROOT / "obsidian_vault" / "tickers"


def _parse_fundamentals(text: str) -> dict:
    """Extract key metrics from the dossier fundamentals snapshot."""
    out: dict = {}

    # ROE / P/E / P/B
    m = re.search(r"\*\*ROE\*\*:\s*([\d.]+)%\s*\|\s*\*\*P/E\*\*:\s*([\d.]+|n/a)\s*\|\s*\*\*P/B\*\*:\s*([\d.]+|n/a)", text)
    if m:
        out["roe"] = float(m.group(1)) / 100
        if m.group(2) != "n/a":
            out["pe"] = float(m.group(2))
        if m.group(3) != "n/a":
            out["pb"] = float(m.group(3))

    # DY / streak / market cap
    m = re.search(r"\*\*DY\*\*:\s*([\d.]+)%", text)
    if m:
        out["dy"] = float(m.group(1)) / 100
    m = re.search(r"\*\*Streak div\*\*:\s*(\d+)y", text)
    if m:
        out["streak"] = int(m.group(1))
    m = re.search(r"\*\*EPS\*\*:\s*([-\d.]+)\s*\|\s*\*\*BVPS\*\*:\s*([-\d.]+)", text)
    if m:
        out["eps"] = float(m.group(1))
        out["bvps"] = float(m.group(2))

    # Last price + YoY
    m = re.search(r"\*\*Last price\*\*:\s*\w+\s+([\d.]+)", text)
    if m:
        out["price"] = float(m.group(1))
    m = re.search(r"\*\*YoY\*\*:\s*([+-][\d.]+)%", text)
    if m:
        out["yoy"] = float(m.group(1))

    # Basel ratio (banks) — latest from BACEN regulatório table
    bm = re.findall(r"\| Basel \|.*?(\d+\.\d+)%", text)
    if bm:
        out["basel"] = float(bm[-1]) / 100  # last column = subject ticker
    cm = re.findall(r"\| CET1 \|.*?(\d+\.\d+)%", text)
    if cm:
        out["cet1"] = float(cm[-1]) / 100
    nm = re.findall(r"\| NPL E-H \|.*?(\d+\.\d+)%", text)
    if nm:
        out["npl"] = float(nm[-1]) / 100

    return out


def _parse_meta(text: str) -> dict:
    """Frontmatter market + sector + is_holding + verdict."""
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    out = {}
    for line in fm.splitlines():
        m = re.match(r"^([\w_]+):\s*(.+)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def _build_tutor(meta: dict, fund: dict) -> str:
    """Build a Tutor section based on parsed metrics + market philosophy."""
    market = meta.get("market", "br")
    sector = meta.get("sector", "")
    is_bank = sector.lower() in ("banks", "bancos")
    is_fii = market == "br" and meta.get("ticker", "").endswith("11") and \
             not is_bank
    is_holding = meta.get("is_holding", "False") == "True"

    bullets: list[str] = []

    # P/E
    if "pe" in fund:
        pe = fund["pe"]
        if is_bank:
            ok = pe <= 10
            ctx = (f"Bancos BR têm spread alto e múltiplos comprimidos — "
                   f"target ≤ 10. **Actual {pe:.2f}** {'passa' if ok else 'NÃO passa'}.")
        elif market == "us":
            ok = pe <= 20
            ctx = (f"Buffett quality: P/E ≤ 20. **Actual {pe:.2f}** "
                   f"{'passa' if ok else 'esticado vs critério'}.")
        else:
            ok = pe <= 22.5
            ctx = (f"Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). "
                   f"**Actual {pe:.2f}** {'passa' if ok else 'fora do screen'}.")
        bullets.append(f"- **P/E = {pe:.2f}** → [[Glossary/PE|porquê isto importa?]]. {ctx}")

    # P/B
    if "pb" in fund:
        pb = fund["pb"]
        if is_bank:
            ok = pb <= 1.5
            ctx = (f"Bancos: P/B ≤ 1.5 = margem sobre equity. **{pb:.2f}** "
                   f"{'OK' if ok else 'caro vs equity (mas verificar ROE)'}.")
        elif market == "us":
            ok = pb <= 3
            ctx = (f"US: P/B ≤ 3. **{pb:.2f}** {'OK' if ok else 'esticado'}.")
        else:
            ctx = (f"BR equity: usado dentro do Graham. **{pb:.2f}** — "
                   f"verificar consistência com ROE.")
        bullets.append(f"- **P/B = {pb:.2f}** → [[Glossary/PB|leitura completa]]. {ctx}")

    # DY
    if "dy" in fund:
        dy = fund["dy"]
        if is_fii:
            ok = dy >= 0.08
            ctx = (f"FIIs: target DY ≥ 8%. **{dy*100:.2f}%** "
                   f"{'OK' if ok else 'baixo para FII; verificar reset/cycle'}.")
        elif market == "us":
            ok = dy >= 0.025
            ctx = (f"US Buffett DRIP: DY ≥ 2.5%. **{dy*100:.2f}%** "
                   f"{'OK' if ok else 'fraco; verificar se é growth pick'}.")
        else:
            ok = dy >= 0.06
            ctx = (f"BR DRIP: DY ≥ 6%. **{dy*100:.2f}%** "
                   f"{'passa' if ok else 'abaixo do floor — DRIP não-óbvio'}.")
        if dy >= 0.15:
            ctx += " ⚠️ DY > 15% frequentemente sinaliza **distress**, não oportunidade."
        bullets.append(f"- **DY = {dy*100:.2f}%** → [[Glossary/DY|leitura + contraméricas]]. {ctx}")

    # ROE
    if "roe" in fund:
        roe = fund["roe"]
        if is_bank:
            ok = roe >= 0.12
            ctx = (f"Bancos BR (Selic alta): target ≥ 12%. **{roe*100:.2f}%** "
                   f"{'OK' if ok else 'fraco'}.")
        else:
            ok = roe >= 0.15
            ctx = (f"Buffett quality: ≥ 15%. **{roe*100:.2f}%** "
                   f"{'compounder-grade' if ok else 'abaixo do critério'}.")
        bullets.append(f"- **ROE = {roe*100:.2f}%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. {ctx}")

    # Graham Number (apenas BR equity não-bank)
    if not is_bank and not is_fii and "eps" in fund and "bvps" in fund and "price" in fund:
        try:
            graham = (22.5 * fund["eps"] * fund["bvps"]) ** 0.5
            ok = fund["price"] <= graham
            bullets.append(
                f"- **Graham Number ≈ R$ {graham:.2f}** vs preço **R$ {fund['price']:.2f}** "
                f"→ [[Glossary/Graham_Number|conceito]]. "
                f"{'✅ Tem margem de segurança Graham.' if ok else '❌ Acima do tecto Graham.'}"
            )
        except (TypeError, ValueError):
            pass

    # Streak
    if "streak" in fund:
        s = fund["streak"]
        threshold = 5 if market == "br" else 10
        ok = s >= threshold
        bullets.append(
            f"- **Streak div = {s}y** → [[Glossary/Dividend_Streak|porque importa]]. "
            f"Target {market.upper()} ≥ {threshold}y; {'**passa**' if ok else 'curto'}."
            + (" Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y." if s >= 25 else "")
        )

    # Bank-specific
    if is_bank:
        if "basel" in fund:
            b = fund["basel"]
            tier = "premium" if b >= 0.16 else ("saudável" if b >= 0.14 else "frágil")
            bullets.append(
                f"- **Basel = {b*100:.2f}%** → [[Glossary/Basel_Ratio|capital regulatório]]. "
                f"Tier **{tier}** (mín BCB ~10.5%; saudável ≥14%; premium ≥16%)."
            )
        if "cet1" in fund:
            c = fund["cet1"]
            tier = "premium" if c >= 0.13 else ("saudável" if c >= 0.11 else "frágil")
            bullets.append(
                f"- **CET1 = {c*100:.2f}%** → [[Glossary/CET1|capital high-quality]]. "
                f"Tier **{tier}** (≥11% médio peer BR; ≥13% leadership tipo ITUB4)."
            )
        if "npl" in fund:
            n = fund["npl"]
            tier = "saudável" if n < 0.03 else ("stress" if n < 0.05 else "alarme")
            bullets.append(
                f"- **NPL = {n*100:.2f}%** → [[Glossary/NPL|crédito em deterioração]]. "
                f"Tier **{tier}** (< 3% saudável, > 5% alarme)."
            )

    # Concept-level guidance (intent, DRIP, Aristocrat membership)
    concept_bullets: list[str] = []
    if is_holding:
        if market == "us" and fund.get("dy", 0) >= 0.025:
            concept_bullets.append(
                "- 💰 **Status DRIP-friendly** (US holding com DY ≥ 2.5%) — "
                "ver [[Glossary/DRIP]] para mecanismo + [[Glossary/Aristocrat]] "
                "para membership formal."
            )
        elif market == "br" and fund.get("dy", 0) >= 0.06:
            concept_bullets.append(
                "- 💰 **Status DRIP-friendly** (BR holding com DY ≥ 6%) — "
                "reinvestimento mensal/quarterly compõe."
            )
    if not is_bank and not is_fii:
        concept_bullets.append(
            "- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|"
            "margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). "
            "Sem ambos, qualquer screen é teatro."
        )

    if not bullets:
        return ""

    out = [
        "## Tutor",
        "",
        "> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). "
        "Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.",
        "",
    ]
    out.extend(bullets)
    if concept_bullets:
        out += ["", "### Conceitos relacionados", ""]
        out.extend(concept_bullets)
    out += ["", ""]
    return "\n".join(out)


_TUTOR_PATTERN = re.compile(
    r"\n## Tutor\n.*?(?=\n## |\n---\n\*Generated|\Z)",
    re.DOTALL,
)


def inject_tutor(path: Path) -> tuple[bool, str]:
    """Returns (changed, status_msg)."""
    text = path.read_text(encoding="utf-8")
    meta = _parse_meta(text)
    fund = _parse_fundamentals(text)
    if not fund:
        return False, "no_fundamentals"

    tutor = _build_tutor(meta, fund)
    if not tutor:
        return False, "no_tutor_built"

    # Strip existing Tutor section if present
    text = _TUTOR_PATTERN.sub("\n", text)

    # Insert before "## 5. " (or before any ## section that's "Riscos identificados") — fallback before footer
    insert_pos = text.find("\n## Riscos identificados")
    if insert_pos < 0:
        # try numbered: ## N. Riscos
        m = re.search(r"\n## \d+\. Riscos", text)
        if m:
            insert_pos = m.start()
    if insert_pos < 0:
        insert_pos = text.find("\n---\n*Generated")

    if insert_pos < 0:
        # append before EOF
        new_text = text.rstrip() + "\n\n" + tutor
    else:
        new_text = text[:insert_pos] + "\n" + tutor + text[insert_pos:].lstrip("\n")

    path.write_text(new_text, encoding="utf-8")
    return True, "injected"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", help="single ticker (otherwise process all)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.ticker:
        files = [DOSSIE_DIR / f"{args.ticker.upper()}_DOSSIE.md"]
    else:
        files = sorted(DOSSIE_DIR.glob("*_DOSSIE.md"))

    ok = skipped = err = 0
    for p in files:
        if not p.exists():
            err += 1
            print(f"  ✗ {p.name} not found")
            continue
        try:
            changed, status = inject_tutor(p)
            if changed:
                ok += 1
                if not args.quiet:
                    print(f"  ✓ {p.name}: {status}")
            else:
                skipped += 1
                if not args.quiet:
                    print(f"  · {p.name}: {status}")
        except Exception as e:
            err += 1
            print(f"  ERR {p.name}: {e}")

    print(f"\n[summary] injected={ok} skipped={skipped} errors={err} of {len(files)}")


if __name__ == "__main__":
    main()
