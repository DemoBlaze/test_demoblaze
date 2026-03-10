import json
import os
from behave import when, then
from features.steps.common_steps import find_product, compute_total

CART_SAVE_PATH = "reports/cart_save.json"


# ── When ──────────────────────────────────────────────────────────────────────


@when("je sauvegarde mon panier")
def step_save_cart(context):
    """Sauvegarde le panier dans un fichier JSON."""
    os.makedirs("reports", exist_ok=True)
    with open(CART_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(context.cart, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Panier sauvegardé ({len(context.cart)} produit(s)) → {CART_SAVE_PATH}")


@when("je restaure mon panier")
def step_restore_cart(context):
    """Restaure le panier depuis le fichier JSON sauvegardé."""
    assert os.path.exists(
        CART_SAVE_PATH
    ), f"Fichier de sauvegarde introuvable : {CART_SAVE_PATH}"
    with open(CART_SAVE_PATH, "r", encoding="utf-8") as f:
        context.cart = json.load(f)
    context.expected_total = compute_total(context.cart)
    print(f"\n📂 Panier restauré : {len(context.cart)} produit(s)")


# ── Then ──────────────────────────────────────────────────────────────────────


@then("le panier restauré contient les produits suivants")
def step_restored_cart_contains(context):
    """Vérifie le contenu et les quantités du panier restauré."""
    names_in_cart = {item["name"]: item["qty"] for item in context.cart}
    for row in context.table:
        product = find_product(context, row["produit"])
        expected_qty = int(row["quantite"])
        assert product["name"] in names_in_cart, (
            f"'{product['name']}' absent du panier restauré.\n"
            f"Panier actuel : {list(names_in_cart.keys())}"
        )
        assert names_in_cart[product["name"]] == expected_qty, (
            f"Quantité attendue pour '{product['name']}' : {expected_qty} "
            f"— Quantité restaurée : {names_in_cart[product['name']]}"
        )
    print("\n✅ Panier restauré conforme.")


@then('le produit "{product_name}" n\'est plus présent dans le panier')
def step_product_not_in_cart(context, product_name):
    """Vérifie qu'un produit a été retiré du panier."""
    product = find_product(context, product_name)
    names_in_cart = [item["name"] for item in context.cart]
    assert (
        product["name"] not in names_in_cart
    ), f"Échec : '{product['name']}' est encore dans le panier."
    print(f"\n✅ '{product['name']}' bien absent du panier.")


@then('le produit "{product_name}" est toujours présent dans le panier')
def step_product_still_in_cart(context, product_name):
    """Vérifie qu'un produit est toujours dans le panier."""
    product = find_product(context, product_name)
    names_in_cart = [item["name"] for item in context.cart]
    assert product["name"] in names_in_cart, (
        f"Échec : '{product['name']}' absent du panier.\n"
        f"Panier actuel : {names_in_cart}"
    )
    print(f"\n✅ '{product['name']}' toujours présent dans le panier.")
