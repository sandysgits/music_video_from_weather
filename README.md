# Weather Webcam Sonification

## 🚀 Motivation

Weather data is often represented in purely numerical or visual formats. However, by combining multiple sensory modalities—such as visualization, real-world webcam imagery, and sound—we can create a richer, more immersive experience.

This project explores how **sonification** and **animation** can bring weather data to life, making it more intuitive, engaging, and accessible:

- 🌌 **Webcam imagery** shows what the weather really looks like, beyond just charts.
- 📈 **Scientific line plots** visualize the meteorological data using clear and accurate graphs.
- 🎵 **Sound (sonification)** maps weather parameters (like temperature or pressure) to musical elements.
- 🌇 Combining all three modalities creates a unique, multi-sensory story of the weather.
Weather data is often represented in purely numerical or visual formats. However, by combining multiple sensory modalities—such as visualization, real-world webcam imagery, and sound—we can create a richer, more immersive experience.

## 📃 Project Overview

This project downloads **weather station data** and **webcam images** from the **Deutscher Wetterdienst (DWD)**. It then visualizes and sonifies this data, merging it into a compelling multimedia experience.

### Features

- 📷 Download webcam images from DWD.
- 🌌 Fetch weather station data (temperature, pressure, humidity, etc.).
- 🎨 Visualize webcam and station data in an animated plot.
- 🎶 Sonify weather data by generating a MIDI file.
- 🎧 Convert MIDI to WAV (currently very basic conversion method, improvements need to be implemented with packages like fluidsynth).
- 🎥 Combine animation and audio into an MP4 video.

## 🚀 Installation

Clone the repository and install dependencies via `pyproject.toml` or `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 📚 Usage

Set options inside `main.py`:

### Required:

- `station_id`: Weather station ID ([see available IDs](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/historical/zehn_min_tu_Beschreibung_Stationen.txt))
- `station`: Webcam station ID ([see available webcams](https://opendata.dwd.de/weather/webcam/))

> Note: You can combine a webcam station with any weather station, e.g. for the webcam 'Offenbach-W', you can use station '01420' (Frankfurt airport), '01424' (Frankfurt Campus Westend) or '07341' (Offenbach Wetterpark).

### Modes

#### **🕚 'now' mode**

- Downloads **live** weather and webcam data.
- Webcam data is only available for the **past 2 days**.
- Generates an animation of the last \~48 hours.

#### **📅 'historic' mode**

- Uses pre-downloaded webcam data stored in:
  ```
  weatherdata/{STATION_NUMBER}_historic/webcam_data/
  ```
- Example dataset included: Offenbach-O & Offenbach-W (2025-03-01 09:30 to 2025-03-07 14:00).

## 🎥 Example Outputs

![Example Animation for 'now'-mode](final_output/Offenbach-W_01420_2025-04-18_18-10_2025-04-18_18-10_420_now.mp4)

![Example Animation for 'historic'-mode](final_output/Offenbach-W_01420_2025-03-01_09-30_2025-03-05_09-30_420_historic.mp4)


## 🎶 Sonification Logic

Weather parameters are mapped to musical features using rules designed to convey both **emotion** and **data meaning**. The MIDI file contains 5 tracks:

| Track | Weather Feature   | Mapping Logic                                                                 |
|-------|-------------------|-------------------------------------------------------------------------------|
| 0     | **Main Melody**   | Temperature → pitch (based on seasonal scale), wind speed → velocity, pressure gradient → duration |
| 1     | **Bass**       | Derived from melody (lower pitch); plays short/long notes based on pressure trend |
| 2     | **Harmony**        | Seasonal chord progressions (I–IV–V–IV); transposed based on pressure gradient |
| 3     | **Drums**          | Temperature (lower octave); volume modified by pressure (low = louder)       |
| 4     | **Rain Sounds**   | Rain intensity → velocity of rhythmic notes                                  |

### 🎺 Notes & Instruments

- **Temperature** determines the melody and harmony notes (mapped to seasonally appropriate musical scales).
- **Wind speed** controls the note **velocity** (volume), from soft breezes to strong gusts.
- **Pressure changes** affect rhythm:
  - Rising pressure → short energetic notes
  - Falling pressure → slower, heavier notes
- **Chords** reflect the current season’s harmonic palette (e.g., major for spring/summer, minor for autumn/winter).
- **Bass** notes reinforce low-frequency textures, with volume increasing during low-pressure (stormy) conditions.
- **Rain** is mapped to soft or strong percussive note-like effects, based on real intensity (0–5 scale).


- MIDI is converted to WAV using a basic synth or a GUI tool like [Signal](https://signal.vercel.app/)

## 💚 How to Use

1. Clone the repo
2. Install dependencies
3. Set options in `main.py`
4. Run the main script

```bash
python main.py
```

## ❌ Current Limitations

- MIDI-to-WAV conversion method is basic
  - Ideally use `fluidsynth` or other external synth for better quality, but this is not yet implemented
  - You can inspect or remix the MIDI file properly using tools like: [https://signal.vercel.app/](https://signal.vercel.app/)
- Webcam images only available from DWD for the past 2 days
  - No historic webcam dataset can be provided in this repo
- Limited set of webcam locations


## 🙌 Contribution

Fork the repo, open a PR, or suggest improvements. We'd love to see your ideas!

## 🌟 Supported by UPAS

This project is supported by the **UPAS Student Idea Pot 2024**. Learn more at: [https://www.meteo-upas.de/](https://www.meteo-upas.de/)

