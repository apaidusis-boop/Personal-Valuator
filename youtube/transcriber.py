"""Transcrição local via faster-whisper.

Modelo default: large-v3-turbo (optimizado para latência, ~8× mais rápido
que large-v3 com qualidade equivalente).

Transcript **nunca é escrito em disco**. Fica em RAM até o extractor terminar.
CUDA-first; fallback automático para CPU se CUDA falhar.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from youtube.models import TranscriptChunk

log = logging.getLogger(__name__)

DEFAULT_MODEL = "large-v3-turbo"


@dataclass
class TranscribeResult:
    chunks: list[TranscriptChunk]
    full_text: str
    lang: str
    duration_sec: float


def transcribe(
    audio_path: Path,
    model_name: str = DEFAULT_MODEL,
    language: str | None = None,
) -> TranscribeResult:
    """Transcreve áudio. Tenta CUDA fp16, cai para CPU int8 se falhar
    (seja no load, seja durante a inferência — ex: cublas DLL em falta)."""
    model, device_used = _load_model(model_name)
    log.info("whisper_load model=%s device=%s", model_name, device_used)

    try:
        return _run_transcribe(model, audio_path, language, device_used)
    except Exception as e:  # noqa: BLE001
        if device_used.startswith("cpu"):
            raise
        log.warning(
            "whisper_cuda_runtime_fail err=%s — falling back to CPU int8", e,
        )
        model, device_used = _load_model(model_name, force_cpu=True)
        return _run_transcribe(model, audio_path, language, device_used)


def _run_transcribe(model, audio_path: Path, language: str | None, device_used: str) -> TranscribeResult:
    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )
    chunks: list[TranscriptChunk] = []
    parts: list[str] = []
    for seg in segments_iter:
        text = seg.text.strip()
        if not text:
            continue
        chunks.append(TranscriptChunk(text=text, ts_start=seg.start, ts_end=seg.end))
        parts.append(text)
    full_text = " ".join(parts)
    log.info(
        "whisper_done device=%s lang=%s duration=%.1fs chunks=%d chars=%d",
        device_used, info.language, info.duration, len(chunks), len(full_text),
    )
    return TranscribeResult(
        chunks=chunks,
        full_text=full_text,
        lang=info.language or "unknown",
        duration_sec=info.duration or 0.0,
    )


def _load_model(model_name: str, force_cpu: bool = False):
    from faster_whisper import WhisperModel

    if force_cpu:
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        return model, "cpu-int8"
    try:
        model = WhisperModel(model_name, device="cuda", compute_type="float16")
        return model, "cuda-fp16"
    except Exception as e:  # noqa: BLE001
        log.warning("cuda_load_failed err=%s — falling back to CPU int8", e)
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        return model, "cpu-int8"
