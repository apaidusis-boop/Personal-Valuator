"""Download de áudio do YouTube via yt-dlp.

Extrai só áudio (bestaudio/m4a). Escreve para directório temporário,
retorna path + metadata. Cleanup é responsabilidade do caller.
"""
from __future__ import annotations

import logging
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yt_dlp

from youtube.models import VideoMetadata

log = logging.getLogger(__name__)


@dataclass
class DownloadResult:
    metadata: VideoMetadata
    audio_path: Path | None  # None se erro
    ok: bool
    error: str | None = None


def _make_opts(tmp_dir: Path) -> dict:
    return {
        "format": "bestaudio/best",
        "outtmpl": str(tmp_dir / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        # Não pós-processar (não precisamos de MP3, Whisper lê m4a/opus directamente).
        "postprocessors": [],
    }


def download(url: str, tmp_dir: Path | None = None) -> DownloadResult:
    """Download áudio. Devolve DownloadResult (ok=False se falhar)."""
    if tmp_dir is None:
        tmp_dir = Path(tempfile.gettempdir()) / "yt_ingest"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(_make_opts(tmp_dir)) as ydl:
            info = ydl.extract_info(url, download=True)
    except yt_dlp.utils.DownloadError as e:
        log.error("download_error url=%s err=%s", url, e)
        return DownloadResult(
            metadata=VideoMetadata(video_id="unknown", url=url),
            audio_path=None,
            ok=False,
            error=str(e),
        )

    video_id = info.get("id") or "unknown"
    ext = info.get("ext") or "m4a"
    audio_path = tmp_dir / f"{video_id}.{ext}"
    if not audio_path.exists():
        # Às vezes yt-dlp muda a extensão silenciosamente. Procurar por glob.
        matches = list(tmp_dir.glob(f"{video_id}.*"))
        if matches:
            audio_path = matches[0]
        else:
            return DownloadResult(
                metadata=VideoMetadata(video_id=video_id, url=url),
                audio_path=None,
                ok=False,
                error=f"audio file not found after download in {tmp_dir}",
            )

    published_at = info.get("upload_date")  # "YYYYMMDD"
    if published_at and len(published_at) == 8:
        published_at = f"{published_at[:4]}-{published_at[4:6]}-{published_at[6:8]}"

    meta = VideoMetadata(
        video_id=video_id,
        url=info.get("webpage_url") or url,
        title=info.get("title"),
        channel=info.get("channel") or info.get("uploader"),
        channel_id=info.get("channel_id"),
        published_at=published_at,
        duration_sec=info.get("duration"),
    )
    return DownloadResult(metadata=meta, audio_path=audio_path, ok=True)
