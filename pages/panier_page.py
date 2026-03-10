# pages/panier_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import CART_URL


class PanierPage(BasePage):
    """
    Page panier de Demoblaze.
    URL : https://www.demoblaze.com/cart.html
    """

    # ── Locators ───────────────────────────────────────────
    # Logo identique à la home — même navbar sur toutes les pages
    LOGO = (By.XPATH, "//a[contains(@class,'navbar-brand') and @href='index.html']")
    CART_TABLE = (By.ID, "tbodyid")
    PLACE_ORDER_BTN = (By.XPATH, "//button[contains(text(),'Place Order')]")

    # ── Actions ────────────────────────────────────────────
    def open(self):
        """Ouvre directement la page panier."""
        self.go_to(CART_URL)
        self.wait_for_element(self.LOGO)
        return self

    def click_logo(self):
        """Clique sur le logo depuis la page panier."""
        self.click(self.LOGO)
        return self

    def is_cart_page(self):
        """Vérifie qu'on est bien sur la page panier."""
        return "cart.html" in self.get_current_url()
