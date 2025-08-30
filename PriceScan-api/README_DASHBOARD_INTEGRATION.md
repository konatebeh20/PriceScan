#  Intégration Dashboard ↔ API PriceScan

Ce guide explique comment configurer et tester la communication entre le dashboard Angular et l'API PriceScan.

##  Prérequis

-  API PriceScan configurée et fonctionnelle
-  Base de données MySQL (XAMPP) accessible
-  Dashboard Angular compilé et accessible
-  Python 3.7+ avec les dépendances installées

## 🗄️ Configuration de la Base de Données

### 1. Créer les Tables du Dashboard

```bash
cd PriceScan-api
python create_dashboard_tables.py
```

Ce script va :
- Créer les nouvelles tables nécessaires au dashboard
- Insérer des données d'exemple (optionnel)
- Vérifier que toutes les tables sont accessibles

### 2. Vérifier la Configuration

Assurez-vous que dans `config/database_config.py` :
```python
# === WINDOWS + XAMPP ===
SQL_DB_URL = DATABASE_URI_XAMPP
```

## 🔧 Démarrage de l'API

### 1. Activer l'Environnement Virtuel

**Windows PowerShell :**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt :**
```cmd
venv\Scripts\activate.bat
```

### 2. Lancer l'API

```bash
python app.py
```

L'API sera accessible sur : `http://localhost:5000`

## 🧪 Tests de Communication

### 1. Test de Santé de l'API

```bash
python test_dashboard_communication.py
```

Ce script teste :
-  Connexion à l'API
-  Endpoints des promotions
-  Endpoints du dashboard
-  Endpoints des reçus, produits, magasins
-  Création et récupération de données
-  Intégration complète

### 2. Test Manuel des Endpoints

**Promotions actives :**
```bash
curl http://localhost:5000/api/promotions/active
```

**Statistiques utilisateur :**
```bash
curl http://localhost:5000/api/dashboard/stats/test-user-123
```

**Profil utilisateur :**
```bash
curl http://localhost:5000/api/dashboard/profile/test-user-123
```

##  Endpoints Disponibles

### 🎯 Promotions
- `GET /api/promotions/active` - Promotions actives
- `GET /api/promotions/featured` - Promotions mises en avant
- `GET /api/promotions/store/{id}` - Promotions d'un magasin
- `GET /api/promotions/product/{id}` - Promotions d'un produit
- `GET /api/promotions/category/{id}` - Promotions d'une catégorie
- `POST /api/promotions/create` - Créer une promotion
- `PATCH /api/promotions/update/{id}` - Mettre à jour une promotion
- `DELETE /api/promotions/delete/{id}` - Supprimer une promotion

###  Dashboard
- `GET /api/dashboard/stats/{user_uid}` - Statistiques utilisateur
- `GET /api/dashboard/profile/{user_uid}` - Profil utilisateur
- `GET /api/dashboard/activity/{user_uid}` - Activité récente
- `GET /api/dashboard/monthly/{user_uid}/{month}/{year}` - Stats mensuelles
- `POST /api/dashboard/profile/update/{user_uid}` - Mettre à jour le profil

### 🧾 Reçus
- `GET /api/receipts/all` - Tous les reçus
- `POST /api/receipts/create` - Créer un reçu
- `PATCH /api/receipts/update/{id}` - Mettre à jour un reçu
- `DELETE /api/receipts/delete/{id}` - Supprimer un reçu

### 📦 Produits
- `GET /api/products/all` - Tous les produits
- `POST /api/products/create` - Créer un produit
- `PATCH /api/products/update/{id}` - Mettre à jour un produit
- `DELETE /api/products/delete/{id}` - Supprimer un produit

### 🏪 Magasins
- `GET /api/stores/all` - Tous les magasins
- `POST /api/stores/create` - Créer un magasin
- `PATCH /api/stores/update/{id}` - Mettre à jour un magasin
- `DELETE /api/stores/delete/{id}` - Supprimer un magasin

### 🏷️ Catégories
- `GET /api/categories/all` - Toutes les catégories
- `POST /api/categories/create` - Créer une catégorie
- `PATCH /api/categories/update/{id}` - Mettre à jour une catégorie
- `DELETE /api/categories/delete/{id}` - Supprimer une catégorie

## 🔗 Intégration avec le Dashboard Angular

### 1. Configuration du Proxy

Le dashboard Angular est configuré pour rediriger les appels API vers `http://localhost:5000` via le fichier `proxy.conf.json`.

### 2. Services Angular

Les services du dashboard utilisent ces endpoints pour :
-  Récupérer les statistiques utilisateur
- 🎯 Afficher les promotions actives
- 🧾 Gérer les reçus scannés
- 📦 Gérer les produits
- 🏪 Gérer les magasins
- 🏷️ Gérer les catégories

### 3. Communication en Temps Réel

Le dashboard peut :
-  Enregistrer de nouveaux reçus
-  Mettre à jour les profils utilisateur
-  Créer des produits et magasins
-  Récupérer les statistiques en temps réel
-  Afficher les promotions actives

##  Démarrage Complet

### 1. Démarrer XAMPP
- Apache : 
- MySQL : 

### 2. Créer les Tables
```bash
cd PriceScan-api
python create_dashboard_tables.py
```

### 3. Lancer l'API
```bash
python app.py
```

### 4. Tester la Communication
```bash
python test_dashboard_communication.py
```

### 5. Lancer le Dashboard
```bash
cd ../PriceScan-dashboard/PriceScan-dashboard/TicketScan-dashboard
ng serve
```

##  Dépannage

### Problème de Connexion à la Base
- Vérifiez que XAMPP est démarré
- Vérifiez la configuration dans `database_config.py`
- Testez avec `python test_database.py`

### Problème de Communication API
- Vérifiez que l'API est lancée sur le port 5000
- Vérifiez les logs de l'API
- Testez avec `python test_dashboard_communication.py`

### Problème de CORS
- L'API est configurée avec CORS activé
- Vérifiez que le proxy Angular est correctement configuré

## 📈 Fonctionnalités Avancées

### 🎯 Promotions Intelligentes
- Calcul automatique des réductions
- Gestion des dates de validité
- Filtrage par magasin/produit/catégorie

###  Statistiques en Temps Réel
- Agrégation automatique des données
- Calcul des tendances mensuelles
- Historique des achats

### 🔔 Notifications
- Alertes de prix
- Notifications de promotions
- Rappels de reçus

## 🎉 Résultat

Une fois configuré, vous aurez :
-  Dashboard Angular fonctionnel
-  API backend complète
-  Base de données avec toutes les tables
-  Communication bidirectionnelle
-  Gestion complète des données utilisateur
-  Système de promotions
-  Statistiques en temps réel

Le dashboard peut maintenant enregistrer, récupérer et afficher toutes les données nécessaires ! 
