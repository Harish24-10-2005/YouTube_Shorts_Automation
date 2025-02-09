import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.huggingface_api_keys = [
            os.getenv("HUGGING_FACE1"),
            os.getenv("HUGGING_FACE2")
        ]
        self.deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")