import sys
# Funktion zur Bestimmung der Jahreszeit basierend auf dem Datum
def get_season(date_str):
    month = int(date_str[4:6])  # Extrahiere den Monat
    if 3 <= month <= 5:
        return 'spring'  # Frühling (E-Dur)
    elif 6 <= month <= 8:
        return 'summer'  # Sommer (g-moll)
    elif 9 <= month <= 11:
        return 'autumn'  # Herbst (F-Dur)
    else:
        return 'winter'  # Winter (f-moll)
 
# Bestimme die Tonart basierend auf der Jahreszeit
def get_scale(season):
    scales = {
        'spring': 'E major',
        'summer': 'G minor',
        'autumn': 'F major',
        'winter': 'F minor'
    }
    return scales[season]

def get_minmax_temp(season):
    minmax = {
        'spring': (-5, 25),
        'summer': (5, 35),
        'autumn': (-10, 25),
        'winter': (-20, 15)
    }
    return minmax[season]

# Gebe Töne der Tonart aus:
def get_notes(scale):
    notes = {
        'E major': ['E1','E2','G#2',
                    'E3', 'F#3','G#3','B3', 'C#4',
                    'E4', 'F#4','G#4','B4', 'C#5',
                    'E5', 'F#5','G#5','B5', 'C#6',
                    'E6', 'F#6','G#6','B6', 'C#7'],
        'G minor': ['G1','G2','C3',
                    'G3', 'A#3','C4','D4', 'F4',
                    'G4', 'A#4','C5','D5', 'F5',
                    'G5', 'A#5','C6','D6', 'F6',
                    'G6', 'A#6','C7','D7', 'F7'],
        'F major': ['F1','F2','A2',
                    'F3', 'G3','A3','C4', 'D4',
                    'F4', 'G4','A4','C5', 'D5',
                    'F5', 'G5','A5','C6', 'D6',
                    'F6', 'G6','A6','C7', 'D7',],
        'F minor': ['F1','F2','A#2',
                    'F3', 'G#3','A#3','C4', 'D#4',
                    'F4', 'G#4','A#4','C5', 'D#5',
                    'F5', 'G#5','A#5','C6', 'D#6',
                    'F6', 'G#6','A#6','C7', 'D#7',]
    }
    return notes[scale]


# function maps value (which is inbetween min_value and max_value) into new range from min_result to max_result
def map_value(value,min_value,max_value,min_result,max_result):
    '''maps value (or array of values) from one range to another'''
    result = min_result + (value - min_value)/(max_value-min_value)*(max_result - min_result)
    return result


def get_midi_instrument_number(instrument_name):
    # Dictionary mapping instrument names to MIDI numbers (General MIDI)
    INSTRUMENTS = {
        "acoustic grand piano": 0,
        "bright acoustic piano": 1,
        "electric grand piano": 2,
        "honky-tonk piano": 3,
        "electric piano 1": 4,
        "electric piano 2": 5,
        "harpsichord": 6,
        "clavinet": 7,
        "celesta": 8,
        "glockenspiel": 9,
        "music box": 10,
        "vibraphone": 11,
        "marimba": 12,
        "xylophone": 13,
        "tubular bells": 14,
        "dulcimer": 15,
        "drawbar organ": 16,
        "percussive organ": 17,
        "rock organ": 18,
        "church organ": 19,
        "reed organ": 20,
        "accordion": 21,
        "harmonica": 22,
        "tango accordion": 23,
        "acoustic guitar (nylon)": 24,
        "acoustic guitar (steel)": 25,
        "electric guitar (jazz)": 26,
        "electric guitar (clean)": 27,
        "electric guitar (muted)": 28,
        "overdriven guitar": 29,
        "distortion guitar": 30,
        "guitar harmonics": 31,
        "acoustic bass": 32,
        "electric bass (finger)": 33,
        "electric bass (pick)": 34,
        "fretless bass": 35,
        "slap bass 1": 36,
        "slap bass 2": 37,
        "synth bass 1": 38,
        "synth bass 2": 39,
        "violin": 40,
        "viola": 41,
        "cello": 42,
        "contrabass": 43,
        "tremolo strings": 44,
        "pizzicato strings": 45,
        "orchestral harp": 46,
        "timpani": 47,
        "string ensemble 1": 48,
        "string ensemble 2": 49,
        "synth strings 1": 50,
        "synth strings 2": 51,
        "choir aahs": 52,
        "voice oohs": 53,
        "synth choir": 54,
        "orchestra hit": 55,
        "trumpet": 56,
        "trombone": 57,
        "tuba": 58,
        "muted trumpet": 59,
        "french horn": 60,
        "brass section": 61,
        "synth brass 1": 62,
        "synth brass 2": 63,
        "soprano sax": 64,
        "alto sax": 65,
        "tenor sax": 66,
        "baritone sax": 67,
        "oboe": 68,
        "english horn": 69,
        "bassoon": 70,
        "clarinet": 71,
        "piccolo": 72,
        "flute": 73,
        "recorder": 74,
        "pan flute": 75,
        "blown bottle": 76,
        "shakuhachi": 77,
        "whistle": 78,
        "ocarina": 79,
        "lead 1 (square)": 80,
        "lead 2 (sawtooth)": 81,
        "lead 3 (calliope)": 82,
        "lead 4 (chiff)": 83,
        "lead 5 (charang)": 84,
        "lead 6 (voice)": 85,
        "lead 7 (fifths)": 86,
        "lead 8 (bass + lead)": 87,
        "pad 1 (new age)": 88,
        "pad 2 (warm)": 89,
        "pad 3 (polysynth)": 90,
        "pad 4 (choir)": 91,
        "pad 5 (bowed)": 92,
        "pad 6 (metallic)": 93,
        "pad 7 (halo)": 94,
        "pad 8 (sweep)": 95,
        "fx 1 (rain)": 96,
        "fx 2 (soundtrack)": 97,
        "fx 3 (crystal)": 98,
        "fx 4 (atmosphere)": 99,
        "fx 5 (brightness)": 100,
        "fx 6 (goblins)": 101,
        "fx 7 (echoes)": 102,
        "fx 8 (sci-fi)": 103,
        "sitar": 104,
        "banjo": 105,
        "shamisen": 106,
        "koto": 107,
        "kalimba": 108,
        "bagpipe": 109,
        "fiddle": 110,
        "shanai": 111,
        "tinkle bell": 112,
        "agogo": 113,
        "steel drums": 114,
        "woodblock": 115,
        "taiko drum": 116,
        "melodic tom": 117,
        "synth drum": 118,
        "reverse cymbal": 119,
        "guitar fret noise": 120,
        "breath noise": 121,
        "seashore": 122,
        "bird tweet": 123,
        "telephone ring": 124,
        "helicopter": 125,
        "applause": 126,
        "gunshot": 127
    }
    instrument_name = instrument_name.lower()
    if instrument_name in INSTRUMENTS:
        return INSTRUMENTS[instrument_name]
    else:
        print(f"Error: '{instrument_name}' is not a valid instrument name.")
        sys.exit(1)

