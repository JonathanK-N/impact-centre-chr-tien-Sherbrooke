
Impact Centre Chrétien Sherbrooke – Plateforme Communautaire
============================================================

Cette application full-stack permet de gérer la vie communautaire d’Impact Centre Chrétien Sherbrooke : membres, départements, Familles d’Impact, événements, annonces, médias et dons.

Sommaire
--------

- [Architecture](#architecture)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Démarrage rapide](#démarrage-rapide)
- [Backend Flask](#backend-flask)
- [Frontend React](#frontend-react)
- [Flux de données et rôles](#flux-de-données-et-rôles)
- [Migrations & Seed](#migrations--seed)
- [Docker](#docker)
- [Préparation Firestore](#préparation-firestore)
- [API & Documentation](#api--documentation)

Architecture
------------

```
impact-centre-chr-tien-Sherbrooke/
├── backend/          # API Flask + SQLAlchemy + JWT
│   ├── app/          # Blueprints, modèles, seeds, services
│   ├── migrations/   # Scripts Alembic
│   ├── instance/     # Base SQLite (créée automatiquement)
│   └── requirements.txt
├── frontend/         # SPA React (Vite) + Tailwind CSS
│   └── src/          # Pages, contextes, services
├── docker-compose.yml
└── README.md
```

Fonctionnalités principales
---------------------------

- Authentification JWT (inscription, connexion, rafraîchissement).
- Rôles : admin, department_lead, family_lead, member.
- Gestion des départements (CRUD, responsables, membres).
- Gestion des Familles d’Impact avec carte Leaflet et recherche par code postal.
- Événements (globaux, département, FI) avec inscriptions.
- Annonces ciblées (globales, département, FI).
- Don en ligne (Stripe/PayPal prêt) + historique.
- Bibliothèque médias (vidéo, audio, documents).
- Profil membre (infos personnelles, engagements).
- Tableau de bord admin + assignation des responsables.

Démarrage rapide
----------------

### Prérequis

- Python 3.11+
- Node.js 18+ / npm
- SQLite (intégré)

### Construction du frontend + backend

```bash
# 1. Installer les dépendances frontend et construire le bundle
cd frontend
npm install
npm run build           # génère le SPA dans backend/app/static/frontend

# 2. Initialiser l'API (exécuter depuis backend/)
cd ../backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app db upgrade
flask --app app seed-db    # optionnel : données de démo
flask --app app run        # une seule commande pour servir API + SPA
```

L’API écoute sur `http://localhost:5000`.

> 💡 En développement frontend pur, tu peux encore utiliser `npm run dev -- --host` dans `frontend/`, mais le backend servira toujours la dernière version compilée. Relance `npm run build` après tes changements pour les voir sur `http://localhost:5000`.

Backend Flask
-------------

- **Structure** : app factory (`app/__init__.py`), blueprints par domaine (`auth`, `departments`, `families`, etc.).
- **ORM** : SQLAlchemy via `app/extensions`.
- **Migrations** : Alembic (`backend/migrations` + `alembic.ini`).
- **Seed** : `flask seed-db` injecte un jeu de données réaliste (admin, membres, départements, FI, événements, dons, médias).
- **Auth** : `flask-jwt-extended` (tokens `access` + `refresh`, rôle dans les claims).
- **Services** : `app/services/firestore_mapping.py` décrit la correspondance Firestore.
- **Swagger** : `/api/docs/openapi.json` expose un OpenAPI simplifié pour import rapide dans Swagger UI.

Frontend React
--------------

- **Stack** : Vite + React 18 + Tailwind CSS + React Router.
- **Etat global** : contexte `AuthContext` (persisté en `localStorage`, tokens + profil).
- **API** : Axios + interceptors (refresh token automatique).
- **UI** : Layout responsive avec navigation latérale, pages spécialisées (Dashboard, Departements, Familles, Evenements, Annonces, Medias, Dons, Profil, Admin).
- **Carte FI** : Leaflet (markers + popup, recherche code postal).

Flux de données et rôles
------------------------

- `admin`: accès complet, gestion des rôles et exports.
- `department_lead`: gestion de son département, annonces ciblées.
- `family_lead`: gestion de sa Famille d’Impact, annonces FI.
- `member`: navigation personnelle, inscriptions événements, dons, profil.

Migrations & Seed
-----------------

- Initialisation base : `flask db upgrade`.
- Ajout de données exemples : `flask seed-db`.
- Pour créer une migration : `flask db migrate -m "message"` puis `flask db upgrade`.

Docker
------

```bash
docker compose up --build
```

Services exposés :

- Frontend : `http://localhost:5173`
- Backend : `http://localhost:5000`

Le volume `backend-db` stocke la base SQLite (monté sur `backend/instance`).

Préparation Firestore
---------------------

Le fichier `backend/app/services/firestore_mapping.py` documente les collections et sous-collections cibles. Chaque entité SQL dispose d’un mapping direct (users, departments, families, events, announcements, donations, media_items) pour accélérer une migration progressive vers Google Firestore.

API & Documentation
-------------------

- Base URL API : `http://localhost:5000/api`
- Endpoints principaux :
  - `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/refresh`
  - `GET|POST /api/departments`, `GET /api/departments/<id>`
  - `GET|POST /api/families`, `POST /api/families/find`
  - `GET|POST /api/events`, `POST /api/events/<id>/participants`
  - `GET|POST /api/announcements`
  - `GET|POST /api/media`
  - `GET|POST /api/donations`, `GET /api/donations/summary`
  - `GET /api/members`, `GET /api/members/<id>`
  - `GET /api/admin/dashboard`
- Spécification OpenAPI : `GET /api/docs/openapi.json`

Notes finales
-------------

- Compte admin par défaut (seed) : `admin@impact-sherbrooke.ca` / `Impact123!`
- En dev, la base SQLite est située dans `backend/instance/impact.db`.
- Adapter les variables d’environnement (`backend/.env.example`) avant déploiement (secrets, tokens Stripe/PayPal, etc.).

Déploiement sur Railway
-----------------------

Les fichiers `railway.toml` et `Procfile` préparent un déploiement automatique (builder Nixpacks).

1. **Variables d’environnement** à définir dans Railway :
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
   - `DATABASE_URL` (laisser vide pour SQLite embarqué ou pointer vers Postgres/MySQL)
2. Railway exécutera automatiquement :
   - `pip install -r backend/requirements.txt`
   - `npm install --prefix frontend`
   - `npm run build --prefix frontend` (le bundle est copié dans `backend/app/static/frontend`)
   - `gunicorn app:create_app --chdir backend --bind 0.0.0.0:$PORT`
3. Santé : l’endpoint `https://<ton-app>.railway.app/api/docs` peut servir de healthcheck rapide.
