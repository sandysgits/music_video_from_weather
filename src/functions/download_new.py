import requests
import os
import zipfile
from datetime import datetime, timedelta

def download_webcam_images_now(station, res, output_path):

    stations = [station]

    # get current date and days before
    # date_today = datetime.today()
    # date_yesterday = date_today - timedelta(days=1)
    # date_before_yesterday = date_today - timedelta(days=2)
    # dates = [date_today.strftime('%Y%m%d'),date_yesterday.strftime('%Y%m%d'),
    #             date_before_yesterday.strftime('%Y%m%d')]

    date_today = datetime.today().strftime('%Y%m%d')
    dates = [date_today]

    # create time string
    dt = 10 # for hourly data or 10 for 10 mins data
    times = [f'{str(i).zfill(4)}' for i in range(0, 2400, dt) if i % 100 != 70 and i % 100 != 90 and i % 100 != 80 and i % 100 != 60]

    # Loop over all stations and dates to download all images
    for s in stations:
        for d in dates:
            for t in times:
                # Define the path and URL
            
                file_path = os.path.join(output_path, f"{s}_{d}_{t}.jpg")
                url = f"https://opendata.dwd.de/weather/webcam/{s}/{s}_{d}_{t}_{res}.jpg"

                # Create the directory if it doesn't exist
                os.makedirs(output_path, exist_ok=True)

                # Check if file already exists
                if os.path.exists(file_path):
                # print(f"File already exists, skipping: {file_path}")
                    continue

                # Send a GET request to the URL
                response = requests.get(url)

                # Check if the image exists (>1024 bytes), if yes, download
                if len(response.content) > 1024:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded: {file_path}")


        print('Downloaded all webcam images')
    return

def download_station_data_now(station_id, output_path):
    """
    Downloads the latest weather station data for the given station ID,
    extracts the zip files, and removes the original zip files.
    """
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Define DWD base directory
    dwd_base_dir = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/'
    
    # URLs for different data types
    data_sources = {
        "temp": f"{dwd_base_dir}air_temperature/now/10minutenwerte_TU_{station_id}_now.zip",
        "precip": f"{dwd_base_dir}precipitation/now/10minutenwerte_nieder_{station_id}_now.zip",
        "wind": f"{dwd_base_dir}wind/now/10minutenwerte_wind_{station_id}_now.zip",
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



def download_station_data_historic(station_id, output_path):
    """
    Downloads the latest weather station data for the given station ID,
    extracts the zip files, and removes the original zip files.
    """
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Define DWD base directory
    dwd_base_dir = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/'
    
    # URLs for different data types
    data_sources = {
        "temp": f"{dwd_base_dir}air_temperature/recent/10minutenwerte_TU_{station_id}_akt.zip",
        "precip": f"{dwd_base_dir}precipitation/recent/10minutenwerte_nieder_{station_id}_akt.zip",
        "wind": f"{dwd_base_dir}wind/recent/10minutenwerte_wind_{station_id}_akt.zip",
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



