"""
Configuration globale du gestionnaire de mots de passe
Permet de personnaliser certains paramètres de l'application
"""

# ============= PARAMÈTRES DE CHIFFREMENT =============

# Nombre d'itérations pour PBKDF2 (plus élevé = plus sûr mais plus lent)
# Recommandé : 100000 ou plus
PBKDF2_ITERATIONS = 100000

# Taille du salt en bytes (minimum 16)
SALT_SIZE = 16

# Longueur de la clé dérivée en bytes (32 = 256 bits)
KEY_LENGTH = 32

# ============= PARAMÈTRES DE GÉNÉRATION DE MOT DE PASSE =============

# Longueur par défaut d'un mot de passe généré
DEFAULT_PASSWORD_LENGTH = 16

# Longueur minimum autorisée
MIN_PASSWORD_LENGTH = 8

# Longueur maximum autorisée
MAX_PASSWORD_LENGTH = 32

# ============= PARAMÈTRES DE L'INTERFACE =============

# Largeur de la fenêtre principale
WINDOW_WIDTH = 900

# Hauteur de la fenêtre principale
WINDOW_HEIGHT = 600

# Largeur minimale
MIN_WINDOW_WIDTH = 700

# Hauteur minimale
MIN_WINDOW_HEIGHT = 400

# ============= NOMS DES FICHIERS =============

# Fichier contenant le salt
SALT_FILE = "salt.bin"

# Fichier contenant les données chiffrées
DATA_FILE = "passwords.enc"

# ============= MESSAGES =============

# Message d'avertissement au premier lancement
FIRST_LAUNCH_MESSAGE = """
Bienvenue! C'est votre premier lancement.

Un mot de passe maître fort est CRUCIAL pour la sécurité.

Recommandations :
✓ Au moins 16 caractères
✓ Mélange de majuscules, minuscules, chiffres, caractères spéciaux
✓ Quelque chose que vous n'oublierez pas mais personne ne pourra deviner

Exemples FORTS :
✓ Tr0p!cal$unset#2026@Sec
✓ MyP@ss2026-VaultSecure!
✓ C0mplex#Pass$2026&Safe

Exemples FAIBLES à éviter :
✗ password123
✗ qwerty
✗ admin
✗ 123456
"""

# ============= OPTIONS DE LOGS =============

# Activer les logs de débogage
DEBUG_MODE = False

# Chemin du fichier de logs
LOG_FILE = "password_manager.log"

# Niveau de log (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"
