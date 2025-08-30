#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
⚡ Test rapide de la configuration Dashboard ↔ API
Vérifie rapidement que tout est en place
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def quick_test():
    """Test rapide de la configuration"""
    print("⚡ Test rapide de la configuration Dashboard ↔ API")
    print("=" * 50)
    
    # Test 1: Vérifier les imports
    print(" Test 1: Vérification des imports...")
    try:
        from config.db import db
        print("    config.db importé avec succès")
    except ImportError as e:
        print(f"    Erreur import config.db: {e}")
        return False
    
    try:
        from model.PriceScan_db import ps_promotions, ps_user_profiles, ps_dashboard_stats
        print("    Nouveaux modèles importés avec succès")
    except ImportError as e:
        print(f"    Erreur import nouveaux modèles: {e}")
        return False
    
    try:
        from helpers.promo_deals import PromoDealsHelper
        print("    Helper promotions importé avec succès")
    except ImportError as e:
        print(f"    Erreur import helper promotions: {e}")
        return False
    
    try:
        from helpers.dashboard_data import DashboardDataHelper
        print("    Helper dashboard importé avec succès")
    except ImportError as e:
        print(f"    Erreur import helper dashboard: {e}")
        return False
    
    # Test 2: Vérifier la configuration de la base
    print("\n Test 2: Vérification de la configuration base...")
    try:
        from config.database_config import SQL_DB_URL
        print(f"    URL de base configurée: {SQL_DB_URL[:50]}...")
        
        if "mysql" in SQL_DB_URL.lower():
            print("    Configuration MySQL détectée")
        else:
            print("     Configuration non-MySQL détectée")
            
    except ImportError as e:
        print(f"    Erreur import config base: {e}")
        return False
    
    # Test 3: Vérifier les ressources API
    print("\n Test 3: Vérification des ressources API...")
    try:
        from resources.promotions import PromotionsApi
        print("    API Promotions importée avec succès")
    except ImportError as e:
        print(f"    Erreur import API Promotions: {e}")
        return False
    
    try:
        from resources.dashboard import DashboardApi
        print("    API Dashboard importée avec succès")
    except ImportError as e:
        print(f"    Erreur import API Dashboard: {e}")
        return False
    
    # Test 4: Vérifier la structure des modèles
    print("\n Test 4: Vérification de la structure des modèles...")
    try:
        # Vérifier que les modèles ont les bons attributs
        promo_attrs = dir(ps_promotions())
        required_attrs = ['title', 'description', 'discount_type', 'discount_value']
        
        missing_attrs = []
        for attr in required_attrs:
            if not hasattr(ps_promotions(), attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            print(f"    Attributs manquants dans ps_promotions: {missing_attrs}")
            return False
        else:
            print("    Modèle ps_promotions correctement configuré")
            
    except Exception as e:
        print(f"    Erreur vérification modèle promotions: {e}")
        return False
    
    # Test 5: Vérifier les helpers
    print("\n Test 5: Vérification des helpers...")
    try:
        # Vérifier que les helpers ont les bonnes méthodes
        promo_methods = dir(PromoDealsHelper)
        required_methods = ['create_promotion', 'get_active_promotions', 'get_featured_promotions']
        
        missing_methods = []
        for method in required_methods:
            if method not in promo_methods:
                missing_methods.append(method)
        
        if missing_methods:
            print(f"    Méthodes manquantes dans PromoDealsHelper: {missing_methods}")
            return False
        else:
            print("    Helper PromoDealsHelper correctement configuré")
            
    except Exception as e:
        print(f"    Erreur vérification helper promotions: {e}")
        return False
    
    try:
        dashboard_methods = dir(DashboardDataHelper)
        required_methods = ['get_user_dashboard_stats', 'get_user_profile_summary']
        
        missing_methods = []
        for method in required_methods:
            if method not in dashboard_methods:
                missing_methods.append(method)
        
        if missing_methods:
            print(f"    Méthodes manquantes dans DashboardDataHelper: {missing_methods}")
            return False
        else:
            print("    Helper DashboardDataHelper correctement configuré")
            
    except Exception as e:
        print(f"    Erreur vérification helper dashboard: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
    print(" La configuration Dashboard ↔ API est prête")
    print("\n Prochaines étapes:")
    print("   1. Créer les tables: python create_dashboard_tables.py")
    print("   2. Lancer l'API: python app.py")
    print("   3. Tester la communication: python test_dashboard_communication.py")
    
    return True

if __name__ == "__main__":
    success = quick_test()
    if not success:
        print("\n Certains tests ont échoué. Vérifiez la configuration.")
        sys.exit(1)
