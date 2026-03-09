# ============================================================
# User Story : Vérifier que le montant total correspond à la
# somme des prix individuels afin de connaître le montant de
# ma commande
# ============================================================

Feature: Vérification du montant total de la commande

  Background:
    Given le catalogue de produits est chargé depuis l'API


  # ----------------------------------------------------------
  #   Calcul du total — prix récupérés dynamiquement
  # ----------------------------------------------------------

  Scenario Outline: Calcul du total pour un seul produit
    Given mon panier contient <quantite> unité(s) de "<produit>"
    Then le total calculé correspond à <quantite> fois le prix du produit

    Examples:
      | produit           | quantite |
      | Samsung galaxy s6 | 1        |
      | Samsung galaxy s6 | 3        |
      | Nokia lumia 1520  | 2        |


  Scenario: Calcul du total pour plusieurs produits différents
    Given mon panier contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 2        |
      | Nokia lumia 1520  | 1        |
      | Sony vaio i5      | 1        |
    Then le total calculé correspond à la somme des prix × quantités


  # ----------------------------------------------------------
  #   Mise à jour du total après modifications
  # ----------------------------------------------------------

  Scenario: Le total est recalculé après modification de quantité
    Given mon panier contient 1 unité(s) de "Samsung galaxy s6"
    When je modifie la quantité de "Samsung galaxy s6" à 3
    Then le total calculé correspond à la somme des prix × quantités


  Scenario: Le total est recalculé après suppression d'un produit
    Given mon panier contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 1        |
      | Nokia lumia 1520  | 1        |
    When je supprime le produit "Nokia lumia 1520" du panier
    Then le total calculé correspond à la somme des prix × quantités


  # ----------------------------------------------------------
  #   Cohérence du total entre panier et paiement
  # ----------------------------------------------------------

  Scenario: Le total est identique du panier jusqu'à la confirmation
    Given mon panier contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 1        |
      | Nokia lumia 1520  | 1        |
    When je passe la commande
    Then le total de la commande est identique au total du panier


  # ----------------------------------------------------------
  #   Format d'affichage du total
  # ----------------------------------------------------------

  Scenario: Le total est affiché avec le bon format monétaire
    Given mon panier contient 1 unité(s) de "Samsung galaxy s6"
    Then le total est affiché avec le symbole "$" et 2 décimales exactes
