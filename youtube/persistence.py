"""Persistência: videos / video_insights / video_themes em ambas as DBs.

Roteamento de market:
  - Insight: lê `market` de config/aliases.yaml para o ticker → BR ou US DB.
  - Theme: se o vídeo for PT → BR DB; se EN → US DB. Configurável via arg.

Uma linha em `videos` é sempre inserida em AMBAS as DBs (facilita consultas
por ticker local sem joins cross-db), mas `video_insights`/`video_themes`
vão só para a DB correcta.
"""
from __future__ import annotations

import json
import logging
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from youtube.models import Insight, Theme, TranscriptChunk, VideoMetadata
from youtube.validator import normalize_claim

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _upsert_video(
    conn: sqlite3.Connection,
    meta: VideoMetadata,
    lang: str,
    status: str,
    tickers_seen: list[str],
    error_msg: str | None = None,
    transcript_text: str | None = None,
    transcript_chunks_json: str | None = None,
) -> None:
    """Upsert. Se transcript_* é None, preserva o valor existente (COALESCE)."""
    conn.execute(
        """INSERT INTO videos
             (video_id, url, title, channel, channel_id, published_at,
              duration_sec, lang, processed_at, status, error_msg, tickers_seen,
              transcript_text, transcript_chunks_json)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(video_id) DO UPDATE SET
             url=excluded.url, title=excluded.title, channel=excluded.channel,
             channel_id=excluded.channel_id, published_at=excluded.published_at,
             duration_sec=excluded.duration_sec, lang=excluded.lang,
             processed_at=excluded.processed_at, status=excluded.status,
             error_msg=excluded.error_msg, tickers_seen=excluded.tickers_seen,
             transcript_text=COALESCE(excluded.transcript_text, videos.transcript_text),
             transcript_chunks_json=COALESCE(excluded.transcript_chunks_json, videos.transcript_chunks_json)""",
        (
            meta.video_id, meta.url, meta.title, meta.channel, meta.channel_id,
            meta.published_at, meta.duration_sec, lang, _now(), status, error_msg,
            json.dumps(tickers_seen),
            transcript_text, transcript_chunks_json,
        ),
    )


