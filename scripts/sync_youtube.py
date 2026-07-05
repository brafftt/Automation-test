#!/usr/bin/env python3
"""
Sincroniza transcrições de vídeos do YouTube para a knowledge base.

Lê URLs de `scripts/youtube-sources.txt` (uma por linha, `#` para comentários) e
escreve markdown com frontmatter em `knowledge-base/youtube/`.

Uso:
    python scripts/sync_youtube.py              # incremental (salta ficheiros existentes)
    python scripts/sync_youtube.py --force      # re-download tudo
    python scripts/sync_youtube.py --url URL    # apenas 1 vídeo
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
    )
except ImportError:
    sys.exit(
        "Falta o pacote `youtube-transcript-api`. Instala com:\n"
        "    pip install youtube-transcript-api pytube"
    )

try:
    from pytube import YouTube
except ImportError:
    YouTube = None  # título fica em fallback


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = REPO_ROOT / "scripts" / "youtube-sources.txt"
OUTPUT_DIR = REPO_ROOT / "knowledge-base" / "youtube"
PREFERRED_LANGS = ["pt", "pt-PT", "pt-BR", "en"]


def extract_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be",):
        return parsed.path.lstrip("/") or None
    if parsed.hostname and "youtube.com" in parsed.hostname:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith(("/embed/", "/shorts/", "/v/")):
            return parsed.path.split("/")[2]
    return None


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")[:80] or "video"


def fetch_title(url: str, video_id: str) -> str:
    if YouTube is None:
        return video_id
    try:
        return YouTube(url).title
    except Exception:
        return video_id


def fetch_transcript(video_id: str) -> tuple[str, str]:
    """Devolve (texto, lang)."""
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    for lang in PREFERRED_LANGS:
        try:
            t = transcripts.find_transcript([lang])
            return _entries_to_text(t.fetch()), t.language_code
        except NoTranscriptFound:
            continue
    # último recurso: primeira transcrição disponível, traduzida para PT se possível
    for t in transcripts:
        try:
            translated = t.translate("pt")
            return _entries_to_text(translated.fetch()), "pt (traduzido)"
        except Exception:
            return _entries_to_text(t.fetch()), t.language_code
    raise NoTranscriptFound(video_id, PREFERRED_LANGS, transcripts)


def _entries_to_text(entries: list[dict]) -> str:
    return "\n".join(e["text"].strip() for e in entries if e.get("text"))


def process_url(url: str, force: bool) -> None:
    video_id = extract_video_id(url)
    if not video_id:
        print(f"⚠️  URL inválida: {url}")
        return

    title = fetch_title(url, video_id)
    filename = f"{slugify(title)}-{video_id}.md"
    output_path = OUTPUT_DIR / filename

    if output_path.exists() and not force:
        print(f"↷ Já existe: {filename}")
        return

    try:
        text, lang = fetch_transcript(video_id)
    except (TranscriptsDisabled, NoTranscriptFound):
        print(f"✗ Sem transcrição disponível: {title} ({video_id})")
        return
    except VideoUnavailable:
        print(f"✗ Vídeo indisponível: {video_id}")
        return

    frontmatter = (
        "---\n"
        f'url: "{url}"\n'
        f"video_id: {video_id}\n"
        f'title: "{title.replace(chr(34), chr(39))}"\n'
        f"lang: {lang}\n"
        f"fetched_at: {datetime.now(timezone.utc).isoformat()}\n"
        "---\n\n"
        f"# {title}\n\n"
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(frontmatter + text + "\n", encoding="utf-8")
    print(f"✓ Escrito: {filename}")


def read_sources() -> list[str]:
    if not SOURCES_FILE.exists():
        return []
    urls = []
    for line in SOURCES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-download mesmo se o ficheiro já existir.")
    parser.add_argument("--url", help="Processar apenas esta URL, ignorando o ficheiro de sources.")
    args = parser.parse_args()

    urls = [args.url] if args.url else read_sources()
    if not urls:
        print(f"Nada para processar. Adiciona URLs em {SOURCES_FILE.relative_to(REPO_ROOT)}.")
        return

    for url in urls:
        process_url(url, force=args.force)


if __name__ == "__main__":
    main()
