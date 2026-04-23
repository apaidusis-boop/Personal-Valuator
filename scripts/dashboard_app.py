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
)


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
    st.title("💼 Investment Intelligence")
    page = st.radio(
        "Navegação",
        ["Portfolio", "Ticker Deep Dive", "YouTube Digest", "Triggers", "Screener"],
        label_visibility="collapsed",
    )
    st.divider()
    fx_rate = load_fx()
    st.caption(f"PTAX USDBRL: **{fx_rate:.4f}**")
    st.caption(f"Data hoje: {date.today().isoformat()}")


# ============================= PAGE 1: Portfolio ===========================

if page == "Portfolio":
    st.title("💼 Minha Carteira")
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
    st.subheader("📋 Holdings")
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
    st.title("🔍 Ticker Deep Dive")
    df = load_holdings()
    all_tickers = sorted(set(df["ticker"].tolist()) |
                         set(t for mk, db in (("br", DB_BR), ("us", DB_US))
                             for (t,) in sqlite3.connect(db).execute("SELECT ticker FROM companies")))
    ticker = st.selectbox("Ticker", all_tickers, index=all_tickers.index("ACN") if "ACN" in all_tickers else 0)

    from scripts.refresh_ticker import _market_of
    market = _market_of(ticker)

    # Verdict
    st.subheader("🎯 Verdict")
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
        st.subheader(f"📺 YouTube insights (últimos 180d, {len(yt)} encontrados)")
        st.dataframe(yt, use_container_width=True, height=300)


# ============================= PAGE 3: YouTube ==============================

elif page == "YouTube Digest":
    st.title("📺 YouTube Digest")
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
    st.title("🎯 Triggers fired (últimos 30d)")
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
    st.title("📊 Screener")
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
