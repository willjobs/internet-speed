import json
import logging
import requests
from datetime import datetime
from pathlib import Path

import dropbox
from dotenv import dotenv_values
from speedtest import Speedtest

config = dotenv_values()
DATA_FILE_NAME = "speed_tests.txt"
DROPBOX_FILE = f"/{DATA_FILE_NAME}"

PROJECT_DIR = Path(__file__).parents[1]
LOCAL_FILE = str(PROJECT_DIR / "data" / DATA_FILE_NAME)
LOG_FILE = str(PROJECT_DIR / "data" / "internet-speed.log")

logger = logging.getLogger("internet_speed")


def setup_logger():
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_my_ip() -> str:
    return requests.get('https://api.ipify.org').content.decode('utf8')


def get_ip_info(ip_address: str) -> str:
    ip_info = json.loads(requests.get(f"https://ipinfo.io/{ip_address}?token={config['IPINFO_API_KEY']}").content.decode("utf8"))
    return f"{ip_info['city']}, {ip_info['org']}"


def get_speed() -> str:
    s = Speedtest()
    logger.info("Running download test...")
    download_bps = s.download()     # Getting download speed
    download_mbps = round(download_bps / 10**6, 1)  # Mbps (bits, not bytes)
    logger.info(f"Done (download = {download_mbps} Mbps). Running upload test...")

    upload_bps = s.upload()     # Getting upload speed
    upload_mbps = round(upload_bps / 10**6, 1)  # Mbps
    logger.info(f"Done (upload = {upload_mbps} Mbps)")

    return f"download = {download_mbps} Mbps  |  upload = {upload_mbps} Mbps"


def get_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def update_dropbox_file(data: str, local_file: str, dropbox_file: str):
    logger.info(f"Saving test results to {local_file}")

    with open(local_file, "a", encoding="utf-8") as f:
        f.write(data)

    try:
        dbx = dropbox.Dropbox(
            app_key=config["DROPBOX_APP_KEY"],
            app_secret=config["DROPBOX_APP_SECRET"],
            oauth2_refresh_token=config["DROPBOX_REFRESH_TOKEN"],
        )
        with open(local_file, "rb") as f:
            _ = dbx.files_upload(f.read(), dropbox_file, mode=dropbox.files.WriteMode("overwrite"))

    except Exception as e:
        logger.error(f"Failed to upload file: {e}")


if __name__ == "__main__":
    setup_logger()
    ip = get_my_ip()
    ip_info = get_ip_info(ip)
    cur_time = get_datetime()
    test_results = get_speed()
    data = f"{cur_time}  |  {ip}  |  {ip_info}  |  {test_results}\n"
    logger.info(f"Saving the following data: {data.strip()}")
    update_dropbox_file(data, LOCAL_FILE, DROPBOX_FILE)
    logger.info("Done!\n")
