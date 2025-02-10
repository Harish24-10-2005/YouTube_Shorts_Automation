import os
from TTS.api import TTS
import torch
import gc
import logging
from typing import List, Dict, Optional
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs  # Added XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.api import TTS
# Allow all required configs to be unpickled safely
torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs  # Added this to the safe globals
])
class VoiceGenerator:
    def __init__(self, 
                 channel = "ChronoShift_Chronicles",
                 output_folder: str = "assets/VoiceScripts",
                 device: str = "cuda" if torch.cuda.is_available() else "cpu",
                 model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        """
        Initialize a voice generator using the VITS model.
        
        Args:
            output_folder: Directory to save generated voice files.
            device: Device to run the model on ('cuda' or 'cpu').
            model_name: Name of the TTS model to use.
        """
        self.output_folder = output_folder
        self.device = device
        self.logger = logging.getLogger(__name__)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        
        try:
            os.makedirs(self.output_folder, exist_ok=True)
            self._clear_memory()
            self.speakerpath = None
            self.logger.info(f"Initializing TTS model {model_name} on {device}")
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            self.Motivational_speaker_path = "D:/AI_AGENT_FOR_YOUTUBE/Shorts_Agent/assets/clonningVoices/voice_preview_motivational coach.mp3"
            self.Mysterious_speaker_path = "D:/AI_AGENT_FOR_YOUTUBE/Shorts_Agent/assets/clonningVoices/voice_preview_cartermotivational.mp3"
            if channel == "motivational":
                self.speakerpath = self.Motivational_speaker_path
            else:
                self.speakerpath = self.Mysterious_speaker_path    
        except Exception as e:
            self.logger.error(f"Error initializing VoiceGenerator: {str(e)}")
            raise
    
    def _clear_memory(self):
        """Clear CUDA memory if using GPU."""
        if self.device == "cuda":
            torch.cuda.empty_cache()
            gc.collect()
    
    def generate_voice(self, 
                       sentence: str, 
                       filename: str = "output.wav",
                       speaker: str = "p267",
                       speed: float = 0.2,
                       split_sentences: bool = True) -> Optional[str]:
        """
        Generate voice for a single sentence.
        
        Args:
            sentence: Text to convert to speech.
            filename: Output filename.
            speaker: Selected speaker key from available speakers.
            speed: Speed factor for the synthesized speech.
            split_sentences: Enable sentence splitting for natural pauses.
            
        Returns:
            Path to generated file or None if generation failed.
        """
        if not sentence:
            raise ValueError("Empty text provided")
            
        filepath = os.path.join(self.output_folder, filename)
        
        try:
            self._clear_memory()
            self.logger.info(f"Generating voice for text: {sentence[:50]}...")

            self.tts.tts_to_file(
                text=sentence,
                speaker_wav=self.speakerpath,
                language="en",
                file_path=filepath,
                split_sentences=split_sentences
            )
            self.logger.info(f"Voice generated successfully at: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error generating voice: {str(e)}")
            return None
        finally:
            self._clear_memory()
            
    def generate_multiple_voices(self, 
                                 sentences: List[str], 
                                 base_filename: str = "voicescript",
                                 speaker: str = "p267",
                                 speed: float = 0.2,
                                 split_sentences: bool = True) -> Dict[str, str]:
        """
        Generate voice files for multiple sentences with sequential naming.
        
        Args:
            sentences: List of sentences to convert to speech.
            base_filename: Base name for output files (appended with sequential numbers).
            speaker: Selected speaker key from available speakers.
            speed: Speed factor for the synthesized speech.
            split_sentences: Enable sentence splitting for natural pauses.
            
        Returns:
            Dictionary mapping each sentence to its output filepath.
        """
        results = {}
        
        for i, sentence in enumerate(sentences, 1):
            filename = f"{base_filename}{i}.wav"
            
            try:
                filepath = self.generate_voice(
                    sentence,
                    filename,
                    speaker=speaker,
                    speed=0.5,   
                    split_sentences=split_sentences
                )
                if filepath:
                    results[sentence] = filepath
                else:
                    self.logger.warning(f"Failed to generate voice for sentence {i}")
                    
            except Exception as e:
                self.logger.error(f"Error processing sentence {i}: {str(e)}")
                continue
                
        return results

# # Example usage:
# if __name__ == "__main__":
#     try:
#         generator = VoiceGenerator()
        
#         # Example list of sentences
#         sentences = [
#             "What if… you unearthed a dusty diary in your attic, its pages filled with impossible events and elegant handwriting?",
#             "Imagine finding a chilling prophecy about a global blackout, dated 1888. Your heart pounds, and you flip to the next entry.",
#             "The next entry speaks of future tech beyond dreams, described so vividly, it feels undeniably real; you're not just reading, you're experiencing it.",
#             "The writer warns of time ripple effects, if technologies fall into the wrong hands. A chill runs down your spine as a connection forms.",
#             "Each page reveals a piece: historical anomalies, temporal paradox warnings. Then, a pattern emerges.",
#             "Diary entries mirror current events, predicting them with unnerving accuracy, like yesterday’s earthquake shaking the city.",
#             "Panic! The most recent entry, dated *tomorrow*, describes a catastrophe in your city…on *your* street.",
#             "Desperate, you seek a solution, but only find cryptic clues, pointing to a hidden object in your house.",
#             "Racing against time, you follow the clues to an antique clock. Inside, a secret compartment reveals a tarnished key, But it doesn't unlock any lock you know of.",
#             "The diary's final entry: 'The key unlocks not a door, but a memory—your own.' Realization dawns: flashes of the future… You are the time traveler."
#         ]
        
#         # Generate voices for all sentences using the selected speaker, speed, and sentence splitting.
#         results = generator.generate_multiple_voices(sentences)
        
#         # Print results
#         for sentence, filepath in results.items():
#             print(f"\nSentence: {sentence}")
#             print(f"Generated file: {filepath}")
            
#     except Exception as e:
#         print(f"Error in main: {str(e)}")
