"""BACEN IF.Data fetcher — popula CET1, Tier1, Basel ratio, RWA, NPL para bancos.

API pública Olinda OData, sem autenticação:
    https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/

Endpoints usados:
    IfDataValores(AnoMes=YYYYMM, TipoInstituicao=N, Relatorio='X')

Mapping CodInst (descoberto via IfDataCadastro):
    - Relatório 5 (Capital) usa TipoInstituicao=1 + Conglomerado **Prudencial**
        BBDC4 → C0080075,  ITUB4 → C0080099
    - Relatório 8 (Crédito por nível A-H) usa TipoInstituicao=2 + Conglomerado **Financeiro**
        BBDC4 → C0010045,  ITUB4 → C0010069

Persiste em data/br_investments.db, tabela `bank_quarterly_history`
(UPDATE em rows existentes — não cria novas).

Idempotente. Cacheable. Resilient: skip silencioso quando IF.Data não tem dados
para um período (BACEN às vezes só publica T-1 trimestres).

Uso:
    python fetchers/bacen_ifdata_fetcher.py --ticker BBDC4
    python fetchers/bacen_ifdata_fetcher.py --all
    python fetchers/bacen_ifdata_fetcher.py --all --since 2023-01-01
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"

OLINDA_BASE = "https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata"

# ticker → {prudencial, financeiro}
# Prudencial cobre Capital/Basel; Financeiro cobre operações de crédito.
BANK_CODE_MAP: dict[str, dict[str, str]] = {
    "BBDC4": {"prudencial": "C0080075", "financeiro": "C0010045"},
    "ITUB4": {"prudencial": "C0080099", "financeiro": "C0010069"},
}

# nome de coluna BACEN → coluna na bank_quarterly_history
# (substring match case-insensitive — BACEN tem newlines/whitespace nos nomes)
CAPITAL_FIELDS = {
    "índice de capital principal": "cet1_ratio",         # CET1
    "índice de basileia": "basel_ratio",                 # Basel total
    "ativos ponderados pelo risco (rwa)": "rwa",         # RWA
    # tier1 não tem coluna na DB hoje — guardamos basel + cet1 só
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "bacen_ifdata.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _period_end_to_anomes(period_end: str) -> int:
    """`'2024-12-31'` → `202412`."""
    return int(period_end[:4] + period_end[5:7])


def _fetch(tipo: int, relatorio: str, anomes: int, cod_inst: str,
           retries: int = 2, sleep_s: float = 1.0) -> list[dict]:
    """GET IfDataValores filtrado por CodInst. Retorna lista de rows."""
    # NB: BACEN OData só aceita %20 (não +) em $filter.
    # requests.get(params=...) substitui espaço por +, por isso
    # construímos a URL manualmente com urllib.parse.quote (safe vazio).
    filter_q = quote(f"CodInst eq '{cod_inst}'", safe="")
    url = (
        f"{OLINDA_BASE}/IfDataValores"
        f"(AnoMes={anomes},TipoInstituicao={tipo},Relatorio='{relatorio}')"
        f"?$format=json&$filter={filter_q}"
    )
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                return r.json().get("value", []) or []
            last_err = RuntimeError(f"HTTP {r.status_code}")
        except Exception as e:
            last_err = e
        time.sleep(sleep_s * (attempt + 1))
    _log({"event": "bacen_fetch_error", "anomes": anomes, "tipo": tipo,
          "rel": relatorio, "cod": cod_inst, "error": str(last_err)[:120]})
    return []


def _extract_capital(rows: list[dict]) -> dict[str, float]:
    """Rel 5 → {cet1_ratio, basel_ratio, rwa, tier1_ratio}."""
    out: dict[str, float] = {}
    for row in rows:
        nome = (row.get("NomeColuna") or "").strip().lower()
        # remove newlines/extra whitespace
        nome_norm = " ".join(nome.split())
        for needle, col in CAPITAL_FIELDS.items():
            if needle in nome_norm:
                try:
                    out[col] = float(row.get("Saldo"))
                except (TypeError, ValueError):
                    pass
                break
    return out


def _extract_npl(rows: list[dict]) -> dict[str, float]:
    """Rel 8 (carteira A-H) → {npl_ratio}.
    NPL definition: nível E-H / Total Geral. Níveis E em diante exigem
    provisão >= 30% (atrasos > 90 dias). Excluímos D porque inclui
    operações renegociadas que ainda performam."""
    by_level: dict[str, float] = {}
    for row in rows:
        nome = (row.get("NomeColuna") or "").strip()
        try:
            saldo = float(row.get("Saldo"))
        except (TypeError, ValueError):
            continue
        by_level[nome] = saldo
    total = by_level.get("Total Geral")
    if not total or total <= 0:
        return {}
    npl_value = sum(by_level.get(lvl, 0.0) for lvl in ("E", "F", "G", "H"))
    return {"npl_ratio": npl_value / total}


def _periods_for_ticker(conn: sqlite3.Connection, ticker: str,
                        since: str | None = None) -> list[str]:
    sql = "SELECT DISTINCT period_end FROM bank_quarterly_history WHERE ticker = ?"
    params: list = [ticker]
    if since:
        sql += " AND period_end >= ?"
        params.append(since)
    sql += " ORDER BY period_end"
    return [r[0] for r in conn.execute(sql, params).fetchall()]


def update_bank_row(conn: sqlite3.Connection, ticker: str, period_end: str,
                    capital: dict[str, float], npl: dict[str, float]) -> bool:
    merged = {**capital, **npl}
    if not merged:
        return False
    cols = ", ".join(f"{k} = ?" for k in merged)
    values = list(merged.values()) + [ticker, period_end]
    # Retry com backoff explicito; SQLite WAL ainda assim pode bloquear se
    # outro writer (perpetuum, dashboard refresh) detém lock breve.
    for attempt in range(8):
        try:
            conn.execute(
                f"UPDATE bank_quarterly_history SET {cols} "
                f"WHERE ticker = ? AND period_end = ?", values,
            )
            return True
        except sqlite3.OperationalError as e:
            if "locked" not in str(e).lower():
                raise
            time.sleep(2 ** min(attempt, 5))
    raise sqlite3.OperationalError(
        f"database remained locked após 8 retries para {ticker}@{period_end}")


def fetch_ticker(ticker: str, since: str | None = None) -> dict:
    if ticker not in BANK_CODE_MAP:
        raise SystemExit(f"ticker {ticker!r} não está em BANK_CODE_MAP. "
                         f"Conhecidos: {list(BANK_CODE_MAP)}")
    codes = BANK_CODE_MAP[ticker]
    stats = {"ticker": ticker, "periods_total": 0, "periods_updated": 0,
             "periods_partial": 0, "periods_empty": 0,
             "first_period": None, "last_period": None,
             "sample_basel": None, "sample_npl": None}

    # Read-only periods list — short conn
    with sqlite3.connect(DB_PATH, timeout=30) as conn:
        periods = _periods_for_ticker(conn, ticker, since=since)
    stats["periods_total"] = len(periods)

    for period_end in periods:
        anomes = _period_end_to_anomes(period_end)
        cap_rows = _fetch(tipo=1, relatorio="5", anomes=anomes,
                          cod_inst=codes["prudencial"])
        npl_rows = _fetch(tipo=2, relatorio="8", anomes=anomes,
                          cod_inst=codes["financeiro"])
        capital = _extract_capital(cap_rows)
        npl = _extract_npl(npl_rows)
        if not (capital or npl):
            stats["periods_empty"] += 1
            continue
        # Open short-lived conn per UPDATE — minimiza window de lock
        with sqlite3.connect(DB_PATH, timeout=30) as conn:
            conn.execute("PRAGMA busy_timeout=30000")
            wrote = update_bank_row(conn, ticker, period_end, capital, npl)
            conn.commit()
        if wrote:
            stats["periods_updated"] += 1
            if stats["first_period"] is None:
                stats["first_period"] = period_end
            stats["last_period"] = period_end
            if stats["sample_basel"] is None and "basel_ratio" in capital:
                stats["sample_basel"] = capital["basel_ratio"]
            if stats["sample_npl"] is None and "npl_ratio" in npl:
                stats["sample_npl"] = npl["npl_ratio"]
            if not (capital and npl):
                stats["periods_partial"] += 1
        # Per-period log line (helps observability)
        print(f"  [{ticker}] {period_end} -> "
              f"basel={capital.get('basel_ratio',0):.2%} "
              f"cet1={capital.get('cet1_ratio',0):.2%} "
              f"npl={npl.get('npl_ratio',0):.2%}", flush=True)

    _log({"event": "bacen_ticker_done", **stats})
    return stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", help="Single bank ticker (BBDC4|ITUB4)")
    ap.add_argument("--all", action="store_true",
                    help="Run all banks in BANK_CODE_MAP")
    ap.add_argument("--since", default=None,
                    help="Only periods >= YYYY-MM-DD")
    args = ap.parse_args()

    if not args.ticker and not args.all:
        ap.error("indicar --ticker X ou --all")

    targets = [args.ticker] if args.ticker else list(BANK_CODE_MAP)
    summary = []
    for t in targets:
        summary.append(fetch_ticker(t, since=args.since))

    print("\n=== Summary ===")
    for s in summary:
        print(f"  {s['ticker']}: {s['periods_updated']}/{s['periods_total']} "
              f"updated ({s['periods_partial']} partial, "
              f"{s['periods_empty']} empty) | "
              f"basel sample={s['sample_basel']} npl sample={s['sample_npl']}")


if __name__ == "__main__":
    main()