def _insert_insight(
    conn: sqlite3.Connection,
    video_id: str,
    ins: Insight,
) -> bool:
    claim_norm = normalize_claim(ins.claim)
    try:
        conn.execute(
            """INSERT INTO video_insights
                 (video_id, ticker, kind, claim, claim_norm, evidence_quote,
                  ts_seconds, confidence, created_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (video_id, ins.ticker, ins.kind, ins.claim, claim_norm,
             ins.evidence_quote, ins.ts_seconds, ins.confidence, _now()),
        )
        return True
    except sqlite3.IntegrityError:
        # Unique index — já existe
        return False


def _insert_theme(
    conn: sqlite3.Connection,
    video_id: str,
    th: Theme,
) -> bool:
    summary_norm = normalize_claim(th.summary)
    try:
        conn.execute(
            """INSERT INTO video_themes
                 (video_id, theme, stance, summary, summary_norm, evidence_quote,
                  ts_seconds, confidence, created_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (video_id, th.theme, th.stance, th.summary, summary_norm,
             th.evidence_quote, th.ts_seconds, th.confidence, _now()),
        )
        return True
    except sqlite3.IntegrityError:
        return False


def persist(
    meta: VideoMetadata,
    lang: str,
    status: str,
    insights: list[Insight],
    themes: list[Theme],
    aliases: dict,
    error_msg: str | None = None,
    transcript_text: str | None = None,
    transcript_chunks: list[TranscriptChunk] | None = None,
) -> dict:
    """Escreve tudo para as DBs correctas. Devolve stats.

    Se `transcript_text` e `transcript_chunks` são passados, são guardados
    na tabela `videos` para permitir re-extract sem re-transcrever.
    """
    ticker_defs = aliases.get("tickers", {}) or {}

    def market_of(ticker: str) -> str:
        entry = ticker_defs.get(ticker, {})
        return (entry.get("market") or "br").lower()

    # Agrupa insights por market
    br_ins = [i for i in insights if market_of(i.ticker) == "br"]
    us_ins = [i for i in insights if market_of(i.ticker) == "us"]

    # Themes: PT → BR, EN → US; default BR.
    theme_db = DB_BR if (lang or "").lower() != "en" else DB_US

    tickers_seen = sorted({i.ticker for i in insights})

    chunks_json = None
    if transcript_chunks is not None:
        chunks_json = json.dumps(
            [[c.text, c.ts_start, c.ts_end] for c in transcript_chunks],
            ensure_ascii=False,
        )

    stats = {"br_insights": 0, "us_insights": 0, "themes": 0, "themes_db": theme_db.name}

    # BR DB
    with sqlite3.connect(DB_BR) as conn:
        _upsert_video(conn, meta, lang, status, tickers_seen, error_msg,
                      transcript_text=transcript_text,
                      transcript_chunks_json=chunks_json)
        for ins in br_ins:
            if _insert_insight(conn, meta.video_id, ins):
                stats["br_insights"] += 1
        if theme_db == DB_BR:
            for th in themes:
                if _insert_theme(conn, meta.video_id, th):
                    stats["themes"] += 1
        conn.commit()

    # US DB (sempre upsert do video metadata para consultas locais)
    with sqlite3.connect(DB_US) as conn:
        _upsert_video(conn, meta, lang, status, tickers_seen, error_msg,
                      transcript_text=transcript_text,
                      transcript_chunks_json=chunks_json)
        for ins in us_ins:
            if _insert_insight(conn, meta.video_id, ins):
                stats["us_insights"] += 1
        if theme_db == DB_US:
            for th in themes:
                if _insert_theme(conn, meta.video_id, th):
                    stats["themes"] += 1
        conn.commit()

    log.info("persist_done %s", stats)
    return stats


def load_cached_transcript(
    video_id: str,
) -> tuple[VideoMetadata, str, list[TranscriptChunk], str] | None:
    """Lê transcript cached da DB BR (é idêntico na US). Devolve
    (meta, lang, chunks, full_text) ou None se não existir / sem transcript.
    """
    with sqlite3.connect(DB_BR) as conn:
        row = conn.execute(
            """SELECT video_id, url, title, channel, channel_id, published_at,
                      duration_sec, lang, transcript_text, transcript_chunks_json
                 FROM videos WHERE video_id = ?""",
            (video_id,),
        ).fetchone()
    if row is None:
        return None
    transcript_text = row[8]
    chunks_json = row[9]
    if not transcript_text or not chunks_json:
        return None
    meta = VideoMetadata(
        video_id=row[0], url=row[1], title=row[2], channel=row[3],
        channel_id=row[4], published_at=row[5], duration_sec=row[6],
    )
    chunks_raw = json.loads(chunks_json)
    chunks = [TranscriptChunk(text=t, ts_start=s, ts_end=e) for t, s, e in chunks_raw]
    return meta, (row[7] or "unknown"), chunks, transcript_text


def clear_video_facts(video_id: str) -> dict:
    """Apaga video_insights + video_themes dum vídeo em ambas as DBs.
    Usado por yt_reextract para re-correr sem duplicar. Não toca em `videos`.
    """
    stats = {"br_insights_deleted": 0, "us_insights_deleted": 0,
             "br_themes_deleted": 0, "us_themes_deleted": 0}
    for db_path, keyi, keyt in ((DB_BR, "br_insights_deleted", "br_themes_deleted"),
                                (DB_US, "us_insights_deleted", "us_themes_deleted")):
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute("DELETE FROM video_insights WHERE video_id=?", (video_id,))
            stats[keyi] = cur.rowcount
            cur = conn.execute("DELETE FROM video_themes WHERE video_id=?", (video_id,))
            stats[keyt] = cur.rowcount
            conn.commit()
    return stats


def list_cached_video_ids(channel: str | None = None) -> list[str]:
    """Lista video_ids que têm transcript cached."""
    sql = "SELECT video_id FROM videos WHERE transcript_text IS NOT NULL AND transcript_chunks_json IS NOT NULL"
    args: tuple = ()
    if channel:
        sql += " AND channel = ?"
        args = (channel,)
    sql += " ORDER BY published_at DESC, processed_at DESC"
    with sqlite3.connect(DB_BR) as conn:
        return [r[0] for r in conn.execute(sql, args)]
