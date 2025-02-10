import os
import json
import subprocess
from typing import Dict, Optional

class VideoMusicSynchronizer:
    def __init__(self, music_path: str, cache_file: str = 'music_sync_cache.json'):
        self.music_path = music_path
        self.cache_file = cache_file
        self.music_sync_cache: Dict[str, Dict[str, float]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, float]]:
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.music_sync_cache, f)

    def get_video_duration(self, video_path: str) -> float:
        try:
            result = subprocess.run([
                'ffprobe', 
                '-v', 'error', 
                '-show_entries', 'format=duration', 
                '-of', 'default=noprint_wrappers=1:nokey=1', 
                video_path
            ], capture_output=True, text=True)
            return float(result.stdout.strip())
        except Exception as e:
            print(f"Error getting video duration: {e}")
            return 0

    def sync_music_to_video(self, video_path: str, output_path: Optional[str] = None) -> str:
        # Get video duration
        video_duration = self.get_video_duration(video_path)
        
        # Determine music start point from cache or reset
        video_key = os.path.basename(video_path)
        if video_key not in self.music_sync_cache:
            self.music_sync_cache[video_key] = {'last_music_start': 0}
        
        # Get last music start point
        last_music_start = self.music_sync_cache[video_key]['last_music_start']
        
        # Calculate music start and end points
        music_start = last_music_start
        music_end = music_start + video_duration
        
        # Prepare output path
        if output_path is None:
            output_path = "output/youtube_with_music.mp4"
        
        # FFmpeg command to mix audio with volume adjustments
        try:
            subprocess.run([
                'ffmpeg', 
            '-i', video_path, 
            '-i', self.music_path, 
            '-filter_complex', 
            f'[1:a]atrim=0:{self.get_video_duration(video_path)},asetpts=PTS-STARTPTS[music],' + 
            '[0:a]volume=10.0[original_loud],' + 
            '[music]volume=1.0[music_low],' + 
            '[original_loud][music_low]amix=inputs=2:duration=first[aout]', 
            '-map', '0:v',  
            '-map', '[aout]',  
            '-c:v', 'copy',  
            '-c:a', 'aac', 
            '-shortest', # Ensure output matches shortest input
                output_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error syncing music: {e}")
            return video_path
        
        # Update cache with new music start point
        self.music_sync_cache[video_key]['last_music_start'] = music_end
        self._save_cache()
        
        return output_path


if __name__ == '__main__':
    synchronizer = VideoMusicSynchronizer('assets\Bg_Music\clockbackgrounf.mp3')
    output_video = synchronizer.sync_music_to_video('D:\AI_AGENT_FOR_YOUTUBE\Shorts_Agent\youtube_shorts.mp4')
    print(f"Video with synced music created: {output_video}")