# PriceScan API - Documentation Complète

**Version:** 1.0.0

**Description:** API de comparaison de prix intelligente

**Base URL:** `/api`

**Total des endpoints:** 38

## 📱 APIs Principales

### AUTH
**Base URL:** `/api/auth`

- **login:** `POST` `/api/auth/login` - Connexion utilisateur
- **loginSocial:** `POST` `/api/auth/loginSocial` - Connexion sociale
- **delete_account:** `DELETE` `/api/auth/delete_account` - Suppression de compte

### USERS
**Base URL:** `/api/users`

- **create:** `POST` `/api/users/CreateUsers` - Créer un utilisateur
- **read_single:** `POST` `/api/users/ReadSingleUsers` - Lire un utilisateur
- **read_all:** `GET` `/api/users/ReadUsers` - Lire tous les utilisateurs
- **update:** `PATCH` `/api/users/UpdateUsers` - Mettre à jour un utilisateur
- **update_password:** `PATCH` `/api/users/updatepassword` - Mettre à jour le mot de passe
- **verify:** `POST` `/api/users/VerifyUser` - Vérifier un utilisateur
- **delete:** `DELETE` `/api/users/DeleteUsers` - Supprimer un utilisateur

### CATEGORIES
**Base URL:** `/api/categories`

- **crud:** `ALL` `/api/categories/<route>` - CRUD complet des catégories

### STORES
**Base URL:** `/api/stores`

- **crud:** `ALL` `/api/stores/<route>` - CRUD complet des magasins

### PRODUCTS
**Base URL:** `/api/products`

- **crud:** `ALL` `/api/products/<route>` - CRUD complet des produits

### PRICES
**Base URL:** `/api/prices`

- **crud:** `ALL` `/api/prices/<route>` - CRUD complet des prix

### RECEIPTS
**Base URL:** `/api/receipts`

- **crud:** `ALL` `/api/receipts/<route>` - CRUD complet des reçus

### FAVORITES
**Base URL:** `/api/favorite`

- **create:** `POST` `/api/favorite/createFavorite` - Créer un favori
- **read_single:** `POST` `/api/favorite/readSingleFavorite` - Lire un favori
- **read_by_user:** `POST` `/api/favorite/readFavoriteUsers` - Lire les favoris d'un utilisateur
- **read_all:** `GET` `/api/favorite/readAllFavorite` - Lire tous les favoris
- **update:** `PATCH` `/api/favorite/updateFavorite` - Mettre à jour un favori
- **delete:** `DELETE` `/api/favorite/deleteFavorite` - Supprimer un favori

### NOTIFICATIONS
**Base URL:** `/api/notifications`

- **read_all:** `GET` `/api/notifications/readallnotification` - Lire toutes les notifications
- **create:** `POST` `/api/notifications/createnotification` - Créer une notification
- **read_single:** `POST` `/api/notifications/readsinglenotification` - Lire une notification
- **delete:** `DELETE` `/api/notifications/deletenotification` - Supprimer une notification

### DEVICE_TOKENS
**Base URL:** `/api/device_tokens`

- **crud:** `ALL` `/api/device_tokens/<route>` - CRUD complet des tokens d'appareil

### SCRAPER_CONTROL
**Base URL:** `/api/scraper`

- **status:** `GET` `/api/scraper/status` - Statut du scraping
- **stores:** `GET` `/api/scraper/stores` - Statut des magasins
- **start:** `POST` `/api/scraper/start` - Démarrer le scraping
- **stop:** `POST` `/api/scraper/stop` - Arrêter le scraping
- **manual:** `POST` `/api/scraper/manual` - Scraping manuel
- **scrape_product:** `POST` `/api/scraper/scrape_product` - Scraper un produit

### SCRAPING_STATS
**Base URL:** `/api/scraping_stats`

- **general:** `GET` `/api/scraping_stats/general` - Statistiques générales
- **recent:** `GET` `/api/scraping_stats/recent` - Statistiques récentes

## 🔧 Endpoints Spéciaux

### health
**URL:** `/health`
**Méthode:** `GET`
**Description:** Vérification de santé de l'API

### compare_prices
**URL:** `/api/compare/<product_id>`
**Méthode:** `GET`
**Description:** Comparer les prix d'un produit entre magasins

### search_products
**URL:** `/api/search`
**Méthode:** `GET`
**Description:** Rechercher des produits
**Paramètres:** q

### user_stats
**URL:** `/api/stats/user/<user_uid>`
**Méthode:** `GET`
**Description:** Statistiques d'un utilisateur

