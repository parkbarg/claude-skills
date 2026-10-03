import re
import sys
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(value: str) -> str:
    """YouTube URL または video ID から video ID を取得する。"""

    # すでに video ID の場合
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value

    parsed = urlparse(value)

    # https://youtu.be/xxxxxxxxxxx
    if parsed.hostname in {"youtu.be", "www.youtu.be"}:
        return parsed.path.lstrip("/").split("/")[0]

    # https://www.youtube.com/watch?v=xxxxxxxxxxx
    if parsed.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            query = parse_qs(parsed.query)
            if "v" in query:
                return query["v"][0]

        # shorts / embed
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] in {"shorts", "embed"}:
            return parts[1]

    raise ValueError("YouTube URL または video ID を認識できませんでした")


def format_time(seconds: float) -> str:
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    return f"{minutes:02}:{seconds:02}"


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_transcript.py <youtube-url-or-video-id>")
        sys.exit(1)

    video_id = extract_video_id(sys.argv[1])

    api = YouTubeTranscriptApi()

    transcript = api.fetch(
        video_id,
        languages=["ja", "en"],
    )

    for item in transcript:
        timestamp = format_time(item.start)
        print(f"[{timestamp}] {item.text}")


if __name__ == "__main__":
    main()
