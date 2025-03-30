import os
import re
from datetime import datetime, timedelta
import shutil

# --- Configuration ---

source_folder = r"C:/Users/Frank/Documents/python/weather_webcam_sonification/Offenbach-W-20250324T081425Z-001/Offenbach-W"  # change this to your folder path
destination_folder = os.path.join(source_folder, 'longest_series')
filename_pattern = r'Offenbach-W_(\d{8}_\d{4})'

# --- Step 1: Get all valid files with timestamps ---
files_with_timestamps = []

for filename in os.listdir(source_folder):
    match = re.match(filename_pattern, filename)
    if match:
        timestamp_str = match.group(1)
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M')
        files_with_timestamps.append((timestamp, filename))

# Sort files by timestamp
files_with_timestamps.sort()

# --- Step 2: Find the longest continuous sequence (10-min steps) ---
longest_sequence = []
current_sequence = []

for i in range(len(files_with_timestamps)):
    if not current_sequence:
        current_sequence.append(files_with_timestamps[i])
    else:
        last_time = current_sequence[-1][0]
        next_time = files_with_timestamps[i][0]
        if next_time - last_time == timedelta(minutes=10):
            current_sequence.append(files_with_timestamps[i])
        else:
            if len(current_sequence) > len(longest_sequence):
                longest_sequence = current_sequence
            current_sequence = [files_with_timestamps[i]]

# Edge case: last sequence might be longest
if len(current_sequence) > len(longest_sequence):
    longest_sequence = current_sequence

# --- Step 3: Move files to new folder ---
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for _, filename in longest_sequence:
    src_path = os.path.join(source_folder, filename)
    dst_path = os.path.join(destination_folder, filename)
    shutil.move(src_path, dst_path)

print(f"Moved {len(longest_sequence)} files to '{destination_folder}'")
