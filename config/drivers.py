# config/drivers.py
import os
from selenium import webdriver

def get_driver(browser=None):
    browser = browser or os.getenv("BROWSER", "chrome")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless=new")

        return webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    elif browser == "mobile":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation",
            {"deviceName": "iPhone 12 Pro"})
        return webdriver.Chrome(options=options)

    else:
        raise ValueError(f"Navigateur non supporté : {browser}")