# 🥋 Jujitsu Tournament Manager (JTM)

## 🎯 Vision du projet

JTM est une plateforme web dédiée à la gestion de tournois de jujitsu.

L’objectif principal est de  **simplifier et automatiser l’inscription des combattants par les clubs** , afin de  **réduire drastiquement la charge de travail des organisateurs** .

À terme, le projet évoluera vers un système complet permettant :

* la gestion des catégories
* la génération intelligente des arbres de tournoi
* la gestion des combats en direct
* et l’aide à l’arbitrage automatisé

---

## 🚀 Objectifs de la Phase 1 (MVP)

Cette première phase se concentre sur un point critique :

👉 **Faciliter et structurer les inscriptions des participants via une API propre et une base de données cohérente**

### Fonctionnalités cibles :

* Création de comptes clubs
* Gestion des participants par club
* Inscription à un tournoi
* Validation des inscriptions par les organisateurs
* Détection d’erreurs (poids, licence, données manquantes)
* Pré-catégorisation automatique

---

## 🧱 Stack technique (Phase 1)

* Backend API : FastAPI
* Validation des données : Pydantic
* Base de données : PostgreSQL (SQLite en dev possible)
* ORM : SQLAlchemy 2.0
* Migrations : Alembic

---

## 🧠 Philosophie du projet

Le projet est conçu en **plusieurs phases évolutives** :

### Phase 1 — Web & Data (actuelle)

* API REST
* Modélisation SQL propre
* Gestion des inscriptions
* Workflow organisateur

### Phase 2 — Moteur métier

* Génération des catégories
* Génération des arbres de tournoi
* Règles sportives avancées

### Phase 3 — Optimisation

* Extraction des cœurs critiques en C++
* Amélioration des performances

### Phase 4 — Extensions

* Aide à l’arbitrage automatisé
* Analyse des combats
* Statistiques avancées

---

## 🗂️ Architecture du projet

```bash
app/
├── api/              # Routes FastAPI
├── core/             # Config, sécurité, DB
├── models/           # Modèles SQLAlchemy
├── schemas/          # Schémas Pydantic
├── services/         # Logique métier
├── repositories/     # Accès aux données
└── main.py           # Entrée de l'application
```

---

## 🧩 Modélisation des données (concept clé)

Le projet repose sur une séparation essentielle :

👉 **Participant ≠ Inscription**

### Participant

Représente une personne :

* nom
* prénom
* club
* niveau

### Registration

Représente une participation à un tournoi :

* poids déclaré
* statut
* validation
* tournoi associé

✔️ Un participant peut participer à plusieurs tournois
✔️ Chaque inscription possède son propre cycle de validation

---

## 🔄 Workflow d’inscription

1. Le club crée ses participants
2. Le club inscrit ses participants à un tournoi
3. L’inscription passe en statut `submitted`
4. L’organisateur vérifie :
   * licence
   * identité
   * poids
5. Statut final :
   * `validated`
   * `rejected`
   * `pending_review`

---

## 📌 Roadmap technique

### Étape 1 — Setup projet

* [ ] Initialiser FastAPI
* [ ] Configurer PostgreSQL
* [ ] Setup SQLAlchemy
* [ ] Setup Alembic

### Étape 2 — Authentification

* [ ] Création utilisateur
* [ ] Login / JWT
* [ ] Gestion des rôles (club / organisateur)

### Étape 3 — Clubs & Participants

* [ ] CRUD clubs
* [ ] CRUD participants
* [ ] Liaison club → participants

### Étape 4 — Tournois

* [ ] CRUD tournois
* [ ] Publication des tournois

### Étape 5 — Inscriptions

* [ ] Création inscription
* [ ] Statuts
* [ ] Validation organisateur

### Étape 6 — Qualité des données

* [ ] Vérifications métier
* [ ] Détection anomalies
* [ ] Logs

---

## 🧪 Bonnes pratiques

* Séparer logique métier / API / DB
* Ne jamais mettre de logique complexe dans les routes
* Toujours passer par les services
* Versionner la base de données (Alembic)
* Écrire du code lisible avant d’optimiser

---

## 🤝 Contribution

Le projet est ouvert aux contributions.

Avant d’ajouter une fonctionnalité :

1. Vérifier si elle correspond à la phase actuelle
2. Respecter l’architecture existante
3. Ajouter des modèles cohérents avec la base SQL
4. Documenter la logique métier

### Idées de contributions

* Amélioration du modèle de données
* Ajout de validations métier
* Optimisation des requêtes SQL
* Ajout de tests
* Préparation du moteur de catégorisation

---

## ⚠️ Ce que le projet n’est PAS (pour le moment)

* Pas encore un moteur complet de tournoi
* Pas encore un système temps réel de combats
* Pas encore une app mobile

👉 Ces éléments viendront dans les phases suivantes

---

## 🔮 Vision long terme

Créer un écosystème complet autour du jujitsu :

* gestion de tournoi
* suivi des combattants
* analyse de performance
* arbitrage assisté
* plateforme utilisée par clubs et fédérations

---

## 🧑‍💻 Auteur

Projet initié par un ingénieur orienté IA/robotique, avec une volonté de construire un outil concret, évolutif et utilisé sur le terrain.

---

## 💬 Notes

Ce projet est aussi un support d’apprentissage :

* API design
* SQL propre
* architecture logicielle
* évolution vers C++

---

## 📦 Statut du projet

🚧 En cours de construction — Phase 1 (Web & API)
