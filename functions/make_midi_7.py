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
    duration = 3
    data = data.iloc[::duration]
    
    for _, row in data.iterrows():

        season = get_season(str(row['MESS_DATUM']))
        scale = get_scale(season)
        note_midis = [str2midi(n) for n in get_notes(scale)]

        # todo: je nach Jahreszeit range von temp ändern

        temp = row['TT_10'] if row['TT_10'] >= -20.0 else -20.0 #todo an Jahreszeit anpassen
        wind_speed = abs(row['FF_10']) if abs(row['FF_10']) <= 25 else 25 #todo dew to windspeed ! also in video!
        pressure = row['PP_10'] if row['PP_10'] >= 100 else 900
        
        note_index = round(map_value(temp, -10, 25, 0, len(note_midis) - 1)) #todo Bereich
        midi_data = note_midis[note_index]
        
        #todo check effect, velmin, max anpassen?
        w_data = map_value(wind_speed, 0, 25, 0, 1)
        note_velocity = round(map_value(w_data, 0, 1, vel_min, vel_max)) 
        volume = note_velocity
        
        #todo eine Kategorie mehr, für 1009-17 duartion = 0.8
        current_pressure_category = 'high' if pressure > 1013.25 else 'low'
        duration_melody = 0.5* duration if current_pressure_category == 'high' else 1.1* duration
        
        #print(f"midi_data {midi_data}")

        # temperature base
        midi.addNote(0, 0, midi_data, start_time, duration_melody, volume)
        
        # temperature
        if (current_pressure_category == 'high'): # spiele 2 Töne pro duration
            midi.addNote(1, 1, midi_data - 8, start_time, 0.5*duration, volume -10)
            midi.addNote(1, 1, midi_data - 8, start_time + 0.5*duration, 0.5*duration, volume -10)
        else: # spiele einen TOn pro duration
            midi.addNote(1, 1, midi_data - 8, start_time, duration, volume -10)
        
        midi.addNote(2, 2, midi_data + 8, start_time, 1.1 *duration, volume - 5)
        
        volume_bass = max(0, min(
            volume+40 + 10 if pressure < 980 else
            volume+40 + 5 if pressure < 1013.25 else
            volume+40 - 10 if pressure > 1040 else
            volume+40 - 5 if pressure >= 1013.25 else
            volume+40, 127
        ))
        
        

        midi.addNote(3, 3, midi_data - 32, start_time, 0.3 , volume_bass)
        midi.addNote(3, 3, midi_data - 32, start_time + 1, 0.3 , volume_bass)
        midi.addNote(3, 3, midi_data - 32, start_time + 2, 0.3 , volume_bass)

        start_time += duration
    
    return midi
