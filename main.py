import json
from flask import Flask, request, jsonify
from midiutil import MIDIFile  # Example library for MIDI
import os

app = Flask(__name__)

@app.route('/run-python', methods=['POST'])
def generate_assets():
    data = request.json
    start_date = data['startDate']
    end_date = data['endDate']
    bpm = int(data['bpm'])

    # Create MIDI
    audio_file = f"output_{start_date}_{end_date}_{bpm}.midi"
    midi = MIDIFile(1)
    midi.addTempo(0, 0, bpm)
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
