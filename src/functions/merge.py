from src.functions.video_funcs import read_station_data
from pathlib import Path
import subprocess
import os
import pandas as pd

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


def merge_station_data(station_id,BASE_DIR, mode):


    WEATHER_DATA_DIR = BASE_DIR / "weatherdata" / f"{station_id}_now"


    # === Get file paths ===
    # NOW
    WEATHER_FILE_TEMP_now = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_tu_*_{station_id}.txt"))[-1]
    WEATHER_FILE_WIND_now = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_ff_*_{station_id}.txt"))[-1]
    WEATHER_FILE_PRECIP_now = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_rr_*_{station_id}.txt"))[-1]

    # RECENT
    WEATHER_FILE_TEMP_recent = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_tu_*_{station_id}.txt"))[-1]
    WEATHER_FILE_WIND_recent = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_ff_*_{station_id}.txt"))[-1]
    WEATHER_FILE_PRECIP_recent = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_rr_*_{station_id}.txt"))[-1]

    # === Read data ===
    print("Loading weather data...")
    df_temp_now = read_station_data(str(WEATHER_FILE_TEMP_now))
    df_wind_now = read_station_data(str(WEATHER_FILE_WIND_now))
    df_precip_now = read_station_data(str(WEATHER_FILE_PRECIP_now))

    df_temp_recent = read_station_data(str(WEATHER_FILE_TEMP_recent))
    df_wind_recent = read_station_data(str(WEATHER_FILE_WIND_recent))
    df_precip_recent = read_station_data(str(WEATHER_FILE_PRECIP_recent))
    print('df_precip_recent', df_precip_recent.head())

    # === Ensure consistent datetime format in all MESS_DATUM columns ===
    for df in [df_temp_now, df_wind_now, df_precip_now,
            df_temp_recent, df_wind_recent, df_precip_recent]:
        df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format="%Y%m%d %H%M", errors='coerce')
    
    print('df_precip_recent fixed?', df_precip_recent.head())

    # === Merge NOW data ===
    common_dates_now = set(df_temp_now['MESS_DATUM']) & set(df_wind_now['MESS_DATUM']) & set(df_precip_now['MESS_DATUM'])

    df_temp_filtered_now = df_temp_now[df_temp_now['MESS_DATUM'].isin(common_dates_now)]
    df_wind_filtered_now = df_wind_now[df_wind_now['MESS_DATUM'].isin(common_dates_now)]
    df_precip_filtered_now = df_precip_now[df_precip_now['MESS_DATUM'].isin(common_dates_now)]

    df_merged_now = df_temp_filtered_now.merge(df_wind_filtered_now, on='MESS_DATUM', how='inner', suffixes=('', '_wind'))
    df_merged_now = df_merged_now.merge(df_precip_filtered_now, on='MESS_DATUM', how='inner', suffixes=('', '_precip'))
    df_merged_now = df_merged_now.loc[:, ~df_merged_now.columns.duplicated()]

    start_time_now = df_merged_now['MESS_DATUM'].iloc[0].strftime('%Y%m%d_%H%M')
    end_time_now = df_merged_now['MESS_DATUM'].iloc[-1].strftime('%Y%m%d_%H%M')
    merged_file_path_now = WEATHER_DATA_DIR / f"merged_weather_data_{start_time_now}_{end_time_now}_{station_id}.txt"
    df_merged_now.to_csv(merged_file_path_now, sep=';', index=False)

    # === Merge RECENT data ===
    common_dates_recent = set(df_temp_recent['MESS_DATUM']) & set(df_wind_recent['MESS_DATUM']) & set(df_precip_recent['MESS_DATUM'])

    df_temp_filtered_recent = df_temp_recent[df_temp_recent['MESS_DATUM'].isin(common_dates_recent)]
    df_wind_filtered_recent = df_wind_recent[df_wind_recent['MESS_DATUM'].isin(common_dates_recent)]
    df_precip_filtered_recent = df_precip_recent[df_precip_recent['MESS_DATUM'].isin(common_dates_recent)]

    df_merged_recent = df_temp_filtered_recent.merge(df_wind_filtered_recent, on='MESS_DATUM', how='inner', suffixes=('', '_wind'))
    df_merged_recent = df_merged_recent.merge(df_precip_filtered_recent, on='MESS_DATUM', how='inner', suffixes=('', '_precip'))
    df_merged_recent = df_merged_recent.loc[:, ~df_merged_recent.columns.duplicated()]

    start_time_recent = df_merged_recent['MESS_DATUM'].iloc[0].strftime('%Y%m%d_%H%M')
    end_time_recent = df_merged_recent['MESS_DATUM'].iloc[-1].strftime('%Y%m%d_%H%M')
    merged_file_path_recent = WEATHER_DATA_DIR / f"merged_weather_data_{start_time_recent}_{end_time_recent}_{station_id}.txt"
    df_merged_recent.to_csv(merged_file_path_recent, sep=';', index=False)

    # === Merge BOTH dataframes into one along the datetime axis ===
    df_merged_all = pd.concat([df_merged_recent, df_merged_now])
    #df_merged_all = df_merged_all.sort_values(by='MESS_DATUM').reset_index(drop=True)
    print(df_merged_now.shape)
    print(df_merged_recent.shape)
    print(df_merged_all.shape)
    start_time_all = df_merged_all['MESS_DATUM'].iloc[0].strftime('%Y%m%d_%H%M')
    end_time_all = df_merged_all['MESS_DATUM'].iloc[-1].strftime('%Y%m%d_%H%M')
    merged_file_path_all = WEATHER_DATA_DIR / f"{station_id}_merged_full_{start_time_all}_{end_time_all}.txt"
    
    df_merged_all.to_csv(merged_file_path_all, sep=';', index=False)
  
    print("✅ Weather data merged and saved for both 'now' and 'recent'.")

    return df_merged_all, merged_file_path_all
