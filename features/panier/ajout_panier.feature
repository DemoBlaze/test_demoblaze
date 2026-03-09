# ============================================================
# User Story : Ajouter un ou plusieurs produits au panier
# En tant qu'utilisateur, je veux pouvoir ajouter un ou plusieurs
# produits afin de pouvoir effectuer une commande
# ============================================================

Feature: Ajout de produits au panier

  Background:
    Given le catalogue de produits est chargé depuis l'API


  # ----------------------------------------------------------
  #  Ajouter un seul produit
  # ----------------------------------------------------------

  Scenario: Ajout d'un produit au panier depuis la page produit
    Given mon panier est vide
    And je suis sur la page produit de "Samsung galaxy s6"
    When je clique sur le bouton "Add to cart"
    Then le produit "Samsung galaxy s6" est présent dans mon panier
    And la quantité du produit "Samsung galaxy s6" dans le panier est de 1


  # ----------------------------------------------------------
  #  Ajouter plusieurs produits différents
  # ----------------------------------------------------------

  Scenario: Ajout de plusieurs produits différents au panier
    Given mon panier est vide
    And je suis sur la page produit de "Samsung galaxy s6"
    When je clique sur le bouton "Add to cart"
    And je navigue vers la page produit de "Nokia lumia 1520"
    And je clique sur le bouton "Add to cart"
    Then mon panier contient les produits suivants
      | produit           |
      | Samsung galaxy s6 |
      | Nokia lumia 1520  |
    And chaque produit a une quantité de 1


  # ----------------------------------------------------------
  #  Ajouter plusieurs fois le même produit
  # ----------------------------------------------------------

  Scenario Outline: Ajout de plusieurs quantités d'un même produit
    Given mon panier est vide
    And je suis sur la page produit de "<produit>"
    When je clique <fois> fois sur le bouton "Add to cart"
    Then la quantité du produit "<produit>" dans le panier est de <fois>
    And le sous-total du produit "<produit>" est correct

    Examples:
      | produit           | fois |
      | Samsung galaxy s6 | 2    |
      | Nokia lumia 1520  | 3    |


  # ----------------------------------------------------------
  #  Vérification du prix lors de l'ajout
  # ----------------------------------------------------------

  Scenario: Le prix du produit ajouté correspond au catalogue
    Given je suis sur la page produit de "Samsung galaxy s6"
    Then le prix affiché correspond au prix du catalogue


  # ----------------------------------------------------------
  #  Vérification du total après ajout
  # ----------------------------------------------------------

  Scenario: Le total du panier est correct après ajout de plusieurs produits
    Given mon panier est vide
    And je suis sur la page produit de "Samsung galaxy s6"
    When je clique sur le bouton "Add to cart"
    And je navigue vers la page produit de "Nokia lumia 1520"
    And je clique sur le bouton "Add to cart"
    Then le total du panier correspond à la somme des prix × quantités


  # ----------------------------------------------------------
  #  Scenario UI — nécessite Selenium ou Playwright
  # ----------------------------------------------------------

  # Scenario: Le bouton "Add to cart" est visible et cliquable sur la page produit
  #   Given je suis sur la page produit de "Samsung galaxy s6"
  #   When j'affiche la page produit
  #   Then le bouton "Add to cart" est visible
  #   And le bouton "Add to cart" est accessible et cliquable
