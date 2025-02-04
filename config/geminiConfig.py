import os
import google.generativeai as genai

class GeminiChat:
    def __init__(self, api_key=None, model_name="gemini-2.0-flash-exp", generation_config=None, history=None):
        """
        Initialize Gemini Chat client.
        
        Args:
            api_key (str): Gemini API key. If None, tries to get from environment variables.
            model_name (str): Model name to use
            generation_config (dict): Configuration for model generation
            history (list): Initial chat history
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("No API key provided and GEMINI_API_KEY environment variable not found")

        genai.configure(api_key=api_key)

        if generation_config is None:
            self.generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        else:
            self.generation_config = generation_config

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
        )

        self.chat_session = self.model.start_chat(history=history or [])

    def send_message(self, message):
        """
        Send message to Gemini and get response.
        
        Args:
            message (str): Input message/text
            
        Returns:
            str: Generated response text
        """
        try:
            response = self.chat_session.send_message(message)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error in Gemini API call: {str(e)}") from e

# if __name__ == "__main__":
#     chat = GeminiChat(api_key=None)
    
#     response = chat.send_message("What's the meaning of life?")
#     print(response)