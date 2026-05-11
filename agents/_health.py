"""Health checks for upstream services + circuit breaker.

Used by tier scheduler bats (Phase EE-AOW) to abort cleanly if infra is
down, instead of running through and producing 27 cascade failures.

Services probed:
- Ollama (localhost:11434/api/tags) — required for thesis, IC, etc.
- yfinance (query1.finance.yahoo.com) — primary BR + US fetcher
- Tavily quota (reads data/tavily_cache/_ratelimit.json) — autoresearch budget
- FMP (financialmodelingprep.com) — optional fallback US

Circuit breaker:
- 3 consecutive errors marks a service as TRIPPED for 24h
- TRIPPED means health-first checks short-circuit to "down" without re-probing
- State persisted in data/health/circuit.json
- Manual reset: `python -m agents._health reset <service>`

CLI:
    python -m agents._health check                  # all services, exit 0 if all green
    python -m agents._health check ollama tavily    # specific subset
    python -m agents._health status                 # human-readable JSON
    python -m agents._health record <service> ok    # mark a successful call (resets counter)
    python -m agents._health record <service> fail  # increments error counter
    python -m agents._health reset <service>        # clear circuit breaker for service
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parent.parent
HEALTH_DIR = ROOT / "data" / "health"
HEALTH_DIR.mkdir(parents=True, exist_ok=True)
CIRCUIT_FILE = HEALTH_DIR / "circuit.json"

OLLAMA_URL = "http://localhost:11434/api/tags"
YFINANCE_HEALTH_URL = "https://query1.finance.yahoo.com/v1/finance/search?q=AAPL"
FMP_HEALTH_URL = "https://financialmodelingprep.com/stable/profile?symbol=AAPL"
TAVILY_RATELIMIT_FILE = ROOT / "data" / "tavily_cache" / "_ratelimit.json"

# Probes added 2026-05-08: previously CVM SSL outage burned 80min/run because
# breaker had no probe → call kept retrying. Light-weight HEAD/GET on each.
CVM_HEALTH_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/"
SEC_HEALTH_URL = "https://www.sec.gov/files/company_tickers.json"
FRED_HEALTH_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF&cosd=2026-01-01"
BCB_HEALTH_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
SEC_USER_AGENT = "investment-intelligence apaidusis@gmail.com"

CIRCUIT_TRIP_THRESHOLD = 3
# 6h cooldown: long enough to avoid hammering a down server, short enough that
# transient outages (CVM/FRED SSL handshake glitches) auto-recover within a
# half-day. Was 24h — that left CVM tripped for full days after 2-3 minute outage.
CIRCUIT_COOLDOWN_HOURS = 6


@dataclass
class HealthResult:
    service: str
    ok: bool
    reason: str
    latency_ms: int | None = None
    extra: dict | None = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_circuit() -> dict:
    if not CIRCUIT_FILE.exists():
        return {}
    try:
        return json.loads(CIRCUIT_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_circuit(state: dict) -> None:
    CIRCUIT_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _is_tripped(service: str) -> tuple[bool, str | None]:
    full_state = _read_circuit()
    state = full_state.get(service, {})
    if not state.get("tripped"):
        return False, None
    tripped_at = state.get("tripped_at")
    if not tripped_at:
        return True, "tripped (no timestamp)"
    try:
        ts = datetime.fromisoformat(tripped_at)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) - ts > timedelta(hours=CIRCUIT_COOLDOWN_HOURS):
            # Cooldown expired — clear persisted state so the next failure
            # starts fresh (errors=0, not at threshold). Without this, the
            # first post-cooldown fail re-trips immediately because errors
            # counter was never decremented.
            state["tripped"] = False
            state["errors"] = 0
            state.pop("tripped_at", None)
            state["auto_reset_at"] = _now_iso()
            full_state[service] = state
            try:
                _write_circuit(full_state)
            except Exception:
                pass
            return False, "cooldown expired (auto-reset)"
        return True, f"tripped at {tripped_at}"
    except Exception:
        return True, "tripped (bad timestamp)"


def record(service: str, outcome: Literal["ok", "fail"], reason: str = "") -> None:
    """Increment error counter on fail; reset on ok. Trip circuit at threshold."""
    state = _read_circuit()
    s = state.get(service, {"errors": 0, "tripped": False})
    if outcome == "ok":
        s["errors"] = 0
        s["tripped"] = False
        s.pop("tripped_at", None)
        s["last_ok"] = _now_iso()
    else:
        s["errors"] = s.get("errors", 0) + 1
        s["last_fail"] = _now_iso()
        s["last_fail_reason"] = reason
        if s["errors"] >= CIRCUIT_TRIP_THRESHOLD and not s.get("tripped"):
            s["tripped"] = True
            s["tripped_at"] = _now_iso()
    state[service] = s
    _write_circuit(state)


def reset(service: str) -> None:
    """Manually clear circuit breaker for a service."""
    state = _read_circuit()
    if service in state:
        state[service] = {"errors": 0, "tripped": False, "manual_reset": _now_iso()}
        _write_circuit(state)


# ---- per-service probes ----

def check_ollama(timeout_s: float = 3.0) -> HealthResult:
    tripped, why = _is_tripped("ollama")
    if tripped:
        return HealthResult("ollama", False, f"circuit_breaker: {why}")
    import urllib.request
    import urllib.error
    t0 = time.time()
    try:
        with urllib.request.urlopen(OLLAMA_URL, timeout=timeout_s) as r:
            data = json.loads(r.read().decode("utf-8"))
        models = [m.get("name") for m in data.get("models", [])]
        latency = int((time.time() - t0) * 1000)
        record("ollama", "ok")
        return HealthResult("ollama", True, "ok", latency_ms=latency, extra={"models": len(models)})
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        record("ollama", "fail", str(e))
        return HealthResult("ollama", False, f"unreachable: {e}")


def check_yfinance(timeout_s: float = 5.0) -> HealthResult:
    tripped, why = _is_tripped("yfinance")
    if tripped:
        return HealthResult("yfinance", False, f"circuit_breaker: {why}")
    import urllib.request
    import urllib.error
    t0 = time.time()
    try:
        req = urllib.request.Request(YFINANCE_HEALTH_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            data = json.loads(r.read().decode("utf-8"))
        latency = int((time.time() - t0) * 1000)
        if data.get("quotes") or data.get("count", 0) > 0:
            record("yfinance", "ok")
            return HealthResult("yfinance", True, "ok", latency_ms=latency)
        record("yfinance", "fail", "empty response")
        return HealthResult("yfinance", False, "empty response")
    except (urllib.error.URLError, OSError, TimeoutError, ValueError) as e:
        record("yfinance", "fail", str(e))
        return HealthResult("yfinance", False, f"unreachable: {e}")


def check_tavily_quota() -> HealthResult:
    """Doesn't ping Tavily — just reads the local rate-limit ledger.

    Returns ok=False if daily/hourly quota exhausted (autoresearch would skip
    anyway, but signal lets tier bat decide whether to invoke autoresearch).
    """
    if not TAVILY_RATELIMIT_FILE.exists():
        return HealthResult("tavily", True, "no usage yet", extra={"day_count": 0, "remaining": 100})
    try:
        rl = json.loads(TAVILY_RATELIMIT_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        return HealthResult("tavily", False, f"unparseable ratelimit file: {e}")
    today = datetime.now(timezone.utc).date().isoformat()
    if rl.get("day") != today:
        # Counters from yesterday — fresh budget
        return HealthResult("tavily", True, "fresh day", extra={"day_count": 0, "remaining": 100})
    day_count = rl.get("day_count", 0)
    hour_count = rl.get("hour_count", 0)
    remaining = max(0, 100 - day_count)
    if remaining == 0:
        return HealthResult("tavily", False, "daily quota exhausted",
                            extra={"day_count": day_count, "remaining": 0})
    return HealthResult("tavily", True, "ok",
                        extra={"day_count": day_count, "hour_count": hour_count, "remaining": remaining})


def check_fmp(timeout_s: float = 5.0) -> HealthResult:
    """Optional: FMP fallback for US fundamentals. Skipped if no API key set."""
    import os
    if not os.getenv("FMP_API_KEY"):
        return HealthResult("fmp", True, "no API key — skipped", extra={"configured": False})
    tripped, why = _is_tripped("fmp")
    if tripped:
        return HealthResult("fmp", False, f"circuit_breaker: {why}")
    import urllib.request
    import urllib.error
    t0 = time.time()
    try:
        url = f"{FMP_HEALTH_URL}&apikey={os.getenv('FMP_API_KEY')}"
        with urllib.request.urlopen(url, timeout=timeout_s) as r:
            data = json.loads(r.read().decode("utf-8"))
        latency = int((time.time() - t0) * 1000)
        if isinstance(data, list) and data:
            record("fmp", "ok")
            return HealthResult("fmp", True, "ok", latency_ms=latency)
        record("fmp", "fail", "empty response")
        return HealthResult("fmp", False, "empty response")
    except (urllib.error.URLError, OSError, TimeoutError, ValueError) as e:
        record("fmp", "fail", str(e))
        return HealthResult("fmp", False, f"unreachable: {e}")


def check_cvm(timeout_s: float = 5.0) -> HealthResult:
    """Probe CVM dados.cvm.gov.br. Catches SSLError that crashed daily 2026-05-07."""
    tripped, why = _is_tripped("cvm")
    if tripped:
        return HealthResult("cvm", False, f"circuit_breaker: {why}")
    import urllib.request
    import urllib.error
    t0 = time.time()
    try:
        req = urllib.request.Request(CVM_HEALTH_URL, method="HEAD",
                                      headers={"User-Agent": "investment-intelligence/1.0"})
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            status = r.status
        latency = int((time.time() - t0) * 1000)
        if 200 <= status < 400:
            record("cvm", "ok")
            return HealthResult("cvm", True, "ok", latency_ms=latency)
        record("cvm", "fail", f"status={status}")
        return HealthResult("cvm", False, f"status={status}")
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        # SSLError, ConnectionError, EOFError all subclass OSError
        record("cvm", "fail", f"{type(e).__name__}: {e}")
        return HealthResult("cvm", False, f"{type(e).__name__}: {e}")


def check_sec(timeout_s: float = 5.0) -> HealthResult:
    """Probe SEC EDGAR. Requires UA per SEC policy."""
    tripped, why = _is_tripped("sec")
    if tripped:
        return HealthResult("sec", False, f"circuit_breaker: {why}")
    import urllib.request
    import urllib.error
    t0 = time.time()
    try:
        req = urllib.request.Request(SEC_HEALTH_URL, method="HEAD",
                                      headers={"User-Agent": SEC_USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            status = r.status
        latency = int((time.time() - t0) * 1000)
        if 200 <= status < 400:
            record("sec", "ok")
            return HealthResult("sec", True, "ok", latency_ms=latency)
        record("sec", "fail", f"status={status}")
        return HealthResult("sec", False, f"status={status}")
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        record("sec", "fail", f"{type(e).__name__}: {e}")
        return HealthResult("sec", False, f"{type(e).__name__}: {e}")


def check_fred(timeout_s: float = 5.0) -> HealthResult:
    """Probe FRED via small CSV pull."""
    tripped, why = _is_tripped("fred")
    if tripped:
        return HealthResult("fred", False, f"circuit_breaker: {why}")
    import urllib.request
    import urllib.error
    t0 = time.time()
    try:
        req = urllib.request.Request(FRED_HEALTH_URL,
                                      headers={"User-Agent": "investment-intelligence/1.0"})
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            data = r.read(512)  # short read suffices
        latency = int((time.time() - t0) * 1000)
        if data and b"DATE" in data:
            record("fred", "ok")
            return HealthResult("fred", True, "ok", latency_ms=latency)
        record("fred", "fail", "no DATE header in response")
        return HealthResult("fred", False, "malformed response")
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        record("fred", "fail", f"{type(e).__name__}: {e}")
        return HealthResult("fred", False, f"{type(e).__name__}: {e}")


def check_bcb(timeout_s: float = 5.0) -> HealthResult:
    """Probe BCB SGS API via last-value SELIC pull."""
    tripped, why = _is_tripped("bcb")
    if tripped:
        return HealthResult("bcb", False, f"circuit_breaker: {why}")
    import urllib.request
    import urllib.error
    t0 = time.time()
    try:
        req = urllib.request.Request(BCB_HEALTH_URL,
                                      headers={"User-Agent": "investment-intelligence/1.0"})
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            data = json.loads(r.read().decode("utf-8"))
        latency = int((time.time() - t0) * 1000)
        if isinstance(data, list) and data and "valor" in data[0]:
            record("bcb", "ok")
            return HealthResult("bcb", True, "ok", latency_ms=latency)
        record("bcb", "fail", "empty/malformed response")
        return HealthResult("bcb", False, "empty response")
    except (urllib.error.URLError, OSError, TimeoutError, ValueError) as e:
        record("bcb", "fail", f"{type(e).__name__}: {e}")
        return HealthResult("bcb", False, f"{type(e).__name__}: {e}")


PROBES = {
    "ollama": check_ollama,
    "yfinance": check_yfinance,
    "tavily": check_tavily_quota,
    "fmp": check_fmp,
    "cvm": check_cvm,
    "sec": check_sec,
    "fred": check_fred,
    "bcb": check_bcb,
}


# ---- Tavily bucket allocation (Phase HH-AOW) ----

TAVILY_BUCKETS_FILE = HEALTH_DIR / "tavily_buckets.json"
TAVILY_BUCKETS_CONFIG = ROOT / "config" / "tavily_buckets.yaml"


def _load_bucket_config() -> dict[str, int]:
    """Read daily caps per bucket from config/tavily_buckets.yaml. Falls back
    to a sensible default if the file is missing."""
    default = {"hourly_autoresearch": 30, "daily_wires": 30, "reactive": 25, "manual": 15}
    if not TAVILY_BUCKETS_CONFIG.exists():
        return default
    try:
        import yaml
        cfg = yaml.safe_load(TAVILY_BUCKETS_CONFIG.read_text(encoding="utf-8"))
        return {b: int(v.get("daily_cap", 0)) for b, v in cfg.get("buckets", {}).items()}
    except Exception:
        return default


def _read_bucket_state() -> dict:
    if not TAVILY_BUCKETS_FILE.exists():
        return {"day": datetime.now(timezone.utc).date().isoformat(), "buckets": {}}
    try:
        return json.loads(TAVILY_BUCKETS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"day": datetime.now(timezone.utc).date().isoformat(), "buckets": {}}


def _write_bucket_state(state: dict) -> None:
    TAVILY_BUCKETS_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def tavily_bucket_check(bucket: str) -> tuple[bool, int, int]:
    """Return (allowed, used_today, cap). Allowed=True if used < cap.

    Caller pattern:
        ok, used, cap = tavily_bucket_check("reactive")
        if not ok: skip; else: search_tavily(...) ; tavily_bucket_record("reactive")
    """
    caps = _load_bucket_config()
    cap = caps.get(bucket, 0)
    if cap == 0:
        return True, 0, 0  # bucket not configured => no enforcement
    state = _read_bucket_state()
    today = datetime.now(timezone.utc).date().isoformat()
    if state.get("day") != today:
        state = {"day": today, "buckets": {}}
        _write_bucket_state(state)
    used = state["buckets"].get(bucket, 0)
    return used < cap, used, cap


def tavily_bucket_record(bucket: str) -> None:
    """Increment per-bucket counter. Call AFTER a successful Tavily call."""
    caps = _load_bucket_config()
    if bucket not in caps:
        return
    state = _read_bucket_state()
    today = datetime.now(timezone.utc).date().isoformat()
    if state.get("day") != today:
        state = {"day": today, "buckets": {}}
    state["buckets"][bucket] = state["buckets"].get(bucket, 0) + 1
    _write_bucket_state(state)


def check_all(services: list[str] | None = None) -> dict[str, HealthResult]:
    services = services or list(PROBES.keys())
    return {name: PROBES[name]() for name in services if name in PROBES}


def all_green(results: dict[str, HealthResult], required: list[str] | None = None) -> bool:
    """Returns True if all REQUIRED services are ok. Optional services (fmp)
    can be down without blocking. Default required = [ollama, yfinance]."""
    required = required or ["ollama", "yfinance"]
    return all(results[name].ok for name in required if name in results)


def _cli() -> int:
    parser = argparse.ArgumentParser(prog="agents._health", description="Health probe + circuit breaker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="Probe all (or specified) services. Exit 0 if all required green.")
    p_check.add_argument("services", nargs="*", default=None)
    p_check.add_argument("--required", nargs="*", default=["ollama", "yfinance"],
                         help="Services that must be green to exit 0")

    p_st = sub.add_parser("status", help="Pretty JSON of last probe + circuit state")

    p_rec = sub.add_parser("record", help="Record outcome from external caller")
    p_rec.add_argument("service")
    p_rec.add_argument("outcome", choices=["ok", "fail"])
    p_rec.add_argument("--reason", default="")

    p_rst = sub.add_parser("reset", help="Manually clear circuit breaker")
    p_rst.add_argument("service")

    p_bk = sub.add_parser("bucket", help="Tavily bucket quota check / record")
    bsub = p_bk.add_subparsers(dest="bcmd", required=True)
    bsub.add_parser("status", help="Show all bucket usage")
    bk_check = bsub.add_parser("check")
    bk_check.add_argument("bucket")
    bk_record = bsub.add_parser("record")
    bk_record.add_argument("bucket")

    args = parser.parse_args()

    if args.cmd == "check":
        results = check_all(args.services)
        for name, r in results.items():
            mark = "OK" if r.ok else "FAIL"
            extra = f" {r.extra}" if r.extra else ""
            lat = f" ({r.latency_ms}ms)" if r.latency_ms is not None else ""
            print(f"[{mark}] {name}: {r.reason}{lat}{extra}")
        return 0 if all_green(results, args.required) else 1

    if args.cmd == "status":
        results = check_all()
        circuit = _read_circuit()
        out = {
            "checked_at": _now_iso(),
            "results": {k: asdict(v) for k, v in results.items()},
            "circuit": circuit,
        }
        print(json.dumps(out, indent=2, default=str))
        return 0

    if args.cmd == "record":
        record(args.service, args.outcome, args.reason)
        print(f"recorded {args.service} {args.outcome}")
        return 0

    if args.cmd == "reset":
        reset(args.service)
        print(f"reset {args.service}")
        return 0

    if args.cmd == "bucket":
        if args.bcmd == "status":
            caps = _load_bucket_config()
            state = _read_bucket_state()
            buckets = state.get("buckets", {})
            for name, cap in caps.items():
                used = buckets.get(name, 0)
                pct = int(used / cap * 100) if cap else 0
                print(f"  {name:25s} {used:3d}/{cap:3d} ({pct:3d}%)")
            return 0
        if args.bcmd == "check":
            ok, used, cap = tavily_bucket_check(args.bucket)
            print(f"{args.bucket}: {used}/{cap} - {'OK' if ok else 'EXHAUSTED'}")
            return 0 if ok else 1
        if args.bcmd == "record":
            tavily_bucket_record(args.bucket)
            ok, used, cap = tavily_bucket_check(args.bucket)
            print(f"recorded {args.bucket} -> {used}/{cap}")
            return 0
    return 2


if __name__ == "__main__":
    sys.exit(_cli())
