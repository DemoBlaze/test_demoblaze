import requests
from behave import given, when
from pages.home_page import HomePage
from pages.panier_page import PanierPage
from config.settings import BASE_URL

# ── Fonctions utilitaires partagées ────────────────────────────────────────────


def find_product(context, search_name):
    """
    Cherche un produit par nom dans context.products.
    Retourne le dict produit ou lève une AssertionError.
    """
    assert (
        hasattr(context, "products") and context.products
    ), "context.products est vide — utilisez le Given 'le catalogue de produits est chargé depuis l'API'."
    search_lower = search_name.lower()
    for name, product in context.products.items():
        if search_lower in name.lower():
            return product
    raise AssertionError(
        f"Produit '{search_name}' introuvable dans le catalogue.\n"
        f"Produits disponibles : {list(context.products.keys())}"
    )


def compute_total(cart):
    """
    Calcule le total du panier.
    Chaque item est un dict avec 'price' (float) et 'qty' (int).
    """
    return round(sum(item["price"] * item["qty"] for item in cart), 2)


# ── Steps catalogue ────────────────────────────────────────────────────────────


@given("le catalogue de produits est chargé depuis l'API")
def step_load_catalogue(context):
    """
    Charge le catalogue depuis https://api.demoblaze.com/entries
    et le stocke dans context.products sous la forme :
    {
        "Samsung galaxy s6": {"name": "Samsung galaxy s6", "price": 360.0, "id": "..."},
        ...
    }
    """
    api_url = "https://api.demoblaze.com/entries"
    response = requests.get(api_url, timeout=10)

    assert response.status_code == 200, (
        f"Échec de chargement du catalogue API. "
        f"Status : {response.status_code} — URL : {api_url}"
    )

    data = response.json()
    items = data.get("Items", [])

    assert len(items) > 0, "Le catalogue API est vide."

    context.products = {}
    for item in items:
        # Normalisation des champs DynamoDB (format {"S": "valeur"} ou valeur directe)
        name = (
            item.get("title", {}).get("S", "")
            if isinstance(item.get("title"), dict)
            else item.get("title", "")
        )
        price_raw = (
            item.get("price", {}).get("N", 0)
            if isinstance(item.get("price"), dict)
            else item.get("price", 0)
        )
        prod_id = (
            item.get("id", {}).get("S", "")
            if isinstance(item.get("id"), dict)
            else item.get("id", "")
        )

        if name:
            context.products[name] = {
                "name": name,
                "price": float(price_raw),
                "id": prod_id,
            }

    print(f"\n📦 Catalogue chargé : {len(context.products)} produit(s) disponible(s).")


# ── Steps navigation ───────────────────────────────────────────────────────────


@given("j'ouvre la page d'accueil")
def step_given_open_home(context):
    """Ouvrir la page d'accueil et attendre le chargement des produits."""
    context.home_page = HomePage(context.driver)
    context.home_page.open()


@given("je suis sur la page d'accueil")
def step_given_on_home(context):
    """Alias — même action que 'j'ouvre la page d'accueil'."""
    step_given_open_home(context)


@given("je suis sur la page panier")
def step_given_panier(context):
    """Naviguer directement vers la page panier."""
    context.panier_page = PanierPage(context.driver)
    context.panier_page.open()
    assert (
        context.panier_page.is_cart_page()
    ), f"Échec : n'est pas sur la page panier. URL actuelle : {context.driver.current_url}"


@given('je suis sur la page produit de "{product_name}"')
def step_given_product_page(context, product_name):
    """
    - @ui : navigue vers la page produit via Selenium
    - @api : définit uniquement context.current_product sans browser
    """
    product = find_product(context, product_name)
    context.current_product = product

    if hasattr(context, "driver") and context.driver is not None:
        # Mode UI — navigation Selenium
        product_url = f"{BASE_URL}/prod.html?idp_={product['id']}"
        context.driver.get(product_url)
        from pages.base_page import BasePage
        from selenium.webdriver.common.by import By

        base = BasePage(context.driver)
        base.wait_for_element((By.ID, "tbodyid"))

    print(f"\n📄 Produit sélectionné : {product['name']} à ${product['price']}")


# ── Steps panier ───────────────────────────────────────────────────────────────


@given("mon panier est vide")
def step_given_empty_cart(context):
    """Initialise un panier vide dans le contexte."""
    context.cart = []
    context.expected_total = 0.0
    print("\n🛒 Panier initialisé vide.")


@given("mon panier contient les produits suivants")
def step_given_cart_with_products(context):
    """
    Initialise le panier avec une table de produits et quantités.
    | produit           | quantite |
    | Samsung galaxy s6 | 2        |
    """
    context.cart = []
    for row in context.table:
        product = find_product(context, row["produit"])
        qty = int(row["quantite"])
        context.cart.append(
            {
                "name": product["name"],
                "price": product["price"],
                "id": product["id"],
                "qty": qty,
            }
        )
    context.expected_total = compute_total(context.cart)
    print(f"\n🛒 Panier initialisé avec {len(context.cart)} produit(s).")


@when('je supprime le produit "{product_name}" du panier')
def step_remove_product(context, product_name):
    """Supprime un produit du panier par son nom."""
    product = find_product(context, product_name)
    before = len(context.cart)
    context.cart = [item for item in context.cart if item["name"] != product["name"]]
    context.expected_total = compute_total(context.cart)
    assert (
        len(context.cart) < before
    ), f"Échec : '{product['name']}' n'était pas dans le panier."
    print(f"\n🗑️ '{product['name']}' supprimé du panier.")


@when("je passe la commande")
def step_place_order(context):
    """Simule le passage de commande — capture le total avant confirmation."""
    context.order_total = compute_total(context.cart)
    print(f"\n📦 Commande passée — total : ${context.order_total}")
