import pandas as pd
# from audiolazy import str2midi
from functions.my_midiutil import MIDIFile
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number, str2midi

def produce_midi_file(data, bpm, start_time, vel_min, vel_max, instruments):
    print("Generating midi file.")
    print(f"Total data points: {len(data)}")
    
    midi = MIDIFile(5)
    midi.addTrackName(0, 0, "Main Melody")
    midi.addTrackName(1, 0, "Harmony")
    midi.addTrackName(2, 0, "Harmony")
    midi.addTrackName(3, 0, "Bass")
    midi.addTrackName(4, 0, "Rain sounds")

    for i in range(5):
        midi.addTempo(i, 0, tempo=bpm)

    instruments_midi = [get_midi_instrument_number(inst) for inst in instruments]
    for i, instr in enumerate(instruments_midi):
        midi.addProgramChange(i, i, 0, instr)

    start_time = 0
    previous_pressure_category = None 
    total_duration = 0  # Initialize total duration counter
    
    for index, row in data.iterrows():
        date = str(row['MESS_DATUM'])
        temp = row['TT_10'] if row['TT_10'] >= -20.0 else -20.0
        wind_speed = abs(row['TD_10']) if abs(row['TD_10']) <= 100 else 100
        pressure = row['PP_10'] if row['PP_10'] >= 100 else 100

        season = get_season(date)
        scale = get_scale(season)
        note_names = get_notes(scale)
        note_midis = [str2midi(n) for n in note_names]
        n_notes = len(note_midis)

        current_pressure_category = 'high' if pressure > 1013.25 else 'low'

        y_data = map_value(temp, -20, 50, 0, 1)
        note_index = round(map_value(y_data, 0, 1, 0, n_notes-1)) 
        midi_data = note_midis[note_index]

        w_data = map_value(wind_speed, 0, 100, 0, 1)
        note_velocity = round(map_value(w_data, 0, 1, vel_min, vel_max)) 
        volume = note_velocity

        #duration = 60 / bpm
        duration = 1
        total_duration += duration  # Accumulate total duration

        midi.addNote(0, 0, midi_data, start_time, duration, volume)
        harmony_note = midi_data - 8

        if current_pressure_category == 'high':
            midi.addNote(1, 1, midi_data - 8, start_time, duration, volume - 10)
            midi.addNote(1, 1, midi_data - 8, start_time + duration, duration, volume - 10)
        else:
            midi.addNote(1, 1, midi_data - 8, start_time, duration, volume - 10)

        midi.addNote(2, 2, harmony_note, start_time, duration, volume - 10)

        if pressure < 950:
            volume_bass = min(volume + 20, vel_max)
        elif pressure < 1013.25:
            volume_bass = min(volume + 10, vel_max)
        elif pressure >= 1013.25:
            volume_bass = volume - 10
        elif pressure > 1070:
            volume_bass = volume - 20
    
        midi.addNote(3, 3, midi_data - 32, start_time, duration, volume_bass)
        start_time += duration
    
    print(f"Total estimated MIDI duration: {total_duration:.2f} seconds")
    return midi
