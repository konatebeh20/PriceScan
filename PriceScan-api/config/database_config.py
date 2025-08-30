# ============================
# CONFIGURATION DES BASES DE DONNEES
# ============================
# 
# Ce fichier contient toutes les configurations possibles pour differents
# environnements et systemes de gestion de bases de donnees.
# 
# INSTRUCTIONS D'UTILISATION :
# 1. Choisissez votre configuration dans la section "CHOIX DE LA CONNEXION ACTIVE"
# 2. Decommentez la ligne correspondante
# 3. Commentez les autres lignes
# 4. Ajustez les parametres selon votre environnement
# 
# ============================

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ============================
# CONFIGURATIONS MYSQL
# ============================

# --- XAMPP (Windows) ---
# Configuration par defaut pour XAMPP
# Port : 3306, User : root, Pas de mot de passe
DATABASE_URI_XAMPP = "mysql+pymysql://root:@localhost:3306/PriceScan_db"

# XAMPP avec mot de passe personnalise
# DATABASE_URI_XAMPP_PWD = "mysql+pymysql://root:votre_mot_de_passe@localhost:3306/PriceScan_db"

# --- phpMyAdmin (Linux/Ubuntu) ---
# Configuration avec utilisateur root
DATABASE_URI_LINUX_ROOT = "mysql+pymysql://root:souris_123@localhost:3306/PriceScan_db"

# Configuration avec utilisateur dedie (recommandee pour la production)
DATABASE_URI_LINUX_USER = "mysql+pymysql://pricescan:scan123@localhost:3306/PriceScan_db"

# --- MySQL distant ---
# Pour une base de donnees hebergee sur un serveur distant
# DATABASE_URI_REMOTE = "mysql+pymysql://user:password@serveur.distant.com:3306/PriceScan_db"

# ============================
# CONFIGURATION POSTGRESQL
# ============================

# PostgreSQL local
DATABASE_URI_POSTGRES = "postgresql+psycopg2://postgres:Konate%202019@localhost:5432/PriceScan_db"

# PostgreSQL distant
# DATABASE_URI_POSTGRES_REMOTE = "postgresql+psycopg2://user:password@serveur.distant.com:5432/PriceScan_db"

# ============================
# CONFIGURATION MONGODB
# ============================

# MongoDB local
DATABASE_URI_MONGO = "mongodb://root:password@localhost:27017/PriceScan_db"

# MongoDB distant
# DATABASE_URI_MONGO_REMOTE = "mongodb://user:password@serveur.distant.com:27017/PriceScan_db"

# MongoDB sans authentification (developpement local)
# DATABASE_URI_MONGO_LOCAL = "mongodb://localhost:27017/PriceScan_db"

# ============================
# CONFIGURATION SQLITE
# ============================

# SQLite (pour le developpement et les tests)
DATABASE_URI_SQLITE = "sqlite:///PriceScan.db"

# SQLite avec chemin absolu
# DATABASE_URI_SQLITE_ABS = "sqlite:////chemin/absolu/vers/PriceScan.db"

# ============================
# CHOIX DE LA CONNEXION ACTIVE
# ============================
#
# DECOMMENTEZ UNE SEULE LIGNE selon votre environnement :
#

# === WINDOWS + XAMPP ===
# SQL_DB_URL = DATABASE_URI_XAMPP

# === LINUX + phpMyAdmin avec root ===
# SQL_DB_URL = DATABASE_URI_LINUX_ROOT

# === LINUX + phpMyAdmin avec utilisateur dedie ===
# SQL_DB_URL = DATABASE_URI_LINUX_USER

# === POSTGRESQL (configuration par defaut) ===
# SQL_DB_URL = DATABASE_URI_POSTGRES

# === WINDOWS + XAMPP ===
SQL_DB_URL = DATABASE_URI_XAMPP

# === MONGODB ===
# SQL_DB_URL = DATABASE_URI_MONGO

# === SQLITE (developpement) ===
# SQL_DB_URL = DATABASE_URI_SQLITE

# ============================
# PRIORITE DES CONFIGURATIONS
# ============================
#
# L'ordre de priorite est le suivant :
# 1. Variable d'environnement DATABASE_URL (si definie)
# 2. Configuration choisie ci-dessus
# 3. Configuration par defaut (PostgreSQL)
#

# Verifier si une variable d'environnement est definie
if os.getenv('DATABASE_URL'):
    SQL_DB_URL = os.getenv('DATABASE_URL')
    print(f"Configuration de base de donnees chargee depuis l'environnement : {SQL_DB_URL}")
else:
    print(f"Configuration de base de donnees utilisee : {SQL_DB_URL}")

# ============================
# VALIDATION DE LA CONFIGURATION
# ============================

def validate_database_config():
    """
    Valide la configuration de la base de donnees
    """
    if not SQL_DB_URL:
        raise ValueError("Aucune configuration de base de donnees n'est definie")
    
    # Verifier le type de base de donnees
    if SQL_DB_URL.startswith('mysql'):
        print("Configuration MySQL detectee")
    elif SQL_DB_URL.startswith('postgresql'):
        print("Configuration PostgreSQL detectee")
    elif SQL_DB_URL.startswith('mongodb'):
        print("Configuration MongoDB detectee")
    elif SQL_DB_URL.startswith('sqlite'):
        print("Configuration SQLite detectee")
    else:
        print("Configuration de base de donnees non reconnue")
    
    return SQL_DB_URL

# ============================
# EXEMPLES D'UTILISATION
# ============================
#
# Pour changer de base de donnees, modifiez simplement la ligne active :
#
# EXEMPLE 1 - XAMPP Windows :
# SQL_DB_URL = DATABASE_URI_XAMPP
#
# EXEMPLE 2 - Linux avec utilisateur dedie :
# SQL_DB_URL = DATABASE_URI_LINUX_USER
#
# EXEMPLE 3 - PostgreSQL :
# SQL_DB_URL = DATABASE_URI_POSTGRES
#
# EXEMPLE 4 - Variable d'environnement :
# export DATABASE_URL="mysql+pymysql://user:pass@localhost:3306/db"
#

if __name__ == "__main__":
    # Test de validation
    try:
        config = validate_database_config()
        print(f"Configuration valide : {config}")
    except Exception as e:
        print(f"Erreur de configuration : {e}")
