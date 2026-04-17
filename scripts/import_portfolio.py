"""Importador de carteira real — BR (XP xlsx) + US (JPM csv).

Popula `portfolio_positions` com quantidade, preço médio (cost basis) e data
de carregamento em ambas as DBs. Substitui `seed_portfolio.py` para os
holdings equities reais (tesouro/debêntures/CRAs ficam fora — o schema
actual só modela equity).

Formato BR: XP "PosiçãoDetalhada" xlsx — secções "Ações", "Fundos Imobiliários".
Formato US: J.P. Morgan Wealth "positions.csv".

Uso:
    python scripts/import_portfolio.py --br "<path>.xlsx" --us "<path>.csv"
    python scripts/import_portfolio.py --br "<path>.xlsx"      # só BR
    python scripts/import_portfolio.py --dry-run --br "..."    # não grava
"""
from __future__ import annotations

import argparse
import csv
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

TODAY = date.today().isoformat()


def ensure_schema(conn: sqlite3.Connection) -> None:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(portfolio_positions)").fetchall()}
    if "quantity" not in cols:
        conn.execute("ALTER TABLE portfolio_positions ADD COLUMN quantity REAL")
    if "notes" not in cols:
        conn.execute("ALTER TABLE portfolio_positions ADD COLUMN notes TEXT")


def _parse_brl(v: object) -> float | None:
    """Parser para números no formato BR (XP): '.' é milhar, ',' é decimal.
    'R$ 1.234,56' → 1234.56
    '1.026'        → 1026  (sem vírgula, '.' vira milhar)
    '120,27'       → 120.27
    Para números sem separadores (US format), retorna como está."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace("R$", "").replace("\xa0", " ").strip()
    s = s.replace("%", "").strip()
    if "," in s:
        # BR: decimal = ",". Remove "." milhares.
        s = s.replace(".", "").replace(",", ".")
    elif "." in s:
        # sem vírgula: "." é milhar (XP). Cuidado: pode ser decimal US.
        # Heurística: se depois do último "." há exactamente 3 dígitos e inteiro
        # antes > 0, é milhar. Caso contrário decimal.
        parts = s.split(".")
        if len(parts) >= 2 and len(parts[-1]) == 3 and all(p.isdigit() for p in parts):
            s = "".join(parts)
    try:
        return float(s)
    except ValueError:
        return None


def _parse_us_number(v: object) -> float | None:
    """US format: ',' é milhar, '.' é decimal. '1,234.56' → 1234.56."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace("$", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def _upsert_company(conn: sqlite3.Connection, ticker: str, name: str,
                    currency: str, sector: str | None = None) -> None:
    conn.execute(
        """INSERT INTO companies (ticker, name, sector, is_holding, currency)
           VALUES (?, ?, ?, 1, ?)
           ON CONFLICT(ticker) DO UPDATE SET
             name=COALESCE(excluded.name, companies.name),
             sector=COALESCE(excluded.sector, companies.sector),
             is_holding=1""",
        (ticker, name, sector, currency),
    )


def _upsert_position(conn: sqlite3.Connection, ticker: str, quantity: float,
                     entry_price: float, entry_date: str,
                     notes: str | None = None) -> None:
    # weight recalculado no fim (pass final); por enquanto placeholder
    conn.execute(
        """INSERT INTO portfolio_positions
             (ticker, weight, entry_date, entry_price, active, quantity, notes)
           VALUES (?, 0.0, ?, ?, 1, ?, ?)
           ON CONFLICT(ticker, entry_date) DO UPDATE SET
             entry_price=excluded.entry_price,
             quantity=excluded.quantity,
             active=1,
             notes=excluded.notes""",
        (ticker, entry_date, entry_price, quantity, notes),
    )


def _recompute_weights(conn: sqlite3.Connection) -> None:
    """Pesos = valor actual (quantity × último close) / total. Se sem preço,
    cai para cost basis (qty × entry_price)."""
    rows = conn.execute(
        "SELECT ticker, entry_date, quantity, entry_price FROM portfolio_positions WHERE active=1"
    ).fetchall()
    mv: list[tuple[str, str, float]] = []
    for tk, ed, qty, ep in rows:
        px = conn.execute(
            "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (tk,)
        ).fetchone()
        unit = px[0] if px and px[0] else ep
        mv.append((tk, ed, (qty or 0) * unit))
    total = sum(v for _, _, v in mv) or 1.0
    for tk, ed, v in mv:
        conn.execute(
            "UPDATE portfolio_positions SET weight=? WHERE ticker=? AND entry_date=?",
            (v / total, tk, ed),
        )


