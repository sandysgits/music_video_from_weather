import requests
import zipfile
import io
import os
import pandas as pd
from datetime import datetime

def download_files(start_date, end_date):
    # URL-Basis für die Dateien
    BASE_URL = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/historical/"

    """Lädt alle relevanten Dateien herunter und gibt die entpackten Dateien zurück."""
    files_downloaded = []
    response = requests.get(BASE_URL)
    print("0")
    
    # Check if base URL is accessible
    if response.status_code != 200:
        print("Fehler beim Zugriff auf die Webseite.")
        return files_downloaded
    
    # Extract years from the start and end dates
    start_year = start_date.year
    end_year = end_date.year

    # Determine which files to download based on the year range
    files_to_download = set()
    print("1")
    # Check for each year range and add the relevant file if the range is covered
    if 2020 <= start_year <= 2023 or 2020 <= end_year <= 2023:
        files_to_download.add("10minutenwerte_TU_07431_20200101_20231231_hist.zip")
    if 2010 <= start_year < 2020 or 2010 <= end_year < 2020:
        files_to_download.add("10minutenwerte_TU_07431_20100101_20191231_hist.zip")
    if 2007 <= start_year < 2010 or 2007 <= end_year < 2010:
        files_to_download.add("10minutenwerte_TU_07431_20071101_20091231_hist.zip")

    # If there are files to download, simulate downloading them
    if files_to_download:
        for file_name in files_to_download:
            print(f"Downloading {file_name} for the date range {start_date} to {end_date}")
            # URL zur Datei erstellen
            file_url = f"{BASE_URL}{file_name}"
            print(f"Lade {file_url} herunter...")
            response = requests.get(file_url)
            if response.status_code == 200:
                # ZIP-Datei entpacken
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                    for file in zip_ref.namelist():
                        # Speichere die entpackte Datei temporär
                        zip_ref.extract(file, ".")
                        files_downloaded.append(file)
                        print(f"Entpackt: {file}")
            else:
                print(f"Datei {file_url} konnte nicht heruntergeladen werden.")
    else:
        print("The specified date range does not match any available files.")                
    
    return files_downloaded

def load_and_combine_data(files_downloaded, start_date, end_date):
    """Lädt die heruntergeladenen Dateien, kombiniert sie und filtert den Zeitraum."""
    data_frames = []
    for file in files_downloaded:
        # Lade CSV-Datei und speichere sie in einem DataFrame
        df = pd.read_csv(file, sep=';', skipinitialspace=True)
        
        # Filtere Datumsspalte nach dem gewünschten Zeitraum
        df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H%M')
        df = df[(df['MESS_DATUM'] >= start_date) & (df['MESS_DATUM'] <= end_date)]
        
        # Füge gefiltertes DataFrame zur Liste hinzu
        data_frames.append(df)
    
    # Kombiniere alle DataFrames
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    # Sortiere nach Datum (falls erforderlich) und entferne Duplikate
    combined_df = combined_df.sort_values(by='MESS_DATUM').drop_duplicates().reset_index(drop=True)
    return combined_df

def data_main(start_time_str, end_time_str):
    # Konvertiere Eingaben in datetime-Objekte
    start_date = datetime.strptime(start_time_str, '%Y%m%d%H%M')
    end_date = datetime.strptime(end_time_str, '%Y%m%d%H%M')
    
    # Lade die Dateien für den Zeitraum herunter und entpacke sie
    files_downloaded = download_files(start_date, end_date)
    print(files_downloaded)
    
    # Lade die Daten und filtere den Zeitraum
    combined_data = load_and_combine_data(files_downloaded, start_date, end_date)
    
    # Entferne die heruntergeladenen Dateien
    for file in files_downloaded:
        os.remove(file)
    
    # Gebe das kombinierte DataFrame zurück
    return combined_data