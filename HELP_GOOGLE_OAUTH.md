# 🆘 AIDE - Erreur Google OAuth "invalid_client"

## Vous recevez cette erreur?
```
Accès bloqué : erreur d'autorisation

The OAuth client was not found.

Erreur 401 : invalid_client
```

---

## ✅ La Solution en 3 points

### 1️⃣ Le problème
**Manque du fichier `google_credentials.json`**

Ce fichier contient vos credentials Google Cloud. Sans lui, l'app ne peut pas communiquer avec Google.

### 2️⃣ Créer le fichier
Suivez ce guide: [SETUP_GOOGLE_OAUTH_SIMPLE.md](SETUP_GOOGLE_OAUTH_SIMPLE.md)

**Temps estimé: 15 minutes**

### 3️⃣ Placer le fichier
```
C:\Users\[VotreNom]\OneDrive\Bureau\password-manager\
└── google_credentials.json    ← PLACER ICI
```

---

## 🎯 Aide rapide selon votre situation

### "Je ne sais pas créer les credentials Google"
→ Lire: [SETUP_GOOGLE_OAUTH_SIMPLE.md](SETUP_GOOGLE_OAUTH_SIMPLE.md) (guide étape-par-étape)

### "J'ai créé les credentials mais je ne sais pas où les placer"
→ Lire: [SETUP_GOOGLE_OAUTH_SIMPLE.md](SETUP_GOOGLE_OAUTH_SIMPLE.md) (Étape 4)

### "J'ai tout fait mais ça ne marche toujours pas"
→ Lire: [TROUBLESHOOT_GOOGLE_OAUTH.md](TROUBLESHOOT_GOOGLE_OAUTH.md) (dépannage avancé)

### "Je veux utiliser juste le mode local sans Google"
→ C'est facile!
```
1. Lancez PasswordManager.exe
2. Entrez un mot de passe maître (au lieu de Google)
3. Cliquez "Se connecter"
4. Profitez!
```

### "Je veux contourner Google"
→ Vous pouvez utiliser **mode local** uniquement (pas Google OAuth)

---

## 📖 Guide complet

| Je veux... | Lire ceci |
|-----------|----------|
| Setup rapide Google | [SETUP_GOOGLE_OAUTH_SIMPLE.md](SETUP_GOOGLE_OAUTH_SIMPLE.md) |
| Details techniques | [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) |
| Dépanner l'erreur | [TROUBLESHOOT_GOOGLE_OAUTH.md](TROUBLESHOOT_GOOGLE_OAUTH.md) |
| Utiliser l'app | [GUIDE_UTILISATEUR_v2.1.md](GUIDE_UTILISATEUR_v2.1.md) |
| Tout savoir | [README_v2.1.md](README_v2.1.md) |

---

## ⚡ Résumé des étapes

```
1. Allez sur: https://console.cloud.google.com/
2. Créez un projet
3. Créez OAuth2 Credentials (type: Desktop)
4. Téléchargez le JSON
5. Renommez en: google_credentials.json
6. Placez dans: password-manager/
7. Vérifiez: http://localhost:8888/ est autorisé
8. Relancez l'app
9. ✅ Cliquez "Se connecter avec Google"
```

---

## 🚀 Prêt?

→ Allez à: [SETUP_GOOGLE_OAUTH_SIMPLE.md](SETUP_GOOGLE_OAUTH_SIMPLE.md)

---

**Besoin d'aide?** Tous les guides sont dans le dossier du Password Manager! 📚
