from base64 import b64decode
from os import getenv
from typing import Dict, List, Sequence
from pydub import AudioSegment
from io import BytesIO
from logging import debug, root, DEBUG, INFO
from copy import replace

from elevenlabs import DialogueInput
from elevenlabs.text_to_dialogue.client import TextToDialogueClient


def text_to_dialogue_with_abrupt_interruptions(
        dialogue_client: TextToDialogueClient,
        inputs: Sequence[DialogueInput],
        shift=0.5) -> AudioSegment:
    # Use of "[interrupting]" tag in the voice lines triggers a bug in
    # ElevenAPI mangling responce timings. The voices do not overlap.
    # As a workaround, we replace such tags with a similar "[jumping in]"
    # and shift timing around explicitly in post-processing.
    bug_workaround = []
    for i in inputs:
        d = i
        if d.text.startswith('[interrupting]'):
            d = replace(d, text=d.text.replace(
                '[interrupting]', '[jumping in]'))
        bug_workaround.append(d)
    response = dialogue_client.convert_with_timestamps(inputs=bug_workaround)
    segment_shifts = []
    total_shift = 0.
    length = 0.
    for segment in response.voice_segments:
        line = inputs[segment.dialogue_input_index]
        if line.text.startswith('[interrupting]'):
            total_shift += min(shift, segment.start_time_seconds)
        segment_shifts.append(total_shift)
        length = max(length, segment.end_time_seconds)

    processed_audio = AudioSegment.silent(1000. * (length - total_shift))

    debug("length: %f, total_shift: %f", length, total_shift)
    debug(response.voice_segments)
    dialogue_audio = AudioSegment.from_file(
        BytesIO(b64decode(response.audio_base_64)))
    for segment in response.voice_segments:
        segment_shift = segment_shifts[segment.dialogue_input_index]
        start_ms = int(segment.start_time_seconds*1000)
        end_ms = int(segment.end_time_seconds*1000)
        clip = dialogue_audio[start_ms:end_ms]
        position_ms = max(
            int((segment.start_time_seconds - segment_shift) * 1000), 0)
        debug("start_ms: %d, end_ms: %d, position_ms: %d",
              start_ms, end_ms, position_ms)
        processed_audio = processed_audio.overlay(clip, position=position_ms)

    return processed_audio

def parse_dialogue(text: Sequence[str], voice_ids: List[str]) -> Sequence[DialogueInput]:
    """Takes script in a form of:
        Name 1: voice line
        Name 2: voice line

        "Name x" can be any string uniquely identifing a speaker.
        Lines without a colon would be spoken by a "default" voice.
    """
    voice_ids = list(voice_ids)
    default_voice_id = None
    speaker_by_name: Dict[str, str] = {}
    for line in text:
        fields = line.split(":", 2)
        if len(fields) < 2:
            if not default_voice_id:
                default_voice_id = voice_ids.pop()
            voice_id = default_voice_id
            speech = fields[0]
        else:
            try:
                next_voice_id = voice_ids[0]
            except IndexError as e:
                speakers = ([fields[0]] + list(speaker_by_name.keys()))
                raise ValueError(f"Too many speakers found: {speakers}, add more voices." ) from e
            voice_id = speaker_by_name.setdefault(fields[0], next_voice_id)
            if next_voice_id == voice_ids[0]:
                del voice_ids[0]
            speech = fields[1]
        yield DialogueInput(text=speech, voice_id=voice_id)
