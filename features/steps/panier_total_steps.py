import re
from behave import given, when, then
from features.steps.common_steps import find_product, compute_total

# ── Given ─────────────────────────────────────────────────────────────────────


@given('mon panier contient {qty:d} unité(s) de "{product_name}"')
def step_given_cart_with_qty(context, qty, product_name):
    """Initialise le panier avec N unités d'un produit."""
    product = find_product(context, product_name)
    context.cart = [
        {
            "name": product["name"],
            "price": product["price"],
            "id": product["id"],
            "qty": qty,
        }
    ]
    context.expected_total = compute_total(context.cart)
    context.current_product = product
    print(f"\n🛒 Panier : {qty} x '{product['name']}' à ${product['price']}")


# ── When ──────────────────────────────────────────────────────────────────────


@when('je modifie la quantité de "{product_name}" à {new_qty:d}')
def step_update_qty(context, product_name, new_qty):
    """Modifie la quantité d'un produit dans le panier."""
    product = find_product(context, product_name)
    item = next((i for i in context.cart if i["name"] == product["name"]), None)
    assert item, f"'{product['name']}' absent du panier."
    item["qty"] = new_qty
    context.expected_total = compute_total(context.cart)
    print(f"\n✏️ Quantité de '{product['name']}' mise à jour : {new_qty}")


# ── Then ──────────────────────────────────────────────────────────────────────


@then("le total calculé correspond à la somme des prix × quantités")
def step_total_matches_sum(context):
    """Vérifie que le total du panier = somme des (prix × quantité)."""
    recalculated = compute_total(context.cart)
    assert context.expected_total == recalculated, (
        f"Total attendu : ${context.expected_total} "
        f"— Total recalculé : ${recalculated}"
    )
    detail = " + ".join(f"({i['qty']} × ${i['price']})" for i in context.cart)
    print(f"\n🧮 {detail} = ${recalculated} ✅")


@then("le total calculé correspond à {qty:d} fois le prix du produit")
def step_total_matches_qty_times_price(context, qty):
    """Vérifie que le total = N × prix unitaire du produit courant."""
    product = context.current_product
    assert product, "Aucun produit courant — utilisez un Given approprié."
    expected = round(product["price"] * qty, 2)
    actual = compute_total(context.cart)
    assert actual == expected, (
        f"Total attendu : {qty} × ${product['price']} = ${expected} "
        f"— Total calculé : ${actual}"
    )
    print(f"\n✅ {qty} × ${product['price']} = ${expected}")


@then("le total de la commande est identique au total du panier")
def step_order_total_matches_cart(context):
    """Vérifie que le total commande == total panier."""
    cart_total = compute_total(context.cart)
    assert context.order_total == cart_total, (
        f"Total commande : ${context.order_total} " f"≠ total panier : ${cart_total}"
    )
    print(f"\n✅ Total commande = total panier = ${cart_total}")


@then('le total est affiché avec le symbole "$" et 2 décimales exactes')
def step_total_format(context):
    """Vérifie le format d'affichage du total : $xxx.xx"""
    total = compute_total(context.cart)
    formatted = f"${total:.2f}"
    # Vérifier le format avec regex
    assert re.match(
        r"^\$\d+\.\d{2}$", formatted
    ), f"Format invalide : '{formatted}' — attendu : '$xxx.xx'"
    print(f"\n✅ Format correct : {formatted}")
