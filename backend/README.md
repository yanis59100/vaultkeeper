# VaultKeeper Backend API

Backend API sécurisé pour VaultKeeper avec architecture Zero-Knowledge.

## 🔐 Architecture Zero-Knowledge

**Principe:** Le serveur ne voit JAMAIS vos mots de passe en clair.

- ✅ Cryptage client-side (AES-256-GCM)
- ✅ Seules les données cryptées sont transmises
- ✅ Le serveur stocke uniquement des blobs chiffrés
- ✅ Même en cas de hack du serveur, données illisibles
- ✅ Même les administrateurs ne peuvent pas lire vos mots de passe

## 🚀 Installation

### Prérequis

- Node.js 18+ 
- PostgreSQL 14+

### 1. Installer les dépendances

```bash
cd backend
npm install
```

### 2. Configuration

Créer un fichier `.env`:

```bash
cp .env.example .env
```

Éditer `.env` et configurer:
- `DATABASE_URL` - URL PostgreSQL
- `JWT_SECRET` - Clé secrète JWT (min 32 caractères)
- `PORT` - Port du serveur (défaut: 3000)

### 3. Initialiser la base de données

```bash
npm run init-db
```

### 4. Lancer le serveur

```bash
# Development
npm run dev

# Production
npm start
```

## 📡 API Endpoints

### Authentification

#### POST /api/auth/register
Créer un compte utilisateur.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "message": "Compte créé avec succès",
  "token": "jwt-token...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "createdAt": "2026-01-21T..."
  }
}
```

#### POST /api/auth/login
Se connecter.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "message": "Connexion réussie",
  "token": "jwt-token...",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

#### GET /api/auth/verify
Vérifier la validité d'un token.

**Headers:**
```
Authorization: Bearer jwt-token...
```

**Response:**
```json
{
  "valid": true,
  "userId": 1,
  "email": "user@example.com"
}
```

### Coffre (Vault)

Tous les endpoints requièrent authentification (Bearer token).

#### GET /api/vault
Récupérer son coffre crypté.

**Response:**
```json
{
  "encryptedData": "base64-encrypted-vault...",
  "salt": "base64-salt...",
  "version": 5,
  "updatedAt": "2026-01-21T..."
}
```

#### POST /api/vault/sync
Synchroniser/uploader son coffre.

**Body:**
```json
{
  "encryptedData": "base64-encrypted-vault...",
  "salt": "base64-salt..."
}
```

**Response:**
```json
{
  "message": "Coffre synchronisé avec succès",
  "version": 6,
  "updatedAt": "2026-01-21T..."
}
```

#### DELETE /api/vault
Supprimer son coffre.

**Response:**
```json
{
  "message": "Coffre supprimé avec succès"
}
```

#### GET /api/vault/history
Historique des 10 dernières synchronisations.

**Response:**
```json
{
  "history": [
    {
      "action": "upload",
      "timestamp": "2026-01-21T...",
      "ip_address": "192.168.1.1"
    }
  ]
}
```

## 🔒 Sécurité

### Mesures implémentées

- ✅ **HTTPS obligatoire** en production
- ✅ **Helmet.js** - Headers de sécurité
- ✅ **CORS strict** - Origines autorisées uniquement
- ✅ **Rate limiting** - 100 req/15min (5 req/15min pour auth)
- ✅ **JWT tokens** - Expiration 7 jours
- ✅ **Bcrypt** - Hashing mots de passe (12 rounds)
- ✅ **Validation** - Express-validator sur tous les inputs
- ✅ **SQL injection protected** - Parameterized queries
- ✅ **Zero-Knowledge** - Serveur ne voit jamais les données en clair

### Recommandations de déploiement

1. **HTTPS uniquement** - Utiliser Let's Encrypt
2. **Variables d'environnement** - Ne jamais commiter .env
3. **Monitoring** - Logs centralisés
4. **Backups** - Base de données quotidiens
5. **Firewall** - Limiter accès PostgreSQL

## 🌍 Déploiement

### Option 1: Railway (Recommandé - Gratuit)

1. Créer compte sur https://railway.app
2. Connecter GitHub
3. Créer nouveau projet depuis repo
4. Ajouter PostgreSQL addon
5. Configurer variables d'environnement
6. Déployer!

**Gratuit:** 500h/mois, 5GB stockage

### Option 2: Render

1. Créer compte sur https://render.com
2. New Web Service depuis GitHub
3. Environment: Node
4. Build: `npm install`
5. Start: `npm start`
6. Ajouter PostgreSQL database
7. Configurer env vars

**Gratuit:** Service se met en veille après 15min inactivité

### Option 3: Heroku

```bash
heroku create vaultkeeper-api
heroku addons:create heroku-postgresql:mini
heroku config:set JWT_SECRET=your-secret
git push heroku main
```

### Variables d'environnement requises

```
DATABASE_URL=postgresql://...
JWT_SECRET=your-super-secret-key
NODE_ENV=production
PORT=3000
CORS_ORIGINS=https://yanis59100.github.io,chrome-extension://*
```

## 🧪 Tests

```bash
# Coming soon
npm test
```

## 📊 Structure

```
backend/
├── config/
│   └── database.js          # PostgreSQL connection
├── database/
│   └── schema.sql           # Database schema
├── middleware/
│   ├── auth.js              # JWT authentication
│   └── errorHandler.js      # Error handling
├── routes/
│   ├── auth.js              # Auth endpoints
│   └── vault.js             # Vault endpoints
├── scripts/
│   └── init-db.js           # Database initialization
├── .env.example             # Example environment vars
├── package.json
└── server.js                # Main server file
```

## 🤝 Contribution

Les contributions sont les bienvenues! 

## 📜 Licence

MIT License - Libre d'utilisation

---

**Développé avec ❤️ pour VaultKeeper**
