"""telegram_loop — Jarbas live.

Long-polling contínuo ao Telegram Bot API. Substitui o cron every:2m do
telegram_controller por um processo sempre-vivo que responde em < 3 seg.

Design:
- `getUpdates` com `timeout=25` → Telegram segura a conexão até chegar msg
  (idle = zero CPU, zero consumo). Quando chega, processa via
  `TelegramControllerAgent.execute_impl` e volta a polar.
- State (last_update_id) partilha com o agent tradicional — podes alternar
  sem perder updates.
- Graceful shutdown via Ctrl+C.

Uso:
    python scripts/telegram_loop.py                # foreground
    python scripts/telegram_loop.py --quiet        # menos logs

Para correr em background Windows, podes usar `pythonw.exe` ou criar
Scheduled Task com trigger "At startup".
"""
from __future__ import annotations

import argparse
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from agents._base import AgentContext
from agents.telegram_controller import TelegramControllerAgent


_stop = False


def _handle_sig(sig, frame):
    global _stop
    _stop = True
    print("\n[jarbas] shutdown requested…", flush=True)


def run(quiet: bool = False) -> int:
    signal.signal(signal.SIGINT, _handle_sig)
    try:
        signal.signal(signal.SIGTERM, _handle_sig)
    except AttributeError:
        pass  # Windows sem SIGTERM

    agent = TelegramControllerAgent()
    ctx = AgentContext(root=ROOT, config={"max_commands_per_run": 10}, dry_run=False)

    if not quiet:
        print(f"[jarbas] 🟢 online — {datetime.now().isoformat(timespec='seconds')}", flush=True)
        print(f"[jarbas] Ctrl+C para parar.", flush=True)

    consecutive_errors = 0

    while not _stop:
        try:
            result = agent.execute_impl(ctx)
            if result.status == "ok":
                if not quiet:
                    print(f"[jarbas] {datetime.now().strftime('%H:%M:%S')} · {result.summary}", flush=True)
                consecutive_errors = 0
            elif result.status == "no_action":
                pass  # idle, normal
            elif result.status == "failed":
                consecutive_errors += 1
                print(f"[jarbas] ⚠ failed: {result.summary}", flush=True)
                if consecutive_errors >= 5:
                    print("[jarbas] 5 erros consecutivos — backoff 60s", flush=True)
                    time.sleep(60)
                    consecutive_errors = 0
                else:
                    time.sleep(5)
                continue
            # Sem sleep entre polls — getUpdates já tem long-poll (timeout=10)
            # dentro do agent, que bloqueia até haver update ou timeout.
        except KeyboardInterrupt:
            break
        except Exception as e:
            consecutive_errors += 1
            print(f"[jarbas] ⚠ exceção: {type(e).__name__}: {e}", flush=True)
            if consecutive_errors >= 5:
                time.sleep(60)
                consecutive_errors = 0
            else:
                time.sleep(3)

    if not quiet:
        print(f"[jarbas] 🔴 offline — {datetime.now().isoformat(timespec='seconds')}", flush=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Jarbas live — Telegram controller em loop contínuo")
    ap.add_argument("--quiet", action="store_true", help="sem logs rotineiros")
    args = ap.parse_args()
    return run(quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
