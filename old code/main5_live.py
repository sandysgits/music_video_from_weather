

# In this Version all the data is downloaded live first and the video is created from the live available data

# Download webcam data

import requests
import numpy as np
import os
from pathlib import Path

from functions.download_new import download_webcam_images_now, download_station_data_now

import importlib
import functions.video_funcs_1
importlib.reload(functions.video_funcs_1)

from functions.video_funcs_1 import generate_weather_animation, read_station_data, load_weather_and_image_data
from functions.make_midi_5 import produce_midi_file
from functions.midi_to_wav_prettymidi import midi_to_wav
from functions.merge_video_audio import merge_video_audio



from functions.merge_weather_data import *
res = "400" # possible resolutions: 114, 1200, 180, 1920, 400, 640, 816, ful

# define which stations to download
stations = ["Offenbach-O"]
BASE_DIR = Path("C:/Users/Frank/Documents/python/weather_webcam_sonification/")
WEATHER_DATA_DIR = BASE_DIR / "weatherdata"
WEBCAM_DATA_DIR = WEATHER_DATA_DIR / "webcam_data" / f"{stations[0]}"

download_webcam_images_now(stations,res,WEBCAM_DATA_DIR)


# Download station data
station_id = '07341'
output_path = WEATHER_DATA_DIR / f"{station_id}_now"
download_station_data_now(station_id, output_path)

# merge station data
df_merged, merged_file_path = merge_latest_station_data(station_id,'now')

# define the paths
AUDIO_OUTPUT_DIR = BASE_DIR / "assets/audio"
VIDEO_OUTPUT_DIR = BASE_DIR / "assets/video"
FINAL_OUTPUT_DIR = BASE_DIR / "final_output"

# Define processing timeframe
START_DATETIME = df_merged['MESS_DATUM'].iloc[0]
END_DATETIME = df_merged['MESS_DATUM'].iloc[-1]

# Formatting time strings for filenames
START_DATETIME_STR = START_DATETIME.strftime('%Y-%m-%d_%H-%M')
END_DATETIME_STR = END_DATETIME.strftime('%Y-%m-%d_%H-%M')

# Calculate 10-minute intervals
INTERVALS = int((END_DATETIME - START_DATETIME).total_seconds() / 600)

# Define audio processing parameters
BPM = 180
FPS = int(BPM / 60)
VEL_MIN = 30  # Minimum volume
VEL_MAX = 70  # Maximum volume
#INSTRUMENTS = ['violin', 'viola', 'cello', 'contrabass', 'seashore']
INSTRUMENTS = ['cello', 'violin', 'cello', 'viola', 'seashore']

# Define output filenames
VIDEO_OUTPUT_FILE = VIDEO_OUTPUT_DIR/ f"video_{START_DATETIME_STR}_{END_DATETIME_STR}_{FPS}fps.mp4"
MIDI_OUTPUT_FILE = AUDIO_OUTPUT_DIR/ f"audio_{START_DATETIME_STR}_{END_DATETIME_STR}_{BPM}.mid"
FINAL_VIDEO_OUTPUT_FILE = FINAL_OUTPUT_DIR / f"final_video_audio_{START_DATETIME_STR}_{END_DATETIME_STR}_{BPM}.mp4"
AUDIO_OUTPUT_FILE = AUDIO_OUTPUT_DIR / f"audio_{START_DATETIME_STR}_{END_DATETIME_STR}_{BPM}.wav"

# ---------------------------
# Data Loading
# ---------------------------
print("Loading weather data...")
df = read_station_data(str(merged_file_path))
image_df, full_weather_data = load_weather_and_image_data(WEBCAM_DATA_DIR, df, START_DATETIME, END_DATETIME)
print("Weather data loaded successfully.")

# ---------------------------
# Generate Weather Animation
# ---------------------------
print("Generating weather animation...")
generate_weather_animation(stations[0],image_df, full_weather_data, WEBCAM_DATA_DIR, VIDEO_OUTPUT_FILE, INTERVALS, FPS)
print("Weather animation created successfully.")






#################################################
# ---------------------------
# Generate MIDI from Weather Data
# ---------------------------
print("Processing weather data for MIDI conversion...")
#full_weather_data.loc[:, 'PP_10'] = full_weather_data['PP_10'].replace(-999, 1015)
print("Generating MIDI file...")
midi = produce_midi_file(full_weather_data, BPM, VEL_MIN, VEL_MAX, INSTRUMENTS)

# Save MIDI file

with open(MIDI_OUTPUT_FILE, "wb") as output_file:
    midi.writeFile(output_file)
print(f"MIDI file saved: {MIDI_OUTPUT_FILE}")

# ---------------------------
# Convert MIDI to WAV
# ---------------------------
print("Converting MIDI to WAV...")
midi_to_wav(str(MIDI_OUTPUT_FILE), AUDIO_OUTPUT_FILE)
print("MIDI converted to WAV successfully.")

# ---------------------------
# Merge Audio with Video
# ---------------------------
VIDEO_INPUT_PATH = BASE_DIR / VIDEO_OUTPUT_FILE
AUDIO_INPUT_PATH = BASE_DIR / AUDIO_OUTPUT_FILE

print("Merging video and audio...")
merge_video_audio(str(VIDEO_INPUT_PATH), str(AUDIO_INPUT_PATH), FINAL_VIDEO_OUTPUT_FILE)
print(f"Final video created: {FINAL_VIDEO_OUTPUT_FILE}")
