# 🚀 Déploiement sur Railway

## Étapes de déploiement

### 1. Préparer le repository
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Déployer sur Railway
1. Aller sur [railway.app](https://railway.app)
2. Se connecter avec GitHub
3. Cliquer "New Project" → "Deploy from GitHub repo"
4. Sélectionner votre repository
5. Railway détectera automatiquement les fichiers de configuration

### 3. Variables d'environnement (optionnelles)
Dans Railway Dashboard → Variables :
```
FLASK_ENV=production
SECRET_KEY=votre-clé-secrète-forte
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

### 4. Base de données
Railway créera automatiquement une base de données SQLite.
Pour PostgreSQL (recommandé en production) :
1. Ajouter PostgreSQL service dans Railway
2. Connecter à votre app
3. Railway configurera automatiquement DATABASE_URL

## ✅ Fichiers créés pour Railway
- `railway.json` - Configuration Railway
- `Procfile` - Commande de démarrage
- `nixpacks.toml` - Configuration build
- `requirements.txt` - Dépendances (avec gunicorn)

## 🔗 Accès après déploiement
- URL automatique : `https://votre-app.railway.app`
- Admin : admin@impactcentre.ca / admin123

## 📊 Monitoring
Railway fournit automatiquement :
- Logs en temps réel
- Métriques de performance
- Redémarrages automatiques
- SSL/HTTPS