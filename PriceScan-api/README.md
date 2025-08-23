# 🚀 PRICESCAN-API

**API REST complète pour l'application PriceScan - Scanner de reçus intelligent avec OCR**

## 📋 Description

PriceScan-API est une API Flask robuste qui fournit des services backend pour l'application mobile PriceScan. Elle inclut :

- 🔍 **OCR intelligent** pour l'extraction de données depuis les reçus
- 🗄️ **Gestion des utilisateurs** avec authentification JWT
- 📊 **Stockage et analyse** des données de reçus
- 🔒 **Sécurité avancée** avec validation et rate limiting
- 📱 **API REST** complète pour l'intégration mobile
- 🐳 **Déploiement Docker** prêt pour la production
- 🗄️ **Support multi-bases de données** (MySQL, PostgreSQL, MongoDB, SQLite)

## ✨ Fonctionnalités

### 🔍 OCR et Traitement d'Images
- Extraction automatique des informations de reçus
- Support multi-langues (Français, Anglais)
- Prétraitement d'images pour améliorer la précision OCR
- Validation intelligente des données extraites

### 🗄️ Gestion des Données
- Stockage sécurisé des reçus et utilisateurs
- **Support multi-bases de données** :
  - MySQL (XAMPP, phpMyAdmin)
  - PostgreSQL
  - MongoDB
  - SQLite (développement)
- API REST complète avec documentation Swagger
- Système de cache Redis pour les performances

### 🔒 Sécurité
- Authentification JWT avec refresh tokens
- Validation des données et protection contre les injections
- Rate limiting et protection CORS
- Chiffrement des mots de passe avec bcrypt

### 📊 Monitoring et Performance
- Métriques Prometheus intégrées
- Logs structurés et rotation automatique
- Health checks et endpoints de diagnostic
- Cache intelligent pour optimiser les performances

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- pip
- Git
- **Base de données** : MySQL, PostgreSQL, MongoDB ou SQLite

### Démarrage en 1 minute

#### Windows
```bash
# Double-cliquez sur start.bat
# Ou en ligne de commande :
start.bat
```

#### Linux/Mac
```bash
# Rendez le script exécutable
chmod +x start.sh

# Lancez le script
./start.sh
```

#### Manuel
```bash
# 1. Cloner le projet
git clone <repository-url>
cd PriceScan-api

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer la base de données (voir section ci-dessous)
# 6. Lancer l'API
python3 app.py
```

### 🚀 Installation Automatique (Recommandée)

#### Windows
```cmd
# Double-cliquez sur install_dependencies.bat
# Ou en ligne de commande :
install_dependencies.bat
```

#### Linux/Mac
```bash
# Rendre le script exécutable
chmod +x install_dependencies.sh

# Lancer l'installation
./install_dependencies.sh
```

### 🧪 Test des Dépendances

Après l'installation, vérifiez que tout est correctement installé :

```bash
# Test complet des dépendances
python test_dependencies.py

# Ou test rapide
python -c "import flask, cv2, sqlalchemy; print('✅ Dépendances OK')"
```

## 🗄️ Configuration des Bases de Données

### Configuration Rapide

1. **Ouvrez** `config/database_config.py`
2. **Décommentez** la ligne correspondant à votre environnement :

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

# === SQLITE (développement) ===
# SQL_DB_URL = DATABASE_URI_SQLITE
```

### Bases de Données Supportées

#### 🪟 **XAMPP (Windows)**
- **Configuration par défaut** : `root` sans mot de passe
- **Port** : 3306
- **Base** : `PriceScan_db`

#### 🐧 **phpMyAdmin (Linux)**
- **Root** : `root:souris_123`
- **Utilisateur dédié** : `pricescan:scan123`
- **Port** : 3306

#### 🐘 **PostgreSQL**
- **Utilisateur** : `postgres:Konate%2019`
- **Port** : 5432

#### 🍃 **MongoDB**
- **Utilisateur** : `root:Konate%2019`
- **Port** : 27017

#### 🗃️ **SQLite**
- **Fichier** : `PriceScan.db`
- **Aucune installation requise**

### Test de Configuration

```bash
# Tester votre configuration
python test_database.py

# Ou tester manuellement
python -c "from config.database_config import validate_database_config; validate_database_config()"
```

### Guide Complet

Consultez le guide détaillé : **[DATABASE_SETUP.md](DATABASE_SETUP.md)**

## 🌐 Utilisation

### Accès à l'API
- **API Base URL**: `http://localhost:5000`
- **Documentation Swagger**: `http://localhost:5000/apidocs`
- **Health Check**: `http://localhost:5000/health`

### Endpoints Principaux

#### 🔐 Authentification
```bash
# Inscription
POST /api/auth/register
{
  "username": "user",
  "password": "password123",
  "email": "user@example.com"
}

# Connexion
POST /api/auth/login
{
  "username": "user",
  "password": "password123"
}
```

