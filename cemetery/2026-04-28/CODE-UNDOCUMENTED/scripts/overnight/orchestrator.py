"""Overnight master orchestrator — corre múltiplas fases sequenciais.

Cada fase tem timeout + try/catch próprio. Se uma falha, outras continuam.
Output final: MORNING_REPORT.md em root com resumo completo.

Phases:
  P1: Populate ## Thesis em holdings sem thesis (~30 min com Qwen 14B)
  P2: Generate 10 new YAML methods from Damodaran (~5 min)
  P3: Run matcher — todos methods × holdings + watchlist (~2 min)
  P4: Perpetuum master full run (~10 sec)
  P5: Batch RAG research (20 strategic queries) (~30-60 min)
  P6: Build MORNING_REPORT.md aggregating everything

Total estimated: 70-100 min wall-clock. Zero Claude tokens.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PY = sys.executable  # current python

PHASES: list[dict] = [
    {
        "id": "P1_thesis",
        "name": "Populate ## Thesis em holdings sem thesis",
        "cmd": [PY, "scripts/overnight/populate_thesis.py"],
        "timeout": 3600,   # 1h
    },
    {
        "id": "P2_methods",
        "name": "Generate 10 new YAML methods from Damodaran",
        "cmd": [PY, "scripts/overnight/generate_methods_from_damodaran.py", "10"],
        "timeout": 900,    # 15 min
    },
    {
        "id": "P3_matcher",
        "name": "Run matcher — all methods × all tickers",
        "cmd": [PY, "-m", "library.matcher"],
        "timeout": 600,
    },
    {
        "id": "P4_perpetuum",
        "name": "Perpetuum master full run",
        "cmd": [PY, "agents/perpetuum_master.py"],
        "timeout": 300,
    },
    {
        "id": "P5_rag",
        "name": "Batch RAG research (20 strategic queries)",
        "cmd": [PY, "scripts/overnight/rag_research_batch.py"],
        "timeout": 4800,   # 80 min
    },
]


def run_phase(phase: dict) -> dict:
    print(f"\n=== [{phase['id']}] {phase['name']} ===")
    t0 = time.time()
    log_path = ROOT / "data" / "overnight" / f"{phase['id']}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        proc = subprocess.run(
            phase["cmd"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=phase["timeout"],
            encoding="utf-8",
            errors="replace",
        )
        log_path.write_text(
            f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}",
            encoding="utf-8",
        )
        elapsed = time.time() - t0
        status = "ok" if proc.returncode == 0 else "fail"
        print(f"  {status} in {elapsed:.1f}s  exit={proc.returncode}")
        return {
            "phase_id": phase["id"],
            "name": phase["name"],
            "status": status,
            "exit_code": proc.returncode,
            "duration_sec": elapsed,
            "stdout_tail": (proc.stdout or "")[-2000:],
            "stderr_tail": (proc.stderr or "")[-500:],
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        print(f"  TIMEOUT after {elapsed:.1f}s")
        return {"phase_id": phase["id"], "name": phase["name"],
                "status": "timeout", "duration_sec": elapsed}
    except Exception as e:
        return {"phase_id": phase["id"], "name": phase["name"],
                "status": "error", "error": str(e)}


def collect_metrics() -> dict:
    """Capture current DB state for morning report."""
    import sqlite3
    metrics = {
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    # Perpetuum health rows
    with sqlite3.connect(ROOT / "data" / "br_investments.db") as c:
        metrics["perpetuum_health_total"] = c.execute("SELECT COUNT(*) FROM perpetuum_health").fetchone()[0]
        metrics["perpetuum_health_by_name"] = dict(c.execute(
            "SELECT perpetuum_name, COUNT(*) FROM perpetuum_health GROUP BY perpetuum_name"
        ).fetchall())

    # Paper signals
    for mkt, dbn in [("br", "br_investments.db"), ("us", "us_investments.db")]:
        with sqlite3.connect(ROOT / "data" / dbn) as c:
            metrics[f"paper_signals_open_{mkt}"] = c.execute(
                "SELECT COUNT(*) FROM paper_trade_signals WHERE status='open'"
            ).fetchone()[0]
            metrics[f"paper_methods_{mkt}"] = c.execute(
                "SELECT COUNT(DISTINCT method_id) FROM paper_trade_signals WHERE status='open'"
            ).fetchone()[0]

    # Vault stats
    vault_tickers = ROOT / "obsidian_vault" / "tickers"
    with_thesis = sum(1 for p in vault_tickers.glob("*.md") if "## Thesis" in p.read_text(encoding="utf-8", errors="ignore"))
    metrics["vault_tickers_with_thesis"] = with_thesis
    metrics["vault_total_tickers"] = len(list(vault_tickers.glob("*.md")))

    # Methods
    metrics["yaml_methods_count"] = len(list((ROOT / "library" / "methods").glob("*.yaml")))

    # RAG
    with sqlite3.connect(ROOT / "library" / "chunks_index.db") as c:
        metrics["rag_chunks_indexed"] = c.execute("SELECT COUNT(*) FROM chunk_index").fetchone()[0]

    return metrics


def build_morning_report(results: list[dict], pre_metrics: dict, post_metrics: dict) -> None:
    lines = [
        "---",
        f"type: morning_report",
        f"date: {date.today().isoformat()}",
        f"tags: [overnight, report, autonomous]",
        "---",
        "",
        f"# 🌅 Morning Report — {date.today().isoformat()}",
        "",
        "> Trabalho autónomo overnight. Tudo local, zero tokens Claude consumidos.",
        "",
        "## ✅ Fases executadas",
        "",
        "| # | Phase | Status | Duration | Notes |",
        "|---|---|---|---:|---|",
    ]
    total_duration = 0
    for i, r in enumerate(results, 1):
        status = r.get("status", "?")
        badge = {"ok": "✅", "fail": "❌", "timeout": "⏰", "error": "💥"}.get(status, "?")
        dur = r.get("duration_sec", 0)
        total_duration += dur
        notes = ""
        if status == "ok":
            # Extract key info from stdout_tail
            tail = r.get("stdout_tail", "")[-200:]
            notes = tail.replace("\n", " ").strip()[:80]
        elif status != "ok":
            err = r.get("error") or r.get("stderr_tail", "")[-100:]
            notes = str(err)[:80]
        lines.append(f"| {i} | {r['name'][:48]} | {badge} {status} | {dur:.0f}s | `{notes}` |")

    lines.append(f"\n**Total**: {len(results)} phases in {total_duration/60:.1f} min\n")

    # Delta metrics
    lines.append("## 📊 Deltas antes/depois overnight")
    lines.append("")
    lines.append("| Metric | Before | After | Delta |")
    lines.append("|---|---:|---:|---:|")
    for key in sorted(set(pre_metrics) | set(post_metrics)):
        if key in ("captured_at", "perpetuum_health_by_name"):
            continue
        b = pre_metrics.get(key, "-")
        a = post_metrics.get(key, "-")
        delta = ""
        if isinstance(b, (int, float)) and isinstance(a, (int, float)):
            d = a - b
            delta = f"+{d}" if d > 0 else str(d)
        lines.append(f"| `{key}` | {b} | {a} | {delta} |")

    lines.append("")
    # Perpetuum breakdown
    lines.append("## 🔁 Perpetuum health breakdown")
    lines.append("")
    lines.append("| Perpetuum | Rows before | Rows after |")
    lines.append("|---|---:|---:|")
    pre_p = pre_metrics.get("perpetuum_health_by_name", {})
    post_p = post_metrics.get("perpetuum_health_by_name", {})
    for p in sorted(set(pre_p) | set(post_p)):
        lines.append(f"| {p} | {pre_p.get(p, 0)} | {post_p.get(p, 0)} |")

    # Where to look
    lines.append("")
    lines.append("## 📂 Output locations")
    lines.append("")
    lines.append(f"- `data/overnight/*.log` — per-phase logs")
    lines.append(f"- `obsidian_vault/briefings/overnight_research_{date.today().isoformat()}/` — 20 RAG research answers")
    lines.append(f"- `library/methods/damodaran_auto_*.yaml` — new YAML methods")
    lines.append(f"- `obsidian_vault/tickers/*.md` — updated with ## Thesis sections")
    lines.append(f"- `data/br_investments.db` / `us_investments.db` — new paper_trade_signals + perpetuum_health rows")
    lines.append("")

    lines.append("## 🚦 Quick checks")
    lines.append("")
    lines.append("```bash")
    lines.append("# Ver RAG research batch")
    lines.append(f"cat obsidian_vault/briefings/overnight_research_{date.today().isoformat()}/index.md")
    lines.append("")
    lines.append("# Ver novos methods YAML")
    lines.append("ls library/methods/damodaran_auto_*.yaml")
    lines.append("")
    lines.append("# Ver signals convergentes (>1 method) após overnight")
    lines.append("sqlite3 data/br_investments.db 'SELECT ticker, COUNT(DISTINCT method_id) FROM paper_trade_signals WHERE status=\"open\" GROUP BY ticker HAVING COUNT(DISTINCT method_id)>=2'")
    lines.append("")
    lines.append("# Current thesis coverage")
    lines.append("grep -l '## Thesis' obsidian_vault/tickers/*.md | wc -l")
    lines.append("```")
    lines.append("")

    report_path = ROOT / "MORNING_REPORT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nMORNING_REPORT.md written.")


def main() -> None:
    started = datetime.now(timezone.utc)
    print(f"=== Overnight Orchestrator — started {started.isoformat()} ===")

    pre = collect_metrics()
    print(f"Pre-metrics captured: perpetuum={pre['perpetuum_health_total']}  thesis={pre['vault_tickers_with_thesis']}")

    results = []
    for phase in PHASES:
        r = run_phase(phase)
        results.append(r)

    post = collect_metrics()
    print(f"Post-metrics captured: perpetuum={post['perpetuum_health_total']}  thesis={post['vault_tickers_with_thesis']}")

    # Save full raw run log
    raw_path = ROOT / "data" / "overnight" / "orchestrator_run.json"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps({
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "pre_metrics": pre,
        "post_metrics": post,
        "phases": results,
    }, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    build_morning_report(results, pre, post)
    print("\nDone. Check MORNING_REPORT.md")


if __name__ == "__main__":
    main()
