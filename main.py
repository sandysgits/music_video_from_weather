# --- USER CONFIGURATION ---
from pathlib import Path
import pandas as pd
import shutil
import os
from src.functions.video_funcs import *
from src.packages.my_midiutil import MIDIFile
from src.functions.soni_functions import *
from src.functions.make_midi import *
from src.functions.midi_to_wav_prettymidi import *
from src.functions.merge import *
from src.functions.download_new import *

def create_music_video_from_weather():
    print("Hello from weather-webcam-sonification! Let's create some music video from the weather!")
    # --- USER CONFIGURATION ---
    # --- Please specify the settings you want ---
    station_id =  "01420"      # Choose the weather station you want to use, e.g. "07341", "01420", ... 
    mode       = "historic"         # You can eather get a long run with "historic" or todays data with "now"
    station    = "Offenbach-W" # Choose the webcam station you want to use, e.g. "Offenbach-O", "Offenbach-W", ...

    bpm = 420  # beats per minute for MIDI # choose BPM that can be divided by 60 !
    fps = int(bpm / 60)
    instruments = ['xylophone', 'acoustic grand piano', 'xylophone', 'contrabass', 'seashore']
    vel_min = 30
    vel_max = 127 #70 # max is 127
    resolution = "400"  # options: 114, 1200, 180, 1920, 400, 640, 816

    if mode == 'historic':
        # Define processing timeframe for "historic" mode
        # only works for 01420 + Offenbach-O or Offenbach-W between 20250301_0930 and 20250307_1400
        start_datetime = pd.to_datetime("2025-03-01 09:30") 
        end_datetime = pd.to_datetime("2025-03-02 09:10")


# ----- CONFIGURATION END ---

    # --- PATH SETUP ---
    BASE_DIR = Path.cwd()
    WEATHER_DATA_DIR = BASE_DIR / "weatherdata" / f"{station_id}_{mode}"
    # if mode == 'now':
        # shutil.rmtree(WEATHER_DATA_DIR, ignore_errors=True)
    WEATHER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    WEBCAM_DATA_DIR = WEATHER_DATA_DIR / f"webcam_data/{station}"
    AUDIO_OUTPUT_DIR = BASE_DIR / "assets/audio"
    VIDEO_OUTPUT_DIR = BASE_DIR / "assets/video"
    FINAL_OUTPUT_DIR = BASE_DIR / "final_output"

    for path in [WEBCAM_DATA_DIR, AUDIO_OUTPUT_DIR, VIDEO_OUTPUT_DIR, FINAL_OUTPUT_DIR]:
        os.makedirs(path, exist_ok=True)

    if mode == 'now':
        # --- DOWNLOAD WEBCAM DATA ---
        download_webcam_images_now(station,resolution,WEBCAM_DATA_DIR)
        # TODO: only download the data that does not exist, only for the current day, for which weatherdata exists too

        # --- DOWNLOAD WEATHER DATA ---
        download_station_data_now(station_id, WEATHER_DATA_DIR)

        # --- MERGE WEATHER DATA ---
        print("Merging latest station data...")
        df_merged, merged_file_path = merge_station_data(station_id, mode)

        # --- PREPARE TIME RANGE ---
        start_datetime = df_merged['MESS_DATUM'].iloc[0]
        end_datetime = df_merged['MESS_DATUM'].iloc[-1]



    if mode == 'historic':

        # Webcam  data in database

        # --- DOWNLOAD WEATHER DATA ---
        download_station_data_historic(station_id, WEATHER_DATA_DIR)

        # --- MERGE WEATHER DATA ---
        print("Merging latest station data...")
        df_merged, merged_file_path = merge_station_data(station_id, mode)

            # todo find the file  most recently created file, that starts with 'merged'
        historic_weather_data_path = list(WEATHER_DATA_DIR.glob("merged*.txt"))[0] #  / "merged_weather_data_20230920_0000_20250322_2350_01420.txt"

        df_merged = read_station_data(historic_weather_data_path)





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
    midi = produce_midi_file(full_weather_data, bpm, vel_min, vel_max, instruments)
    with open(audio_path, "wb") as output_file:
        midi.writeFile(output_file)
    print(f"MIDI saved to: {audio_path}")

    # --- CONVERT MIDI TO WAV ---
    print("Converting MIDI to WAV...")
    midi_to_wav(str(audio_path), BASE_DIR / "assets/weather_audio.wav")

    # --- MERGE VIDEO AND AUDIO ---
    final_output_path = FINAL_OUTPUT_DIR / f"{station}_{station_id}_{start_str}_{end_str}_{bpm}_{mode}.mp4"
    merge_video_audio(str(output_filename), BASE_DIR / "assets/weather_audio.wav", str(final_output_path))
    print(f"Final video with audio saved to: {final_output_path}")

if __name__ == "__main__":
    create_music_video_from_weather()