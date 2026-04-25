---
type: design_audit
updated: 2026-04-25
owner: helena_linha
tags: [design, audit, helena, mega]
---

# 01 — Design audit

> Helena Mega · run **2026-04-25** · 67 ficheiros · **12** violações (0 errors / 12 warns / 0 info)

## Resumo executivo

Distribuição por regra:

| Regra | Severidade | Descrição | Hits |
|---|---|---|---:|
| `DS001` | error 🟢 | Rainbow/sequential cmap em styler | 0 |
| `DS002` | error 🟢 | st.metric() cru | 0 |
| `DS003` | error 🟢 | Emoji-prefix em heading | 0 |
| `DS004` | error 🟢 | px.pie() banido (anti-padrão #6 ornamental) | 0 |
| `DS005` | warn 🟡 | Plotly template cru (plotly_white/plotly_dark) | 5 |
| `DS006` | warn 🟡 | Hex literal fora dos 5 tokens | 5 |
| `DS007` | warn 🟢 | Cor por nome (black/red/blue/…) | 0 |
| `DS008` | warn 🟡 | Caption >8 palavras | 2 |
| `DS009` | info ⚪ | Página sem inject_css() | 0 |

Top 10 ficheiros com mais violações:

| Ficheiro | Violações | Linhas |
|---|---:|---:|
| `scripts/us_portfolio_report.py` | 5 | 375 |
| `scripts/compare_ibov.py` | 4 | 187 |
| `scripts/dashboard_app.py` | 2 | 1055 |
| `scripts/compare_ticker_vs_macro.py` | 1 | 76 |

## Detalhe por regra

### `DS005` — Plotly template cru (plotly_white/plotly_dark)  _(warn, 5 hits)_

**Fix sugerido**: Não passar template= ou usar template='ii_dark' explicitamente.

| Ficheiro | Linha | Trecho |
|---|---:|---|
| `scripts/compare_ibov.py` | 102 | `template="plotly_white",` |
| `scripts/compare_ticker_vs_macro.py` | 67 | `hovermode="x unified", template="plotly_white",` |
| `scripts/us_portfolio_report.py` | 146 | `pie.update_layout(title="Alocação por Sector", template="plotly_white", height=400)` |
| `scripts/us_portfolio_report.py` | 154 | `bar_mv.update_layout(title="Market Value por Posição", template="plotly_white",` |
| `scripts/us_portfolio_report.py` | 163 | `bar_pnl.update_layout(title="P&L Não Realizado (USD)", template="plotly_white",` |

### `DS006` — Hex literal fora dos 5 tokens  _(warn, 5 hits)_

**Fix sugerido**: Usar COLORS['accent'|'positive'|'negative'|'warning'|'amethyst'].

| Ficheiro | Linha | Trecho |
|---|---:|---|
| `scripts/compare_ibov.py` | 88 | `line=dict(color="#10b981", width=2.5),  ← #10b981` |
| `scripts/compare_ibov.py` | 93 | `line=dict(color="#64748b", width=2, dash="dot"),  ← #64748b` |
| `scripts/compare_ibov.py` | 96 | `fig.add_hline(y=100, line=dict(color="#94a3b8", width=1),  ← #94a3b8` |
| `scripts/us_portfolio_report.py` | 152 | `marker_color="#2E86AB",  ← #2E86AB` |
| `scripts/us_portfolio_report.py` | 158 | `colors = ["#28a745" if v >= 0 else "#dc3545" for v in port["pnl"]]  ← #28a745` |

### `DS008` — Caption >8 palavras  _(warn, 2 hits)_

**Fix sugerido**: Captions ≤8 palavras factuais. Cortar adjectivos.

| Ficheiro | Linha | Trecho |
|---|---:|---|
| `scripts/dashboard_app.py` | 524 | `section_caption("RAG local · Damodaran + Dalio · Qwen 14B")` |
| `scripts/dashboard_app.py` | 787 | `section_caption("Quarterly history · CVM oficial · 5 stocks BR")` |

## Cobertura de design system por ficheiro

| Ficheiro | inject_css? | kpi_tile import? | Streamlit page? | LoC |
|---|---|---|---|---:|
| `scripts/dashboard_app.py` | ✅ | ✅ | ✅ | 1055 |

## Cross-links

- [[Design_System]] — fonte das regras
- [[../scripts/_theme.py]] — tokens canónicos
- [[../scripts/_components.py]] — helpers `kpi_tile`, `status_pill`, …
- [[Helena Linha]] — owner
