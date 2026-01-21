# 🪟 Installation Windows - Gestionnaire de Mots de Passe

## 📌 Trois méthodes pour installer

### Méthode 1️⃣ : Exécutable Standalone (Recommandé) ⭐

**Avantages:** Pas de dépendances, facile d'installer
**Inconvénients:** Fichier plus gros (~150 MB)

#### Étape 1: Créer l'exécutable

```bash
# Depuis le dossier du projet
python build_exe.py
```

Ou manuellement:
```bash
pip install pyinstaller
pyinstaller main.py --name=PasswordManager --onefile --windowed --collect-all=cryptography
```

#### Étape 2: Lancer l'application

Allez dans le dossier `dist/` et **double-cliquez** sur `PasswordManager.exe`

✅ **C'est tout!** L'application démarre directement.

---

### Méthode 2️⃣ : Script Batch (Simple)

**Avantages:** Pas besoin de compilation, léger
**Inconvénients:** Nécessite Python installé

#### Étape 1: Installer Python

1. Téléchargez Python 3.7+ depuis https://www.python.org/downloads/
2. **Important:** Lors de l'installation, cochez `[x] Add Python to PATH`
3. Terminez l'installation

#### Étape 2: Installer les dépendances

Double-cliquez sur `install_dependencies.py`

Ou ouvrez PowerShell dans le dossier et tapez:
```powershell
python install_dependencies.py
```

#### Étape 3: Lancer l'application

Double-cliquez sur **`run.bat`**

✅ L'application démarre!

---

### Méthode 3️⃣ : Ligne de Commande

#### Étape 1: Installer Python

Même procédure que Méthode 2

#### Étape 2: Ouvrir PowerShell

1. Appuyez sur `Windows + X`
2. Sélectionnez **"PowerShell (Admin)"** ou **"Terminal"**
3. Naviguez vers le dossier:
```powershell
cd C:\chemin\vers\password-manager
```

#### Étape 3: Installer les dépendances
```powershell
python -m pip install cryptography
```

#### Étape 4: Lancer l'application
```powershell
python main.py
```

---

## ✅ Vérification de l'installation

### Python est-il installé?
```powershell
python --version
```

Vous devriez voir: `Python 3.x.x`

### Cryptography est-il installé?
```powershell
python -c "import cryptography; print('OK')"
```

Vous devriez voir: `OK`

---

## 🚨 Dépannage Windows

### "Python n'est pas reconnu"
```
'python' n'est pas reconnu comme une commande...
```

**Solution:**
1. Réinstallez Python
2. **Cochez obligatoirement:** `[x] Add Python to PATH`
3. Redémarrez l'ordinateur
4. Retestez

### "ModuleNotFoundError: No module named 'tkinter'"
```
ModuleNotFoundError: No module named 'tkinter'
```

**Solution:**
1. Réinstallez Python avec l'option **"tcl/tk and IDLE"**
2. Ou exécutez: `python -m pip install tk`

### "ModuleNotFoundError: No module named 'cryptography'"
```
ModuleNotFoundError: No module named 'cryptography'
```

**Solution:**
```powershell
python -m pip install cryptography
```

### L'exécutable ne démarre pas
**Solution:**
1. Téléchargez la dernière version du Runtime Microsoft C++
2. Installez-la: https://support.microsoft.com/en-us/help/2977003
3. Relancez l'exécutable

### "Windows Defender bloque l'exécutable"

C'est normal pour un exécutable créé avec PyInstaller

**Solution:**
1. Cliquez sur **"Plus d'infos"**
2. Cliquez sur **"Exécuter quand même"**

Ou ajouter une exception:
1. Ouvrez **Windows Defender**
2. Allez dans **Paramètres > Accès contrôlé des dossiers**
3. Ajoutez le fichier .exe à la liste blanche

---

## 📦 Distribution

### Créer un installateur NSIS

Pour une distribution professionnelle:

1. Créez le .exe avec `build_exe.py`
2. Téléchargez NSIS: https://nsis.sourceforge.io/
3. Créez un fichier `.nsi`:

```nsis
; Instalateur NSIS simplifié
!include "MUI2.nsh"

Name "Gestionnaire de Mots de Passe"
OutFile "PasswordManager-Setup.exe"
InstallDir "$PROGRAMFILES\PasswordManager"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "French"

Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\PasswordManager.exe"
  
  CreateDirectory "$SMPROGRAMS\PasswordManager"
  CreateShortCut "$SMPROGRAMS\PasswordManager\PasswordManager.lnk" "$INSTDIR\PasswordManager.exe"
  CreateShortCut "$DESKTOP\PasswordManager.lnk" "$INSTDIR\PasswordManager.exe"
SectionEnd
```

4. Lancez NSIS et compilez

---

## 🎯 Guide de démarrage rapide Windows

### Option A: Installation rapide (< 1 minute)

```
1. Double-cliquez: run.bat
2. Attendez l'installation des dépendances
3. L'application démarre automatiquement
```

### Option B: Exécutable (Recommandé)

```
1. Ouvrez PowerShell
2. python build_exe.py
3. Allez dans dist/
4. Double-cliquez: PasswordManager.exe
```

---

## 🔒 Sécurité Windows

### Mot de passe maître
- Minimum 16 caractères recommandés
- Exemple: `Tr0p!cal$unset#2026@Sec`

### Sauvegarde des données
Windows stocke les fichiers dans:
```
C:\Users\VotreNom\password-manager\
```

Fichiers importants:
- `salt.bin` - Salt de chiffrement
- `passwords.enc` - Données chiffrées

**Sauvegardez-les régulièrement!**

### Antivirus
Si votre antivirus vous avertit:
1. C'est normal pour un exécutable Python
2. Ajoutez une exception dans l'antivirus
3. Ou lancez avec `run.bat`

---

## 📱 Utilisation sur Windows

### Ajouter un compte

```
1. Lancez l'application
2. Entrez le mot de passe maître
3. Cliquez "➕ Ajouter un compte"
4. Remplissez: Site, Utilisateur, Mot de passe
5. Validez
```

### Générer un mot de passe

```
1. Cliquez "🔄 Générer mot de passe"
2. Choisissez la longueur
3. Cliquez "Générer"
4. Cliquez "Copier"
5. Collez dans votre formulaire
```

### Récupérer un mot de passe

```
Clic droit sur un compte
Mot de passe copié automatiquement ✓
```

---

## 🆘 Support Windows

### Erreurs courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| `'python' is not recognized` | Python pas dans PATH | Réinstallez avec "Add to PATH" |
| `No module named 'cryptography'` | Cryptography absent | `pip install cryptography` |
| `No module named 'tkinter'` | Tkinter absent | Réinstallez Python avec Tcl/Tk |
| `Windows Defender blocks it` | Exécutable inconnu | Cliquez "Run anyway" |

### Test de l'installation

```powershell
# Vérifier Python
python --version

# Vérifier Tkinter
python -c "import tkinter; print('OK')"

# Vérifier Cryptography
python -c "import cryptography; print('OK')"

# Tout est OK si vous voyez "OK" 3 fois
```

---

## 🎉 Installation réussie!

Vous êtes maintenant prêt à utiliser votre gestionnaire de mots de passe sécurisé sur Windows! 🔐

**Conseils:**
- Créez un raccourci sur le bureau
- Épinglez à la barre des tâches
- Sauvegardez régulièrement vos données

Bon usage! 🚀
