import whisper
import subprocess
import os
from datetime import timedelta

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format"""
    td = timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds // 60) % 60
    seconds = td.seconds % 60
    milliseconds = round(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def transcribe_and_caption(video_path, output_path="output.srt", model_name="base"):
    """
    Transcribe video and create caption file with small text segments synchronized using word-level timestamps.
    """
    try:
        # Load the Whisper model
        print(f"Loading {model_name} model...")
        model = whisper.load_model(model_name)
        
        # Transcribe the video with word-level timestamps
        print("Transcribing video...")
        result = model.transcribe(video_path, word_timestamps=True)
        
        # Process segments
        print("Generating captions...")
        srt_index = 1
        with open(output_path, "w", encoding="utf-8") as srt_file:
            for segment in result["segments"]:
                # Get timing and text
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"].strip()
                
                # Use word-level timestamps if available
                if "words" in segment:
                    for word_info in segment["words"]:
                        word_start = word_info["start"]
                        word_end = word_info["end"]
                        word_text = word_info["word"].strip()
                        
                        # Write SRT entry for each word
                        srt_file.write(f"{srt_index}\n")
                        srt_file.write(f"{format_timestamp(word_start)} --> {format_timestamp(word_end)}\n")
                        srt_file.write(f"{word_text}\n\n")
                        srt_index += 1
                else:
                    # Fallback to segment-level timestamps if word-level timestamps are not available
                    srt_file.write(f"{srt_index}\n")
                    srt_file.write(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n")
                    srt_file.write(f"{text}\n\n")
                    srt_index += 1
        
        # Get video dimensions
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0", video_path
        ]
        dimensions = subprocess.check_output(probe_cmd, universal_newlines=True).strip()
        width, height = map(int, dimensions.split('x'))
        
        # Burn subtitles into video
        output_video = "output\output_with_captions.mp4"
        bottom_padding = 20
        ffmpeg_command = [
            "ffmpeg", "-i", video_path,
            "-vf", f"subtitles={output_path}:force_style='"
                   f"Alignment=2,"  # Center alignment at the bottom
                   f"FontName=Roboto,"  # Modern font
                   f"FontSize={int(height * 0.007)},"  # Larger font size (7% of video height)
                   f"PrimaryColour=&HFFD700&,"  # Gold text color for mystery
                   f"OutlineColour=&H000000&,"  # Black outline for contrast
                   f"BorderStyle=3,"  # Outline style
                   f"Outline=3,"  # Thicker outline
                   f"MarginV={bottom_padding},"  # Vertical margin from the bottom
                   f"BackColour=&H40000000&'" , # Semi-transparent black background
            "-c:v", "libx264",  # Re-encode video to ensure compatibility
            "-preset", "fast",  # Faster encoding speed
            "-crf", "23",       # Standard quality
            "-c:a", "aac",      # Re-encode audio to AAC (compatible with MP4)
            "-b:a", "128k",     # Set audio bitrate
            output_video
        ]
        
        print("Adding captions to video...")
        subprocess.run(ffmpeg_command)
        
        print(f"Process completed! Captioned video saved as {output_video}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

# if __name__ == "__main__":
#     video_file = r"D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\output\youtube_shorts.mp4"  # Replace with your video path
#     transcribe_and_caption(video_file)