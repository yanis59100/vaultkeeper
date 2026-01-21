"""
Client Python pour communiquer avec le backend Node.js VaultKeeper
"""

import requests
import json
import base64
from typing import Dict, Optional, List
from datetime import datetime


class VaultKeeperBackendClient:
    """Client pour synchroniser les mots de passe avec le serveur VaultKeeper"""
    
    def __init__(self, backend_url: str = "http://localhost:3000"):
        """
        Initialise le client backend
        
        Args:
            backend_url: URL du serveur backend (par défaut localhost:3000)
        """
        self.backend_url = backend_url.rstrip('/')
        self.token = None
        self.user_email = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'VaultKeeper-Desktop/1.0'
        })
    
    def _set_auth_header(self):
        """Ajoute le token JWT aux headers"""
        if self.token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}'
            })
    
    def health_check(self) -> bool:
        """Vérifier si le serveur est accessible"""
        try:
            response = self.session.get(f"{self.backend_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erreur de connexion au backend: {e}")
            return False
    
    def register(self, email: str, password: str) -> Dict:
        """
        Enregistrer un nouvel utilisateur
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe (sera hashé côté serveur)
        
        Returns:
            {
                'success': bool,
                'message': str,
                'token': str (si succès)
            }
        """
        try:
            response = self.session.post(
                f"{self.backend_url}/api/auth/register",
                json={'email': email, 'password': password},
                timeout=10
            )
            data = response.json()
            
            if response.status_code == 201:
                self.token = data.get('token')
                self.user_email = email
                self._set_auth_header()
                return {
                    'success': True,
                    'message': 'RegistrationSuccessful',
                    'token': self.token
                }
            else:
                return {
                    'success': False,
                    'message': data.get('error', 'Unknown error')
                }
        except requests.exceptions.Timeout:
            return {'success': False, 'message': 'Backend timeout'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def login(self, email: str, password: str) -> Dict:
        """
        Connexion utilisateur
        
        Args:
            email: Email
            password: Mot de passe
        
        Returns:
            {'success': bool, 'message': str, 'token': str}
        """
        try:
            response = self.session.post(
                f"{self.backend_url}/api/auth/login",
                json={'email': email, 'password': password},
                timeout=10
            )
            data = response.json()
            
            if response.status_code == 200:
                self.token = data.get('token')
                self.user_email = email
                self._set_auth_header()
                return {
                    'success': True,
                    'message': 'Login successful',
                    'token': self.token
                }
            else:
                return {
                    'success': False,
                    'message': data.get('error', 'Login failed')
                }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def verify_token(self) -> bool:
        """Vérifier si le token JWT est valide"""
        if not self.token:
            return False
        
        try:
            self._set_auth_header()
            response = self.session.get(
                f"{self.backend_url}/api/auth/verify",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def sync_vault(self, encrypted_data: str, salt: str) -> Dict:
        """
        Synchroniser le coffre chiffré avec le serveur
        
        Args:
            encrypted_data: Données chiffrées (base64)
            salt: Salt utilisé pour le chiffrement
        
        Returns:
            {'success': bool, 'message': str, 'version': int}
        """
        if not self.token:
            return {'success': False, 'message': 'Not authenticated'}
        
        try:
            self._set_auth_header()
            response = self.session.post(
                f"{self.backend_url}/api/vault/sync",
                json={
                    'encrypted_data': encrypted_data,
                    'salt': salt
                },
                timeout=10
            )
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Sync successful',
                    'version': data.get('version')
                }
            else:
                return {
                    'success': False,
                    'message': data.get('error', 'Sync failed')
                }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_vault(self) -> Dict:
        """
        Récupérer le coffre synchronisé
        
        Returns:
            {
                'success': bool,
                'message': str,
                'data': {'encrypted_data': str, 'salt': str, 'version': int}
            }
        """
        if not self.token:
            return {'success': False, 'message': 'Not authenticated'}
        
        try:
            self._set_auth_header()
            response = self.session.get(
                f"{self.backend_url}/api/vault",
                timeout=10
            )
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Vault retrieved',
                    'data': {
                        'encrypted_data': data.get('encrypted_data'),
                        'salt': data.get('salt'),
                        'version': data.get('version', 0)
                    }
                }
            else:
                return {
                    'success': False,
                    'message': data.get('error', 'Failed to retrieve vault')
                }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_sync_history(self) -> Dict:
        """
        Récupérer l'historique de synchronisation
        
        Returns:
            {'success': bool, 'message': str, 'history': List[Dict]}
        """
        if not self.token:
            return {'success': False, 'message': 'Not authenticated'}
        
        try:
            self._set_auth_header()
            response = self.session.get(
                f"{self.backend_url}/api/vault/history",
                timeout=10
            )
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'History retrieved',
                    'history': data.get('history', [])
                }
            else:
                return {
                    'success': False,
                    'message': data.get('error', 'Failed to retrieve history')
                }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def logout(self):
        """Déconnecter l'utilisateur"""
        self.token = None
        self.user_email = None
        self.session.headers.pop('Authorization', None)
    
    def is_authenticated(self) -> bool:
        """Vérifier si l'utilisateur est authentifié"""
        return self.token is not None


# Test simple
if __name__ == "__main__":
    client = VaultKeeperBackendClient()
    
    print("🔍 Vérification du serveur...")
    if client.health_check():
        print("✅ Serveur accessible!")
    else:
        print("❌ Serveur non accessible")
