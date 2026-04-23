"""Router: filtra transcript por aliases (tickers + temas).

Input:  TranscriptChunks + aliases.yaml
Output: dict {ticker: [text_window]} + dict {theme: [text_window]}

Each window expands ±DEFAULT_WINDOW_SEC à volta do chunk que teve match,
para dar contexto ao extractor LLM.

Short-circuit: se não houver qualquer match, caller marca o vídeo como
`skipped_no_relevance` e não invoca o extractor.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from youtube.models import TranscriptChunk

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
ALIASES_PATH = ROOT / "config" / "aliases.yaml"

DEFAULT_WINDOW_SEC = 90.0


@dataclass
class RouterWindow:
    """Janela de contexto para o extractor."""

    text: str
    ts_start: float
    ts_end: float
    matched_terms: list[str] = field(default_factory=list)


@dataclass
class RouterOutput:
    ticker_windows: dict[str, list[RouterWindow]]
    theme_windows: dict[str, list[RouterWindow]]
    tickers_matched: list[str]
    themes_matched: list[str]

    @property
    def has_matches(self) -> bool:
        return bool(self.tickers_matched) or bool(self.themes_matched)


def load_aliases(path: Path | None = None) -> dict:
    p = path or ALIASES_PATH
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_pattern(terms: list[str]) -> re.Pattern | None:
    """Compila regex \\b(term1|term2|...)\\b case-insensitive."""
    cleaned = [re.escape(t) for t in terms if t and t.strip()]
    if not cleaned:
        return None
    return re.compile(r"\b(" + "|".join(cleaned) + r")\b", re.IGNORECASE)


def _collect_terms_ticker(entry: dict) -> list[str]:
    terms: list[str] = []
    terms.extend(entry.get("names", []) or [])
    terms.extend(entry.get("products", []) or [])
    terms.extend(entry.get("people", []) or [])
    return [t for t in terms if t]


def _window_around(
    chunks: list[TranscriptChunk],
    idx: int,
    window_sec: float,
) -> tuple[int, int]:
    target_start = chunks[idx].ts_start - window_sec
    target_end = chunks[idx].ts_end + window_sec
    lo = idx
    while lo > 0 and chunks[lo - 1].ts_end >= target_start:
        lo -= 1
    hi = idx
    while hi < len(chunks) - 1 and chunks[hi + 1].ts_start <= target_end:
        hi += 1
    return lo, hi


def _merge_windows(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []
    ranges = sorted(ranges)
    merged = [ranges[0]]
    for lo, hi in ranges[1:]:
        last_lo, last_hi = merged[-1]
        if lo <= last_hi + 1:
            merged[-1] = (last_lo, max(last_hi, hi))
        else:
            merged.append((lo, hi))
    return merged


def _window_text(chunks: list[TranscriptChunk], lo: int, hi: int) -> RouterWindow:
    segs = chunks[lo : hi + 1]
    return RouterWindow(
        text=" ".join(c.text for c in segs),
        ts_start=segs[0].ts_start,
        ts_end=segs[-1].ts_end,
    )


def route(
    chunks: list[TranscriptChunk],
    aliases: dict,
    window_sec: float = DEFAULT_WINDOW_SEC,
) -> RouterOutput:
    ticker_windows: dict[str, list[RouterWindow]] = {}
    theme_windows: dict[str, list[RouterWindow]] = {}

    ticker_defs = aliases.get("tickers", {}) or {}
    theme_defs = aliases.get("themes", {}) or {}

    # ---------- Tickers ----------
    for ticker, entry in ticker_defs.items():
        terms = _collect_terms_ticker(entry)
        pat = _build_pattern(terms)
        if pat is None:
            continue
        match_ranges: list[tuple[int, int]] = []
        matched_terms: list[str] = []
        for i, ch in enumerate(chunks):
            found = pat.findall(ch.text)
            if found:
                matched_terms.extend(found)
                lo, hi = _window_around(chunks, i, window_sec)
                match_ranges.append((lo, hi))
        if not match_ranges:
            continue
        merged = _merge_windows(match_ranges)
        windows = [_window_text(chunks, lo, hi) for lo, hi in merged]
        for w in windows:
            w.matched_terms = sorted(set(t.lower() for t in matched_terms))
        ticker_windows[ticker] = windows

    # ---------- Themes ----------
    for theme, entry in theme_defs.items():
        terms = entry.get("keywords", []) or []
        pat = _build_pattern(terms)
        if pat is None:
            continue
        match_ranges = []
        matched_terms = []
        for i, ch in enumerate(chunks):
            found = pat.findall(ch.text)
            if found:
                matched_terms.extend(found)
                lo, hi = _window_around(chunks, i, window_sec)
                match_ranges.append((lo, hi))
        if not match_ranges:
            continue
        merged = _merge_windows(match_ranges)
        windows = [_window_text(chunks, lo, hi) for lo, hi in merged]
        for w in windows:
            w.matched_terms = sorted(set(t.lower() for t in matched_terms))
        theme_windows[theme] = windows

    out = RouterOutput(
        ticker_windows=ticker_windows,
        theme_windows=theme_windows,
        tickers_matched=sorted(ticker_windows.keys()),
        themes_matched=sorted(theme_windows.keys()),
    )
    log.info(
        "router_done tickers=%d themes=%d",
        len(out.tickers_matched), len(out.themes_matched),
    )
    return out
