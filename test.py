# from TTS.api import TTS

# # Initialize the TTS model
# tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True, gpu=False)

# # Print available speakers
# print("Available speakers:", tts.speakers)

# # Choose a speaker
# selected_speaker = "p254"

para = """
    "What if… you unearthed a dusty diary in your attic, its pages filled with impossible events and elegant handwriting?",
    "Imagine finding a chilling prophecy about a global blackout, dated 1888. Your heart pounds, and you flip to the next entry.",
    "The next entry speaks of future tech beyond dreams, described so vividly, it feels undeniably real; you're not just reading, you're experiencing it.",
    "The writer warns of time ripple effects, if technologies fall into the wrong hands. A chill runs down your spine as a connection forms.",
    "Each page reveals a piece: historical anomalies, temporal paradox warnings. Then, a pattern emerges.",
    "Diary entries mirror current events, predicting them with unnerving accuracy, like yesterday’s earthquake shaking the city.",
    "Panic! The most recent entry, dated *tomorrow*, describes a catastrophe in your city…on *your* street. ",
    "Desperate, you seek a solution, but only find cryptic clues, pointing to a hidden object in your house.",
    "Racing against time, you follow the clues to an antique clock. Inside, a secret compartment reveals a tarnished key, But it doesn't unlock any lock you know of.",
    "The diary's final entry: 'The key unlocks not a door, but a memory—your own.' Realization dawns: flashes of the future… You are the time traveler."
"""

# # Specify output file path
# output_path = "motivational_voice.wav"

# # Synthesize with different speeds:
# # For slower speech (e.g., 50% speed)
# tts.tts_to_file(
#     text=para,
#     file_path=output_path,
#     speaker=selected_speaker,
#     speed=0.5,          # 0.5x speed (slower)
#     split_sentences=True
# )

# print("Audio saved as", output_path)
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs  # Added XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# Allow all required configs to be unpickled safely
torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs  # Added this to the safe globals
])

from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS and move to device
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
tts.tts_to_file(
    text=para,
    speaker_wav="D:/AI_AGENT_FOR_YOUTUBE/Shorts_Agent/assets/clonningVoices/voice_preview_cartermotivational.mp3",
    language="en",
    file_path="output.wav"
)