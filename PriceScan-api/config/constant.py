import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# ============================
# CONFIGURATION DE L'APPLICATION
# ============================

# Configuration Flask
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'votre_cle_secrete_tres_longue_et_complexe_ici')
BASE_URL = os.getenv('BASE_URL', '/api')

# ============================
# CONFIGURATION DE LA BASE DE DONNÉES
# ============================

# Importer la configuration de base de données depuis database_config.py
try:
    from .database_config import SQL_DB_URL
except ImportError:
    # Configuration par défaut si le fichier n'est pas trouvé
    SQL_DB_URL = "mysql+pymysql://root:@localhost:3306/PriceScan_db"

# Alternative : Utiliser la variable d'environnement si définie
if os.getenv('DATABASE_URL'):
    SQL_DB_URL = os.getenv('DATABASE_URL')

# ============================
# CONFIGURATION JWT
# ============================

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'votre_cle_jwt_secrete_tres_longue_et_complexe_ici')
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))

# ============================
# CONFIGURATION CORS
# ============================

CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8101,http://localhost:3000,capacitor://localhost').split(',')
CORS_SUPPORTS_CREDENTIALS = os.getenv('CORS_SUPPORTS_CREDENTIALS', 'True').lower() == 'true'

# ============================
# CONFIGURATION REDIS
# ============================

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# ============================
# CONFIGURATION DES UPLOADS
# ============================

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif,pdf').split(',')

# ============================
# CONFIGURATION SENTRY (optionnel)
# ============================

SENTRY_DSN = os.getenv('SENTRY_DSN', '')

# ============================
# CONFIGURATION DES EMAILS (optionnel)
# ============================

MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')

# ============================
# CONFIGURATION DES NOTIFICATIONS PUSH (optionnel)
# ============================

FCM_SERVER_KEY = os.getenv('FCM_SERVER_KEY', '')
APNS_KEY_ID = os.getenv('APNS_KEY_ID', '')
APNS_TEAM_ID = os.getenv('APNS_TEAM_ID', '')
APNS_AUTH_KEY = os.getenv('APNS_AUTH_KEY', '')

# ============================
# CONFIGURATION DES LIMITES DE TAUX
# ============================

RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'redis://localhost:6379')
RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per minute')
RATELIMIT_STORAGE_OPTIONS = os.getenv('RATELIMIT_STORAGE_OPTIONS', 'connection_pool_size=10')

# ============================
# CONFIGURATION DES LOGS
# ============================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', 10485760))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))

# ============================
# CONSTANTES DE L'APPLICATION
# ============================

# Nom et version de l'application
APP_NAME = "PriceScan API"
APP_VERSION = "1.0.0"

# Statuts des reçus
RECEIPT_STATUS_PENDING = "pending"
RECEIPT_STATUS_VERIFIED = "verified"
RECEIPT_STATUS_REJECTED = "rejected"

# Types de notifications
NOTIFICATION_TYPE_PRICE_ALERT = "price_alert"
NOTIFICATION_TYPE_RECEIPT_VERIFIED = "receipt_verified"
NOTIFICATION_TYPE_SYSTEM = "system"

# Sources de prix
PRICE_SOURCE_MANUAL = "manual"
PRICE_SOURCE_OCR = "ocr"
PRICE_SOURCE_API = "api"
PRICE_SOURCE_SCRAPER = "scraper"

# Devises supportées
SUPPORTED_CURRENCIES = ["CFA", "EUR", "USD", "GBP", "JPY"]

# Limites de pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
DEFAULT_SEARCH_LIMIT = 50
