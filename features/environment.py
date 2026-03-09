import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEMOBLAZE_API = os.getenv("API_BASE_URL")
CATEGORIES = ["phone", "notebook", "monitor"]


def before_all(context):
    """
    Récupère le catalogue complet une seule fois pour toute la suite de tests.
    context.products = {"Samsung galaxy s6": 360.0, "Nokia lumia 1520": 820.0, ...}
    """
    assert DEMOBLAZE_API, "Variable API_BASE_URL manquante dans le fichier .env"
    context.api_base_url = DEMOBLAZE_API
    context.products = {}

    for cat in CATEGORIES:
        try:
            response = requests.post(
                f"{context.api_base_url}/bycat",
                json={"cat": cat},
                timeout=10
            )
            response.raise_for_status()
            for item in response.json().get("Items", []):
                context.products[item["title"]] = {
                    "price": float(item["price"]),
                    "id": item["id"]
                }
        except requests.RequestException as e:
            raise RuntimeError(
                f"Impossible de récupérer le catalogue '{cat}' : {e}")

    assert context.products, "Le catalogue est vide — vérifiez l'API demoblaze"
    print(f"\n✅ Catalogue chargé : {len(context.products)} produits")


def before_scenario(context, scenario):
    """Initialise un panier vide avant chaque scénario."""
    context.cart = []
    context.expected_total = 0.0
    context.current_product = None


def after_scenario(context, scenario):
    pass
