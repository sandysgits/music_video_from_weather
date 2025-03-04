import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import io

# Import project-specific functions
from functions.video_funcs_1 import generate_weather_animation, read_station_data, load_weather_and_image_data
from functions.my_midiutil import MIDIFile
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number
from functions.make_midi import produce_midi_file
from functions.download import download_files, load_and_combine_data, data_main
from functions.midi_to_wav_prettymidi import midi_to_wav
from functions.merge_video_audio import merge_video_audio


# ---------------------------
# Configuration & Parameters
# ---------------------------
BASE_DIR = Path(__file__).parent
print('Base directory is:', BASE_DIR)
WEATHER_DATA_DIR = BASE_DIR / "weatherdata"
WEBCAM_DATA_DIR = WEATHER_DATA_DIR / "webcam_data"
AUDIO_OUTPUT_DIR = BASE_DIR / "assets/audio"
VIDEO_OUTPUT_DIR = BASE_DIR / "assets/video"
FINAL_OUTPUT_DIR = BASE_DIR / "final_output"

# Define input weather data file
#WEATHER_FILE = WEATHER_DATA_DIR / "produkt_zehn_min_tu_20230828_20250227_07431.txt"
WEATHER_FILE = WEATHER_DATA_DIR / "merged_weather_data_20230831_0000_20250227_2350.txt"

# Define processing timeframe
START_DATETIME = pd.to_datetime("2025-02-17 00:00")
END_DATETIME = pd.to_datetime("2025-02-17 19:00")

# Formatting time strings for filenames
START_DATETIME_STR = START_DATETIME.strftime('%Y-%m-%d_%H-%M')
END_DATETIME_STR = END_DATETIME.strftime('%Y-%m-%d_%H-%M')

# Calculate 10-minute intervals
INTERVALS = int((END_DATETIME - START_DATETIME).total_seconds() / 600)

# Define audio processing parameters
BPM = 180
FPS = BPM / 60
VEL_MIN = 30  # Minimum volume
VEL_MAX = 70  # Maximum volume
INSTRUMENTS = ['violin', 'viola', 'cello', 'contrabass', 'seashore']
#INSTRUMENTS = ['cello', 'violin', 'cello', 'viola', 'seashore']

# Define output filenames
VIDEO_OUTPUT_FILE = VIDEO_OUTPUT_DIR/ f"video_{START_DATETIME_STR}_{END_DATETIME_STR}_{FPS}.mp4"
MIDI_OUTPUT_FILE = AUDIO_OUTPUT_DIR/ f"audio_{START_DATETIME_STR}_{END_DATETIME_STR}_{BPM}.mid"
FINAL_VIDEO_OUTPUT_FILE = FINAL_OUTPUT_DIR / f"final_video_audio_{START_DATETIME_STR}_{END_DATETIME_STR}_{BPM}.mp4"
AUDIO_OUTPUT_FILE = AUDIO_OUTPUT_DIR / f"audio_{START_DATETIME_STR}_{END_DATETIME_STR}_{BPM}.wav"

# ---------------------------
# Data Loading
# ---------------------------
print("Loading weather data...")
df = read_station_data(str(WEATHER_FILE))
image_df, full_weather_data = load_weather_and_image_data(WEBCAM_DATA_DIR, df, START_DATETIME, END_DATETIME)
print("Weather data loaded successfully.")

# ---------------------------
# Generate Weather Animation
# ---------------------------
print("Generating weather animation...")
#generate_weather_animation(image_df, full_weather_data, WEBCAM_DATA_DIR, VIDEO_OUTPUT_FILE, INTERVALS, FPS)
print("Weather animation created successfully.")

# ---------------------------
# Generate MIDI from Weather Data
# ---------------------------
print("Processing weather data for MIDI conversion...")
full_weather_data.loc[:, 'PP_10'] = full_weather_data['PP_10'].replace(-999, 1015)
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
#merge_video_audio(str(VIDEO_INPUT_PATH), str(AUDIO_INPUT_PATH), FINAL_VIDEO_OUTPUT_FILE)
print(f"Final video created: {FINAL_VIDEO_OUTPUT_FILE}")
