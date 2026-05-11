"""pod_poll — periodic poller para podcasts em config/podcast_sources.yaml.

Cada poll:
  1. Fetch RSS feed (1 req/feed, ~50KB).
  2. Parse <item>s; cada um tem <enclosure url=...mp3>, <pubDate>, <title>.
  3. Filtra: items publicados desde last_seen_at do feed.
  4. Dedup contra videos table (source='podcast'); state em pod_poll_state.json.
  5. Download MP3 → cache em data/podcast_audio/.
  6. Dispara yt_ingest.py --audio-file --source-id PODCAST-<slug>-<date>
     reaproveitando Whisper + Ollama.

State em data/pod_poll_state.json:
  { feed_name: {"last_seen_at": "ISO", "guids": [...]} }

Uso:
    python scripts/pod_poll.py                  # poll todos
    python scripts/pod_poll.py --dry-run        # listar sem download
    python scripts/pod_poll.py --only "WSJ"     # 1 feed por substring
    python scripts/pod_poll.py --max-per-feed 1 # cap p/ não saturar GPU
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

import yaml  # noqa: E402

CONFIG_FILE = ROOT / "config" / "podcast_sources.yaml"
STATE_FILE = ROOT / "data" / "pod_poll_state.json"
LOG_FILE = ROOT / "logs" / "pod_poll.log"
AUDIO_DIR = ROOT / "data" / "podcast_audio"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
INGEST = ROOT / "scripts" / "yt_ingest.py"

UA = "Mozilla/5.0 ii-pod-poll/1.0"


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


def _slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:60] or "podcast"


def fetch_feed(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


# Minimal RSS parser — avoids feedparser dependency.
ITEM_RE = re.compile(r"<item[\s>](.*?)</item>", re.DOTALL)
TITLE_RE = re.compile(r"<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", re.DOTALL)
PUBDATE_RE = re.compile(r"<pubDate[^>]*>(.*?)</pubDate>", re.DOTALL)
GUID_RE = re.compile(r"<guid[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</guid>", re.DOTALL)
ENCL_RE = re.compile(r"<enclosure[^>]*url=\"([^\"]+)\"", re.DOTALL)
DURATION_RE = re.compile(r"<itunes:duration[^>]*>(.*?)</itunes:duration>", re.DOTALL)


def parse_feed(xml: str) -> list[dict]:
    out = []
    for m in ITEM_RE.finditer(xml):
        block = m.group(1)
        title = (TITLE_RE.search(block) or [""]).group(1).strip() if TITLE_RE.search(block) else ""
        pubdate = (PUBDATE_RE.search(block).group(1).strip() if PUBDATE_RE.search(block) else "")
        guid = (GUID_RE.search(block).group(1).strip() if GUID_RE.search(block) else "")
        encl = (ENCL_RE.search(block).group(1).strip() if ENCL_RE.search(block) else "")
        dur_str = (DURATION_RE.search(block).group(1).strip() if DURATION_RE.search(block) else "")
        if not encl:
            continue
        out.append({
            "title": title[:200],
            "pubdate_raw": pubdate,
            "pubdate_iso": _parse_pubdate(pubdate),
            "guid": guid or encl,
            "audio_url": encl,
            "duration_sec": _parse_duration(dur_str),
        })
    return out


def _parse_pubdate(s: str) -> str:
    """RFC 822 → ISO 8601 (best effort). Returns YYYY-MM-DD if parse fails."""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat(timespec="seconds")
    except Exception:
        return s[:10] if s else ""


def _parse_duration(s: str) -> int:
    """itunes:duration can be HH:MM:SS, MM:SS, or just seconds."""
    s = (s or "").strip()
    if not s:
        return 0
    if s.isdigit():
        return int(s)
    parts = s.split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
    except ValueError:
        return 0
    return 0


def already_ingested(source_id: str) -> bool:
    for db in (DB_BR, DB_US):
        if not db.exists():
            continue
        try:
            with sqlite3.connect(db) as c:
                n = c.execute(
                    "SELECT COUNT(*) FROM videos WHERE video_id=?", (source_id,)
                ).fetchone()[0]
                if n > 0:
                    return True
        except sqlite3.OperationalError:
            continue
    return False


def download_audio(url: str, target: Path, timeout: int = 120) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 1024:
        return True
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            with target.open("wb") as f:
                while True:
                    chunk = r.read(64 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
        return True
    except Exception as e:
        _log(f"download FAIL {url[:60]}: {type(e).__name__}: {e}")
        if target.exists():
            target.unlink(missing_ok=True)
        return False


def ingest_episode(feed_name: str, item: dict, dry_run: bool) -> int:
    show_slug = _slugify(feed_name)
    date_part = item["pubdate_iso"][:10] or "unknown-date"
    # GUID hash to disambiguate same-day episodes (WSJ Minute Briefing has 6/dia)
    import hashlib
    guid_hash = hashlib.sha256(item["guid"].encode()).hexdigest()[:8]
    source_id = f"pod-{show_slug}-{date_part}-{guid_hash}"

    if already_ingested(source_id):
        _log(f"[{feed_name}] skip {source_id} (already ingested)")
        return 0

    audio_path = AUDIO_DIR / f"{source_id}.mp3"
    if dry_run:
        _log(f"[DRY-RUN][{feed_name}] would ingest {source_id} '{item['title'][:60]}'")
        return 0

    _log(f"[{feed_name}] download {item['audio_url'][:60]} → {audio_path.name}")
    if not download_audio(item["audio_url"], audio_path):
        return 1

    cmd = [
        sys.executable, "-X", "utf8", str(INGEST),
        "--audio-file", str(audio_path),
        "--source-id", source_id,
        "--source-channel", feed_name,
        "--source-title", item["title"],
        "--source-pubdate", item["pubdate_iso"],
        "--source-url", item["audio_url"],
    ]
    _log(f"[{feed_name}] ingest {source_id}")
    r = subprocess.run(cmd, cwd=str(ROOT), text=True, encoding="utf-8", errors="replace")

    # Cleanup audio after successful ingest (saves disk; cached transcript stays)
    if r.returncode == 0 and audio_path.exists():
        try:
            audio_path.unlink()
        except OSError:
            pass

    return r.returncode


def poll_feed(feed: dict, state: dict, dry_run: bool, max_per: int) -> int:
    name = feed["name"]
    url = feed["rss"]
    feed_state = state.setdefault(name, {})
    last_seen = feed_state.get("last_seen_at", "1970-01-01T00:00:00+00:00")
    seen_guids = set(feed_state.get("guids", []))

    try:
        xml = fetch_feed(url)
    except Exception as e:
        _log(f"[{name}] feed FAIL: {type(e).__name__}: {e}")
        return 0

    items = parse_feed(xml)
    if not items:
        _log(f"[{name}] no items parsed (feed likely malformed)")
        return 0

    candidates = [it for it in items
                  if it["guid"] not in seen_guids
                  and (it["pubdate_iso"] or "9999") > last_seen]

    candidates = candidates[:max_per] if max_per else candidates

    if not candidates:
        _log(f"[{name}] 0 new episodes (last_seen={last_seen[:10]})")
        return 0

    rc_total = 0
    for item in candidates:
        rc = ingest_episode(name, item, dry_run)
        rc_total += abs(rc)
        if not dry_run:
            seen_guids.add(item["guid"])
            if item["pubdate_iso"] and item["pubdate_iso"] > last_seen:
                last_seen = item["pubdate_iso"]

    if not dry_run:
        feed_state["last_seen_at"] = last_seen
        feed_state["guids"] = list(seen_guids)[-100:]
    return rc_total


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="Listar mas não descarregar nem ingerir")
    p.add_argument("--only", default=None,
                   help="Substring no nome do feed (ex: 'WSJ')")
    p.add_argument("--max-per-feed", type=int, default=2,
                   help="Cap de episódios novos por feed por poll")
    p.add_argument("--priority", choices=["high", "medium", "low", "all"],
                   default="all")
    args = p.parse_args()

    if not CONFIG_FILE.exists():
        _log(f"ERROR: {CONFIG_FILE} missing")
        return 2

    cfg = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    feeds = cfg.get("feeds", [])
    if args.only:
        feeds = [f for f in feeds if args.only.lower() in f["name"].lower()]
    if args.priority != "all":
        feeds = [f for f in feeds if f.get("priority") == args.priority]

    if not feeds:
        _log("no feeds matched filters")
        return 0

    state = _read_state()
    rc_total = 0
    for feed in feeds:
        try:
            rc = poll_feed(feed, state, args.dry_run, args.max_per_feed)
            rc_total += rc
        except Exception as e:
            _log(f"[{feed['name']}] poll exception: {type(e).__name__}: {e}")

    _write_state(state)
    _log(f"summary: {len(feeds)} feeds polled, rc_total={rc_total}")
    return 0 if rc_total < 5 else 1  # treat occasional failures as non-fatal


if __name__ == "__main__":
    sys.exit(main())
