#!/usr/bin/env python3
"""
Script pour créer un exécutable Windows (.exe) avec PyInstaller
Utilisation: python build_exe.py
"""

import os
import sys
import subprocess
import shutil


def build_executable():
    """Crée l'exécutable Windows"""
    
    print("=" * 70)
    print("🔨 Création de l'exécutable Windows (.exe)")
    print("=" * 70)
    print()
    
    # Vérifier PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller n'est pas installé")
        print("Installation de PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Créer le répertoire de sortie
    dist_dir = os.path.join(os.path.dirname(__file__), "dist")
    build_dir = os.path.join(os.path.dirname(__file__), "build")
    
    # Nettoyer les répertoires existants
    print("Nettoyage des répertoires existants...")
    for d in [dist_dir, build_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    # Options PyInstaller
    pyinstaller_args = [
        "main.py",
        "--name=PasswordManager",
        "--onefile",
        "--windowed",
        "--icon=password-manager.ico" if os.path.exists("password-manager.ico") else "",
        "--collect-all=cryptography",
        "--hidden-import=cryptography.hazmat.backends.openssl",
        "--hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2",
        "--add-data=.:.",
        "--specpath=build",
        "--distpath=dist",
        "--buildpath=build",
    ]
    
    # Filtrer les arguments vides
    pyinstaller_args = [arg for arg in pyinstaller_args if arg]
    
    print("\nLancement de PyInstaller...")
    print(f"Commande: pyinstaller {' '.join(pyinstaller_args)}")
    print()
    
    try:
        subprocess.check_call(["pyinstaller"] + pyinstaller_args)
    except FileNotFoundError:
        print("❌ PyInstaller n'a pas pu être lancé")
        print("Essayez: pip install pyinstaller")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création de l'exécutable: {e}")
        return False
    
    # Vérifier le résultat
    exe_path = os.path.join(dist_dir, "PasswordManager.exe")
    if os.path.exists(exe_path):
        exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print("\n" + "=" * 70)
        print("✅ Exécutable créé avec succès!")
        print("=" * 70)
        print(f"📍 Localisation: {exe_path}")
        print(f"💾 Taille: {exe_size:.1f} MB")
        print()
        print("Pour lancer l'application:")
        print(f"  Double-cliquez sur: PasswordManager.exe")
        print(f"  Ou lancez depuis le terminal: .\\dist\\PasswordManager.exe")
        print()
        return True
    else:
        print("❌ L'exécutable n'a pas pu être créé")
        return False


def create_installer():
    """Crée un installateur Windows (optionnel)"""
    print("\n" + "=" * 70)
    print("💿 Création d'un installateur Windows")
    print("=" * 70)
    print()
    print("Pour créer un installateur professionnel, utilisez:")
    print("  • NSIS: https://nsis.sourceforge.io/")
    print("  • Inno Setup: https://jrsoftware.org/isinfo.php")
    print()


if __name__ == "__main__":
    try:
        success = build_executable()
        if success:
            create_installer()
            print("✨ Fait! L'application est prête à être utilisée sur Windows.")
        else:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
