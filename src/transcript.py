import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    url = url.strip()

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0].split("&")[0]

    parsed = urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        vid = parse_qs(parsed.query).get("v", [None])[0]
        if vid:
            return vid

    match = re.search(r'(?:embed|shorts|v)/([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)

    raise ValueError(f"Could not extract video ID from URL: {url}")


def _entries_to_text(entries) -> str:
    """Convert transcript entries to plain text."""
    parts = []
    for entry in entries:
        if isinstance(entry, dict):
            parts.append(entry.get("text", ""))
        else:
            # v1.x returns objects with .text attribute
            parts.append(getattr(entry, "text", str(entry)))
    return " ".join(parts).strip()


def get_transcript(url: str) -> str:
    """
    Fetch transcript using youtube-transcript-api v1.2.4
    v1.x API:
      - YouTubeTranscriptApi() creates an instance
      - instance.list(video_id)  → lists available transcripts
      - instance.fetch(video_id, languages=[...]) → fetches transcript
    """
    video_id = extract_video_id(url)
    print(f"[INFO] Video ID: {video_id}")

    api = YouTubeTranscriptApi()

    # Step 1: List all available transcripts so we know what's there
    try:
        transcript_list = api.list(video_id)
        available = []
        for t in transcript_list:
            lang_code = getattr(t, 'language_code', '')
            lang_name = getattr(t, 'language', '')
            is_generated = getattr(t, 'is_generated', True)
            available.append(f"  - [{lang_code}] {lang_name} ({'auto' if is_generated else 'manual'})")
        print(f"[INFO] Available transcripts:\n" + "\n".join(available))
    except Exception as e:
        print(f"[WARN] Could not list transcripts: {e}")

    # Step 2: Try fetching in language priority order
    language_attempts = [
        ['en', 'en-US', 'en-GB'],   # English first
        ['hi'],                      # Hindi (common for Indian videos)
        ['en', 'hi'],                # English or Hindi
    ]

    for langs in language_attempts:
        try:
            result = api.fetch(video_id, languages=langs)
            text = _entries_to_text(result)
            if text:
                print(f"[INFO] Success with languages={langs} ({len(text)} chars)")
                return text
        except Exception as e:
            print(f"[WARN] fetch with languages={langs} failed: {e}")

    # Step 3: Fetch without any language filter (grab whatever is available)
    try:
        result = api.fetch(video_id)
        text = _entries_to_text(result)
        if text:
            print(f"[INFO] Success without language filter ({len(text)} chars)")
            return text
    except Exception as e:
        print(f"[WARN] fetch without language filter failed: {e}")

    # Step 4: Use list() to manually iterate and fetch each transcript
    try:
        transcript_list = api.list(video_id)
        for t in transcript_list:
            try:
                lang_code = getattr(t, 'language_code', 'unknown')
                result = api.fetch(video_id, languages=[lang_code])
                text = _entries_to_text(result)
                if text:
                    print(f"[INFO] Success via list iteration: {lang_code} ({len(text)} chars)")
                    return text
            except Exception as e:
                print(f"[WARN] List iteration failed for {lang_code}: {e}")
                continue
    except Exception as e:
        print(f"[WARN] List iteration outer failed: {e}")

    raise ValueError(
        "No transcript could be retrieved for this video. "
        "It may have captions disabled."
    )
