# Installation Browser Extension - Password Manager Pro v3.0

## Vue d'ensemble

L'extension Password Manager Pro offre:
- 🔐 Auto-fill automatique des champs de connexion
- 📋 Accès rapide à vos comptes
- 📊 Visualisation des logs d'audit
- 🔑 Détection automatique de site
- 💾 Synchronisation avec l'API locale

## Installation sur Firefox

### Étape 1: Préparer les fichiers
```
password-manager/
├── browser_extension_firefox.json      (manifest.json)
├── browser_extension_background.js     (background.js)
├── browser_extension_content.js        (content.js)
├── browser_extension_popup.html        (popup.html)
└── browser_extension_popup.js          (popup.js)
```

### Étape 2: Créer la structure du dossier
```bash
mkdir -p firefox_extension
cp browser_extension_firefox.json firefox_extension/manifest.json
cp browser_extension_background.js firefox_extension/background.js
cp browser_extension_content.js firefox_extension/content.js
cp browser_extension_popup.html firefox_extension/popup.html
cp browser_extension_popup.js firefox_extension/popup.js
```

### Étape 3: Charger l'extension en dev
1. Ouvrir Firefox
2. Aller à `about:debugging#/runtime/this-firefox`
3. Cliquer "Charger un module temporaire"
4. Sélectionner le fichier `manifest.json` du dossier `firefox_extension/`
5. L'extension apparaît dans la barre d'outils

### Étape 4: Empaqueter pour distribution (optionnel)
```bash
cd firefox_extension
# Créer un ZIP avec tous les fichiers
zip -r password-manager-pro.zip manifest.json background.js content.js popup.html popup.js
```

## Installation sur Chrome/Chromium

### Étape 1: Adapter le manifest pour Chrome
Le fichier `manifest.json` fonctionne aussi pour Chrome (même format v3)

### Étape 2: Charger l'extension
1. Ouvrir Chrome/Brave/Edge
2. Aller à `chrome://extensions/`
3. Activer "Mode développeur" (haut à droite)
4. Cliquer "Charger l'extension non empaquetée"
5. Sélectionner le dossier de l'extension

### Étape 3: Utilisation immédiate
- L'extension est chargée et fonctionnelle
- L'icône 🔐 apparaît dans la barre d'outils

## Utilisation de l'extension

### 1. Première connexion
1. Cliquer sur l'icône 🔐 dans la barre d'outils
2. Entrer vos identifiants
3. Optionnel: Entrer votre code 2FA
4. Cliquer "Se connecter"

### 2. Auto-fill automatique
- L'extension détecte les champs de mot de passe
- Une icône 🔑 verte apparaît à droite du champ
- Cliquer sur 🔑 pour voir les comptes disponibles
- Sélectionner le compte pour remplir automatiquement

### 3. Accès rapide
- Cliquer sur l'icône 🔐 pour voir tous vos comptes
- Cliquer sur "Copier" pour copier le mot de passe
- "🔄 Actualiser" pour recharger la liste
- "📋 Logs" pour voir l'historique d'audit
- "🚪 Déconnexion" pour se déconnecter

### 4. Contexte menu
- Clic droit dans un champ → "Remplir avec Password Manager"
- Remplissage rapide du champ

## Configuration requise

### API locale
L'extension nécessite que l'API soit lancée:
```bash
python api.py
# Ou si intégré au GUI
# L'API démarre automatiquement avec le gestionnaire
```

### Serveur local
- URL: `http://localhost:8000`
- Endpoints: `/login`, `/accounts`, `/audit-logs`, `/health`
- JWT authentication activée

### Navigateurs supportés
- ✅ Firefox 115+
- ✅ Chrome 120+
- ✅ Brave (compatible Chrome)
- ✅ Edge 120+
- ✅ Opera (compatible Chrome)

## Sécurité de l'extension

### 1. Stockage local
- Token JWT stocké dans `chrome.storage.local`
- Suppression automatique à la déconnexion
- Pas de stockage en clair du mot de passe

### 2. Communication
- Toutes les requêtes utilisent HTTPS (recommandé)
- JWT token pour authentification API
- Content Security Policy activée

### 3. Permissions minimales
- `activeTab`: Détection du site actif
- `scripting`: Injection de code pour auto-fill
- `storage`: Stockage du token
- `webNavigation`: Suivi des changements de pages

### 4. Bonnes pratiques
- ✓ Ne jamais stocker le mot de passe maître
- ✓ Token expiration: Configurable via API
- ✓ Logout automatique possible
- ✓ Audit log des tous les remplissages

## Dépannage

### L'extension ne se charge pas
```
Vérifier:
1. Les fichiers manifest.json, background.js, content.js, popup.html, popup.js existent
2. Le manifest.json est valide (pas d'erreurs de syntaxe JSON)
3. Le chemin est correct lors du chargement
```

### Auto-fill ne fonctionne pas
```
Vérifier:
1. L'API est lancée (http://localhost:8000/health)
2. Vous êtes connecté (vérifier le popup)
3. Le site a un compte configuré
4. JavaScript est activé dans le navigateur
5. L'extension a les permissions (chrome://extensions → détails)
```

### Erreur "API Error: 401"
```
Vérifier:
1. Vous êtes connecté
2. Le token JWT est valide
3. Relancer l'extension ou vous reconnecter
```

### La connexion échoue
```
Vérifier:
1. API locale lancée: python api.py
2. Port 8000 est disponible (netstat -an | grep 8000)
3. Identifiants corrects
4. 2FA correct si activé
```

## Développement

### Modification du popup
Éditer `browser_extension_popup.js` et `browser_extension_popup.html`, puis recharger l'extension:
- Firefox: Clic droit sur l'extension → Recharger
- Chrome: chrome://extensions → Recharger

### Modification du content script
Éditer `browser_extension_content.js`, puis:
1. Recharger l'extension
2. Actualiser la page (Ctrl+R)

### Debugging
- Firefox: `about:debugging` → Extension → "Inspecter"
- Chrome: chrome://extensions → Details → "Background page" ou "Service Worker"
- Console du navigateur: F12 → Console

### Logs
Tous les remplissages sont loggés:
- Logs audit: Visible via "📋 Logs" dans le popup
- API logs: Visible dans la console du serveur
- Browser logs: F12 → Console

## APIs disponibles

### POST /login
```json
{
  "username": "user",
  "password": "pass",
  "totp": "123456"  // optionnel
}
```

### GET /accounts
Retourne la liste de tous les comptes de l'utilisateur

### GET /audit-logs
Retourne les logs d'audit avec timestamps

### GET /health
Vérifie l'état de l'API

## Version de l'extension

- **Version**: 3.0.0
- **Manifest version**: 3 (moderne et sécurisé)
- **Dernière mise à jour**: 2024
- **Auteur**: Password Manager Pro Team

## Support

Pour les problèmes:
1. Vérifier les logs (F12 → Console)
2. Vérifier que l'API est lancée
3. Relancer l'extension
4. Vérifier les permissions

---

✓ Installation et utilisation de l'extension terminées
