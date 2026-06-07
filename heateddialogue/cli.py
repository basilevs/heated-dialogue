"""Command-line entry points for the heated-dialogue package."""
import argparse
from logging import DEBUG, root
from os import getenv
from pathlib import Path
import sys

from elevenlabs import ElevenLabs

from heateddialogue import parse_dialogue, text_to_dialogue_with_abrupt_interruptions


def _fetch_voice_ids(client: ElevenLabs, voice_type: str) -> list[str]:
    """Return up to 100 voice IDs for a given ElevenLabs voice_type."""

    try:
        response = client.voices.search(
            voice_type=voice_type,
            page_size=100,
        )
    except Exception as exc:
        raise SystemExit(f"Failed to fetch ElevenLabs voices: {exc}") from exc

    voice_ids: list[str] = []
    for voice in response.voices:
        voice_id = voice.voice_id
        if voice_id:
            voice_ids.append(voice_id)

    return voice_ids


def get_available_speakers(client: ElevenLabs) -> list[str]:
    """Fetch user voices first, then fall back to default voices."""

    saved_voice_ids = _fetch_voice_ids(client, "saved")
    if saved_voice_ids:
        return saved_voice_ids

    default_voice_ids = _fetch_voice_ids(client, "default")
    if default_voice_ids:
        return default_voice_ids

    raise SystemExit("No voices available from ElevenLabs (saved or default).")


def detect_export_format(filename: str) -> str:
    """Infer an export format from output filename extension.

    pydub requires explicit format names that are sometimes different from
    common file extensions (for example, .m4a uses the ffmpeg `ipod` muxer).
    """

    extension = Path(filename).suffix.lower().lstrip(".")
    if not extension:
        raise SystemExit("Output filename must include an extension, e.g. output.mp3")

    extension_to_format = {
        "mp3": "mp3",
        "wav": "wav",
        "flac": "flac",
        "ogg": "ogg",
        "oga": "ogg",
        "aac": "adts",
        "m4a": "ipod",
        "mp4": "mp4",
        "aif": "aiff",
        "aiff": "aiff",
    }

    export_format = extension_to_format.get(extension)
    if export_format is None:
        supported = ", ".join(sorted(extension_to_format.keys()))
        raise SystemExit(f"Unsupported output extension '.{extension}'. Supported: {supported}")

    return export_format

def text2dialogue() -> None:
    """Read text from stdin and export generated dialogue audio to a file."""

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Output audio filename")
    parser.add_argument(
        "--shift",
        type=float,
        default=0.5,
        help=(
            "Interruption overlap in seconds. Larger values create longer "
            "talk-over of the rude interrupter."
        ),
    )
    args = parser.parse_args()

    api_key=getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit("Set ELEVENLABS_API_KEY environment variable")
    
    client = ElevenLabs(api_key=api_key)

    available_speakers = get_available_speakers(client)
    #root.setLevel(DEBUG)
    inputs = parse_dialogue(sys.stdin.readlines(), available_speakers)
    audio = text_to_dialogue_with_abrupt_interruptions(
        client.text_to_dialogue,
        list(inputs),
        shift=args.shift,
    )
    output_path = args.filename
    output_format = detect_export_format(output_path)
    audio.export(output_path, format=output_format)
