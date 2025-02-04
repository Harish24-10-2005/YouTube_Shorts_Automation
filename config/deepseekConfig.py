from openai import OpenAI
from dotenv import load_dotenv
import os

class OpenRouterClient:
    def __init__(self, api_key=None, base_url="https://openrouter.ai/api/v1", 
                 default_model="deepseek/deepseek-r1:free", 
                 default_headers=None):
        """
        Initialize the OpenRouter client.
        
        Args:
            api_key (str, optional): OpenRouter API key. If not provided, tries to load from .env.
            base_url (str): OpenRouter API base URL
            default_model (str): Default model to use for completions
            default_headers (dict): Default headers for API requests
        """
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("OPENROUTER_API_KEY")

        if default_headers is None:
            default_headers = {
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            }

        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.default_model = default_model
        self.default_headers = default_headers

    def get_completion(self, messages, model=None, headers=None):
        """
        Get chat completion from OpenRouter API.
        
        Args:
            messages (list): List of message dictionaries
            model (str, optional): Override default model
            headers (dict, optional): Override default headers
            
        Returns:
            str: Generated completion content
        """
        model = model or self.default_model
        headers = headers or self.default_headers

        completion = self.client.chat.completions.create(
            extra_headers=headers,
            model=model,
            messages=messages
        )
        try:
            if completion is None or completion.choices is None or completion.choices[0] is None:
                raise ValueError("DeepSeek API did not return any data")
            if completion.choices[0].message.content is None:
                return None
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error in get_completion: {e}")
            return None

# if __name__ == "__main__":
#     client = OpenRouterClient(
#         api_key="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"
#     )
#     response = client.get_completion(
#         messages=[{"role": "user", "content": "What if dinosaurs ruled cities in 2025?"}]
#     )
    
#     print(response)