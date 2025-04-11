import requests
import os
import zipfile
from datetime import datetime, timedelta

def download_webcam_images(station, res, output_path):
    stations = [station]

    # get current date and two days before
    date_today = datetime.today()
    date_yesterday = date_today - timedelta(days=1)
    date_before_yesterday = date_today - timedelta(days=2)
    dates = [date_today.strftime('%Y%m%d'),
             date_yesterday.strftime('%Y%m%d'),
             date_before_yesterday.strftime('%Y%m%d')]

    # 10-min interval
    dt = 10
    times = [
        f'{str(i).zfill(4)}'
        for i in range(0, 2400, dt)
        if i % 100 not in [60, 70, 80, 90]
    ]

    downloaded_datetimes = []

    os.makedirs(output_path, exist_ok=True)

    for s in stations:
        for d in dates:
            for t in times:
                file_path = os.path.join(output_path, f"{s}_{d}_{t}.jpg")
                url = f"https://opendata.dwd.de/weather/webcam/{s}/{s}_{d}_{t}_{res}.jpg"

                if os.path.exists(file_path):
                    continue

                try:
                    response = requests.get(url, timeout=10)
                    if len(response.content) > 1024:
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        print(f"Downloaded: {file_path}")

                        dt_str = f"{d}{t}"
                        dt_obj = datetime.strptime(dt_str, "%Y%m%d%H%M")
                        downloaded_datetimes.append(dt_obj)
                except Exception as e:
                    print(f"⚠️ Failed to download {url}: {e}")

    print('✅ Finished downloading webcam images')

    # If no new downloads, try to infer from existing files
    if not downloaded_datetimes:
        existing_files = [
            f for f in os.listdir(output_path)
            if f.startswith(station) and f.endswith('.jpg')
        ]

        for fname in existing_files:
            try:
                parts = fname.replace('.jpg', '').split('_')
                date_str = parts[1]
                time_str = parts[2]
                dt_str = f"{date_str}{time_str}"
                dt_obj = datetime.strptime(dt_str, "%Y%m%d%H%M")
                downloaded_datetimes.append(dt_obj)
            except Exception as e:
                print(f"⚠️ Skipping malformed filename: {fname} ({e})")

    if downloaded_datetimes:
        return min(downloaded_datetimes), max(downloaded_datetimes)
    else:
        print("⚠️ No webcam images found.")
        return None, None





# --- Function to download station data from DWD Website for today 'now' or last years 'recent'
def download_station_data(station_id, output_path, type):
    """
    Downloads the latest weather station data for the given station ID,
    extracts the zip files, and removes the original zip files.
    """
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Define DWD base directory
    dwd_base_dir = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/'
    
    if type == 'recent':
        suffix = 'akt'
    elif type == 'now':
        suffix = 'now'
    else:
        print(f"Error: type in download_station_data not supported, only 'now' or 'recent' available!")
    # URLs for different data types
    data_sources = {
        "temp": f"{dwd_base_dir}air_temperature/" + type + f"/10minutenwerte_TU_{station_id}_" + suffix + ".zip",
        "precip": f"{dwd_base_dir}precipitation/" + type + f"/10minutenwerte_nieder_{station_id}_" + suffix + ".zip",
        "wind": f"{dwd_base_dir}wind/" + type + f"/10minutenwerte_wind_{station_id}_" + suffix + ".zip",
    }
    
    for data_type, url in data_sources.items():
        zip_file_path = output_path / f"{data_type}.zip"
        
        # Download file
        response = requests.get(url)
        if response.status_code == 200:
            with open(zip_file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {zip_file_path}")
        else:
            print(f"Failed to download {url}")
            continue
        
        # Extract the zip file
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(output_path)
            print(f"Extracted: {zip_file_path}")
        except zipfile.BadZipFile:
            print(f"Error: Corrupt zip file {zip_file_path}")
            continue
        
        # Delete the zip file
        os.remove(zip_file_path)
        print(f"Deleted: {zip_file_path}")




