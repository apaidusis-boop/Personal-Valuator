"""dashboard_app — webapp Streamlit local para visualização interactiva.

Corre com: `streamlit run scripts/dashboard_app.py` → http://localhost:8501

Abas:
  1. 💼 Portfolio — MV consolidado, evolução, holdings table, alocação pie
  2. 🔍 Ticker Deep Dive — select ticker → verdict + charts + peers + insights
  3. 📺 YouTube — digest por canal + ticker
  4. 🎯 Triggers & Signals — fired triggers + watch list
  5. 📊 Screener — filtros live sobre universe

Zero tokens Claude. Dados vêm do SQLite + analytics/fx + scoring.
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


st.set_page_config(
    page_title="Investment Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

from scripts._theme import inject_css, brand_sidebar, section_caption, COLORS  # noqa: E402

inject_css()


@st.cache_data(ttl=60)
def load_holdings() -> pd.DataFrame:
    rows = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            df = pd.read_sql_query("""
                SELECT p.ticker, p.quantity, p.entry_price, p.entry_date, p.notes,
                       c.name, c.sector, c.currency,
                       (SELECT close FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS price,
                       (SELECT date  FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS price_date,
                       (SELECT score FROM scores WHERE ticker=p.ticker ORDER BY run_date DESC LIMIT 1) AS screen_score,
                       (SELECT passes_screen FROM scores WHERE ticker=p.ticker ORDER BY run_date DESC LIMIT 1) AS screen_pass
                FROM portfolio_positions p LEFT JOIN companies c ON c.ticker=p.ticker
                WHERE p.active=1
            """, c)
            df["market"] = market
            rows.append(df)
    out = pd.concat(rows, ignore_index=True)
    out["market_value_native"] = out["price"].fillna(0) * out["quantity"].fillna(0)
    out["cost_native"] = out["entry_price"].fillna(0) * out["quantity"].fillna(0)
    out["pnl_pct"] = ((out["price"] / out["entry_price"]) - 1) * 100
    out["pnl_abs_native"] = out["market_value_native"] - out["cost_native"]
    return out


@st.cache_data(ttl=300)
def load_fx() -> float:
    with sqlite3.connect(DB_BR) as c:
        r = c.execute(
            "SELECT value FROM series WHERE series_id='USDBRL_PTAX' ORDER BY date DESC LIMIT 1"
        ).fetchone()
    return float(r[0]) if r else 5.0


@st.cache_data(ttl=60)
def load_snapshots(days: int = 180) -> pd.DataFrame:
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    rows = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            try:
                df = pd.read_sql_query(
                    "SELECT date, ticker, mv_brl, mv_native FROM portfolio_snapshots WHERE date >= ?",
                    c, params=[cutoff],
                )
                df["market"] = market
                rows.append(df)
            except Exception:
                pass
    if not rows:
        return pd.DataFrame(columns=["date", "ticker", "mv_brl", "market"])
    return pd.concat(rows, ignore_index=True)


@st.cache_data(ttl=60)
def load_prices(ticker: str, market: str, days: int = 365) -> pd.DataFrame:
    db = DB_BR if market == "br" else DB_US
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    with sqlite3.connect(db) as c:
        return pd.read_sql_query(
            "SELECT date, close FROM prices WHERE ticker=? AND date>=? ORDER BY date",
            c, params=[ticker, cutoff],
        )


@st.cache_data(ttl=60)
def load_ticker_insights(ticker: str, days: int = 180) -> pd.DataFrame:
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    rows = []
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                df = pd.read_sql_query("""
                    SELECT v.published_at, v.channel, i.kind, i.claim, i.confidence
                    FROM video_insights i LEFT JOIN videos v ON i.video_id=v.video_id
                    WHERE i.ticker=? AND (v.published_at >= ? OR i.created_at >= ?)
                    ORDER BY v.published_at DESC
                """, c, params=[ticker, cutoff, cutoff])
                rows.append(df)
            except Exception:
                pass
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


@st.cache_data(ttl=60)
def load_ticker_fundamentals(ticker: str, market: str) -> pd.DataFrame:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        return pd.read_sql_query(
            """SELECT period_end, pe, pb, dy, roe, eps, bvps, dividend_streak_years
               FROM fundamentals WHERE ticker=? ORDER BY period_end""",
            c, params=[ticker],
        )


def load_verdict(ticker: str) -> dict | None:
    try:
        from scripts.verdict import compute_verdict
        v = compute_verdict(ticker)
        from dataclasses import asdict
        return asdict(v)
    except Exception as e:
        return {"error": str(e)}


# ============================= SIDEBAR =====================================

with st.sidebar:
    brand_sidebar()
    page = st.radio(
        "nav",
        ["Portfolio", "Ticker Deep Dive", "Actions Queue", "Ask Library",
         "Perpetuum Health", "Paper Signals", "RI Timeline",
         "YouTube Digest", "Triggers", "Screener"],
        label_visibility="collapsed",
    )
    _border = COLORS["border"]
    _muted = COLORS["muted"]
    _text = COLORS["text"]
    st.markdown(
        f"<div style='height:1px;background:{_border};margin:18px 0;'></div>",
        unsafe_allow_html=True,
    )
    fx_rate = load_fx()
    st.markdown(
        f"""<div style='font-size:0.75rem;color:{_muted};line-height:1.6;'>
        <div>USDBRL <span style='color:{_text};font-family:ui-monospace,monospace;'>{fx_rate:.4f}</span></div>
        <div>{date.today().isoformat()}</div>
        </div>""",
        unsafe_allow_html=True,
    )


# ============================= PAGE 1: Portfolio ===========================

if page == "Portfolio":
    st.title("Portfolio")
    section_caption("BR + US, agregado em BRL")
    df = load_holdings()
    df["mv_brl"] = df.apply(
        lambda r: r["market_value_native"] * (fx_rate if r["market"] == "us" else 1.0),
        axis=1,
    )
    df["weight"] = df["mv_brl"] / df["mv_brl"].sum() * 100

    total_brl = df["mv_brl"].sum()
    br_mv = df.loc[df["market"] == "br", "mv_brl"].sum()
    us_mv = df.loc[df["market"] == "us", "mv_brl"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total BRL", f"R$ {total_brl:,.0f}")
    col2.metric("Total USD", f"$ {total_brl / fx_rate:,.0f}")
    col3.metric("🇧🇷 BR", f"R$ {br_mv:,.0f}", f"{br_mv/total_brl*100:.1f}%")
    col4.metric("🇺🇸 US", f"R$ {us_mv:,.0f}", f"{us_mv/total_brl*100:.1f}%")

    st.divider()

    # Evolution chart
    snaps = load_snapshots(180)
    if not snaps.empty:
        daily = snaps.groupby(["date", "market"])["mv_brl"].sum().reset_index()
        fig = px.line(daily, x="date", y="mv_brl", color="market",
                      title="Evolução MV (BRL) — últimos 180d",
                      labels={"mv_brl": "MV (BRL)", "date": "Data"})
        # Total line
        total = snaps.groupby("date")["mv_brl"].sum().reset_index()
        fig.add_trace(go.Scatter(x=total["date"], y=total["mv_brl"],
                                 mode="lines", name="Total",
                                 line={"color": "black", "width": 2}))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem snapshots ainda. Corre: `python scripts/snapshot_portfolio.py --backfill 90`")

    # Allocation pies
    col1, col2 = st.columns(2)
    with col1:
        sec_agg = df.groupby("sector")["mv_brl"].sum().reset_index().sort_values("mv_brl", ascending=False)
        fig_sec = px.pie(sec_agg, values="mv_brl", names="sector", title="Alocação por Sector")
        st.plotly_chart(fig_sec, use_container_width=True)
    with col2:
        fig_mkt = px.pie(df.groupby("market")["mv_brl"].sum().reset_index(),
                         values="mv_brl", names="market", title="Alocação BR vs US")
        st.plotly_chart(fig_mkt, use_container_width=True)

    st.divider()
    st.subheader("Holdings")
    display = df[["ticker", "market", "sector", "quantity", "entry_price", "price",
                  "mv_brl", "weight", "pnl_pct", "screen_score", "screen_pass"]].copy()
    display.columns = ["Ticker", "Mkt", "Sector", "Qty", "Entry", "Now", "MV (BRL)", "Weight %", "P&L %", "Screen", "Pass"]
    display = display.sort_values("MV (BRL)", ascending=False)
    st.dataframe(
        display.style.format({
            "Qty": "{:g}", "Entry": "{:,.2f}", "Now": "{:,.2f}",
            "MV (BRL)": "R$ {:,.0f}", "Weight %": "{:.1f}%", "P&L %": "{:+.2f}%",
            "Screen": "{:.2f}",
        }).background_gradient(subset=["P&L %"], cmap="RdYlGn", vmin=-50, vmax=100),
        use_container_width=True,
        height=min(600, 40 * len(df) + 50),
    )


# ============================= PAGE 2: Ticker Deep Dive ====================

elif page == "Ticker Deep Dive":
    st.title("Ticker deep dive")
    section_caption("Verdict, fundamentals, charts e insights por ticker")
    df = load_holdings()
    all_tickers = sorted(set(df["ticker"].tolist()) |
                         set(t for mk, db in (("br", DB_BR), ("us", DB_US))
                             for (t,) in sqlite3.connect(db).execute("SELECT ticker FROM companies")))
    ticker = st.selectbox("Ticker", all_tickers, index=all_tickers.index("ACN") if "ACN" in all_tickers else 0)

    from scripts.refresh_ticker import _market_of
    market = _market_of(ticker)

    # Verdict
    st.subheader("Verdict")
    with st.spinner("Computing verdict..."):
        v = load_verdict(ticker)
    if v and not v.get("error"):
        color = {"BUY": "🟢", "ADD": "🟢", "WATCH": "🟡",
                 "HOLD": "🟠", "SELL": "🔴", "AVOID": "⛔", "SKIP": "⚪"}.get(v["action"], "•")
        st.markdown(f"### {color} {v['action']}  —  Score **{v['total_score']:.1f}/10**  (conf {v['confidence_pct']}%)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Quality", f"{v['quality_score']:.1f}/10")
        c2.metric("Valuation", f"{v['valuation_score']:.1f}/10")
        c3.metric("Momentum", f"{v['momentum_score']:.1f}/10")
        c4.metric("Narrativa", f"{v['narrative_score']:.1f}/10")
        with st.expander("Razões"):
            for r in v["reasons"]:
                st.write(f"- {r}")
    else:
        st.warning(v.get("error") if v else "verdict indisponível")

    st.divider()

    # Price chart
    px_df = load_prices(ticker, market, 365)
    if not px_df.empty:
        fig = px.line(px_df, x="date", y="close", title=f"{ticker} — 1y close")
        st.plotly_chart(fig, use_container_width=True)

    # Fundamentals trend
    fund = load_ticker_fundamentals(ticker, market)
    if not fund.empty and len(fund) >= 2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("P/E + P/B")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fund["period_end"], y=fund["pe"], name="P/E"))
            fig.add_trace(go.Scatter(x=fund["period_end"], y=fund["pb"], name="P/B"))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("ROE & DY")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fund["period_end"], y=fund["roe"] * 100, name="ROE %"))
            fig.add_trace(go.Scatter(x=fund["period_end"], y=fund["dy"] * 100, name="DY %"))
            st.plotly_chart(fig, use_container_width=True)

    # YouTube insights
    yt = load_ticker_insights(ticker, 180)
    if not yt.empty:
        st.subheader(f"YouTube insights · 180d · {len(yt)} found")
        st.dataframe(yt, use_container_width=True, height=300)


# ============================= PAGE 3: Actions Queue =======================

elif page == "Actions Queue":
    import json as _json
    import subprocess as _subprocess

    st.title("Actions queue")
    section_caption("Decisões pendentes — approve, ignore, anote")

    @st.cache_data(ttl=15)
    def load_open_actions() -> pd.DataFrame:
        rows = []
        for mkt, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                df = pd.read_sql_query(
                    """SELECT id, ticker, kind, action_hint, opened_at, notes, trigger_snapshot_json
                       FROM watchlist_actions WHERE status='open' ORDER BY opened_at DESC""",
                    c,
                )
                df["market"] = mkt
                rows.append(df)
        out = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
        if out.empty:
            return out
        out["ref"] = out["market"] + "/" + out["id"].astype(str)
        out["is_perpetuum"] = out["kind"].str.startswith("perpetuum:")
        return out

    actions = load_open_actions()

    if actions.empty:
        st.success("✨ Sem actions pendentes. Tudo limpo.")
        st.stop()

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total open", len(actions))
    c2.metric("BR", int((actions["market"] == "br").sum()))
    c3.metric("US", int((actions["market"] == "us").sum()))
    c4.metric("Perpetuum", int(actions["is_perpetuum"].sum()))

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        mkt_f = st.multiselect("Market", ["br", "us"], default=["br", "us"], key="aq_mkt")
    with fc2:
        kinds = sorted(actions["kind"].unique())
        kind_f = st.multiselect("Kind", kinds, default=kinds, key="aq_kind")
    with fc3:
        ticker_f = st.text_input("Ticker filter", "", key="aq_ticker").strip().upper()

    filt = actions[actions["market"].isin(mkt_f) & actions["kind"].isin(kind_f)]
    if ticker_f:
        filt = filt[filt["ticker"].str.contains(ticker_f, na=False)]

    st.divider()
    st.caption(f"Mostrando {len(filt)} de {len(actions)} actions")

    # Per-row UI
    for _, row in filt.iterrows():
        ref = row["ref"]
        snap = {}
        if row["trigger_snapshot_json"]:
            try:
                snap = _json.loads(row["trigger_snapshot_json"])
            except Exception:
                snap = {}

        # Color by kind
        if row["is_perpetuum"]:
            badge = "🔧"
        elif "altman" in row["kind"] or "piotroski" in row["kind"]:
            badge = "⚠️"
        elif "dy" in row["kind"].lower() or "ADD" in (row["action_hint"] or ""):
            badge = "🟢"
        else:
            badge = "•"

        with st.container(border=True):
            head_c1, head_c2, head_c3 = st.columns([3, 2, 2])
            with head_c1:
                st.markdown(f"### {badge} `{ref}` — **{row['ticker']}**")
                st.caption(f"`{row['kind']}` · opened {row['opened_at']}")
            with head_c2:
                st.markdown(f"**Hint**: {row['action_hint'] or '—'}")
            with head_c3:
                if row["notes"]:
                    st.caption(f"📝 {row['notes'][:150]}")

            with st.expander("🔍 Snapshot details"):
                if snap:
                    st.json(snap)
                else:
                    st.caption("Sem snapshot disponível.")

            btn_c1, btn_c2, btn_c3, btn_c4 = st.columns([1, 1, 2, 2])
            confirm_key = f"confirm_{ref}"

            with btn_c1:
                if st.button("✅ Approve", key=f"app_{ref}", use_container_width=True):
                    st.session_state[confirm_key] = "approve"

            with btn_c2:
                if st.button("❌ Ignore", key=f"ign_{ref}", use_container_width=True):
                    st.session_state[confirm_key] = "ignore"

            with btn_c3:
                note_text = st.text_input(
                    "Note (optional)", key=f"note_{ref}", label_visibility="collapsed",
                    placeholder="Optional note…",
                )

            with btn_c4:
                if st.button("📝 Add note", key=f"addn_{ref}", use_container_width=True, disabled=not note_text):
                    proc = _subprocess.run(
                        ["python", "scripts/action_cli.py", "note", ref, "--note", note_text],
                        cwd=str(ROOT), capture_output=True, text=True,
                        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
                    )
                    if proc.returncode == 0:
                        st.success(f"Note added to {ref}")
                        load_open_actions.clear()
                        st.rerun()
                    else:
                        st.error(f"Failed: {proc.stderr[-300:]}")

            # Confirm modal pattern
            if st.session_state.get(confirm_key):
                action = st.session_state[confirm_key]
                with st.warning(f"Confirma **{action}** action `{ref}` ({row['ticker']})?"):
                    cf1, cf2 = st.columns(2)
                    with cf1:
                        if st.button(f"Sim, {action}", key=f"yes_{ref}", type="primary", use_container_width=True):
                            cmd = None
                            label = ""
                            if action == "approve":
                                if row["is_perpetuum"]:
                                    cmd = ["python", "scripts/perpetuum_action_run.py", str(row["id"]),
                                           "--market", row["market"]]
                                    label = "perpetuum run"
                                else:
                                    cmd = ["python", "scripts/action_cli.py", "resolve", ref]
                                    if note_text:
                                        cmd += ["--note", note_text]
                                    label = "resolve"
                            else:  # ignore
                                cmd = ["python", "scripts/action_cli.py", "ignore", ref]
                                if note_text:
                                    cmd += ["--note", note_text]
                                label = "ignore"

                            with st.spinner(f"Running {label}…"):
                                proc = _subprocess.run(
                                    cmd, cwd=str(ROOT), capture_output=True, text=True,
                                    env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
                                    timeout=300,
                                )
                            if proc.returncode == 0:
                                st.success(f"✅ {ref} {action}d")
                                if proc.stdout:
                                    with st.expander("output"):
                                        st.code(proc.stdout[-2000:])
                            else:
                                st.error(f"Exit {proc.returncode}: {(proc.stderr or proc.stdout)[-500:]}")

                            del st.session_state[confirm_key]
                            load_open_actions.clear()
                            st.rerun()
                    with cf2:
                        if st.button("Cancelar", key=f"no_{ref}", use_container_width=True):
                            del st.session_state[confirm_key]
                            st.rerun()


# ============================= PAGE 4: Ask Library =========================

elif page == "Ask Library":
    import os as _os
    import subprocess as _subprocess

    st.title("Ask library")
    section_caption("RAG local · Damodaran + Dalio · Qwen 14B")

    # Persistent history
    if "ask_history" not in st.session_state:
        st.session_state["ask_history"] = []

    with st.form("ask_form", clear_on_submit=False):
        q = st.text_area(
            "Pergunta (PT/EN)",
            placeholder="Ex: Quais critérios Damodaran para narrative-driven valuation?",
            height=80,
        )
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            k = st.number_input("Chunks (k)", min_value=2, max_value=15, value=6, step=1)
        with c2:
            mode = st.selectbox("Modo", ["ask (RAG + Qwen synth)", "query (só busca)"])
        submitted = st.form_submit_button("🔍 Ask", type="primary", use_container_width=True)

    if submitted and q.strip():
        cmd_mode = "ask" if mode.startswith("ask") else "query"
        cmd = ["python", "-m", "library.rag", cmd_mode, q.strip(), "--k", str(int(k))]
        env = {"PYTHONIOENCODING": "utf-8", **_os.environ}
        with st.spinner(f"Running {cmd_mode}… (Qwen 14B local pode levar 30-60s)"):
            try:
                proc = _subprocess.run(
                    cmd, cwd=str(ROOT), capture_output=True, text=True,
                    env=env, timeout=300,
                )
            except _subprocess.TimeoutExpired:
                st.error("Timeout (>5min). Tenta pergunta mais específica.")
                proc = None

        if proc is not None:
            entry = {
                "q": q.strip(),
                "mode": cmd_mode,
                "k": int(k),
                "ts": date.today().isoformat(),
                "ok": proc.returncode == 0,
                "stdout": proc.stdout or "",
                "stderr": proc.stderr or "",
            }
            st.session_state["ask_history"].insert(0, entry)
            st.session_state["ask_history"] = st.session_state["ask_history"][:10]

            if proc.returncode == 0:
                st.success("✅ Resposta")
                st.markdown(proc.stdout)
            else:
                st.error(f"Exit {proc.returncode}")
                st.code(proc.stderr[-1000:] or proc.stdout[-1000:])

    if st.session_state["ask_history"]:
        st.divider()
        st.subheader("Histórico recente")
        for i, h in enumerate(st.session_state["ask_history"]):
            icon = "✅" if h["ok"] else "❌"
            with st.expander(f"{icon} [{h['ts']}] {h['q'][:80]} ({h['mode']}, k={h['k']})"):
                if h["ok"]:
                    st.markdown(h["stdout"])
                else:
                    st.code(h["stderr"][-1000:] or h["stdout"][-1000:])


# ============================= PAGE 5: Perpetuum Health ====================

elif page == "Perpetuum Health":
    st.title("Perpetuum health")
    section_caption("9 perpetuums · status, flagged subjects, trends")

    @st.cache_data(ttl=30)
    def load_perpetuum_health() -> pd.DataFrame:
        rows = []
        for mkt, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                try:
                    df = pd.read_sql_query(
                        """SELECT perpetuum_name, subject_id, run_date, score, flag_count,
                                  tier, details_json, action_hint
                           FROM perpetuum_health""",
                        c,
                    )
                    df["market"] = mkt
                    rows.append(df)
                except Exception:
                    pass
        if not rows:
            return pd.DataFrame()
        return pd.concat(rows, ignore_index=True)

    h = load_perpetuum_health()
    if h.empty:
        st.warning("Sem dados em perpetuum_health. Corre `python agents/perpetuum_master.py`.")
        st.stop()

    # Summary by perpetuum
    summary = h.groupby("perpetuum_name").agg(
        subjects=("subject_id", "count"),
        flagged=("flag_count", lambda x: int((x > 0).sum())),
        avg_score=("score", "mean"),
        last_run=("run_date", "max"),
    ).reset_index().sort_values("subjects", ascending=False)

    today_str = date.today().isoformat()
    summary["stale_days"] = summary["last_run"].apply(
        lambda d: (date.today() - date.fromisoformat(d)).days if d else 999
    )
    summary["status"] = summary["stale_days"].apply(
        lambda d: "🟢 fresh" if d <= 1 else "🟡 1-3d" if d <= 3 else "🔴 stale"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Perpetuums", len(summary))
    c2.metric("Total subjects", int(summary["subjects"].sum()))
    c3.metric("Flagged", int(summary["flagged"].sum()))
    fresh_count = int((summary["stale_days"] <= 1).sum())
    c4.metric("Fresh today", f"{fresh_count}/{len(summary)}")

    st.divider()
    st.subheader("Summary")
    st.dataframe(
        summary[["perpetuum_name", "status", "subjects", "flagged", "avg_score", "last_run", "stale_days"]]
        .style.format({"avg_score": "{:.1f}", "stale_days": "{:.0f}"})
        .background_gradient(subset=["avg_score"], cmap="RdYlGn", vmin=0, vmax=100)
        .background_gradient(subset=["flagged"], cmap="Reds", vmin=0, vmax=summary["flagged"].max() or 1),
        use_container_width=True,
    )

    # Trend chart — rows over time per perpetuum
    st.subheader("Subjects scored · 30d")
    hist = h.copy()
    hist["run_date"] = pd.to_datetime(hist["run_date"])
    cutoff = pd.Timestamp(date.today() - timedelta(days=30))
    hist = hist[hist["run_date"] >= cutoff]
    if not hist.empty:
        daily = hist.groupby([hist["run_date"].dt.date, "perpetuum_name"]).size().reset_index(name="rows")
        daily.columns = ["date", "perpetuum", "rows"]
        fig = px.line(daily, x="date", y="rows", color="perpetuum",
                      title="Daily rows scored per perpetuum")
        st.plotly_chart(fig, use_container_width=True)

    # Drill-down: pick perpetuum → top flagged
    st.subheader("Drill-down")
    chosen = st.selectbox("Perpetuum", summary["perpetuum_name"].tolist())
    sub = h[h["perpetuum_name"] == chosen].copy()
    sub_recent = sub.sort_values("run_date", ascending=False).drop_duplicates("subject_id")
    flagged_only = st.checkbox("Only flagged (flag_count > 0)", value=True)
    if flagged_only:
        sub_recent = sub_recent[sub_recent["flag_count"] > 0]
    sub_recent = sub_recent.sort_values(["flag_count", "score"], ascending=[False, True]).head(50)
    st.dataframe(
        sub_recent[["subject_id", "score", "flag_count", "tier", "action_hint", "run_date", "market"]],
        use_container_width=True,
        height=400,
    )


# ============================= PAGE 6: Paper Signals ========================

elif page == "Paper Signals":
    st.title("Paper signals")
    section_caption("YAML methods × portfolio · paper-only")

    @st.cache_data(ttl=60)
    def load_paper_signals() -> pd.DataFrame:
        rows = []
        for mkt, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                try:
                    df = pd.read_sql_query("SELECT * FROM paper_trade_signals", c)
                    df["market"] = mkt
                    rows.append(df)
                except Exception:
                    pass
        return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()

    ps = load_paper_signals()
    if ps.empty:
        st.warning("Sem paper signals. Corre `python -m library.matcher`.")
        st.stop()

    # KPIs
    open_n = int((ps["status"] == "open").sum())
    closed_n = int((ps["status"] != "open").sum())
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total signals", len(ps))
    c2.metric("Open", open_n)
    c3.metric("Closed", closed_n)
    c4.metric("Methods active", ps["method_id"].nunique())

    # Filters
    st.divider()
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        mkt_f = st.multiselect("Market", ["br", "us"], default=["br", "us"], key="ps_mkt")
    with fc2:
        status_opts = sorted(ps["status"].dropna().unique().tolist())
        status_f = st.multiselect("Status", status_opts, default=["open"] if "open" in status_opts else status_opts, key="ps_status")
    with fc3:
        method_f = st.multiselect("Method", sorted(ps["method_id"].dropna().unique()), key="ps_method")
    with fc4:
        ticker_f = st.text_input("Ticker filter", "", key="ps_ticker").strip().upper()

    filt = ps[ps["market"].isin(mkt_f)]
    if status_f:
        filt = filt[filt["status"].isin(status_f)]
    if method_f:
        filt = filt[filt["method_id"].isin(method_f)]
    if ticker_f:
        filt = filt[filt["ticker"].str.contains(ticker_f, na=False)]

    # Convergence detection: same ticker, multiple methods, status=open
    open_subset = filt[filt["status"] == "open"]
    convergence = open_subset.groupby("ticker")["method_id"].nunique().reset_index(name="methods_count")
    convergence = convergence[convergence["methods_count"] >= 2].sort_values("methods_count", ascending=False)
    if not convergence.empty:
        st.subheader(f"Convergent · ≥2 methods · {len(convergence)} tickers")
        st.dataframe(convergence, use_container_width=True, height=min(300, 40 * len(convergence) + 50))

    st.divider()
    st.subheader(f"Signals · {len(filt)} of {len(ps)}")
    show_cols = [c for c in ["ticker", "market", "method_id", "direction", "horizon",
                              "expected_move_pct", "entry_price", "status",
                              "signal_date", "closed_at", "realized_return_pct",
                              "thesis"] if c in filt.columns]
    sort_col = "signal_date" if "signal_date" in filt.columns else show_cols[0]
    st.dataframe(
        filt[show_cols].sort_values(sort_col, ascending=False).head(500),
        use_container_width=True, height=500,
    )


# ============================= PAGE 7: RI Timeline ==========================

elif page == "RI Timeline":
    st.title("RI timeline")
    section_caption("Quarterly history · CVM oficial · 5 stocks BR")

    @st.cache_data(ttl=300)
    def load_quarterly(ticker: str) -> pd.DataFrame:
        with sqlite3.connect(DB_BR) as c:
            return pd.read_sql_query(
                "SELECT * FROM quarterly_history WHERE ticker=? ORDER BY period_end",
                c, params=[ticker],
            )

    @st.cache_data(ttl=300)
    def list_ri_tickers() -> list[str]:
        with sqlite3.connect(DB_BR) as c:
            return [r[0] for r in c.execute(
                "SELECT DISTINCT ticker FROM quarterly_history ORDER BY ticker"
            ).fetchall()]

    tickers = list_ri_tickers()
    if not tickers:
        st.warning("Sem dados em quarterly_history. Corre `python -m library.ri.cvm_parser build`.")
        st.stop()

    ticker = st.selectbox("Ticker", tickers)
    qh = load_quarterly(ticker)

    if qh.empty:
        st.warning(f"Sem trimestres para {ticker}.")
        st.stop()

    # KPIs — latest period
    latest = qh.iloc[-1]
    prev = qh.iloc[-5] if len(qh) > 4 else None  # YoY

    def _yoy(metric: str) -> str:
        if prev is None or pd.isna(prev[metric]) or prev[metric] == 0:
            return ""
        delta = (latest[metric] - prev[metric]) / abs(prev[metric]) * 100
        return f"{delta:+.1f}% YoY"

    def _scale(v):
        if pd.isna(v):
            return "—"
        if abs(v) >= 1e9:
            return f"{v/1e9:.2f}B"
        if abs(v) >= 1e6:
            return f"{v/1e6:.1f}M"
        return f"{v:,.0f}"

    st.markdown(f"### {ticker} — último trimestre: **{latest['period_end']}** ({latest['source']})")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", _scale(latest["revenue"]), _yoy("revenue"))
    c2.metric("EBIT", _scale(latest["ebit"]), _yoy("ebit"))
    c3.metric("Net Income", _scale(latest["net_income"]), _yoy("net_income"))
    c4.metric("Equity", _scale(latest["equity"]), _yoy("equity"))

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Gross margin", f"{latest['gross_margin']*100:.1f}%" if not pd.isna(latest["gross_margin"]) else "—")
    c6.metric("EBIT margin", f"{latest['ebit_margin']*100:.1f}%" if not pd.isna(latest["ebit_margin"]) else "—")
    c7.metric("Net margin", f"{latest['net_margin']*100:.1f}%" if not pd.isna(latest["net_margin"]) else "—")
    c8.metric("Debt total", _scale(latest["debt_total"]))

    st.divider()

    # Charts
    qh_chart = qh.copy()
    qh_chart["period_end"] = pd.to_datetime(qh_chart["period_end"])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue · EBIT · Net Income")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["revenue"], name="Revenue", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["ebit"], name="EBIT", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["net_income"], name="Net Income", mode="lines+markers"))
        fig.update_layout(yaxis_title="Valor (BRL)", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Margens (%)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["gross_margin"] * 100, name="Gross %", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["ebit_margin"] * 100, name="EBIT %", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["net_margin"] * 100, name="Net %", mode="lines+markers"))
        fig.update_layout(yaxis_title="%", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Equity vs Debt")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["equity"], name="Equity", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["debt_total"], name="Debt", mode="lines+markers"))
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Cash flow")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["fco"], name="FCO (operação)", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["fci"], name="FCI (invest.)", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=qh_chart["period_end"], y=qh_chart["fcf_proxy"], name="FCF proxy", mode="lines+markers"))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(f"Trimestres · {len(qh)}")
    show = qh[["period_end", "source", "revenue", "ebit", "net_income", "equity",
               "gross_margin", "ebit_margin", "net_margin", "debt_total"]].copy()
    st.dataframe(
        show.style.format({
            "revenue": "{:,.0f}", "ebit": "{:,.0f}", "net_income": "{:,.0f}",
            "equity": "{:,.0f}", "debt_total": "{:,.0f}",
            "gross_margin": "{:.2%}", "ebit_margin": "{:.2%}", "net_margin": "{:.2%}",
        }),
        use_container_width=True, height=400,
    )

    # Link to vault
    ri_note_path = ROOT / "obsidian_vault" / "tickers" / f"{ticker}_RI.md"
    if ri_note_path.exists():
        st.info(f"📂 Vault note: `obsidian_vault/tickers/{ticker}_RI.md`")


# ============================= PAGE 8: YouTube ==============================

elif page == "YouTube Digest":
    st.title("YouTube digest")
    section_caption("Vídeos por canal e insights por ticker")
    with sqlite3.connect(DB_BR) as c:
        channels = [r[0] for r in c.execute("SELECT DISTINCT channel FROM videos WHERE channel IS NOT NULL ORDER BY channel")]
    channel = st.selectbox("Canal", ["(todos)"] + channels)
    days = st.slider("Últimos N dias", 7, 90, 30)
    cutoff = (date.today() - timedelta(days=days)).isoformat()

    with sqlite3.connect(DB_BR) as c:
        if channel == "(todos)":
            vids = pd.read_sql_query(
                "SELECT video_id, channel, title, published_at, duration_sec FROM videos "
                "WHERE published_at >= ? ORDER BY published_at DESC",
                c, params=[cutoff],
            )
        else:
            vids = pd.read_sql_query(
                "SELECT video_id, channel, title, published_at, duration_sec FROM videos "
                "WHERE channel=? AND published_at >= ? ORDER BY published_at DESC",
                c, params=[channel, cutoff],
            )
    st.metric("Vídeos no período", len(vids))

    if not vids.empty:
        ids = vids["video_id"].tolist()
        placeholders = ",".join(["?"] * len(ids))
        insights = []
        for db in (DB_BR, DB_US):
            with sqlite3.connect(db) as c:
                ins = pd.read_sql_query(
                    f"SELECT video_id, ticker, kind, claim, confidence FROM video_insights WHERE video_id IN ({placeholders})",
                    c, params=ids,
                )
                insights.append(ins)
        all_ins = pd.concat(insights, ignore_index=True)
        st.subheader("Tickers mais citados")
        top = all_ins["ticker"].value_counts().head(20).reset_index()
        top.columns = ["Ticker", "Count"]
        st.bar_chart(top.set_index("Ticker"))

        st.subheader("Insights")
        st.dataframe(all_ins.sort_values("confidence", ascending=False).head(50),
                     use_container_width=True, height=400)


# ============================= PAGE 4: Triggers ============================

elif page == "Triggers":
    st.title("Triggers fired")
    section_caption("Eventos disparados nos últimos 30 dias")
    import json
    log_dir = ROOT / "logs"
    rows = []
    cutoff = (date.today() - timedelta(days=30)).isoformat()
    for f in sorted(log_dir.glob("trigger_monitor_*.log"), reverse=True):
        if f.stem.split("_")[-1] < cutoff:
            continue
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("event") == "fired":
                rows.append(d)
    if rows:
        df_t = pd.DataFrame(rows)
        st.dataframe(df_t[["ts", "trigger_id", "ticker", "market", "kind", "snapshot"]].tail(100),
                     use_container_width=True, height=500)
    else:
        st.info("Nenhum trigger fired nos últimos 30d.")


# ============================= PAGE 5: Screener ============================

elif page == "Screener":
    st.title("Screener")
    section_caption("Filtros live sobre o universo BR + US")
    with sqlite3.connect(DB_BR) as c:
        br = pd.read_sql_query("""
            SELECT c.ticker, c.name, c.sector, c.is_holding, 'br' AS market,
                   f.pe, f.pb, f.dy, f.roe, f.dividend_streak_years,
                   s.score AS screen_score, s.passes_screen
            FROM companies c
            LEFT JOIN (SELECT ticker, MAX(period_end) AS mp FROM fundamentals GROUP BY ticker) lf
                ON lf.ticker=c.ticker
            LEFT JOIN fundamentals f ON f.ticker=c.ticker AND f.period_end=lf.mp
            LEFT JOIN (SELECT ticker, MAX(run_date) AS md FROM scores GROUP BY ticker) ls
                ON ls.ticker=c.ticker
            LEFT JOIN scores s ON s.ticker=c.ticker AND s.run_date=ls.md
        """, c)
    with sqlite3.connect(DB_US) as c:
        us = pd.read_sql_query("""
            SELECT c.ticker, c.name, c.sector, c.is_holding, 'us' AS market,
                   f.pe, f.pb, f.dy, f.roe, f.dividend_streak_years,
                   s.score AS screen_score, s.passes_screen
            FROM companies c
            LEFT JOIN (SELECT ticker, MAX(period_end) AS mp FROM fundamentals GROUP BY ticker) lf
                ON lf.ticker=c.ticker
            LEFT JOIN fundamentals f ON f.ticker=c.ticker AND f.period_end=lf.mp
            LEFT JOIN (SELECT ticker, MAX(run_date) AS md FROM scores GROUP BY ticker) ls
                ON ls.ticker=c.ticker
            LEFT JOIN scores s ON s.ticker=c.ticker AND s.run_date=ls.md
        """, c)
    df = pd.concat([br, us], ignore_index=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        mkt_filt = st.multiselect("Market", ["br", "us"], default=["br", "us"])
    with col2:
        sector_filt = st.multiselect("Sector", sorted(df["sector"].dropna().unique()))
    with col3:
        pe_max = st.slider("P/E max", 0.0, 80.0, 25.0)
    with col4:
        dy_min = st.slider("DY min %", 0.0, 15.0, 2.0) / 100
    with col5:
        roe_min = st.slider("ROE min %", 0.0, 50.0, 10.0) / 100

    filt = df[df["market"].isin(mkt_filt)]
    if sector_filt:
        filt = filt[filt["sector"].isin(sector_filt)]
    filt = filt[filt["pe"].fillna(99) <= pe_max]
    filt = filt[filt["dy"].fillna(0) >= dy_min]
    filt = filt[filt["roe"].fillna(0) >= roe_min]

    st.metric("Candidates", len(filt))
    st.dataframe(
        filt.sort_values("screen_score", ascending=False),
        use_container_width=True, height=500,
    )
