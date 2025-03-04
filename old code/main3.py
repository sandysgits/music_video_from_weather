import os
from pathlib import Path
import pandas as pd
from functions.video_funcs_1 import generate_weather_animation, read_station_data, load_weather_and_image_data

# Get the absolute path of the directory where main.py is located
base_dir = Path(__file__).parent
print(base_dir)

# Construct the file path relative to main.py
#file_path = base_dir / "weatherdata" / "produkt_zehn_now_tu_20250219_20250219_07431.txt"
file_path = base_dir / "weatherdata" / "produkt_zehn_min_tu_20230828_20250227_07431.txt"
webcam_path = base_dir / "weatherdata/webcam_data/" 

# Read the data using the fixed path
df = read_station_data(str(file_path))


start_datetime = pd.to_datetime("2025-02-17 01:00")
end_datetime = pd.to_datetime("2025-02-19 14:00")

start_datetime_str = start_datetime.strftime('%Y-%m-%d_%H-%M')
end_datetime_str = end_datetime.strftime('%Y-%m-%d_%H-%M')

# Calculate total minutes difference
intervals = int((end_datetime - start_datetime).total_seconds() / 60 / 10)
#print(intervals)



image_df, full_weather_data = load_weather_and_image_data(webcam_path, df, start_datetime, end_datetime)
output_filename = f"{start_datetime_str}_animation1.mp4"

print('data was read')
generate_weather_animation(image_df, full_weather_data, webcam_path, output_filename , frames = intervals)
print('video was created')
#print(full_weather_data)

###############################
""" 
""" 
from functions.my_midiutil import MIDIFile  # Example library for MIDI
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number
from functions.make_midi_4 import produce_midi_file
from functions.download import download_files, load_and_combine_data, data_main
import io
import json
import pandas as pd
from datetime import datetime


#start_date = "2025-02-17"
#end_date   = "2025-02-19"
#
bpm = 180
 # Create MIDI
audio_file = f"output_{start_datetime_str}_{end_datetime_str}_{bpm}.mid"
# Lade die Datei
#file_path = f"./weatherdata/produkt_zehn_now_tu_20250219_20250219_07431.txt"


#start_time = datetime.strptime(start_date, '%Y-%m-%d')
#end_time = datetime.strptime(end_date, '%Y-%m-%d')

#data = pd.read_csv(file_path, sep=';', skipinitialspace=True)
data = full_weather_data
#data['PP_10'] = data['PP_10'].replace(-999, 1015) #fix the missing pressure data so it can still produce a midi file
data.loc[:, 'PP_10'] = data['PP_10'].replace(-999, 1015)

print("Data loaded.")

vel_min = 30 # minimal Volume
vel_max = 70 # max. volume

# Choose your instruments:
instruments = ['violin', 'viola', 'cello', 'contrabass', 'seashore']

# Erstelle Midi file aus den Daten:
midi= produce_midi_file(data, bpm,  vel_min, vel_max, instruments)
print("Midi produced.")

with open(f"./assets/audio/{audio_file}", "wb") as output_file:
       midi.writeFile(output_file)

# Create an in-memory buffer
print("Write midi to {audio_file}")
midi_buffer = io.BytesIO()

# Write the MIDI data to the buffer
midi.writeFile(midi_buffer)

# Get the binary data from the buffer
midi_data = midi_buffer.getvalue()

from functions.midi_to_wav_prettymidi import midi_to_wav

base_dir = Path(__file__).parent
file_path_midi = base_dir / "assets/audio/" / audio_file
print(file_path_midi)
# Convert MIDI to WAV
midi_to_wav(str(file_path_midi), "weather_audio.wav")
# read the midi data """ """


## merge audio and video
from functions.merge_video_audio import merge_video_audio
video_path = "C:/Users/Frank/Documents/python/weather_webcam_sonification/"+ output_filename
audio_path = "C:/Users/Frank/Documents/python/weather_webcam_sonification/weather_audio.wav"

output_vid_aud_fname = f"final_video_{start_datetime_str}_{end_datetime_str}_{bpm}.mp4"
merge_video_audio(video_path, audio_path, output_vid_aud_fname)