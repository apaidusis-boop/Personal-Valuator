"""LocalClaw system check + setup helper (Phase EE.4).

Verifica o ambiente para acesso remoto e modelos de elite:

  1. Ollama: lista modelos instalados, sugere upgrade Qwen 32B → Llama 3.3 70B
  2. Tailscale: detecta se está instalado/ligado, sugere setup
  3. Mission Control Next.js: confirma scaffold em mission-control/
  4. Telegram: confirma .env e sugere restart Jarbas se Antonio Carlos é novo

Uso:
    python scripts/localclaw_setup.py             # check tudo
    python scripts/localclaw_setup.py --upgrade   # imprime comandos exactos para upgrade
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_ollama() -> dict:
    """Inspect Ollama models. Returns dict with installed list + recommendations."""
    out: dict = {"available": False, "models": [], "recommendations": []}
    try:
        r = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10
        )
        if r.returncode != 0:
            out["error"] = "ollama list failed"
            return out
    except FileNotFoundError:
        out["error"] = "ollama CLI não encontrado"
        return out
    except Exception as e:
        out["error"] = str(e)
        return out

    out["available"] = True
    lines = (r.stdout or "").strip().split("\n")[1:]  # skip header
    out["models"] = [line.split()[0] for line in lines if line.strip()]

    # Recommendations
    has_chief = any("qwen2.5:32b" in m for m in out["models"])
    has_elite = any(("llama3.3:70b" in m) or ("qwen2.5:72b" in m) for m in out["models"])

    if not has_chief:
        out["recommendations"].append({
            "kind": "missing-chief-model",
            "msg": "Antonio Carlos precisa de Qwen 2.5 32B para tool-calling.",
            "command": "ollama pull qwen2.5:32b-instruct-q4_K_M",
            "size": "~19 GB",
        })
    if not has_elite:
        out["recommendations"].append({
            "kind": "elite-model-upgrade",
            "msg": "Para dossier 5k palavras (ii deepdive --model), pulla Llama 3.3 70B.",
            "command": "ollama pull llama3.3:70b",
            "size": "~40 GB · 32GB VRAM + 8-15 GB RAM offload no 5090",
        })
    return out


def check_tailscale() -> dict:
    """Detect Tailscale install + connection status."""
    out: dict = {"installed": False, "connected": False}
    # Try Windows path + PATH
    candidates = [
        "tailscale",
        r"C:\Program Files\Tailscale\tailscale.exe",
        r"C:\Program Files (x86)\Tailscale\tailscale.exe",
    ]
    cli = None
    for c in candidates:
        try:
            r = subprocess.run([c, "version"], capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                cli = c
                out["installed"] = True
                out["version"] = (r.stdout or "").strip().split("\n")[0]
                break
        except FileNotFoundError:
            continue
        except Exception:
            continue
    if not out["installed"]:
        out["recommendations"] = [{
            "kind": "install-tailscale",
            "msg": "Instala Tailscale para acesso remoto (Mission Control + Antonio Carlos longe de casa).",
            "command": "winget install --id Tailscale.Tailscale -e",
            "after": "Depois corre 'tailscale up' e faz login no browser.",
        }]
        return out

    try:
        r = subprocess.run([cli, "status", "--json"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            try:
                data = json.loads(r.stdout or "{}")
                out["connected"] = bool(data.get("Self", {}).get("Online"))
                out["self_ip"] = data.get("Self", {}).get("TailscaleIPs", [None])[0]
                out["hostname"] = data.get("Self", {}).get("HostName")
            except Exception:
                pass
    except Exception:
        pass
    return out


def check_mission_control() -> dict:
    mc = ROOT / "mission-control"
    out: dict = {
        "scaffold_present": mc.exists(),
        "node_modules": (mc / "node_modules").exists(),
        "package_json": (mc / "package.json").exists(),
    }
    if out["scaffold_present"] and out["package_json"]:
        try:
            pkg = json.loads((mc / "package.json").read_text(encoding="utf-8"))
            out["scripts"] = list(pkg.get("scripts", {}).keys())
        except Exception:
            pass
    return out


def check_telegram() -> dict:
    env = ROOT / ".env"
    out: dict = {"env_present": env.exists(), "antonio_wired": False}
    if env.exists():
        text = env.read_text(encoding="utf-8")
        out["telegram_token_set"] = "TELEGRAM_BOT_TOKEN=" in text and not "TELEGRAM_BOT_TOKEN=\n" in text
        out["telegram_chat_set"] = "TELEGRAM_CHAT_ID=" in text
    # Check telegram_controller wired to Antonio Carlos
    tc = ROOT / "agents" / "telegram_controller.py"
    if tc.exists():
        out["antonio_wired"] = "chief_of_staff" in tc.read_text(encoding="utf-8")
    out["recommendations"] = []
    if out["antonio_wired"]:
        out["recommendations"].append({
            "kind": "restart-jarbas",
            "msg": "telegram_controller foi alterado para usar Antonio Carlos. "
                   "Restarta o long-poll para a alteração entrar em produção.",
            "command": "python scripts/telegram_loop.py",
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="LocalClaw setup check (Phase EE.4)")
    ap.add_argument("--upgrade", action="store_true",
                    help="print exact commands for missing pieces")
    args = ap.parse_args()

    sep = "═" * 60
    print(f"\n{sep}\n  LocalClaw — system check\n{sep}\n")

    sections = [
        ("OLLAMA",         check_ollama()),
        ("TAILSCALE",      check_tailscale()),
        ("MISSION CONTROL", check_mission_control()),
        ("TELEGRAM",       check_telegram()),
    ]

    all_recs: list = []
    for label, data in sections:
        print(f"\n[{label}]")
        for k, v in data.items():
            if k == "recommendations":
                if isinstance(v, list):
                    all_recs.extend([(label, r) for r in v])
                continue
            if isinstance(v, list):
                v_str = ", ".join(str(x) for x in v[:6]) + (f" +{len(v)-6}" if len(v) > 6 else "")
            else:
                v_str = str(v)
            print(f"  {k:24} {v_str}")

    if all_recs:
        print(f"\n{sep}\n  RECOMENDAÇÕES ({len(all_recs)})\n{sep}")
        for label, r in all_recs:
            print(f"\n  [{label}] {r.get('msg','?')}")
            if r.get("command"):
                print(f"    $ {r['command']}")
            if r.get("size"):
                print(f"    ({r['size']})")
            if r.get("after"):
                print(f"    Após: {r['after']}")
    else:
        print(f"\n{sep}\n  ✓ Tudo a postos. LocalClaw operacional.\n{sep}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
