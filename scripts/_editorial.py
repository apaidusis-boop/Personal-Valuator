"""_editorial — Design System v2.0 (Kenya Hara / MUJI / Banca Privada).

Substitui _terminal.py (deprecated). Filosofia: NÃO É DASHBOARD, É UM DOCUMENTO.

Paleta cream warm + Source Serif 4 + Inter + IBM Plex Mono.
Voz PT-BR completa.

Uso:
    from scripts._editorial import inject_editorial_css, ED, EDITORIAL_TEMPLATE
    from scripts._editorial import lede, eyebrow, hl, deck, section_h, quiet_stat
    inject_editorial_css()
    fig.update_layout(template=EDITORIAL_TEMPLATE)
"""
from __future__ import annotations

from typing import Literal, Optional

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


# ─────────── Tokens ───────────

ED = {
    "paper":     "#f4eee5",
    "paper_2":   "#ede5d8",
    "ink":       "#2a2622",
    "ink_2":     "#4a423a",
    "muted":     "#786f64",
    "muted_2":   "#a89b88",
    "rule":      "#d8d0c4",
    "rule_soft": "#e7e0d2",
    "clay":      "#b85c38",
    "pos":       "#527a45",
    "neg":       "#a0473d",
    "warn":      "#a8763d",
}

Tone = Literal["neutral", "pos", "neg", "warn", "clay"]


# ─────────── CSS injection ───────────

_EDITORIAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ==================== Reset Streamlit chrome — !important to win over _theme.py dark ==================== */
.stApp,
[data-testid="stAppViewContainer"],
html, body {{
  background: {ED['paper']} !important;
  color: {ED['ink']} !important;
}}
[data-testid="stMain"] {{ background: {ED['paper']} !important; }}
.main {{ background: {ED['paper']} !important; }}
[data-testid="stHeader"] {{ background: transparent !important; height: 0; }}
[data-testid="stToolbar"] {{ display: none; }}
.main .block-container {{
  padding-top: 36px !important;
  padding-bottom: 96px !important;
  padding-left: 56px !important;
  padding-right: 80px !important;
  max-width: 1200px;
  background: {ED['paper']} !important;
}}
#MainMenu, footer {{ visibility: hidden; }}

/* ==================== Tipografia ==================== */
html, body, [data-testid="stAppViewContainer"], .main, .block-container,
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li, .stText {{
  font-family: 'Source Serif 4', Georgia, serif !important;
  color: {ED['ink']};
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  font-feature-settings: 'tnum' 1;
}}

/* H1 — page-level title (italic serif 46px) */
.stMarkdown h1, h1 {{
  font-family: 'Source Serif 4', serif !important;
  font-style: italic;
  font-size: 46px !important;
  font-weight: 700 !important;
  letter-spacing: -0.025em;
  line-height: 1.05;
  color: {ED['ink']} !important;
  margin: 12px 0 12px 0 !important;
  font-variation-settings: "opsz" 60;
  border: none;
}}

/* H2 — section title (italic serif 22px) */
.stMarkdown h2, h2 {{
  font-family: 'Source Serif 4', serif !important;
  font-style: italic;
  font-size: 22px !important;
  font-weight: 400 !important;
  letter-spacing: -0.01em;
  color: {ED['ink']} !important;
  margin: 56px 0 4px 0 !important;
  border: none;
}}

/* H3 — sub-section (Inter sans 9.5 tracked) */
.stMarkdown h3, h3 {{
  font-family: 'Inter', sans-serif !important;
  font-size: 10.5px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.22em;
  color: {ED['muted']} !important;
  margin: 20px 0 12px 0 !important;
}}

/* ==================== Sidebar ==================== */
[data-testid="stSidebar"] {{
  background: {ED['paper']} !important;
  border-right: 1px solid {ED['rule']};
}}
[data-testid="stSidebar"] > div:first-child {{ padding: 32px 24px 24px 32px; }}
[data-testid="stSidebar"] .stMarkdown {{ font-size: 14px; }}

/* Radio (nav) — serif italic on active */
[data-testid="stSidebar"] .stRadio label {{
  font-family: 'Source Serif 4', serif !important;
  font-size: 16px !important;
  padding: 4px 0 !important;
  color: {ED['ink_2']} !important;
}}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label {{
  margin: 0 !important;
  padding: 4px 0 !important;
  border: none;
}}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {{
  color: {ED['clay']};
}}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:has(input:checked) {{
  color: {ED['clay']} !important;
  font-style: italic;
}}
/* hide radio circles for cleaner look */
[data-testid="stSidebar"] .stRadio [role="radio"] {{ display: none !important; }}

