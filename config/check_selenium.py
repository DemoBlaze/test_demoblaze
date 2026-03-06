import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.drivers import get_driver

driver = get_driver()
driver.get("https://www.google.com")
print("Titre :", driver.title)
driver.quit()
print("Selenium OK")