"""Retry wrapper with backoff + HEARTBEAT.md + Telegram alert on final failure.

Why: daily_run.bat steps run once. Network blip mid-run loses the whole step
until next day. After 2026-05-07 daily was killed by Ctrl+C at CVM step,
this wrapper guarantees:
  1. step is re-attempted up to N times (default 3) with backoff 1m/5m/15m
  2. on final failure: line appended to HEARTBEAT.md so next daily run can
     replay the missed step
  3. on final failure: best-effort Telegram alert (silent if not configured)

Usage from .bat:
    "%PY%" scripts\\_retry.py --tag CVM-PDF -- python monitors\\cvm_pdf_extractor.py --limit 20

Or via the .bat wrapper:
    call scripts\\_retry.bat CVM-PDF python monitors\\cvm_pdf_extractor.py --limit 20

Exit code: 0 if any attempt succeeded; non-zero from last attempt otherwise.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEARTBEAT_PATH = ROOT / "obsidian_vault" / "workspace" / "HEARTBEAT.md"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
RETRY_LOG = LOG_DIR / "retry_wrapper.log"

DEFAULT_BACKOFFS = [60, 300, 900]  # 1m, 5m, 15m


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _log(msg: str) -> None:
    line = f"{_now_iso()} {msg}\n"
    with RETRY_LOG.open("a", encoding="utf-8") as f:
        f.write(line)
    sys.stderr.write(line)


def _append_heartbeat(tag: str, cmd: list[str], attempts: int, last_exit: int) -> None:
    """Append a >>-prefixed checklist item to HEARTBEAT.md so the next
    heartbeat run replays the failed step."""
    HEARTBEAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not HEARTBEAT_PATH.exists():
        HEARTBEAT_PATH.write_text(
            "---\ntype: heartbeat\nupdated: " + _now_iso() + "\n---\n\n"
            "# HEARTBEAT — pending tasks\n\n"
            "Items prefixed with `>>` are executed by `agents._heartbeat` on\n"
            "the next run. Items without `>>` are notes for the founder.\n\n"
            "## Auto-injected (retry wrapper failures)\n\n",
            encoding="utf-8",
        )
    body = HEARTBEAT_PATH.read_text(encoding="utf-8")
    cmd_str = " ".join(_quote_if_needed(c) for c in cmd)
    new_line = f"- [ ] >> {cmd_str}  <!-- failed {tag}, exit={last_exit} after {attempts} attempts at {_now_iso()} -->"
    if new_line in body:
        return  # already queued
    if "## Auto-injected (retry wrapper failures)" in body:
        body = body.replace(
            "## Auto-injected (retry wrapper failures)\n\n",
            f"## Auto-injected (retry wrapper failures)\n\n{new_line}\n",
            1,
        )
    else:
        body = body.rstrip() + f"\n\n## Auto-injected (retry wrapper failures)\n\n{new_line}\n"
    HEARTBEAT_PATH.write_text(body, encoding="utf-8")


def _quote_if_needed(s: str) -> str:
    return f'"{s}"' if " " in s and not s.startswith('"') else s


def _push_telegram(tag: str, attempts: int, last_exit: int, cmd: list[str]) -> None:
    """Best-effort Telegram push. Silent failure if not configured."""
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            try:
                from dotenv import load_dotenv
                load_dotenv(ROOT / ".env")
                token = os.environ.get("TELEGRAM_BOT_TOKEN")
                chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            except ImportError:
                pass
        if not token or not chat_id:
            return
        import urllib.parse, urllib.request
        cmd_short = " ".join(cmd)[:120]
        text = (f"🚨 *{tag}* failed after {attempts} attempts (exit={last_exit}).\n"
                f"Cmd: `{cmd_short}`\nQueued in HEARTBEAT.md for replay.")
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data, method="POST",
        )
        urllib.request.urlopen(req, timeout=10).read()
    except Exception:
        pass  # never break the wrapper because of a notification glitch


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tag", required=True, help="Short label for logs/alerts")
    p.add_argument("--attempts", type=int, default=3)
    p.add_argument("--backoff", default="60,300,900",
                   help="Comma-separated seconds between attempts")
    p.add_argument("--timeout", type=int, default=1800,
                   help="Per-attempt timeout in seconds (default 30min)")
    p.add_argument("--no-heartbeat", action="store_true",
                   help="Skip HEARTBEAT.md append on final failure")
    p.add_argument("cmd", nargs=argparse.REMAINDER,
                   help="Command to run (after --)")
    args = p.parse_args()

    if not args.cmd:
        print("error: no command given", file=sys.stderr)
        return 2
    if args.cmd and args.cmd[0] == "--":
        args.cmd = args.cmd[1:]

    backoffs = [int(b.strip()) for b in args.backoff.split(",") if b.strip()]
    while len(backoffs) < args.attempts - 1:
        backoffs.append(backoffs[-1] if backoffs else 60)

    last_exit = 1
    for attempt in range(1, args.attempts + 1):
        _log(f"[{args.tag}] attempt {attempt}/{args.attempts}: {' '.join(args.cmd)}")
        try:
            r = subprocess.run(args.cmd, cwd=str(ROOT), timeout=args.timeout)
            last_exit = r.returncode
        except subprocess.TimeoutExpired:
            last_exit = 124
            _log(f"[{args.tag}] timeout after {args.timeout}s on attempt {attempt}")
        except Exception as e:
            last_exit = 125
            _log(f"[{args.tag}] launcher error attempt {attempt}: {type(e).__name__}: {e}")

        if last_exit == 0:
            _log(f"[{args.tag}] OK on attempt {attempt}")
            return 0

        if attempt < args.attempts:
            sleep_s = backoffs[attempt - 1] if attempt - 1 < len(backoffs) else 60
            _log(f"[{args.tag}] sleeping {sleep_s}s before retry")
            time.sleep(sleep_s)

    _log(f"[{args.tag}] FINAL FAIL after {args.attempts} attempts, exit={last_exit}")
    if not args.no_heartbeat:
        try:
            _append_heartbeat(args.tag, args.cmd, args.attempts, last_exit)
        except Exception as e:
            _log(f"[{args.tag}] heartbeat append error: {e}")
    _push_telegram(args.tag, args.attempts, last_exit, args.cmd)
    return last_exit


if __name__ == "__main__":
    sys.exit(main())
