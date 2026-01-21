# Installation via .EXE Installateur

## Étapes pour créer l'installateur.exe

### Sur Windows (recommandé):

#### **Option 1: Double-clic (Plus simple)**

1. Double-clic sur `build_installer.bat` (je vais créer ce fichier)
2. Attends que ça se termine
3. L'installateur sera dans `dist/PasswordManagerInstaller.exe`

#### **Option 2: Ligne de commande**

```bash
python build_installer.py
```

Cela crée: `dist/PasswordManagerInstaller.exe`

### Sur Linux/macOS:

```bash
python3 build_installer.py
```

---

## Utilisation de l'installateur.exe

1. **Double-clic** sur `PasswordManagerInstaller.exe`
2. Fenêtre d'installation s'ouvre automatiquement
3. Clique sur **"Installer"**
4. L'application s'installe automatiquement sur le Bureau
5. C'est prêt ! Double-clic sur le raccourci Bureau pour utiliser l'app

---

## Contenu de l'installateur.exe

L'installateur fait automatiquement:
- ✅ Vérifie Python 3.7+
- ✅ Installe cryptography et pyinstaller
- ✅ Crée PasswordManager.exe
- ✅ Crée un dossier sur le Bureau
- ✅ Copie l'app dans ce dossier
- ✅ Crée un raccourci Bureau
- ✅ Copie vos données chiffrées (si existantes)

---

## Distribution

### Pour partager l'installateur:

1. Exécute `python build_installer.py`
2. Copie `dist/PasswordManagerInstaller.exe` n'importe où
3. Partage-le avec d'autres utilisateurs Windows
4. Ils n'ont besoin que de:
   - Windows 10/11
   - Python 3.7+ (avec "Add Python to PATH")

C'est tout ! 🎉

---

## Dépannage

**"Python n'est pas installé ou accessible"**
- Télécharge Python 3.7+ depuis: https://www.python.org/downloads/
- **Important**: Coche "Add Python to PATH" lors de l'installation
- Redémarre l'ordinateur
- Relance PasswordManagerInstaller.exe

**"Erreur lors de l'installation des dépendances"**
- Essaye d'exécuter l'installateur en tant qu'administrateur
- Clic droit → "Exécuter en tant qu'administrateur"

**"L'exécutable n'a pas pu être créé"**
- Assure-toi que tous les fichiers .py sont présents (gui.py, password_manager.py, etc.)
- Vérifiez les permissions du dossier
- Essaye de relancer l'installateur

---

## Structure après installation

```
Desktop/
├── PasswordManager.lnk  (raccourci pour lancer)
└── Gestionnaire de Mots de Passe/
    ├── PasswordManager.exe (application)
    ├── salt.bin (clé de chiffrement)
    └── passwords.enc (mots de passe chiffrés)
```

Vous pouvez ensuite:
- Supprimer PasswordManagerInstaller.exe (pas nécessaire après installation)
- Épingler PasswordManager à la barre des tâches
- Créer des raccourcis supplémentaires
