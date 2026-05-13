"""
Update portfolio from XP XLSX snapshot 2026-05-06.

Changes vs DB state 2026-04-24:
  Equities: VALE3+1, BBDC4+9, ITSA4+13, KLBN11+59, ADD BTLG12
  RF: update valor_atual + spread_taxa on 12 rows, INSERT XP Fundo
"""
import sqlite3
from datetime import datetime

SNAPSHOT_DATE = "2026-05-06"
FETCHED_AT = "2026-05-06T19:24:00Z"

# ── Fixed income updates: (id, new_valor_atual, new_spread_taxa, new_unit_price) ──
# unit_price for bonds = current PU; for Tesouro = position/qty (derived)
RF_UPDATES = [
    # Tesouro Direto
    (13, 43290.11, None,   43290.11 / 232.73),  # NTN-B1 dez/2084
    (14,  9916.33, None,    9916.33 /   5.71),  # NTNB PRINC ago/2040
    (15,   611.28, None,     611.28 /   0.25),  # NTNB PRINC mai/2035
    # Renda Fixa — IPCA+
    (16, 17060.35, 0.0723, 4890.39),  # NTN-B MAI/2045
    (17,  9039.62, 0.1420, 1198.62),  # DEB CSN MINERACAO JUL/2031
    (18, 11531.35, 0.0760, 1189.90),  # CRA KLABIN MAI/2034
    (19, 10137.46, 0.1033, 1151.82),  # CRA MARFRIG AGO/2030
    (20, 10882.78, 0.0769, 1142.74),  # DEB ELETROBRAS SET/2031
    (21,  8756.85, 0.0756, 5141.56),  # NTN-B MAI/2035 (2023-07-05)
    (22,  8756.85, 0.0756, 4419.66),  # NTN-B MAI/2035 (2025-04-29)
    (23,   527.32, 0.4856,  501.17),  # DEB RAIZEN MAR/2029
    # Pós-fixado
    (24, 22647.09, None,  1078.43),   # LCA BTG PACTUAL SET/2026 (cdi_pct stays 0.87)
]

# ── New RF row: XP Fundo Mútuo Privatização Eletrobrás RL ──
XP_FUNDO = {
    "name": "XP Fundo Mútuo Privatização Eletrobrás RL",
    "kind": "fundo",
    "indexador": None,
    "spread_taxa": None,
    "cdi_pct": None,
    "entry_date": None,
    "maturity_date": None,
    "quantity": None,
    "entry_unit_price": None,
    "valor_aplicado": 3726.12,
    "valor_atual": 7814.21,
    "currency": "BRL",
    "source": "XP",
    "fetched_at": FETCHED_AT,
    "notes": "Rentabilidade líquida 95.87% | bruta 109.71% | valor líquido R$7298.17",
}

# ── Equity position updates: (ticker, new_qty, new_entry_price) ──
EQUITY_UPDATES = [
    ("VALE3",  501.0, 61.84),
    ("BBDC4", 1837.0, 16.10),
    ("ITSA4", 2485.0,  7.79),
    ("KLBN11", 1059.0, 18.29),
]

# ── New equity: BTLG12 (corporate event residual from BTLG11) ──
BTLG12_POS = {
    "ticker": "BTLG12",
    "weight": 0.0,
    "entry_date": SNAPSHOT_DATE,
    "entry_price": 0.09,
    "active": 1,
    "quantity": 48.0,
    "notes": "Residual corporativo BTLG11 — XP import 2026-05-06 | essentially zero value R$4.32",
}
BTLG12_CO = {
    "ticker": "BTLG12",
    "name": "BTG Logística 12 (residual)",
    "sector": "Logística",
    "is_holding": 1,
    "currency": "BRL",
}


