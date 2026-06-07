"""Command-line entry points for the heated-dialogue package."""
import argparse
from os import getenv
import sys

from elevenlabs import ElevenLabs

from heateddialogue import parse_dialogue, text_to_dialogue_with_abrupt_interruptions

def text2dialogue() -> None:
    """Read text from stdin and export generated dialogue audio to a file."""

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Output audio filename")
    args = parser.parse_args()

    client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))

    available_speakers = ['UgBBYS2sOqTuMpoF3BR0', 'XcXEQzuLXRU9RcfWzEJt']
    inputs = parse_dialogue(sys.stdin.readlines(), available_speakers)
    audio = text_to_dialogue_with_abrupt_interruptions(client.text_to_dialogue, list(inputs), shift=0.5)
    output_path = args.filename
    audio.export(output_path, format="mp3")
