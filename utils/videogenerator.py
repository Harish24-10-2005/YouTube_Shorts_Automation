import datetime
import json
import os
import re
import shutil
from typing import Dict, List, Optional, Tuple
from PIL import Image
from config.config import Config
from Agents.contentAgent import ContentAgent
from Agents.imageGeneration import ImageGenerator
from Agents.scriptsAgent import ScriptAgent
from Agents.voiceGeneration import VoiceGenerator
from Agents.bgMusicAgent import VideoMusicSynchronizer
from Agents.captionAgent import transcribe_and_caption
from Agents.editAgent import VideoEditor
from utils.utils import DirectoryManager
import streamlit as st
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

    @staticmethod
    def move_files_to_ai_images(src_dirs: List[str], channel: str = "motivation") -> None:
        """
        Moves all files from each directory in `src_dirs` into a destination folder 
        structure as follows:
        
        AI_Youtube_backUp
        ├── motivation (or any provided channel name)
        │   ├── <timestamp_folder1>
        │   │   ├── file1
        │   │   ├── file2
        │   │   └── ...
        │   └── <timestamp_folder2>
        │       ├── file3
        │       ├── file4
        │       └── ...
        └── ChonoshiftChronicles (if used as a channel)
            ├── <timestamp_folder1>
            │   ├── file5
            │   └── ...
            └── <timestamp_folder2>
                ├── file6
                └── ...
        
        For each source directory, a new timestamp-named subfolder is created under the
        channel folder inside "AI_Youtube_backUp", and all files from that source directory
        are moved there.
        
        Args:
            src_dirs: List of source directory paths to move files from.
            channel: Channel name used as the destination subfolder under "AI_Youtube_backUp"
                     (default is "motivation").
        """
        # Define the root backup folder and the channel folder within it.
        root_dir = "AI_Youtube_backUp"
        dest_channel_dir = os.path.join(root_dir, channel)
        
        # Create the channel folder (and root folder) if it doesn't exist.
        if not os.path.exists(dest_channel_dir):
            os.makedirs(dest_channel_dir)
        
        # Process each source directory separately.
        for src_dir in src_dirs:
            if os.path.exists(src_dir):
                # Create a unique timestamp folder for this batch of files.
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                dest_subfolder = os.path.join(dest_channel_dir, timestamp)
                os.makedirs(dest_subfolder, exist_ok=True)
                
                # Move every file from the current source directory to the timestamp folder.
                for file_name in os.listdir(src_dir):
                    src_file = os.path.join(src_dir, file_name)
                    if os.path.isfile(src_file):
                        dest_file = os.path.join(dest_subfolder, file_name)
                        shutil.move(src_file, dest_file)
                        print(f"Moved: {src_file} -> {dest_file}")
            else:
                print(f"Source directory not found: {src_dir}")


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
            os.path.join("assets", "VoiceScripts")
        ])

        directories_to_move = [
            "output",
            os.path.join("assets", "images")
        ]
        self.move_files_to_ai_images(src_dirs=directories_to_move,channel=channel)
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
        # This part of the code is responsible for generating voice scripts and image prompts based on
        # the content provided. Here's a breakdown of what it does:
            script_output = self.script_agent.generate_Scripts_Gemini(content, channel=channel,video_mode=video_mode)
            voice_scripts, image_prompts = self._parse_script_output(script_output)
        st.header("Voice Scripts")
        with st.container():
            st.markdown("""
                <style>
                .script-box {
                    background-color: #1D2951;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                }
                </style>
            """, unsafe_allow_html=True)
            
            if isinstance(voice_scripts, list):
                for idx, script in enumerate(voice_scripts, start=1):
                    with st.container():
                        st.markdown(f"""
                            <div class="script-box">
                                <b>Script {idx}</b><br>
                                {script}
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="script-box">
                        {voice_scripts}
                    </div>
                """, unsafe_allow_html=True)

        # Image Prompts Section
        st.header("Image Prompts")
        with st.container():
            if isinstance(image_prompts, list):
                for idx, prompt in enumerate(image_prompts, start=1):
                    with st.container():
                        st.markdown(f"""
                            <div class="script-box">
                                <b>Prompt {idx}</b><br>
                                {prompt}
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="script-box">
                        {image_prompts}
                    </div>
                """, unsafe_allow_html=True)


        print(script_output)
        print(len(voice_scripts))
        print("=============================================")
        print(len(image_prompts))
        image_output_dir = os.path.join("assets", "images")
        self.directory_manager.ensure_directories_exist([image_output_dir])
        self.image_generator.generate_all_images(image_prompts)
        
        voice_output_dir = os.path.join("assets", "VoiceScripts")
        self.directory_manager.ensure_directories_exist([voice_output_dir])
        if channel == "motivation":
            self.voice_generator = VoiceGenerator(channel="motivation")
        else: 
            self.voice_generator = VoiceGenerator(channel="ChronoShift_Chronicles")
        voice_results = self.voice_generator.generate_multiple_voices(voice_scripts)


        st.sidebar.header("Generated Images")
        supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        image_files = [
            file for file in os.listdir(image_output_dir)
            if file.lower().endswith(supported_formats)
        ]

        if image_files:
            for image_file in image_files:
                image_path = os.path.join(image_output_dir, image_file)
                # Open the image file using PIL
                image = Image.open(image_path)
                # Display the image in the sidebar with its filename as caption
                st.sidebar.image(image, caption=image_file, use_container_width=True)
        else:
            st.sidebar.write("No images found.")
        print("==============================================edit video===============================================")
        
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
        self.history_tracker.add_entry(
            title=title,
            channel=channel,
            content=content,
            voice_scripts=voice_scripts,
            image_prompts=image_prompts
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