"""_terminal — Bloomberg-inspired CSS + Plotly template para páginas de varrimento.

Usado em: Home, Portfolio, Triggers, Signals, Screener, Paper Signals,
Perpetuum Health. Densidade alta, mono em todo lado, cor é dado.

Não usado em: Ticker, RI Timeline, IC Debate, Actions detail (modo editorial).

Princípios:
  - Tipografia única: JetBrains Mono / system mono
  - Background near-black, sem gradiente, sem shadow
  - Headers em UPPERCASE 10px com letter-spacing
  - Borders 1px subtle (--bz-border #1a1d23)
  - Cor é semântica: green/red/amber/accent — nunca decoração
  - Tabelas tabular-nums alinhamento à direita para números
  - Zero radius (cornerless) ou radius máximo de 2px
"""
from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


# ─────────── Tokens ───────────

BZ = {
    "bg":          "#0a0c10",
    "bg_alt":      "#0d0f14",
    "surface":     "#10131a",
    "border":      "#1a1d26",
    "border_soft": "#13161d",
    "text":        "#c8ccd1",
    "text_dim":    "#8a8f96",
    "muted":       "#5c6370",
    "green":       "#4ade80",
    "red":         "#f87171",
    "amber":       "#fbbf24",
    "accent":      "#4f8df9",
    "select":      "#1e2a44",  # row selected bg (subtle blue tint)
}


# ─────────── CSS injection ───────────

_TERMINAL_CSS = f"""
<style>
/* ==================== Reset Streamlit chrome ==================== */
.stApp {{ background: {BZ['bg']}; }}
[data-testid="stAppViewContainer"] {{ background: {BZ['bg']}; }}
[data-testid="stHeader"] {{ background: transparent; height:0; }}
[data-testid="stToolbar"] {{ display:none; }}
.main .block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 100%; }}
#MainMenu, footer {{ visibility: hidden; }}

/* ==================== Tipografia: tudo mono ==================== */
html, body, [data-testid="stAppViewContainer"], .main, .block-container,
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li,
.stText, .stCode, .stDataFrame, .stTable, button, input, select, textarea {{
  font-family: 'JetBrains Mono', 'SF Mono', 'Cascadia Mono', ui-monospace, Consolas, monospace !important;
  font-feature-settings: 'tnum' 1, 'zero' 1;
  letter-spacing: 0;
  color: {BZ['text']};
}}
.stMarkdown {{ font-size: 12.5px; line-height: 1.55; }}

/* H1 — section title */
.stMarkdown h1, h1 {{
  font-size: 13px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: {BZ['text']} !important;
  border-bottom: 1px solid {BZ['border']};
  padding-bottom: 6px;
  margin: 18px 0 14px 0 !important;
}}
.stMarkdown h2, h2 {{
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: {BZ['text_dim']} !important;
  margin: 22px 0 10px 0 !important;
  border: none;
}}
.stMarkdown h3, h3 {{
  font-size: 10px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: {BZ['muted']} !important;
  margin: 14px 0 6px 0 !important;
}}

/* ==================== Sidebar ==================== */
[data-testid="stSidebar"] {{
  background: {BZ['bg_alt']} !important;
  border-right: 1px solid {BZ['border']};
}}
[data-testid="stSidebar"] > div:first-child {{ padding-top: 12px; }}
[data-testid="stSidebar"] .stMarkdown {{ font-size: 11.5px; }}
[data-testid="stSidebar"] hr {{ border-color: {BZ['border']}; }}

/* Radio (nav) */
.stRadio label {{ font-size: 11.5px !important; padding: 2px 0; }}
.stRadio [role="radiogroup"] > label {{
  margin: 0 !important;
  padding: 4px 8px !important;
  border-radius: 0;
  border-left: 2px solid transparent;
}}
.stRadio [role="radiogroup"] > label:hover {{
  background: {BZ['surface']};
  border-left-color: {BZ['border']};
}}
.stRadio [role="radiogroup"] > label[data-checked="true"],
.stRadio [role="radiogroup"] > label:has(input:checked) {{
  background: {BZ['surface']};
  border-left-color: {BZ['accent']};
  color: {BZ['accent']};
}}

/* ==================== Buttons ==================== */
.stButton > button {{
  background: transparent;
  border: 1px solid {BZ['border']};
  border-radius: 2px;
  color: {BZ['text']};
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 5px 10px;
  transition: none;
  box-shadow: none;
}}
.stButton > button:hover {{
  border-color: {BZ['accent']};
  color: {BZ['accent']};
  background: transparent;
}}
.stButton > button:focus {{ box-shadow: none !important; outline: none; }}

/* ==================== Inputs ==================== */
input, .stTextInput input, .stMultiSelect div[data-baseweb="select"] > div {{
  background: {BZ['bg']} !important;
  border: 1px solid {BZ['border']} !important;
  border-radius: 2px !important;
  color: {BZ['text']} !important;
  font-size: 11.5px !important;
  font-family: 'JetBrains Mono', monospace !important;
}}
.stMultiSelect [data-baseweb="tag"] {{
  background: {BZ['surface']} !important;
  border: 1px solid {BZ['border']} !important;
  border-radius: 2px !important;
  color: {BZ['accent']} !important;
  font-family: 'JetBrains Mono', monospace !important;
}}

/* ==================== Tables / DataFrames ==================== */
.stDataFrame, [data-testid="stDataFrame"] {{
  border: 1px solid {BZ['border']};
  border-radius: 0;
}}
.stDataFrame [role="columnheader"] {{
  background: {BZ['bg_alt']} !important;
  color: {BZ['text_dim']} !important;
  font-size: 10px !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
  border-bottom: 1px solid {BZ['border']};
}}
.stDataFrame [role="cell"] {{
  font-size: 11.5px !important;
  border-bottom: 1px solid {BZ['border_soft']};
  padding: 4px 8px;
}}
.stDataFrame [role="row"]:hover [role="cell"] {{
  background: {BZ['surface']} !important;
}}

/* ==================== Expander ==================== */
.stExpander {{
  background: transparent;
  border: 1px solid {BZ['border']};
  border-radius: 0;
}}
.stExpander summary {{
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: {BZ['text_dim']};
  padding: 6px 10px !important;
}}

/* ==================== Plotly chart container ==================== */
.js-plotly-plot, .plot-container {{ background: {BZ['bg']} !important; }}

/* ==================== Custom utility classes ==================== */
.bz-row {{
  display: grid;
  font-size: 11.5px;
  padding: 3px 8px;
  border-bottom: 1px solid {BZ['border_soft']};
  align-items: center;
}}
.bz-row:hover {{ background: {BZ['surface']}; }}
.bz-row.is-active {{ background: {BZ['select']}; border-left: 2px solid {BZ['accent']}; padding-left: 6px; }}
.bz-num {{
  text-align: right;
  font-feature-settings: 'tnum' 1;
}}
.bz-pos {{ color: {BZ['green']}; }}
.bz-neg {{ color: {BZ['red']}; }}
.bz-amb {{ color: {BZ['amber']}; }}
.bz-mut {{ color: {BZ['muted']}; }}
.bz-dim {{ color: {BZ['text_dim']}; }}
.bz-acc {{ color: {BZ['accent']}; }}

.bz-eyebrow {{
  font-size: 9.5px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: {BZ['muted']};
  font-weight: 600;
  margin-bottom: 4px;
}}

.bz-stat {{
  display: inline-block;
  margin-right: 18px;
}}
.bz-stat .label {{
  font-size: 9.5px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: {BZ['muted']};
  display: block;
}}
.bz-stat .value {{
  font-size: 14px;
  color: {BZ['text']};
  font-weight: 500;
  font-feature-settings: 'tnum' 1;
}}
.bz-stat.green .value {{ color: {BZ['green']}; }}
.bz-stat.red .value {{ color: {BZ['red']}; }}
.bz-stat.amber .value {{ color: {BZ['amber']}; }}
</style>
"""


