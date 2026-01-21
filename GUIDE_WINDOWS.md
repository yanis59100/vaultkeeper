# 🪟 Guide Complet Windows - Gestionnaire de Mots de Passe

## 🚀 Installation rapide (5 minutes)

### Méthode recommandée: Installation automatique

1. **Téléchargez ou clonez le projet**
   ```
   À partir de GitHub ou extraire le ZIP
   ```

2. **Double-cliquez sur `install.bat`**
   - L'installation s'effectue automatiquement
   - Python sera détecté/installé
   - Les dépendances seront téléchargées
   - L'exécutable sera créé
   - Un raccourci sera ajouté au bureau

3. **Lancez depuis le raccourci du bureau** 🎉

---

## 📋 Prérequis Windows

### Configuration minimale
- Windows 7 ou ultérieur
- 200 MB d'espace disque
- Connexion internet (première installation)

### Recommandé
- Windows 10 ou 11
- 500 MB d'espace disque
- Aucune connexion internet requise après installation

---

## 💾 Trois façons de lancer l'application

### Option 1: Double-cliquez sur `PasswordManager.exe` (Meilleur)
- Emplacement: `dist\PasswordManager.exe`
- Avantages: Rapide, aucune dépendance requise
- Demarrage: < 2 secondes

### Option 2: Double-cliquez sur `run.bat`
- Emplacement: Racine du projet
- Avantages: Automatique, gère les dépendances
- Demarrage: 3-5 secondes

### Option 3: PowerShell/CMD
```powershell
cd C:\chemin\vers\password-manager
python main.py
```
- Avantages: Contrôle total, affichage des logs
- Demarrage: 2-3 secondes

---

## 🎨 Première utilisation

### 1. Lancer l'application
Double-cliquez sur l'icône ou raccourci

### 2. Écran d'authentification
- Entrez un **mot de passe maître** fort (16+ caractères)
- Exemple: `Tr0p!cal$unset#2026@Sec`
- Cliquez "Se connecter" ou appuyez sur Entrée

### 3. Écran principal
- Liste vide au premier lancement
- Prêt à ajouter vos comptes

### 4. Ajouter votre premier compte
1. Cliquez sur **"➕ Ajouter un compte"**
2. Remplissez:
   - Site/Service: `Gmail`
   - Utilisateur/Email: `votre@email.com`
   - Mot de passe: `votre_mot_de_passe`
3. Cliquez **"Ajouter"**

### 5. Vérifier le compte
- Le compte apparaît dans la liste
- Le mot de passe est affiché comme `●●●●●●●●●●`

---

## 📖 Guide complet des fonctionnalités

### ➕ Ajouter un compte

```
Bouton: "➕ Ajouter un compte"
Remplir les champs:
  Site: Gmail / GitHub / Facebook / etc.
  Utilisateur: nom d'utilisateur ou email
  Mot de passe: [votre mot de passe]
Cliquer: "Ajouter"
```

**Exemples:**
- Site: `Gmail`, Utilisateur: `john@gmail.com`
- Site: `GitHub`, Utilisateur: `johndoe`
- Site: `Amazon`, Utilisateur: `john.doe@email.com`

---

### 🔄 Générer un mot de passe sécurisé

```
Bouton: "🔄 Générer mot de passe"
Réglez:
  Longueur: 16-20 caractères (glissez le curseur)
  Options:
    ☑ Majuscules (A-Z)
    ☑ Chiffres (0-9)
    ☑ Caractères spéciaux (!@#$%)
Cliquez: "Générer"
Résultat: kP8@mX9$nL2#qR5!vW3j
Cliquez: "Copier"
Collez: Ctrl+V dans le formulaire
```

**Recommandations:**
- Longueur: 18-20 caractères
- Options: Tout cocher pour maximum de sécurité
- Unique par service

---

### 🔍 Rechercher un compte

```
Bouton: "🔍 Rechercher"
Entrez: Gmail (ou partie du nom)
Résultats: Tous les comptes Gmail
```

**Exemples de recherche:**
- `Gmail` → trouve tous les comptes Gmail
- `john` → trouve tous les comptes avec "john"
- `@` → trouve tous les comptes email

---

### ✏️ Modifier un compte

```
1. Sélectionnez un compte dans la liste
2. Cliquez: "✏️ Modifier"
3. Mettez à jour les données
4. Cliquez: "Modifier"
```

**Cas d'usage:**
- Modifier un mot de passe après le changer sur le site
- Ajouter/modifier le nom d'utilisateur
- Corriger une erreur d'enregistrement

---

### 🗑️ Supprimer un compte

```
1. Sélectionnez un compte dans la liste
2. Cliquez: "🗑️ Supprimer"
3. Confirmez: "Oui"
```

⚠️ **Attention:** Suppression définitive, pas d'annulation possible

---

### 📋 Copier facilement (Clic droit)

```
1. Faites un clic droit sur un compte
2. Le mot de passe est copié automatiquement
3. Collez avec: Ctrl+V
```

**C'est le plus rapide!**

---

## 🔐 Sécurité Windows

### Mot de passe maître
**Très important!** Choisissez un mot de passe:
- ✅ Au minimum 16 caractères
- ✅ Mélange de majuscules, minuscules, chiffres, spéciaux
- ✅ Unique et mémorable
- ✅ Pas de mots du dictionnaire
- ✅ Écrit dans un endroit sûr

**Exemples forts:**
- `Tr0p!cal$unset#2026@Secure`
- `MyVault*2026&SAFE!Password`
- `SecureP@ssw0rd#Manager2026`

