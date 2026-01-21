"""Module d'installation de dépendances"""

import subprocess
import sys

def install_dependencies():
    """Installe les dépendances requises"""
    print("Installation des dépendances...")
    
    try:
        import cryptography
        print("✓ cryptography est déjà installé")
    except ImportError:
        print("Installation de cryptography...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    
    print("\n✓ Toutes les dépendances sont installées!")


if __name__ == "__main__":
    install_dependencies()
