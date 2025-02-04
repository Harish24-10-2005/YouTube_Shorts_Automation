import os
import subprocess
from PIL import Image
from pydub import AudioSegment
import shutil
import tempfile

class VideoEditor:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.width = 1080  # YouTube Shorts width
        self.height = 1920  # YouTube Shorts height
        
    def validate_files(self, image_dir, voice_dir):
        """Validate that we have correct number of files"""
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        voice_files = [f for f in os.listdir(voice_dir) if f.lower().endswith(('.mp3', '.wav'))]
        
        if len(image_files) != 2 * len(voice_files):
            raise ValueError(f"Number of images ({len(image_files)}) must be exactly double the number of voice files ({len(voice_files)})")
        
        return sorted(image_files), sorted(voice_files)

    def get_audio_duration(self, audio_path):
        """Get duration of audio file in seconds"""
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0

    def resize_image(self, image_path, output_path):
        """Resize image to fit YouTube Shorts dimensions"""
        with Image.open(image_path) as img:
            # Calculate new dimensions maintaining aspect ratio
            ratio = min(self.width/img.width, self.height/img.height)
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
            filter_complex = f'[0:v]scale={self.width}:{self.height},zoompan=z=\'if(lte(zoom,1.0),1.1,max(1.001,zoom-0.0015))\':d={int(duration*30)}:s={self.width}x{self.height}[v]'
        else:  # pan effect
            filter_complex = f'[0:v]scale={self.width}:{self.height},crop={self.width}:{self.height}:\'iw/2-(iw/2)*sin(t/5)\':\'ih/2-(ih/2)*sin(t/7)\'[v]'

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

    def create_final_video(self, image_dir, voice_dir, output_path):
        """Create final video with all segments"""
        # Validate and get sorted files
        image_files, voice_files = self.validate_files(image_dir, voice_dir)
        segments = []
        
        # Process each voice script with its two corresponding images
        for voice_idx, voice_file in enumerate(voice_files):
            print(f"Processing voice script {voice_idx + 1}/{len(voice_files)}")
            
            voice_path = os.path.join(voice_dir, voice_file)
            voice_duration = self.get_audio_duration(voice_path)
            image_duration = voice_duration / 2
            
            # Get the two corresponding images
            img1_idx = voice_idx * 2
            img2_idx = voice_idx * 2 + 1
            
            # Create segments for both images
            image_segments = []
            for i, img_idx in enumerate([img1_idx, img2_idx]):
                image_path = os.path.join(image_dir, image_files[img_idx])
                temp_segment = os.path.join(self.temp_dir, f'temp_segment_{img_idx}.mp4')
                
                # Alternate between zoom and pan effects
                effect_type = "zoom" if i % 2 == 0 else "pan"
                self.create_video_segment(image_path, image_duration, temp_segment, effect_type)
                image_segments.append(temp_segment)
            
            # Concatenate two image segments
            segment_list = os.path.join(self.temp_dir, f'segment_list_{voice_idx}.txt')
            with open(segment_list, 'w') as f:
                for seg in image_segments:
                    f.write(f"file '{seg}'\n")
            
            # Create combined video segment
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
            
            # Add 1-second gap after each segment (except last)
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
        
        # Concatenate all segments into final video
        print("Creating final video...")
        subprocess.run([
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', final_concat,
            '-c', 'copy',
            output_path
        ], check=True)
        
        # Cleanup
        shutil.rmtree(self.temp_dir)
        print("Video creation completed!")

    def create_gap(self, output_path):
        """Create 1-second black gap with fade transition"""
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'color=c=black:s={self.width}x{self.height}:d=1',
            '-vf', 'fade=in:0:5,fade=out:25:5',  # Add fade in/out effect
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        subprocess.run(cmd, check=True)

# def main():
#     try:
#         editor = VideoEditor()
#         editor.create_final_video(
#             image_dir='images',
#             voice_dir='voicescripts',
#             output_path='youtube_shorts.mp4'
#         )
#     except ValueError as e:
#         print(f"Error: {e}")
#         print("\nPlease ensure you have:")
#         print("- Exactly twice as many images as voice scripts")
#         print("- All images in the 'images' folder")
#         print("- All voice scripts in the 'voicescripts' folder")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()