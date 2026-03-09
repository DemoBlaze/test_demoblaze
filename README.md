# test_demoblaze
Mise en place de la structure de base pour un projet de test. Le site à l'étude est l'e-commerce DemoBlaze.

## Structure du projet
Le projet est organisé en plusieurs fichiers et dossiers. Voici la structure du projet :

```
test_demoblaze/
│
├── features/                            ← fichiers des tests **BDD**  Behave
│   ├── __init__.py
│   ├── environment.py
│   ├──panier
│   └──commande/
│   └── steps/
│       ├── __init__.py
         ├──panier/
         ├──commande/
│   │
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── panier_page.py
│   └── commande_page.py
│
├── api_tests/
│   ├── __init__.py
│   └── base_test.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── drivers.py
│
├── utils/
│   ├── __init__.py
│   ├── jira_reporter.py
│   └── squash_reporter.py
│
├── reports/                    ← pour les fichiers de  reporting Allure
│
├── behave.ini
├── .coveragerc
├── .env.example
├── .env
└── requirements.txt

```
