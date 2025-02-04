from phi.agent import Agent
from phi.tools import tool
import json
import os
from dotenv import load_dotenv
from Agents.bgMusicAgent import VideoMusicSynchronizer
from Agents.captionAgent import transcribe_and_caption
from Agents.editAgent import VideoEditor
from prompt.prompt import SCRIPT_PROMPT
from config.deepseekConfig import OpenRouterClient
import google.generativeai as genai
from  config.geminiConfig import GeminiChat
from Agents.contentAgent import ContentAgent
from Agents.imageGeneration import ImageGenerator
from Agents.scriptsAgent import ScriptAgent
from Agents.voiceGeneration import VoiceScriptGenerator
import re 
import shutil


load_dotenv()

HuggingFace_API_Key = os.getenv("HUGGING_FACE") 
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

content_agent = ContentAgent()
script_agent = ScriptAgent()


# Define the directories to delete contents from
directories_to_delete_contents = [
    r"D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\output",
    r"D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\assets\images",
    r"D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\assets\voiceScripts"
]

# Loop through each directory and delete its contents
for directory in directories_to_delete_contents:
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print(f"Deleted contents of {directory}")
    except Exception as e:
        print(f"Error deleting contents of {directory}: {e}")
print("=============================================deleted contents===============================================")
title = "What if dinosaurs present in 2025?"
print("==============================================generate content===============================================")
generated_content = content_agent.generate_content_Gemini(title)
script = script_agent.generate_Scripts_Gemini(generated_content)
pattern = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
match = pattern.search(script)
if match:
    json_str = match.group(1)
    try:
        data = json.loads(json_str)
        print("Parsed JSON:")
        print(json.dumps(data, indent=4))
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
else:
    print("No JSON block found in the provided string.")

voice_scripts = data.get("voice_scripts", [])
image_prompts = data.get("image_prompts", [])

print("==============================================generate images===============================================")

# HuggingFace_API_Key = os.getenv("HUGGING_FACE") 
generator = ImageGenerator(api_key=HuggingFace_API_Key)
generator.generate_images(image_prompts)

print("==============================================generate voices===============================================")

# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
generator = VoiceScriptGenerator(DEEPGRAM_API_KEY)
responses = generator.generate_voices_from_list(voice_scripts)
for response in responses:
    print(response.to_json(indent=4))

print("==============================================edit video===============================================")

try:
    editor = VideoEditor()
    editor.create_final_video(
        image_dir='images',
        voice_dir='voicescripts',
        output_path='output/youtube_shorts.mp4'
    )
except ValueError as e:
    print(f"Error: {e}")
    print("\nPlease ensure you have:")
    print("- Exactly twice as many images as voice scripts")
    print("- All images in the 'images' folder")
    print("- All voice scripts in the 'voicescripts' folder")
except Exception as e:
    print(f"An error occurred: {e}")

print("==============================================transcribe and caption===============================================")

video_file = r"D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\output\youtube_shorts.mp4"  
transcribe_and_caption(video_file)

print("==============================================sync music===============================================")
synchronizer = VideoMusicSynchronizer('D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\assets\Bg_Music\clockbackgrounf.mp3')
output_video = synchronizer.sync_music_to_video('D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\output\output_with_captions.mp4')
print(f"Video with synced music created: {output_video}")

