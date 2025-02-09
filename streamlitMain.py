import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Adjust the import paths as needed
from StreamlitUtils.ChronoShifChronicles import StreamlitInterface
from StreamlitUtils.motivAition import StreamlitInterfaceMotivAition

st.set_page_config(page_title="AI-Powered YouTube Video Generator", layout="wide")

def load_image(url, width=None):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def main():
    # Initialize session state for storing the user's generator selection.
    if 'generator_choice' not in st.session_state:
        st.session_state.generator_choice = None

  

    col1, col2 = st.sidebar.columns(2)
    youtube_logo_url = "https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png"  #:contentReference[oaicite:0]{index=0}
    shorts_logo_url = "https://upload.wikimedia.org/wikipedia/commons/f/fc/Youtube_shorts_icon.svg" # :contentReference[oaicite:1]{index=1}

    with col1:
        st.image(youtube_logo_url, width=60)
    st.sidebar.title("Choose a Channel")
    if st.sidebar.button("ChronoShif Chronicles"):
        st.session_state.generator_choice = "YouTube Shorts Generator"

    st.sidebar.markdown("---")
    
    if st.sidebar.button("MotivAition Channel"):
        st.session_state.generator_choice = "Motivational Video Generator"

    # Load the selected interface based on session state.
    if st.session_state.generator_choice == "YouTube Shorts Generator":
        app = StreamlitInterface()
        app.run()
    elif st.session_state.generator_choice == "Motivational Video Generator":
        app = StreamlitInterfaceMotivAition()
        app.run()
    else:
        st.write("Please select a video generator option from the sidebar.")

if __name__ == "__main__":
    main()