def str2midi(note):
    """
    Returns a note-to-MIDI mapping for notes from C0 to C8.

    Returns:
        dict: A dictionary mapping note names (e.g., "C4") to MIDI numbers.
    """
    note_map = {
        "C0": 0, "C#0": 1, "D0": 2, "D#0": 3, "E0": 4, "F0": 5, "F#0": 6, "G0": 7, "G#0": 8, "A0": 9, "A#0": 10, "B0": 11,
        "C1": 12, "C#1": 13, "D1": 14, "D#1": 15, "E1": 16, "F1": 17, "F#1": 18, "G1": 19, "G#1": 20, "A1": 21, "A#1": 22, "B1": 23,
        "C2": 24, "C#2": 25, "D2": 26, "D#2": 27, "E2": 28, "F2": 29, "F#2": 30, "G2": 31, "G#2": 32, "A2": 33, "A#2": 34, "B2": 35,
        "C3": 36, "C#3": 37, "D3": 38, "D#3": 39, "E3": 40, "F3": 41, "F#3": 42, "G3": 43, "G#3": 44, "A3": 45, "A#3": 46, "B3": 47,
        "C4": 48, "C#4": 49, "D4": 50, "D#4": 51, "E4": 52, "F4": 53, "F#4": 54, "G4": 55, "G#4": 56, "A4": 57, "A#4": 58, "B4": 59,
        "C5": 60, "C#5": 61, "D5": 62, "D#5": 63, "E5": 64, "F5": 65, "F#5": 66, "G5": 67, "G#5": 68, "A5": 69, "A#5": 70, "B5": 71,
        "C6": 72, "C#6": 73, "D6": 74, "D#6": 75, "E6": 76, "F6": 77, "F#6": 78, "G6": 79, "G#6": 80, "A6": 81, "A#6": 82, "B6": 83,
        "C7": 84, "C#7": 85, "D7": 86, "D#7": 87, "E7": 88, "F7": 89, "F#7": 90, "G7": 91, "G#7": 92, "A7": 93, "A#7": 94, "B7": 95,
        "C8": 96
    }

    # Check if the note exists in the dictionary
    if note not in note_map:
        raise ValueError(f"Invalid note: {note}. Note must be between C0 and C8.")
    
    return note_map[note]


# Function to get the chords (triads) for the 1st, 4th, and 5th degrees of a scale
def get_chords_for_scale(scale):
    """
    Returns the chords (triads) for the 1st, 4th, and 5th degrees of the given scale.
    """
    chords = {
            'E major': {
                'I': ['E0', 'G#0', 'B0'],  # E major chord
                'IV': ['A0', 'C#1', 'E1'],  # A major chord
                'V': ['B0', 'D#1', 'F#1']   # B major chord
            },
            'G minor': {
                'I': ['G0', 'A#0', 'D1'],  # G minor chord
                'IV': ['C1', 'D#1', 'G1'],  # C minor chord
                'V': ['D1', 'F1', 'A#1']   # D minor chord
            },
            'F major': {
                'I': ['F0', 'A0', 'C1'],  # F major chord
                'IV': ['A#0', 'D1', 'F1'],  # A# major chord
                'V': ['C1', 'E1', 'G1']   # C major chord
            },
            'F minor': {
                'I': ['F0', 'A#0', 'C1'],  # F minor chord
                'IV': ['A#0', 'D#1', 'F1'],  # A# minor chord
                'V': ['C1', 'F1', 'G#1']   # C minor chord
            }
        }
    return chords.get(scale, {})
