"""_theme.py — Helena Linha design system v1.

Centraliza:
  - Paleta de cores (5 tokens semantic + 5 categóricos)
  - Plotly template (dark, restrained palette)
  - CSS injection helper para Streamlit

Uso:
    from scripts._theme import inject_css, PLOTLY_TEMPLATE, COLORS
    inject_css()  # call once after st.set_page_config
    fig.update_layout(template=PLOTLY_TEMPLATE)
"""
from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ────────────────── tokens ──────────────────

COLORS = {
    "bg": "#0f1115",
    "surface": "#161a22",
    "surface_2": "#1d2330",
    "border": "#222833",
    "text": "#e6e8eb",
    "muted": "#7a8290",
    "accent": "#4f8df9",
    "positive": "#4ade80",
    "negative": "#f87171",
    "warning": "#fbbf24",
    "neutral_chart": "#94a3b8",
}

# 5-color categorical palette (no rainbow). Order matters: most-important first.
CATEGORICAL = [
    "#4f8df9",  # accent blue
    "#4ade80",  # positive green
    "#f87171",  # negative terracotta
    "#fbbf24",  # warning mustard
    "#a78bfa",  # amethyst
]

# ────────────────── plotly template ──────────────────

_layout = go.Layout(
    paper_bgcolor=COLORS["surface"],
    plot_bgcolor=COLORS["surface"],
    font={"family": "system-ui, -apple-system, sans-serif",
          "color": COLORS["text"], "size": 13},
    title={"font": {"color": COLORS["text"], "size": 15, "family": "system-ui"},
           "x": 0.0, "xanchor": "left", "pad": {"l": 0, "t": 4}},
    xaxis={"gridcolor": COLORS["border"], "linecolor": COLORS["border"],
           "tickfont": {"color": COLORS["muted"]}, "title_font": {"color": COLORS["muted"]},
           "zeroline": False},
    yaxis={"gridcolor": COLORS["border"], "linecolor": COLORS["border"],
           "tickfont": {"color": COLORS["muted"]}, "title_font": {"color": COLORS["muted"]},
           "zeroline": False},
    legend={"font": {"color": COLORS["muted"], "size": 11},
            "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
            "orientation": "h", "y": 1.05, "x": 0},
    margin={"l": 8, "r": 8, "t": 36, "b": 8},
    colorway=CATEGORICAL,
    hoverlabel={"bgcolor": COLORS["surface_2"], "bordercolor": COLORS["border"],
                "font": {"color": COLORS["text"], "family": "system-ui"}},
)

PLOTLY_TEMPLATE = go.layout.Template(layout=_layout)
pio.templates["ii_dark"] = PLOTLY_TEMPLATE
pio.templates.default = "ii_dark"

# ────────────────── streamlit css ──────────────────

