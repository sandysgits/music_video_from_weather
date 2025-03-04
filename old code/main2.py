import os
from pathlib import Path
from functions.video_funcs import generate_weather_animation, read_station_data

# Get the absolute path of the directory where main.py is located
base_dir = Path(__file__).parent
print(base_dir)

# Construct the file path relative to main.py
#file_path = base_dir / "weatherdata" / "produkt_zehn_now_tu_20250219_20250219_07431.txt"
file_path = base_dir / "weatherdata" / "produkt_zehn_min_tu_20230828_20250227_07431.txt"
webcam_path = base_dir / "weatherdata/webcam_data/" 

# Read the data using the fixed path
df = read_station_data(str(file_path))
print('data was read')
generate_weather_animation(df, webcam_path, frames = 88)
print('video was created')


###############################
""" 

from functions.my_midiutil import MIDIFile  # Example library for MIDI
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number
from functions.make_midi import produce_midi_file
from functions.download import download_files, load_and_combine_data, data_main
import io
import json
import pandas as pd
from datetime import datetime

start_date = "2025-02-19"
end_date   = "2025-02-20"
bpm = 90
 # Create MIDI
audio_file = f"output_{start_date}_{end_date}_{bpm}.midi"
# Lade die Datei
file_path = f"./weatherdata/produkt_zehn_now_tu_20250219_20250219_07431.txt"

start_time = datetime.strptime(start_date, '%Y-%m-%d')
end_time = datetime.strptime(end_date, '%Y-%m-%d')

data = pd.read_csv(file_path, sep=';', skipinitialspace=True)
data['PP_10'] = data['PP_10'].replace(-999, 1015) #fix the missing pressure data so it can still produce a midi file
print("Data loaded.")

vel_min = 30 # minimal Volume
vel_max = 70 # max. volume

# Choose your instruments:
instruments = ['violin', 'viola', 'cello', 'contrabass', 'seashore']

# Erstelle Midi file aus den Daten:
midi = produce_midi_file(data, bpm, start_time, vel_min, vel_max, instruments)
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

# read the midi data """