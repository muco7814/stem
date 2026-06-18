from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load the vocal track
vocals_path = './separated_audio/htdemucs/audio2/vocals.wav'
vocal_audio = AudioSegment.from_wav(vocals_path)

# Normalize the audio to -20 dBFS (decibels relative to full scale)
# This will make the average loudness of the track around -20 dB.
normalized_vocal_audio = vocal_audio.normalize(headroom=0.0)

# Export the normalized audio
normalized_vocals_path = './separated_audio/htdemucs/audio2/vocals_normalized.wav'
normalized_vocal_audio.export(normalized_vocals_path, format="wav")

print(f"Normalized vocal track saved to: {normalized_vocals_path}")