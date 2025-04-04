from pathlib import Path
from tinysoundfont._tinysoundfont import SoundFont
from scipy.io.wavfile import write
import mido
import numpy as np

# Paths
BASE_DIR = Path.cwd()
midi_path = BASE_DIR / "assets/audio/output_2025-03-01_09-30_2025-03-02_09-10_420.mid"
sf2_path = BASE_DIR / "assets/FluidR3_GM.sf2"
wav_path = BASE_DIR / "output.wav"

def midi_to_wav(midi_path, sf2_path, wav_path):
    sample_rate = 44100
    synth = SoundFont(str(sf2_path))

    # After: synth = SoundFont(str(sf2_path))
    synth.channel_set_preset_index(0, 0)  # Channel 0 → Grand Piano
    synth.channel_set_volume(0, 1.0)

    frames = sample_rate * 2
    buf = bytearray(frames * 8)
    synth.note_on(0, 60, 127)  # Middle C
    synth.render(buf)
    synth.note_off(0, 60)

    chunk = np.frombuffer(buf, dtype=np.float32).reshape(-1, 2)
    print("🎵 Test note amplitude:", np.max(np.abs(chunk)))




    mid = mido.MidiFile(midi_path)

    audio_chunks = []

    for msg in mid:
       # print(msg)
        if msg.time > 0:
            frames = int(msg.time * sample_rate)
            buf = bytearray(frames * 8)  # stereo: 2 channels × 4 bytes
            synth.render(buf)
            chunk = np.frombuffer(buf, dtype=np.float32).reshape(-1, 2)
            audio_chunks.append(chunk)

        if msg.type == 'note_on' and msg.velocity > 0:
            synth.note_on(msg.channel, msg.note, msg.velocity)
        elif msg.type in ['note_off', 'note_on'] and msg.velocity == 0:
            synth.note_off(msg.channel, msg.note)
        elif msg.type == 'program_change':
            # 🩹 FIX: assign the right preset to the channel
            synth.channel_set_preset_index(msg.channel, msg.program)

    # Tail
    tail_buf = bytearray((sample_rate // 2) * 8)
    synth.render(tail_buf)
    tail = np.frombuffer(tail_buf, dtype=np.float32).reshape(-1, 2)
    audio_chunks.append(tail)

    # Combine
    full_audio = np.concatenate(audio_chunks)

    # Option A: Downmix to mono
    mono_audio = full_audio.mean(axis=1)

    print("Audio max amplitude:", np.max(np.abs(full_audio)))


    # Normalize to int16
    mono_audio = np.int16(mono_audio / np.max(np.abs(mono_audio)) * 32767)

    # Write to WAV
    write(wav_path, sample_rate, mono_audio)
    print(f"✅ WAV saved: {wav_path}")


# Run it
midi_to_wav(midi_path, sf2_path, wav_path)
