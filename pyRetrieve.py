#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-12Dec-01
Modified on 2020-01Jan-21
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to retrieve Florida Inspections and Restaurant License Files.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2025-06-14       RWM        Initial Stub and Layout

'''

version = '0.01.a'
# Import Libraries needed for Scraping the various web pages
import datetime
import csv
import sys
import codecs
import mysql.connector
import requests
import os
from urllib.parse import urljoin

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Set Character Output
print('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Establish MySQL Connection
cnx = mysql.connector.connect(user='root', password='password',
                              host='dewalt',
                              database='restaurants',
                              auth_plugin='mysql_native_password')

# Visible Parsing
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Base Path for Output
localPath = 'D:\\OneDrive - Mdga, Inc\\Restaurants_Florida\\'

def download_file_series(base_url, file_pattern, start_index, end_index, download_dir):
    """
    Downloads a series of files from a URL based on a numeric pattern.

    Args:
        base_url (str): The base URL containing the directory path.
        file_pattern (str): A string pattern for the filename, using {i} as a placeholder
                            for the number. Example: 'hrfood{i}.csv'.
        start_index (int): The starting number for the file sequence.
        end_index (int): The ending number for the file sequence (inclusive).
        download_dir (str): The directory where downloaded files will be saved.
    """
    # --- Input Validation ---
    if not base_url.endswith('/'):
        base_url += '/'
    if start_index < 1:
        print(f"Error: start_index must be 1 or greater for pattern '{file_pattern}'.")
        return
    if end_index < start_index:
        print(f"Error: end_index must be >= start_index for pattern '{file_pattern}'.")
        return

    # --- Create Download Directory ---
    if not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir)
            print(f"Created directory: {download_dir}")
        except OSError as e:
            print(f"Error creating directory {download_dir}: {e}")
            return

    # --- Download Loop ---
    print("\n" + "="*40)
    print(f"Starting Download Series")
    print(f"  Pattern:   {file_pattern}")
    print(f"  Directory: {download_dir}")
    print(f"  Indices:   {start_index} to {end_index}")
    print("="*40)

    session = requests.Session()

    for i in range(start_index, end_index + 1):
        file_name = file_pattern.format(i=i)
        file_url = urljoin(base_url, file_name)
        local_file_path = os.path.join(download_dir, file_name)

        print(f"\nAttempting to download: {file_url}")

        try:
            # Send GET request with stream=True to handle large files potentially
            response = session.get(file_url, stream=True, timeout=30)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '').lower()
                # Check for common CSV/text content types
                if 'csv' in content_type or 'text' in content_type or 'octet-stream' in content_type:
                    with open(local_file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Successfully downloaded and saved: {local_file_path}")
                else:
                    print(f"Skipped: Unexpected content type '{content_type}' for {file_url}")
                    # Clean up the empty file that might have been created
                    if os.path.exists(local_file_path):
                        os.remove(local_file_path)

            elif response.status_code == 404:
                print(f"File not found (404): {file_url}. Stopping this series.")
                break # If one file is missing, assume the sequence ends
            else:
                print(f"Failed to download {file_url}. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error during request for {file_url}: {e}")

    print(f"\n--- Finished Series: {file_pattern} ---")

# --- Execute the download functions ---
if __name__ == "__main__":
    # --- General Configuration ---
    # Base URL where all the files are located
    BASE_DOWNLOAD_URL = 'https://www2.myfloridalicense.com/sto/file_download/extracts/'
    # Main directory to store all downloaded data subfolders
    MAIN_DOWNLOAD_DIRECTORY = "florida_inspection_data"

    # --- Configuration for 'hrfood' files ---
    # Downloads files like hrfood1.csv, hrfood2.csv, etc.
    HRFOOD_CONFIG = {
        "pattern": "hrfood{i}.csv",
        "start": 1,
        "end": 7, # Adjust as needed
        "subdir": "hr_food"
    }

    # --- Configuration for 'fdinspi' files ---
    # Downloads files like 1fdinspi.csv, 2fdinspi.csv, etc.
    FDINSPI_CONFIG = {
        "pattern": "{i}fdinspi.csv",
        "start": 1,
        "end": 7, # Adjust as needed
        "subdir": "fd_inspi"
    }

    # --- Execute Downloads ---
    print("Starting download process for all file series.")

    # 1. Download the 'hrfood' series
    download_file_series(
        base_url=BASE_DOWNLOAD_URL,
        file_pattern=HRFOOD_CONFIG["pattern"],
        start_index=HRFOOD_CONFIG["start"],
        end_index=HRFOOD_CONFIG["end"],
        download_dir=localPath
    )

    # 2. Download the 'fdinspi' series
    download_file_series(
        base_url=BASE_DOWNLOAD_URL,
        file_pattern=FDINSPI_CONFIG["pattern"],
        start_index=FDINSPI_CONFIG["start"],
        end_index=FDINSPI_CONFIG["end"],
        download_dir=localPath
    )

    print("\nAll download processes have been completed.")
