# ============================
# DATABASE CONFIGURATION
# ============================

# --- MySQL avec XAMPP (Windows) ---
# Par défaut : user = root, pas de mot de passe
# Si mot de passe défini, remplacer après root:
DATABASE_URI_XAMPP = "mysql+pymysql://root:@localhost:3306/PriceScan_db"


# --- MySQL avec phpMyAdmin (Linux / Ubuntu) ---
# Exemple avec root + mot de passe
DATABASE_URI_LINUX_ROOT = "mysql+pymysql://root:souris_123@localhost:3306/PriceScan_db"

# # Exemple avec utilisateur dédié
# DATABASE_URI_LINUX_USER = "mysql+pymysql://pricescan:scan123@localhost:3306/PriceScan_db"


# --- PostgreSQL ---
# Format : postgresql+psycopg2://user:password@host:port/dbname
DATABASE_URI_POSTGRES = "postgresql+psycopg2://postgres:Konate%2019@localhost:5432/PriceScan_db"


# --- MongoDB ---
# Format standard de connexion MongoDB
# mongodb://user:password@host:port/dbname
DATABASE_URI_MONGO = "mongodb://root:Konate%2019@localhost:27017/PriceScan_db"


# ============================
# Choix de la connexion active
# ============================

# Active l'une des connexions selon l'environnement
DATABASE_URI = DATABASE_URI_XAMPP
# DATABASE_URI = DATABASE_URI_LINUX_ROOT
# DATABASE_URI = DATABASE_URI_LINUX_USER
# DATABASE_URI = DATABASE_URI_POSTGRES
# DATABASE_URI = DATABASE_URI_MONGO
