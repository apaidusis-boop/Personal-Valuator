"""Helena desktop backend — FastAPI sidecar.

Exposes the existing Python intelligence (SQLite, scoring, agents) as a local
HTTP API for the Tauri/Next.js frontend to consume.

Surface principle (per `feedback_terminal_obsidian` memory):
    Terminal = sala do chefe (existing CLI untouched).
    Obsidian/desktop app = Escritório (this is part of it).

Run dev:
    cd desktop/backend
    uvicorn main:app --reload --port 8765

Run prod (bundled by PyInstaller, spawned by Tauri sidecar):
    helena-backend.exe   # listens on 127.0.0.1:8765
"""
from __future__ import annotations

import sys
from pathlib import Path

# Resolve repo root so we can import `analytics`, `scoring`, `agents`, etc.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from desktop.backend.routers import positions, ticker, agents as agents_router  # noqa: E402
from desktop.backend.routers import actions, signals  # noqa: E402

app = FastAPI(
    title="Helena Backend",
    version="0.1.0",
    description="Local-only sidecar exposing investment-intelligence as REST.",
)

# Tauri webview origin is `tauri://localhost` on prod.
# Dev: Vite serves on either 127.0.0.1:1420 or localhost:1420 — accept both.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^(http://(localhost|127\.0\.0\.1):1420|tauri://localhost)$",
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(positions.router, prefix="/api", tags=["positions"])
app.include_router(ticker.router, prefix="/api", tags=["ticker"])
app.include_router(agents_router.router, prefix="/api", tags=["agents"])
app.include_router(actions.router, prefix="/api", tags=["actions"])
app.include_router(signals.router, prefix="/api", tags=["signals"])


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "helena-backend", "version": app.version}


@app.get("/api/meta")
def meta() -> dict:
    """Bootstrap info for the frontend — fx, last update, count of holdings."""
    import sqlite3
    db_br = ROOT / "data" / "br_investments.db"
    db_us = ROOT / "data" / "us_investments.db"
    fx = 5.0
    holdings = 0
    last_price = None
    try:
        with sqlite3.connect(db_br) as c:
            r = c.execute(
                "SELECT value FROM series WHERE series_id='USDBRL_PTAX' "
                "ORDER BY date DESC LIMIT 1"
            ).fetchone()
            if r:
                fx = float(r[0])
        for db in (db_br, db_us):
            with sqlite3.connect(db) as c:
                n = c.execute(
                    "SELECT COUNT(*) FROM portfolio_positions WHERE active=1"
                ).fetchone()[0]
                holdings += n
                lp = c.execute(
                    "SELECT MAX(date) FROM prices"
                ).fetchone()[0]
                if lp and (last_price is None or lp > last_price):
                    last_price = lp
    except Exception:
        pass
    return {
        "fx_usdbrl": fx,
        "holdings_active": holdings,
        "last_price_date": last_price,
    }
