# ============================
# EXEMPLES DE CONFIGURATION DES BASES DE DONNÉES
# ============================
#
# Ce fichier contient des exemples de configuration pour différents
# environnements et cas d'usage.
#
# UTILISATION :
# 1. Copiez ce fichier vers database_config.py
# 2. Décommentez la configuration souhaitée
# 3. Ajustez les paramètres selon votre environnement
#
# ============================

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ============================
# EXEMPLE 1: XAMPP SUR WINDOWS
# ============================
# Configuration typique pour le développement sur Windows
# avec XAMPP installé

def config_xampp_windows():
    """Configuration XAMPP sur Windows"""
    
    # Configuration par défaut (root sans mot de passe)
    DATABASE_URI_XAMPP = "mysql+pymysql://root:@localhost:3306/PriceScan_db"
    
    # Configuration avec mot de passe personnalisé
    # DATABASE_URI_XAMPP_PWD = "mysql+pymysql://root:votre_mot_de_passe@localhost:3306/PriceScan_db"
    
    # Configuration avec port personnalisé
    # DATABASE_URI_XAMPP_CUSTOM_PORT = "mysql+pymysql://root:@localhost:3307/PriceScan_db"
    
    return DATABASE_URI_XAMPP

# ============================
# EXEMPLE 2: LINUX + PHPMyADMIN
# ============================
# Configuration pour serveurs Linux avec phpMyAdmin

def config_linux_phpmyadmin():
    """Configuration Linux + phpMyAdmin"""
    
    # Configuration avec utilisateur root
    DATABASE_URI_LINUX_ROOT = "mysql+pymysql://root:souris_123@localhost:3306/PriceScan_db"
    
    # Configuration avec utilisateur dédié (recommandé)
    DATABASE_URI_LINUX_USER = "mysql+pymysql://pricescan:scan123@localhost:3306/PriceScan_db"
    
    # Configuration avec serveur distant
    # DATABASE_URI_LINUX_REMOTE = "mysql+pymysql://user:password@192.168.1.100:3306/PriceScan_db"
    
    return DATABASE_URI_LINUX_USER

# ============================
# EXEMPLE 3: POSTGRESQL
# ============================
# Configuration pour bases de données PostgreSQL

def config_postgresql():
    """Configuration PostgreSQL"""
    
    # Configuration locale
    DATABASE_URI_POSTGRES_LOCAL = "postgresql+psycopg2://postgres:Konate%2019@localhost:5432/PriceScan_db"
    
    # Configuration avec utilisateur dédié
    DATABASE_URI_POSTGRES_USER = "postgresql+psycopg2://pricescan:scan123@localhost:5432/PriceScan_db"
    
    # Configuration serveur distant
    # DATABASE_URI_POSTGRES_REMOTE = "postgresql+psycopg2://user:password@serveur.distant.com:5432/PriceScan_db"
    
    # Configuration avec SSL
    # DATABASE_URI_POSTGRES_SSL = "postgresql+psycopg2://user:password@localhost:5432/PriceScan_db?sslmode=require"
    
    return DATABASE_URI_POSTGRES_LOCAL

# ============================
# EXEMPLE 4: MONGODB
# ============================
# Configuration pour bases de données MongoDB

def config_mongodb():
    """Configuration MongoDB"""
    
    # Configuration locale avec authentification
    DATABASE_URI_MONGO_LOCAL = "mongodb://root:Konate%2019@localhost:27017/PriceScan_db"
    
    # Configuration locale sans authentification (développement)
    DATABASE_URI_MONGO_DEV = "mongodb://localhost:27017/PriceScan_db"
    
    # Configuration avec utilisateur dédié
    DATABASE_URI_MONGO_USER = "mongodb://pricescan:scan123@localhost:27017/PriceScan_db"
    
    # Configuration serveur distant
    # DATABASE_URI_MONGO_REMOTE = "mongodb://user:password@serveur.distant.com:27017/PriceScan_db"
    
    # Configuration avec réplica set
    # DATABASE_URI_MONGO_REPLICA = "mongodb://user:password@host1:27017,host2:27017,host3:27017/PriceScan_db?replicaSet=myReplicaSet"
    
    return DATABASE_URI_MONGO_LOCAL

# ============================
# EXEMPLE 5: SQLITE
# ============================
# Configuration pour développement avec SQLite

