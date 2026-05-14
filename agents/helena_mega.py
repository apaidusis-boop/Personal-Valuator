"""MegaHelenaAgent — orchestrates audit + curate + spike + report.

Invoked manually or scheduled. Produces 4 artifacts in
`obsidian_vault/skills/design.lint_mega/`:

    00_MASTER.md      executive summary (read first)
    01_Audit.md       design system linter findings (DS001-DS009)
    02_Curation.md    39 community skills triaged (install/consider/skip)
    03_Spikes.md      4 platform paths (Streamlit/Tauri/Next.js/Obsidian)

Convocar:
    python agents/helena_mega.py                 # all 4 stages
    python agents/helena_mega.py audit           # one stage
    python agents/helena_mega.py curate
    python agents/helena_mega.py spike
    python agents/helena_mega.py report          # consolidator (re-runs audit in-mem)
    python agents/helena_mega.py --dry-run       # smoke-test, no write

Schedule:
    Helena Mega corre on-demand. Não é cron — é invocada quando o founder
    pede "Helena, mega review". Para watch automático use Helena Linha
    (scripts/design_research.py, weekly Sunday).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents._base import AgentContext, AgentResult, BaseAgent  # noqa: E402
from agents.helena import audit, curate, spike, report  # noqa: E402
from agents.helena import VAULT_OUT  # noqa: E402


class MegaHelenaAgent(BaseAgent):
    name = "helena_mega"
    description = (
        "Mega Helena — design audit + skill curation + 4-path platform spikes "
        "+ master consolidator. On-demand."
    )
    default_schedule = "manual"

    STAGES = ("audit", "curate", "spike", "report")

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        actions: list[str] = []
        errors: list[str] = []
        stages = self.config.get("stages") or list(self.STAGES)
        dry = ctx.dry_run

        if "audit" in stages:
            try:
                violations, file_meta, targets = audit.run(["scripts"])
                if not dry:
                    md = audit.render_md(violations, file_meta, targets)
                    (VAULT_OUT / "01_Audit.md").write_text(md, encoding="utf-8")
                actions.append(
                    f"audit · {len(violations)} violations · {len(targets)} files"
                )
            except Exception as e:
                errors.append(f"audit: {type(e).__name__}: {e}")

        if "curate" in stages:
            try:
                if not dry:
                    md = curate.render_md()
                    (VAULT_OUT / "02_Curation.md").write_text(md, encoding="utf-8")
                actions.append(f"curate · {len(curate.CANDIDATES)} candidates")
            except Exception as e:
                errors.append(f"curate: {type(e).__name__}: {e}")

        if "spike" in stages:
            try:
                if not dry:
                    md = spike.render_md()
                    (VAULT_OUT / "03_Spikes.md").write_text(md, encoding="utf-8")
                actions.append(f"spike · {len(spike.PATHS)} paths")
            except Exception as e:
                errors.append(f"spike: {type(e).__name__}: {e}")

        if "report" in stages:
            try:
                if not dry:
                    md = report.render_md()
                    (VAULT_OUT / "00_MASTER.md").write_text(md, encoding="utf-8")
                actions.append("report · 00_MASTER written")
            except Exception as e:
                errors.append(f"report: {type(e).__name__}: {e}")

        status = "ok" if actions and not errors else ("failed" if errors else "no_action")
        summary_parts = [a for a in actions]
        if errors:
            summary_parts.append(f"errors={len(errors)}")
        summary = " · ".join(summary_parts) or "no-op"

        return AgentResult(
            agent=self.name,
            status=status,
            summary=summary,
            started_at="", finished_at="", duration_sec=0,
            actions=actions, errors=errors,
            data={"stages_run": stages, "vault_out": str(VAULT_OUT.relative_to(ROOT))},
        )


# ────────────────── CLI ──────────────────


def _cli() -> int:
    ap = argparse.ArgumentParser(
        description="Mega Helena — design audit + curation + spikes + master report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "stage",
        nargs="?",
        default="all",
        choices=["all", "audit", "curate", "spike", "report"],
        help="Stage to run (default: all)",
    )
    ap.add_argument("--dry-run", action="store_true",
                    help="Compute everything but don't write files")
    args = ap.parse_args()

    stages = list(MegaHelenaAgent.STAGES) if args.stage == "all" else [args.stage]
    agent = MegaHelenaAgent(config={"stages": stages})
    ctx = AgentContext(root=ROOT, config={}, dry_run=args.dry_run, reason="manual")
    result = agent.execute(ctx)

    print(f"\n[helena_mega] status={result.status}  duration={result.duration_sec:.2f}s")
    for a in result.actions:
        print(f"  · {a}")
    for e in result.errors:
        print(f"  ! {e}")
    if not args.dry_run and result.status == "ok":
        print(f"\nartifacts in {VAULT_OUT.relative_to(ROOT)}:")
        for f in sorted(VAULT_OUT.glob("*.md")):
            print(f"  {f.relative_to(ROOT)}  ({f.stat().st_size} bytes)")

    return 0 if result.status in ("ok", "no_action") else 1


if __name__ == "__main__":
    raise SystemExit(_cli())
