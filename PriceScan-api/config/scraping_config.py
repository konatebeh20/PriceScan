#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
⚙️ Configuration du Scraping Automatique PriceScan
Paramètres configurables pour le système de scraping
"""

import os
from datetime import time

# Configuration générale du scraping
SCRAPING_ENABLED = os.getenv('SCRAPING_ENABLED', 'true').lower() == 'true'
SCRAPING_DEBUG = os.getenv('SCRAPING_DEBUG', 'false').lower() == 'true'

# Configuration des intervalles (en secondes)
# En production: 5 jours (432000 secondes)
# En développement: 1-2 heures
if os.getenv('ENVIRONMENT', 'development').lower() == 'production':
    SCRAPING_INTERVALS = {
        'carrefour': int(os.getenv('SCRAPING_CARREFOUR_INTERVAL', 432000)),      # 5 jours
        'kedjenou': int(os.getenv('SCRAPING_KEDJENOU_INTERVAL', 432000)),        # 5 jours
        'afrikmall': int(os.getenv('SCRAPING_AFRIKMALL_INTERVAL', 432000)),      # 5 jours
        'bazart': int(os.getenv('SCRAPING_BAZART_INTERVAL', 432000)),            # 5 jours
        'jumia': int(os.getenv('SCRAPING_JUMIA_INTERVAL', 432000))               # 5 jours
    }
else:
    SCRAPING_INTERVALS = {
        'carrefour': int(os.getenv('SCRAPING_CARREFOUR_INTERVAL', 3600)),        # 1 heure
        'kedjenou': int(os.getenv('SCRAPING_KEDJENOU_INTERVAL', 3600)),          # 1 heure
        'afrikmall': int(os.getenv('SCRAPING_AFRIKMALL_INTERVAL', 7200)),        # 2 heures
        'bazart': int(os.getenv('SCRAPING_BAZART_INTERVAL', 7200)),              # 2 heures
        'jumia': int(os.getenv('SCRAPING_JUMIA_INTERVAL', 3600))                 # 1 heure
    }

# Configuration des produits populaires
POPULAR_PRODUCTS = [
    'smartphone', 'laptop', 'écran', 'clavier', 'souris',
    'casque', 'enceinte', 'câble', 'chargeur', 'adaptateur',
    'mémoire', 'disque dur', 'processeur', 'carte graphique',
    'imprimante', 'scanner', 'webcam', 'microphone', 'tablette',
    'montre connectée', 'enceinte bluetooth', 'câble hdmi'
]

# Configuration des délais (en secondes)
SCRAPING_DELAYS = {
    'min_delay': float(os.getenv('SCRAPING_MIN_DELAY', 0.5)),
    'max_delay': float(os.getenv('SCRAPING_MAX_DELAY', 3.0)),
    'store_delay': float(os.getenv('SCRAPING_STORE_DELAY', 2.0))
}

# Configuration des timeouts
SCRAPING_TIMEOUTS = {
    'request_timeout': int(os.getenv('SCRAPING_REQUEST_TIMEOUT', 10)),
    'connection_timeout': int(os.getenv('SCRAPING_CONNECTION_TIMEOUT', 5))
}

# Configuration des limites
SCRAPING_LIMITS = {
    'max_products_per_store': int(os.getenv('SCRAPING_MAX_PRODUCTS', 20)),
    'max_workers': int(os.getenv('SCRAPING_MAX_WORKERS', 4)),
    'max_retries': int(os.getenv('SCRAPING_MAX_RETRIES', 3))
}

# Configuration des heures de pointe
PEAK_HOURS = {
    'start': time(9, 0),   # 9h00
    'end': time(18, 0)     # 18h00
}

# Configuration des jours de la semaine
SCRAPING_SCHEDULE = {
    'monday': True,
    'tuesday': True,
    'wednesday': True,
    'thursday': True,
    'friday': True,
    'saturday': True,
    'sunday': False
}

# Configuration des magasins
STORE_CONFIG = {
    'carrefour': {
        'enabled': os.getenv('SCRAPING_CARREFOUR_ENABLED', 'true').lower() == 'true',
        'name': 'Carrefour',
        'url_base': 'https://www.carrefour.ci',
        'search_url': 'https://www.carrefour.ci/recherche?q={query}',
        'selectors': {
            'product_container': '.product-item',
            'product_name': '.product-name',
            'product_price': '.product-price',
            'product_image': '.product-image img'
        }
    },
    'kedjenou': {
        'enabled': os.getenv('SCRAPING_KEDJENOU_ENABLED', 'true').lower() == 'true',
        'name': 'Kedjenou',
        'url_base': 'https://kedjenou.ci',
        'search_url': 'https://kedjenou.ci/recherche?q={query}',
        'selectors': {
            'product_container': '.product-card',
            'product_name': 'h3, h2, .product-name',
            'product_price': '.price, .amount',
            'product_image': 'img'
        }
    },
    'afrikmall': {
        'enabled': os.getenv('SCRAPING_AFRIKMALL_ENABLED', 'true').lower() == 'true',
        'name': 'AfrikMall',
        'url_base': 'https://afrikmall.com',
        'search_url': 'https://afrikmall.com/search?q={query}',
        'selectors': {
            'product_container': '.product-card',
            'product_name': 'h3, h2, .product-name',
            'product_price': '.price, .amount',
            'product_image': 'img'
        }
    },
    'bazart': {
        'enabled': os.getenv('SCRAPING_BAZART_ENABLED', 'true').lower() == 'true',
        'name': 'Bazart',
        'url_base': 'https://bazart.ci',
        'search_url': 'https://bazart.ci/recherche?q={query}',
        'selectors': {
            'product_container': '.product-card',
            'product_name': 'h3, h2, .product-name',
            'product_price': '.price, .amount',
            'product_image': 'img'
        }
    },
    'jumia': {
        'enabled': os.getenv('SCRAPING_JUMIA_ENABLED', 'true').lower() == 'true',
        'name': 'Jumia',
        'url_base': 'https://www.jumia.ci',
        'search_url': 'https://www.jumia.ci/catalog/?q={query}',
        'selectors': {
            'product_container': '.sku',
            'product_name': '.name',
            'product_price': '.price',
            'product_image': '.img'
        }
    }
}

# Configuration des en-têtes HTTP
HTTP_HEADERS = {
    'User-Agent': os.getenv('SCRAPING_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Configuration des logs
LOGGING_CONFIG = {
    'level': os.getenv('SCRAPING_LOG_LEVEL', 'INFO'),
    'file': os.getenv('SCRAPING_LOG_FILE', 'logger/auto_scraper.log'),
    'max_size': int(os.getenv('SCRAPING_LOG_MAX_SIZE', 10 * 1024 * 1024)),  # 10MB
    'backup_count': int(os.getenv('SCRAPING_LOG_BACKUP_COUNT', 5))
}

# Configuration des notifications
NOTIFICATION_CONFIG = {
    'enabled': os.getenv('SCRAPING_NOTIFICATIONS_ENABLED', 'false').lower() == 'true',
    'email': os.getenv('SCRAPING_NOTIFICATION_EMAIL', ''),
    'webhook': os.getenv('SCRAPING_WEBHOOK_URL', ''),
    'telegram_bot_token': os.getenv('SCRAPING_TELEGRAM_BOT_TOKEN', ''),
    'telegram_chat_id': os.getenv('SCRAPING_TELEGRAM_CHAT_ID', '')
}

# Configuration de la base de données
DATABASE_CONFIG = {
    'batch_size': int(os.getenv('SCRAPING_BATCH_SIZE', 100)),
    'commit_interval': int(os.getenv('SCRAPING_COMMIT_INTERVAL', 50)),
    'connection_timeout': int(os.getenv('SCRAPING_DB_TIMEOUT', 30))
}

# Configuration des erreurs et retry
ERROR_CONFIG = {
    'max_consecutive_errors': int(os.getenv('SCRAPING_MAX_CONSECUTIVE_ERRORS', 5)),
    'error_cooldown': int(os.getenv('SCRAPING_ERROR_COOLDOWN', 300)),  # 5 minutes
    'retry_delay': int(os.getenv('SCRAPING_RETRY_DELAY', 60))         # 1 minute
}

def get_store_config(store_id):
    """Retourne la configuration d'un magasin"""
    return STORE_CONFIG.get(store_id, {})

def is_scraping_enabled():
    """Vérifie si le scraping est activé"""
    return SCRAPING_ENABLED

def get_scraping_interval(store_id):
    """Retourne l'intervalle de scraping pour un magasin"""
    return SCRAPING_INTERVALS.get(store_id, 3600)

def get_popular_products():
    """Retourne la liste des produits populaires"""
    return POPULAR_PRODUCTS.copy()

def get_http_headers():
    """Retourne les en-têtes HTTP pour le scraping"""
    return HTTP_HEADERS.copy()

def get_store_selectors(store_id):
    """Retourne les sélecteurs CSS pour un magasin"""
    store_config = get_store_config(store_id)
    return store_config.get('selectors', {})

def is_peak_hour():
    """Vérifie si c'est une heure de pointe"""
    from datetime import datetime
    now = datetime.now().time()
    return PEAK_HOURS['start'] <= now <= PEAK_HOURS['end']

def should_scrape_today():
    """Vérifie si le scraping doit être effectué aujourd'hui"""
    from datetime import datetime
    today = datetime.now().strftime('%A').lower()
    return SCRAPING_SCHEDULE.get(today, True)
