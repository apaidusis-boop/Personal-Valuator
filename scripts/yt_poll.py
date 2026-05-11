"""yt_poll — periodic poller para canais em config/youtube_sources.yaml.

Cada poll:
  1. Lê channel.uploads playlist via YouTube API (1 unit/canal).
  2. Lista vídeos publicados desde last_seen_at do canal.
  3. Filtra: shorts/lives via metadata + min_duration_sec via duration check.
  4. Dedup contra `videos` table (BR + US DBs).
  5. Dispara yt_ingest_batch.py com os IDs novos.

State per-channel em data/yt_poll_state.json:
  {
    "channel_id": {"last_seen_at": "ISO_TS", "video_ids_seen": [...]},
    ...
  }

Uso:
    python scripts/yt_poll.py                  # poll todos
    python scripts/yt_poll.py --dry-run        # listar novos sem ingerir
    python scripts/yt_poll.py --only "BTG"     # 1 canal por substring no nome
    python scripts/yt_poll.py --max-per-channel 2  # cap p/ não saturar GPU

Custo API: 1 unit por canal (playlistItems.list). 23 canais × 6 polls/dia
≈ 138 units/dia (1.4% de 10k quota).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sqlite3
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

import yaml  # noqa: E402

CONFIG_FILE = ROOT / "config" / "youtube_sources.yaml"
STATE_FILE = ROOT / "data" / "yt_poll_state.json"
LOG_FILE = ROOT / "logs" / "yt_poll.log"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
INGEST_BATCH = ROOT / "scripts" / "yt_ingest_batch.py"

API_KEY = os.environ.get("YOUTUBE_API_KEY", "")


def _log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"{ts} {msg}\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)
    print(line, end="", flush=True)


def _read_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _yt_get(url: str) -> dict:
    """GET helper with circuit-breaker integration if available."""
    try:
        from agents._health import record as _hb_record
    except ImportError:
        _hb_record = None
    req = urllib.request.Request(url, headers={"User-Agent": "ii-yt-poll/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode("utf-8"))
        if _hb_record:
            _hb_record("youtube", "ok")
        return data
    except Exception as e:
        if _hb_record:
            _hb_record("youtube", "fail", f"{type(e).__name__}: {str(e)[:200]}")
        raise


def fetch_uploads_playlist_id(channel_id: str) -> str | None:
    """Cada channel_id YouTube tem uma uploads playlist com prefixo UU
    em vez de UC. Mas seguro: pedir via channels.list."""
    qs = urllib.parse.urlencode({
        "part": "contentDetails", "id": channel_id, "key": API_KEY,
    })
    data = _yt_get(f"https://www.googleapis.com/youtube/v3/channels?{qs}")
    items = data.get("items", [])
    if not items:
        return None
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def list_recent_videos(uploads_id: str, max_results: int = 10) -> list[dict]:
    """Lista vídeos mais recentes do canal via playlistItems."""
    qs = urllib.parse.urlencode({
        "part": "snippet,contentDetails",
        "playlistId": uploads_id,
        "maxResults": max_results,
        "key": API_KEY,
    })
    data = _yt_get(f"https://www.googleapis.com/youtube/v3/playlistItems?{qs}")
    out = []
    for it in data.get("items", []):
        sn = it["snippet"]
        cd = it["contentDetails"]
        out.append({
            "video_id": cd["videoId"],
            "title": sn["title"],
            "published_at": cd.get("videoPublishedAt") or sn["publishedAt"],
        })
    return out


def fetch_video_durations(video_ids: list[str]) -> dict[str, int]:
    """Chama videos.list para confirmar duration + liveBroadcastContent.
    1 quota unit por chamada (até 50 IDs). Devolve dict id→duration_sec."""
    if not video_ids:
        return {}
    out: dict[str, int] = {}
    # YouTube API allows up to 50 IDs per call
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        qs = urllib.parse.urlencode({
            "part": "contentDetails,snippet",
            "id": ",".join(batch),
            "key": API_KEY,
        })
        data = _yt_get(f"https://www.googleapis.com/youtube/v3/videos?{qs}")
        for it in data.get("items", []):
            vid = it["id"]
            iso_dur = it["contentDetails"].get("duration", "PT0S")
            live = it["snippet"].get("liveBroadcastContent", "none")
            out[vid] = (_parse_iso_duration(iso_dur), live)
    return out


def _parse_iso_duration(iso: str) -> int:
    """PT1H23M45S → seconds. PT15M → 900. PT45S → 45."""
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return 0
    h, mi, s = m.groups(default="0")
    return int(h) * 3600 + int(mi) * 60 + int(s)


def already_ingested(video_id: str) -> bool:
    for db in (DB_BR, DB_US):
        if not db.exists():
            continue
        try:
            with sqlite3.connect(db) as c:
                n = c.execute(
                    "SELECT COUNT(*) FROM videos WHERE video_id=?", (video_id,)
                ).fetchone()[0]
                if n > 0:
                    return True
        except sqlite3.OperationalError:
            continue
    return False


def poll_channel(channel: dict, state: dict, dry_run: bool, max_per: int) -> list[str]:
    """Devolve lista de novos video_ids que passaram filtros."""
    name = channel["name"]
    cid = channel["channel_id"]
    skip_kinds = set(channel.get("skip_kinds", []))
    min_dur = int(channel.get("min_duration_sec", 0))

    ch_state = state.setdefault(cid, {})
    last_seen = ch_state.get("last_seen_at", "1970-01-01T00:00:00+00:00")
    seen_ids = set(ch_state.get("video_ids_seen", []))

    uploads = ch_state.get("uploads_playlist_id")
    if not uploads:
        try:
            uploads = fetch_uploads_playlist_id(cid)
        except Exception as e:
            _log(f"[{name}] FAIL channel resolve: {type(e).__name__}: {e}")
            return []
        if not uploads:
            _log(f"[{name}] no uploads playlist, skipping")
            return []
        ch_state["uploads_playlist_id"] = uploads

    try:
        recent = list_recent_videos(uploads, max_results=10)
    except Exception as e:
        _log(f"[{name}] FAIL list videos: {type(e).__name__}: {e}")
        return []

    candidates = [v for v in recent
                  if v["video_id"] not in seen_ids
                  and v["published_at"] > last_seen]
    if not candidates:
        _log(f"[{name}] 0 new videos (last_seen={last_seen[:10]})")
        return []

    # Fetch durations + live status to filter
    ids = [v["video_id"] for v in candidates]
    metas = fetch_video_durations(ids)

    keep: list[str] = []
    for v in candidates:
        meta = metas.get(v["video_id"])
        if not meta:
            continue
        dur, live = meta
        if "shorts" in skip_kinds and dur < 60:
            continue
        if "live" in skip_kinds and live != "none":
            continue
        if dur < min_dur:
            _log(f"[{name}] skip {v['video_id']} dur={dur}s < min={min_dur}s ({v['title'][:50]})")
            continue
        if already_ingested(v["video_id"]):
            seen_ids.add(v["video_id"])
            continue
        keep.append(v["video_id"])
        _log(f"[{name}] queue {v['video_id']} dur={dur}s '{v['title'][:60]}'")

    keep = keep[:max_per] if max_per else keep

    # Only mutate state on real runs — dry-run must be repeatable.
    if not dry_run:
        seen_ids.update(keep)
        if recent:
            ch_state["last_seen_at"] = max(v["published_at"] for v in recent)
        ch_state["video_ids_seen"] = list(seen_ids)[-100:]  # cap at 100 ids
    return keep


def run_ingest(video_ids: list[str], dry_run: bool) -> int:
    if not video_ids:
        return 0
    if dry_run:
        _log(f"[DRY-RUN] would ingest {len(video_ids)} videos: {','.join(video_ids[:5])}{'...' if len(video_ids) > 5 else ''}")
        return 0
    py = sys.executable
    cmd = [py, "-X", "utf8", str(INGEST_BATCH), "--ids", ",".join(video_ids)]
    _log(f"INGEST {len(video_ids)} videos: {','.join(video_ids[:5])}{'...' if len(video_ids) > 5 else ''}")
    r = subprocess.run(cmd, cwd=str(ROOT), text=True, encoding="utf-8", errors="replace")
    return r.returncode


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="Listar mas não ingerir")
    p.add_argument("--only", default=None,
                   help="Substring no nome do canal (ex: 'BTG')")
    p.add_argument("--max-per-channel", type=int, default=3,
                   help="Cap de vídeos novos por canal por poll")
    p.add_argument("--priority", choices=["high", "medium", "low", "all"],
                   default="all")
    args = p.parse_args()

    if not API_KEY:
        _log("ERROR: YOUTUBE_API_KEY not set in env or .env")
        return 2

    if not CONFIG_FILE.exists():
        _log(f"ERROR: {CONFIG_FILE} missing")
        return 2

    cfg = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    channels = cfg.get("channels", [])
    if args.only:
        channels = [c for c in channels if args.only.lower() in c["name"].lower()]
    if args.priority != "all":
        channels = [c for c in channels if c.get("priority") == args.priority]

    if not channels:
        _log("no channels matched filters")
        return 0

    state = _read_state()
    all_to_ingest: list[str] = []

    for ch in channels:
        try:
            new_ids = poll_channel(ch, state, args.dry_run, args.max_per_channel)
            all_to_ingest.extend(new_ids)
        except Exception as e:
            _log(f"[{ch['name']}] poll exception: {type(e).__name__}: {e}")

    _write_state(state)
    _log(f"summary: {len(channels)} channels polled, {len(all_to_ingest)} new videos queued")

    rc = run_ingest(all_to_ingest, args.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main())
