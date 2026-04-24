"""agents_cli — manage + run agents. Wrapped por `ii agents <cmd>`.

Comandos:
    ii agents list                      # lista todos registered
    ii agents status                    # dashboard
    ii agents run <name> [--dry-run]    # execução manual
    ii agents run-due                   # executa todos schedule-due agora
    ii agents enable <name>
    ii agents disable <name>
    ii agents create <name> --schedule "daily:07:00" --desc "..."
    ii agents logs <name> [--tail N]
    ii agents show <name>               # config + state + status
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from agents._registry import list_agents, find_registration, AGENTS_YAML  # noqa: E402
from agents._runner import run_by_name, run_all_due  # noqa: E402
from agents._state import AgentState  # noqa: E402


def cmd_list(args):
    regs = list_agents()
    if not regs:
        print("(no agents registered — edit config/agents.yaml)")
        return
    print(f"{'NAME':<22} {'ENABLED':<8} {'SCHEDULE':<22} {'LAST RUN':<22} {'STATUS':<12} RUNS")
    for reg, agent in regs:
        state = AgentState(reg.name, root=ROOT)
        d = state.as_dict()
        last_run = d.get("last_run") or "(never)"
        status = d.get("last_status") or "-"
        runs = d.get("run_count", 0)
        enabled = "✓" if reg.enabled else "✗"
        loaded = "" if agent else " [FAIL LOAD]"
        print(f"{reg.name:<22} {enabled:<8} {reg.schedule:<22} {last_run[:19]:<22} {status:<12} {runs}{loaded}")


def cmd_status(args):
    print(f"Agents config: {AGENTS_YAML}")
    print(f"Data dir: {ROOT / 'data' / 'agents'}")
    regs = list_agents()
    ok = sum(1 for _, a in regs if a is not None)
    print(f"\n{len(regs)} agents registered ({ok} loaded OK)")
    print()
    for reg, agent in regs:
        state = AgentState(reg.name, root=ROOT).as_dict()
        icon = {"ok": "✅", "no_action": "·", "failed": "❌", "skipped": "⏭"}.get(state.get("last_status"), "?")
        print(f"  {icon} {reg.name}")
        print(f"      schedule: {reg.schedule}  enabled: {reg.enabled}")
        print(f"      last:     {state.get('last_run') or '(never)'}  status: {state.get('last_status') or '-'}")
        print(f"      runs:     {state.get('run_count',0)}  failed: {state.get('failed_count',0)}")


def cmd_run(args):
    result = run_by_name(args.name, ROOT, dry_run=args.dry_run)
    if result is None:
        print(f"agent '{args.name}' not found in config/agents.yaml")
        return 1
    icon = {"ok": "✅", "no_action": "·", "failed": "❌", "skipped": "⏭"}.get(result.status, "?")
    print(f"\n{icon} {result.agent} — {result.status}  ({result.duration_sec:.1f}s)")
    print(f"Summary: {result.summary}")
    if result.actions:
        print("\nActions:")
        for a in result.actions:
            print(f"  ✓ {a}")
    if result.errors:
        print("\nErrors:")
        for e in result.errors:
            print(f"  ❌ {e}")
    return 0 if result.status != "failed" else 1


def cmd_run_due(args):
    print("[runner] checking schedules...")
    results = run_all_due(ROOT, dry_run=args.dry_run)
    if not results:
        print("[runner] no agents due")
        return
    print(f"\n{len(results)} agents ran:")
    for r in results:
        icon = {"ok": "✅", "no_action": "·", "failed": "❌"}.get(r.status, "?")
        print(f"  {icon} {r.agent} ({r.duration_sec:.1f}s) — {r.summary[:80]}")


def _toggle(name: str, enable: bool):
    try:
        import yaml
    except ImportError:
        print("pyyaml required")
        return 1
    if not AGENTS_YAML.exists():
        print(f"no {AGENTS_YAML}")
        return 1
    data = yaml.safe_load(AGENTS_YAML.read_text(encoding="utf-8")) or {}
    found = False
    for entry in data.get("agents", []):
        if entry["name"] == name:
            entry["enabled"] = enable
            found = True
            break
    if not found:
        print(f"agent '{name}' not found")
        return 1
    AGENTS_YAML.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"✓ {name} {'enabled' if enable else 'disabled'}")


def cmd_enable(args):
    return _toggle(args.name, True)


def cmd_disable(args):
    return _toggle(args.name, False)


def cmd_create(args):
    """Scaffolds new agent from template."""
    name = args.name.lower().replace("-", "_")
    class_name = "".join(p.capitalize() for p in name.split("_")) + "Agent"
    template_path = ROOT / "agents" / "templates" / "periodic.py.tpl"
    if not template_path.exists():
        print(f"template missing: {template_path}")
        return 1
    target = ROOT / "agents" / f"{name}.py"
    if target.exists():
        print(f"✗ agent '{name}' already exists at {target}")
        return 1
    tpl = template_path.read_text(encoding="utf-8")
    content = (tpl
               .replace("{{AGENT_NAME}}", name)
               .replace("{{AGENT_CLASS}}", class_name)
               .replace("{{DESCRIPTION}}", args.desc)
               .replace("{{SCHEDULE}}", args.schedule))
    target.write_text(content, encoding="utf-8")
    print(f"✓ scaffolded {target}")
    # Append to config/agents.yaml
    try:
        import yaml
        data = yaml.safe_load(AGENTS_YAML.read_text(encoding="utf-8")) or {"agents": []}
        data.setdefault("agents", []).append({
            "name": name,
            "class": f"agents.{name}:{class_name}",
            "enabled": True,
            "schedule": args.schedule,
            "description": args.desc,
            "config": {},
        })
        AGENTS_YAML.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(f"✓ registered in {AGENTS_YAML}")
    except Exception as e:
        print(f"⚠ could not auto-register (edit {AGENTS_YAML} manually): {e}")
    print(f"\nNext steps:")
    print(f"  1. Edit {target} — implement execute_impl()")
    print(f"  2. ii agents run {name}  (manual test)")
    print(f"  3. ii agents enable/disable {name}")


def cmd_show(args):
    reg = find_registration(args.name)
    if not reg:
        print(f"agent '{args.name}' not found")
        return 1
    state = AgentState(args.name, root=ROOT).as_dict()
    print(f"=== {reg.name} ===")
    print(f"class:       {reg.class_path}")
    print(f"description: {reg.description}")
    print(f"schedule:    {reg.schedule}")
    print(f"enabled:     {reg.enabled}")
    print(f"config:      {reg.config}")
    print(f"\nState:")
    for k, v in state.items():
        print(f"  {k}: {v}")


def cmd_logs(args):
    log_dir = ROOT / "logs" / "agents"
    if not log_dir.exists():
        print("(no logs yet)")
        return
    files = sorted(log_dir.glob(f"{args.name}_*.log"), reverse=True)
    if not files:
        print(f"(no logs for {args.name})")
        return
    latest = files[0]
    text = latest.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    tail_n = args.tail or 50
    for line in lines[-tail_n:]:
        print(line)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list")
    sub.add_parser("status")

    r = sub.add_parser("run")
    r.add_argument("name")
    r.add_argument("--dry-run", action="store_true")

    rd = sub.add_parser("run-due")
    rd.add_argument("--dry-run", action="store_true")

    e = sub.add_parser("enable"); e.add_argument("name")
    d = sub.add_parser("disable"); d.add_argument("name")

    c = sub.add_parser("create")
    c.add_argument("name")
    c.add_argument("--schedule", default="manual",
                   help="manual | daily:HH:MM | every:Nm | every:Nh | weekly:DOW:HH:MM")
    c.add_argument("--desc", default="TODO describe")

    s = sub.add_parser("show"); s.add_argument("name")

    lg = sub.add_parser("logs")
    lg.add_argument("name"); lg.add_argument("--tail", type=int, default=50)

    args = ap.parse_args()
    fn = {
        "list": cmd_list, "status": cmd_status,
        "run": cmd_run, "run-due": cmd_run_due,
        "enable": cmd_enable, "disable": cmd_disable,
        "create": cmd_create, "show": cmd_show, "logs": cmd_logs,
    }[args.cmd]
    return fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
