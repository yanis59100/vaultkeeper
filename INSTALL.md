# 📦 Guide d'Installation et Utilisation

## Vérification rapide

Tous les tests sont passés avec succès (10/10) ✅

```
Ran 10 tests in 0.472s
OK
```

## 🚀 Démarrage rapide

### Linux/macOS
```bash
cd /home/yanis/password-manager
./run.sh
```

### Windows
Double-cliquez sur `run.bat` ou ouvrez un terminal et exécutez:
```cmd
cd C:\chemin\vers\password-manager
python main.py
```

## 📋 Étapes d'utilisation

### 1️⃣ Premier lancement
- L'application demande un **mot de passe maître**
- Choisissez un mot de passe FORT (16+ caractères)
- Exemple : `Tr0p!cal$unset#2026@Sec`
- Validez en appuyant sur Entrée ou le bouton "Se connecter"

### 2️⃣ Ajouter des comptes
```
Cliquez sur "➕ Ajouter un compte"
- Site/Service: Gmail
- Utilisateur/Email: monmail@gmail.com
- Mot de passe: [votre mot de passe Gmail]
```

### 3️⃣ Générer un mot de passe sécurisé
```
Cliquez sur "🔄 Générer mot de passe"
- Longueur: 20 caractères (ajustable 8-32)
- Cochez: Majuscules ✓, Chiffres ✓, Caractères spéciaux ✓
- Cliquez "Générer"
- Cliquez "Copier" pour copier dans le presse-papiers
```

### 4️⃣ Retrouver vos comptes
```
Cliquez sur "🔍 Rechercher"
- Cherchez par site (Gmail, GitHub, etc.)
- Ou par nom d'utilisateur
```

### 5️⃣ Modifier un compte
```
Sélectionnez le compte dans la liste
Cliquez "✏️ Modifier"
Mettez à jour l'identifiant ou le mot de passe
```

### 6️⃣ Supprimer un compte
```
Sélectionnez le compte dans la liste
Cliquez "🗑️ Supprimer"
Confirmez la suppression
```

### 💡 Copier rapidement un mot de passe
```
Faites un clic droit sur n'importe quel compte
Le mot de passe est copié automatiquement
```

## 🔒 Sécurité - Points importants

### ✅ Ce qui est sécurisé
- Les mots de passe sont **chiffrés en AES-256** (militaire)
- Pas de connexion internet requise
- Les données restent toujours sur votre ordinateur
- Utilise PBKDF2 pour dériver la clé du mot de passe maître

### ⚠️ Points d'attention
1. **Mot de passe maître** - Doit être TRÈS fort et unique
   - Minimum 16 caractères recommandés
   - Mélange de majuscules, minuscules, chiffres, caractères spéciaux
   - Exemples :
     - ✅ `Tr0p!cal$unset#2026@Sec`
     - ✅ `MyP@ss2026-Vault!`
     - ❌ `password123` (trop faible)

2. **Sauvegardes** - Stockez vos données ailleurs
   - Fichiers critiques : `salt.bin` et `passwords.enc`
   - Sauvegardez-les régulièrement sur un disque externe
   - En cas de perte du mot de passe maître, il n'y a pas de récupération

3. **Partage** - Ne partagez JAMAIS
   - Votre mot de passe maître
   - Les fichiers `salt.bin` et `passwords.enc`
   - Vos mots de passe individuels

## 📊 Fichiers du projet

```
password-manager/
├── main.py                      # Point d'entrée principal
├── gui.py                       # Interface graphique (Tkinter)
├── password_manager.py          # Logique métier (gestion des comptes)
├── encryption.py                # Chiffrement/Déchiffrement (AES-256)
├── test_password_manager.py     # Tests automatisés (10 tests)
├── run.sh                       # Script de lancement (Linux/macOS)
├── run.bat                      # Script de lancement (Windows)
├── install_dependencies.py      # Installateur de dépendances
├── requirements.txt             # Liste des dépendances
├── README.md                    # Documentation complète
├── INSTALL.md                   # Ce fichier
│
├── salt.bin                     # Salt généré (créé au 1er lancement)
└── passwords.enc                # Données chiffrées (créé au 1er lancement)
```

## 🧪 Exécuter les tests

```bash
cd /home/yanis/password-manager
python3 test_password_manager.py
```

Les tests vérifient :
- ✓ Chiffrement/Déchiffrement
- ✓ Vérification du mot de passe maître
- ✓ Ajout/Suppression/Modification de comptes
- ✓ Génération de mots de passe
- ✓ Recherche de comptes
- ✓ Persistance des données

## 🐛 Dépannage

### L'application ne démarre pas
**Problème**: `Module not found: tkinter`
**Solution**: 
```bash
# Linux Debian/Ubuntu
sudo apt-get install python3-tk

# Linux Fedora
sudo dnf install python3-tkinter

# macOS (généralement inclus)
# Windows (généralement inclus avec Python)
```

### L'application ne démarre pas - Erreur cryptography
**Problème**: `ImportError: cannot import name 'PBKDF2HMAC'`
**Solution**: 
```bash
python3 install_dependencies.py
```

### Mot de passe maître oublié
❌ **Il n'existe pas de mécanisme de récupération**
- Le mot de passe maître est impossible à retrouver
- Les données chiffrées sont définitivement perdues

**Prévention**: Écrivez le mot de passe maître dans un endroit sûr (coffre-fort, gestionnaire de mots de passe)

### "Mot de passe maître incorrect"
- Vérifiez les majuscules/minuscules (sensible à la casse)
- Vérifiez que vous n'aviez pas d'espace avant/après
- Les fichiers `salt.bin` ou `passwords.enc` ont peut-être été modifiés

## 💾 Sauvegarde et Restauration

### Sauvegarder vos mots de passe
```bash
# Créer une sauvegarde
cp salt.bin salt.bin.backup
cp passwords.enc passwords.enc.backup

# Stocker sur un disque externe ou cloud sécurisé
```

### Restaurer vos mots de passe
```bash
# Si vous avez une sauvegarde
cp salt.bin.backup salt.bin
cp passwords.enc.backup passwords.enc
```

## 🎓 Fonctionnalités avancées

### Génération de mots de passe personnalisés
- Longueur : 8 à 32 caractères
- Options :
  - Majuscules (A-Z)
  - Minuscules (a-z) - toujours activé
  - Chiffres (0-9)
  - Caractères spéciaux (!@#$%^&*...)

### Recherche intelligente
Recherchez par :
- Nom du site exact : `Gmail`
- Début du nom : `Gm`
- Nom d'utilisateur : `monmail@`

### Multicomptes par site
Vous pouvez avoir plusieurs comptes pour le même site :
```
Gmail
  ├── personnel@gmail.com
  ├── professionnel@gmail.com
  └── secondaire@gmail.com
```

## 📝 Contrats de confidentialité

⚠️ **Cette application est locale et hors ligne**
- Aucune donnée n'est envoyée en ligne
- Aucun serveur n'est impliqué
- Vos mots de passe restent 100% sous votre contrôle

## 🚨 Limitations et Notes

- Pas de synchronisation multi-appareils
- Pas d'import/export de données
- Pas de notifications d'alerte de mots de passe faibles
- Pas de suivi d'historique des modifications

## 📞 Support

Pour des problèmes supplémentaires :
1. Vérifiez les logs de l'application
2. Testez avec `python3 test_password_manager.py`
3. Consultez le README.md pour plus de détails techniques

---

**Vous êtes maintenant prêt à utiliser votre gestionnaire de mots de passe sécurisé ! 🔐**
