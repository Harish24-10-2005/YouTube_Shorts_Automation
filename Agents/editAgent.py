import os
import subprocess
from PIL import Image
from pydub import AudioSegment
import shutil
import tempfile

class VideoEditor:
    def __init__(self,video_mode: bool = False):
        self.temp_dir = tempfile.mkdtemp()
        if video_mode:
            self.width = 1920  # YouTube video width
            self.height = 1080  # YouTube video height
        else:
            self.width = 1080  # YouTube Shorts width (portrait)
            self.height = 1920 # YouTube Shorts height
        
    def validate_files(self, image_dir, voice_dir,video_mode: bool = False, channel: str = None):
        """Validate that we have the correct number of files and maintain folder order"""
        # List files matching the extensions
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        voice_files = [f for f in os.listdir(voice_dir) if f.lower().endswith(('.mp3', '.wav'))]

        # Sort files by creation time so that the order in the folder is preserved
        image_files.sort(key=lambda f: os.path.getctime(os.path.join(image_dir, f)))
        voice_files.sort(key=lambda f: os.path.getctime(os.path.join(voice_dir, f)))
        if channel == "motivation":
            if video_mode:
                if len(image_files) != 3 * len(voice_files):
                    raise ValueError(f"Number of images ({len(image_files)}) must be exactly 10")
            else:
                if len(image_files) != 5 * len(voice_files):
                    raise ValueError(f"Number of images ({len(image_files)}) must be exactly 2")
        else:
            if len(image_files) != 2 * len(voice_files):
                raise ValueError(f"Number of images ({len(image_files)}) must be exactly double the number of voice files ({len(voice_files)})")
        
        return image_files, voice_files

    def get_audio_duration(self, audio_path):
        """Get duration of audio file in seconds"""
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0

    def resize_image(self, image_path, output_path):
        """Resize image to fit YouTube Shorts dimensions"""
        with Image.open(image_path) as img:
            # Calculate new dimensions maintaining aspect ratio
            ratio = min(self.width / img.width, self.height / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            
            # Resize image
            resized = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Create new image with black background
            new_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            
            # Paste resized image in center
            x = (self.width - new_size[0]) // 2
            y = (self.height - new_size[1]) // 2
            new_img.paste(resized, (x, y))
            
            new_img.save(output_path, 'PNG')

    def create_video_segment(self, image_path, duration, output_path, effect_type="zoom"):
        """Create video segment with zoom/pan effect"""
        # Resize image first
        temp_img_path = os.path.join(self.temp_dir, 'temp_resized.png')
        self.resize_image(image_path, temp_img_path)
        
        # Define filter based on effect type
        if effect_type == "zoom":
            filter_complex = (
                f"[0:v]scale={self.width}:{self.height},"
                f"zoompan=z='if(lte(zoom,1.0),1.1,max(1.001,zoom-0.0015))':"
                f"d={int(duration*30)}:s={self.width}x{self.height}[v]"
            )
        elif effect_type == "slide":
            filter_complex = (
                f"[0:v]scale={self.width}:{self.height},"
                f"crop={self.width}:{self.height}:x='(iw-{self.width})*t/{duration}':y=0,"
                f"pad={self.width}:{self.height}:(ow-iw)/2:(oh-ih)/2[v]"
            )
        elif effect_type == "fade":
            # This example creates a fade-in effect over the first 1 second.
            filter_complex = (
                f"[0:v]scale={self.width}:{self.height},fade=t=in:st=0:d=1[v]"
            )

        else:  # pan effect
            filter_complex = (
                f"[0:v]scale={self.width}:{self.height},"
                f"crop={self.width}:{self.height}:"
                f"iw/2-(iw/2)*sin(t/5):"
                f"ih/2-(ih/2)*sin(t/7)[v]"
            )

        zoom_cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', temp_img_path,
            '-t', str(duration),
            '-filter_complex', filter_complex,
            '-map', '[v]',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'medium',
            output_path
        ]
        
        subprocess.run(zoom_cmd, check=True)

    def create_final_video(self, image_dir, voice_dir,output_path , video_mode = False, channel: str = None):
        """Create final video with all segments"""
        # Validate and get files maintaining folder order
        image_files, voice_files = self.validate_files(image_dir, voice_dir,video_mode = video_mode, channel = channel)
        segments = []
        
        # Process each voice script with its two corresponding images
        for voice_idx, voice_file in enumerate(voice_files):
            print(f"Processing voice script {voice_idx + 1}/{len(voice_files)}")
            
            voice_path = os.path.join(voice_dir, voice_file)
            voice_duration = self.get_audio_duration(voice_path)
            image_duration = voice_duration / 2
            
            if channel == "motivation":
                if video_mode:
                    # For video mode: 3 images per voice
                    image_duration = voice_duration / 3
                    image_segments = []
                    for j in range(3):
                        img_idx = voice_idx * 3 + j
                        image_path = os.path.join(image_dir, image_files[img_idx])
                        temp_segment = os.path.join(self.temp_dir, f'temp_segment_{img_idx}.mp4')
                        
                        # Alternate between zoom and pan effects
                        effect_type = "zoom" if j % 2 == 0 else "fade"
                        self.create_video_segment(image_path, image_duration, temp_segment, effect_type)
                        image_segments.append(temp_segment)
                        
                else:
                    # For non-video mode: 5 images per voice
                    image_duration = voice_duration / 5
                    image_segments = []
                    for j in range(5):
                        img_idx = voice_idx * 5 + j
                        image_path = os.path.join(image_dir, image_files[img_idx])
                        temp_segment = os.path.join(self.temp_dir, f'temp_segment_{img_idx}.mp4')
                        
                        # Alternate between zoom and pan effects
                        effect_type = "fade" if j % 2 == 0 else "zoom"
                        self.create_video_segment(image_path, image_duration, temp_segment, effect_type)
                        image_segments.append(temp_segment)
            else:        
                img1_idx = voice_idx * 2
                img2_idx = voice_idx * 2 + 1
                
                # Create segments for both images
                image_segments = []
                for i, img_idx in enumerate([img1_idx, img2_idx]):
                    image_path = os.path.join(image_dir, image_files[img_idx])
                    temp_segment = os.path.join(self.temp_dir, f'temp_segment_{img_idx}.mp4')
                    
                    # Alternate between zoom and pan effects
                    effect_type = "fade" if i % 2 == 0 else "zoom"
                    self.create_video_segment(image_path, image_duration, temp_segment, effect_type)
                    image_segments.append(temp_segment)
                
            # Concatenate two image segments
            segment_list = os.path.join(self.temp_dir, f'segment_list_{voice_idx}.txt')
            with open(segment_list, 'w') as f:
                for seg in image_segments:
                    f.write(f"file '{seg}'\n")
            
            segment_video = os.path.join(self.temp_dir, f'segment_{voice_idx}.mp4')
            subprocess.run([
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', segment_list,
                '-c', 'copy',
                segment_video
            ], check=True)
            
            # Add audio to segment
            final_segment = os.path.join(self.temp_dir, f'final_segment_{voice_idx}.mp4')
            subprocess.run([
                'ffmpeg', '-y',
                '-i', segment_video,
                '-i', voice_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                final_segment
            ], check=True)
            
            segments.append(final_segment)
            
            # Add gap after each segment except the last one
            if voice_idx < len(voice_files) - 1:
                gap_path = os.path.join(self.temp_dir, f'gap_{voice_idx}.mp4')
                self.create_gap(gap_path)
                segments.append(gap_path)
            
            print(f"Completed voice script {voice_idx + 1}/{len(voice_files)}")
        
        # Create final concat file
        final_concat = os.path.join(self.temp_dir, 'final_concat.txt')
        with open(final_concat, 'w') as f:
            for segment in segments:
                f.write(f"file '{segment}'\n")
        
        print("Creating final video...")
        subprocess.run([
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', final_concat,
            '-c', 'copy',
            output_path
        ], check=True)
        
        # Cleanup temporary directory
        shutil.rmtree(self.temp_dir)
        print("Video creation completed!")

    def create_gap(self, output_path):
        """Create a short (20-millisecond) black gap"""
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'color=c=black:s={self.width}x{self.height}:d=0.01',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        subprocess.run(cmd, check=True)

def main():
    try:
        editor = VideoEditor(video_mode=True)
        editor.create_final_video(
            image_dir='assets/images',
            voice_dir='assets/VoiceScripts',
            output_path='youtube_shorts.mp4',
            video_mode=False,
            channel=None
        )
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease ensure you have:")
        print("- Exactly twice as many images as voice scripts")
        print("- All images in the 'images' folder")
        print("- All voice scripts in the 'VoiceScripts' folder")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