def run():
    conn = sqlite3.connect("data/br_investments.db")
    cur = conn.cursor()

    print("=== 1. Updating fixed_income_positions ===")
    for row_id, valor_atual, spread_taxa, unit_price in RF_UPDATES:
        cur.execute(
            """UPDATE fixed_income_positions
               SET valor_atual = ?, entry_unit_price = ?,
                   spread_taxa = CASE WHEN ? IS NOT NULL THEN ? ELSE spread_taxa END,
                   fetched_at = ?
               WHERE id = ?""",
            (valor_atual, unit_price, spread_taxa, spread_taxa, FETCHED_AT, row_id),
        )
        print(f"  id={row_id}: valor_atual={valor_atual:.2f}")

    # Insert XP Fundo if not already present
    exists = cur.execute(
        "SELECT id FROM fixed_income_positions WHERE name = ? AND kind = 'fundo'",
        (XP_FUNDO["name"],),
    ).fetchone()
    if exists:
        cur.execute(
            "UPDATE fixed_income_positions SET valor_atual=?, fetched_at=? WHERE id=?",
            (XP_FUNDO["valor_atual"], FETCHED_AT, exists[0]),
        )
        print(f"  XP Fundo: updated (id={exists[0]})")
    else:
        cur.execute(
            """INSERT INTO fixed_income_positions
               (name,kind,indexador,spread_taxa,cdi_pct,entry_date,maturity_date,
                quantity,entry_unit_price,valor_aplicado,valor_atual,currency,source,fetched_at,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                XP_FUNDO["name"], XP_FUNDO["kind"], XP_FUNDO["indexador"],
                XP_FUNDO["spread_taxa"], XP_FUNDO["cdi_pct"], XP_FUNDO["entry_date"],
                XP_FUNDO["maturity_date"], XP_FUNDO["quantity"], XP_FUNDO["entry_unit_price"],
                XP_FUNDO["valor_aplicado"], XP_FUNDO["valor_atual"], XP_FUNDO["currency"],
                XP_FUNDO["source"], XP_FUNDO["fetched_at"], XP_FUNDO["notes"],
            ),
        )
        print("  XP Fundo: inserted")

    print("\n=== 2. Updating equity portfolio_positions ===")
    for ticker, qty, pm in EQUITY_UPDATES:
        cur.execute(
            "UPDATE portfolio_positions SET quantity=?, entry_price=? WHERE ticker=? AND active=1",
            (qty, pm, ticker),
        )
        n = cur.rowcount
        print(f"  {ticker}: qty={qty}, PM={pm} ({n} row updated)")

    print("\n=== 3. Adding BTLG12 ===")
    # companies table
    exists_co = cur.execute(
        "SELECT ticker FROM companies WHERE ticker='BTLG12'"
    ).fetchone()
    if not exists_co:
        cur.execute(
            "INSERT INTO companies (ticker,name,sector,is_holding,currency) VALUES (?,?,?,?,?)",
            (BTLG12_CO["ticker"], BTLG12_CO["name"], BTLG12_CO["sector"],
             BTLG12_CO["is_holding"], BTLG12_CO["currency"]),
        )
        print("  companies: BTLG12 inserted")
    else:
        print("  companies: BTLG12 already present")

    # portfolio_positions
    exists_pp = cur.execute(
        "SELECT ticker FROM portfolio_positions WHERE ticker='BTLG12' AND active=1"
    ).fetchone()
    if not exists_pp:
        cur.execute(
            """INSERT INTO portfolio_positions (ticker,weight,entry_date,entry_price,active,quantity,notes)
               VALUES (?,?,?,?,?,?,?)""",
            (BTLG12_POS["ticker"], BTLG12_POS["weight"], BTLG12_POS["entry_date"],
             BTLG12_POS["entry_price"], BTLG12_POS["active"], BTLG12_POS["quantity"],
             BTLG12_POS["notes"]),
        )
        print("  portfolio_positions: BTLG12 inserted")
    else:
        print("  portfolio_positions: BTLG12 already present")

    conn.commit()
    conn.close()

    print("\n=== Verification ===")
    conn2 = sqlite3.connect("data/br_investments.db")
    print("\nRF totals:")
    rows = conn2.execute(
        "SELECT kind, COUNT(*), SUM(valor_atual) FROM fixed_income_positions GROUP BY kind ORDER BY kind"
    ).fetchall()
    total_rf = 0
    for r in rows:
        print(f"  {r[0]}: {r[1]} posições, R${r[2]:,.2f}")
        total_rf += r[2]
    print(f"  TOTAL RF: R${total_rf:,.2f}")

    print("\nEquity positions (active):")
    rows = conn2.execute(
        "SELECT ticker, quantity, entry_price FROM portfolio_positions WHERE active=1 ORDER BY ticker"
    ).fetchall()
    for r in rows:
        print(f"  {r[0]}: qty={r[1]}, PM=R${r[2]}")
    conn2.close()


if __name__ == "__main__":
    run()
