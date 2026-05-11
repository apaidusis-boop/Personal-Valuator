"""Apaga ficheiros temporários (áudio) depois da ingestão.

Nunca escrevemos transcripts em disco; logo o cleanup só trata do áudio.
"""
from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def remove_audio(audio_path: Path | None) -> None:
    if audio_path is None:
        return
    try:
        if audio_path.exists():
            audio_path.unlink()
            log.info("cleanup_removed path=%s", audio_path)
    except OSError as e:
        log.warning("cleanup_fail path=%s err=%s", audio_path, e)
