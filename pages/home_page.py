from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.settings import HOME_URL, EXPLICIT_WAIT


class HomePage(BasePage):
    """
    Page d'accueil de Demoblaze.
    URL : https://www.demoblaze.com/index.html
    """

    # ── Locators ───────────────────────────────────────────
    LOGO = (By.XPATH, "//a[contains(@class,'navbar-brand') and @href='index.html']")
    NAVBAR = (By.ID, "navbarExample")
    CART_LINK = (By.XPATH, "//a[@href='cart.html']")

    # Grille des produits
    PRODUCT_LIST = (By.ID, "tbodyid")
    PRODUCT_CARDS = (By.XPATH, "//div[@id='tbodyid']//div[contains(@class,'card')]")
    PRODUCT_NAMES = (
        By.XPATH,
        "//div[@id='tbodyid']//h4[contains(@class,'card-title')]//a",
    )
    PRODUCT_PRICES = (By.XPATH, "//div[@id='tbodyid']//h5")

    # Carousel
    CAROUSEL = (By.ID, "carouselExampleIndicators")

    # ── Actions ────────────────────────────────────────────
    def open(self):
        """Ouvre la page d'accueil et attend le chargement des produits."""
        self.go_to(HOME_URL)
        self.wait_for_element(self.PRODUCT_LIST)
        WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.presence_of_all_elements_located(self.PRODUCT_CARDS)
        )
        return self

    def click_logo(self):
        """Clique sur le logo PRODUCT STORE."""
        self.click(self.LOGO)
        return self

    def go_to_cart(self):
        """Navigue vers la page panier via la navbar."""
        self.click(self.CART_LINK)
        self.wait_for_url_contains("cart.html")
        return self

    # ── Vérifications ──────────────────────────────────────
    def is_home_page(self):
        """Vérifie qu'on est bien sur la home via la liste produits."""
        return self.is_displayed(self.PRODUCT_LIST)

    def get_product_cards(self):
        """Retourne la liste des cartes produits affichées."""
        return self.driver.find_elements(*self.PRODUCT_CARDS)

    def get_product_names(self):
        """Retourne la liste des noms de produits."""
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_product_prices(self):
        """Retourne la liste des prix de produits."""
        elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_page_title(self):
        """Retourne le titre de l'onglet du navigateur."""
        return self.driver.title

    def is_carousel_displayed(self):
        """Vérifie que le carousel est affiché."""
        return self.is_displayed(self.CAROUSEL)
