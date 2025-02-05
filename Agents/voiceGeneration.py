import os
from TTS.api import TTS
import torch
import gc
import logging
from typing import List, Dict, Optional

class VoiceGenerator:
    def __init__(self, 
                 output_folder: str = "assets/VoiceScripts",
                 device: str = "cuda" if torch.cuda.is_available() else "cpu",
                 model_name: str = "tts_models/en/ljspeech/tacotron2-DDC"):
        """
        Initialize a voice generator using Tacotron2 model.
        
        Args:
            output_folder: Directory to save generated voice files
            device: Device to run the model on ('cuda' or 'cpu')
            model_name: Name of the TTS model to use
        """
        self.output_folder = output_folder
        self.device = device
        self.logger = logging.getLogger(__name__)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        
        try:
            os.makedirs(self.output_folder, exist_ok=True)
            self._clear_memory()
            
            self.logger.info(f"Initializing TTS model {model_name} on {device}")
            self.tts = TTS(model_name).to(device)
            
        except Exception as e:
            self.logger.error(f"Error initializing VoiceGenerator: {str(e)}")
            raise
    
    def _clear_memory(self):
        """Clear CUDA memory if using GPU"""
        if self.device == "cuda":
            torch.cuda.empty_cache()
            gc.collect()
    
    def generate_voice(self, 
                      sentence: str, 
                      filename: str = "output.wav") -> Optional[str]:
        """
        Generate voice for a single sentence.
        
        Args:
            sentence: Text to convert to speech
            filename: Output filename
            
        Returns:
            Path to generated file or None if generation failed
        """
        if not sentence:
            raise ValueError("Empty text provided")
            
        filepath = os.path.join(self.output_folder, filename)
        
        try:
            self._clear_memory()
            self.logger.info(f"Generating voice for text: {sentence[:50]}...")
            
            self.tts.tts_to_file(
                text=sentence,
                file_path=filepath
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
                               base_filename: str = "voicescript") -> Dict[str, str]:
        """
        Generate voice files for multiple sentences with sequential naming.
        
        Args:
            sentences: List of sentences to convert to speech
            base_filename: Base name for output files (will be appended with numbers)
            
        Returns:
            Dictionary mapping sentence to output filepath
        """
        results = {}
        
        for i, sentence in enumerate(sentences, 1):
            filename = f"{base_filename}{i}.wav"
            
            try:
                filepath = self.generate_voice(sentence, filename)
                if filepath:
                    results[sentence] = filepath
                else:
                    self.logger.warning(f"Failed to generate voice for sentence {i}")
                    
            except Exception as e:
                self.logger.error(f"Error processing sentence {i}: {str(e)}")
                continue
                
        return results

# if __name__ == "__main__":
#     try:
#         generator = VoiceGenerator()
        
#         # Example list of sentences
#         sentences = [
#             "In the depths of neural networks, secrets await discovery.",
#             "The quantum computer hums with infinite possibilities.",
#             "Through the digital realm, information flows like water.",
#             "Algorithms dance in the silicon forest of computation."
#         ]
        
#         # Generate voices for all sentences
#         results = generator.generate_multiple_voices(sentences)
        
#         # Print results
#         for sentence, filepath in results.items():
#             print(f"\nSentence: {sentence}")
#             print(f"Generated file: {filepath}")
            
#     except Exception as e:
#         print(f"Error in main: {str(e)}")