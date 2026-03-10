# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# ── URLs ───────────────────────────────────────────────────
# strip("/") évite le double slash si BASE_URL a un trailing slash
BASE_URL = os.getenv("BASE_URL", "https://www.demoblaze.com").rstrip("/")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.demoblaze.com").rstrip("/")

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

TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