# ========== BR — XP xlsx ==========

BR_ETF_ADDITIONS = [
    # ticker, name, sector — para inclusão no universe + companies
    ("LFTB11", "iShares Tesouro Selic ETF", "ETF-RF"),
    ("IVVB11", "iShares S&P 500 (BRL)",      "ETF-US"),
]


def _load_br_stocks_fiis(xlsx_path: Path) -> tuple[list[dict], list[dict], dict]:
    """Devolve (acoes, fiis, meta). Só varre as secções 'Ações' e 'Fundos
    Imobiliários'. Header das duas:
      Ações  : ticker, Posição, %, Rent%, PM, Último, Qtd
      FIIs   : ticker, Posição, %, Rent%_prov, Rent%_bruta, PM, Último, Qtd
    """
    import openpyxl
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))

    acoes: list[dict] = []
    fiis: list[dict] = []
    meta: dict = {"total_patrimonio": None}

    section = None
    # XP tem secção "Proventos" com sub-blocos "Ações"/"Fundos Imobiliários"
    # que são *dividendos pendentes*, não posições. Após ver Proventos ou
    # Dividendos, bloqueamos as secções de tickers.
    after_proventos = False
    for i, row in enumerate(rows):
        cells = [str(c).strip() if c is not None else "" for c in row]
        if not any(cells):
            continue
        c0 = cells[0]
        if c0.startswith("R$") and meta["total_patrimonio"] is None:
            meta["total_patrimonio"] = _parse_brl(c0)
        if c0.startswith("Dividendos") or c0 == "Proventos" or c0 == "Custódia Remunerada":
            after_proventos = True
            section = "skip"
            continue
        if not after_proventos:
            if c0 == "Ações":
                section = "acoes"
                continue
            if c0 == "Fundos Imobiliários":
                section = "fiis"
                continue
        if c0 in ("Tesouro Direto", "Fundos de Investimentos", "Renda Fixa"):
            section = "skip"
            continue
        # linhas header das tabelas (começam com "% | ..." ou "0,X% | ...")
        if re.match(r"^\d", c0) and "|" in c0:
            continue

        # linhas de ticker têm tipo "XXXX3" ou "XXXXX11" na primeira coluna
        if section in ("acoes", "fiis") and re.match(r"^[A-Z]{3,6}\d{1,2}$", c0):
            qty_col = 6 if section == "acoes" else 7
            pm_col  = 4 if section == "acoes" else 5
            item = {
                "ticker": c0,
                "posicao": _parse_brl(cells[1]),
                "preco_medio": _parse_brl(cells[pm_col]),
                "ultimo": _parse_brl(cells[pm_col + 1]),
                "quantidade": _parse_brl(cells[qty_col]),
            }
            if section == "acoes":
                acoes.append(item)
            else:
                fiis.append(item)

    return acoes, fiis, meta


