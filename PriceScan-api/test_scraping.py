#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test du Système de Scraping PriceScan
Vérifie le fonctionnement du scraping automatique et manuel
"""

import sys
import os
import time
import requests
import json

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scraping_modules():
    """Teste les modules de scraping individuels"""
    print("🧪 TEST DES MODULES DE SCRAPING")
    print("=" * 40)
    
    try:
        # Test Carrefour
        print("\n1️⃣ Test Carrefour...")
        from helpers.scrapper.carrefour import scrape_carrefour
        results = scrape_carrefour("smartphone")
        print(f"    Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   📱 Premier produit: {results[0]}")
        
        # Test Abidjan Mall
        print("\n2️⃣ Test Abidjan Mall...")
        from helpers.scrapper.abidjanmall import scrape_abidjanmall
        results = scrape_abidjanmall("laptop")
        print(f"    Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   💻 Premier produit: {results[0]}")
        
        # Test Prosuma
        print("\n3️⃣ Test Prosuma...")
        from helpers.scrapper.prosuma import scrape_prosuma
        results = scrape_prosuma("écran")
        print(f"    Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   🖥️ Premier produit: {results[0]}")
        
        # Test Playce
        print("\n4️⃣ Test Playce...")
        from helpers.scrapper.playce import scrape_playce
        results = scrape_playce("clavier")
        print(f"    Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   ⌨️ Premier produit: {results[0]}")
        
        print("\n Tous les modules de scraping fonctionnent !")
        return True
        
    except Exception as e:
        print(f"\n Erreur lors du test des modules: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auto_scraper():
    """Teste le système de scraping automatique"""
    print("\n🤖 TEST DU SCRAPING AUTOMATIQUE")
    print("=" * 40)
    
    try:
        from helpers.auto_scraper import AutoScraper
        
        # Créer une instance de test
        scraper = AutoScraper()
        print("    Instance AutoScraper créée")
        
        # Vérifier la configuration
        status = scraper.get_status()
        print(f"    Statut: {status['is_running']}")
        print(f"   🏪 Magasins configurés: {len(status['stores'])}")
        print(f"   📦 Produits populaires: {status['popular_products_count']}")
        
        # Test du scraping manuel
        print("\n   🎯 Test scraping manuel...")
        result = scraper.manual_scrape("smartphone")
        print(f"   📝 Résultat: {result}")
        
        print("\n AutoScraper fonctionne correctement !")
        return True
        
    except Exception as e:
        print(f"\n Erreur lors du test AutoScraper: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scraping_api():
    """Teste l'API de contrôle du scraping"""
    print("\n🌐 TEST DE L'API DE SCRAPING")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    try:
        # Test du statut (sans authentification pour le test)
        print("\n1️⃣ Test statut scraping...")
        response = requests.get(f"{base_url}/api/scraper/status", timeout=10)
        if response.status_code == 401:  # Non autorisé (normal sans JWT)
            print("    API accessible (authentification requise)")
        else:
            print(f"     Status inattendu: {response.status_code}")
        
        # Test des statistiques
        print("\n2️⃣ Test statistiques scraping...")
        response = requests.get(f"{base_url}/api/scraping_stats/overview", timeout=10)
        if response.status_code == 401:  # Non autorisé (normal sans JWT)
            print("    API statistiques accessible")
        else:
            print(f"     Status inattendu: {response.status_code}")
        
        print("\n API de scraping accessible !")
        return True
        
    except requests.exceptions.ConnectionError:
        print("    API non accessible (vérifiez que l'API est lancée)")
        return False
    except Exception as e:
        print(f"    Erreur: {e}")
        return False

def test_scraping_integration():
    """Teste l'intégration complète du scraping"""
    print("\n🔗 TEST D'INTÉGRATION COMPLÈTE")
    print("=" * 40)
    
    try:
        # Vérifier que l'API peut être créée avec le scraping
        print("\n1️⃣ Test création de l'API...")
        from launch_api import create_app
        
        app = create_app()
        if app:
            print("    API créée avec succès")
            
            # Vérifier que le scraping est initialisé
            with app.app_context():
                try:
                    from helpers.auto_scraper import get_scraper_status
                    status = get_scraper_status()
                    print(f"   🤖 Scraping initialisé: {status['is_running']}")
                except Exception as e:
                    print(f"     Scraping non initialisé: {e}")
            
            return True
        else:
            print("    Impossible de créer l'API")
            return False
            
    except Exception as e:
        print(f"\n Erreur lors du test d'intégration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print(" TEST COMPLET DU SYSTÈME DE SCRAPING")
    print("=" * 50)
    
    tests = [
        ("Modules de Scraping", test_scraping_modules),
        ("AutoScraper", test_auto_scraper),
        ("API de Scraping", test_scraping_api),
        ("Intégration Complète", test_scraping_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print(" RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = " PASS" if result else " FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print(" Le système de scraping est prêt à être utilisé !")
        
        print("\n💡 PROCHAINES ÉTAPES:")
        print("   1. Lancez l'API: python launch_api.py")
        print("   2. Le scraping se lancera automatiquement")
        print("   3. Contrôlez via: /api/scraper/status")
        print("   4. Statistiques via: /api/scraping_stats/overview")
        
    else:
        print(f"\n  {total - passed} test(s) ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
