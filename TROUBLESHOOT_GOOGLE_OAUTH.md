# 🔧 DÉPANNAGE - Google OAuth "invalid_client"

## ❌ Erreur: "OAuth client was not found" / "401: invalid_client"

### Cause
Le fichier `google_credentials.json` n'existe pas ou n'est pas valide.

---

## ✅ SOLUTION - Étapes à suivre

### Étape 1: Créer un projet Google Cloud (5 minutes)

```
1. Allez sur: https://console.cloud.google.com/
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create Project"
4. Nom: "Password Manager" (ou autre)
5. Cliquez "Create"
```

### Étape 2: Créer les credentials OAuth (5 minutes)

```
1. Allez à: APIs & Services > Credentials
2. Cliquez "+ Create Credentials" > "OAuth client ID"
3. Si demandé: Configurez l'écran de consentement OAuth
   - Type d'application: "Desktop"
   - Remplissez les champs
   - Sauvegardez
4. Revenez à Credentials
5. Cliquez "+ Create Credentials" > "OAuth client ID"
6. Sélectionnez "Desktop application"
7. Cliquez "Create"
8. Une popup s'affiche avec vos credentials
9. Cliquez l'icône download (télécharger le JSON)
```

### Étape 3: Placer le fichier credentials (2 minutes)

**Option A: Depuis le dossier du projet**
```
1. Le fichier JSON téléchargé est nommé quelque chose comme:
   client_secret_XXXXX.apps.googleusercontent.com.json

2. Renommez-le en: google_credentials.json

3. Placez-le dans:
   C:\Users\[VotreNom]\OneDrive\Bureau\password-manager\

4. IMPORTANT: À côté de PasswordManager.exe ET du dossier dist/

   Structure:
   password-manager/
   ├── PasswordManager.exe
   ├── google_credentials.json      ← ICI
   ├── dist/
   │   └── PasswordManager.exe
   └── ...
```

**Option B: Depuis l'exécutable compilé**
```
1. Même fichier que ci-dessus

2. Placez-le AUSSI dans le dossier dist/:
   password-manager/dist/
   ├── PasswordManager.exe
   └── google_credentials.json      ← ICI

   Cela permet à l'exe de trouver les credentials
```

### Étape 4: Vérifier les autorisation de redirection (3 minutes)

```
1. Allez à: Google Cloud Console > Credentials
2. Cliquez sur votre "OAuth 2.0 Client IDs" (Bureau)
3. Vérifiez "Authorized redirect URIs"
4. Doit contenir: http://localhost:8888/
5. Si absent, ajoutez-le
6. Cliquez "Save"
```

### Étape 5: Tester (1 minute)

```
1. Double-cliquez PasswordManager.exe
2. Cliquez "🔗 Se connecter avec Google"
3. Un navigateur s'ouvrira
4. Connectez-vous avec votre compte Google
5. Autorisez l'accès
6. ✅ Succès !
```

---

## 🔍 Vérifications rapides

### Le fichier google_credentials.json existe?
```
Windows:
1. Ouvrez l'Explorateur de fichiers
2. Allez dans: C:\Users\[VotreNom]\OneDrive\Bureau\password-manager\
3. Cherchez le fichier: google_credentials.json
4. Si absent ❌ → Refaites les étapes 1-3
5. Si présent ✅ → Continuez
```

### Le fichier est valide?
```
1. Double-cliquez google_credentials.json
2. Ouvre avec VS Code ou Notepad
3. Vérifiez qu'il contient:
   - "client_id"
   - "client_secret"
   - "redirect_uris" incluant "http://localhost:8888/"
4. Si absent ❌ → Le fichier est corrompu, retéléchargez-le
5. Si présent ✅ → Bon !
```

### Les valeurs par défaut?
```
Vérifiez que le fichier NE contient PAS:
- "YOUR_CLIENT_ID"
- "YOUR_CLIENT_SECRET"

Si présent ❌ → Vous avez ouvert l'exemple, pas le vrai fichier
Si absent ✅ → Correct !
```

---

## 🆘 Erreurs courantes

### "Erreur 401: invalid_client"
**Cause**: Credentials invalides ou expirées
**Solution**:
1. Retéléchargez les credentials depuis Google Cloud Console
2. Vérifiez client_id et client_secret
3. Remplacez google_credentials.json

### "Fichier google_credentials.json non trouvé"
**Cause**: Fichier au mauvais endroit
**Solution**:
1. Vérifiez le chemin exact
2. Doit être dans le même dossier que l'exe
3. Vérifiez l'extension (.json, pas .txt)

### "Impossible de redirection (redirect_uri)"
**Cause**: http://localhost:8888/ pas autorisé
**Solution**:
1. Google Cloud Console > Credentials
2. Cliquez sur votre OAuth Client
3. Ajoutez: http://localhost:8888/
4. Sauvegardez

### "Port 8888 déjà utilisé"
**Cause**: Autre application utilise le port
**Solution**:
1. Fermez l'autre application
2. Ou redémarrez l'ordinateur

### "Navigateur ne s'ouvre pas"
**Cause**: Navigateur par défaut pas configuré
**Solution**:
1. Ouvrez manuellement: http://localhost:8888
2. Vous pouvez voir la page de connexion

---

## 📝 Exemple de fichier valide

```json
{
  "installed": {
    "client_id": "123456789-abcdefghijklmnop.apps.googleusercontent.com",
    "client_secret": "GOCSPX-xxxxxxxxxxxxxxxxxxxx",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "redirect_uris": [
      "http://localhost:8888/"
    ]
  }
}
```

**⚠️ ATTENTION**: Gardez ce fichier SECRET!
- Ne le partagez jamais
- Ne le commitez pas sur GitHub
- Seul vous devez le voir

---

## 🎯 Résumé rapide

| Étape | Action | Temps |
|-------|--------|-------|
| 1 | Créer projet Google Cloud | 5 min |
| 2 | Créer OAuth2 Credentials | 5 min |
| 3 | Télécharger JSON | 1 min |
| 4 | Renommer en google_credentials.json | 1 min |
| 5 | Placer dans le dossier | 1 min |
| 6 | Vérifier les redirect URIs | 2 min |
| 7 | Tester | 1 min |
| **TOTAL** | | **16 min** |

---

## ✅ Vérification finale

Avant de relancer l'application:

- [ ] google_credentials.json existe
- [ ] Fichier contient client_id et client_secret
- [ ] Pas de valeurs "YOUR_..."
- [ ] Fichier est dans: password-manager/ (dossier du projet)
- [ ] Fichier est aussi dans: password-manager/dist/ (pour l'exe)
- [ ] http://localhost:8888/ est dans Authorized redirect URIs
- [ ] Connexion internet fonctionnelle

---

## 🆘 Si ça ne marche toujours pas

1. Fermez complètement l'application
2. Supprimez le dossier `.users/` (vous perdrez les données)
3. Redémarrez l'application
4. Retentez la connexion Google

---

**Besoin d'aide?**
Consultez:
- QUICK_SETUP.md - Installation rapide
- GOOGLE_OAUTH_SETUP.md - Guide complet
- GUIDE_UTILISATEUR_v2.1.md - Guide utilisateur

**Bon courage! 🚀**
