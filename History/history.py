import pandas as pd
from datetime import datetime
import os
import streamlit as st

class VideoHistoryTracker:
    def __init__(self):
        self.history_file = "History\Video_generation_history.xlsx"
        self.columns = [
            "DateTime", 
            "Title", 
            "Channel",
            "Content",
            "Voice Scripts",
            "Image Prompts"
        ]
        self._initialize_history_file()

    def _initialize_history_file(self):
        """Initialize the history Excel file if it doesn't exist"""
        if not os.path.exists(self.history_file):
            df = pd.DataFrame(columns=self.columns)
            df.to_excel(self.history_file, index=False)

    def add_entry(self, title, channel, content=None, voice_scripts=None, image_prompts=None):
        """Add a new entry to the history"""
        try:
            df = pd.read_excel(self.history_file)
            
            new_entry = {
                "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Title": title,
                "Channel": channel,
                "Content": content if content else "Default content used",
                "Voice Scripts": voice_scripts if voice_scripts else "Default scripts used",
                "Image Prompts": image_prompts if image_prompts else "Default prompts used"
            }
            
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_excel(self.history_file, index=False)
            return True
        except Exception as e:
            print(f"Error adding history entry: {str(e)}")
            return False

    def get_history(self):
        """Retrieve the generation history"""
        try:
            if os.path.exists(self.history_file):
                return pd.read_excel(self.history_file)
            return pd.DataFrame(columns=self.columns)
        except Exception as e:
            print(f"Error reading history: {str(e)}")
            return pd.DataFrame(columns=self.columns)

def display_history_table():
    """Display the video generation history in Streamlit"""
    tracker = VideoHistoryTracker()
    history_df = tracker.get_history()
    
    if not history_df.empty:
        st.header("Video Generation History")
        
        # Add search functionality
        search_term = st.text_input("Search in history:", "")
        if search_term:
            mask = history_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            filtered_df = history_df[mask]
        else:
            filtered_df = history_df
            
        sort_column = st.selectbox("Sort by:", history_df.columns.tolist())
        sort_order = st.radio("Sort order:", ("Ascending", "Descending"))
        
        filtered_df = filtered_df.sort_values(
            by=sort_column, 
            ascending=(sort_order == "Ascending")
        )
        
        st.dataframe(
            filtered_df,
            column_config={
                "DateTime": st.column_config.DatetimeColumn(
                    "Date & Time",
                    format="DD/MM/YYYY HH:mm:ss"
                ),
                "Content": st.column_config.TextColumn(
                    "Content",
                    width="large",
                    help="Video content/script"
                ),
                "Voice Scripts": st.column_config.TextColumn(
                    "Voice Scripts",
                    width="large"
                ),
                "Image Prompts": st.column_config.TextColumn(
                    "Image Prompts",
                    width="large"
                )
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No video generation history available yet.")

