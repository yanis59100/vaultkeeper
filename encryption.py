"""Module de chiffrement pour le gestionnaire de mots de passe - Renforcé"""

import os
import json
import base64
import hashlib
import time
import ctypes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class PasswordEncryption:
    """Gère le chiffrement et déchiffrement des données - Version sécurisée avec support multi-utilisateur"""
    
    USERS_DIR = ".users"  # Dossier pour les données utilisateur
    
    def __init__(self, master_password: str, user_id: str = "local"):
        """
        Initialise le gestionnaire de chiffrement
        
        Args:
            master_password: Le mot de passe maître ou l'email Google
            user_id: Identifiant utilisateur (email pour Google OAuth, "local" pour mode local)
        """
        if len(master_password) < 6:
            raise ValueError("Le mot de passe maître doit avoir au moins 6 caractères")
        
        self.master_password = master_password
        self.user_id = user_id
        self._setup_user_directory()
        self.cipher = self._get_cipher()
    
    def _setup_user_directory(self):
        """Crée le dossier utilisateur s'il n'existe pas"""
        if not os.path.exists(self.USERS_DIR):
            os.makedirs(self.USERS_DIR, exist_ok=True)
            self._protect_file(self.USERS_DIR)
        
        # Créer un dossier pour cet utilisateur (sanitized user_id)
        safe_user_id = self._sanitize_filename(self.user_id)
        self.user_dir = os.path.join(self.USERS_DIR, safe_user_id)
        
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir, exist_ok=True)
            self._protect_file(self.user_dir)
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Rend un string safe pour utilisation comme nom de fichier"""
        # Remplacer les caractères non-sûrs
        safe_name = filename.replace("@", "_at_").replace("/", "_").replace("\\", "_")
        safe_name = safe_name.replace(":", "_").replace("*", "_").replace("?", "_")
        safe_name = safe_name.replace('"', "_").replace("<", "_").replace(">", "_")
        safe_name = safe_name.replace("|", "_")
        return safe_name[:50]  # Limiter la longueur
    
    def _get_file_path(self, filename: str) -> str:
        """Retourne le chemin complet d'un fichier utilisateur"""
        return os.path.join(self.user_dir, filename)
    
    def _get_cipher(self) -> Fernet:
        """
        Crée un objet Fernet à partir du mot de passe maître avec PBKDF2 renforcé
        
        Returns:
            Objet Fernet pour le chiffrement/déchiffrement
        """
        salt_file = self._get_file_path(".salt.bin")
        
        # Génère ou charge le salt
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as f:
                salt = f.read()
        else:
            salt = os.urandom(32)  # Salt plus long (32 bytes au lieu de 16)
            with open(salt_file, 'wb') as f:
                f.write(salt)
            # Protéger le fichier de salt
            self._protect_file(salt_file)
        
        # Dérive la clé du mot de passe maître avec PBKDF2 renforcé
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,  # Augmenté (NIST recommande 600000+, mais bon compromis perfs)
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(self.master_password.encode())
        )
        return Fernet(key)
    
    @staticmethod
    def _protect_file(filepath):
        """Rend le fichier moins visible/accessible sur Windows"""
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(filepath, 2)  # FILE_ATTRIBUTE_HIDDEN
        except:
            pass  # Silencieusement échouer si pas sur Windows
    
    def _compute_data_hash(self, data: dict) -> bytes:
        """Calcule un hash HMAC des données pour vérifier l'intégrité"""
        json_data = json.dumps(data, ensure_ascii=False, sort_keys=True)
        hash_key = hashlib.pbkdf2_hmac('sha256', self.master_password.encode(), b'integrity', 10000)
        return hashlib.new('sha256', json_data.encode() + hash_key).digest()
    
    def encrypt_data(self, data: dict) -> None:
        """
        Chiffre et enregistre les données de manière sécurisée avec gestion des accès
        
        Args:
            data: Dictionnaire contenant les comptes
        """
        json_data = json.dumps(data, ensure_ascii=False)
        encrypted = self.cipher.encrypt(json_data.encode())
        
        data_file = self._get_file_path(".passwords.enc")
        hash_file = self._get_file_path(".hash.bin")
        
        # Écrire les données chiffrées avec retry sur permission denied
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Supprimer le fichier ancien s'il existe
                if os.path.exists(data_file):
                    try:
                        os.remove(data_file)
                    except:
                        time.sleep(0.1)  # Attendre si le fichier est verrouillé
                
                # Écrire les nouvelles données
                with open(data_file, 'wb') as f:
                    f.write(encrypted)
                self._protect_file(data_file)
                break
            except (PermissionError, OSError) as e:
                if attempt < max_retries - 1:
                    time.sleep(0.2)  # Attendre et réessayer
                else:
                    raise
        
        # Écrire le hash pour vérifier l'intégrité
        data_hash = self._compute_data_hash(data)
        for attempt in range(max_retries):
            try:
                if os.path.exists(hash_file):
                    try:
                        os.remove(hash_file)
                    except:
                        time.sleep(0.1)
                
                with open(hash_file, 'wb') as f:
                    f.write(data_hash)
                self._protect_file(hash_file)
                break
            except (PermissionError, OSError) as e:
                if attempt < max_retries - 1:
                    time.sleep(0.2)
                else:
                    raise
    
    def decrypt_data(self) -> dict:
        """
        Déchiffre et charge les données avec vérification d'intégrité
        
        Returns:
            Dictionnaire contenant les comptes, ou {} si fichier n'existe pas
            
        Raises:
            ValueError: Si le mot de passe maître est incorrect ou données corrompues
        """
        data_file = self._get_file_path(".passwords.enc")
        hash_file = self._get_file_path(".hash.bin")
        
        if not os.path.exists(data_file):
            return {}
        
        try:
            with open(data_file, 'rb') as f:
                encrypted = f.read()
            
            # Vérifier l'intégrité si possible
            if os.path.exists(hash_file):
                with open(hash_file, 'rb') as f:
                    stored_hash = f.read()
            else:
                stored_hash = None
            
            decrypted = self.cipher.decrypt(encrypted)
            data = json.loads(decrypted.decode())
            
            # Vérifier le hash si disponible
            if stored_hash:
                computed_hash = self._compute_data_hash(data)
                if computed_hash != stored_hash:
                    raise ValueError("⚠️ Les données semblent avoir été modifiées!")
            
            return data
        
        except InvalidToken:
            raise ValueError("❌ Mot de passe maître incorrect!")
        except json.JSONDecodeError:
            raise ValueError("❌ Les données sont corrompues!")
        except Exception as e:
            raise ValueError(f"❌ Erreur de déchiffrement: {e}")
    
    def verify_master_password(self) -> bool:
        """
        Vérifie que le mot de passe maître est correct
        
        Returns:
            True si le mot de passe est correct, False sinon
        """
        data_file = self._get_file_path(".passwords.enc")
        
        if not os.path.exists(data_file):
            return True  # Première utilisation
        
        try:
            self.decrypt_data()
            return True
        except:
            return False
