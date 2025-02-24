from midi2audio import FluidSynth
import os
from pathlib import Path
print('packages read')

base_dir = Path(__file__).parent.parent
file_path_sf2 = base_dir / "assets/audio/TimGM6mb.sf2"
file_path_midi = base_dir / "assets/audio/output_2025-02-19_2025-02-20_90.midi"
print(file_path_midi)

print("SF2 exists:", os.path.exists(file_path_sf2))
print("MIDI exists:", os.path.exists(file_path_midi))

fs = FluidSynth(file_path_sf2) 
print('fs go')
fs.midi_to_audio(file_path_midi, "weather_audio.wav")

# https://github.com/asigalov61/tegridy-tools/blob/main/tegridy-tools/midi_to_colab_audio.py
# maybe use this