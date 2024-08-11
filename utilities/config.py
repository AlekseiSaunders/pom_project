# config.py

import os
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# URLs
QA_BASE_URL = "https://wildxr-cm-qa.azurewebsites.net/"
# LOGIN_URL = f'{BASE_URL}/login'

# WebDrivers
CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH', os.path.join(BASE_DIR, 'webdrivers', 'chromedriver.exe'))
EDGE_DRIVER_PATH = os.environ.get('EDGE_DRIVER_PATH', os.path.join(BASE_DIR, 'webdrivers', 'msedgedriver.exe'))
FIREFOX_DRIVER_PATH = os.environ.get('GECKO_DRIVER_PATH', os.path.join(BASE_DIR, 'webdrivers', 'geckodriver.exe'))

#  Validate WebDriver paths
# for driver_name, driver_path in [
#     ("chrome", CHROME_DRIVER_PATH),
#     ("firefox", FIREFOX_DRIVER_PATH),
#     ("edge", EDGE_DRIVER_PATH)
# ]:
#     if not os.path.exists(driver_path):
#         raise FileNotFoundError(f"{driver_name} WebDriver not found at {driver_path}. Please check your WebDriver path settings.")

# Screenshot Folder
SCREENSHOT_DIR = os.environ.get('SELENIUM_SCREENSHOT_DIR', os.path.join(BASE_DIR, 'screenshots'))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Upload file folder
FILE_UPLOAD_DIR = os.environ.get("FILE_UPLOAD_DIR", os.path.join(BASE_DIR, 'uploads'))

# Timeouts
DEFAULT_TIMEOUT = 10
EXTENDED_TIMEOUT = 30

# Other constants
MAX_RETRIES = 3

