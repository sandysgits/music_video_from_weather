from src.functions.video_funcs import read_station_data
from pathlib import Path
import subprocess
import os

#####################################################################################
# --- Function to merge video and audio files ---
# This function uses FFmpeg to merge an MP4 video file with a WAV audio file.
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

#####################################################################################
# --- Function to merge weather data ---
def merge_station_data(station_id, mode):
    BASE_DIR = Path.cwd()
    print('Base directory is:', BASE_DIR)

    if mode == 'now':
      WEATHER_DATA_DIR = BASE_DIR / "weatherdata" / f"{station_id}_now"
    elif mode == 'historic':
      WEATHER_DATA_DIR = BASE_DIR / "weatherdata" / f"{station_id}_historic"

    if mode == 'now':
    # Find the latest available weather data files
      WEATHER_FILE_TEMP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_tu_*_{station_id}.txt"))[-1]
      WEATHER_FILE_WIND = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_ff_*_{station_id}.txt"))[-1]
      WEATHER_FILE_PRECIP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_rr_*_{station_id}.txt"))[-1]
    elif mode == 'historic':
      WEATHER_FILE_TEMP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_tu_*_{station_id}.txt"))[-1]
      WEATHER_FILE_WIND = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_ff_*_{station_id}.txt"))[-1]
      WEATHER_FILE_PRECIP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_rr_*_{station_id}.txt"))[-1]
    
  # Read the data
    print("Loading weather data...")
    df_temp = read_station_data(str(WEATHER_FILE_TEMP))
    df_wind = read_station_data(str(WEATHER_FILE_WIND))
    df_precip = read_station_data(str(WEATHER_FILE_PRECIP))

    # Merge only on common 'MESS_DATUM' values
    common_dates = set(df_temp['MESS_DATUM']) & set(df_wind['MESS_DATUM']) & set(df_precip['MESS_DATUM'])

    # Filter each dataframe to include only rows with common 'MESS_DATUM'
    df_temp_filtered = df_temp[df_temp['MESS_DATUM'].isin(common_dates)]
    df_wind_filtered = df_wind[df_wind['MESS_DATUM'].isin(common_dates)]
    df_precip_filtered = df_precip[df_precip['MESS_DATUM'].isin(common_dates)]

    # Perform inner merge on 'MESS_DATUM'
    df_merged = df_temp_filtered.merge(df_wind_filtered, on='MESS_DATUM', how='inner', suffixes=('', '_wind'))
    df_merged = df_merged.merge(df_precip_filtered, on='MESS_DATUM', how='inner', suffixes=('', '_precip'))

    # Remove duplicate 'STATIONS_ID' columns if present
    df_merged = df_merged.loc[:, ~df_merged.columns.duplicated()]

    # Determine the first and last timestamp for the filename and format them
    start_time = df_merged['MESS_DATUM'].iloc[0].strftime('%Y%m%d_%H%M')
    end_time = df_merged['MESS_DATUM'].iloc[-1].strftime('%Y%m%d_%H%M')
    merged_file_path = WEATHER_DATA_DIR / f"merged_weather_data_{start_time}_{end_time}_{station_id}.txt"

    df_merged.to_csv(merged_file_path, sep=';', index=False)
    print(f"Merged weather data saved at: {merged_file_path}")

    return df_merged, merged_file_path
