# 🛒 test_demoblaze

> Projet de tests automatisés de l'e-commerce **[DemoBlaze](https://www.demoblaze.com)** — approche **BDD** avec Behave, pattern **Page Object Model**, reporting **Allure** et intégration **Jira / Squash TM**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Behave](https://img.shields.io/badge/Behave-BDD-00b300?style=flat-square&logo=cucumber&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=flat-square&logo=selenium&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Reporting-orange?style=flat-square)
![Jira](https://img.shields.io/badge/Jira-Integration-0052CC?style=flat-square&logo=jira&logoColor=white)
![Squash](https://img.shields.io/badge/Squash-TM-6A0DAD?style=flat-square)

---

## 📋 Table des matières

- [🧰 Stack technique](#-stack-technique)
- [📁 Structure du projet](#-structure-du-projet)
- [✅ Prérequis](#-prérequis)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [▶️ Lancer les tests](#️-lancer-les-tests)
- [📊 Reporting Allure](#-reporting-allure)
- [🔗 Ressources](#-ressources)

---

## 🧰 Stack technique

| Icône | Catégorie | Outil | Détail |
|:---:|---|---|---|
| 🐍 | **Langage** | Python | 3.10+ |
| 🥒 | **Framework BDD** | Behave | Scénarios Gherkin |
| 🌐 | **Automatisation navigateur** | Selenium WebDriver | Pattern POM |
| 🔌 | **Tests API** | Requests | REST |
| 📊 | **Reporting** | Allure Framework | Rapport HTML |
| 🔗 | **Intégrations** | Jira · Squash TM | CI/CD |
| 📈 | **Couverture de code** | Coverage.py | `.coveragerc` |
| 🔐 | **Variables d'environnement** | python-dotenv | `.env` |
| 📦 | **Gestion des dépendances** | pip | `requirements.txt` |

---

## 📁 Structure du projet

```
test_demoblaze/
│
├── features/                        ← Scénarios BDD (fichiers .feature) & hooks Behave
│   ├── __init__.py
│   ├── environment.py               ← Hooks before/after scenario, suite…
│   ├── panier/                      ← Scénarios Gherkin — domaine Panier
│   ├── commande/                    ← Scénarios Gherkin — domaine Commande
│   └── steps/                       ← Implémentation des steps
│       ├── __init__.py
│       ├── panier/                  ← Steps liés au panier
│       └── commande/                ← Steps liés à la commande
│
├── pages/                           ← Pattern Page Object Model (POM)
│   ├── __init__.py
│   ├── base_page.py                 ← Classe parente — méthodes communes Selenium
│   ├── panier_page.py               ← Page Object Panier
│   └── commande_page.py             ← Page Object Commande
│
├── api_tests/                       ← Tests API REST
│   ├── __init__.py
│   └── base_test.py                 ← Classe de base pour les appels API
│
├── config/                          ← Configuration globale du projet
│   ├── __init__.py
│   ├── settings.py                  ← Variables globales (URLs, timeouts…)
│   └── drivers.py                   ← Initialisation & configuration WebDriver
│
├── utils/                           ← Utilitaires & intégrations externes
│   ├── __init__.py
│   ├── jira_reporter.py             ← Remontée des résultats → Jira
│   └── squash_reporter.py           ← Export des résultats → Squash TM
│
├── reports/                         ← Rapports Allure (générés automatiquement)
│
├── behave.ini                       ← Configuration Behave (tags, format, paths…)
├── .coveragerc                      ← Configuration Coverage.py
├── .env.example                     ← Template des variables d'environnement
├── .env                             ← Variables locales ⚠️ ne pas commiter
└── requirements.txt                 ← Dépendances Python du projet
```

---

## ✅ Prérequis

| Icône | Outil | Version | Remarque |
|:---:|---|---|---|
| 🐍 | **Python** | 3.10+ | [Télécharger](https://www.python.org/downloads/) |
| 📦 | **pip** | inclus avec Python | — |
| 🌐 | **Google Chrome** ou Firefox | dernière version | Navigateur cible Selenium |
| 🔧 | **ChromeDriver** | compatible avec Chrome | [Télécharger](https://chromedriver.chromium.org/) ou via `webdriver-manager` |
| ☕ | **Java** | 8+ | Requis pour Allure CLI |
| 📊 | **Allure CLI** | dernière version | [Guide d'installation](https://docs.qameta.io/allure/#_installing_a_commandline) |

---

## 🚀 Installation

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/<votre-organisation>/test_demoblaze.git
cd test_demoblaze
```

### 2️⃣ Créer et activer un environnement virtuel

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer sur macOS / Linux
source .venv/bin/activate

# Activer sur Windows
.venv\Scripts\activate
```

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Copier le fichier d'exemple

```bash
cp .env.example .env
```

### 2. Renseigner les variables dans `.env`

| Variable | Exemple | Description |
|---|---|---|
| `BASE_URL` | `https://www.demoblaze.com` | URL cible des tests |
| `BROWSER` | `chrome` | `chrome` ou `firefox` |
| `HEADLESS` | `false` | Mode sans interface graphique |
| `JIRA_URL` | `https://xxx.atlassian.net` | Instance Jira *(optionnel)* |
| `JIRA_USER` | `email@domaine.com` | Compte Jira |
| `JIRA_TOKEN` | `votre_api_token` | Token API Jira |
| `SQUASH_URL` | `https://squash.domaine.com` | Instance Squash TM *(optionnel)* |
| `SQUASH_USER` | `votre_user` | Compte Squash |
| `SQUASH_TOKEN` | `votre_token` | Token API Squash |

> ⚠️ **Important** — Le fichier `.env` est ignoré par Git (`.gitignore`). Ne le commitez jamais dans le dépôt.

---

## ▶️ Lancer les tests

### 🟢 Tous les tests

```bash
behave
```

### 🏷️ Filtrer par tag

```bash
# Tests du domaine Panier
behave --tags=panier

# Tests de priorité P1
behave --tags=P1

# Exclure les tests en cours de développement
behave --tags=~wip
```

### 📊 Avec génération du rapport Allure

```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/
```

### 📈 Avec mesure de couverture de code

```bash
coverage run -m behave
coverage report
coverage html    # → génère un rapport HTML dans htmlcov/
```

---

## 📊 Reporting Allure

Une fois les tests exécutés avec le formatter Allure, générez et consultez le rapport :

```bash
# ⚙️  Étape 1 — Générer le rapport HTML
allure generate reports/ --clean -o reports/allure-report

# 🌐  Étape 2 — Ouvrir le rapport dans le navigateur
allure open reports/allure-report

# 🚀  Raccourci — Lancer directement un serveur local
allure serve reports/
```

---

## 🔗 Ressources

| Icône | Ressource | Lien |
|:---:|---|---|
| 🛒 | **Site testé — DemoBlaze** | [demoblaze.com](https://www.demoblaze.com) |
| 🥒 | **Documentation Behave** | [behave.readthedocs.io](https://behave.readthedocs.io/) |
| 🌐 | **Documentation Selenium Python** | [selenium-python.readthedocs.io](https://selenium-python.readthedocs.io/) |
| 📊 | **Documentation Allure** | [docs.qameta.io/allure](https://docs.qameta.io/allure/) |
| 🔧 | **ChromeDriver** | [chromedriver.chromium.org](https://chromedriver.chromium.org/) |