_CSS = f"""
<style>
:root {{
  --bg: {COLORS['bg']};
  --surface: {COLORS['surface']};
  --surface-2: {COLORS['surface_2']};
  --border: {COLORS['border']};
  --text: {COLORS['text']};
  --muted: {COLORS['muted']};
  --accent: {COLORS['accent']};
  --positive: {COLORS['positive']};
  --negative: {COLORS['negative']};
  --warning: {COLORS['warning']};
}}

html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  color: var(--text);
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}}

[data-testid="stHeader"] {{ background: transparent; height: 0; }}
[data-testid="stToolbar"] {{ display: none; }}

/* Sidebar */
[data-testid="stSidebar"] {{
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {{
  color: var(--text);
  font-weight: 600;
  letter-spacing: -0.01em;
}}

/* Headings */
h1, h2, h3, h4 {{
  color: var(--text);
  font-weight: 600;
  letter-spacing: -0.015em;
  line-height: 1.25;
}}
h1 {{ font-size: 1.6rem; margin: 0 0 0.4rem 0; }}
h2 {{ font-size: 1.2rem; margin: 1.2rem 0 0.4rem 0; }}
h3 {{ font-size: 1.0rem; margin: 0.8rem 0 0.3rem 0; color: var(--muted); font-weight: 500; }}

/* Captions softer */
[data-testid="stCaptionContainer"], .stCaption {{
  color: var(--muted) !important;
  font-size: 0.82rem;
  font-weight: 400;
}}

/* Metric cards — Helena polish 2026-04-25 */
[data-testid="stMetric"] {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 2px solid var(--accent);
  border-radius: 4px;
  padding: 14px 18px;
  transition: border-left-color 0.15s ease;
}}
[data-testid="stMetric"]:hover {{
  border-left-color: var(--positive);
}}
[data-testid="stMetricLabel"] {{
  color: var(--muted) !important;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  font-weight: 600;
  margin-bottom: 4px;
}}
[data-testid="stMetricValue"] {{
  color: var(--text) !important;
  font-family: ui-monospace, "SF Mono", "Cascadia Mono", monospace;
  font-feature-settings: "tnum" 1;  /* tabular numerals */
  font-weight: 500;
  font-size: 1.45rem;
  letter-spacing: -0.01em;
}}
[data-testid="stMetricDelta"] {{
  font-size: 0.78rem;
  font-family: ui-monospace, monospace;
  opacity: 0.85;
}}

/* Containers with border */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: var(--surface);
  border: 1px solid var(--border) !important;
  border-radius: 6px;
}}

/* Buttons — calmer */
.stButton > button {{
  background: var(--surface-2);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 5px;
  font-weight: 500;
  font-size: 0.85rem;
  padding: 0.4rem 0.9rem;
  transition: all 0.12s;
}}
.stButton > button:hover {{
  background: var(--border);
  border-color: var(--accent);
  color: var(--text);
}}
.stButton > button[kind="primary"] {{
  background: var(--accent);
  border-color: var(--accent);
  color: white;
}}
.stButton > button[kind="primary"]:hover {{
  background: #6ba2ff;
  border-color: #6ba2ff;
}}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div, .stNumberInput input {{
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 5px !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 1px var(--accent) !important;
}}

/* Dataframes — Helena polish: tabular numerals, header weight */
[data-testid="stDataFrame"] {{
  border: 1px solid var(--border);
  border-radius: 4px;
}}
[data-testid="stDataFrame"] [data-testid="stStyledFullScreenButton"] {{ display: none; }}
[data-testid="stDataFrame"] table {{
  font-family: ui-monospace, "SF Mono", "Cascadia Mono", monospace;
  font-feature-settings: "tnum" 1;
  font-size: 0.84rem;
}}
[data-testid="stDataFrame"] thead th {{
  background: var(--surface-2) !important;
  color: var(--muted) !important;
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.05em;
  font-weight: 600;
  border-bottom: 1px solid var(--border);
}}
[data-testid="stDataFrame"] tbody tr:hover {{
  background: var(--surface-2) !important;
}}

/* Dividers softer */
hr {{
  border-color: var(--border) !important;
  margin: 1.2rem 0 !important;
}}

/* Radio (sidebar nav) */
[data-testid="stSidebar"] .stRadio label {{
  color: var(--muted);
  font-weight: 500;
  font-size: 0.88rem;
  padding: 0.3rem 0;
}}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label {{
  color: var(--accent);
}}

/* Reduce top padding of main area */
.block-container {{ padding-top: 1.6rem !important; padding-bottom: 2rem !important; max-width: 1280px; }}

/* Tabs cleaner */
.stTabs [data-baseweb="tab-list"] {{
  border-bottom: 1px solid var(--border);
  gap: 0;
}}
.stTabs [data-baseweb="tab"] {{
  background: transparent;
  color: var(--muted);
  border: none;
  padding: 0.5rem 1rem;
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
  color: var(--text);
  border-bottom: 2px solid var(--accent);
}}

/* Expander */
.streamlit-expanderHeader {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 5px;
}}
</style>
"""


def inject_css() -> None:
    """Inject design system CSS. Call once after st.set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)


def brand_sidebar() -> None:
    """Render the canonical brand block in the sidebar."""
    st.markdown(
        f"""
        <div style="padding: 4px 0 18px 0; border-bottom: 1px solid {COLORS['border']}; margin-bottom: 16px;">
          <div style="font-size: 1.05rem; font-weight: 600; color: {COLORS['text']}; letter-spacing: -0.01em;">
            Investment Intelligence
          </div>
          <div style="font-size: 0.72rem; color: {COLORS['muted']}; letter-spacing: 0.04em; text-transform: uppercase; margin-top: 2px;">
            BR · US · DRIP
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_caption(text: str) -> None:
    """Tiny caption used below page titles. Keep ≤8 words."""
    st.markdown(
        f"<div style='color: {COLORS['muted']}; font-size: 0.82rem; margin: -10px 0 18px 0;'>{text}</div>",
        unsafe_allow_html=True,
    )
