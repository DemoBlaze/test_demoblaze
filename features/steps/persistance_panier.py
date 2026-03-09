from behave import when, then
from features.steps.common_steps import find_product, compute_total

# ── Steps spécifiques à sauvegarde_panier.feature ────────────────────────────
# Les steps partagés (catalogue, panier vide, ajout produits, etc.)
# sont dans common_steps.py
# La sauvegarde est simulée en mémoire — les scénarios nécessitant
# un vrai navigateur (session, cookies, reconnexion) sont commentés dans la feature


# ── When ──────────────────────────────────────────────────────────────────────


@when("je sauvegarde mon panier")
def step_save_cart(context):
    """Sauvegarde une copie du panier en mémoire."""
    context.saved_cart = [item.copy() for item in context.cart]
    context.saved_total = context.expected_total
    print(
        f"\n💾 Panier sauvegardé : {len(context.saved_cart)} produit(s) — total : ${context.saved_total}"
    )


@when("je restaure mon panier")
def step_restore_cart(context):
    """Restaure le panier depuis la sauvegarde."""
    assert hasattr(
        context, "saved_cart"
    ), "Aucun panier sauvegardé — utilisez 'je sauvegarde mon panier'"
    context.cart = [item.copy() for item in context.saved_cart]
    context.expected_total = compute_total(context.cart)
    print(
        f"\n🔄 Panier restauré : {len(context.cart)} produit(s) — total : ${context.expected_total}"
    )


# ── Then ──────────────────────────────────────────────────────────────────────


@then("le panier restauré contient les produits suivants")
def step_restored_cart_contains(context):
    names_in_cart = [item["name"] for item in context.cart]
    for row in context.table:
        product = find_product(context, row["produit"])
        qty = int(row["quantite"])

        assert product["name"] in names_in_cart, (
            f"'{product['name']}' absent du panier restauré\n"
            f"Panier actuel : {names_in_cart}"
        )
        item = next(i for i in context.cart if i["name"] == product["name"])
        assert item["qty"] == qty, (
            f"Quantité attendue pour '{product['name']}' : {qty} "
            f"— Quantité restaurée : {item['qty']}"
        )
        print(f"\n✅ '{product['name']}' présent avec quantité {qty}")


@then('le produit "{search_name}" n\'est plus présent dans le panier')
def step_product_absent(context, search_name):
    product = find_product(context, search_name)
    names_in_cart = [item["name"] for item in context.cart]
    assert (
        product["name"] not in names_in_cart
    ), f"'{product['name']}' est encore présent dans le panier alors qu'il devrait être supprimé"
    print(f"\n✅ '{product['name']}' absent du panier")


@then('le produit "{search_name}" est toujours présent dans le panier')
def step_product_still_present(context, search_name):
    product = find_product(context, search_name)
    names_in_cart = [item["name"] for item in context.cart]
    assert product["name"] in names_in_cart, (
        f"'{product['name']}' absent du panier alors qu'il devrait être présent\n"
        f"Panier actuel : {names_in_cart}"
    )
    print(f"\n✅ '{product['name']}' toujours présent dans le panier")
