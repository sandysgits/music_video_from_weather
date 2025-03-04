# import json
# from flask import Flask, request, jsonify
from weather_webcam_sonification.functions.my_midiutil import MIDIFile  # Example library for MIDI
# from audiolazy import str2midi
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number
from functions.make_midi import produce_midi_file
from functions.download import download_files, load_and_combine_data, data_main
# import requests
# import zipfile
import io
import json
# import os
import pandas as pd
from datetime import datetime

def generate_media(start_date, end_date, bpm):

    # Create MIDI
    audio_file = f"output_{start_date}_{end_date}_{bpm}.midi"
    # Lade die Datei
    file_path = f"./weatherdata/OF_wetterpark_zehn_min_tu_20200101_20211231_07341.txt"
    files_downloaded = [file_path]
    start_time = datetime.strptime(start_date, '%Y-%m-%d')
    end_time = datetime.strptime(end_date, '%Y-%m-%d')
    print("Loading data...")
    #data = load_and_combine_data(files_downloaded, start_date, end_date)
    data = pd.read_csv(file_path, sep=';', skipinitialspace=True)
    data = data.iloc[::30]  # Wählt jede 30. Zeile aus (alle 5 min)
    print("Data loaded.")
    
    vel_min = 30 # minimal Volume
    vel_max = 70 # max. volume

    # Choose your instruments:
    instruments = ['violin', 'viola', 'cello', 'contrabass', 'seashore']

    # Erstelle Midi file aus den Daten:
    midi = produce_midi_file(data, bpm, start_time, vel_min, vel_max, instruments)
    print("Midi produced.")
    
    #with open(f"./assets/audio/{audio_file}", "wb") as output_file:
    #    midi.writeFile(output_file)

    # Create an in-memory buffer
    print("Write midi to {audio_file}")
    midi_buffer = io.BytesIO()
    
    # Write the MIDI data to the buffer
    midi.writeFile(midi_buffer)

    # Get the binary data from the buffer
    midi_data = midi_buffer.getvalue()

    # Generate Videos:
    # ...... (data, start_time, end_time, bpm)

    video1_data = b""
    video2_data = b""

    return json.dumps({
        "audioFile": midi_data,
        "video1": video1_data,
        "video2": video2_data,
    })

if __name__ == '__main__':
    os.makedirs("./assets/audio", exist_ok=True)
    os.makedirs("./assets/video", exist_ok=True)
    app.run(debug=True)

# generate_media("2024-12-01", "2024-12-04", 90)
