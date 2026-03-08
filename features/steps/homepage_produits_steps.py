from behave import then

# ── Steps spécifiques à la vérification des produits ──────────────────────────


@then("le titre de la page est correct")
def step_then_title(context):
    """Vérifier le titre de l'onglet navigateur."""
    title = context.home_page.get_page_title()
    assert title == "STORE", f"Échec : titre attendu 'STORE', titre actuel : '{title}'"


@then("la liste des produits est visible")
def step_then_product_list_visible(context):
    """Vérifier que le conteneur de produits est affiché."""
    assert (
        context.home_page.is_home_page()
    ), "Échec : le conteneur de produits (#tbodyid) n'est pas visible."


@then("au moins un produit est affiché")
def step_then_products_displayed(context):
    """Vérifier qu'au moins un produit est chargé dans la grille."""
    cards = context.home_page.get_product_cards()
    assert (
        len(cards) > 0
    ), f"Échec : aucun produit trouvé sur la homepage. Nombre de cartes : {len(cards)}"
    context.product_count = len(cards)
    print(f"\n✅ {len(cards)} produit(s) affiché(s) sur la homepage.")


@then("chaque produit a un nom et un prix")
def step_then_products_have_name_and_price(context):
    """Vérifier que chaque produit visible a un nom et un prix."""
    names = context.home_page.get_product_names()
    prices = context.home_page.get_product_prices()

    assert len(names) > 0, "Échec : aucun nom de produit trouvé."
    assert len(prices) > 0, "Échec : aucun prix de produit trouvé."

    for nom in names:
        assert nom != "", "Échec : un produit a un nom vide."

    for prix in prices:
        assert (
            "$" in prix or prix.replace(".", "").isdigit()
        ), f"Échec : prix inattendu '{prix}' — format attendu : '$xxx'"

    print("\n✅ Produits vérifiés :")
    for nom, prix in zip(names, prices):
        print(f"   - {nom} : {prix}")