/* ==================== Buttons (carteira list) ==================== */
[data-testid="stSidebar"] .stButton > button {{
  background: transparent !important;
  border: none !important;
  border-bottom: 1px solid {ED['rule_soft']} !important;
  border-radius: 0 !important;
  color: {ED['ink']} !important;
  font-family: 'Source Serif 4', serif !important;
  font-size: 14.5px !important;
  font-weight: 400 !important;
  text-align: left !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  padding: 11px 0 !important;
  width: 100%;
  justify-content: flex-start !important;
  box-shadow: none !important;
  line-height: 1.35 !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
  color: {ED['clay']} !important;
  background: transparent !important;
  border-color: {ED['rule_soft']} !important;
}}
[data-testid="stSidebar"] .stButton > button:focus {{ box-shadow: none !important; outline: none; }}

/* Main area buttons (CTA-style) — different from sidebar */
.main .stButton > button {{
  background: transparent;
  border: 1px solid {ED['ink']};
  border-radius: 0;
  color: {ED['ink']};
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  padding: 8px 18px;
  box-shadow: none;
}}
.main .stButton > button:hover {{
  background: {ED['ink']};
  color: {ED['paper']};
}}

/* ==================== Inputs ==================== */
input, .stTextInput input {{
  background: {ED['paper']} !important;
  border: none !important;
  border-bottom: 1px solid {ED['ink']} !important;
  border-radius: 0 !important;
  color: {ED['ink']} !important;
  font-family: 'Source Serif 4', serif !important;
  font-size: 15px !important;
  padding: 4px 0 !important;
}}
.stMultiSelect div[data-baseweb="select"] > div {{
  background: {ED['paper']} !important;
  border: none !important;
  border-bottom: 1px solid {ED['rule']} !important;
  border-radius: 0 !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 12.5px !important;
}}
.stMultiSelect [data-baseweb="tag"] {{
  background: {ED['paper_2']} !important;
  border: 1px solid {ED['rule']} !important;
  border-radius: 0 !important;
  color: {ED['ink']} !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 11px !important;
}}
.stSelectbox div[data-baseweb="select"] > div {{
  background: {ED['paper']} !important;
  border: none !important;
  border-bottom: 1px solid {ED['rule']} !important;
  border-radius: 0 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 12.5px !important;
}}

/* ==================== Tables ==================== */
.stDataFrame, [data-testid="stDataFrame"] {{
  border: none;
  border-top: 1px solid {ED['ink']};
  border-radius: 0;
  background: {ED['paper']};
}}
.stDataFrame [role="columnheader"] {{
  background: {ED['paper']} !important;
  color: {ED['muted']} !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 9.5px !important;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-weight: 600 !important;
  border-bottom: 1px solid {ED['ink']} !important;
}}
.stDataFrame [role="cell"] {{
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 13px !important;
  border-bottom: 1px solid {ED['rule_soft']} !important;
  background: {ED['paper']} !important;
  color: {ED['ink_2']} !important;
}}

/* ==================== Plotly chart container ==================== */
.js-plotly-plot, .plot-container {{ background: {ED['paper']} !important; }}

/* ==================== Custom utility classes ==================== */
.ed-lede {{
  font-family: 'Source Serif 4', serif;
  font-size: 18px;
  line-height: 1.55;
  color: {ED['ink_2']};
  margin: 8px 0 32px 0;
  max-width: 720px;
  font-variation-settings: "opsz" 30;
}}
.ed-lede strong {{
  font-weight: 600;
  color: {ED['ink']};
  font-family: 'IBM Plex Mono', monospace;
  font-size: 17px;
  font-feature-settings: 'tnum' 1;
}}
.ed-lede .pos {{ color: {ED['pos']}; font-weight: 500; }}
.ed-lede .neg {{ color: {ED['neg']}; font-weight: 500; }}

