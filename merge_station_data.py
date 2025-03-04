from functions.video_funcs_1 import generate_weather_animation, read_station_data, load_weather_and_image_data
from pathlib import Path

BASE_DIR = Path(__file__).parent
print('Base directory is:', BASE_DIR)
WEATHER_DATA_DIR = BASE_DIR / "weatherdata"

# Define input weather data files
WEATHER_FILE_TEMP = WEATHER_DATA_DIR / "produkt_zehn_min_tu_20230828_20250227_07431.txt"
WEATHER_FILE_WIND = WEATHER_DATA_DIR / "produkt_zehn_min_ff_20230831_20250302_07341.txt"
WEATHER_FILE_PRECIP = WEATHER_DATA_DIR / "produkt_zehn_min_rr_20230831_20250302_07341.txt"

# Read the data
print("Loading weather data...")
df_temp = read_station_data(str(WEATHER_FILE_TEMP))
df_wind = read_station_data(str(WEATHER_FILE_WIND))
df_precip = read_station_data(str(WEATHER_FILE_PRECIP))

# Ensure 'MESS_DATUM' exists and concatenate
if 'MESS_DATUM' in df_temp.columns and 'MESS_DATUM' in df_wind.columns and 'MESS_DATUM' in df_precip.columns:
    df_merged = df_temp.merge(df_wind, on='MESS_DATUM', how='outer').merge(df_precip, on='MESS_DATUM', how='outer')
    merged_file_path = WEATHER_DATA_DIR / "merged_weather_data.txt"
    df_merged.to_csv(merged_file_path, sep=';', index=False)
    print(f"Merged weather data saved at: {merged_file_path}")
else:
    print("Error: 'MESS_DATUM' column not found in one or more dataframes.")
