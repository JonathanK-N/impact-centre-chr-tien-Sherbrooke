# 🚀 Guide d'Installation - Impact Centre Mobile

## 📋 Prérequis

### Système
- Node.js 18+ 
- npm ou yarn
- Git
- MongoDB (local ou Atlas)

### Mobile (React Native)
- Expo CLI: `npm install -g @expo/cli`
- Expo Go app sur votre téléphone
- Android Studio (pour Android)
- Xcode (pour iOS, macOS uniquement)

## 🛠️ Installation Backend (Next.js)

### 1. Setup du projet
```bash
cd backend
npm install
```

### 2. Configuration environnement
```bash
cp .env.example .env
```

Modifier `.env` avec vos valeurs:
```env
MONGODB_URI=mongodb://localhost:27017/impact-centre
JWT_SECRET=your-super-secret-jwt-key
STRIPE_SECRET_KEY=sk_test_your_stripe_key
```

### 3. Base de données
```bash
# Démarrer MongoDB localement
mongod

# Ou utiliser MongoDB Atlas (cloud)
# Remplacer MONGODB_URI dans .env
```

### 4. Lancer le serveur
```bash
npm run dev
```
Backend accessible sur: `http://localhost:3000`

## 📱 Installation Mobile (React Native)

### 1. Setup du projet
```bash
cd mobile
npm install
```

### 2. Configuration
Modifier `src/services/api.ts`:
```typescript
const API_BASE_URL = __DEV__ 
  ? 'http://YOUR_LOCAL_IP:3000/api'  // Remplacer par votre IP locale
  : 'https://your-backend.railway.app/api';
```

### 3. Lancer l'app
```bash
# Démarrer Expo
npm start

# Ou directement sur plateforme
npm run android  # Android
npm run ios      # iOS
```

## 🔧 Configuration Développement

### Backend API Routes
- `POST /api/auth/login` - Connexion
- `POST /api/auth/register` - Inscription  
- `GET /api/auth/me` - Profil utilisateur
- `GET /api/departments` - Liste départements
- `GET /api/events` - Liste événements
- `GET /api/families` - Liste familles

### Mobile Navigation
- **Auth Stack**: Login, Register
- **Main Tabs**: Dashboard, Events, Departments, Families, Profile

## 🧪 Tests

### Backend
```bash
cd backend
npm test
```

### Mobile
```bash
cd mobile
npm test
```

## 📱 Build Mobile

### Android
```bash
# Build APK de développement
eas build --platform android --profile development

# Build APK de production
eas build --platform android --profile production
```

### iOS
```bash
# Build iOS (nécessite compte Apple Developer)
eas build --platform ios --profile production
```

## 🚨 Dépannage

### Erreurs communes

**Backend ne démarre pas:**
- Vérifier MongoDB est démarré
- Vérifier les variables d'environnement
- Port 3000 disponible

**Mobile ne se connecte pas:**
- Vérifier l'IP locale dans api.ts
- Backend accessible depuis le téléphone
- Firewall/antivirus bloque la connexion

**Erreur de build mobile:**
```bash
# Nettoyer le cache
expo r -c
npm start -- --reset-cache
```

## 📚 Ressources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Native Documentation](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)

## 🆘 Support

Pour toute question:
1. Vérifier les logs d'erreur
2. Consulter la documentation
3. Contacter l'équipe de développement