.ed-stats {{
  display: grid;
  grid-template-columns: repeat(4, max-content);
  column-gap: 48px;
  row-gap: 12px;
  padding: 18px 0;
  border-top: 1px solid {ED['rule']};
  border-bottom: 1px solid {ED['rule']};
  margin-bottom: 56px;
}}
.ed-stat-l {{
  font-family: 'Inter', sans-serif;
  font-size: 9.5px;
  color: {ED['muted']};
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-weight: 600;
  margin-bottom: 4px;
}}
.ed-stat-v {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 14px;
  color: {ED['ink']};
  font-weight: 500;
  font-feature-settings: 'tnum' 1;
}}
.ed-stat-v.pos {{ color: {ED['pos']}; }}
.ed-stat-v.neg {{ color: {ED['neg']}; }}
.ed-stat-v.warn {{ color: {ED['warn']}; }}

.ed-eyebrow {{
  font-family: 'Inter', sans-serif;
  font-size: 10.5px;
  color: {ED['muted']};
  text-transform: uppercase;
  letter-spacing: 0.22em;
  font-weight: 600;
  margin: 0 0 12px 0;
}}

.ed-deck {{
  font-family: 'Source Serif 4', serif;
  font-size: 17px;
  color: {ED['ink_2']};
  line-height: 1.55;
  margin: 0 0 36px 0;
  max-width: 60ch;
}}
.ed-deck em {{ color: {ED['clay']}; font-style: italic; }}

.ed-section-deck {{
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  color: {ED['muted']};
  margin: 0 0 22px 0;
  max-width: 60ch;
  line-height: 1.55;
}}

.ed-cart-meta {{
  font-family: 'Inter', sans-serif;
  font-size: 10.5px;
  color: {ED['muted']};
  margin-top: -6px;
  margin-bottom: 6px;
  letter-spacing: 0.04em;
  padding-bottom: 4px;
  border-bottom: 1px solid {ED['rule_soft']};
}}

.ed-footer {{
  margin-top: 56px;
  padding-top: 18px;
  border-top: 1px solid {ED['rule']};
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  color: {ED['muted']};
  line-height: 1.7;
}}
.ed-brand {{
  font-family: 'Source Serif 4', serif;
  font-style: italic;
  font-weight: 400;
  font-size: 22px;
  color: {ED['ink']};
  letter-spacing: -0.02em;
  margin-bottom: 4px;
  line-height: 1.15;
}}
.ed-brand-tag {{
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  color: {ED['muted']};
  text-transform: uppercase;
  letter-spacing: 0.18em;
  margin-bottom: 32px;
}}
.ed-nav-h {{
  font-family: 'Inter', sans-serif;
  font-size: 9.5px;
  color: {ED['muted']};
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-weight: 600;
  margin: 28px 0 8px 0;
}}

/* Composition table (HTML rendered) */
.ed-table {{
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
}}
.ed-table th {{
  font-family: 'Inter', sans-serif;
  font-size: 9.5px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-weight: 600;
  color: {ED['muted']};
  text-align: right;
  padding: 12px 18px 14px 0;
  border-bottom: 1px solid {ED['ink']};
}}
.ed-table th:first-child {{ text-align: left; padding-left: 0; }}
.ed-table td {{
  padding: 14px 18px 14px 0;
  text-align: right;
  border-bottom: 1px solid {ED['rule_soft']};
  font-family: 'IBM Plex Mono', monospace;
  font-size: 13px;
  color: {ED['ink_2']};
}}
.ed-table td:first-child {{
  text-align: left;
  padding-left: 0;
  font-family: 'Source Serif 4', serif;
  font-size: 15px;
  color: {ED['ink']};
  font-weight: 500;
}}
.ed-table tr:hover td {{ color: {ED['ink']}; background: {ED['paper_2']}; }}
.ed-pos {{ color: {ED['pos']}; }}
.ed-neg {{ color: {ED['neg']}; }}
.ed-dim {{ color: {ED['muted']}; }}

