# Configuration Google OAuth2

## Vue d'ensemble

L'application supporte maintenant l'authentification via Google OAuth2. Cela permet aux utilisateurs de se connecter avec leur compte Google et d'accéder à leur coffre-fort de mots de passe personnel.

## Configuration requise

### 1. Créer un projet Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet
3. Accédez à **APIs & Services** > **Credentials**
4. Cliquez sur **Create Credentials** > **OAuth Client ID**
5. Sélectionnez **Desktop application** (Application de bureau)
6. Téléchargez le fichier JSON des credentials

### 2. Configuration du fichier credentials

1. Renommez le fichier téléchargé en `google_credentials.json`
2. Placez-le dans le même dossier que `PasswordManager.exe` ou dans le dossier du projet
3. Le contenu du fichier doit ressembler à :

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost:8888/"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    ...
  }
}
```

### 3. Configurer les URI de redirection autorisées

Dans Google Cloud Console :
1. Allez à **APIs & Services** > **Credentials**
2. Cliquez sur votre OAuth Client ID
3. Ajoutez `http://localhost:8888/` à la liste des **Authorized redirect URIs**
4. Assurez-vous que **Authorized JavaScript origins** inclut `http://localhost`

## Utilisation

### Authentification locale (par défaut)

1. Lancez l'application
2. Entrez votre mot de passe maître
3. Vous avez accès à votre coffre-fort

### Authentification Google

1. Lancez l'application
2. Cliquez sur "🔗 Se connecter avec Google"
3. Un navigateur s'ouvrira automatiquement pour la connexion Google
4. Complétez l'authentification
5. Une fois authentifié, l'application récupère votre adresse email Google
6. Votre coffre-fort personnel est créé avec votre email comme identifiant

## Architecture multi-utilisateur

Chaque utilisateur a son propre coffre-fort chiffré :

- **Mode local** : Données stockées dans `.users/local/`
- **Mode Google** : Données stockées dans `.users/{email_sanitized}/`

Les données de chaque utilisateur sont complètement isolées et chiffrées avec leur propre clé dérivée.

## Fichiers de données

```
.users/
├── local/                    # Utilisateur en mode local
│   ├── .salt.bin            # Salt pour dérivation de clé
│   ├── .passwords.enc       # Données chiffrées
│   └── .hash.bin            # Hash d'intégrité
└── email_at_gmail.com/      # Utilisateur Google (email sanitized)
    ├── .salt.bin
    ├── .passwords.enc
    └── .hash.bin
```

## Sécurité

### Chiffrement

- **Algorithme** : AES-256 Fernet
- **Dérivation de clé** : PBKDF2-SHA256 (480,000 itérations)
- **Salt** : 32 octets aléatoires par utilisateur
- **Intégrité** : Hash HMAC-SHA256

### Token Google

- Les tokens Google ne sont pas sauvegardés
- Seules les informations de profil (email, nom, image) sont utilisées
- La clé de chiffrement est dérivée de l'email Google

## Dépannage

### "Authentification Google échouée"

1. Vérifiez que `google_credentials.json` est présent
2. Vérifiez les permissions du fichier
3. Assurez-vous que le port 8888 n'est pas en utilisation

### "Une fenêtre de navigateur ne s'ouvre pas"

1. Démarrez manuellement votre navigateur
2. Allez à `http://localhost:8888`
3. Le navigateur peut ne pas s'ouvrir automatiquement dans certains environnements

### "Erreur de redirection"

1. Vérifiez l'URI de redirection dans Google Cloud Console
2. Assurez-vous que `http://localhost:8888/` est autorisé

## Notes de version

- **v2.0** : Ajout de l'authentification Google OAuth2
- Chaque utilisateur a son propre coffre-fort isolé
- Support complet du chiffrement AES-256 par utilisateur

## Support

Pour les problèmes :
1. Vérifiez le fichier `google_credentials.json`
2. Consultez les logs de PyInstaller si vous compilez vous-même
3. Testez d'abord en mode développement (python main.py)
