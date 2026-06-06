from base64 import b64decode
from os import getenv
from typing import Sequence
from elevenlabs import ElevenLabs, DialogueInput
from elevenlabs.text_to_dialogue.client import TextToDialogueClient
from pydub import AudioSegment
from io import BytesIO
from logging import debug, root, DEBUG



def text_to_dialogue_with_abrupt_interruptions(dialogue_client: TextToDialogueClient, inputs: Sequence[DialogueInput], shift=0.5) -> AudioSegment:
    response = dialogue_client.convert_with_timestamps(inputs=inputs)
    segment_shifts=[]
    total_shift = 0.    
    length = 0.
    for line, segment in zip(inputs, response.voice_segments):
        if line.text.startswith('[interrupting]'):
            total_shift += min(shift, segment.start_time_seconds)
        segment_shifts.append(total_shift)
        length = max(length, segment.end_time_seconds)

    processed_audio = AudioSegment.silent(1000. * (length - total_shift))

    debug("length: %f, total_shift: %f", length, total_shift)
    debug(response.voice_segments)
    dialogue_audio = AudioSegment.from_file(BytesIO(b64decode(response.audio_base_64)))
    for segment in response.voice_segments:
        segment_shift = segment_shifts[segment.dialogue_input_index]
        start_ms = int(segment.start_time_seconds*1000)
        end_ms = int(segment.end_time_seconds*1000)
        clip = dialogue_audio[start_ms:end_ms]
        position_ms = max(int((segment.start_time_seconds - segment_shift) * 1000), 0)
        debug("start_ms: %d, end_ms: %d, position_ms: %d", start_ms, end_ms, position_ms)
        processed_audio = processed_audio.overlay(clip, position = position_ms)

    return processed_audio

client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))
inputs=[
    DialogueInput(
        text="So I was thinking we could-",
        voice_id="UgBBYS2sOqTuMpoF3BR0",
    ),
    DialogueInput(
        text="[interrupting] -test our new timing features?",
        voice_id="XcXEQzuLXRU9RcfWzEJt",
    ),
    DialogueInput(
        text="Exactly! How did you-",
        voice_id="UgBBYS2sOqTuMpoF3BR0",
    ),
    DialogueInput(
        text="[interrupting] -know what you were thinking? Lucky guess!",
        voice_id="XcXEQzuLXRU9RcfWzEJt",
    )
]


root.setLevel(DEBUG)
output_path = "dialogue_audio.mp3"
audio = text_to_dialogue_with_abrupt_interruptions(client.text_to_dialogue, inputs, shift=1.0)
audio.export(output_path, format="mp3")

print(f"Saved audio to {output_path}")