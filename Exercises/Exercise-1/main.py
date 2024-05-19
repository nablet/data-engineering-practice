import requests
import os
import asyncio
from utils.utils import extract_csv_from_zip
from httpclientsession.httpclientsession import AioHttpSession
from concurrent.futures import ThreadPoolExecutor


download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

DOWNLOAD_FOLDER = "downloads"


def main():
    aiohttp = AioHttpSession()

    # Create downloads dir
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)

    # Download files
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        coroutines = [aiohttp.download_file(uri, DOWNLOAD_FOLDER) for uri in download_uris]
        downloaded_files = loop.run_until_complete(asyncio.gather(*coroutines))
    aiohttp.close()

    # Unzip downloaded files, will also delete after
    for file_path in downloaded_files:
        extract_csv_from_zip(file_path, DOWNLOAD_FOLDER)



if __name__ == "__main__":
    main()
