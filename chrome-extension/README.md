# VaultKeeper - Extension Chrome

Extension Chrome pour VaultKeeper, gestionnaire de mots de passe sécurisé avec design cyberpunk.

## 🎨 Fonctionnalités

- 🔐 **Cryptage AES-256-GCM** - Sécurité militaire avec Web Crypto API
- 🎨 **Interface cyberpunk** - 30 particules animées, effets néon
- 💾 **Stockage local** - Toutes vos données restent sur votre machine
- ⭐ **Système de favoris** - Accès rapide à vos comptes importants
- 📊 **Indicateur de force** - Évaluez vos mots de passe en temps réel
- 🔧 **Générateur avancé** - Créez des mots de passe ultra-sécurisés
- ✏️ **Remplissage automatique** - Remplissez les formulaires en 1 clic
- 🔒 **Auto-lock** - Verrouillage après 15 minutes d'inactivité
- 📁 **6 catégories** - Banque, Email, Social, Travail, Gaming, Autre

## 📥 Installation

### Méthode 1: Mode Développeur (Test)

1. Ouvrez Chrome et allez dans `chrome://extensions/`
2. Activez **"Mode développeur"** (en haut à droite)
3. Cliquez sur **"Charger l'extension non empaquetée"**
4. Sélectionnez le dossier `chrome-extension`
5. L'icône VaultKeeper apparaît dans votre barre d'outils!

### Méthode 2: Chrome Web Store (À venir)

L'extension sera bientôt disponible sur le Chrome Web Store.

## 🚀 Utilisation

### Première utilisation

1. Cliquez sur l'icône VaultKeeper
2. Créez votre mot de passe maître (8+ caractères)
3. Votre coffre est créé!

### Ajouter un mot de passe

1. Cliquez sur l'icône **➕**
2. Remplissez les informations
3. Cliquez sur **💾 Enregistrer**

### Remplir automatiquement

1. Allez sur un site de connexion
2. Ouvrez VaultKeeper
3. Cliquez sur **✏️ Remplir** pour le compte voulu
4. Les champs sont remplis automatiquement!

### Générer un mot de passe

1. Cliquez sur l'icône **🎲**
2. Ajustez la longueur et les options
3. Cliquez sur **📋** pour copier

## 🔒 Sécurité

### Cryptage

- **Algorithme**: AES-256-GCM (Web Crypto API)
- **Dérivation**: PBKDF2 avec 100,000 itérations
- **Hash**: SHA-256

### Stockage

- Toutes les données sont stockées localement dans `chrome.storage.local`
- Les mots de passe sont chiffrés avant stockage
- Le mot de passe maître n'est jamais stocké
- Aucune transmission réseau

### Confidentialité

- ✅ Aucune collecte de données
- ✅ Aucune télémétrie
- ✅ Aucune connexion internet
- ✅ Code source ouvert et auditable

## 📝 Permissions requises

- **storage** - Pour sauvegarder vos mots de passe localement
- **activeTab** - Pour remplir automatiquement les formulaires
- **tabs** - Pour détecter les formulaires de connexion
- **scripting** - Pour injecter du code dans les pages web

## 🛠️ Développement

### Structure du projet

```
chrome-extension/
├── manifest.json       # Configuration de l'extension
├── popup.html          # Interface principale
├── popup.css           # Styles cyberpunk
├── popup.js            # Logique de l'interface
├── crypto.js           # Cryptage AES-256-GCM
├── background.js       # Service worker
├── content.js          # Script d'injection
├── icons/              # Icônes de l'extension
└── README.md           # Cette documentation
```

### Technologies utilisées

- **Manifest V3** - Dernière version des extensions Chrome
- **Web Crypto API** - Cryptage natif du navigateur
- **Chrome Storage API** - Stockage local sécurisé
- **Content Scripts** - Injection dans les pages web
- **Service Workers** - Gestion en arrière-plan

## 🐛 Problèmes connus

### "Extension non vérifiée"

C'est normal pour les extensions en mode développeur. Pour une utilisation permanente, attendez la publication sur Chrome Web Store.

### Perte de données

Si vous désinstallez l'extension, **toutes vos données seront perdues**. Exportez régulièrement vos mots de passe via l'app desktop.

## 🔗 Liens

- **App Desktop**: https://github.com/yanis59100/vaultkeeper
- **Site Web**: https://yanis59100.github.io/vaultkeeper
- **Développeur**: https://github.com/yanis59100

## 📜 Licence

MIT License - Libre et gratuit pour usage personnel et commercial.

---

**Fait avec ❤️ par yanis59100**
