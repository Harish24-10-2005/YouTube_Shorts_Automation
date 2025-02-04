from phi.agent import Agent
from phi.tools import tool
import json
import os
from dotenv import load_dotenv
from prompt.prompt import CONTENT_PROMPT
from config.deepseekConfig import OpenRouterClient
import google.generativeai as genai
from  config.geminiConfig import GeminiChat

load_dotenv()

class ContentAgent:
    def __init__(self, **kwargs):
        """
        Initialize the Content Agent with OpenRouter client and content prompt.
        """
        load_dotenv()
        # self.client = OpenRouterClient(
        #     api_key=os.getenv("OPENROUTER_API_KEY"),
        # )
        self.chat = GeminiChat(api_key=None)
        self.prompt = CONTENT_PROMPT  

    def generate_content_DeepSeek(self, title: str, model: str = None) -> str:
        """
        Generate content based on the given title using the configured prompt template.
        
        Args:
            title (str): The title to generate content for
            model (str, optional): Override default model
            
        Returns:
            str: Generated content from the AI model
        """
        formatted_messages = self.prompt.replace("{title}", title)
        
        response = self.client.get_completion(
            messages=[{"role": "user", "content": formatted_messages}]
        )
        
        return response
        
    def generate_content_Gemini(self, title: str, model: str = None) -> str:

        fullPrompt = self.prompt.replace("{title}", title)
        response = self.chat.send_message(fullPrompt)
        return response

# if __name__ == "__main__":
#     content_agent = ContentAgent()
    
#     # Generate content for a sample title
#     title = "What if dinosaurs ruled cities in 2025?"
#     # generated_content = content_agent.generate_content_DeepSeek(title)
#     # if generated_content is None:
#     #     generated_content = content_agent.generate_content_Gemini(title)
#     generated_content = content_agent.generate_content_Gemini(title)

#     print(f"Generated Content for '{title}':")
#     print(generated_content)