from os import getenv
from pprint import pprint
from elevenlabs import ElevenLabs, DialogueInput

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

client = ElevenLabs(api_key=getenv("ELEVENLABS_API_KEY"))
response = client.text_to_dialogue.convert_with_timestamps(inputs=inputs)

pprint(response.voice_segments)

# Output:
# [VoiceSegment(voice_id='UgBBYS2sOqTuMpoF3BR0', start_time_seconds=0.0, end_time_seconds=1.488, character_start_index=0, character_end_index=27, dialogue_input_index=0),
#  VoiceSegment(voice_id='XcXEQzuLXRU9RcfWzEJt', start_time_seconds=1.488, end_time_seconds=1.488, character_start_index=27, character_end_index=72, dialogue_input_index=1),
#  VoiceSegment(voice_id='UgBBYS2sOqTuMpoF3BR0', start_time_seconds=1.488, end_time_seconds=1.488, character_start_index=72, character_end_index=93, dialogue_input_index=2),
#  VoiceSegment(voice_id='XcXEQzuLXRU9RcfWzEJt', start_time_seconds=1.488, end_time_seconds=7.75, character_start_index=93, character_end_index=150, dialogue_input_index=3)]

# Note that three segmens start at the same time
