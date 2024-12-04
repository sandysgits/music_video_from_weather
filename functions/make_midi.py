import pandas as pd
# from audiolazy import str2midi
from my_midiutil import MIDIFile
from functions.soni_functions import get_season, get_scale, map_value, get_notes, get_midi_instrument_number, str2midi

def produce_midi_file(data, bpm, start_time, vel_min, vel_max, instruments):
    print("Generating midi file.")
    # Erstelle eine neue MIDI-Datei mit mehreren Spuren
    midi = MIDIFile(5)  # drei Spuren
    midi.addTrackName(0, 0, "Main Melody")
    midi.addTrackName(1, 0, "Harmony")
    midi.addTrackName(2, 0, "Harmony")
    midi.addTrackName(3, 0, "Bass")
    midi.addTrackName(4, 0, "Rain sounds")

    midi.addTempo(0, 0, tempo = bpm)  # Setze ein Standard-Tempo für Spur 0
    midi.addTempo(1, 0, tempo = bpm)  # Setze ein Standard-Tempo für Spur 1
    midi.addTempo(2, 0, tempo = bpm)  # Setze ein Standard-Tempo für Spur 2
    midi.addTempo(3, 0, tempo = bpm)  # Setze ein Standard-Tempo für Spur 3
    midi.addTempo(4, 0, tempo = bpm)  # Setze ein Standard-Tempo für Spur 4

    # Setze Instrumente für die Spuren (Instrumentennummern nach General MIDI)
    first_midi_instrument = get_midi_instrument_number(instruments[0])
    second_midi_instrument = get_midi_instrument_number(instruments[1])
    third_midi_instrument = get_midi_instrument_number(instruments[2])
    fourth_midi_instrument = get_midi_instrument_number(instruments[3])
    fifth_midi_instrument = get_midi_instrument_number(instruments[4])

    midi.addProgramChange(0, 0, 0, first_midi_instrument)  # Spur 0, Kanal 0, Zeitpunkt 0, Instrument 0 (Klavier)
    midi.addProgramChange(1, 1, 0, second_midi_instrument)  # Spur 1, Kanal 1, Zeitpunkt 0, Instrument 41 (Violine), 42 Cello
    midi.addProgramChange(2, 2, 0, third_midi_instrument) # Spur 2, Kanal 2, Zeitpunkt 0, Instrument 122 (Seashore)
    midi.addProgramChange(3, 3, 0, fourth_midi_instrument) # Spur 3, Kanal 3, Zeitpunkt 0, Instrument 122 (Seashore)
    midi.addProgramChange(4, 4, 0, fifth_midi_instrument)


    # Initialisierung der Startzeit und der vorherigen Druckkategorie
    start_time = 0
    previous_pressure_category = None 

    # Füge Noten basierend auf den Wetterdaten hinzu
    for index, row in data.iterrows():
        date = str(row['MESS_DATUM'])
        if (row['TT_10'] >= -20.0):
            temp = row['TT_10']  # Melodie-Noten basierend auf der Temperatur
        if (abs(row['TD_10']) <= 100):
            wind_speed = abs(row['TD_10'])  # Bestimmt die Länge der Noten
        if (row['PP_10'] >= 100):
            pressure = row['PP_10']  # Beeinflusst die Lautstärke

        # Bestimme die Tonart
        season = get_season(date)
        scale = get_scale(season)
        note_names = get_notes(scale)
        # print(note_names)
        # ODER über vorgegebene Noten
        #note_names = ['C1','C2','G2',
        #             'C3','E3','G3','A3','B3',
        #             'D4','E4','G4','A4','B4',
        #             'D5','E5','G5','A5','B5',
        #             'D6','E6','F#6','G6','A6']
        note_midis = [str2midi(n) for n in note_names] #make a list of midi note numbers
        n_notes = len(note_midis)

        # Bestimme die Kategorie für den Druck (Hochdruck vs. Tiefdruck)
        current_pressure_category = 'high' if pressure > 1013.25 else 'low'

        # Setze den Takt, wenn sich die Kategorie geändert hat
        #if current_pressure_category != previous_pressure_category:
        #    if current_pressure_category == 'high':
        #        midi.addTimeSignature(track, start_time, 6, 2, 24)  # 6/4 Takt
        #        midi.addTimeSignature(1, start_time, 6, 2, 24)  # 6/4 Takt
        #    else:
        #        midi.addTimeSignature(track, start_time, 4, 2, 24)  # 4/4 Takt
        #        midi.addTimeSignature(1, start_time, 4, 2, 24)  # 4/4 Takt
        #    previous_pressure_category = current_pressure_category

        # Konvertiere Temperatur in eine MIDI-Note
        y_data = map_value(temp, -20, 50, 0, 1)
        note_index = round(map_value(y_data, 0, 1, 0, n_notes-1)) #bigger craters are mapped to lower notes
        midi_data = note_midis[note_index]

        # Konvertiere Wind in Lautstärke
        w_data = map_value(wind_speed, 0, 100, 0, 1)
        note_velocity = round(map_value(w_data, 0, 1, vel_min, vel_max)) #bigger craters will be louder
        volume = note_velocity

        # Bestimme die Notenlänge
        duration_beats = 1
        duration = duration_beats *60 / bpm #max(0.1, 2 - (abs(wind_speed) / 10))

        # Ändere Notenlänge der Melodie bei Hoch-/Tiefdruck
        if (current_pressure_category == 'high'):
            duration_melody = 0.1 * duration
        else:
            duration_melody = 1.1* duration

        # Füge die Note zur MIDI-Datei hinzu
        midi.addNote(0, 0, midi_data, start_time, duration_melody, volume)

        # Füge eine harmonische Note zur zweiten Spur hinzu (z. B. eine Terz höher)
        harmony_note = midi_data - 8  # Eine Terz (4 Halbtonschritte) höher und eine Oktave tiefer
        # 2. Instrument
        if (current_pressure_category == 'high'): # spiele 2 Töne pro duration
            midi.addNote(1, 1, midi_data - 8, start_time, 0.5*duration, volume -10)
            midi.addNote(1, 1, midi_data - 8, start_time + 0.5*duration, 0.5*duration, volume -10)
        else: # spiele einen TOn pro duration
            midi.addNote(1, 1, midi_data - 8, start_time, duration, volume -10)

        midi.addNote(2, 2, harmony_note, start_time, 1.1*duration, volume - 10)  # Spur 1, Kanal 1, leiserer Ton

        # Konvertiere Druck in Lautstärke mit 4 verschiedenen SChritten
        if (pressure < 950):
            volume_bass = min(volume + 20, vel_max)
        elif (pressure < 1013.25):
            volume_bass = min(volume + 10, vel_max)
        elif (pressure >= 1013.25):
            volume_bass = volume -10
        elif (pressure > 1070):
            volume_bass = volume -20
    
        midi.addNote(3, 3, midi_data - 32, start_time, 0.3*duration, volume_bass)

        # Erhöhe die Startzeit für die nächste Note
        start_time += duration
        
    return midi
