from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.settings import HOME_URL


class HomePage(BasePage):
    """
    Page d'accueil de Demoblaze.
    URL : https://www.demoblaze.com/index.html
    """

    # ── Locators ───────────────────────────────────────────
    LOGO = (By.CSS_SELECTOR, "a.navbar-brand")  # FIX 3
    NAVBAR = (By.ID, "navbarExample")
    CART_LINK = (By.XPATH, "//a[@href='cart.html']")

    PRODUCT_LIST = (By.ID, "tbodyid")
    PRODUCT_CARDS = (By.XPATH, "//div[@id='tbodyid']//div[contains(@class,'card')]")
    PRODUCT_NAMES = (
        By.XPATH,
        "//div[@id='tbodyid']//h4[contains(@class,'card-title')]//a",
    )
    PRODUCT_PRICES = (By.XPATH, "//div[@id='tbodyid']//h5")
    CAROUSEL = (By.ID, "carouselExampleIndicators")

    # ── Actions ────────────────────────────────────────────
    def open(self):
        """Ouvre la page d'accueil et attend le chargement des produits."""
        self.go_to(HOME_URL)
        self.wait_for_element(self.PRODUCT_LIST)
        self.wait.until(  # FIX 1
            EC.visibility_of_all_elements_located(self.PRODUCT_CARDS)
        )
        return self

    def click_logo(self):
        self.click(self.LOGO)
        return self

    def go_to_cart(self):
        self.click(self.CART_LINK)
        self.wait_for_url_contains("cart.html")
        return self

    # ── Vérifications ──────────────────────────────────────
    def is_home_page(self):
        return self.is_displayed(self.PRODUCT_LIST)

    def get_product_cards(self):  # FIX 2
        self.wait.until(EC.visibility_of_all_elements_located(self.PRODUCT_CARDS))
        return self.driver.find_elements(*self.PRODUCT_CARDS)

    def get_product_names(self):  # FIX 2
        self.wait.until(EC.visibility_of_all_elements_located(self.PRODUCT_NAMES))
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_product_prices(self):  # FIX 2
        self.wait.until(EC.visibility_of_all_elements_located(self.PRODUCT_PRICES))
        elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_page_title(self):
        return self.driver.title

    def is_carousel_displayed(self):
        return self.is_displayed(self.CAROUSEL)
