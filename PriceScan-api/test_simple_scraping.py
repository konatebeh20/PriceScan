#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test Simple du Scraping PriceScan
Test rapide pour vérifier le fonctionnement
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_jumia_scraping():
    """Test du scraping Jumia"""
    print("🧪 Test du scraping Jumia...")
    
    try:
        from helpers.scrapper.jumia import scraper_jumia
        
        # Test avec un produit simple
        results = scraper_jumia("smartphone")
        
        if results:
            print(f"✅ Succès! {len(results)} produits trouvés")
            print(f"📱 Premier produit: {results[0]}")
            return True
        else:
            print("⚠️  Aucun produit trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_auto_scraper():
    """Test de l'AutoScraper"""
    print("\n🤖 Test de l'AutoScraper...")
    
    try:
        from helpers.auto_scraper import AutoScraper
        
        # Créer une instance
        scraper = AutoScraper()
        print("✅ Instance créée")
        
        # Vérifier la configuration
        status = scraper.get_status()
        print(f"📊 Statut: {status['is_running']}")
        print(f"🏪 Magasins: {len(status['stores'])}")
        
        # Afficher les intervalles
        for store_id, store_info in status['stores'].items():
            if store_info['enabled']:
                interval_hours = store_info['interval'] / 3600
                print(f"   🏪 {store_info['name']}: {interval_hours:.1f}h")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test de la configuration"""
    print("\n⚙️  Test de la configuration...")
    
    try:
        from config.scraping_config import SCRAPING_INTERVALS, STORE_CONFIG
        
        print("✅ Configuration chargée")
        print(f"📊 Intervalles: {len(SCRAPING_INTERVALS)} magasins")
        print(f"🏪 Magasins configurés: {len(STORE_CONFIG)}")
        
        # Vérifier Jumia
        if 'jumia' in SCRAPING_INTERVALS:
            jumia_interval = SCRAPING_INTERVALS['jumia']
            jumia_days = jumia_interval / (24 * 3600)
            print(f"   🏪 Jumia: {jumia_days:.1f} jours")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST SIMPLE DU SCRAPING PRICESCAN")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Scraping Jumia", test_jumia_scraping),
        ("AutoScraper", test_auto_scraper)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("🚀 Le scraping est prêt à fonctionner !")
        
        print("\n💡 POUR LANCER EN PRODUCTION:")
        print("   python run_production.py")
        
        print("\n💡 POUR LANCER EN DÉVELOPPEMENT:")
        print("   python app.py")
        
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué")

if __name__ == "__main__":
    main()
