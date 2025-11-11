# Impact Centre Chrétien Sherbrooke - Plateforme Web

Une application web complète développée avec Flask pour gérer la vie communautaire de l'église Impact Centre Chrétien Sherbrooke.

## 🎯 Fonctionnalités

### 🔐 Authentification & Gestion des utilisateurs
- Inscription et connexion sécurisées
- Gestion des rôles (Admin, Responsable Département, Responsable Famille, Membre)
- Profils utilisateurs complets avec informations personnelles et spirituelles

### 🏢 Gestion des Départements
- Création et gestion des départements de l'église
- Attribution de responsables
- Système d'adhésion aux départements
- Annonces ciblées par département

### 🏠 Familles d'Impact (Groupes de maison)
- Gestion des groupes de maison avec localisation
- Carte interactive des Familles d'Impact
- Système de demande d'adhésion
- Gestion des capacités et horaires

### 📅 Événements
- Calendrier interactif des événements
- Inscription aux événements
- Événements globaux, par département ou par famille
- Gestion des capacités et listes d'attente

### 📢 Système d'annonces
- Annonces globales et ciblées
- Niveaux de priorité
- Épinglage d'annonces importantes

### 🎥 Médias
- Intégration de vidéos YouTube
- Lecteur audio intégré
- Téléchargement de documents PDF
- Catégorisation des contenus

### 💸 Dons en ligne
- Interface de dons sécurisée
- Historique des dons
- Génération de reçus fiscaux
- Résumés annuels

### 🧑‍💼 Administration
- Dashboard administrateur complet
- Gestion centralisée des utilisateurs
- Statistiques et rapports
- Export de données

## 🛠️ Technologies utilisées

- **Backend**: Python 3.8+ avec Flask
- **Base de données**: SQLite (développement) avec SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Authentification**: Flask-Login avec sessions sécurisées
- **Migrations**: Alembic
- **Templates**: Jinja2

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet** (si applicable)
   ```bash
   git clone <repository-url>
   cd impact-centre-chr-tien-Sherbrooke
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurer les variables d'environnement**
   - Copier le fichier `.env` et ajuster les valeurs selon vos besoins
   - Configurer les clés Stripe pour les dons (optionnel)
   - Configurer les paramètres email (optionnel)

6. **Initialiser la base de données**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Créer les données de démonstration**
   ```bash
   flask init-db
   ```
   > Besoin d'un aperçu complet ? [python seed/seed.py](seed/seed.py) pour avoir accès à plus de détails sur les données générées.

8. **Lancer l'application**
   ```bash
   python app.py
   ```

L'application sera accessible à l'adresse: `http://localhost:5000`

## 👤 Comptes de démonstration

Après l'initialisation de la base de données, vous pouvez utiliser ces comptes:

### Administrateur
- **Email**: admin@impactcentre.ca
- **Mot de passe**: admin123

### Utilisateurs de test
- **Email**: jean.dupont@email.com
- **Mot de passe**: password123
- **Rôle**: Responsable Département

- **Email**: marie.martin@email.com
- **Mot de passe**: password123
- **Rôle**: Responsable Famille

- **Email**: pierre.gagnon@email.com
- **Mot de passe**: password123
- **Rôle**: Membre

## 🗂️ Structure du projet

```
impact-centre-chr-tien-Sherbrooke/
├── app/
│   ├── models/          # Modèles de base de données
│   ├── routes/          # Routes/Blueprints Flask
│   ├── templates/       # Templates HTML Jinja2
│   ├── static/          # Fichiers statiques (CSS, JS, images)
│   └── __init__.py      # Factory de l'application
├── migrations/          # Migrations Alembic
├── config.py           # Configuration de l'application
├── app.py              # Point d'entrée principal
├── requirements.txt    # Dépendances Python
├── .env               # Variables d'environnement
└── README.md          # Documentation
```

## 🚀 Déploiement

### Préparation pour la production

1. **Modifier la configuration**
   - Changer `FLASK_ENV=production` dans `.env`
   - Utiliser une base de données PostgreSQL ou MySQL
   - Configurer une clé secrète forte

2. **Configurer les services externes**
   - Stripe pour les paiements
   - Service email (Gmail, SendGrid, etc.)

3. **Déploiement avec Docker** (optionnel)
   ```bash
   # Créer l'image Docker
   docker build -t impact-centre-app .
   
   # Lancer le conteneur
   docker run -p 5000:5000 impact-centre-app
   ```

## 🔧 Migration vers Firebase Firestore

L'application est conçue pour faciliter une future migration vers Firebase Firestore:

- Structure de données compatible avec les collections Firestore
- Évitement des jointures complexes
- Modèles adaptés pour la dénormalisation

## 🤝 Contribution

Pour contribuer au projet:

1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## 📄 Licence

Ce projet est développé spécifiquement pour Impact Centre Chrétien Sherbrooke.

## 📞 Support

Pour toute question ou support technique, contactez l'équipe de développement.

---

**Développé avec ❤️ pour la communauté Impact Centre Chrétien Sherbrooke**
