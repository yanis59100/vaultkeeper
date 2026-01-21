# 🚀 Guide de démarrage rapide VaultKeeper Backend

## Installation locale (5 minutes)

### 1. Installer PostgreSQL

**Windows:**
- Télécharge: https://www.postgresql.org/download/windows/
- Installe avec mdp: `postgres`
- Port par défaut: 5432

**OU utilise une base cloud gratuite:**
- Supabase: https://supabase.com (gratuit, 500MB)
- Neon: https://neon.tech (gratuit, 3GB)

### 2. Installer les dépendances

```bash
cd backend
npm install
```

### 3. Configurer l'environnement

```bash
# Copier le fichier exemple
copy .env.example .env

# Éditer .env avec Notepad
notepad .env
```

**Modifier dans .env:**
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/vaultkeeper
JWT_SECRET=ton-secret-jwt-ultra-securise-min-32-caracteres-aleatoires
```

### 4. Créer la base de données

```bash
# Ouvrir psql
psql -U postgres

# Créer la base
CREATE DATABASE vaultkeeper;
\q
```

### 5. Initialiser les tables

```bash
npm run init-db
```

**Tu devrais voir:**
```
✅ Database initialized successfully!
📊 Tables created: users, vaults, sync_logs
```

### 6. Lancer le serveur

```bash
npm run dev
```

**Tu devrais voir:**
```
🚀 VaultKeeper Backend running on port 3000
📊 Environment: development
🔐 JWT expires in: 7d
✅ Connected to PostgreSQL database
```

### 7. Tester l'API

Ouvre: http://localhost:3000/health

**Tu devrais voir:**
```json
{
  "status": "ok",
  "timestamp": "2026-01-21T...",
  "version": "1.0.0"
}
```

## ✅ Installation terminée!

**Prochaines étapes:**
1. Modifier `chrome-extension/api.js` → Changer `baseURL` si déployé
2. Tester l'inscription depuis l'extension
3. Tester la synchronisation

## 🌐 Déploiement gratuit (Railway)

### 1. Créer compte Railway

https://railway.app → Sign up with GitHub

### 2. Nouveau projet

- Click "New Project"
- "Deploy from GitHub repo"
- Sélectionne `vaultkeeper`
- Railway détecte automatiquement Node.js

### 3. Ajouter PostgreSQL

- Click "+ New"
- "Database" → "Add PostgreSQL"
- Railway crée automatiquement DATABASE_URL

### 4. Variables d'environnement

Settings → Variables:
```
JWT_SECRET=ton-secret-genere-aleatoire
NODE_ENV=production
CORS_ORIGINS=https://yanis59100.github.io,chrome-extension://*
```

### 5. Déployer

- Railway déploie automatiquement
- URL fournie: `https://vaultkeeper-production.up.railway.app`
- Copie cette URL pour l'extension

### 6. Mettre à jour l'extension

Dans `chrome-extension/api.js`:
```javascript
this.baseURL = 'https://vaultkeeper-production.up.railway.app/api';
```

## 🎉 C'est terminé!

Ton backend est en ligne et sécurisé!