/* Expander (More) */
.stExpander {{
  background: transparent;
  border: none;
  border-top: 1px solid {ED['rule_soft']};
  border-radius: 0;
}}
.stExpander summary {{
  font-family: 'Inter', sans-serif !important;
  font-size: 10.5px !important;
  text-transform: uppercase;
  letter-spacing: 0.22em;
  color: {ED['muted']} !important;
  font-weight: 600 !important;
  padding: 10px 0 !important;
}}
</style>
"""


def inject_editorial_css() -> None:
    """Apply Hara/MUJI editorial CSS. Call once per page."""
    st.markdown(_EDITORIAL_CSS, unsafe_allow_html=True)


# ─────────── Plotly template ───────────

_EDITORIAL_LAYOUT = go.Layout(
    paper_bgcolor=ED["paper"],
    plot_bgcolor=ED["paper"],
    font={"family": "'Source Serif 4', Georgia, serif",
          "color": ED["ink"], "size": 12},
    xaxis={
        "gridcolor": "rgba(0,0,0,0)",
        "linecolor": "rgba(0,0,0,0)",
        "zeroline": False,
        "tickfont": {"family": "'Source Serif 4', serif",
                     "size": 11, "color": ED["muted"]},
        "showgrid": False,
        "showline": False,
        "ticks": "",
    },
    yaxis={
        "gridcolor": ED["rule_soft"],
        "linecolor": "rgba(0,0,0,0)",
        "zeroline": True,
        "zerolinecolor": ED["rule"],
        "zerolinewidth": 0.6,
        "tickfont": {"family": "'Source Serif 4', serif",
                     "size": 11, "color": ED["muted"], "style": "italic"},
        "showgrid": False,
        "showline": False,
        "ticks": "",
        "tickformat": ",.0f",
    },
    legend={
        "bgcolor": "rgba(0,0,0,0)",
        "bordercolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
        "font": {"family": "'Source Serif 4', serif",
                 "size": 11, "color": ED["muted"]},
        "orientation": "h",
        "yanchor": "bottom",
        "y": -0.18,
        "x": 0,
    },
    margin={"l": 12, "r": 80, "t": 12, "b": 36},
    hoverlabel={
        "bgcolor": ED["paper_2"],
        "bordercolor": ED["rule"],
        "font": {"family": "'IBM Plex Mono', monospace",
                 "size": 12, "color": ED["ink"]},
    },
    hovermode="x unified",
    showlegend=False,
)

EDITORIAL_TEMPLATE = go.layout.Template(layout=_EDITORIAL_LAYOUT)
pio.templates["ii_editorial"] = EDITORIAL_TEMPLATE
# Override the default Plotly template to editorial — kicks any leftover ii_dark
pio.templates.default = "ii_editorial"


# ─────────── Component helpers ───────────

def lede(text_html: str) -> None:
    """Editorial opening sentence. text_html may include <strong> and .pos/.neg spans."""
    st.markdown(f'<div class="ed-lede">{text_html}</div>', unsafe_allow_html=True)


def quiet_stats(stats: list[tuple[str, str, str]]) -> None:
    """Quiet stat grid (NOT a hero bar). Each stat = (label, value, tone).
    tone in {"neutral", "pos", "neg", "warn"}.
    """
    cells = []
    for label, value, tone in stats:
        cls = f"ed-stat-v {tone}" if tone != "neutral" else "ed-stat-v"
        cells.append(
            f'<div><div class="ed-stat-l">{label}</div>'
            f'<div class="{cls}">{value}</div></div>'
        )
    st.markdown(f'<div class="ed-stats">{"".join(cells)}</div>', unsafe_allow_html=True)


def eyebrow(text: str) -> None:
    """Tiny uppercase tracked label above headlines."""
    st.markdown(f'<div class="ed-eyebrow">{text}</div>', unsafe_allow_html=True)


def deck(html: str) -> None:
    """Sub-headline serif body. May include <em> for italic clay accent."""
    st.markdown(f'<div class="ed-deck">{html}</div>', unsafe_allow_html=True)


def section_h(title: str, deck_text: Optional[str] = None) -> None:
    """Section header — H2 italic serif + optional sans deck."""
    st.markdown(f"## {title}", unsafe_allow_html=False)
    if deck_text:
        st.markdown(f'<div class="ed-section-deck">{deck_text}</div>', unsafe_allow_html=True)


def brand_block() -> None:
    """Sidebar brand block."""
    st.markdown(
        f'<div class="ed-brand"><i>Investment</i><br>Intelligence</div>'
        f'<div class="ed-brand-tag">Carteira pessoal · BR · EUA</div>',
        unsafe_allow_html=True,
    )


def nav_section(title: str) -> None:
    """Sidebar nav section header."""
    st.markdown(f'<div class="ed-nav-h">{title}</div>', unsafe_allow_html=True)


def cart_meta(meta_text: str) -> None:
    """Small metadata under a carteira button."""
    st.markdown(f'<div class="ed-cart-meta">{meta_text}</div>', unsafe_allow_html=True)


def footer(html: str) -> None:
    """Sidebar footer."""
    st.markdown(f'<div class="ed-footer">{html}</div>', unsafe_allow_html=True)
