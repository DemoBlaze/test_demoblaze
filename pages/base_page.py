from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.support import expected_conditions as EC
from config.settings import EXPLICIT_WAIT


class BasePage:
    """
    Classe de base pour toutes les pages.
    Contient les méthodes communes Selenium.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    # ── Navigation ─────────────────────────────────────────
    def go_to(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title

    # ── Attentes explicites ────────────────────────────────
    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_url_contains(self, text):
        return self.wait.until(EC.url_contains(text))

    def wait_for_url_to_be(self, url):
        return self.wait.until(EC.url_to_be(url))

    # ── Interactions ───────────────────────────────────────
    def click(self, locator):
        for attempt in range(3):
            try:
                element = self.wait_for_clickable(locator)
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == 2:
                    raise

    def find(self, locator):
        return self.wait_for_element(locator)

    def is_displayed(self, locator):
        try:
            return self.wait_for_element(locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
