# Guide d'Installation Rapide
## Impact Centre Chrétien Sherbrooke

### 🚀 Installation en 5 minutes

#### 1. Prérequis
- Python 3.8+ installé
- Git (optionnel)

#### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

#### 3. Initialisation de la base de données
```bash
python init_app.py
```

#### 4. Lancement de l'application
```bash
python run.py
```

#### 5. Accès à l'application
- **URL**: http://localhost:5000
- **Admin**: admin@impactcentre.ca / admin123

### 👥 Comptes de test disponibles

| Email | Mot de passe | Rôle |
|-------|--------------|------|
| admin@impactcentre.ca | admin123 | Administrateur |
| jean.dupont@email.com | password123 | Responsable Département |
| marie.martin@email.com | password123 | Responsable Famille |
| pierre.gagnon@email.com | password123 | Membre |
| sophie.lavoie@email.com | password123 | Nouveau membre |

### 🎯 Fonctionnalités disponibles

✅ **Authentification complète**
- Inscription/Connexion
- Gestion des rôles
- Profils utilisateurs

✅ **Gestion des départements**
- Adhésion aux départements
- Gestion par les responsables
- Annonces ciblées

✅ **Familles d'Impact**
- Groupes de maison
- Localisation géographique
- Gestion des capacités

✅ **Événements**
- Calendrier interactif
- Inscriptions en ligne
- Gestion des participants

✅ **Système d'annonces**
- Annonces globales et ciblées
- Niveaux de priorité
- Épinglage important

✅ **Dons en ligne**
- Interface de dons
- Historique personnel
- Reçus fiscaux

✅ **Médias**
- Vidéos YouTube
- Fichiers audio
- Documents PDF

✅ **Administration**
- Dashboard complet
- Gestion centralisée
- Statistiques détaillées

### 🔧 Configuration avancée

#### Variables d'environnement (.env)
```env
FLASK_ENV=development
SECRET_KEY=votre-clé-secrète
DATABASE_URL=sqlite:///impact_centre.db

# Stripe (optionnel)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Email (optionnel)
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app
```

#### Déploiement avec Docker
```bash
docker build -t impact-centre .
docker run -p 5000:5000 impact-centre
```

#### Déploiement avec Docker Compose
```bash
docker-compose up -d
```

### 📱 Interface responsive
L'application est entièrement responsive et fonctionne sur:
- 💻 Ordinateurs de bureau
- 📱 Tablettes
- 📱 Smartphones

### 🔒 Sécurité
- Sessions sécurisées avec Flask-Login
- Validation des formulaires
- Protection CSRF
- Hashage des mots de passe

### 📊 Base de données
- **Développement**: SQLite (incluse)
- **Production**: PostgreSQL recommandée
- **Migrations**: Alembic intégré

### 🆘 Support
Pour toute question ou problème:
1. Vérifiez que Python 3.8+ est installé
2. Vérifiez que toutes les dépendances sont installées
3. Consultez les logs d'erreur dans la console

### 🎉 Prêt à utiliser !
Votre plateforme communautaire est maintenant opérationnelle et prête à accueillir votre communauté !