"""Command-line entry points for the heated-dialogue package."""
from os import getenv
import sys

from elevenlabs import ElevenLabs

from heateddialogue import parse_dialogue, text_to_dialogue_with_abrupt_interruptions

def text2dialogue() -> None:
    """Read text from stdin and process it into a dialogue.

    Currently a stub: echoes the received text to stdout so the entry
    point can be exercised end-to-end.
    """

    client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))

    available_speakers = ['UgBBYS2sOqTuMpoF3BR0', 'XcXEQzuLXRU9RcfWzEJt']
    inputs = parse_dialogue(sys.stdin.readlines(), available_speakers)
    audio = text_to_dialogue_with_abrupt_interruptions(client.text_to_dialogue, inputs, shift=0.5)
    output_path = "dialogue_audio.mp3"
    audio.export(output_path, format="mp3")
