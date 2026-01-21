#!/usr/bin/env python3
"""
Script pour créer l'installateur.exe
Exécuter: python build_installer.py
"""

import subprocess
import sys

print("=" * 60)
print("Création de l'installateur Windows (.exe)")
print("=" * 60)
print()

# Vérifier PyInstaller
print("[1/3] Verification de PyInstaller...")
try:
    result = subprocess.run(["pip", "show", "pyinstaller"], capture_output=True)
    if result.returncode != 0:
        print("Installation de PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
except:
    print("Erreur: Impossible d'installer PyInstaller")
    sys.exit(1)

# Créer l'installateur.exe
print("[2/3] Creation de l'installateur...")
cmd = [
    "pyinstaller",
    "installer.py",
    "--name=PasswordManagerInstaller",
    "--onefile",
    "--windowed",
    "--icon=NONE"
]

try:
    subprocess.run(cmd, check=True)
    print("[3/3] Success ! L'installateur est cree: dist/PasswordManagerInstaller.exe")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de la creation: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("Installation de l'installateur .exe reussie!")
print("=" * 60)
print()
print("Fichier: dist/PasswordManagerInstaller.exe")
print()
print("Pour utiliser l'installateur:")
print("  1. Copie PasswordManagerInstaller.exe sur le Bureau")
print("  2. Double-clic sur PasswordManagerInstaller.exe")
print("  3. Clique sur 'Installer'")
print()
