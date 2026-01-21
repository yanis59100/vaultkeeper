"""Logique du gestionnaire de mots de passe"""

import string
import secrets
from typing import List, Optional, Dict
from datetime import datetime
from encryption import PasswordEncryption


class PasswordManager:
    """Gestionnaires des comptes et mots de passe"""
    
    def __init__(self, master_password: str, user_id: str = "local"):
        """
        Initialise le gestionnaire de mots de passe
        
        Args:
            master_password: Le mot de passe maître ou l'email Google
            user_id: Identifiant utilisateur (par défaut "local" pour mode local)
        """
        self.user_id = user_id
        self.encryption = PasswordEncryption(master_password, user_id=user_id)
        self.accounts = self.encryption.decrypt_data()
    
    def add_account(self, site: str, username: str, password: str, 
                   url: str = "", notes: str = "", 
                   category: str = "General", is_favorite: bool = False) -> None:
        """
        Ajoute un nouveau compte
        
        Args:
            site: Nom du site/service
            username: Nom d'utilisateur ou email
            password: Mot de passe
            url: URL du site
            notes: Notes/commentaires
            category: Catégorie (General, Social, Banking, Email, Gaming, Work, Other)
            is_favorite: Marquer comme favori
        """
        if site not in self.accounts:
            self.accounts[site] = []
        
        now = datetime.now().isoformat()
        self.accounts[site].append({
            "username": username,
            "password": password,
            "url": url,
            "notes": notes,
            "category": category,
            "is_favorite": is_favorite,
            "created_at": now,
            "modified_at": now
        })
        
        self._save()
    
    def get_accounts(self, site: Optional[str] = None) -> dict:
        """
        Récupère les comptes
        
        Args:
            site: Optionnel, pour récupérer les comptes d'un site spécifique
        
        Returns:
            Dictionnaire des comptes
        """
        if site:
            return {site: self.accounts.get(site, [])}
        return self.accounts
    
    def delete_account(self, site: str, username: str) -> bool:
        """
        Supprime un compte
        
        Args:
            site: Nom du site
            username: Nom d'utilisateur
        
        Returns:
            True si la suppression a réussi, False sinon
        """
        if site in self.accounts:
            self.accounts[site] = [
                acc for acc in self.accounts[site] 
                if acc["username"] != username
            ]
            
            if not self.accounts[site]:
                del self.accounts[site]
            
            self._save()
            return True
        
        return False
    
    def update_account(self, site: str, old_username: str, 
                       new_username: str, new_password: str,
                       url: str = None, notes: str = None,
                       category: str = None, is_favorite: bool = None) -> bool:
        """
        Met à jour un compte existant
        
        Args:
            site: Nom du site
            old_username: Ancien nom d'utilisateur
            new_username: Nouveau nom d'utilisateur
            new_password: Nouveau mot de passe
            url: URL du site (optionnel)
            notes: Notes (optionnel)
            category: Catégorie (optionnel)
            is_favorite: Favori (optionnel)
        
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        if site in self.accounts:
            for account in self.accounts[site]:
                if account["username"] == old_username:
                    account["username"] = new_username
                    account["password"] = new_password
                    account["modified_at"] = datetime.now().isoformat()
                    
                    # Mettre à jour les champs optionnels s'ils sont fournis
                    if url is not None:
                        account["url"] = url
                    if notes is not None:
                        account["notes"] = notes
                    if category is not None:
                        account["category"] = category
                    if is_favorite is not None:
                        account["is_favorite"] = is_favorite
                    
                    # S'assurer que tous les champs existent (rétrocompatibilité)
                    if "url" not in account:
                        account["url"] = ""
                    if "notes" not in account:
                        account["notes"] = ""
                    if "category" not in account:
                        account["category"] = "General"
                    if "is_favorite" not in account:
                        account["is_favorite"] = False
                    if "created_at" not in account:
                        account["created_at"] = datetime.now().isoformat()
                    
                    self._save()
                    return True
        
        return False
    
    def generate_password(self, length: int = 16, 
                         use_special: bool = True,
                         use_digits: bool = True,
                         use_uppercase: bool = True) -> str:
        """
        Génère un mot de passe sécurisé aléatoire
        
        Args:
            length: Longueur du mot de passe
            use_special: Inclure les caractères spéciaux
            use_digits: Inclure les chiffres
            use_uppercase: Inclure les majuscules
        
        Returns:
            Mot de passe généré
        """
        characters = string.ascii_lowercase
        
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_digits:
            characters += string.digits
        if use_special:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if length < 1:
            length = 16
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def search_accounts(self, query: str) -> dict:
        """
        Recherche des comptes par site ou utilisateur
        
        Args:
            query: Terme de recherche
        
        Returns:
            Dictionnaire des comptes correspondant
        """
        results = {}
        query_lower = query.lower()
        
        for site, accounts in self.accounts.items():
            if query_lower in site.lower():
                results[site] = accounts
            else:
                matching = [
                    acc for acc in accounts 
                    if query_lower in acc["username"].lower()
                ]
                if matching:
                    results[site] = matching
        
        return results
    
    def get_all_sites(self) -> List[str]:
        """
        Récupère la liste de tous les sites enregistrés
        
        Returns:
            Liste des noms de sites
        """
        return sorted(list(self.accounts.keys()))
    
    def get_favorites(self) -> Dict[str, List[dict]]:
        """
        Récupère tous les comptes favoris
        
        Returns:
            Dictionnaire des comptes favoris
        """
        favorites = {}
        for site, accounts in self.accounts.items():
            fav_accounts = [acc for acc in accounts if acc.get("is_favorite", False)]
            if fav_accounts:
                favorites[site] = fav_accounts
        return favorites
    
    def get_by_category(self, category: str) -> Dict[str, List[dict]]:
        """
        Récupère les comptes par catégorie
        
        Returns:
            Dictionnaire des comptes de cette catégorie
        """
        results = {}
        for site, accounts in self.accounts.items():
            cat_accounts = [acc for acc in accounts if acc.get("category", "General") == category]
            if cat_accounts:
                results[site] = cat_accounts
        return results
    
    def check_password_strength(self, password: str) -> Dict[str, any]:
        """
        Évalue la force d'un mot de passe
        
        Returns:
            Dict avec score (0-4), couleur, label, suggestions
        """
        score = 0
        suggestions = []
        
        # Longueur
        if len(password) >= 12:
            score += 1
        else:
            suggestions.append("Use at least 12 characters")
        
        # Majuscules
        if any(c.isupper() for c in password):
            score += 1
        else:
            suggestions.append("Add uppercase letters")
        
        # Minuscules
        if any(c.islower() for c in password):
            score += 0.5
        
        # Chiffres
        if any(c.isdigit() for c in password):
            score += 1
        else:
            suggestions.append("Add numbers")
        
        # Caractères spéciaux
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            suggestions.append("Add special characters")
        
        # Variété
        if len(set(password)) > len(password) * 0.6:
            score += 0.5
        
        # Déterminer couleur et label
        if score >= 4:
            color = "#10b981"  # Vert
            label = "Very Strong"
        elif score >= 3:
            color = "#10b981"  # Vert
            label = "Strong"
        elif score >= 2:
            color = "#f59e0b"  # Orange
            label = "Medium"
        elif score >= 1:
            color = "#f59e0b"  # Orange
            label = "Weak"
        else:
            color = "#ef4444"  # Rouge
            label = "Very Weak"
        
        return {
            "score": min(score, 4),
            "max_score": 4,
            "color": color,
            "label": label,
            "suggestions": suggestions
        }
    
    def export_data(self, format: str = "json") -> str:
        """
        Export les données (non chiffrées) en JSON ou CSV
        ATTENTION: Les mots de passe sont en clair!
        
        Returns:
            String avec les données
        """
        import json
        
        if format == "json":
            return json.dumps(self.accounts, indent=2)
        elif format == "csv":
            lines = ["Site,Username,Password,URL,Notes,Category,Favorite,Created,Modified"]
            for site, accounts in self.accounts.items():
                for acc in accounts:
                    lines.append(
                        f"{site},{acc.get('username', '')},{acc.get('password', '')}," +
                        f"{acc.get('url', '')},{acc.get('notes', '')},{acc.get('category', 'General')}," +
                        f"{acc.get('is_favorite', False)},{acc.get('created_at', '')},{acc.get('modified_at', '')}"
                    )
            return "\n".join(lines)
        return ""
    
    def _save(self) -> None:
        """Enregistre les données chiffrées"""
        self.encryption.encrypt_data(self.accounts)
