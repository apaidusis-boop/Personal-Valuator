"""FII inf_mensal CVM ingest — monthly NAV/DY/cotistas para os 5 FIIs do catalog.

Source: dados.cvm.gov.br/dados/FII/DOC/INF_MENSAL/DADOS/inf_mensal_fii_<YYYY>.zip
Ano = ano civil; cada ZIP contém 3 CSVs:
  - inf_mensal_fii_geral       (identificação + segmento)
  - inf_mensal_fii_complemento (NAV, dividend yield, cotistas, rentabilidade)
  - inf_mensal_fii_ativo_passivo (breakdown patrimonial detalhado)

Fluxo:
  1. Download (cached, TTL 7 days for current year, 365 days for past years)
  2. Resolve CNPJ for catalog FIIs sem cnpj — via Nome_Fundo_Classe pattern match
  3. Filter all 3 CSVs to nossos CNPJs
  4. Insert into fii_monthly + fii_balance_sheet (granular)

Uso:
    python -m library.ri.fii_filings download --year 2025
    python -m library.ri.fii_filings resolve-cnpjs --year 2025
    python -m library.ri.fii_filings ingest --year 2025
    python -m library.ri.fii_filings show XPML11
"""
from __future__ import annotations

import argparse
import csv
import io
import sqlite3
import sys
import time
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "br_investments.db"
CACHE = ROOT / "library" / "ri" / "cache" / "FII_INF_MENSAL"

CACHE.mkdir(parents=True, exist_ok=True)

URL = "https://dados.cvm.gov.br/dados/FII/DOC/INF_MENSAL/DADOS/inf_mensal_fii_{year}.zip"
USER_AGENT = "investment-intelligence-bot/1.0 (personal-research; non-commercial)"

