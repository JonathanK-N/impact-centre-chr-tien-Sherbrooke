# 🚀 Guide de Déploiement - Impact Centre Mobile

## 🌐 Déploiement Backend sur Railway

### 1. Préparation
```bash
cd backend
npm install -g @railway/cli
railway login
```

### 2. Configuration Railway
```bash
# Créer nouveau projet
railway new

# Ou connecter projet existant
railway link [project-id]
```

### 3. Variables d'environnement
```bash
# Ajouter les variables via CLI
railway variables set MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/impact-centre
railway variables set JWT_SECRET=your-production-jwt-secret
railway variables set STRIPE_SECRET_KEY=sk_live_your_stripe_key
railway variables set NODE_ENV=production
```

### 4. Déploiement
```bash
# Déployer
railway up

# Ou via GitHub (recommandé)
# 1. Push vers GitHub
# 2. Connecter repo dans Railway dashboard
# 3. Auto-deploy activé
```

### 5. Configuration domaine
```bash
# Générer domaine Railway
railway domain

# Ou domaine personnalisé dans dashboard
# your-app.railway.app → api.impactcentre.ca
```

## 📱 Déploiement Mobile

### 1. Configuration EAS (Expo Application Services)
```bash
cd mobile
npm install -g eas-cli
eas login
```

### 2. Configuration projet
```bash
# Initialiser EAS
eas build:configure

# Créer eas.json
```

Exemple `eas.json`:
```json
{
  "cli": {
    "version": ">= 5.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {}
  }
}
```

### 3. Build Android
```bash
# Build APK de test
eas build --platform android --profile preview

# Build AAB pour Play Store
eas build --platform android --profile production
```

### 4. Build iOS
```bash
# Nécessite Apple Developer Account ($99/an)
eas build --platform ios --profile production
```

### 5. Publication
```bash
# Google Play Store
eas submit --platform android

# Apple App Store
eas submit --platform ios
```

## 🗄️ Base de données MongoDB Atlas

### 1. Création cluster
1. Aller sur [MongoDB Atlas](https://cloud.mongodb.com)
2. Créer compte/se connecter
3. Créer nouveau cluster (gratuit M0)
4. Configurer utilisateur et IP whitelist

### 2. Configuration
```bash
# String de connexion
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/impact-centre

# Ajouter dans Railway variables
railway variables set MONGODB_URI="mongodb+srv://..."
```

### 3. Migration données
```bash
# Export depuis SQLite (ancien)
python migrate_to_mongo.py

# Ou import manuel via MongoDB Compass
```

## 🔐 Configuration SSL/HTTPS

### Railway (automatique)
- SSL automatique sur domaines Railway
- Certificats Let's Encrypt
- HTTPS forcé en production

### Domaine personnalisé
1. Configurer DNS CNAME vers Railway
2. Ajouter domaine dans Railway dashboard
3. SSL automatique activé

## 📊 Monitoring et Logs

### Railway Logs
```bash
# Voir logs en temps réel
railway logs

# Logs spécifiques
railway logs --tail 100
```

### Monitoring mobile
- Expo Analytics (gratuit)
- Sentry pour crash reporting
- Firebase Analytics

## 🚀 CI/CD Pipeline

### GitHub Actions (recommandé)
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: railway/cli@v2
        with:
          command: up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Auto-deploy mobile
```yaml
# .github/workflows/mobile.yml
name: EAS Build

on:
  push:
    branches: [main]
    paths: ['mobile/**']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --platform android --non-interactive
```

## 🔄 Mise à jour OTA (Over-The-Air)

### Configuration
```bash
# Publier mise à jour
eas update --branch production --message "Fix login bug"

# Auto-update dans app.json
{
  "expo": {
    "updates": {
      "url": "https://u.expo.dev/[project-id]"
    }
  }
}
```

## 📋 Checklist Déploiement

### Backend
- [ ] Variables d'environnement configurées
- [ ] Base de données MongoDB Atlas
- [ ] SSL/HTTPS activé
- [ ] Logs monitoring configuré
- [ ] Backup base de données

### Mobile
- [ ] API_BASE_URL mis à jour
- [ ] Icons et splash screen
- [ ] Permissions configurées
- [ ] Store listings préparés
- [ ] Tests sur devices réels

### Post-déploiement
- [ ] Tests fonctionnels complets
- [ ] Performance monitoring
- [ ] Crash reporting activé
- [ ] Analytics configurées
- [ ] Documentation mise à jour

## 🆘 Rollback

### Backend
```bash
# Rollback Railway
railway rollback [deployment-id]
```

### Mobile
```bash
# Rollback OTA
eas update --branch production --message "Rollback" --republish
```

## 📞 Support Production

### Monitoring
- Railway dashboard pour backend
- Expo dashboard pour mobile
- MongoDB Atlas pour base de données

### Alertes
- Railway notifications
- Expo crash reports
- MongoDB Atlas alerts

### Maintenance
- Backups automatiques MongoDB
- Logs rotation Railway
- Updates sécurité régulières