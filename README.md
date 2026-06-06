# Problem
ElevenLabs generates high qaulity voice acting, but has not implemented natural interruptions yet.
Prepending voice lines with "[interrupting]" tag does affect intonation, but fails to overlap multiple speakers.
This makes it hard to make an illusion of a heated debate.

# Solution
Use API to generate non-ovelpaping acting and shift voice clips around in a post-processing remix to achieve the overlap.

# Disclaimer
This is an upolished prototype demostrating the feasibility.

# Prerequisites
FFmpeg has to be available. Check by running:

```
ffmpeg -version
```

# Run
```
git clone https://github.com/basilevs/heated-dialogue.git
pip install -e ./heated-dialogue
export ELEVENLABS_API_KEY=<key>
python3 ./heated-dialogue/prototype.py
```