def config_sqlite():
    """Configuration SQLite"""
    
    # Configuration relative au dossier du projet
    DATABASE_URI_SQLITE_RELATIVE = "sqlite:///PriceScan.db"
    
    # Configuration avec chemin absolu
    DATABASE_URI_SQLITE_ABSOLUTE = "sqlite:////chemin/absolu/vers/PriceScan.db"
    
    # Configuration en mémoire (pour les tests)
    DATABASE_URI_SQLITE_MEMORY = "sqlite:///:memory:"
    
    return DATABASE_URI_SQLITE_RELATIVE

# ============================
# EXEMPLE 6: CONFIGURATION AVANCÉE
# ============================
# Exemples de configuration avancée

def config_avancee():
    """Configuration avancée avec options"""
    
    # MySQL avec options de connexion
    DATABASE_URI_MYSQL_ADVANCED = (
        "mysql+pymysql://user:password@localhost:3306/PriceScan_db"
        "?charset=utf8mb4"
        "&autocommit=true"
        "&pool_size=10"
        "&max_overflow=20"
    )
    
    # PostgreSQL avec options de connexion
    DATABASE_URI_POSTGRES_ADVANCED = (
        "postgresql+psycopg2://user:password@localhost:5432/PriceScan_db"
        "?sslmode=require"
        "&connect_timeout=10"
        "&application_name=PriceScan"
    )
    
    # MongoDB avec options de connexion
    DATABASE_URI_MONGO_ADVANCED = (
        "mongodb://user:password@localhost:27017/PriceScan_db"
        "?authSource=admin"
        "&maxPoolSize=50"
        "&w=majority"
        "&readPreference=primary"
    )
    
    return DATABASE_URI_MYSQL_ADVANCED

# ============================
# EXEMPLE 7: CONFIGURATION PAR ENVIRONNEMENT
# ============================
# Configuration automatique selon l'environnement

def config_par_environnement():
    """Configuration automatique selon l'environnement"""
    
    # Détecter l'environnement
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        # Production : PostgreSQL distant
        return "postgresql+psycopg2://prod_user:prod_pass@prod_server:5432/PriceScan_prod"
    
    elif env == 'staging':
        # Staging : MySQL distant
        return "mysql+pymysql://staging_user:staging_pass@staging_server:3306/PriceScan_staging"
    
    elif env == 'testing':
        # Tests : SQLite en mémoire
        return "sqlite:///:memory:"
    
    else:
        # Développement : XAMPP par défaut
        return "mysql+pymysql://root:@localhost:3306/PriceScan_db"

# ============================
# EXEMPLE 8: CONFIGURATION AVEC FALLBACK
# ============================
# Configuration avec fallback automatique

def config_avec_fallback():
    """Configuration avec fallback automatique"""
    
    # Essayer différentes configurations dans l'ordre
    configs = [
        # 1. Variable d'environnement (priorité maximale)
        os.getenv('DATABASE_URL'),
        
        # 2. Configuration XAMPP (Windows)
        "mysql+pymysql://root:@localhost:3306/PriceScan_db",
        
        # 3. Configuration Linux
        "mysql+pymysql://root:souris_123@localhost:3306/PriceScan_db",
        
        # 4. Configuration PostgreSQL
        "postgresql+psycopg2://postgres:Konate%2019@localhost:5432/PriceScan_db",
        
        # 5. Configuration SQLite (fallback final)
        "sqlite:///PriceScan.db"
    ]
    
    # Retourner la première configuration valide
    for config in configs:
        if config:
            return config
    
    # Fallback par défaut
    return "sqlite:///PriceScan.db"

# ============================
# FONCTION PRINCIPALE
# ============================

def get_database_config():
    """Fonction principale pour obtenir la configuration"""
    
    # Choisir la méthode de configuration souhaitée
    
    # Méthode 1: Configuration fixe
    # return config_xampp_windows()
    
    # Méthode 2: Configuration par environnement
    # return config_par_environnement()
    
    # Méthode 3: Configuration avec fallback
    return config_avec_fallback()

# ============================
# TEST DE LA CONFIGURATION
# ============================

if __name__ == "__main__":
    print("🔧 Test des configurations de base de données")
    print("=" * 50)
    
    print(f"Configuration XAMPP Windows: {config_xampp_windows()}")
    print(f"Configuration Linux phpMyAdmin: {config_linux_phpmyadmin()}")
    print(f"Configuration PostgreSQL: {config_postgresql()}")
    print(f"Configuration MongoDB: {config_mongodb()}")
    print(f"Configuration SQLite: {config_sqlite()}")
    print(f"Configuration par environnement: {config_par_environnement()}")
    print(f"Configuration avec fallback: {config_avec_fallback()}")
    
    print("\n Toutes les configurations sont valides")