# Heuristic name patterns para FIIs sem CNPJ explícito
NAME_PATTERNS = {
    "VGIR11": ["VALORA RE III", "VALORA CRI"],
    "PVBI11": ["VBI PRIME", "VBI PRIME PROPERTIES"],
    "RBRX11": ["RBR X", "RBR ALPHA MULTIESTRATEGIA"],
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS fii_monthly (
    cnpj                              TEXT NOT NULL,
    ticker                            TEXT,
    period_end                        TEXT NOT NULL,
    patrimonio_liquido                REAL,
    cotas_emitidas                    REAL,
    valor_patrimonial_cota            REAL,
    rentabilidade_efetiva_mes_pct     REAL,
    rentabilidade_patrimonial_mes_pct REAL,
    dy_mes_pct                        REAL,
    total_cotistas                    INTEGER,
    pf_cotistas                       INTEGER,
    nome_fundo                        TEXT,
    segmento                          TEXT,
    PRIMARY KEY (cnpj, period_end)
);

CREATE INDEX IF NOT EXISTS idx_fii_ticker ON fii_monthly(ticker, period_end);

CREATE TABLE IF NOT EXISTS fii_balance_sheet (
    cnpj                       TEXT NOT NULL,
    ticker                     TEXT,
    period_end                 TEXT NOT NULL,
    total_investido            REAL,
    direitos_bens_imoveis      REAL,
    imoveis_renda_acabados     REAL,
    imoveis_renda_construcao   REAL,
    cri_cra                    REAL,
    fii                        REAL,        -- holdings em outros FIIs
    debentures                 REAL,
    contas_receber_aluguel     REAL,
    rendimentos_distribuir     REAL,
    total_passivo              REAL,
    PRIMARY KEY (cnpj, period_end)
);

CREATE INDEX IF NOT EXISTS idx_fiibs_ticker ON fii_balance_sheet(ticker, period_end);
"""


def ensure_schema() -> None:
    with sqlite3.connect(DB) as c:
        c.executescript(SCHEMA)
        c.commit()


def cache_path(year: int) -> Path:
    return CACHE / f"inf_mensal_fii_{year}.zip"


def download(year: int, force: bool = False, ttl_days: int = 7) -> Path:
    p = cache_path(year)
    if p.exists() and not force:
        age = (time.time() - p.stat().st_mtime) / 86400
        if age < ttl_days:
            return p
    url = URL.format(year=year)
    print(f"[fii_filings] downloading {url}")
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=120)
    r.raise_for_status()
    p.write_bytes(r.content)
    print(f"  saved {len(r.content)/1024/1024:.1f}MB to {p.relative_to(ROOT)}")
    return p


def _read_zip_csv(zip_path: Path, name_substr: str) -> list[dict]:
    with zipfile.ZipFile(zip_path) as zf:
        for n in zf.namelist():
            if name_substr in n and n.endswith(".csv"):
                with zf.open(n) as f:
                    text = io.TextIOWrapper(f, encoding="latin-1", newline="")
                    return list(csv.DictReader(text, delimiter=";"))
    return []


def fii_catalog_cnpjs() -> dict[str, dict]:
    """Return {cnpj_clean: {ticker, name, ...}} for all FIIs (holdings + watchlist)."""
    from library.ri import catalog
    out = {}
    for entry in catalog.all_fiis(include_watchlist=True):
        cnpj = entry.get("cnpj")
        if cnpj:
            cnpj_clean = "".join(c for c in cnpj if c.isdigit())
            out[cnpj_clean] = entry
    return out


def resolve_missing_cnpjs(year: int) -> dict:
    """For FIIs in catalog (holdings + watchlist) without CNPJ, search geral CSV by name pattern."""
    from library.ri import catalog as _catalog
    p = download(year)
    geral = _read_zip_csv(p, "geral")
    resolved = {}
    for entry in _catalog.all_fiis(include_watchlist=True):
        ticker = entry["ticker"]
        if entry.get("cnpj"):
            continue
        patterns = NAME_PATTERNS.get(ticker, [ticker.rstrip("0123456789")])
        for row in geral:
            nome = (row.get("Nome_Fundo_Classe") or "").upper()
            for pat in patterns:
                if pat.upper() in nome:
                    resolved[ticker] = {
                        "cnpj": row.get("CNPJ_Fundo_Classe"),
                        "nome": row.get("Nome_Fundo_Classe"),
                        "segmento": row.get("Segmento_Atuacao"),
                    }
                    break
            if ticker in resolved:
                break
    return resolved


def ingest(year: int, ticker_filter: str | None = None) -> dict:
    ensure_schema()
    p = download(year)
    geral = _read_zip_csv(p, "geral")
    comp = _read_zip_csv(p, "complemento")
    ap_data = _read_zip_csv(p, "ativo_passivo")

    cnpjs_map = fii_catalog_cnpjs()
    # Augment with resolve_missing_cnpjs (in-memory; doesn't update catalog)
    resolved = resolve_missing_cnpjs(year)
    for ticker, info in resolved.items():
        cnpj_clean = "".join(c for c in (info["cnpj"] or "") if c.isdigit())
        if cnpj_clean and cnpj_clean not in cnpjs_map:
            cnpjs_map[cnpj_clean] = {"ticker": ticker, "name": info["nome"]}
            print(f"  resolved {ticker} -> CNPJ {info['cnpj']}")

    # Build geral lookup (for ticker + segmento per CNPJ)
    geral_lookup = {}
    for row in geral:
        cn = "".join(c for c in (row.get("CNPJ_Fundo_Classe") or "") if c.isdigit())
        geral_lookup[cn] = row

    counts = {"monthly": 0, "balance": 0}

    with sqlite3.connect(DB) as c:
        # Complemento → fii_monthly
        for row in comp:
            cn = "".join(ch for ch in (row.get("CNPJ_Fundo_Classe") or "") if ch.isdigit())
            if cn not in cnpjs_map:
                continue
            entry = cnpjs_map[cn]
            ticker = entry.get("ticker")
            if ticker_filter and ticker != ticker_filter:
                continue
            geral_row = geral_lookup.get(cn, {})
            try:
                c.execute(
                    """INSERT OR REPLACE INTO fii_monthly
                       (cnpj, ticker, period_end, patrimonio_liquido, cotas_emitidas,
                        valor_patrimonial_cota, rentabilidade_efetiva_mes_pct,
                        rentabilidade_patrimonial_mes_pct, dy_mes_pct,
                        total_cotistas, pf_cotistas, nome_fundo, segmento)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        cn, ticker, row.get("Data_Referencia"),
                        _f(row.get("Patrimonio_Liquido")),
                        _f(row.get("Cotas_Emitidas")),
                        _f(row.get("Valor_Patrimonial_Cotas")),
                        _f(row.get("Percentual_Rentabilidade_Efetiva_Mes")),
                        _f(row.get("Percentual_Rentabilidade_Patrimonial_Mes")),
                        _f(row.get("Percentual_Dividend_Yield_Mes")),
                        _i(row.get("Total_Numero_Cotistas")),
                        _i(row.get("Numero_Cotistas_Pessoa_Fisica")),
                        geral_row.get("Nome_Fundo_Classe"),
                        geral_row.get("Segmento_Atuacao"),
                    ),
                )
                counts["monthly"] += 1
            except Exception as e:
                print(f"  monthly insert error {ticker}: {e}")

        # Ativo_passivo → fii_balance_sheet
        for row in ap_data:
            cn = "".join(ch for ch in (row.get("CNPJ_Fundo_Classe") or "") if ch.isdigit())
            if cn not in cnpjs_map:
                continue
            entry = cnpjs_map[cn]
            ticker = entry.get("ticker")
            if ticker_filter and ticker != ticker_filter:
                continue
            try:
                c.execute(
                    """INSERT OR REPLACE INTO fii_balance_sheet
                       (cnpj, ticker, period_end, total_investido, direitos_bens_imoveis,
                        imoveis_renda_acabados, imoveis_renda_construcao, cri_cra, fii,
                        debentures, contas_receber_aluguel, rendimentos_distribuir, total_passivo)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        cn, ticker, row.get("Data_Referencia"),
                        _f(row.get("Total_Investido")),
                        _f(row.get("Direitos_Bens_Imoveis")),
                        _f(row.get("Imoveis_Renda_Acabados")),
                        _f(row.get("Imoveis_Renda_Construcao")),
                        _f(row.get("CRI_CRA")) or _f(row.get("CRI")),
                        _f(row.get("FII")),
                        _f(row.get("Debentures")),
                        _f(row.get("Contas_Receber_Aluguel")),
                        _f(row.get("Rendimentos_Distribuir")),
                        _f(row.get("Total_Passivo")),
                    ),
                )
                counts["balance"] += 1
            except Exception as e:
                pass
        c.commit()
    return counts


def _f(v) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v.replace(",", "."))
    except (ValueError, AttributeError):
        return None


def _i(v) -> int | None:
    f = _f(v)
    return int(f) if f is not None else None


def show(ticker: str) -> None:
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT period_end, patrimonio_liquido, cotas_emitidas, valor_patrimonial_cota,
                   rentabilidade_efetiva_mes_pct, dy_mes_pct, total_cotistas
            FROM fii_monthly WHERE ticker=? ORDER BY period_end DESC
        """, (ticker,)).fetchall()
    if not rows:
        print(f"No data for {ticker}. Run ingest first.")
        return
    print(f"\n=== {ticker} — fii_monthly ({len(rows)} months) ===")
    print(f"{'period':<12} {'PL (R$mi)':>12} {'cotas':>14} {'NAV/cota':>10} {'ret_ef%':>8} {'DY_mes%':>8} {'cotistas':>10}")
    print("-" * 90)
    for r in rows[:24]:
        pl = (r['patrimonio_liquido'] or 0) / 1e6
        cot = r['cotas_emitidas'] or 0
        nav = r['valor_patrimonial_cota'] or 0
        re_ = r['rentabilidade_efetiva_mes_pct'] or 0
        dy = r['dy_mes_pct'] or 0
        ct = r['total_cotistas'] or 0
        print(f"{r['period_end']:<12} {pl:>12,.1f} {cot:>14,.0f} {nav:>10,.2f} {re_:>8.2f} {dy:>8.2f} {ct:>10,}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    p_dl = sub.add_parser("download"); p_dl.add_argument("--year", type=int, required=True); p_dl.add_argument("--force", action="store_true")
    p_res = sub.add_parser("resolve-cnpjs"); p_res.add_argument("--year", type=int, required=True)
    p_ing = sub.add_parser("ingest"); p_ing.add_argument("--year", type=int, required=True); p_ing.add_argument("--ticker")
    p_show = sub.add_parser("show"); p_show.add_argument("ticker")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.cmd == "download":
        download(args.year, force=args.force)
    elif args.cmd == "resolve-cnpjs":
        r = resolve_missing_cnpjs(args.year)
        print(f"Resolved {len(r)} CNPJs:")
        for ticker, info in r.items():
            print(f"  {ticker:<8} -> {info['cnpj']}  {info['nome'][:50]}  ({info['segmento']})")
    elif args.cmd == "ingest":
        r = ingest(args.year, ticker_filter=args.ticker)
        print(f"\nResult: monthly={r['monthly']} balance_rows={r['balance']}")
    elif args.cmd == "show":
        show(args.ticker.upper())
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
