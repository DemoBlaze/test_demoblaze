import os
import sys

# Modification du path avant l'import de config.drivers
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.drivers import get_driver  # noqa: E402

driver = get_driver()
driver.get("https://www.google.com")
print("Titre :", driver.title)
driver.quit()
print("Selenium OK")
