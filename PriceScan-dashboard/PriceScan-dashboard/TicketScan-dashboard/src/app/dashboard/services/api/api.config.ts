// ========================================
// 🔧 CONFIGURATION DE L'API PRICESCAN
// ========================================
// Configuration mise à jour pour l'API PriceScan locale
// ========================================

export const API_CONFIG = {
  // API PriceScan locale
  BASE_URL: 'http://localhost:5000/api',
  
  // Endpoints du dashboard
  DASHBOARD: {
    STATS: 'http://localhost:5000/api/dashboard/stats',
    PROFILE: 'http://localhost:5000/api/dashboard/profile',
    ACTIVITY: 'http://localhost:5000/api/dashboard/activity',
    RECENT_RECEIPTS: 'http://localhost:5000/api/dashboard/recent-receipts'
  },
  
  // Endpoints des promotions
  PROMOTIONS: {
    BASE: 'http://localhost:5000/api/promotions',
    ACTIVE: 'http://localhost:5000/api/promotions/active',
    FEATURED: 'http://localhost:5000/api/promotions/featured',
    BY_ID: (id: number) => `http://localhost:5000/api/promotions/${id}`
  },
  
  // Endpoints des utilisateurs
  USERS: {
    BASE: 'http://localhost:5000/api/users',
    PROFILE: 'http://localhost:5000/api/users/profile',
    LOGIN: 'http://localhost:5000/api/auth/login',
    REGISTER: 'http://localhost:5000/api/auth/register'
  },
  
  // Endpoints des reçus
  RECEIPTS: {
    BASE: 'http://localhost:5000/api/receipts',
    BY_ID: (id: number) => `http://localhost:5000/api/receipts/${id}`,
    SCAN_HISTORY: 'http://localhost:5000/api/receipts/scan-history'
  },
  
  // Endpoints des produits
  PRODUCTS: {
    BASE: 'http://localhost:5000/api/products',
    BY_ID: (id: number) => `http://localhost:5000/api/products/${id}`,
    SEARCH: (query: string) => `http://localhost:5000/api/products/search?q=${query}`
  },
  
  // Endpoints des magasins
  STORES: {
    BASE: 'http://localhost:5000/api/stores',
    BY_ID: (id: number) => `http://localhost:5000/api/stores/${id}`,
    NEARBY: 'http://localhost:5000/api/stores/nearby'
  },
  
  // Endpoints des catégories
  CATEGORIES: {
    BASE: 'http://localhost:5000/api/categories',
    BY_ID: (id: number) => `http://localhost:5000/api/categories/${id}`,
    FEATURED: 'http://localhost:5000/api/categories/featured'
  },
  
  // Configuration des requêtes
  REQUEST_CONFIG: {
    timeout: 30000,
    retries: 3,
    retryDelay: 1000
  },
  
  // Headers par défaut
  DEFAULT_HEADERS: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
};

export const ENVIRONMENT_CONFIG = {
  development: {
    API_URL: 'http://localhost:5000/api',
    ENABLE_LOGGING: true,
    ENABLE_MOCK_DATA: false
  },
  production: {
    API_URL: 'https://api.pricescan.com/v1',
    ENABLE_LOGGING: false,
    ENABLE_MOCK_DATA: false
  },
  test: {
    API_URL: 'http://localhost:5001/api',
    ENABLE_LOGGING: true,
    ENABLE_MOCK_DATA: true
  }
};

export function getApiConfig() {
  // Pour le moment, utiliser la configuration de développement
  // En production, vous pourriez vérifier process.env.NODE_ENV
  return API_CONFIG;
}

export function getEnvironmentConfig() {
  // Retourner la configuration de développement par défaut
  return ENVIRONMENT_CONFIG.development;
}
