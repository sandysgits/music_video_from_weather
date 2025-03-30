from functions.video_funcs_1 import * #generate_weather_animation, read_station_data, load_weather_and_image_data
from pathlib import Path
import glob

# Define base directory
#BASE_DIR = Path(__file__).parent
BASE_DIR = Path("C:/Users/Frank/Documents/python/weather_webcam_sonification/")
print('Base directory is:', BASE_DIR)
WEATHER_DATA_DIR = BASE_DIR / "weatherdata" / "07341_now"

# Define station ID
station_id = '07341'

# Find the latest available weather data files
WEATHER_FILE_TEMP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_tu_*_{station_id}.txt"))[-1]
WEATHER_FILE_WIND = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_ff_*_{station_id}.txt"))[-1]
WEATHER_FILE_PRECIP = sorted(WEATHER_DATA_DIR.glob(f"produkt_zehn_now_rr_*_{station_id}.txt"))[-1]


# Read the data
print("Loading weather data...")
df_temp = read_station_data(str(WEATHER_FILE_TEMP))
df_wind = read_station_data(str(WEATHER_FILE_WIND))
df_precip = read_station_data(str(WEATHER_FILE_PRECIP))

# Merge only on common 'MESS_DATUM' values
common_dates = set(df_temp['MESS_DATUM']) & set(df_wind['MESS_DATUM']) & set(df_precip['MESS_DATUM'])

# Filter each dataframe to include only rows with common 'MESS_DATUM'
df_temp_filtered = df_temp[df_temp['MESS_DATUM'].isin(common_dates)]
df_wind_filtered = df_wind[df_wind['MESS_DATUM'].isin(common_dates)]
df_precip_filtered = df_precip[df_precip['MESS_DATUM'].isin(common_dates)]

# Perform inner merge on 'MESS_DATUM'
df_merged = df_temp_filtered.merge(df_wind_filtered, on='MESS_DATUM', how='inner', suffixes=('', '_wind'))
df_merged = df_merged.merge(df_precip_filtered, on='MESS_DATUM', how='inner', suffixes=('', '_precip'))

# Remove duplicate 'STATIONS_ID' columns if present
df_merged = df_merged.loc[:, ~df_merged.columns.duplicated()]

# Determine the first and last timestamp for the filename and format them
start_time = df_merged['MESS_DATUM'].iloc[0].strftime('%Y%m%d_%H%M')
end_time = df_merged['MESS_DATUM'].iloc[-1].strftime('%Y%m%d_%H%M')
merged_file_path = WEATHER_DATA_DIR / f"merged_weather_data_{start_time}_{end_time}_{station_id}.txt"

df_merged.to_csv(merged_file_path, sep=';', index=False)
print(f"Merged weather data saved at: {merged_file_path}")

