import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from PIL import Image
import pandas as pd
from IPython.display import display, HTML
from matplotlib.animation import FFMpegWriter

def load_weather_and_image_data_historic(base_path, df, start_datetime, end_datetime, frames=5):
    """Finds and loads weather and image data for a given timeframe."""
    print(f"Loading data from {start_datetime} to {end_datetime}...")
    
    # Extract unique dates and times from image filenames
    existing_images = []
    for filename in os.listdir(base_path):
        if filename.endswith(".jpg"):
            parts = filename.split("_")
            if len(parts) == 3:
                date_time = parts[1] + " " + parts[2].replace(".jpg", "")
                existing_images.append(date_time)

    # Convert to DataFrame
    image_df = pd.DataFrame(existing_images, columns=['DateTime'])
    image_df['DateTime'] = pd.to_datetime(image_df['DateTime'], format='%Y%m%d %H%M')
    # Filter by the given time range
    image_df = image_df[(image_df['DateTime'] >= start_datetime) & (image_df['DateTime'] <= end_datetime)]
    
    if image_df.empty:
        print("Warning: No images found for the specified time range.")
    else:
        print(f"Successfully loaded {len(image_df)} images.")
    
    # Load weather data
    full_weather_data = df[(df['MESS_DATUM'] >= start_datetime) & (df['MESS_DATUM'] <= end_datetime)]
    
    if full_weather_data.empty:
        print("Warning: No weather data found for the specified time range.")
    else:
        print(f"Successfully loaded {len(full_weather_data)} weather data points.")
    
    if len(image_df) != len(full_weather_data):
        print('Not enough webcam images available at the specified time span!')
        return
    
    return image_df, full_weather_data


def load_weather_and_image_data_now(base_path, full_weather_data, frames=5):
    """Loads image + weather data for shared timestamps only."""

    # === Extract datetimes from webcam image filenames ===
    existing_images = []
    for filename in os.listdir(base_path):
        if filename.endswith(".jpg"):
            parts = filename.split("_")
            if len(parts) == 3:
                date_time = parts[1] + " " + parts[2].replace(".jpg", "")
                existing_images.append(date_time)

    # === Create image_df ===
    image_df = pd.DataFrame(existing_images, columns=['DateTime'])
    image_df['DateTime'] = pd.to_datetime(image_df['DateTime'], format='%Y%m%d %H%M')
    image_df = image_df.sort_values('DateTime').reset_index(drop=True)

    print("🖼️ Available webcam times:")
    print(image_df.head())

    # === Extract start and end datetime from webcam images ===
    start_datetime_webcam = image_df['DateTime'].min()
    end_datetime_webcam = image_df['DateTime'].max()

    print(f"📅 Webcam images range from {start_datetime_webcam} to {end_datetime_webcam}")

    # === Find common timestamps between webcam and weather data ===
    print(full_weather_data.head())
    weather_times = full_weather_data['MESS_DATUM']
    print(weather_times[0])
    image_times = image_df['DateTime']
    print(image_times[0])

    common_times = sorted(set(weather_times) & set(image_times))

    if not common_times:
        print("⚠️ No overlapping datetimes found between images and weather data.")
        return None, None, None, None

    # === Filter both datasets to keep only common timestamps ===
    image_df = image_df[image_df['DateTime'].isin(common_times)].reset_index(drop=True)
    weather_filtered = full_weather_data[full_weather_data['MESS_DATUM'].isin(common_times)].reset_index(drop=True)
    
    print(weather_filtered.dtypes)

    # # Optional: limit to N frames (for preview/testing)
    # if frames and len(image_df) > frames:
    #     image_df = image_df.iloc[:frames]
    #     valid_times = image_df['DateTime']
    #     weather_filtered = weather_filtered[weather_filtered['MESS_DATUM'].isin(valid_times)].reset_index(drop=True)

    return image_df, weather_filtered, start_datetime_webcam, end_datetime_webcam



