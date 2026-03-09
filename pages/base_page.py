# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.settings import TIMEOUT


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def open(self, url):
        self.driver.get(url)

    def wait_for(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def clear_and_type(self, locator, text):
        el = self.wait_for(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.wait_for(locator).text

    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def find(self, locator):
        return self.wait_for(locator)