**Exemples faibles:**
- ❌ `password123`
- ❌ `Azerty`
- ❌ `12345678`

---

### Où sont stockées les données?

Par défaut: **Même dossier que l'application**

Fichiers importants:
- `salt.bin` - Salt de chiffrement (16 bytes)
- `passwords.enc` - Données chiffrées

**Emplacement exact (si lancé via `run.bat`):**
```
C:\Users\VotreNom\AppData\Local\password-manager\
```

### 💾 Sauvegarder vos données

**IMPORTANT:** Faites des sauvegardes régulières!

```
1. Localisez salt.bin et passwords.enc
2. Copier-les sur un disque externe
3. Ou sur OneDrive/Google Drive chiffré
```

**Automatiser les sauvegardes:**

Créez une tâche Windows Scheduler:
1. Appuyez sur `Windows + R`
2. Tapez: `taskschd.msc`
3. Action → Créer une tâche planifiée
4. Planifiez une copie quotidienne

---

### 🛡️ Protection Windows Defender

Windows Defender peut avertir sur l'exécutable auto-créé

**Pas de danger:** C'est un faux positif

**Si vous recevez un avertissement:**
1. Cliquez **"Plus d'infos"**
2. Cliquez **"Exécuter quand même"**

**Ou ajouter une exception:**
1. Ouvrir Windows Defender
2. Paramètres → Accès contrôlé des dossiers
3. Ajouter le dossier à la liste blanche

---

## ⚙️ Configuration avancée Windows

### Changer le dossier de données

Modifiez `config.py`:
```python
# Avant
DATA_FILE = "passwords.enc"
SALT_FILE = "salt.bin"

# Après (exemple)
DATA_FILE = "C:\\Users\\VotreNom\\Secure\\passwords.enc"
SALT_FILE = "C:\\Users\\VotreNom\\Secure\\salt.bin"
```

### Lancer l'application au démarrage

1. Appuyez sur `Windows + R`
2. Tapez: `shell:startup`
3. Collez un raccourci vers `PasswordManager.exe`

### Créer un raccourci personnalisé

1. Clic droit sur `PasswordManager.exe`
2. Créer un raccourci
3. Clic droit sur le raccourci → Propriétés
4. Avancé → Exécuter en tant qu'administrateur

---

## 🔧 Dépannage Windows

### L'application ne démarre pas

**Vérification 1: Python installé?**
```powershell
python --version
```

**Vérification 2: Cryptography installé?**
```powershell
python -c "import cryptography; print('OK')"
```

**Vérification 3: Tkinter installé?**
```powershell
python -c "import tkinter; print('OK')"
```

---

### "PasswordManager.exe a cessé de fonctionner"

**Solution 1:** Téléchargez le Runtime Microsoft C++
- Lien: https://support.microsoft.com/en-us/help/2977003
- Installez-le et redémarrez

**Solution 2:** Utilisez `run.bat` à la place
- Double-cliquez sur `run.bat`
- Plus stable que l'exécutable

---

### "Accès refusé" (permissions)

**Solution:** Lancez avec droits administrateur
1. Clic droit sur l'application
2. Sélectionnez "Exécuter en tant qu'administrateur"

Ou créez un raccourci avec admin:
1. Clic droit → Propriétés → Avancé
2. Cochez "Exécuter en tant qu'administrateur"

---

### "Mot de passe maître oublié"

❌ **Malheureusement, pas de solution**

Les données sont chiffrées et irrécupérables sans le mot de passe maître

**Prévention:**
- Écrivez-le dans un gestionnaire de mots de passe
- Ou sur un papier dans un endroit sûr
- Faites des tests réguliers

---

### Les fichiers salt.bin ou passwords.enc sont disparus

**Solution:**
1. Restaurez à partir d'une sauvegarde
2. Ou recommencez avec un nouveau mot de passe maître
3. Vos anciens comptes seront perdus

**Prévention:** Sauvegardez régulièrement!

---

## 📞 Support Windows

### Vérifier la version de Windows

Appuyez sur `Windows + R` et tapez: `winver`

### Logs de l'application

Lancez via PowerShell pour voir les logs:
```powershell
cd C:\chemin\vers\password-manager
python main.py 2>&1 | Tee-Object -FilePath app.log
```

### Contacter le support

Consultez la documentation:
- `README.md` - Vue d'ensemble
- `INSTALL.md` - Guide d'installation
- `MODULE_DOCS.md` - Détails techniques

---

## ✨ Astuces Windows

### Raccourci clavier personnalisé

1. Clic droit sur le raccourci
2. Propriétés → Raccourci
3. Champ "Touche de raccourci"
4. Appuyez sur la combinaison (ex: Ctrl+Alt+P)
5. Appliquer

### Épingler à la barre des tâches

1. Clic droit sur `PasswordManager.exe`
2. "Épingler à la barre des tâches"
3. Accès rapide!

### Créer un sous-dossier de sécurité

```
C:\Users\VotreNom\Secure\PasswordManager\
├── PasswordManager.exe
├── salt.bin
└── passwords.enc
```

Avec permissions réduites (lecture/écriture vous seul)

---

## 🎉 Installation réussie!

Vous êtes maintenant prêt à utiliser votre gestionnaire de mots de passe sur Windows!

**Points importants:**
✅ Mot de passe maître fort
✅ Sauvegardes régulières
✅ Ne partagez jamais votre mot de passe maître
✅ Comptes à jour régulièrement

**Bon usage! 🔐**
