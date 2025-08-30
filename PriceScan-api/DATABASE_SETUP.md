# 🗄️ GUIDE DE CONFIGURATION DES BASES DE DONNÉES

Ce guide vous explique comment configurer PriceScan API avec différentes bases de données selon votre environnement.

##  Table des matières

1. [Configuration rapide](#-configuration-rapide)
2. [XAMPP sur Windows](#-xampp-sur-windows)
3. [phpMyAdmin sur Linux](#-phpmyadmin-sur-linux)
4. [PostgreSQL](#-postgresql)
5. [MongoDB](#-mongodb)
6. [SQLite](#-sqlite)
7. [Dépannage](#-dépannage)

##  Configuration rapide

### Étape 1 : Choisir votre base de données
Ouvrez le fichier `config/database_config.py` et décommentez la ligne correspondant à votre environnement :

```python
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
```

### Étape 2 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 3 : Créer la base de données
Suivez les instructions spécifiques à votre base de données ci-dessous.

## 🪟 XAMPP sur Windows

### Installation
1. Téléchargez XAMPP depuis [https://www.apachefriends.org/](https://www.apachefriends.org/)
2. Installez XAMPP (MySQL sera installé automatiquement)
3. Lancez XAMPP Control Panel
4. Démarrez les services Apache et MySQL

### Configuration
1. Ouvrez phpMyAdmin : http://localhost/phpmyadmin
2. Créez une nouvelle base de données nommée `PriceScan_db`
3. Vérifiez que l'utilisateur `root` n'a pas de mot de passe

### Test de connexion
```bash
# Dans le dossier PriceScan-api
python -c "from config.database_config import validate_database_config; validate_database_config()"
```

**Résultat attendu :**
```
✓ Configuration MySQL détectée
Configuration valide : mysql+pymysql://root:@localhost:3306/PriceScan_db
```

## 🐧 phpMyAdmin sur Linux

### Installation (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install apache2 mysql-server php php-mysql phpmyadmin
sudo mysql_secure_installation
```

### Configuration MySQL
```bash
# Se connecter à MySQL
sudo mysql -u root -p

# Créer la base de données
CREATE DATABASE PriceScan_db;

# Créer un utilisateur dédié (recommandé)
CREATE USER 'pricescan'@'localhost' IDENTIFIED BY 'scan123';
GRANT ALL PRIVILEGES ON PriceScan_db.* TO 'pricescan'@'localhost';
FLUSH PRIVILEGES;

# Ou utiliser root (moins sécurisé)
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'souris_123';
FLUSH PRIVILEGES;

EXIT;
```

### Configuration PriceScan
Dans `config/database_config.py`, décommentez :
```python
# === LINUX + phpMyAdmin avec utilisateur dédié ===
SQL_DB_URL = DATABASE_URI_LINUX_USER

# OU pour root
# SQL_DB_URL = DATABASE_URI_LINUX_ROOT
```

## 🐘 PostgreSQL

### Installation

#### Windows
1. Téléchargez depuis [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Installez avec l'utilisateur `postgres` et le mot de passe `Konate%2019`

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql

# Dans PostgreSQL
CREATE DATABASE PriceScan_db;
CREATE USER pricescan WITH PASSWORD 'scan123';
GRANT ALL PRIVILEGES ON DATABASE PriceScan_db TO pricescan;
\q
```

### Configuration PriceScan
Dans `config/database_config.py`, décommentez :
```python
# === POSTGRESQL ===
SQL_DB_URL = DATABASE_URI_POSTGRES
```

### Test de connexion
```bash
python -c "from config.database_config import validate_database_config; validate_database_config()"
```

## 🍃 MongoDB

### Installation

#### Windows
1. Téléchargez depuis [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Installez MongoDB Community Server

#### Linux (Ubuntu/Debian)
```bash
# Importer la clé publique MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Ajouter le dépôt MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Installer MongoDB
sudo apt update
sudo apt install mongodb-org

# Démarrer MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Configuration
```bash
# Se connecter à MongoDB
mongosh

# Créer la base de données
use PriceScan_db

# Créer un utilisateur administrateur
db.createUser({
  user: "root",
  pwd: "Konate%2019",
  roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
})

exit
```

### Configuration PriceScan
Dans `config/database_config.py`, décommentez :
```python
# === MONGODB ===
SQL_DB_URL = DATABASE_URI_MONGO
```

## 🗃️ SQLite

### Configuration
SQLite ne nécessite aucune installation. C'est parfait pour le développement et les tests.

Dans `config/database_config.py`, décommentez :
```python
# === SQLITE (développement) ===
SQL_DB_URL = DATABASE_URI_SQLITE
```

## 🔧 Dépannage

### Erreur de connexion MySQL
```bash
# Vérifier que MySQL est démarré
# Windows
net start mysql

# Linux
sudo systemctl status mysql
sudo systemctl start mysql
```

### Erreur de port
```bash
# Vérifier les ports utilisés
# Windows
netstat -ano | findstr :3306

# Linux
sudo netstat -tlnp | grep :3306
```

### Erreur d'authentification
```bash
# Réinitialiser le mot de passe root MySQL
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nouveau_mot_de_passe';
FLUSH PRIVILEGES;
EXIT;
```

### Erreur de module Python
```bash
# Installer les dépendances manquantes
pip install pymysql psycopg2-binary pymongo

# Ou réinstaller toutes les dépendances
pip install -r requirements.txt
```

## 📝 Variables d'environnement

Vous pouvez aussi utiliser des variables d'environnement pour configurer la base de données :

### Windows
```cmd
set DATABASE_URL=mysql+pymysql://root:@localhost:3306/PriceScan_db
```

### Linux/Mac
```bash
export DATABASE_URL="mysql+pymysql://root:souris_123@localhost:3306/PriceScan_db"
```

### Fichier .env
Créez un fichier `.env` dans le dossier `PriceScan-api` :
```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/PriceScan_db
```

##  Test final

Après configuration, testez votre installation :

```bash
# 1. Vérifier la configuration
python -c "from config.database_config import validate_database_config; validate_database_config()"

# 2. Démarrer l'API
python app.py

# 3. Tester l'endpoint de santé
curl http://localhost:5000/health
```

## 🆘 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs de votre base de données
2. Vérifiez que le service est démarré
3. Vérifiez les paramètres de connexion (host, port, utilisateur, mot de passe)
4. Consultez la documentation officielle de votre base de données

---

**Note :** Ce guide couvre les configurations les plus courantes. Pour des configurations avancées ou des environnements de production, consultez la documentation officielle de chaque base de données.
