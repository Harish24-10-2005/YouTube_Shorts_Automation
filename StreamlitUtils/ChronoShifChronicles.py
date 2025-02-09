import os
from typing import Dict
import streamlit as st

from config.config import Config
from utils.videogenerator import VideoGenerator
from config.config import Config
from Agents.contentAgent import ContentAgent
from Agents.imageGeneration import ImageGenerator
from Agents.scriptsAgent import ScriptAgent
from Agents.voiceGeneration import VoiceGenerator
from Agents.bgMusicAgent import VideoMusicSynchronizer
from Agents.captionAgent import transcribe_and_caption
from Agents.editAgent import VideoEditor
from utils.utils import DirectoryManager

class StreamlitInterface:
    def __init__(self):
        self.config = Config()
        self.video_generator = VideoGenerator(self.config)
        
    def setup_page(self):
        # st.set_page_config(page_title="AI-Powered YouTube Shorts Generator", layout="wide")
        ChronoShiftChronicles = "assets\logo\chronoShift_chronicles.jpg"
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(ChronoShiftChronicles, width=60)
        with col2:
            st.title("ChronoShift Chronicles")
        st.markdown("Generate engaging and Mysterious YouTube Shorts with a few clicks!")
        
    def setup_sidebar(self) -> Dict:
        st.sidebar.header("Input Options")
        
        inputs = {
            "title": st.sidebar.text_input(
                "Video Title",
                value="What If the Black Hole's Silent Scream Reveals the Universe's Darkest Secret?"
            ),
            "use_custom_content": st.sidebar.checkbox("Provide custom content?", value=False),
            "custom_content": None,
            "use_custom_scripts": st.sidebar.checkbox("Provide custom voice scripts & image prompts", value=False),
            "custom_voice_scripts": None,
            "custom_image_prompts": None,
            "include_caption": st.sidebar.checkbox("Include captioning", value=False),
            "use_custom_bg_music": st.sidebar.checkbox("Provide custom background music?", value=False),
            "custom_bg_music_file": None
        }
        
        if inputs["use_custom_content"]:
            inputs["custom_content"] = st.sidebar.text_area("Enter your custom content:")
            
        if inputs["use_custom_scripts"]:
            st.sidebar.markdown("**Voice Scripts (one per line):**")
            inputs["custom_voice_scripts"] = st.sidebar.text_area("Enter voice scripts:")
            st.sidebar.markdown("**Image Prompts (one per line, must be exactly twice the number of voice scripts):**")
            inputs["custom_image_prompts"] = st.sidebar.text_area("Enter image prompts:")
            
        if inputs["use_custom_bg_music"]:
            inputs["custom_bg_music_file"] = st.sidebar.file_uploader(
                "Upload background music (mp3/wav)",
                type=["mp3", "wav"]
            )
            
        return inputs
        
    def run(self):
        self.setup_page()
        inputs = self.setup_sidebar()
        
        if st.button("Generate Video"):
            try:
                with st.spinner("Generating video..."):
                    custom_bg_music_path = None
                    if inputs["use_custom_bg_music"] and inputs["custom_bg_music_file"]:
                        custom_bg_music_path = os.path.join("assets", "Bg_Music", "custom_bg_music.mp3")
                        os.makedirs(os.path.dirname(custom_bg_music_path), exist_ok=True)
                        with open(custom_bg_music_path, "wb") as f:
                            f.write(inputs["custom_bg_music_file"].getbuffer())
                    
                    # Generate video
                    final_video_path = self.video_generator.generate_video(
                        title=inputs["title"],
                        custom_content=inputs["custom_content"],
                        custom_voice_scripts=inputs["custom_voice_scripts"],
                        custom_image_prompts=inputs["custom_image_prompts"],
                        include_caption=inputs["include_caption"],
                        custom_bg_music_path=custom_bg_music_path
                    )
                    
                    # Display final video
                    st.header("Final Video")
                    if os.path.exists(final_video_path):
                        with open(final_video_path, "rb") as video_file:
                            video_bytes = video_file.read()
                            st.video(video_bytes)
                    else:
                        st.error("Final video file not found!")
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = StreamlitInterface()
    app.run()