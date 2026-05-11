"""Tier lockfile helper for Phase EE Tiered Scheduler.

Each cron tier (hourly / q4h / daily) acquires a named lockfile under
``data/locks/<tier>.lock`` before running. Locks contain the holder PID;
if the PID is dead (process crashed mid-run), the next acquire detects
the stale lock and takes over without manual intervention.

Designed for use from .bat files via subprocess invocation:

    python -m agents._lock acquire hourly --blocked-by daily
    if errorlevel 1, exit early (some tier is busy)
    ...do work...
    python -m agents._lock release hourly

The contextmanager ``tier_lock(...)`` is provided for in-process use.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCKS_DIR = ROOT / "data" / "locks"


class LockBusy(RuntimeError):
    """Raised when a lock cannot be acquired because another process holds it."""


def _ensure_locks_dir() -> None:
    LOCKS_DIR.mkdir(parents=True, exist_ok=True)


def _lock_path(tier: str) -> Path:
    return LOCKS_DIR / f"{tier}.lock"


def _pid_alive(pid: int) -> bool:
    """Return True if `pid` is currently running.

    Windows: OpenProcess + GetExitCodeProcess via ctypes (sub-ms, no
    subprocess). A handle returned by OpenProcess proves the OS still
    knows the PID; we then check if its exit code is STILL_ACTIVE (259)
    to distinguish "running" from "terminated, kernel object retained".

    POSIX: ``os.kill(pid, 0)`` raises ProcessLookupError if dead.
    """
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        kernel32 = ctypes.windll.kernel32
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        try:
            exit_code = wintypes.DWORD()
            ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
            if not ok:
                return False
            return exit_code.value == STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False
    except OSError:
        return False


def _read_lock(path: Path) -> tuple[int, float] | None:
    try:
        text = path.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError):
        return None
    parts = text.split("\n")
    try:
        pid = int(parts[0])
        ts = float(parts[1]) if len(parts) > 1 else 0.0
    except (ValueError, IndexError):
        return None
    return pid, ts


def _is_lock_alive(path: Path) -> bool:
    info = _read_lock(path)
    if info is None:
        return False
    pid, _ = info
    return _pid_alive(pid)


def acquire(tier: str, blocked_by: list[str] | None = None) -> bool:
    """Attempt to acquire the named tier lock.

    Returns True on success. Raises LockBusy if a blocking tier or the same
    tier already holds a live lock. Stale locks (dead PID) are taken over.
    """
    _ensure_locks_dir()
    blocked_by = blocked_by or []
    for higher in blocked_by:
        higher_lock = _lock_path(higher)
        if _is_lock_alive(higher_lock):
            info = _read_lock(higher_lock)
            raise LockBusy(f"tier '{tier}' blocked by '{higher}' (pid={info[0] if info else '?'})")
    own = _lock_path(tier)
    if _is_lock_alive(own):
        info = _read_lock(own)
        raise LockBusy(f"tier '{tier}' already held (pid={info[0] if info else '?'})")
    own.write_text(f"{os.getpid()}\n{time.time()}\n", encoding="utf-8")
    return True


def release(tier: str) -> bool:
    """Release the named tier lock. No-op if not held."""
    path = _lock_path(tier)
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return False


@contextmanager
def tier_lock(tier: str, blocked_by: list[str] | None = None):
    """In-process context manager — acquire on enter, release on exit."""
    acquire(tier, blocked_by=blocked_by)
    try:
        yield
    finally:
        release(tier)


def status() -> dict[str, dict]:
    """Snapshot of all known locks (for ops / diagnostics)."""
    _ensure_locks_dir()
    out: dict[str, dict] = {}
    for f in LOCKS_DIR.glob("*.lock"):
        info = _read_lock(f)
        if info is None:
            out[f.stem] = {"alive": False, "pid": None, "ts": None, "stale": True}
            continue
        pid, ts = info
        out[f.stem] = {
            "alive": _pid_alive(pid),
            "pid": pid,
            "ts": ts,
            "age_seconds": time.time() - ts if ts else None,
        }
    return out


def _cli() -> int:
    parser = argparse.ArgumentParser(prog="agents._lock", description="Tier lock helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_acq = sub.add_parser("acquire")
    p_acq.add_argument("tier")
    p_acq.add_argument("--blocked-by", nargs="*", default=[],
                       help="Higher-priority tiers that block this one")

    p_rel = sub.add_parser("release")
    p_rel.add_argument("tier")

    p_st = sub.add_parser("status")

    args = parser.parse_args()
    if args.cmd == "acquire":
        try:
            acquire(args.tier, blocked_by=args.blocked_by)
            print(f"acquired {args.tier} pid={os.getpid()}")
            return 0
        except LockBusy as e:
            print(f"BUSY: {e}", file=sys.stderr)
            return 1
    if args.cmd == "release":
        ok = release(args.tier)
        print(f"released {args.tier}" if ok else f"no lock to release: {args.tier}")
        return 0
    if args.cmd == "status":
        import json
        st = status()
        print(json.dumps(st, indent=2, default=str))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(_cli())
