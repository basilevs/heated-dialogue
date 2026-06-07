# Problem
ElevenLabs generates high qaulity voice acting, but has not implemented natural interruptions yet.
Prepending voice lines with "[interrupting]" tag does affect intonation, but fails to overlap multiple speakers.
This makes it hard to make an illusion of a heated debate.

<img width="1536" height="1024" alt="debate" src="https://github.com/user-attachments/assets/43134397-4738-4819-97ee-b3ac4ece7fd6" />


# Solution
Use API to generate non-ovelpaping acting and shift voice clips around in a post-processing remix to achieve the overlap.

# Disclaimer
This is an upolished prototype demostrating the feasibility.
Voice discovery fetches only the first page from
ElevenLabs (up to 100 voices). It checks saved voices first and falls back to
default voices.

# Prerequisites
FFmpeg has to be available. Check by running:
```
ffmpeg -version
```

# Run
```
pip install 'git+https://github.com/basilevs/heated-dialogue.git#egg=heated-dialogue'
export ELEVENLABS_API_KEY=<key>
text2dialogue --shift 0.7 dialogue_audio.mp3 <<EOF
Speaker 1: I'm talking a lot-
Speaker 2: [interrupting] I'm interrupting
EOF
open dialogue_audio.mp3
```

# Contribute
```
git clone https://github.com/basilevs/heated-dialogue.git
pip install -e ./heated-dialogue
```
