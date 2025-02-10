import whisper
import subprocess
import os
from datetime import timedelta

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format"""
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() // 60) % 60)
    secs = int(td.total_seconds() % 60)
    milliseconds = int(round((td.total_seconds() - int(td.total_seconds())) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def transcribe_and_caption(video_path, output_path="output.srt", model_name="base", offset=0.1):
    """
    Transcribe video and create caption file with word-level timestamps.
    A small offset (in seconds) is added to each word's end timestamp for better sync.
    Then, burn glowing captions into the video.
    """
    try:
        # Load the Whisper model
        print(f"Loading {model_name} model...")
        model = whisper.load_model(model_name)
        
        # Transcribe the video with word-level timestamps
        print("Transcribing video...")
        result = model.transcribe(video_path, word_timestamps=True)
        
        # Process segments and write SRT file
        print("Generating captions...")
        srt_index = 1
        with open(output_path, "w", encoding="utf-8") as srt_file:
            for segment in result["segments"]:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"].strip()
                
                if "words" in segment:
                    for word_info in segment["words"]:
                        word_start = word_info["start"]
                        word_end = word_info["end"]
                        word_text = word_info["word"].strip()
                        
                        # Adjust the end time by adding an offset
                        word_end_adjusted = min(word_end + offset, end_time)
                        
                        # Write SRT entry for each word
                        srt_file.write(f"{srt_index}\n")
                        srt_file.write(f"{format_timestamp(word_start)} --> {format_timestamp(word_end_adjusted)}\n")
                        srt_file.write(f"{word_text}\n\n")
                        srt_index += 1
                else:
                    # Fallback if word-level timestamps are not available.
                    srt_file.write(f"{srt_index}\n")
                    srt_file.write(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n")
                    srt_file.write(f"{text}\n\n")
                    srt_index += 1
        
        # Get video dimensions using ffprobe
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0", video_path
        ]
        dimensions = subprocess.check_output(probe_cmd, universal_newlines=True).strip()
        width, height = map(int, dimensions.split('x'))
        
        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_video = os.path.join(output_dir, "output_with_glowing_captions.mp4")
        bottom_padding = 50  # Vertical margin for captions
        
        # Calculate font size proportional to video height
        font_size = int(height * 0.007)
        
        # Build FFmpeg command using filter_complex to create a glowing subtitle effect:
        ffmpeg_command = [
            "ffmpeg", "-i", video_path,
            "-vf", (
                f"subtitles={output_path}:force_style='"
                f"Alignment=2,"                # Center alignment
                f"FontName=Impact,"            # Bold font
                f"FontSize={int(height * 0.04)}," # Font size (4% of video height)
                f"PrimaryColour=&H00FFD700&,"  # Gold color (BGR: 00 D7 FF)
                f"OutlineColour=&H60FFD700&,"  # Semi-transparent gold outline
                f"Shadow=0,"                   # No shadow
                f"BorderStyle=1,"              # Outline only
                f"Outline=3,"                  # Thicker outline for glow effect
                f"MarginV={bottom_padding}'"   # Bottom margin
            ),
            "-c:v", "libx264", 
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            output_video
        ]

        
        print("Adding glowing captions to video...")
        subprocess.run(ffmpeg_command, check=True)
        
        print(f"Process completed! Captioned video saved as {output_video}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

# # Example usage:
# video_file = r"D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\output\motiv_shorts.mp4"
# transcribe_and_caption(video_file)
