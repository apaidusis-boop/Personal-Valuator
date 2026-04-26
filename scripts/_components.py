"""_components.py — Helena Linha reusable UI components v1.

Componentes que respeitam o Design System em `obsidian_vault/skills/Design_System.md`.
Importar daqui; nunca duplicar HTML inline nas páginas.

Uso:
    from scripts._components import kpi_tile, status_pill, section_header, agent_attribution

    kpi_tile("Market value", "R$ 248.301", delta="+1.2%", tone="positive")
    status_pill("Pass", tone="positive")
    section_header("Holdings", "BR · US consolidated")
"""
from __future__ import annotations

from typing import Literal, Optional

import streamlit as st

from scripts._theme import COLORS

Tone = Literal["neutral", "positive", "negative", "warning", "accent"]

_TONE_COLOR = {
    "neutral": COLORS["muted"],
    "positive": COLORS["positive"],
    "negative": COLORS["negative"],
    "warning": COLORS["warning"],
    "accent": COLORS["accent"],
}


def kpi_tile(
    label: str,
    value: str,
    delta: Optional[str] = None,
    footnote: Optional[str] = None,
    tone: Tone = "accent",
) -> None:
    """Card métrico com left-accent border.

    Helena Linha v1 — substitui `st.metric` para garantir tipografia tabular,
    cor controlada, e footnote opcional (raro em st.metric).

    Args:
        label: nome curto, será UPPERCASED via CSS.
        value: a métrica em si. Já formatada (R$ ..., +1.2%, etc.).
        delta: variação opcional, em string já formatada ("+1.2%", "-340 bps").
        footnote: linha extra abaixo do delta, em muted (≤8 palavras).
        tone: cor do accent left-border. "accent" é default azul.
    """
    accent = _TONE_COLOR.get(tone, COLORS["accent"])
    delta_color = COLORS["positive"] if (delta and delta.startswith("+")) else (
        COLORS["negative"] if (delta and delta.startswith("-")) else COLORS["muted"]
    )
    delta_html = (
        f'<div style="color:{delta_color};font-size:.78rem;font-family:ui-monospace,monospace;'
        f'font-feature-settings:\'tnum\' 1;margin-top:2px;">{delta}</div>'
        if delta else ""
    )
    footnote_html = (
        f'<div style="color:{COLORS["muted"]};font-size:.72rem;margin-top:6px;'
        f'letter-spacing:.02em;">{footnote}</div>'
        if footnote else ""
    )
    st.markdown(
        f"""
        <div style="
            background:{COLORS['surface']};
            border:1px solid {COLORS['border']};
            border-left:2px solid {accent};
            border-radius:4px;
            padding:14px 18px;
        ">
          <div style="color:{COLORS['muted']};font-size:.7rem;text-transform:uppercase;
                      letter-spacing:.07em;font-weight:600;margin-bottom:4px;">{label}</div>
          <div style="color:{COLORS['text']};font-family:ui-monospace,'SF Mono','Cascadia Mono',monospace;
                      font-feature-settings:'tnum' 1;font-weight:500;font-size:1.45rem;
                      letter-spacing:-0.01em;line-height:1.1;">{value}</div>
          {delta_html}
          {footnote_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_pill(text: str, tone: Tone = "neutral") -> str:
    """Badge inline. Devolve string HTML — usar com `unsafe_allow_html=True` ou em st.markdown.

    Use para indicar estado em tabelas, listas, headers ("✅ Fresh", "⚠️ Stale").
    Mantém-se semanticamente próximo do badge (≤2 palavras).
    """
    color = _TONE_COLOR.get(tone, COLORS["muted"])
    bg = f"{color}1f"  # ~12% alpha via hex8
    return (
        f'<span style="display:inline-block;padding:2px 8px;border-radius:10px;'
        f'background:{bg};color:{color};font-size:.72rem;font-weight:600;'
        f'letter-spacing:.04em;text-transform:uppercase;font-family:ui-monospace,monospace;">'
        f'{text}</span>'
    )


def section_header(title: str, caption: Optional[str] = None) -> None:
    """H2 + caption opcional. Espaçamento consistente entre secções.

    Caption ≤ 8 palavras, factual. Se mais longa, refactor para um parágrafo
    abaixo do header em vez de empacotar em caption.
    """
    cap = (
        f'<div style="color:{COLORS["muted"]};font-size:.82rem;'
        f'margin:-6px 0 14px 0;letter-spacing:.01em;">{caption}</div>'
        if caption else ""
    )
    st.markdown(
        f"""
        <div style="margin:1.6rem 0 0.4rem 0;">
          <div style="color:{COLORS['text']};font-size:1.2rem;font-weight:600;
                      letter-spacing:-0.015em;line-height:1.25;">{title}</div>
          {cap}
        </div>
        """,
        unsafe_allow_html=True,
    )


def agent_attribution(agent: str, tier: str, why: str) -> None:
    """Footer "by {agent} · {tier} · {why}" — transparency moment para acções autónomas.

    Aplicar em toda Actions Queue row, toda notificação Telegram com origem agentic,
    todo memo gerado por perpetuum. Implementa os 3 momentos do Design System:
    Why (why) · What (label da acção) · Who paid (agent + tier).
    """
    st.markdown(
        f'<div style="color:{COLORS["muted"]};font-size:.72rem;'
        f'font-family:ui-monospace,monospace;letter-spacing:.02em;'
        f'padding:6px 0;border-top:1px solid {COLORS["border"]};margin-top:8px;">'
        f'by <span style="color:{COLORS["accent"]};">{agent}</span> · '
        f'<span style="color:{COLORS["text"]};">{tier}</span> · '
        f'{why}'
        f'</div>',
        unsafe_allow_html=True,
    )


_VERDICT_TONE: dict[str, Tone] = {
    "BUY": "positive",
    "ACCUMULATE": "positive",
    "HOLD": "warning",
    "TRIM": "warning",
    "AVOID": "negative",
    "SELL": "negative",
    "EXIT": "negative",
    "REJECT": "negative",
    "UNKNOWN": "neutral",
}


def verdict_pill(verdict: str) -> str:
    """Semantic-coloured pill for BUY/HOLD/AVOID/SELL/etc.

    Returns HTML string. Use with `unsafe_allow_html=True` ou em st.markdown.
    Unknown verdicts fall back to neutral tone.
    """
    v = (verdict or "UNKNOWN").upper().strip()
    tone = _VERDICT_TONE.get(v, "neutral")
    return status_pill(v, tone=tone)


def story_card(
    title: str,
    subtitle: Optional[str] = None,
    body: Optional[list[str]] = None,
    pill_html: Optional[str] = None,
    footer: Optional[str] = None,
    tone: Tone = "accent",
) -> None:
    """Card narrativo — para IC debates, variant views, RI changes, etc.

    Diferente do kpi_tile (que é métrica + delta + footnote),
    story_card carrega prosa curta: 2-4 linhas de body + 1 footer factual.

    Args:
        title: identifier (ticker, perpetuum name, decision label).
        subtitle: contexto secundário em muted (sector, market, date).
        body: lista de linhas curtas (≤90 chars cada). Cada linha vira <li>-style.
        pill_html: badge HTML (de status_pill ou verdict_pill) renderizado no header.
        footer: linha factual final em muted (source, ago, link).
        tone: cor do accent left-border.
    """
    accent = _TONE_COLOR.get(tone, COLORS["accent"])
    sub_html = (
        f'<div style="color:{COLORS["muted"]};font-size:.75rem;letter-spacing:.02em;'
        f'margin-top:2px;">{subtitle}</div>' if subtitle else ""
    )
    body_html = ""
    if body:
        items = "".join(
            f'<li style="margin:4px 0;line-height:1.45;">{line}</li>' for line in body
        )
        body_html = (
            f'<ul style="margin:10px 0 0 0;padding-left:18px;color:{COLORS["text"]};'
            f'font-size:.85rem;list-style:square;">{items}</ul>'
        )
    pill_block = (
        f'<div style="margin-left:auto;">{pill_html}</div>' if pill_html else ""
    )
    footer_html = (
        f'<div style="color:{COLORS["muted"]};font-size:.7rem;'
        f'font-family:ui-monospace,monospace;letter-spacing:.02em;'
        f'margin-top:10px;padding-top:8px;border-top:1px solid {COLORS["border"]};">'
        f'{footer}</div>' if footer else ""
    )
    st.markdown(
        f"""
        <div style="
            background:{COLORS['surface']};
            border:1px solid {COLORS['border']};
            border-left:2px solid {accent};
            border-radius:4px;
            padding:14px 18px;
            margin-bottom:10px;
        ">
          <div style="display:flex;align-items:flex-start;gap:10px;">
            <div style="flex:1;">
              <div style="color:{COLORS['text']};font-weight:600;font-size:.95rem;
                          letter-spacing:-0.01em;">{title}</div>
              {sub_html}
            </div>
            {pill_block}
          </div>
          {body_html}
          {footer_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(
    big_number: str,
    eyebrow: Optional[str] = None,
    delta_text: Optional[str] = None,
    delta_tone: Tone = "neutral",
    caption_chips: Optional[list[str]] = None,
) -> None:
    """Hero number — Apple Newsroom-style landing element.

    Big tabular number (3.2rem), small uppercase eyebrow above, semantic delta
    + neutral caption chips below. Massive top/bottom padding deliberately —
    breathing room is the entire point.

    Args:
        big_number: the headline figure, already formatted (R$ 287,432).
        eyebrow: tiny uppercase label above (date, "PORTFOLIO", "TODAY").
        delta_text: optional change indicator next to chips ("+1.2% 7d").
        delta_tone: semantic colour for the delta_text.
        caption_chips: list of factual stats joined by " · " in muted (≤4 chips).
    """
    eyebrow_html = (
        f'<div style="font-size:.72rem;color:{COLORS["muted"]};text-transform:uppercase;'
        f'letter-spacing:.08em;font-weight:600;margin-bottom:10px;">{eyebrow}</div>'
        if eyebrow else ""
    )
    delta_color = _TONE_COLOR.get(delta_tone, COLORS["muted"])
    chips_parts: list[str] = []
    if delta_text:
        chips_parts.append(f'<span style="color:{delta_color};font-weight:600;">{delta_text}</span>')
    if caption_chips:
        chips_parts.extend(caption_chips)
    chips_html = (
        f'<div style="font-size:.86rem;color:{COLORS["muted"]};margin-top:18px;'
        f'font-family:ui-monospace,\'SF Mono\',monospace;letter-spacing:.02em;'
        f'font-feature-settings:\'tnum\' 1;">'
        f'{"&nbsp;&nbsp;·&nbsp;&nbsp;".join(chips_parts)}</div>'
        if chips_parts else ""
    )
    st.markdown(
        f"""
        <div style="padding:36px 0 28px 0;">
          {eyebrow_html}
          <div style="font-size:3.4rem;font-weight:700;letter-spacing:-.025em;
                      color:{COLORS['text']};line-height:1.05;
                      font-family:ui-monospace,'SF Mono','Cascadia Mono',monospace;
                      font-feature-settings:'tnum' 1;">
            {big_number}
          </div>
          {chips_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def ask_box(
    placeholder: str = "Pergunta qualquer coisa ao cérebro local…",
    caption: Optional[str] = None,
    disabled: bool = True,
    key: str = "ask_box",
) -> Optional[str]:
    """Prominent text input for the Home page Ask experience.

    When disabled=True (default), it's a placeholder for U.3 wiring.
    When disabled=False, returns the user input string for routing into
    `library.rag ask`.
    """
    val = st.text_input(
        "Ask",
        placeholder=f"🔍   {placeholder}",
        key=key,
        label_visibility="collapsed",
        disabled=disabled,
    )
    if caption:
        st.markdown(
            f'<div style="color:{COLORS["muted"]};font-size:.74rem;'
            f'margin-top:-8px;letter-spacing:.02em;">{caption}</div>',
            unsafe_allow_html=True,
        )
    return val if val and not disabled else None


def divider(label: Optional[str] = None) -> None:
    """Separador horizontal com label opcional centrado em cima."""
    if label:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;margin:1.4rem 0;">
              <div style="flex:1;height:1px;background:{COLORS['border']};"></div>
              <div style="padding:0 12px;color:{COLORS['muted']};font-size:.72rem;
                          text-transform:uppercase;letter-spacing:.08em;font-weight:600;">{label}</div>
              <div style="flex:1;height:1px;background:{COLORS['border']};"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<hr style="border:none;border-top:1px solid {COLORS["border"]};margin:1.2rem 0;"/>',
            unsafe_allow_html=True,
        )
