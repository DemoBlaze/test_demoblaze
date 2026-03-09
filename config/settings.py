# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.demoblaze.com/")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.demoblaze.com/")
BROWSER = os.getenv("BROWSER", "chrome")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
