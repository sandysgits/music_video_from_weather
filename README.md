# Weather Webcam Sonification

## Motivation
Weather data is often represented in purely numerical or visual formats. However, by combining multiple sensory modalities—such as visualization, real-world webcam imagery, and sound—we can create a richer, more immersive experience. This project explores how sonification and animation can bring weather data to life, making it more intuitive, engaging, and accessible.

Webcam data provides a direct visual representation of actual weather conditions, offering a perspective that goes beyond abstract graphs and numbers. By integrating live weather footage with data visualizations, we create a more comprehensive and realistic depiction of weather changes. Seeing the sky darken, clouds gather, or rain begin to fall adds context that a simple line graph cannot provide.

Adding sound as another sensory layer enhances this experience even further. Through sonification, we can represent various meteorological changes dynamically, allowing us to hear the weather evolve over time. For example, a pressure drop could be mapped to a descending pitch to indicate worsening conditions, while temperature changes might be reflected in tonal shifts. These are just examples of how sonification can translate numerical weather patterns into an auditory experience, offering new ways to interpret and understand complex data.


## Overview
This project downloads **weather station data** and **webcam images** from the **Deutscher Wetterdienst (DWD)** for the same time period. We then **visualize** the data and **sonify** it, merging both into a compelling multimedia experience.

## Features
✅ **Download weather data** (temperature, pressure, humidity, etc.) from DWD.  
✅ **Fetch webcam images** from DWD for the same time period.  
✅ **Visualize both datasets** in an animated plot.  
✅ **Sonify the weather data** and convert it into a MIDI file.  
transform the midi into a wav file.
✅ **Combine the animation with the sonified data** into an MP4 file.  

## Example Dataset
A small **example dataset** is included in the repository, containing:
- A `.txt` file with **exemplary weather data**.
- The **corresponding webcam images** from the same time period.

📄 **Path:** `/data/sample_weather_data.txt` and associated images in `/data/webcam_images/`

This dataset allows you to test the visualization and sonification features without downloading new data.

## Installation
To set up the environment automatically, use the provided YAML file:
```sh
conda env create -f environment/environment.yaml
conda activate weather_sonifi
```
Alternatively, install dependencies manually with Conda:
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
### **Option 1: Download Station and Webcam Data Live from DWD and Create Video**
Fetch the latest weather and webcam data from DWD and generate the animated visualization:
```sh
python main.py --start "2025-02-19 00:00" --end "2025-02-20 00:00"
```

### **Option 2: Use Example Data**
If you want to generate the visualization using the included example dataset:
```sh
python main.py --use-example-data
```
This will process the pre-downloaded weather data and corresponding webcam images.

### **Generating the Final Video with Audio**
To convert the MIDI file to a `.wav` file and merge it with the animation:
```sh
python merge_audio_video.py
```
This outputs `final_weather_video.mp4` with synchronized sonification.

## Example Output
![Example Animation](assets/example_animation.gif)

## Environment File
The `environment.yaml` file is stored in the `environment/` directory and can be used to set up the project easily. 

📄 **Path:** `environment/environment.yaml`

## Contribution
Feel free to fork, improve, or extend this project. Open a pull request if you have improvements or new features.


## License
???

## Supported by UPAS
UPAS is a ...

