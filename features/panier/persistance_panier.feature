# ============================================================
# User Story : Sauvegarder son panier
# En tant qu'utilisateur, je veux pouvoir sauvegarder mon panier
# afin de pouvoir continuer mes achats et/ou passer commande
# ============================================================

Feature: Sauvegarde du panier

  Background:
    Given le catalogue de produits est chargé depuis l'API


  # ------------------------------------------------------------------------------------
  #   Panier sauvegardé — logique testable sans navigateur
  # ------------------------------------------------------------------------------------

  Scenario: Le panier est sauvegardé avec les produits et leurs quantités
    Given mon panier est vide
    And mon panier contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 2        |
      | Nokia lumia 1520  | 1        |
    When je sauvegarde mon panier
    And je restaure mon panier
    Then le panier restauré contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 2        |
      | Nokia lumia 1520  | 1        |


  Scenario: La sauvegarde reflète la suppression d'un produit du panier
    Given mon panier est vide
    And mon panier contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 1        |
      | Nokia lumia 1520  | 1        |
    When je supprime le produit "Nokia lumia 1520" du panier
    And je sauvegarde mon panier
    And je restaure mon panier
    Then le produit "Nokia lumia 1520" n'est plus présent dans le panier
    And le produit "Samsung galaxy s6" est toujours présent dans le panier


  Scenario: Le panier sauvegardé peut être utilisé pour passer commande
    Given mon panier est vide
    And mon panier contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 2        |
      | Nokia lumia 1520  | 1        |
    When je sauvegarde mon panier
    And je passe la commande
    Then le total de la commande est identique au total du panier


  Scenario: Le total du panier restauré est correct
    Given mon panier est vide
    And mon panier contient les produits suivants
      | produit           | quantite |
      | Samsung galaxy s6 | 2        |
      | Nokia lumia 1520  | 1        |
    When je sauvegarde mon panier
    And je restaure mon panier
    Then le total calculé correspond à la somme des prix × quantités


  # ------------------------------------------------------------------------------------
  #   Scenarios nécessitant un navigateur — à tester avec Selenium
  # ------------------------------------------------------------------------------------

  # Scenario: Le panier est conservé après déconnexion et reconnexion
  #   Given je suis connecté à mon compte
  #   And mon panier contient les produits suivants
  #     | produit           | quantite |
  #     | Samsung galaxy s6 | 2        |
  #     | Nokia lumia 1520  | 1        |
  #   When je me déconnecte
  #   And je me reconnecte à mon compte
  #   Then le panier contient toujours les mêmes produits et quantités

  # Scenario: Le panier est conservé pour un utilisateur non connecté entre deux visites
  #   Given je ne suis pas connecté à mon compte
  #   And mon panier contient les produits suivants
  #     | produit           | quantite |
  #     | Samsung galaxy s6 | 2        |
  #     | Nokia lumia 1520  | 1        |
  #   When je ferme le navigateur
  #   And je rouvre le navigateur et accède au site
  #   Then mon panier contient toujours les mêmes produits et quantités

  # Scenario: Le panier temporaire est fusionné au panier du compte après connexion
  #   Given je ne suis pas connecté à mon compte
  #   And mon panier contient 1 unité de "Samsung galaxy s6"
  #   When je me connecte à mon compte
  #   Then le produit "Samsung galaxy s6" est présent dans mon panier
  #   And les produits déjà présents avant connexion sont conservés
