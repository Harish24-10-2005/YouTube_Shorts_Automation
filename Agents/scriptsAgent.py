from phi.agent import Agent
from phi.tools import tool
import json
import os
from dotenv import load_dotenv
from prompt.prompt import SCRIPT_PROMPT
from config.deepseekConfig import OpenRouterClient
import google.generativeai as genai
from config.geminiConfig import GeminiChat
from .contentAgent import ContentAgent
import re 
load_dotenv()

class ScriptAgent:
    def __init__(self, **kwargs):
        """
        Initialize the Content Agent with OpenRouter client and content prompt.
        """
        load_dotenv()
        # self.client = OpenRouterClient(
        #     api_key=os.getenv("OPENROUTER_API_KEY"),
        # )
        self.chat = GeminiChat(api_key=None)
        self.prompt = SCRIPT_PROMPT  

    def generate_Script_DeepSeek(self, content: str, model: str = None) -> str:
        """
        Generate content based on the given title using the configured prompt template.
        
        Args:
            title (str): The title to generate content for
            model (str, optional): Override default model
            
        Returns:
            str: Generated content from the AI model
        """
        formatted_messages = self.prompt.replace("{content}", content)
        
        response = self.client.get_completion(
            messages=[{"role": "user", "content": formatted_messages}]
        )
        
        return response
        
    def generate_Scripts_Gemini(self, content: str, model: str = None) -> str:

        fullPrompt = self.prompt.replace("{content}", content)
        response = self.chat.send_message(fullPrompt)
        return response

# if __name__ == "__main__":
#     content_agent = ContentAgent()
#     script_agent = ScriptAgent()
#     title = "What if dinosaurs ruled cities in 2025?"
#     # generated_content = content_agent.generate_content_DeepSeek(title)
#     # if generated_content is None:
#     #     generated_content = content_agent.generate_content_Gemini(title)
#     generated_content = content_agent.generate_content_Gemini(title)
#     script = script_agent.generate_Scripts_Gemini(generated_content)
#     print(script)
#     pattern = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
#     match = pattern.search(script)

#     if match:
#         # Extract the JSON string
#         json_str = match.group(1)
#         try:
#             # Parse the JSON string into a Python dictionary
#             data = json.loads(json_str)
#             # Now data is a Python dictionary containing voice_scripts and image_prompts
#             print("Parsed JSON:")
#             print(json.dumps(data, indent=4))
#         except json.JSONDecodeError as e:
#             print("Error decoding JSON:", e)
#     else:
#         print("No JSON block found in the provided string.")
    
#     voice_scripts = data.get("voice_scripts", [])
#     image_prompts = data.get("image_prompts", [])
#     print(voice_scripts[0])
#     print("=============================================")
#     print(image_prompts[0])