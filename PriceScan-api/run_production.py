#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Lancement de l'API PriceScan en mode Production
Configure et démarre l'API avec le scraping automatique tous les 5 jours
"""

import os
import sys
from dotenv import load_dotenv

def load_production_config():
    """Charge la configuration de production"""
    print("⚙️  Chargement de la configuration de production...")
    
    # Charger le fichier de configuration de production
    config_file = 'config/production.env'
    if os.path.exists(config_file):
        load_dotenv(config_file)
        print(f" Configuration chargée depuis {config_file}")
    else:
        print(f"  Fichier de configuration {config_file} non trouvé")
        print("🔧 Utilisation des valeurs par défaut")
    
    # Vérifier les variables d'environnement
    env_vars = [
        'ENVIRONMENT',
        'SCRAPING_ENABLED',
        'SCRAPING_CARREFOUR_INTERVAL',
        'SCRAPING_ABIDJANMALL_INTERVAL',
        'SCRAPING_PROSUMA_INTERVAL',
        'SCRAPING_PLACE_INTERVAL',
        'SCRAPING_JUMIA_INTERVAL'
    ]
    
    print("\n Configuration actuelle:")
    for var in env_vars:
        value = os.getenv(var, 'Non défini')
        print(f"   {var}: {value}")
    
    # Vérifier les intervalles de scraping
    intervals = {
        'Carrefour': int(os.getenv('SCRAPING_CARREFOUR_INTERVAL', 432000)),
        'Abidjan Mall': int(os.getenv('SCRAPING_ABIDJANMALL_INTERVAL', 432000)),
        'Prosuma': int(os.getenv('SCRAPING_PROSUMA_INTERVAL', 432000)),
        'Playce': int(os.getenv('SCRAPING_PLACE_INTERVAL', 432000)),
        'Jumia': int(os.getenv('SCRAPING_JUMIA_INTERVAL', 432000))
    }
    
    print("\n⏰ Intervalles de scraping configurés:")
    for store, interval in intervals.items():
        days = interval / (24 * 3600)
        hours = interval / 3600
        print(f"   🏪 {store}: {days:.1f} jours ({hours:.1f} heures)")
    
    return True

def start_production_api():
    """Démarre l'API en mode production"""
    print("\n Démarrage de l'API PriceScan en mode production...")
    
    try:
        # Importer et démarrer l'API
        from app import app
        
        print(" API Flask chargée avec succès")
        print("🔧 Configuration de production activée")
        print("🤖 Scraping automatique configuré pour s'exécuter tous les 5 jours")
        
        # Démarrer l'API
        app.run(
            debug=False,  # Désactiver le mode debug en production
            host="0.0.0.0",
            port=int(os.getenv('PORT', 5000)),
            threaded=True
        )
        
    except Exception as e:
        print(f" Erreur lors du démarrage de l'API: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print(" LANCEMENT DE L'API PRICESCAN EN MODE PRODUCTION")
    print("=" * 60)
    
    # Charger la configuration
    if not load_production_config():
        print(" Impossible de charger la configuration")
        sys.exit(1)
    
    # Démarrer l'API
    if not start_production_api():
        print(" Impossible de démarrer l'API")
        sys.exit(1)

if __name__ == "__main__":
    main()