def generate_weather_animation(station_name, image_df, full_weather_data, base_path, output_file_name,frames,fps):
    image_df = image_df.sort_values(by='DateTime').reset_index(drop=True)
    full_weather_data = full_weather_data.sort_values(by='MESS_DATUM').reset_index(drop=True)
    # Increase animation embedding limit
    plt.rcParams['animation.embed_limit'] = 100
    
    """Plots the weather animation."""
    # Stabilize y-axis limits
    pressure_ylim = [full_weather_data['PP_10'].min() - 1, full_weather_data['PP_10'].max() + 1]
    temperature_ylim = [full_weather_data['TT_10'].min() - 1, full_weather_data['TT_10'].max() + 1]
    precipitation_ylim = [0, full_weather_data['RWS_10'].max() + 1]
    wind_ylim = [full_weather_data['FF_10'].min() - 1, full_weather_data['FF_10'].max() + 1]

    # Initialize the figure
    # fig, (ax_webcam, ax_pressure, ax_temperature) = plt.subplots(
    #     3, 1, figsize=(10, 16), gridspec_kw={'height_ratios': [5, 2, 2]}
    # )
    fig, (ax_webcam, ax_pressure, ax_temperature) = plt.subplots(
        3, 1, figsize=(10, 16), gridspec_kw={'height_ratios': [5, 2, 2]}
    )
    plt.subplots_adjust(hspace=0.3)

    # Plot full data lines initially up to the number of frames
    subset_weather_data = full_weather_data.iloc[:frames]

    # Plot pressure and wind speed in first subplot
    ax_pressure.plot(
        subset_weather_data['MESS_DATUM'], subset_weather_data['PP_10'],
        label="Pressure (hPa)", color='blue', linewidth=2
    )
    ax_pressure.set_ylim(pressure_ylim)
    ax_pressure.set_ylabel("Pressure (hPa)")
    ax_wind = ax_pressure.twinx()
    ax_wind.plot(
        subset_weather_data['MESS_DATUM'], subset_weather_data['FF_10'],
        label="Wind speed (m/s)", color='green', linestyle="--", linewidth=2
    )
    ax_wind.set_ylim(wind_ylim)
    ax_wind.set_ylabel("Wind Speed (m/s)")

    # Plot temperature and precipitation in second subplot
    ax_temperature.plot(
        subset_weather_data['MESS_DATUM'], subset_weather_data['TT_10'],
        label="Temperature (°C)", color='orange', linewidth=2
    )
    ax_temperature.set_ylim(temperature_ylim[0])
    ax_temperature.set_ylabel("Temperature (°C)")

    ax_precipitation = ax_temperature.twinx()
    ax_precipitation.plot(
        subset_weather_data['MESS_DATUM'], subset_weather_data['RWS_10'],
        label="Precipitation (mm)", color='green', linestyle="--", linewidth=2
    )
    ax_precipitation.set_ylim(precipitation_ylim)
    ax_precipitation.set_ylabel("Precipitation (mm)")

    ax_pressure.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax_temperature.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Initialize scatter points for red dots
    pressure_scatter = ax_pressure.scatter([], [], color='red', s=50)
    wind_scatter = ax_wind.scatter([], [], color='red', s=50, label='Current Time')
    temperature_scatter = ax_temperature.scatter([], [], color='red', s=50)
    precipitation_scatter = ax_precipitation.scatter([], [], color='red', s=50, label='Current Time')

    # Create a combined legend for pressure, precipitation, and current time
    lines_pressure, labels_pressure = ax_pressure.get_legend_handles_labels()
    lines_wind, labels_wind = ax_wind.get_legend_handles_labels()
    ax_pressure.legend(lines_pressure+ lines_wind , labels_pressure+labels_wind , loc='upper left')
    
    # Create a combined legend for temperature, dewpoint, and current time
    lines_temperature, labels_temperature = ax_temperature.get_legend_handles_labels()
    lines_precipitation, labels_precipitation = ax_precipitation.get_legend_handles_labels()
    ax_temperature.legend(lines_temperature + lines_precipitation, labels_temperature + labels_precipitation , loc='upper left')

    # Function to update the animation
    def update_plot(frame):
        print(f"frame {frame} generated")
        current_time = image_df.iloc[frame]['DateTime']

        # Webcam Image Display
        ax_webcam.clear()
        date_str = current_time.strftime('%Y%m%d')
        time_str = current_time.strftime('%H%M')

        image_path = os.path.join(base_path, f"{station_name}_{date_str}_{time_str}.jpg")

        if os.path.exists(image_path):
            img = Image.open(image_path)
            ax_webcam.imshow(img)
            ax_webcam.axis('off')
            ax_webcam.set_title(f"Webcam Image\n{(current_time + pd.Timedelta(hours=1)):%H:%M} CET", fontsize=14)

        # Filter weather data up to current time
        weather_data = subset_weather_data[subset_weather_data['MESS_DATUM'] <= current_time]
        if not weather_data.empty:
            latest_data_point = weather_data.iloc[-1]
            latest_time_num = mdates.date2num(latest_data_point['MESS_DATUM'])

            # Update scatter points
            pressure_scatter.set_offsets([[latest_time_num, latest_data_point['PP_10']]])
            wind_scatter.set_offsets([[latest_time_num, latest_data_point['FF_10']]])
            temperature_scatter.set_offsets([[latest_time_num, latest_data_point['TT_10']]])
            precipitation_scatter.set_offsets([[latest_time_num, latest_data_point['RWS_10']]])

    # Create the animation
    interval = 500
    writer = FFMpegWriter(fps=fps, bitrate=5000)  # You can try 5000–10000 for high quality

    ani = animation.FuncAnimation(fig, update_plot, frames=frames, interval=interval, blit=False)
    ani.save(output_file_name, writer=writer, dpi=200)

    display(HTML(ani.to_jshtml()))



def read_station_data(file_path):
    print(f"Reading data from {file_path}...")

    # Read data normally (let pandas infer types)
    df = pd.read_csv(file_path, sep=';', skipinitialspace=True)

    # Manually parse the datetime column
    df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format="%Y%m%d%H%M", errors='coerce')

    print(f"Data successfully loaded. Shape: {df.shape}")
    print(df.dtypes)  # Optional: check column types
    return df

