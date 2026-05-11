"""Generate the curated 'human' morning summary that wraps _LEITURA_DA_MANHA.md.

Adds a TLDR at top + decision framework for $1.5k + sell candidates context.
Run AFTER overnight_orchestrator.py completes.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOMORROW = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
OUT_DIR = ROOT / "obsidian_vault" / f"Overnight_{TOMORROW}"
RI_URLS_YAML = ROOT / "config" / "ri_urls.yaml"


def count_dossiers() -> int:
    if not OUT_DIR.exists():
        return 0
    return len([f for f in OUT_DIR.glob("*.md")
                if not f.name.startswith("_")])


def yaml_stats() -> dict:
    if not RI_URLS_YAML.exists():
        return {"ok": 0, "failed": 0, "skipped": 0}
    with RI_URLS_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    stats = {"ok": 0, "failed": 0, "skipped": 0, "total": len(data)}
    for cfg in data.values():
        st = cfg.get("status", "")
        stats[st] = stats.get(st, 0) + 1
    return stats


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_dossiers = count_dossiers()
    yaml_st = yaml_stats()

    L = []
    L.append(f"# Bom dia ({TOMORROW})")
    L.append("")
    L.append("> Tu pediste um overnight deep-dive em todo o universo "
             "para decidir os $1,500 USD esta semana e ver candidatos "
             "para sell. Aqui está.")
    L.append("")

    L.append("## ⚡ Onde está cada coisa")
    L.append("")
    L.append("```")
    L.append(f"obsidian_vault/Overnight_{TOMORROW}/")
    L.append("├── _BOM_DIA.md          ← este ficheiro (TLDR humano)")
    L.append("├── _LEITURA_DA_MANHA.md ← relatório consolidado ($1.5k tabela)")
    L.append("├── _CODE_HEALTH.md      ← audit dos ficheiros novos")
    L.append("└── <TICKER>.md          ← dossier por ticker (~150-300 linhas cada)")
    L.append("```")
    L.append("")

    L.append("## 📋 TL;DR (3 minutos)")
    L.append("")
    L.append(f"- **Cobertura**: {n_dossiers} dossiers gerados de "
             f"{yaml_st.get('total', 0)} tickers no universo.")
    L.append(f"- **URL discovery**: {yaml_st.get('ok', 0)} ok, "
             f"{yaml_st.get('failed', 0)} failed (heuristic não match), "
             f"{yaml_st.get('skipped', 0)} skipped (ETFs).")
    L.append("- **Para o $1.5k**: vê tabela em `_LEITURA_DA_MANHA.md → "
             "Recomendação para $1,500 USD`. Top 3 ranked pelo composite "
             "(score nosso + filings novos + valuation simples + posição P/L).")
    L.append("- **Sell candidates**: vê \"Bottom 5\" na mesma secção. "
             "Score baixo + não passa screen + underwater = bandeira.")
    L.append("- **Sinais críticos**: secção 🚨 lista mudanças executivas, "
             "M&A, ofícios CVM/B3, downgrades, declarações dividend.")
    L.append("- **Sob-cobertura**: alguns tickers BR mid-cap falharam URL "
             "discovery. Lista em `_LEITURA_DA_MANHA.md → Errors`. "
             "Para mapear manualmente: editar `config/ri_urls.yaml`.")
    L.append("")

    L.append("## 🎯 Decisões para tomar hoje")
    L.append("")
    L.append("### Decisão 1: $1,500 USD esta semana")
    L.append("")
    L.append("Abre `_LEITURA_DA_MANHA.md` → `Recomendação para $1,500 USD`. ")
    L.append("Vê:")
    L.append("- **Top 8 candidatos** ordenados por composite score")
    L.append("- **Sugestão concreta** de alocação distribuída ou concentrada")
    L.append("- **Filings novos** que afectam cada um")
    L.append("")
    L.append("**Como decidir** (ordem de impacto):")
    L.append("1. Score nosso ≥0.6 + passa screen ✅")
    L.append("2. Aristocrat / streak ≥10 anos (DRIP qualidade)")
    L.append("3. Sem sinais 🚨 críticos negativos")
    L.append("4. P/L da posição actual (preferir ainda em desconto vs entry)")
    L.append("5. Alocação sectorial: evitar concentrar mais no sector "
             "que já dominas")
    L.append("")

    L.append("### Decisão 2: 2 sells para realocar")
    L.append("")
    L.append("Diz-me **quais 2 tickers** estás a pensar vender. Eu vou:")
    L.append("- Comparar contra os top picks (cross-sectional)")
    L.append("- Calcular P/L e tax impact (capital gains)")
    L.append("- Sugerir replacement no mesmo bucket sectorial")
    L.append("- Confirmar se o sell é tactical (perda controlada) "
             "ou strategic (mudança de tese)")
    L.append("")
    L.append("Ou consulta directamente \"Bottom 5\" no relatório auto-gen "
             "para ver os candidatos que o composite flagged.")
    L.append("")

    L.append("## ⚠️ Ressalvas honestas (não confiar 100%)")
    L.append("")
    L.append("- **Composite score é heurístico** — pondera score nosso + "
             "valuation simples + signals novos. Não é DCF formal.")
    L.append("- **Filings novos detectados podem incluir falsos positivos** "
             "(ex: BBDC4 detectou 27 mas ~12 são duplicados de DB com "
             "título ligeiramente diferente).")
    L.append("- **Sinais críticos auto-flagged usam keyword matching** — "
             "alguns são informacionais (ex: 'incorporação' pode ser "
             "M&A material OU rotina contábil).")
    L.append("- **Cobertura US watchlist baixa para tickers exóticos** — "
             "se um ticker te interessa mas não está coberto, manda-me "
             "URL do RI e re-corro single-ticker.")
    L.append("- **ITSA4 1T26 release esperado HOJE** — vê secção dedicada "
             "no relatório se já apanhei. Se não, corre "
             "`.venv\\Scripts\\python.exe scripts/morning_itsa4_check.py`.")
    L.append("")

    L.append("## 🔧 Comandos úteis para hoje")
    L.append("")
    L.append("```powershell")
    L.append("# Re-scrape ITSA4 para apanhar 1T26 release fresco")
    L.append(".venv\\Scripts\\python.exe scripts/morning_itsa4_check.py")
    L.append("")
    L.append("# Deep dive single ticker")
    L.append(".venv\\Scripts\\python.exe scripts/pilot_deep_dive.py --tickers TKR --force-fresh --deep")
    L.append("")
    L.append("# Re-run uma phase específica")
    L.append(".venv\\Scripts\\python.exe scripts/overnight_orchestrator.py --phase holdings_us")
    L.append("")
    L.append("# Ver as falhas de URL discovery")
    L.append("python -c \"import yaml; d=yaml.safe_load(open('config/ri_urls.yaml')); [print(t) for t,c in d.items() if c['status']=='failed']\"")
    L.append("```")
    L.append("")

    L.append("---")
    L.append(f"_Generated by `scripts/morning_curated.py` at "
             f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")

    out_path = OUT_DIR / "_BOM_DIA.md"
    out_path.write_text("\n".join(L), encoding="utf-8")
    print(f"Bom dia summary saved: {out_path}")
    return 0


if __name__ == "__main__":
    main()
