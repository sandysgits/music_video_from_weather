

todo:
create .yaml file for all virtual environment
create README

# Weather Webcam Sonification

## Overview
This project downloads **weather station data** and **webcam images** from the **Deutscher Wetterdienst (DWD)** for the same time period. We then **visualize** the data and **sonify** it, merging both into a compelling multimedia experience.

## Features
✅ **Download weather data** (temperature, pressure, humidity, etc.) from DWD.  
✅ **Fetch webcam images** from DWD for the same time period.  
✅ **Visualize both datasets** in an animated plot.  
✅ **Sonify the weather data** and convert it into a MIDI file.  
✅ **Combine the animation with the sonified data** into an MP4 file.  

## Example Dataset
A small dataset is included in the repository as an example. You can find it in:
```
/data/sample_weather_data.txt
```
This dataset allows you to test the visualization and sonification features without downloading new data.

## Installation
To run this project, install the necessary dependencies using Conda:
```sh
conda create -n weather_sonifi python=3.9
conda activate weather_sonifi
conda install -c conda-forge matplotlib pandas pillow fluidsynth midi2audio
```
If you prefer **pip**, run:
```sh
pip install matplotlib pandas pillow fluidsynth midi2audio pretty_midi
```

## Usage
### **1️⃣ Download and Process Data**
Run the following command to fetch weather and webcam data for a given time range:
```sh
python main.py --start "2025-02-19 00:00" --end "2025-02-20 00:00"
```

### **2️⃣ Generate Animation and MIDI Sonification**
This will automatically:
- Fetch and preprocess data
- Generate an animated visualization
- Create a sonified MIDI file

### **3️⃣ Convert MIDI to Audio and Merge with Animation**
To convert the MIDI file to a `.wav` file and merge it with the animation:
```sh
python merge_audio_video.py
```
This outputs `final_weather_video.mp4` with synchronized sonification.

## Example Output
![Example Animation](assets/example_animation.gif)

## Contribution
Feel free to fork, improve, or extend this project! Open a pull request if you have improvements or new features.

## License
???

## Supported by UPAS
UPAS is a ...

