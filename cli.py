#!/usr/bin/env python3
"""Interface CLI du gestionnaire de mots de passe (sans Tkinter)"""

import sys
import os
from password_manager import PasswordManager
from getpass import getpass


class PasswordManagerCLI:
    """Interface CLI simple"""
    
    def __init__(self):
        self.manager = None
        self.authenticated = False
    
    def clear_screen(self):
        """Efface l'écran"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title):
        """Affiche un en-tête"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")
    
    def authenticate(self):
        """Authentifie l'utilisateur"""
        self.print_header("🔐 AUTHENTIFICATION")
        
        master_password = getpass("Entrez votre mot de passe maître: ")
        
        if not master_password:
            print("❌ Mot de passe vide!")
            return False
        
        try:
            self.manager = PasswordManager(master_password)
            
            if not self.manager.encryption.verify_master_password():
                print("❌ Mot de passe maître incorrect!")
                self.manager = None
                return False
            
            print("✅ Authentification réussie!\n")
            self.authenticated = True
            return True
        except ValueError as e:
            print(f"❌ Erreur: {e}\n")
            return False
    
    def show_menu(self):
        """Affiche le menu principal"""
        self.print_header("MENU PRINCIPAL")
        print("1. ➕ Ajouter un compte")
        print("2. 📋 Afficher tous les comptes")
        print("3. 🔍 Rechercher un compte")
        print("4. ✏️  Modifier un compte")
        print("5. 🗑️  Supprimer un compte")
        print("6. 🔄 Générer un mot de passe")
        print("7. 🔐 Changer le mot de passe maître")
        print("8. 🚪 Déconnexion")
        print("0. ❌ Quitter")
        print("\n" + "-" * 60)
    
    def add_account(self):
        """Ajoute un compte"""
        self.print_header("AJOUTER UN COMPTE")
        
        site = input("Site/Service: ").strip()
        if not site:
            print("❌ Le site ne peut pas être vide!")
            return
        
        username = input("Utilisateur/Email: ").strip()
        if not username:
            print("❌ L'utilisateur ne peut pas être vide!")
            return
        
        password = getpass("Mot de passe: ")
        if not password:
            print("❌ Le mot de passe ne peut pas être vide!")
            return
        
        self.manager.add_account(site, username, password)
        print(f"✅ Compte '{username}' pour {site} ajouté avec succès!\n")
    
    def display_all_accounts(self):
        """Affiche tous les comptes"""
        accounts = self.manager.get_accounts()
        
        if not accounts:
            self.print_header("COMPTES")
            print("Aucun compte enregistré\n")
            return
        
        self.print_header("TOUS LES COMPTES")
        
        for site in sorted(accounts.keys()):
            print(f"\n📍 {site}")
            for i, account in enumerate(accounts[site], 1):
                pwd_masked = "●" * len(account["password"])
                print(f"   {i}. {account['username']} | {pwd_masked}")
        
        print("\n" + "-" * 60 + "\n")
    
    def search_accounts(self):
        """Recherche des comptes"""
        self.print_header("RECHERCHER")
        
        query = input("Terme de recherche: ").strip()
        if not query:
            print("❌ Requête vide!")
            return
        
        results = self.manager.search_accounts(query)
        
        if not results:
            print(f"❌ Aucun compte trouvé pour '{query}'\n")
            return
        
        print(f"✅ Résultats pour '{query}':\n")
        
        for site in sorted(results.keys()):
            print(f"📍 {site}")
            for i, account in enumerate(results[site], 1):
                pwd_masked = "●" * len(account["password"])
                print(f"   {i}. {account['username']} | {pwd_masked}")
        
        print("\n" + "-" * 60)
        
        # Option pour copier
        choice = input("\nVoulez-vous voir le mot de passe ? (y/n): ").lower()
        if choice == 'y':
            self._show_password(results)
    
    def _show_password(self, results):
        """Affiche un mot de passe sélectionné"""
        site = input("\nSite: ").strip()
        username = input("Utilisateur: ").strip()
        
        if site in results:
            for account in results[site]:
                if account["username"] == username:
                    print(f"\n🔓 Mot de passe: {account['password']}\n")
                    return
        
        print("❌ Compte non trouvé!\n")
    
    def modify_account(self):
        """Modifie un compte"""
        self.display_all_accounts()
        
        self.print_header("MODIFIER UN COMPTE")
        
        site = input("Site: ").strip()
        old_username = input("Ancien utilisateur: ").strip()
        
        new_username = input("Nouveau utilisateur: ").strip()
        if not new_username:
            new_username = old_username
        
        new_password = getpass("Nouveau mot de passe: ")
        if not new_password:
            print("❌ Le mot de passe ne peut pas être vide!")
            return
        
        if self.manager.update_account(site, old_username, new_username, new_password):
            print(f"✅ Compte modifié avec succès!\n")
        else:
            print(f"❌ Compte non trouvé!\n")
    
    def delete_account(self):
        """Supprime un compte"""
        self.display_all_accounts()
        
        self.print_header("SUPPRIMER UN COMPTE")
        
        site = input("Site: ").strip()
        username = input("Utilisateur: ").strip()
        
        confirm = input(f"Êtes-vous sûr de vouloir supprimer '{username}' de {site}? (oui/non): ").lower()
        
        if confirm in ['oui', 'o', 'yes', 'y']:
            if self.manager.delete_account(site, username):
                print(f"✅ Compte supprimé!\n")
            else:
                print(f"❌ Compte non trouvé!\n")
        else:
            print("❌ Suppression annulée!\n")
    
    def generate_password(self):
        """Génère un mot de passe"""
        self.print_header("GÉNÉRER UN MOT DE PASSE")
        
        try:
            length = int(input("Longueur (8-32) [16]: ") or "16")
            if length < 8 or length > 32:
                print("❌ Longueur invalide (8-32)!")
                return
        except ValueError:
            length = 16
        
        uppercase = input("Inclure majuscules? (o/n) [o]: ").lower() != 'n'
        digits = input("Inclure chiffres? (o/n) [o]: ").lower() != 'n'
        special = input("Inclure caractères spéciaux? (o/n) [o]: ").lower() != 'n'
        
        password = self.manager.generate_password(
            length=length,
            use_uppercase=uppercase,
            use_digits=digits,
            use_special=special
        )
        
        print(f"\n🔐 Mot de passe généré:\n   {password}\n")
        
        copy_choice = input("Copier dans le presse-papiers? (o/n): ").lower()
        if copy_choice in ['o', 'oui', 'yes', 'y']:
            try:
                import pyperclip
                pyperclip.copy(password)
                print("✅ Copié!\n")
            except:
                print("⚠️  Impossible de copier (pyperclip non installé)\n")
    
    def run(self):
        """Boucle principale"""
        self.clear_screen()
        
        print("\n╔══════════════════════════════════════════════════════════╗")
        print("║  🔐 Gestionnaire de Mots de Passe Sécurisé              ║")
        print("║  Version CLI (Interface Ligne de Commande)              ║")
        print("╚══════════════════════════════════════════════════════════╝\n")
        
        # Authentification
        while not self.authenticated:
            if not self.authenticate():
                retry = input("Réessayer? (o/n): ").lower()
                if retry not in ['o', 'oui', 'yes', 'y']:
                    print("❌ Quitter...\n")
                    return
                self.clear_screen()
        
        # Boucle principale
        while True:
            self.show_menu()
            choice = input("Sélectionnez une option: ").strip()
            
            if choice == '1':
                self.add_account()
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == '2':
                self.display_all_accounts()
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == '3':
                self.search_accounts()
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == '4':
                self.modify_account()
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == '5':
                self.delete_account()
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == '6':
                self.generate_password()
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == '7':
                print("\n⚠️  Fonctionnalité non implémentée\n")
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == '8':
                print("🚪 Déconnexion...\n")
                self.manager = None
                self.authenticated = False
                # Redémarrer l'authentification
                while not self.authenticated:
                    if not self.authenticate():
                        retry = input("Réessayer? (o/n): ").lower()
                        if retry not in ['o', 'oui', 'yes', 'y']:
                            print("❌ Quitter...\n")
                            return
                        self.clear_screen()
            
            elif choice == '0':
                print("\n👋 Au revoir!\n")
                return
            
            else:
                print("❌ Option invalide!\n")
                input("Appuyez sur Entrée pour continuer...")
            
            self.clear_screen()


def main():
    """Point d'entrée"""
    try:
        cli = PasswordManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n❌ Arrêt de l'application.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
