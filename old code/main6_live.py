# --- USER CONFIGURATION ---
from pathlib import Path

station_id = "07341"
mode = "now"  # or "historic"
bpm = 180  # beats per minute for MIDI
fps = int(bpm / 60)
instruments = ['violin', 'viola', 'cello', 'contrabass', 'seashore']
vel_min = 30
vel_max = 70
station = "Offenbach-O"
resolution = "400"  # options: 114, 1200, 180, 1920, 400, 640, 816, ful

# --- PATH SETUP ---
from functions.video_funcs_1 import generate_weather_animation, read_station_data, load_weather_and_image_data
from functions.my_midiutil import MIDIFile
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number
from functions.make_midi_5 import produce_midi_file
from functions.download import download_files, load_and_combine_data, data_main
from functions.midi_to_wav_prettymidi import midi_to_wav
from functions.merge_video_audio import merge_video_audio
from functions.merge_weather_data import merge_latest_station_data
from functions.download_new import download_webcam_images_now, download_station_data_now
import pandas as pd
import io

BASE_DIR = Path("C:/Users/Frank/Documents/python/weather_webcam_sonification/")
WEATHER_DATA_DIR = BASE_DIR / "weatherdata" / f"{station_id}_{mode}"
WEBCAM_DATA_DIR = WEATHER_DATA_DIR / "webcam_data"
AUDIO_OUTPUT_DIR = BASE_DIR / "assets/audio"
VIDEO_OUTPUT_DIR = BASE_DIR / "assets/video"
FINAL_OUTPUT_DIR = BASE_DIR / "final_output"


if mode == 'now':
    # --- DOWNLOAD WEBCAM DATA ---
    download_webcam_images_now(station,resolution,WEBCAM_DATA_DIR)

    # --- DOWNLOAD WEATHER DATA ---
    download_station_data_now(station_id, WEATHER_DATA_DIR)


# --- MERGE WEATHER DATA ---
print("Merging latest station data...")
df_merged, merged_file_path = merge_latest_station_data(station_id, mode)

# --- PREPARE TIME RANGE ---
start_datetime = df_merged['MESS_DATUM'].iloc[0]
end_datetime = df_merged['MESS_DATUM'].iloc[-1]
start_str = start_datetime.strftime('%Y-%m-%d_%H-%M')
end_str = end_datetime.strftime('%Y-%m-%d_%H-%M')
intervals = int((end_datetime - start_datetime).total_seconds() / 600)

# --- LOAD IMAGE DATA ---
print("Loading image and weather data for video...")
image_df, full_weather_data = load_weather_and_image_data(WEBCAM_DATA_DIR, df_merged, start_datetime, end_datetime)
frames = len(image_df)

# --- GENERATE WEATHER VIDEO ---
output_filename = VIDEO_OUTPUT_DIR / f"{start_str}_to_{end_str}_animation.mp4"
print("Generating weather animation video...")
generate_weather_animation(station, image_df, full_weather_data, WEBCAM_DATA_DIR, output_filename,intervals, fps)
print(f"Video saved to: {output_filename}")

# --- GENERATE MIDI ---
audio_filename = f"output_{start_str}_{end_str}_{bpm}.mid"
audio_path = AUDIO_OUTPUT_DIR / audio_filename
print("Generating MIDI file...")
midi = produce_midi_file(df_merged, bpm, vel_min, vel_max, instruments)
with open(audio_path, "wb") as output_file:
    midi.writeFile(output_file)
print(f"MIDI saved to: {audio_path}")

# --- CONVERT MIDI TO WAV ---
print("Converting MIDI to WAV...")
midi_to_wav(str(audio_path), "weather_audio.wav")

# --- MERGE VIDEO AND AUDIO ---
final_output_path = FINAL_OUTPUT_DIR / f"final_video_audio_{start_str}_{end_str}_{bpm}bpm.mp4"
merge_video_audio(str(output_filename), "weather_audio.wav", str(final_output_path))
print(f"Final video with audio saved to: {final_output_path}")
