from functions.video_funcs_1 import * #generate_weather_animation, read_station_data, load_weather_and_image_data
from pathlib import Path
import glob

# Define base directory
#BASE_DIR = Path(__file__).parent
BASE_DIR = Path("C:/Users/Frank/Documents/python/weather_webcam_sonification/")
print('Base directory is:', BASE_DIR)
WEATHER_DATA_DIR = BASE_DIR / "weatherdata"

# Define station ID
station_id = "01420"

# Find the latest available weather data files
WEATHER_FILE_TEMP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_tu_*_{station_id}.txt"))[-1]
WEATHER_FILE_WIND = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_ff_*_{station_id}.txt"))[-1]
WEATHER_FILE_PRECIP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_min_rr_*_{station_id}.txt"))[-1]


# Read the data
print("Loading weather data...")
df_temp = read_station_data(str(WEATHER_FILE_TEMP))
df_wind = read_station_data(str(WEATHER_FILE_WIND))
df_precip = read_station_data(str(WEATHER_FILE_PRECIP))

# Ensure all dataframes have the same number of rows
if len(df_temp) == len(df_wind) == len(df_precip):
    # Merge dataframes along columns, keeping only one instance of 'MESS_DATUM' and 'STATIONS_ID'
    df_merged = pd.concat([df_temp, df_wind.drop(columns=['MESS_DATUM', 'STATIONS_ID'], errors='ignore'),
                            df_precip.drop(columns=['MESS_DATUM', 'STATIONS_ID'], errors='ignore')], axis=1)
    
    # Determine the first and last timestamp for the filename and format them
    start_time = df_merged['MESS_DATUM'].iloc[0].strftime('%Y%m%d_%H%M')
    end_time = df_merged['MESS_DATUM'].iloc[-1].strftime('%Y%m%d_%H%M')
    merged_file_path = WEATHER_DATA_DIR / f"merged_weather_data_{start_time}_{end_time}.txt"
    
    df_merged.to_csv(merged_file_path, sep=';', index=False)
    print(f"Merged weather data saved at: {merged_file_path}")
else:
    print("Error: Dataframes have different row counts and cannot be merged.")
