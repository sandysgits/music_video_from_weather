import json
# from flask import Flask, request, jsonify
from my_midiutil import MIDIFile  # Example library for MIDI
# from audiolazy import str2midi
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number
from functions.make_midi import produce_midi_file
from functions.download import download_files, load_and_combine_data, data_main
import requests
import zipfile
import io
import os
import pandas as pd
from datetime import datetime

def generate_media(start_date, end_date, bpm):

    # Create MIDI
    audio_file = f"output_{start_date}_{end_date}_{bpm}.midi"
    # Lade die Datei
    file_path = f"./weatherdata/OF_wetterpark_zehn_min_tu_20200101_20211231_07341.txt"
    files_downloaded = [file_path]
    #start_date = datetime.strptime(start_time, '%Y%m%d%H%M')
    #end_date = datetime.strptime(end_time, '%Y%m%d%H%M')
    print("Loading data...")
    data = load_and_combine_data(files_downloaded, start_date, end_date)
    #data = pd.read_csv(file_path, sep=';', skipinitialspace=True)
    data = data.iloc[::30]  # Wählt jede 30. Zeile aus (alle 5 min)
    print("Data loaded.")
    
    
    #instruments = ['violin', 'viola', 'cello', 'contrabass', 'seashore']
    # Erstelle Midi file aus den Daten:
    midi = produce_midi_file(data, bpm, start_time)
    
    with open(f"./assets/audio/{audio_file}", "wb") as output_file:
        midi.writeFile(output_file)

    # Create videos (placeholders for now)
    video1 = f"video1_{start_date}_{end_date}_{bpm}.mp4"
    video2 = f"video2_{start_date}_{end_date}_{bpm}.mp4"
    with open(f"./assets/video/{video1}", "wb") as vid1, open(f"./assets/video/{video2}", "wb") as vid2:
        vid1.write(b"")  # Placeholder for video content
        vid2.write(b"")

    return jsonify({
        "audioFile": audio_file,
        "video1": video1,
        "video2": video2
    })

if __name__ == '__main__':
    os.makedirs("./assets/audio", exist_ok=True)
    os.makedirs("./assets/video", exist_ok=True)
    app.run(debug=True)
