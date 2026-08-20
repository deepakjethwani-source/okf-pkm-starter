#!/usr/bin/env python3
"""
clip_yt.py - Fetch a YouTube transcript + metadata into a Markdown file for your
knowledge-base `raw/` folder.

Usage:
    python tools/clip_yt.py "<youtube_url>" [--out raw] [--timestamps] [--lang en] [--force]

Options:
    --out DIR       Output directory (default: raw)
    --timestamps    Keep coarse [mm:ss] markers in the transcript body
    --lang CODE     Preferred caption language (default: en). Falls back to en.
    --force         Re-clip even if a file for this video already exists

Dependencies:
    pip install youtube-transcript-api        (required - the transcript itself)
    pip install yt-dlp                        (optional but recommended - rich
                                               metadata: title, channel, date,
                                               duration, chapters, description)

If yt-dlp is missing, you still get the transcript, just with thinner metadata.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date


# --------------------------------------------------------------------------- #
# Pure helpers (no network) - these are unit-tested at the bottom of the file  #
# --------------------------------------------------------------------------- #

def extract_video_id(url):
    """Pull the 11-char video id out of any common YouTube URL form, or a bare id."""
    if not url:
        return None
    patterns = [
        r"(?:v=|/embed/|/shorts/|/live/|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for p in patterns:
        m = re.search(p, url.strip())
        if m:
            return m.group(1)
    return None


def slugify(text, maxlen=60):
    text = re.sub(r"[^\w\s-]", "", (text or "")).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:maxlen].strip("-") or "untitled"


def format_date(yyyymmdd):
    if not yyyymmdd or len(str(yyyymmdd)) != 8:
        return None
    s = str(yyyymmdd)
    return f"{s[:4]}-{s[4:6]}-{s[6:]}"


def format_duration(seconds):
    if not seconds:
        return None
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m}m {s}s" if h else f"{m}m {s}s"


def fmt_timestamp(seconds):
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def yaml_str(s):
    """Quote/escape a value for a YAML front-matter field."""
    if s is None:
        return '""'
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_body(segments, with_timestamps=False, window=30, group=40):
    """segments: list of (start_seconds, text). Returns a clean Markdown body."""
    segs = [(t, re.sub(r"\s+", " ", txt).strip())
            for t, txt in segments if txt and txt.strip()]
    if not segs:
        return ""

    if not with_timestamps:
        paras, buf = [], []
        for _, txt in segs:
            buf.append(txt)
            if len(buf) >= group:
                paras.append(" ".join(buf))
                buf = []
        if buf:
            paras.append(" ".join(buf))
        return "\n\n".join(paras)

    blocks, cur_start, buf = [], None, []
    for t, txt in segs:
        if cur_start is None:
            cur_start = t
        buf.append(txt)
        if t - cur_start >= window:
            blocks.append(f"**[{fmt_timestamp(cur_start)}]** " + " ".join(buf))
            cur_start, buf = None, []
    if buf:
        blocks.append(f"**[{fmt_timestamp(cur_start or 0)}]** " + " ".join(buf))
    return "\n\n".join(blocks)


def build_document(meta, body, url, video_id):
    """Assemble front matter + optional chapters + description + transcript."""
    fm = [
        "---",
        f"title: {yaml_str(meta.get('title') or video_id)}",
        f"channel: {yaml_str(meta.get('channel'))}",
        f"url: {yaml_str(url)}",
        f"video_id: {yaml_str(video_id)}",
        f"upload_date: {yaml_str(format_date(meta.get('upload_date')))}",
        f"duration: {yaml_str(format_duration(meta.get('duration')))}",
        f"fetched: {yaml_str(date.today().isoformat())}",
        "tags: [yt-transcript]",
        "---",
        "",
        f"# {meta.get('title') or video_id}",
        "",
    ]
    parts = ["\n".join(fm)]

    chapters = meta.get("chapters") or []
    if chapters:
        lines = ["## Chapters", ""]
        for ch in chapters:
            lines.append(f"- [{fmt_timestamp(ch.get('start_time'))}] {ch.get('title', '').strip()}")
        parts.append("\n".join(lines))

    desc = (meta.get("description") or "").strip()
    if desc:
        parts.append("## Description\n\n" + desc)

    parts.append("## Transcript\n\n" + body)
    return "\n\n".join(parts).rstrip() + "\n"


def already_clipped(out_dir, video_id):
    """Return an existing file path if this video_id is already in out_dir."""
    if not os.path.isdir(out_dir):
        return None
    needle = f'video_id: "{video_id}"'
    for name in os.listdir(out_dir):
        if not name.lower().endswith(".md"):
            continue
        path = os.path.join(out_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                if needle in f.read(2000):
                    return path
        except OSError:
            continue
    return None


# --------------------------------------------------------------------------- #
# Network helpers                                                              #
# --------------------------------------------------------------------------- #

def fetch_metadata(url):
    """Rich metadata via yt-dlp. Returns {} if yt-dlp is not installed."""
    if shutil.which("yt-dlp") is None:
        print("  note: yt-dlp not found - continuing with minimal metadata "
              "(pip install yt-dlp for title/date/chapters).", file=sys.stderr)
        return {}
    try:
        out = subprocess.run(
            ["yt-dlp", "--dump-single-json", "--skip-download", url],
            capture_output=True, text=True, check=True,
        ).stdout
        d = json.loads(out)
        return {
            "title": d.get("title"),
            "channel": d.get("channel") or d.get("uploader"),
            "upload_date": d.get("upload_date"),
            "duration": d.get("duration"),
            "description": d.get("description"),
            "chapters": d.get("chapters") or [],
        }
    except Exception as e:  # noqa: BLE001 - degrade gracefully
        print(f"  note: yt-dlp metadata failed ({e}); continuing.", file=sys.stderr)
        return {}


def fetch_segments(video_id, lang):
    """
    Return a list of (start_seconds, text). Works with both the modern
    (>=1.0 instance) and legacy (<=0.6 classmethod) youtube-transcript-api.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("ERROR: youtube-transcript-api is not installed.\n"
              "       Run: pip install youtube-transcript-api", file=sys.stderr)
        sys.exit(2)

    langs = [lang, "en"] if lang != "en" else ["en"]

    # Modern API (>= 1.0): instance .fetch() returning snippet objects
    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=langs)
        return [(getattr(s, "start", 0.0), getattr(s, "text", "")) for s in fetched]
    except AttributeError:
        pass  # old library shape - fall through
    except Exception as e:  # noqa: BLE001
        # Modern lib present but this video failed - report clearly.
        print(f"ERROR: could not fetch transcript for {video_id}: {e}\n"
              "       The video may have captions disabled.", file=sys.stderr)
        sys.exit(1)

    # Legacy API (<= 0.6): classmethod returning list of dicts
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
        return [(d.get("start", 0.0), d.get("text", "")) for d in data]
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: could not fetch transcript for {video_id}: {e}\n"
              "       The video may have captions disabled.", file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description="Clip a YouTube transcript into raw/ as Markdown.")
    ap.add_argument("url", help="YouTube URL or 11-char video id")
    ap.add_argument("--out", default="raw", help="Output directory (default: raw)")
    ap.add_argument("--timestamps", action="store_true", help="Keep [mm:ss] markers")
    ap.add_argument("--lang", default="en", help="Preferred caption language (default: en)")
    ap.add_argument("--force", action="store_true", help="Re-clip even if it exists")
    args = ap.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"ERROR: couldn't find a video id in: {args.url}", file=sys.stderr)
        sys.exit(2)

    os.makedirs(args.out, exist_ok=True)

    existing = already_clipped(args.out, video_id)
    if existing and not args.force:
        print(f"Already clipped: {existing}\n(use --force to overwrite)")
        return

    print(f"Fetching metadata for {video_id} ...")
    meta = fetch_metadata(args.url)

    print("Fetching transcript ...")
    segments = fetch_segments(video_id, args.lang)
    if not segments:
        print("ERROR: transcript came back empty.", file=sys.stderr)
        sys.exit(1)

    body = build_body(segments, with_timestamps=args.timestamps)
    document = build_document(meta, body, args.url, video_id)

    datestr = format_date(meta.get("upload_date")) or date.today().isoformat()
    fname = f"{datestr}-{slugify(meta.get('title') or video_id)}.md"
    path = os.path.join(args.out, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(document)

    words = len(body.split())
    print(f"Saved: {path}")
    print(f"Title: {meta.get('title') or '(unknown - install yt-dlp for metadata)'}")
    print(f"Words: {words:,}")


if __name__ == "__main__":
    main()
