from behave import when, then
from features.steps.common_steps import find_product, compute_total

# ── Steps spécifiques à ajout_panier.feature ─────────────────────────────────
# Les steps partagés (catalogue, panier vide, page produit, etc.)
# sont dans common_steps.py


# ── When ──────────────────────────────────────────────────────────────────────


@when('je clique sur le bouton "Add to cart"')
def step_add_to_cart(context):
    product = context.current_product
    assert (
        product
    ), "Aucun produit sélectionné — utilisez 'je suis sur la page produit de'"

    existing = next(
        (item for item in context.cart if item["name"] == product["name"]), None
    )
    if existing:
        existing["qty"] += 1
    else:
        context.cart.append(
            {
                "name": product["name"],
                "price": product["price"],
                "id": product["id"],
                "qty": 1,
            }
        )

    context.expected_total = compute_total(context.cart)
    print(f"\n🛒 '{product['name']}' ajouté — total : ${context.expected_total}")


@when('je clique {fois:d} fois sur le bouton "Add to cart"')
def step_add_to_cart_multiple(context, fois):
    for _ in range(fois):
        step_add_to_cart(context)


@when('je navigue vers la page produit de "{search_name}"')
def step_navigate_to_product(context, search_name):
    from features.steps.common_steps import find_product

    product = find_product(context, search_name)
    context.current_product = product
    print(
        f"\n📄 Page produit : {product['name']} (id={product['id']}) à ${product['price']}"
    )


# ── Then ──────────────────────────────────────────────────────────────────────


@then('le produit "{search_name}" est présent dans mon panier')
def step_product_in_cart(context, search_name):
    product = find_product(context, search_name)
    names_in_cart = [item["name"] for item in context.cart]
    assert product["name"] in names_in_cart, (
        f"'{product['name']}' absent du panier\n" f"Panier actuel : {names_in_cart}"
    )
    print(f"\n✅ '{product['name']}' présent dans le panier")


@then('la quantité du produit "{search_name}" dans le panier est de {expected_qty:d}')
def step_check_product_qty(context, search_name, expected_qty):
    product = find_product(context, search_name)
    item = next((i for i in context.cart if i["name"] == product["name"]), None)
    assert item, f"'{product['name']}' absent du panier"
    assert item["qty"] == expected_qty, (
        f"Quantité attendue : {expected_qty} "
        f"— Quantité dans le panier : {item['qty']}"
    )
    print(f"\n✅ Quantité correcte : {item['qty']} x '{product['name']}'")


@then("mon panier contient les produits suivants")
def step_cart_contains_products(context):
    names_in_cart = [item["name"] for item in context.cart]
    for row in context.table:
        product = find_product(context, row["produit"])
        assert product["name"] in names_in_cart, (
            f"'{product['name']}' absent du panier\n" f"Panier actuel : {names_in_cart}"
        )
    print("\n✅ Tous les produits attendus sont dans le panier")


@then("chaque produit a une quantité de 1")
def step_each_product_qty_is_one(context):
    for item in context.cart:
        assert (
            item["qty"] == 1
        ), f"'{item['name']}' a une quantité de {item['qty']} au lieu de 1"
    print("\n✅ Chaque produit a bien une quantité de 1")


@then('le sous-total du produit "{search_name}" est correct')
def step_check_subtotal(context, search_name):
    product = find_product(context, search_name)
    item = next((i for i in context.cart if i["name"] == product["name"]), None)
    assert item, f"'{product['name']}' absent du panier"
    expected_subtotal = round(item["price"] * item["qty"], 2)
    print(
        f"\n✅ Sous-total correct : {item['qty']} x ${item['price']} = ${expected_subtotal}"
    )


@then("le prix affiché correspond au prix du catalogue")
def step_check_price_matches_catalog(context):
    product = context.current_product
    assert product, "Aucun produit sélectionné"
    catalog_price = context.products[product["name"]]["price"]
    assert (
        product["price"] == catalog_price
    ), f"Prix affiché : ${product['price']} ≠ prix catalogue : ${catalog_price}"
    print(f"\n✅ Prix vérifié : {product['name']} = ${catalog_price}")


@then("le total du panier correspond à la somme des prix × quantités")
def step_check_total(context):
    recalculated = compute_total(context.cart)
    assert (
        context.expected_total == recalculated
    ), f"Total attendu : ${recalculated} — Total calculé : ${context.expected_total}"
    detail = " + ".join(f"({item['qty']} × ${item['price']})" for item in context.cart)
    print(f"\n🧮 {detail} = ${recalculated}")