#### 🏪 Magasins
```bash
# Récupérer tous les magasins
GET /api/stores/all

# Créer un magasin
POST /api/stores/create
{
  "store_name": "Carrefour",
  "store_city": "Abidjan"
}
```

#### 📦 Produits
```bash
# Récupérer tous les produits
GET /api/products/all

# Rechercher des produits
GET /api/products/search?q=riz

# Créer un produit
POST /api/products/create
{
  "product_name": "Riz Basmati",
  "product_brand": "Uncle Ben's"
}
```

#### 💰 Prix et Comparaisons
```bash
# Comparer les prix d'un produit
GET /api/compare/{product_id}

# Récupérer les prix par produit
GET /api/prices/by_product?product_id=1

# Créer un prix
POST /api/prices/create
{
  "product_id": 1,
  "store_id": 1,
  "price_amount": 2500
}
```

#### 📸 Scan de Reçus
```bash
# Upload et scan d'image
POST /api/receipts/scan
{
  "u_uid": "user_uuid",
  "receipt_image": "base64_encoded_image_data"
}
```

#### 📊 Gestion des Reçus
```bash
# Récupérer tous les reçus
GET /api/receipts/all

# Récupérer un reçu spécifique
GET /api/receipts/{id}

# Supprimer un reçu
DELETE /api/receipts/{id}
```

## 🐳 Déploiement Docker

### Démarrage rapide avec Docker Compose
```bash
# Lancer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

### Services inclus
- **API Flask** (port 5000)
- **MySQL** (port 3306)
- **Redis** (port 6379)
- **Nginx** (port 80/443)

## ⚙️ Configuration

### Variables d'Environnement
Copiez `env.example` vers `.env` et configurez :

```env
# Base de données
DATABASE_URL=mysql+pymysql://root:@localhost:3306/PriceScan_db

# Sécurité
SECRET_KEY=votre_cle_secrete_tres_longue
JWT_SECRET_KEY=votre_cle_jwt_secrete

# CORS
CORS_ORIGINS=http://localhost:8101,capacitor://localhost
```

### Base de Données

#### Création de la base
```bash
# MySQL (XAMPP/phpMyAdmin)
# Ouvrez phpMyAdmin et créez la base "PriceScan_db"

# PostgreSQL
createdb PriceScan_db

# MongoDB
mongosh
use PriceScan_db
```

## 🧪 Tests

### Lancement des tests
```bash
# Tests unitaires
pytest

# Avec couverture
pytest --cov=app tests/

# Tests spécifiques
pytest tests/test_api.py -v
```

### Tests d'intégration
```bash
# Test de l'API
curl http://localhost:5000/health

# Test d'authentification
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","email":"test@test.com"}'
```

## 📊 Monitoring

### Métriques Prometheus
- Accès via `http://localhost:9090`
- Métriques automatiques de l'API Flask
- Alertes configurables

### Dashboard Grafana
- Accès via `http://localhost:3000`
- Login: `admin` / `admin`
- Dashboards préconfigurés

### Logs
```bash
# Logs de l'application
tail -f logs/app.log

# Logs Docker
docker-compose logs -f api
```

## 🔧 Maintenance

### Sauvegarde automatique
```bash
# Sauvegarde de la base de données
docker-compose exec backup bash /backup.sh

# Restauration
mysql -u root -p PriceScan_db < backup/PriceScan_YYYYMMDD_HHMMSS.sql
```

### Mise à jour
```bash
# Récupérer les dernières modifications
git pull origin main

# Mettre à jour les dépendances
pip install -r requirements.txt

# Redémarrer l'application
docker-compose restart api
```

## 🆘 Dépannage

### Problèmes courants

#### Port déjà utilisé
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

#### Erreurs de base de données
```bash
# Tester la configuration
python test_database.py

# Vérifier la connexion
python -c "from config.database_config import validate_database_config; validate_database_config()"
```

#### Problèmes de dépendances
```bash
# Nettoyer et réinstaller
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 📚 Documentation

- **Guide complet**: `instructions.txt`
- **Configuration BDD**: `DATABASE_SETUP.md`
- **Variables d'environnement**: `env.example`
- **Déploiement Docker**: `docker-compose.yml`
- **Configuration Nginx**: `nginx/nginx.conf`

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)
- **Email**: support@pricescan.com

## 🎉 Remerciements

- **Flask** - Framework web Python
- **Tesseract** - Moteur OCR
- **Docker** - Conteneurisation
- **Prometheus** - Monitoring
- **Grafana** - Visualisation

---

**Développé par l'équipe PriceScan**

**Version**: 1.0.0

**Dernière mise à jour**: Décembre 2024
