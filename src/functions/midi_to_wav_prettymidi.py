import pretty_midi
import numpy as np
from scipy.io.wavfile import write
import subprocess
import os

def midi_to_wav(midi_file, output_wav, sample_rate=44100):
    
    """Convert MIDI to WAV using synthesized sine waves."""
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    print('midi data read')
    # Generate audio using default PrettyMIDI synth
    audio_data = midi_data.synthesize(fs=sample_rate)
    print('midi data syntesized')
    # Normalize audio to 16-bit PCM
    audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
    # Ensure the output directory exists
    # Write to WAV file
    write(output_wav, sample_rate, audio_data)


