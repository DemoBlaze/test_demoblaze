from behave import given, when, then


# ── Steps partagés entre toutes les features ─────────────────────────────────
# Ce fichier centralise les steps communs pour éviter les AmbiguousStep.
# Règle : un step ne doit être défini qu'une seule fois dans features/steps/


def find_product(context, search_name: str) -> dict:
    """
    Cherche un produit dans le catalogue par correspondance partielle
    insensible à la casse.
    Retourne {"name": str, "price": float, "id": str}
    """
    match = next(
        (title for title in context.products if search_name.lower() in title.lower()),
        None
    )
    assert match, (
        f"Produit '{search_name}' introuvable dans le catalogue\n"
        f"Produits disponibles : {list(context.products.keys())}"
    )
    return {
        "name":  match,
        "price": context.products[match]["price"],
        "id":    context.products[match]["id"]
    }


def compute_total(cart: list) -> float:
    """Calcule le total du panier en mémoire."""
    return round(sum(item["price"] * item["qty"] for item in cart), 2)


@given("le catalogue de produits est chargé depuis l'API")
def step_catalog_loaded(context):
    assert context.products, (
        f"Le catalogue est vide — vérifiez que API_BASE_URL={context.api_base_url} est accessible"
    )
    print(
        f"\n✅ {len(context.products)} produits chargés depuis {context.api_base_url}")


@given("mon panier est vide")
def step_cart_is_empty(context):
    context.cart = []
    context.expected_total = 0.0
    print("\n🛒 Panier vidé")


@given('je suis sur la page produit de "{search_name}"')
def step_on_product_page(context, search_name):
    product = find_product(context, search_name)
    context.current_product = product
    print(
        f"\n📄 Page produit : {product['name']} (id={product['id']}) à ${product['price']}")


@given('mon panier contient {qty:d} unité(s) de "{search_name}"')
def step_add_single_product(context, qty, search_name):
    product = find_product(context, search_name)
    context.cart = [{"name": product["name"],
                     "price": product["price"], "qty": qty}]
    context.expected_total = compute_total(context.cart)
    print(
        f"\n🛒 {qty} x '{product['name']}' à ${product['price']} — total : ${context.expected_total}")


# Sans ":" — Behave tronque le ":" lors de la génération des snippets
# La feature doit utiliser exactement : "mon panier contient les produits suivants"
@given("mon panier contient les produits suivants")
def step_add_multiple_products(context):
    context.cart = []
    for row in context.table:
        product = find_product(context, row["produit"])
        qty = int(row["quantite"])
        context.cart.append(
            {"name": product["name"], "price": product["price"], "qty": qty})
        print(f"\n🛒 {qty} x '{product['name']}' à ${product['price']}")
    context.expected_total = compute_total(context.cart)
    print(f"\n💰 Total initial : ${context.expected_total}")


@when('je supprime le produit "{search_name}" du panier')
def step_delete_product(context, search_name):
    product = find_product(context, search_name)
    context.cart = [
        item for item in context.cart if item["name"] != product["name"]]
    context.expected_total = compute_total(context.cart)
    print(
        f"\n🗑️ '{product['name']}' supprimé — total : ${context.expected_total}")


@when("je passe la commande")
def step_place_order(context):
    context.order_total = context.expected_total
    print(f"\n📦 Commande passée — total : ${context.order_total}")


@then("le total de la commande est identique au total du panier")
def step_check_order_total(context):
    assert context.order_total == context.expected_total, (
        f"Total commande : ${context.order_total} ≠ total panier : ${context.expected_total}"
    )
    print(f"\n✅ Total cohérent : ${context.order_total}")


@then("le total calculé correspond à la somme des prix × quantités")
def step_check_multi_total(context):
    recalculated = compute_total(context.cart)
    assert context.expected_total == recalculated, (
        f"Total attendu : ${recalculated} — Total calculé : ${context.expected_total}"
    )
    detail = " + ".join(
        f"({item['qty']} × ${item['price']})" for item in context.cart
    )
    print(f"\n🧮 {detail} = ${recalculated}")
