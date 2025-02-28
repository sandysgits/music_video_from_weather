import subprocess
import os

def merge_video_audio(video_file, audio_file, output_file):
    """Merge an MP4 video with a WAV audio file using FFmpeg via subprocess."""
    
    # Check if the files exist
    if not os.path.exists(video_file):
        print(f"Error: Video file '{video_file}' not found.")
        return
    if not os.path.exists(audio_file):
        print(f"Error: Audio file '{audio_file}' not found.")
        return

    # FFmpeg command to merge audio and video
    command = [
        "ffmpeg",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",  # Copy video stream without re-encoding
        "-c:a", "aac",    # Convert audio to AAC (compatible with MP4)
        "-b:a", "192k",   # Set audio bitrate
        "-strict", "experimental", 
        output_file
    ]

    try:
        # Run the command
        subprocess.run(command, check=True)
        print(f"Successfully merged {video_file} and {audio_file} into {output_file}")
    
    except subprocess.CalledProcessError as e:
        print("FFmpeg failed:", e)

video_path = "C:/Users/Frank/Documents/python/weather_webcam_sonification/2025-02-18_00-00_animation1.mp4"
audio_path = "C:/Users/Frank/Documents/python/weather_webcam_sonification/weather_audio.wav"
# Example usage
merge_video_audio(video_path, audio_path, "video_and_audio.mp4")
