# 🔗 Configuration Google OAuth - Étapes pour Lostyxs59@gmail.com

## ❌ Vous avez reçu: "OAuth client was not found" / "Erreur 401: invalid_client"

### La Solution: Créer un fichier `google_credentials.json`

---

## 📋 5 Étapes Rapides (15 minutes)

### ✅ Étape 1: Créer un projet Google Cloud

```
1. Ouvrez: https://console.cloud.google.com/
2. En haut à gauche, cliquez sur "Select a project"
3. Cliquez "New Project"
4. Nom: "Password Manager"
5. Cliquez "Create"
6. Attendez 1-2 minutes
```

### ✅ Étape 2: Créer les credentials OAuth

```
1. Dans Google Cloud Console
2. À gauche, cliquez "APIs & Services"
3. Cliquez "Credentials"
4. Cliquez le bouton bleu "+ Create Credentials"
5. Sélectionnez "OAuth client ID"

Si on vous demande "Create OAuth consent screen":
  - Cliquez "Create"
  - Type d'appli: "Desktop"
  - Cliquez "Create"
  
7. Maintenant, retournez à Credentials
8. Cliquez "+ Create Credentials"
9. Sélectionnez "OAuth client ID"
10. Type: "Desktop application"
11. Cliquez "Create"
12. Une popup s'affiche ✅
```

### ✅ Étape 3: Télécharger le JSON

```
Dans la popup (ou dans Credentials si elle s'est fermée):
1. Trouvez votre "OAuth 2.0 Client ID" (type: "Desktop")
2. À droite, cliquez l'icône "Download" (⬇️)
3. Un fichier JSON se télécharge
4. Il s'appelle quelque chose comme: "client_secret_XXXXX.json"
```

### ✅ Étape 4: Renommer et placer le fichier

**Sur votre ordinateur:**

```
1. Le fichier téléchargé est: client_secret_XXXXX.json
   (vous pouvez le trouver dans: C:\Users\[VotreNom]\Downloads\)

2. Renommez-le en: google_credentials.json

3. Copiez-le DANS le dossier du Password Manager:
   C:\Users\[VotreNom]\OneDrive\Bureau\password-manager\

   Structure finale:
   C:\Users\[VotreNom]\OneDrive\Bureau\password-manager\
   ├── PasswordManager.exe
   ├── google_credentials.json          ← PLACER ICI
   ├── dist\
   │   └── PasswordManager.exe
   └── ...
```

### ✅ Étape 5: Vérifier les redirects autorisés

**Back dans Google Cloud Console:**

```
1. Allez à: Credentials
2. Cliquez sur votre "OAuth 2.0 Client IDs" (Desktop)
3. Regardez: "Authorized redirect URIs"
4. Vérifiez qu'il contient: http://localhost:8888/
5. Si ABSENT, cliquez "Edit", ajoutez-le, et cliquez "Save"
```

---

## 🚀 Tester maintenant!

```
1. Double-cliquez: PasswordManager.exe
2. Cliquez: "🔗 Se connecter avec Google"
3. Un navigateur s'ouvrira
4. Connectez-vous avec: Lostyxs59@gmail.com
5. Cliquez "Continuer" si demandé
6. ✅ Succès !
```

---

## 🔍 Vérifications rapides

**Le fichier google_credentials.json est bien placé?**
```
1. Ouvrez l'Explorateur
2. Allez à: C:\Users\[VotreNom]\OneDrive\Bureau\password-manager\
3. Cherchez le fichier: google_credentials.json
4. Doit être dans ce dossier EXACTEMENT
```

**Le fichier est valide?**
```
1. Double-cliquez google_credentials.json
2. Ouvre avec Notepad ou VS Code
3. Doit contenir:
   {
     "installed": {
       "client_id": "...",
       "client_secret": "...",
       ...
     }
   }
4. Si c'est du texte vide ou "YOUR_..." → Mauvais fichier
```

---

## ❌ Problèmes courants et solutions

### "Le fichier n'a pas pu être téléchargé"
✅ Utilisez un autre navigateur ou réessayez

### "Je ne vois pas le bouton Download"
✅ Cliquez directement sur le "Client ID" dans la liste

### "Ça demande encore mes identifiants"
✅ Redémarrez l'application et réessayez

### "Port 8888 déjà utilisé"
✅ Fermez tout et redémarrez l'ordinateur

---

## 📞 En cas de difficulté

1. Vérifiez d'abord: [TROUBLESHOOT_GOOGLE_OAUTH.md](TROUBLESHOOT_GOOGLE_OAUTH.md)
2. Consultez: [QUICK_SETUP.md](QUICK_SETUP.md)
3. Lisez: [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)

---

## ✅ Checklist finale

Avant de relancer:
- [ ] google_credentials.json créé dans Google Cloud
- [ ] Fichier JSON téléchargé
- [ ] Fichier renommé en: google_credentials.json
- [ ] Fichier placé dans: password-manager/
- [ ] http://localhost:8888/ ajouté dans Authorized redirect URIs
- [ ] Fichier NE contient pas: "YOUR_..."

---

**Ça devrait marcher maintenant! 🎉**

Lancez PasswordManager.exe et cliquez "Se connecter avec Google" 🚀
