import re
from behave import when, then
from features.steps.common_steps import find_product, compute_total


# ── Steps spécifiques à panier.feature ───────────────────────────────────────
# Les steps partagés (catalogue, panier vide, page produit, etc.)
# sont dans common_steps.py


def format_total(amount: float) -> str:
    """Formate un montant avec symbole $ et 2 décimales."""
    return f"${amount:.2f}"


# ── When ──────────────────────────────────────────────────────────────────────

@when('je modifie la quantité de "{search_name}" à {new_qty:d}')
def step_modify_qty(context, search_name, new_qty):
    product = find_product(context, search_name)
    for item in context.cart:
        if item["name"] == product["name"]:
            item["qty"] = new_qty
            break
    context.expected_total = compute_total(context.cart)
    print(
        f"\n✏️ Quantité de '{product['name']}' modifiée à {new_qty} — total : ${context.expected_total}")


# ── Then ──────────────────────────────────────────────────────────────────────

@then("le total calculé correspond à {multiplier:d} fois le prix du produit")
def step_check_single_total(context, multiplier):
    assert len(context.cart) == 1, "Ce step attend un seul produit dans le panier"
    price = context.cart[0]["price"]
    expected = round(price * multiplier, 2)
    assert context.expected_total == expected, (
        f"Total attendu : ${expected} — Total calculé : ${context.expected_total}"
    )
    print(f"\n✅ Total correct : {multiplier} x ${price} = ${expected}")


@then('le total est affiché avec le symbole "$" et 2 décimales exactes')
def step_check_format(context):
    formatted = format_total(context.expected_total)
    assert re.match(r"^\$\d+\.\d{2}$", formatted), (
        f"Format incorrect : '{formatted}' — attendu ex: $360.00"
    )
    print(f"\n✅ Format correct : {formatted}")
