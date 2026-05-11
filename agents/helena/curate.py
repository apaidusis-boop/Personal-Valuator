"""curate — community skill go/no-go evaluator.

Static decision matrix for the community skills the founder dropped on 2026-04-25.
Each candidate is tiered against the in-house arsenal:

    INSTALL   — fills a real gap, recent, well-maintained, design-strong
    CONSIDER  — interesting but unclear fit; need 30-min spike before installing
    SKIP      — duplicates existing capability, out-of-scope, or noise

In-house arsenal already at hand (do NOT recommend duplicates):
    huashu-design       — high-fi prototypes, 5×20 design philosophies (~/.claude/skills/)
    ui-ux-pro-max-skill — 67 styles, 161 palettes, 57 font pairings, 99 UX rules
    hue                 — meta-skill that generates design language skills
    figma:figma-*       — full Figma toolkit (use_figma, code-connect, …)
    OneDrive/Claude/Skills/{design-system, theme-factory, Front Design}
    scripts/yt_ingest.py + library/rag — local YouTube + RAG (Phase Q + library)
    obsidian_vault + library — knowledge graph already built

Run:
    python -m agents.helena.curate
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import VAULT_OUT, ROOT


@dataclass
class Candidate:
    name: str                    # display name
    source: str                  # github repo, URL, or local path
    category: str                # design / dev / hooks / research / finance / productivity
    tier: str                    # INSTALL / CONSIDER / SKIP
    rationale: str               # 1-2 sentences why this tier
    duplicates: str = ""         # what we already have that overlaps
    fit_score: int = 0           # 0-100 internal fit score (for sorting)


# ────────────────── candidate inventory ──────────────────


CANDIDATES: list[Candidate] = [
    # ━━━━━━━━━━━━━━━━━━━━━━ design ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="designer-skills (julianoczkowski)",
        source="https://github.com/julianoczkowski/designer-skills",
        category="design",
        tier="INSTALL",
        rationale="7 skills mapping a real design process (research → wireframe → "
                  "high-fi → handoff). Helena flow currently jumps from brief to "
                  "code; this gives her the missing intermediate stages.",
        duplicates="Tangentially overlaps huashu-design (prototyping) but the "
                   "process scaffolding is different.",
        fit_score=88,
    ),
    Candidate(
        name="interface-design (Dammyjay93)",
        source="https://github.com/Dammyjay93/interface-design",
        category="design",
        tier="CONSIDER",
        rationale="Scope claims 'interface design'. Need to read SKILL.md before "
                  "deciding — risk of overlap with huashu-design prototyping mode.",
        duplicates="huashu-design app prototyping mode covers similar ground.",
        fit_score=58,
    ),
    Candidate(
        name="hue (dominikmartn)",
        source="https://github.com/dominikmartn/hue",
        category="design",
        tier="INSTALL",
        rationale="Already in ~/.claude/skills/. Confirm it's the latest version. "
                  "Generates design language skills from references.",
        duplicates="Already installed.",
        fit_score=100,
    ),
    Candidate(
        name="huashu-design",
        source="https://github.com/alchaincyf/huashu-design",
        category="design",
        tier="INSTALL",
        rationale="Already installed. Hi-fi prototyping + 5 streams × 20 philosophies "
                  "+ video export. Underused — should be Helena's go-to for protótipos.",
        duplicates="Already installed.",
        fit_score=100,
    ),
    Candidate(
        name="ui-ux-pro-max-skill",
        source="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
        category="design",
        tier="INSTALL",
        rationale="Already installed. 67 UI styles + 161 palettes + 57 font pairs. "
                  "Use as reference DB when picking variants for new pages.",
        duplicates="Already installed.",
        fit_score=100,
    ),
    Candidate(
        name="OneDrive/Claude/Skills/design-system",
        source="C:/Users/paidu/OneDrive/Claude/Skills/design-system",
        category="design",
        tier="CONSIDER",
        rationale="Local copy with components/layouts/showcase/themes/tokens. "
                  "Audit overlap with our Helena Design System v1.0 — keep best.",
        duplicates="Helena Design_System.md v1.0",
        fit_score=55,
    ),
    Candidate(
        name="OneDrive/Claude/Skills/theme-factory",
        source="C:/Users/paidu/OneDrive/Claude/Skills/theme-factory",
        category="design",
        tier="CONSIDER",
        rationale="Has theme-showcase.pdf — read it; if useful, integrate as "
                  "reference for Path B (Tauri) theme rollout.",
        duplicates="scripts/_theme.py defines our tokens already",
        fit_score=50,
    ),
    Candidate(
        name="OneDrive/Claude/Skills/Front Design (frontend-design.md)",
        source="C:/Users/paidu/OneDrive/Claude/Skills/Front  Design",
        category="design",
        tier="CONSIDER",
        rationale="Single .md skill. Open and audit before deciding.",
        fit_score=40,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ finance ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="Snyk — Top Claude Skills for Finance/Quant",
        source="https://snyk.io/pt-BR/articles/top-claude-skills-finance-quantitative-developers/",
        category="finance",
        tier="CONSIDER",
        rationale="Article (not a skill repo). Triage 2-3 specific skills it "
                  "recommends; install only if they touch DCF, screener or risk.",
        fit_score=55,
    ),
    Candidate(
        name="CFO Connect — Claude for Finance Teams",
        source="https://www.cfoconnect.eu/resources/event-recaps/claude-for-finance-teams/",
        category="finance",
        tier="SKIP",
        rationale="Talk recap, not code. Extract 2-3 patterns into vault if any "
                  "stand out, no install needed.",
        fit_score=20,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ dev workflow ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="Superpowers (obra)",
        source="https://github.com/obra/superpowers",
        category="dev",
        tier="SKIP",
        rationale="Brainstorming + TDD enforcement + execution planning. Overkill "
                  "for a 1-dev personal project; we already have perpetuums for "
                  "structured work.",
        duplicates="agents/perpetuum_master.py + Plan mode",
        fit_score=22,
    ),
    Candidate(
        name="Superpowers Lab (obra)",
        source="https://github.com/obra/superpowers-lab",
        category="dev",
        tier="SKIP",
        rationale="Bleeding-edge fork of Superpowers. Same reason to skip.",
        duplicates="agents/perpetuum_master.py",
        fit_score=18,
    ),
    Candidate(
        name="Skill Seekers (yusufkaraaslan)",
        source="https://github.com/yusufkaraaslan/Skill_Seekers",
        category="dev",
        tier="CONSIDER",
        rationale="Auto-generates a skill from any docs site/PDF. Concrete use: "
                  "feed it Bigdata.com docs + yfinance docs + brapi.dev docs to "
                  "get 3 lookup skills. 1h test before committing.",
        fit_score=68,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ research / knowledge ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="Tapestry (knowledge graph from PDFs)",
        source="awesome-claude-skills (BehiSecc)",
        category="research",
        tier="SKIP",
        rationale="Builds knowledge graphs from PDFs. We already have library/rag "
                  "(nomic-embed local) + Obsidian vault + library/ingest pipeline.",
        duplicates="library/rag, library/ingest, obsidian_vault",
        fit_score=15,
    ),
    Candidate(
        name="YouTube Transcript / Article Extractor",
        source="awesome-claude-skills (BehiSecc)",
        category="research",
        tier="SKIP",
        rationale="Claude-side YouTube ingestion. We have scripts/yt_ingest.py v2 "
                  "(Phase Q) — local Whisper + Ollama, zero tokens.",
        duplicates="scripts/yt_ingest.py, scripts/yt_reextract.py, scripts/yt_digest.py",
        fit_score=10,
    ),
    Candidate(
        name="Brainstorming Skill",
        source="superpowers (obra)",
        category="research",
        tier="SKIP",
        rationale="Structured brainstorming. We have agents/synthetic_ic.py "
                  "(Buffett+Druck+Taleb+Klarman+Dalio debate) which is more "
                  "domain-specific.",
        duplicates="agents/synthetic_ic.py",
        fit_score=20,
    ),
    Candidate(
        name="Content Research Writer (citations)",
        source="awesome-claude-skills (BehiSecc)",
        category="research",
        tier="SKIP",
        rationale="Adds citations + iterates. Not a writing-heavy workflow here; "
                  "founder writes own theses, agents generate structured memos.",
        fit_score=15,
    ),
    Candidate(
        name="EPUB / PDF Analyzer",
        source="awesome-claude-skills (BehiSecc)",
        category="research",
        tier="SKIP",
        rationale="Summarizes/queries ebooks. We have library/extract_insights "
                  "(Ollama local) — similar with Buffett/Klarman/Druckenmiller "
                  "playbook lens.",
        duplicates="library/ingest + library/extract_insights",
        fit_score=12,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ productivity ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="Invoice / File Organizer",
        source="awesome-claude-skills (BehiSecc)",
        category="productivity",
        tier="SKIP",
        rationale="Organizes receipts/invoices. Out of scope for investment "
                  "intelligence project.",
        fit_score=5,
    ),
    Candidate(
        name="Web Asset Generator (icons, OG, PWA)",
        source="awesome-claude-skills (BehiSecc) / travisvn",
        category="productivity",
        tier="CONSIDER",
        rationale="If we go Path B (Tauri) or Path C (Next.js), need favicon, "
                  "icons, OG tags. Install only when we commit to a path with web/web-app surface.",
        fit_score=45,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ hooks ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="johnlindquist/claude-hooks",
        source="https://github.com/johnlindquist/claude-hooks",
        category="hooks",
        tier="CONSIDER",
        rationale="TypeScript hook framework. Useful if we want to enforce "
                  "Helena audit on save. But adds a TS dependency to a Python "
                  "project — evaluate cost/benefit.",
        fit_score=42,
    ),
    Candidate(
        name="CCHooks (GowayLee)",
        source="github GowayLee/CCHooks",
        category="hooks",
        tier="CONSIDER",
        rationale="Python equivalent of johnlindquist. Better fit for our stack; "
                  "could trigger `python -m agents.helena.audit` on PreToolUse "
                  "Edit/Write to scripts/.",
        fit_score=72,
    ),
    Candidate(
        name="claude-code-hooks-sdk (beyondcode)",
        source="github beyondcode/claude-code-hooks-sdk",
        category="hooks",
        tier="SKIP",
        rationale="PHP/Laravel-style. Not our stack.",
        fit_score=5,
    ),
    Candidate(
        name="Claudio (Christopher Toth — sound effects)",
        source="github Christopher Toth Claudio",
        category="hooks",
        tier="CONSIDER",
        rationale="OS-native sounds on Claude events. Cosmetic but mildly useful "
                  "for long perpetuum runs (overnight).",
        fit_score=35,
    ),
    Candidate(
        name="CC Notify (desktop notifications)",
        source="awesome-claude-code (hesreallyhim)",
        category="hooks",
        tier="CONSIDER",
        rationale="Desktop notification on completion. Overlaps with our "
                  "Telegram push (notifiers/telegram.py); could complement it "
                  "for in-front-of-PC sessions.",
        duplicates="notifiers/telegram.py",
        fit_score=48,
    ),
    Candidate(
        name="codeinbox/claude-code-discord",
        source="https://github.com/codeinbox/claude-code-discord",
        category="hooks",
        tier="SKIP",
        rationale="Discord/Slack notification. We already use Telegram (Phase V "
                  "Jarbas bot).",
        duplicates="notifiers/telegram.py + Jarbas bot",
        fit_score=10,
    ),
    Candidate(
        name="fcakyon Code Quality Hooks",
        source="awesome-claude-code (hesreallyhim)",
        category="hooks",
        tier="SKIP",
        rationale="Linting + TDD enforcement collection. Too generic; we'd want "
                  "Helena audit specifically on UI files, not blanket TDD.",
        fit_score=18,
    ),
    Candidate(
        name="bartolli TypeScript Quality Hooks",
        source="awesome-claude-code (hesreallyhim)",
        category="hooks",
        tier="SKIP",
        rationale="TypeScript-specific. Out of scope unless we go Path B (Tauri) "
                  "or Path C (Next.js); revisit then.",
        fit_score=15,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ security ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="ffuf_claude_skill",
        source="awesome-claude-skills (BehiSecc)",
        category="security",
        tier="SKIP",
        rationale="Security fuzzing. Out of scope for investment intelligence.",
        fit_score=2,
    ),
    Candidate(
        name="Defense-in-Depth Skill",
        source="awesome-claude-skills (BehiSecc)",
        category="security",
        tier="SKIP",
        rationale="Multi-layer security. Out of scope.",
        fit_score=2,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ dev (extra) ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="Test-Driven Development Skill",
        source="superpowers (obra) / awesome-claude-skills",
        category="dev",
        tier="SKIP",
        rationale="TDD enforcement. Personal project; tests exist where they "
                  "matter (analytics, scoring), not blanket.",
        fit_score=20,
    ),
    Candidate(
        name="Systematic Debugging Skill",
        source="superpowers (obra)",
        category="dev",
        tier="CONSIDER",
        rationale="Forces root-cause analysis vs random fixes. Aligned with "
                  "founder's preference (memory: 'feedback_inhouse_first').",
        fit_score=55,
    ),
    Candidate(
        name="Finishing a Development Branch Skill",
        source="awesome-claude-skills (BehiSecc)",
        category="dev",
        tier="SKIP",
        rationale="PR cleanup workflow. We use small commits + manual PR; "
                  "minor friction not worth a skill.",
        fit_score=18,
    ),
    Candidate(
        name="Git Worktrees Skill",
        source="awesome-claude-skills (BehiSecc)",
        category="dev",
        tier="SKIP",
        rationale="Multi-branch worktrees. Solo dev on main most of the time.",
        fit_score=15,
    ),
    Candidate(
        name="Pypict (combinatorial testing)",
        source="awesome-claude-skills (BehiSecc)",
        category="dev",
        tier="SKIP",
        rationale="Generates QA test matrices. Heavy infra for personal scope.",
        fit_score=10,
    ),
    Candidate(
        name="Webapp Testing with Playwright",
        source="awesome-claude-skills (BehiSecc)",
        category="dev",
        tier="CONSIDER",
        rationale="E2E testing. Becomes relevant if we go Path B (Tauri) or "
                  "Path C (Next.js); already have SKL_playwright_mcp.md noted.",
        duplicates="obsidian_vault/skills/SKL_playwright_mcp.md (already evaluated)",
        fit_score=42,
    ),

    # ━━━━━━━━━━━━━━━━━━━━━━ catalogs (read-only) ━━━━━━━━━━━━━━━━━━━━━━
    Candidate(
        name="awesome-claude-skills (BehiSecc)",
        source="https://github.com/BehiSecc/awesome-claude-skills",
        category="catalog",
        tier="CONSIDER",
        rationale="Curated index. Use as discovery, not install. Re-scan monthly "
                  "via Helena scout.",
        fit_score=60,
    ),
    Candidate(
        name="awesome-claude-skills (travisvn)",
        source="https://github.com/travisvn/awesome-claude-skills",
        category="catalog",
        tier="CONSIDER",
        rationale="Second curated index. Cross-reference with BehiSecc's.",
        fit_score=55,
    ),
    Candidate(
        name="awesome-claude-code (hesreallyhim)",
        source="https://github.com/hesreallyhim/awesome-claude-code",
        category="catalog",
        tier="CONSIDER",
        rationale="Hooks-focused index. Use when we decide on hook strategy.",
        fit_score=55,
    ),
]


# ────────────────── render ──────────────────


def render_md() -> str:
    today = date.today().isoformat()
    by_tier: dict[str, list[Candidate]] = {"INSTALL": [], "CONSIDER": [], "SKIP": []}
    for c in CANDIDATES:
        by_tier[c.tier].append(c)
    for t in by_tier:
        by_tier[t].sort(key=lambda c: -c.fit_score)

    counts = {t: len(by_tier[t]) for t in by_tier}

    out = [
        "---",
        "type: skill_curation",
        f"updated: {today}",
        "owner: helena_linha",
        "tags: [skills, curation, helena, mega]",
        "---",
        "",
        "# 02 — Skill curation",
        "",
        f"> Helena Mega · run **{today}** · {len(CANDIDATES)} candidatos avaliados · "
        f"**{counts['INSTALL']}** install / **{counts['CONSIDER']}** consider / "
        f"**{counts['SKIP']}** skip",
        "",
        "## Princípio",
        "",
        "Excesso de skills = AI slop. Cada install adiciona context que disputa atenção; "
        "5 skills bem usadas > 30 instaladas. Critério hard:",
        "",
        "1. **Preenche um gap real** que o arsenal in-house não cobre",
        "2. **Manutenção activa** (commit em ≤180 dias)",
        "3. **Não duplica** capability já existente",
        "4. **Domain fit** — investment intelligence, design, ou developer workflow",
        "",
        "## Arsenal in-house (referência)",
        "",
        "Capabilities que já temos — **não recomendar duplicados**:",
        "",
        "| Capability | Onde |",
        "|---|---|",
        "| YouTube ingestion local | `scripts/yt_ingest.py` (Phase Q v2) |",
        "| RAG semantic search | `library/rag` (nomic-embed local + Qwen) |",
        "| Knowledge graph | `obsidian_vault` + `library/ingest` |",
        "| Method extraction (Buffett/Druck/…) | `library/extract_insights` |",
        "| Synthetic IC debate | `agents/synthetic_ic.py` |",
        "| Telegram push | `notifiers/telegram.py` + Jarbas bot |",
        "| Design System v1.0 | `obsidian_vault/skills/Design_System.md` |",
        "| Design tokens / CSS | `scripts/_theme.py` |",
        "| Reusable components | `scripts/_components.py` |",
        "| Hi-fi prototyping | `huashu-design` skill |",
        "| Style/palette/typography DB | `ui-ux-pro-max-skill` |",
        "| Design language generator | `hue` skill |",
        "| Figma toolkit | `figma:figma-*` skills |",
        "| Perpetuum / autonomy | `agents/perpetuum_master.py` (Phase X) |",
        "",
    ]

    tier_blurb = {
        "INSTALL": "Instalar (ou já instalado e em uso). Preenche gap real.",
        "CONSIDER": "30-min spike antes de decidir. Risco de duplicar ou ser overhead.",
        "SKIP": "Não instalar — duplica capability existente, fora de scope, ou abandonware.",
    }

    for tier in ["INSTALL", "CONSIDER", "SKIP"]:
        rows = by_tier[tier]
        out += [
            f"## {tier} ({len(rows)})",
            "",
            f"_{tier_blurb[tier]}_",
            "",
            "| Skill | Categoria | Fit | Razão |",
            "|---|---|---:|---|",
        ]
        for c in rows:
            rationale = c.rationale.replace("|", "\\|")[:280]
            cat = c.category
            out.append(f"| **[{c.name}]({c.source})** | {cat} | {c.fit_score} | {rationale} |")
        out.append("")
        # Detailed duplicates section per tier
        with_dupes = [c for c in rows if c.duplicates]
        if with_dupes and tier in ("CONSIDER", "SKIP"):
            out.append(f"### Duplicações detectadas ({tier.lower()})")
            out.append("")
            for c in with_dupes:
                out.append(f"- **{c.name}** ↔ {c.duplicates}")
            out.append("")

    out += [
        "## Próximas acções (proposta Helena)",
        "",
        "1. **Confirmar in-place** — `huashu-design`, `hue`, `ui-ux-pro-max-skill` "
        "estão em `~/.claude/skills/`. Helena começa a usá-los activamente em "
        "todo prototype novo (ver `Claude_Design_Integration.md`).",
        "2. **Instalar `julianoczkowski/designer-skills`** — adiciona o process "
        "(research → wireframe → high-fi → handoff) que a casa não tem.",
        "3. **30-min spikes (em paralelo, baixo custo)**:",
        "   - `Dammyjay93/interface-design` — abrir SKILL.md, comparar com huashu-design",
        "   - OneDrive/{design-system, theme-factory, Front Design} — auditar conteúdo, "
        "promover o útil para `obsidian_vault/skills/`",
        "   - `Skill_Seekers` — 1 teste real: gerar skill a partir de docs `brapi.dev`",
        "   - `CCHooks` (Python) — wire `python -m agents.helena.audit` em PreToolUse hook",
        "4. **Adiar até decidir Path A/B/C/D**:",
        "   - Web Asset Generator (só relevante se houver web surface)",
        "   - Playwright skills (só relevante para Path B/C)",
        "   - bartolli TS hooks (só relevante para Path B/C)",
        "5. **Definitivamente não instalar** — todos os SKIP acima. Razões na tabela.",
        "",
        "## Cross-links",
        "",
        "- [[Design_Watch]] — re-scan semanal automático de novos repos",
        "- [[Claude_Design_Integration]] — Anthropic Labs prototyping flow",
        "- [[Helena Linha]] — owner",
        "",
    ]

    return "\n".join(out)


def main() -> int:
    import sys
    ap = argparse.ArgumentParser(description="Helena skill curation")
    ap.add_argument("--print", action="store_true")
    args = ap.parse_args()

    md = render_md()

    if args.print:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        sys.stdout.write(md + "\n")
        return 0

    out_path = VAULT_OUT / "02_Curation.md"
    out_path.write_text(md, encoding="utf-8")
    counts = {"INSTALL": 0, "CONSIDER": 0, "SKIP": 0}
    for c in CANDIDATES:
        counts[c.tier] += 1
    print(f"wrote {out_path.relative_to(ROOT)} · {len(CANDIDATES)} candidates "
          f"({counts['INSTALL']} install / {counts['CONSIDER']} consider / "
          f"{counts['SKIP']} skip)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
