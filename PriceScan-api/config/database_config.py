# ============================
# CONFIGURATION DES BASES DE DONNÉES
# ============================
# 
# Ce fichier contient toutes les configurations possibles pour différents
# environnements et systèmes de gestion de bases de données.
# 
# INSTRUCTIONS D'UTILISATION :
# 1. Choisissez votre configuration dans la section "CHOIX DE LA CONNEXION ACTIVE"
# 2. Décommentez la ligne correspondante
# 3. Commentez les autres lignes
# 4. Ajustez les paramètres selon votre environnement
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
# Configuration par défaut pour XAMPP
# Port : 3306, User : root, Pas de mot de passe
DATABASE_URI_XAMPP = "mysql+pymysql://root:@localhost:3306/PriceScan_db"

# XAMPP avec mot de passe personnalisé
# DATABASE_URI_XAMPP_PWD = "mysql+pymysql://root:votre_mot_de_passe@localhost:3306/PriceScan_db"

# --- phpMyAdmin (Linux/Ubuntu) ---
# Configuration avec utilisateur root
DATABASE_URI_LINUX_ROOT = "mysql+pymysql://root:souris_123@localhost:3306/PriceScan_db"

# Configuration avec utilisateur dédié (recommandé pour la production)
DATABASE_URI_LINUX_USER = "mysql+pymysql://pricescan:scan123@localhost:3306/PriceScan_db"

# --- MySQL distant ---
# Pour une base de données hébergée sur un serveur distant
# DATABASE_URI_REMOTE = "mysql+pymysql://user:password@serveur.distant.com:3306/PriceScan_db"

# ============================
# CONFIGURATION POSTGRESQL
# ============================

# PostgreSQL local
DATABASE_URI_POSTGRES = "postgresql+psycopg2://postgres:Konate%2019@localhost:5432/PriceScan_db"

# PostgreSQL distant
# DATABASE_URI_POSTGRES_REMOTE = "postgresql+psycopg2://user:password@serveur.distant.com:5432/PriceScan_db"

# ============================
# CONFIGURATION MONGODB
# ============================

# MongoDB local
DATABASE_URI_MONGO = "mongodb://root:Konate%2019@localhost:27017/PriceScan_db"

# MongoDB distant
# DATABASE_URI_MONGO_REMOTE = "mongodb://user:password@serveur.distant.com:27017/PriceScan_db"

# MongoDB sans authentification (développement local)
# DATABASE_URI_MONGO_LOCAL = "mongodb://localhost:27017/PriceScan_db"

# ============================
# CONFIGURATION SQLITE
# ============================

# SQLite (pour le développement et les tests)
DATABASE_URI_SQLITE = "sqlite:///PriceScan.db"

# SQLite avec chemin absolu
# DATABASE_URI_SQLITE_ABS = "sqlite:////chemin/absolu/vers/PriceScan.db"

# ============================
# CHOIX DE LA CONNEXION ACTIVE
# ============================
#
# DÉCOMMENTEZ UNE SEULE LIGNE selon votre environnement :
#

# === WINDOWS + XAMPP (configuration par défaut) ===
SQL_DB_URL = DATABASE_URI_XAMPP

# === LINUX + phpMyAdmin avec root ===
# SQL_DB_URL = DATABASE_URI_LINUX_ROOT

# === LINUX + phpMyAdmin avec utilisateur dédié ===
# SQL_DB_URL = DATABASE_URI_LINUX_USER

# === POSTGRESQL ===
# SQL_DB_URL = DATABASE_URI_POSTGRES

# === MONGODB ===
# SQL_DB_URL = DATABASE_URI_MONGO

# === SQLITE (développement) ===
# SQL_DB_URL = DATABASE_URI_SQLITE

# ============================
# PRIORITÉ DES CONFIGURATIONS
# ============================
#
# L'ordre de priorité est le suivant :
# 1. Variable d'environnement DATABASE_URL (si définie)
# 2. Configuration choisie ci-dessus
# 3. Configuration par défaut (XAMPP)
#

# Vérifier si une variable d'environnement est définie
if os.getenv('DATABASE_URL'):
    SQL_DB_URL = os.getenv('DATABASE_URL')
    print(f"Configuration de base de données chargée depuis l'environnement : {SQL_DB_URL}")
else:
    print(f"Configuration de base de données utilisée : {SQL_DB_URL}")

# ============================
# VALIDATION DE LA CONFIGURATION
# ============================

def validate_database_config():
    """
    Valide la configuration de la base de données
    """
    if not SQL_DB_URL:
        raise ValueError("Aucune configuration de base de données n'est définie")
    
    # Vérifier le type de base de données
    if SQL_DB_URL.startswith('mysql'):
        print("✓ Configuration MySQL détectée")
    elif SQL_DB_URL.startswith('postgresql'):
        print("✓ Configuration PostgreSQL détectée")
    elif SQL_DB_URL.startswith('mongodb'):
        print("✓ Configuration MongoDB détectée")
    elif SQL_DB_URL.startswith('sqlite'):
        print("✓ Configuration SQLite détectée")
    else:
        print("⚠ Configuration de base de données non reconnue")
    
    return SQL_DB_URL

# ============================
# EXEMPLES D'UTILISATION
# ============================
#
# Pour changer de base de données, modifiez simplement la ligne active :
#
# EXEMPLE 1 - XAMPP Windows :
# SQL_DB_URL = DATABASE_URI_XAMPP
#
# EXEMPLE 2 - Linux avec utilisateur dédié :
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
