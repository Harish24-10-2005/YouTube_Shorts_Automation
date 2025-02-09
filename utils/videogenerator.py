import json
import os
import re
from typing import Dict, List, Optional, Tuple

from config.config import Config
from Agents.contentAgent import ContentAgent
from Agents.imageGeneration import ImageGenerator
from Agents.scriptsAgent import ScriptAgent
from Agents.voiceGeneration import VoiceGenerator
from Agents.bgMusicAgent import VideoMusicSynchronizer
from Agents.captionAgent import transcribe_and_caption
from Agents.editAgent import VideoEditor
from utils.utils import DirectoryManager

class VideoGenerator:
    def __init__(self, config: Config,video_mode: bool = False):
        self.content_agent = ContentAgent()
        self.script_agent = ScriptAgent()
        self.voice_generator = VoiceGenerator()
        self.image_generator = ImageGenerator(api_keys=config.huggingface_api_keys,video_mode=video_mode)
        self.video_editor = VideoEditor(video_mode=video_mode)
        self.directory_manager = DirectoryManager()
        
    def _parse_script_output(self, script_output: str) -> Tuple[List[str], List[str]]:
        """Parse the script output to extract voice scripts and image prompts"""
        pattern = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
        match = pattern.search(script_output)
        if not match:
            raise ValueError("No JSON block found in the generated script.")
        
        try:
            data = json.loads(match.group(1))
            return data.get("voice_scripts", []), data.get("image_prompts", [])
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")

    def generate_video(self,
                      title: str,
                      channel: str = None,
                      video_mode:bool = False,
                      custom_content: Optional[str] = None,
                      custom_voice_scripts: Optional[str] = None,
                      custom_image_prompts: Optional[str] = None,
                      include_caption: bool = False,
                      custom_bg_music_path: Optional[str] = None) -> str:
        """
        Generate a complete video with the given parameters
        Returns the path to the final video
        # """
        self.directory_manager.clear_directories([
            "output",
            os.path.join("assets", "images"),
            os.path.join("assets", "VoiceScripts")
        ])
        if channel == "motivation":
            if video_mode:
                print("video mode")
                content = custom_content if custom_content else self.content_agent.generate_content_Gemini(title,channel="motivation",video_mode=True)
            else:
                content = custom_content if custom_content else self.content_agent.generate_content_Gemini(title,channel="motivation")
        else:
            content = custom_content if custom_content else self.content_agent.generate_content_Gemini(title)
        
        if custom_voice_scripts and custom_image_prompts:
            voice_scripts = [line.strip() for line in custom_voice_scripts.splitlines() if line.strip()]
            image_prompts = [line.strip() for line in custom_image_prompts.splitlines() if line.strip()]
            if channel != "motivation":
                if len(image_prompts) != 2 * len(voice_scripts):
                    raise ValueError("Number of image prompts must be exactly twice the number of voice scripts")
        else:
            script_output = self.script_agent.generate_Scripts_Gemini(content, channel=channel,video_mode=video_mode)
            voice_scripts, image_prompts = self._parse_script_output(script_output)
        print(script_output)
        print(len(voice_scripts))
        print("=============================================")
        print(len(image_prompts))
        image_output_dir = os.path.join("assets", "images")
        self.directory_manager.ensure_directories_exist([image_output_dir])
        self.image_generator.generate_all_images(image_prompts)
        
        voice_output_dir = os.path.join("assets", "VoiceScripts")
        self.directory_manager.ensure_directories_exist([voice_output_dir])
        voice_results = self.voice_generator.generate_multiple_voices(voice_scripts)
        
        for sentence, filepath in voice_results.items():
            print(f"\nSentence: {sentence}")
            print(f"Generated file: {filepath}")
        output_path = os.path.join("output", "youtube_shorts.mp4")
        self.video_editor.create_final_video(
            image_dir=image_output_dir,
            voice_dir=voice_output_dir,
            output_path=output_path,
            video_mode=video_mode,
            channel=channel
        )
        
        if include_caption:
            transcribe_and_caption(output_path)
        if channel == "motivation":
            if video_mode:
                bg_music_path = custom_bg_music_path or os.path.join("assets", "Bg_Music", "video_motivational.mp3")
            else:
                bg_music_path = custom_bg_music_path or os.path.join("assets", "Bg_Music","shorts_motivational.mp3")
        else:
            bg_music_path = custom_bg_music_path or os.path.join("assets", "Bg_Music", "clockbackgrounf.mp3")
        music_synchronizer = VideoMusicSynchronizer(bg_music_path)
        final_video_path = music_synchronizer.sync_music_to_video(output_path)
        
        return final_video_path