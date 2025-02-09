from TTS.api import TTS

# Initialize the TTS model
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True, gpu=False)

# Print available speakers
print("Available speakers:", tts.speakers)

# Choose a speaker
selected_speaker = "p267"

# Define your text
para = "You weren't built to crumble; you were forged in fire to rise! The universe didn't design you for mediocrity; it crafted you for greatness. Stop accepting the narrative of failure; embrace the power that surges within you, waiting to be unleashed!"

# Specify output file path
output_path = "motivational_voice.wav"

# Synthesize with different speeds:
# For slower speech (e.g., 50% speed)
tts.tts_to_file(
    text=para,
    file_path=output_path,
    speaker=selected_speaker,
    speed=0.5,          # 0.5x speed (slower)
    split_sentences=True
)

print("Audio saved as", output_path)
