# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.demoblaze.com/")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.demoblaze.com/")
BROWSER = os.getenv("BROWSER", "chrome")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

# URLs des pages
HOME_URL = f"{BASE_URL}/index.html"
CART_URL = f"{BASE_URL}/cart.html"

# ── Navigateur ─────────────────────────────────────────────
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# ── Timeouts ───────────────────────────────────────────────
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "30"))

# ── Credentials ────────────────────────────────────────────
TEST_USERNAME = os.getenv("TEST_USERNAME", "")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")


# ── User Credentials ────────────────────────────────────────
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
