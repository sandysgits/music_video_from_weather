from src.packages.my_midiutil import MIDIFile
from src.functions.soni_functions import *

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

    max_wind_speed = 15   # this is the wind speed with the highest volume
    chord_pattern = ["I", "IV", "V", "IV"]  # Chord progression pattern

    for idx, row in enumerate(data.iterrows()):
        _, row = row
        season = get_season(str(row['MESS_DATUM']))
        scale = get_scale(season)
        chords = get_chords_for_scale(scale)
        chords_from_pattern = [chords[chord] for chord in chord_pattern if chord in chords]  # Map to actual chords
        print(chords_from_pattern, chords)
        note_midis = [str2midi(n) for n in get_notes(scale)]

        # Depending on season the allowed range of temp changes
        min_temp, max_temp = get_minmax_temp(season)

        # Make sure values do not exceed the allowed range
        temp = row['TT_10'] if row['TT_10'] >= min_temp else min_temp 
        temp = row['TT_10'] if row['TT_10'] < max_temp else max_temp
        wind_speed = abs(row['FF_10']) if abs(row['FF_10']) <= max_wind_speed else max_wind_speed 
        pressure = row['PP_10'] if row['PP_10'] >= 100 else 900
        
            # Calculate pressure gradient
        if idx > 0:
            prev_pressure = data.iloc[idx - 1]['PP_10']
            pressure_gradient = pressure - prev_pressure
        else:
            pressure_gradient = 0

        note_index = round(map_value(temp, -10, 25, 0, len(note_midis) - 1)) #todo Bereich
        midi_data = note_midis[note_index]
        
        #todo check effect, velmin, max anpassen?
        w_data = map_value(wind_speed, 0, max_wind_speed, 0, 1)
        note_velocity = round(map_value(w_data, 0, 1, vel_min, vel_max)) 
        volume = note_velocity
        
        #todo eine Kategorie mehr, für 1009-17 duartion = 0.8
        current_pressure_category = 'high' if pressure > 1013.25 else 'low'
        duration_melody = 0.5* duration if current_pressure_category == 'high' else 1.1* duration
        
        #print(f"midi_data {midi_data}")

        # temperature base
        midi.addNote(0, 0, midi_data, start_time, duration_melody, volume)
        
        # temperature
        if (pressure_gradient >= 0): # spiele 2 Töne pro duration
            midi.addNote(1, 1, midi_data - 5, start_time, 0.5*duration, volume -10)
            midi.addNote(1, 1, midi_data - 5, start_time + 0.5*duration, 0.5*duration, volume -10)
        else: # spiele einen TOn pro duration
            midi.addNote(1, 1, midi_data - 5, start_time, duration, volume -10)
        
        # midi.addNote(2, 2, midi_data + 7, start_time, 1.1 *duration, volume - 5)
         # Add chord to track 1 every 3rd tone
        if idx % 3 == 0:
            chord_notes = chords_from_pattern[(idx // 3) % len(chords_from_pattern)]
            # chord_notes = chords[chord_type]

            # Convert note names to MIDI numbers
            chord_notes_midi = [str2midi(note) for note in chord_notes]
   
            if pressure_gradient >= 0:
                chord_notes_midi = [n + 12 for n in chord_notes_midi]  # Lower by one octave
            for note in chord_notes_midi:
                midi.addNote(2, 2, note, start_time, 1.5*duration, vel_max - 20)



        volume_bass = max(0, min(
            volume+60 + 10 if pressure < 980 else
            volume+60 + 5 if pressure < 1013.25 else
            volume+60 - 10 if pressure > 1040 else
            volume+60 - 5 if pressure >= 1013.25 else
            volume+60, vel_max
        ))
        
        

        midi.addNote(3, 3, midi_data - 36, start_time, 0.3 , volume_bass)
        midi.addNote(3, 3, midi_data - 36, start_time + 1, 0.3 , volume_bass)
        midi.addNote(3, 3, midi_data - 36, start_time + 2, 0.3 , volume_bass)

        start_time += duration
    
    return midi
