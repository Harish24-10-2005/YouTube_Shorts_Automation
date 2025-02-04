import os
from deepgram import DeepgramClient, SpeakOptions

class VoiceScriptGenerator:
    def __init__(self, api_key, model="aura-orpheus-en", output_folder="assets\VoiceScripts"):
        """
        Initialize the VoiceScriptGenerator.

        :param api_key: Your Deepgram API key.
        :param model: The voice model to use.
        :param output_folder: The folder where audio files will be saved.
        """
        self.deepgram = DeepgramClient(api_key)
        self.options = SpeakOptions(model=model)
        self.output_folder = output_folder
        
        # Create the output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def generate_voice(self, sentence: str, index: int):
        """
        Generate a voice file from a sentence and save it to the output folder.

        :param sentence: The sentence to convert to speech.
        :param index: The index used to generate the filename.
        :return: The response from the Deepgram API.
        """
        # Prepare the text payload
        text_payload = {"text": sentence}
        # Create a filename (e.g., scripts/script1.mp3)
        filename = os.path.join(self.output_folder, f"script{index}.mp3")
        # Generate and save the voice file using the Deepgram API
        response = self.deepgram.speak.v("1").save(filename, text_payload, self.options)
        return response

    def generate_voices_from_list(self, sentences: list):
        """
        Generate voice files for a list of sentences.

        :param sentences: A list of sentences to convert to speech.
        :return: A list of responses from the Deepgram API for each generated voice file.
        """
        responses = []
        for idx, sentence in enumerate(sentences, start=1):
            try:
                response = self.generate_voice(sentence, idx)
                print(f"Generated voice for 'script{idx}.mp3'")
                responses.append(response)
            except Exception as e:
                print(f"Error generating voice for 'script{idx}.mp3': {e}")
        return responses


# if __name__ == "__main__":
#     # Your Deepgram API key
#     DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

#     sentences = [
#         "Deepgram is great for real-time conversations…",
#         "And also, you can build apps for things like customer support, logistics, and more.",
#         "What do you think of the voices?"
#     ]

#     generator = VoiceScriptGenerator(DEEPGRAM_API_KEY)

#     responses = generator.generate_voices_from_list(sentences)

#     for response in responses:
#         print(response.to_json(indent=4))
