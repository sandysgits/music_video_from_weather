import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from PIL import Image
import pandas as pd
from IPython.display import display, HTML

def generate_weather_animation(df, base_path, frames=5, interval=500):
    """
    Generates and displays an animated weather plot based on webcam images and weather data.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing weather data with 'MESS_DATUM', 'PP_10', 'RF_10', 'TT_10', and 'TD_10'.
        base_path (str): Path to the directory containing webcam images.
        frames (int): Number of frames to animate.
        interval (int): Interval between frames in milliseconds.
    """
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

    # Filter for the most recent day
    most_recent_day = image_df['DateTime'].dt.date.max()
    image_df = image_df[image_df['DateTime'].dt.date == most_recent_day]

    # Load weather data
    full_weather_data = df[df['MESS_DATUM'].dt.date == most_recent_day]

    # Stabilize y-axis limits
    pressure_ylim = [df['PP_10'].min() - 1, df['PP_10'].max() + 1]
    temperature_ylim = [df['TT_10'].min() - 1, df['TT_10'].max() + 1]
    humidity_ylim = [df['RF_10'].min() - 5, df['RF_10'].max() + 5]
    dewpoint_ylim = [df['TD_10'].min() - 1, df['TD_10'].max() + 1]

    # Initialize the figure
    fig, (ax_webcam, ax_pressure, ax_temperature) = plt.subplots(
        3, 1, figsize=(10, 16), gridspec_kw={'height_ratios': [5, 2, 2]}
    )
    plt.subplots_adjust(hspace=0.3)

    # Subset the weather data to match frame count
    subset_weather_data = full_weather_data.iloc[:frames]

    # Plot data
    ax_pressure.plot(subset_weather_data['MESS_DATUM'], subset_weather_data['PP_10'], label="Pressure (hPa)", color='blue', linewidth=2)
    ax_pressure.set_ylim(pressure_ylim)
    ax_pressure.set_ylabel("Pressure (hPa)")
    ax_humidity = ax_pressure.twinx()
    ax_humidity.plot(subset_weather_data['MESS_DATUM'], subset_weather_data['RF_10'], label="Humidity (%)", color='green', linestyle="--", linewidth=2)
    ax_humidity.set_ylim(humidity_ylim)
    ax_humidity.set_ylabel("Humidity (%)")
    ax_temperature.plot(subset_weather_data['MESS_DATUM'], subset_weather_data['TT_10'], label="Temperature (°C)", color='orange', linewidth=2)
    ax_temperature.plot(subset_weather_data['MESS_DATUM'], subset_weather_data['TD_10'], label="Dewpoint (°C)", color='purple', linestyle="--", linewidth=2)
    ax_temperature.set_ylim(dewpoint_ylim[0], temperature_ylim[1])
    ax_temperature.set_ylabel("Temperature (°C)")
    ax_pressure.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax_temperature.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Initialize scatter points
    pressure_scatter = ax_pressure.scatter([], [], color='red', s=50)
    humidity_scatter = ax_humidity.scatter([], [], color='red', s=50, label='Current Time')
    temperature_scatter = ax_temperature.scatter([], [], color='red', s=50, label='Current Time')
    dewpoint_scatter = ax_temperature.scatter([], [], color='red', s=50)

    # Legends
    lines_pressure, labels_pressure = ax_pressure.get_legend_handles_labels()
    lines_humidity, labels_humidity = ax_humidity.get_legend_handles_labels()
    ax_pressure.legend(lines_pressure + lines_humidity, labels_pressure + labels_humidity, loc='upper left')
    lines_temperature, labels_temperature = ax_temperature.get_legend_handles_labels()
    ax_temperature.legend(lines_temperature, labels_temperature, loc='upper left')

    # Function to update animation
    def update_plot(frame):
        current_time = image_df.iloc[frame]['DateTime']
        ax_webcam.clear()
        date_str = current_time.strftime('%Y%m%d')
        time_str = current_time.strftime('%H%M')
        image_path = os.path.join(base_path, f"Offenbach-W_{date_str}_{time_str}.jpg")
        if os.path.exists(image_path):
            img = Image.open(image_path)
            ax_webcam.imshow(img)
            ax_webcam.axis('off')
            ax_webcam.set_title(f"Webcam Image\n{(current_time + pd.Timedelta(hours=1)):%H:%M} CET", fontsize=14)
        weather_data = subset_weather_data[subset_weather_data['MESS_DATUM'] <= current_time]
        if not weather_data.empty:
            latest_data_point = weather_data.iloc[-1]
            latest_time_num = mdates.date2num(latest_data_point['MESS_DATUM'])
            pressure_scatter.set_offsets([[latest_time_num, latest_data_point['PP_10']]])
            humidity_scatter.set_offsets([[latest_time_num, latest_data_point['RF_10']]])
            temperature_scatter.set_offsets([[latest_time_num, latest_data_point['TT_10']]])
            dewpoint_scatter.set_offsets([[latest_time_num, latest_data_point['TD_10']]])

    ani = animation.FuncAnimation(fig, update_plot, frames=frames, interval=interval, blit=False)
    ani.save("weather_animation_2.mp4", writer="ffmpeg", fps=3)
    #display(HTML(ani.to_jshtml()))

def read_station_data(file_path):
    # Read the data into a pandas DataFrame
    print(f"Reading data from {file_path}...")
    df = pd.read_csv(file_path, sep=';', parse_dates=['MESS_DATUM'], dayfirst=True)
    print(f"Data successfully loaded. Shape: {df.shape}")
    return df