def inject_terminal_css() -> None:
    """Apply Bloomberg-inspired CSS. Call once per page."""
    st.markdown(_TERMINAL_CSS, unsafe_allow_html=True)


# ─────────── Plotly template ───────────

_TERMINAL_LAYOUT = go.Layout(
    paper_bgcolor=BZ["bg"],
    plot_bgcolor=BZ["bg"],
    font={"family": "'JetBrains Mono', 'SF Mono', monospace", "color": BZ["text"], "size": 11},
    xaxis={
        "gridcolor": BZ["border_soft"],
        "linecolor": BZ["border"],
        "zerolinecolor": BZ["border"],
        "tickfont": {"size": 10, "color": BZ["text_dim"]},
        "showgrid": True,
        "showline": True,
    },
    yaxis={
        "gridcolor": BZ["border_soft"],
        "linecolor": BZ["border"],
        "zerolinecolor": BZ["border"],
        "tickfont": {"size": 10, "color": BZ["text_dim"]},
        "showgrid": True,
        "showline": True,
        "tickformat": ",.1f",
    },
    legend={
        "bgcolor": "rgba(0,0,0,0)",
        "bordercolor": BZ["border"],
        "borderwidth": 0,
        "font": {"size": 10, "color": BZ["text_dim"]},
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.02,
        "x": 0,
    },
    margin={"l": 50, "r": 20, "t": 30, "b": 30},
    hoverlabel={
        "bgcolor": BZ["bg_alt"],
        "bordercolor": BZ["border"],
        "font": {"family": "'JetBrains Mono', monospace", "size": 11, "color": BZ["text"]},
    },
    colorway=[BZ["accent"], BZ["green"], BZ["amber"], BZ["red"], "#a78bfa", "#22d3ee", "#fb923c"],
)

TERMINAL_TEMPLATE = go.layout.Template(layout=_TERMINAL_LAYOUT)
pio.templates["bz_terminal"] = TERMINAL_TEMPLATE


# ─────────── Helpers ───────────

def stat(label: str, value: str, tone: str = "neutral") -> str:
    """Inline stat block (eyebrow label + value). Returns HTML string."""
    cls = f"bz-stat {tone}" if tone != "neutral" else "bz-stat"
    return (
        f'<div class="{cls}">'
        f'<span class="label">{label}</span>'
        f'<span class="value">{value}</span>'
        f'</div>'
    )


def pct(value: float, decimals: int = 1) -> str:
    """Format percentage with sign + tone class wrapping."""
    if value is None:
        return f'<span class="bz-mut">—</span>'
    cls = "bz-pos" if value >= 0 else "bz-neg"
    return f'<span class="{cls}">{value:+.{decimals}f}%</span>'


def num(value: float | int, decimals: int = 0, prefix: str = "", suffix: str = "") -> str:
    """Tabular number, no tone."""
    if value is None:
        return f'<span class="bz-mut">—</span>'
    fmt = f"{{:,.{decimals}f}}" if decimals > 0 else "{:,.0f}"
    return f'<span class="bz-num">{prefix}{fmt.format(value).replace(",", ".")}{suffix}</span>'


def eyebrow(text: str) -> None:
    """Tiny uppercase label (section eyebrow)."""
    st.markdown(f'<div class="bz-eyebrow">{text}</div>', unsafe_allow_html=True)
