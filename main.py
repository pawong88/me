import requests
import os
import sys
from pathlib import Path
import datetime
from src.fit_smoke import run_smoke
from src.fit_fire import run_fire
from roboflow import Roboflow

# get current date and time YYYY_MM_DD_HH_MM_SS
now = datetime.datetime.now()
current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

# Base Directory
BASE_DIR = Path(__file__).parent
PARENT_DIR = BASE_DIR.parent

# Make folders at raw_img directory
RAW_IMG = Path(PARENT_DIR, "raw_img")
RAW_IMG.mkdir(parents=True, exist_ok=True)
RAW_IMG_PATH = str(RAW_IMG)

# Make predict img directory
PREDICT_IMG = Path(PARENT_DIR, "predict_img")
PREDICT_IMG.mkdir(parents=True, exist_ok=True)
# get image path of predict_img
PREDICT_IMG_PATH = str(PREDICT_IMG)
url = 'http://192.168.4.1/capture'

# loop response = requests.get(url) for 4 times
for i in range(4):
    response = requests.get(url)

if not os.path.exists(RAW_IMG):
    os.makedirs(RAW_IMG)

if response.status_code == 200:
    print("writing image...")
    PATH_FILE = os.path.join(RAW_IMG, f"img_raw_{current_time}.jpg")
    with open(PATH_FILE, "wb") as f:
        content = response.content
        f.write(content)
        print("Finish writing image...")

run_smoke(RAW_IMG_PATH, PREDICT_IMG_PATH, current_time)
run_fire(RAW_IMG_PATH, PREDICT_IMG_PATH, current_time)

from src.upload_img import upload_img

upload_img(PREDICT_IMG_PATH, current_time)




print("Finish running smoke...")
