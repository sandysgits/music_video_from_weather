import pandas as pd
from functions.my_midiutil import MIDIFile
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number, str2midi

def produce_midi_file(data, bpm, vel_min, vel_max, instruments):
    print("Generating MIDI file...")
    
    # Initialize MIDI File with 5 tracks
    midi = MIDIFile(5)
    track_names = ["Main Melody", "Harmony", "Harmony", "Bass", "Rain Sounds"]
    
    for i, name in enumerate(track_names):
        midi.addTrackName(i, 0, name)
        midi.addTempo(i, 0, bpm)
        midi.addProgramChange(i, i, 0, get_midi_instrument_number(instruments[i]))
    
    start_time = 0
    
    for _, row in data.iterrows():
        temp = row['TT_10'] if row['TT_10'] >= -20.0 else -20.0
        wind_speed = abs(row['TD_10']) if abs(row['TD_10']) <= 100 else 100
        pressure = row['PP_10'] if row['PP_10'] >= 100 else 100
        
        season = get_season(str(row['MESS_DATUM']))
        scale = get_scale(season)
        note_midis = [str2midi(n) for n in get_notes(scale)]
        
        note_index = round(map_value(temp, -20, 50, 0, len(note_midis) - 1))
        midi_data = note_midis[note_index]
        
        note_velocity = round(map_value(wind_speed, 0, 100, vel_min, vel_max))
        volume = max(0, min(note_velocity, 127))
        
        current_pressure_category = 'high' if pressure > 1013.25 else 'low'
        duration_melody = 0.5 if current_pressure_category == 'high' else 1.1
        
        midi.addNote(0, 0, midi_data, start_time, duration_melody, volume)
        midi.addNote(1, 1, midi_data - 8, start_time, 0.5 * duration_melody, volume + 10)
        midi.addNote(1, 1, midi_data - 8, start_time + 0.5 * duration_melody, 0.5 * duration_melody, volume + 10)
        midi.addNote(2, 2, midi_data + 8, start_time, 1.1 * duration_melody, volume - 10)
        
        volume_bass = max(0, min(
            volume + 20 if pressure < 950 else
            volume + 10 if pressure < 1013.25 else
            volume - 10 if pressure >= 1013.25 else
            volume - 20, 127
        ))
        
        midi.addNote(3, 3, midi_data - 32, start_time, 0.5 * duration_melody, volume_bass)
        start_time += 1
    
    return midi
