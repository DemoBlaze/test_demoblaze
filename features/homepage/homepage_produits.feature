@ui
Feature: Affichage de la page d'accueil
  En tant que visiteur du site Demoblaze
  Je veux que la page d'accueil s'affiche correctement
  Afin de pouvoir consulter les produits disponibles

  Scenario: La homepage affiche des produits
    Given j'ouvre la page d'accueil
    Then le titre de la page est correct
    And la liste des produits est visible
    And au moins un produit est affiché
    And chaque produit a un nom et un prix