def import_br(xlsx_path: Path, dry_run: bool = False) -> dict:
    acoes, fiis, meta = _load_br_stocks_fiis(xlsx_path)
    print(f"\n=== BR: Ações ({len(acoes)}) + FIIs ({len(fiis)}) ===")
    print(f"  total_patrimonio (XP): R$ {meta['total_patrimonio']:,.2f}")

    if dry_run:
        for a in acoes + fiis:
            q = a.get("quantidade") or 0
            pm = a.get("preco_medio") or 0
            last = a.get("ultimo") or 0
            pos = a.get("posicao") or 0
            print(f"  DRY  {a['ticker']:8s} qty={q:>9.2f}  pm=R${pm:<8.2f}  last=R${last:<8.2f}  pos=R${pos:>12,.2f}")
        return {"acoes": acoes, "fiis": fiis, "meta": meta}

    with sqlite3.connect(DB_BR) as conn:
        ensure_schema(conn)

        # ETFs novos (LFTB11, IVVB11) para entrar em companies
        for tk, nm, sec in BR_ETF_ADDITIONS:
            _upsert_company(conn, tk, nm, "BRL", sec)

        # Limpa imports anteriores da mesma data (permite re-correr)
        conn.execute("DELETE FROM portfolio_positions WHERE entry_date = ?", (TODAY,))

        for a in acoes + fiis:
            if not a["ticker"] or not a["quantidade"] or not a["preco_medio"]:
                continue
            _upsert_position(
                conn, a["ticker"], a["quantidade"], a["preco_medio"],
                TODAY, notes=f"XP import {TODAY}"
            )
            # garante is_holding=1 em companies (idempotente)
            conn.execute(
                "UPDATE companies SET is_holding=1 WHERE ticker=?", (a["ticker"],)
            )

        _recompute_weights(conn)
        conn.commit()

        total_mv = conn.execute(
            "SELECT sum(quantity * (select close from prices p where p.ticker=pp.ticker order by date desc limit 1)) "
            "FROM portfolio_positions pp WHERE active=1"
        ).fetchone()[0] or 0
        print(f"  persistido: {len(acoes)+len(fiis)} posições")
        print(f"  MV calculado (último close DB): R$ {total_mv:,.2f}")

    return {"acoes": acoes, "fiis": fiis, "meta": meta}


# ========== US — JPM CSV ==========

US_SKIP = {"QACDS", "", None}  # cash sweep + USD cash line


def import_us(csv_path: Path, dry_run: bool = False) -> dict:
    positions: list[dict] = []
    with csv_path.open("r", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            tk = (row.get("Ticker") or "").strip()
            if not tk or tk in US_SKIP:
                continue
            # JPM escreve "BRKB"; normaliza para "BRK-B"
            if tk == "BRKB":
                tk = "BRK-B"
            qty = _parse_us_number(row.get("Quantity"))
            px = _parse_us_number(row.get("Price"))
            unit_cost = _parse_us_number(row.get("Unit Cost"))
            value = _parse_us_number(row.get("Value"))
            desc = (row.get("Description") or "").strip()
            positions.append({
                "ticker": tk, "quantity": qty, "price": px,
                "unit_cost": unit_cost or px, "value": value,
                "description": desc[:60],
            })

    print(f"\n=== US: {len(positions)} posições ===")
    mv_total = sum(p["value"] or 0 for p in positions)
    print(f"  MV (JPM): $ {mv_total:,.2f}")

    if dry_run:
        for p in positions:
            q = p.get("quantity") or 0
            px = p.get("price") or 0
            uc = p.get("unit_cost") or 0
            val = p.get("value") or 0
            print(f"  DRY  {p['ticker']:7s} qty={q:<10.4f}  px=${px:<9.2f}  uc=${uc:<9.2f}  val=${val:>10,.2f}  [{p['description']}]")
        return {"positions": positions}

    with sqlite3.connect(DB_US) as conn:
        ensure_schema(conn)

        conn.execute("DELETE FROM portfolio_positions WHERE entry_date = ?", (TODAY,))

        for p in positions:
            if not p["quantity"] or not p["unit_cost"]:
                continue
            _upsert_position(
                conn, p["ticker"], p["quantity"], p["unit_cost"],
                TODAY, notes=f"JPM import {TODAY}"
            )
            conn.execute(
                "UPDATE companies SET is_holding=1 WHERE ticker=?", (p["ticker"],)
            )

        _recompute_weights(conn)
        conn.commit()

        total_mv = conn.execute(
            "SELECT sum(quantity * (select close from prices p where p.ticker=pp.ticker order by date desc limit 1)) "
            "FROM portfolio_positions pp WHERE active=1"
        ).fetchone()[0] or 0
        print(f"  persistido: {len(positions)} posições")
        print(f"  MV calculado (último close DB): $ {total_mv:,.2f}")

    return {"positions": positions}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--br", help="Caminho para o xlsx XP PosiçãoDetalhada")
    ap.add_argument("--us", help="Caminho para o csv JPM positions")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.br and not args.us:
        ap.error("precisa --br e/ou --us")

    if args.br:
        import_br(Path(args.br), dry_run=args.dry_run)
    if args.us:
        import_us(Path(args.us), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
