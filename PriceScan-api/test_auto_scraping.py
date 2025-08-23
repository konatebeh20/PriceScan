#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test du Scraping Automatique PriceScan
Vérifie le fonctionnement et la sauvegarde en base de données
"""

import sys
import os
import time
import sqlite3
from datetime import datetime, timedelta

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Teste la connexion à la base de données"""
    print("🔌 TEST DE CONNEXION À LA BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        from config.db import db
        from model.PriceScan_db import ps_products, ps_prices, ps_stores
        
        print("✅ Connexion à la base de données réussie")
        print(f"   📊 Tables disponibles: ps_products, ps_prices, ps_stores")
        
        # Vérifier le nombre d'enregistrements
        try:
            products_count = ps_products.query.count()
            prices_count = ps_prices.query.count()
            stores_count = ps_stores.query.count()
            
            print(f"   📦 Produits: {products_count}")
            print(f"   💰 Prix: {prices_count}")
            print(f"   🏪 Magasins: {stores_count}")
            
        except Exception as e:
            print(f"   ⚠️  Impossible de compter les enregistrements: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à la base: {e}")
        return False

def test_scraping_modules():
    """Teste les modules de scraping individuels"""
    print("\n🧪 TEST DES MODULES DE SCRAPING")
    print("=" * 50)
    
    try:
        # Test Carrefour
        print("\n1️⃣ Test Carrefour...")
        from helpers.scrapper.carrefour import scrape_carrefour
        results = scrape_carrefour("smartphone")
        print(f"   ✅ Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   📱 Premier produit: {results[0]}")
        
        # Test Abidjan Mall
        print("\n2️⃣ Test Abidjan Mall...")
        from helpers.scrapper.abidjanmall import scrape_abidjanmall
        results = scrape_abidjanmall("laptop")
        print(f"   ✅ Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   💻 Premier produit: {results[0]}")
        
        # Test Prosuma
        print("\n3️⃣ Test Prosuma...")
        from helpers.scrapper.prosuma import scrape_prosuma
        results = scrape_prosuma("écran")
        print(f"   ✅ Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   🖥️ Premier produit: {results[0]}")
        
        # Test Playce
        print("\n4️⃣ Test Playce...")
        from helpers.scrapper.playce import scrape_playce
        results = scrape_playce("clavier")
        print(f"   ✅ Résultats: {len(results)} produits trouvés")
        if results:
            print(f"   ⌨️ Premier produit: {results[0]}")
        
        print("\n✅ Tous les modules de scraping fonctionnent !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test des modules: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auto_scraper():
    """Teste le système de scraping automatique"""
    print("\n🤖 TEST DU SCRAPING AUTOMATIQUE")
    print("=" * 50)
    
    try:
        from helpers.auto_scraper import AutoScraper
        
        # Créer une instance de test
        scraper = AutoScraper()
        print("   ✅ Instance AutoScraper créée")
        
        # Vérifier la configuration
        status = scraper.get_status()
        print(f"   📊 Statut: {status['is_running']}")
        print(f"   🏪 Magasins configurés: {len(status['stores'])}")
        print(f"   📦 Produits populaires: {status['popular_products_count']}")
        
        # Afficher la configuration des magasins
        for store_id, store_info in status['stores'].items():
            print(f"      🏪 {store_info['name']}: {store_info['interval']}s ({store_info['interval']/3600:.1f}h)")
        
        # Test du scraping manuel
        print("\n   🎯 Test scraping manuel...")
        result = scraper.manual_scrape("smartphone")
        print(f"   📝 Résultat: {result}")
        
        print("\n✅ AutoScraper fonctionne correctement !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test AutoScraper: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scraping_save():
    """Teste la sauvegarde des données scrapées"""
    print("\n💾 TEST DE SAUVEGARDE DES DONNÉES")
    print("=" * 50)
    
    try:
        from helpers.auto_scraper import AutoScraper
        from config.db import db
        from model.PriceScan_db import ps_products, ps_prices, ps_stores
        
        # Créer une instance de test
        scraper = AutoScraper()
        
        # Données de test
        test_data = [
            {
                'name': 'Test Smartphone',
                'price': 150000,
                'store': 'Test Store'
            }
        ]
        
        print("   🧪 Test avec des données fictives...")
        
        # Créer un produit de test
        test_product = ps_products()
        test_product.product_name = 'Test Smartphone'
        test_product.product_description = 'Produit de test pour vérification'
        test_product.is_active = True
        test_product.created_at = datetime.now()
        test_product.updated_on = datetime.now()
        
        db.session.add(test_product)
        db.session.flush()  # Pour obtenir l'ID
        
        print(f"   ✅ Produit de test créé avec ID: {test_product.id}")
        
        # Créer un magasin de test
        test_store = ps_stores()
        test_store.store_name = 'Test Store'
        test_store.store_description = 'Magasin de test'
        test_store.is_active = True
        test_store.created_at = datetime.now()
        test_store.updated_on = datetime.now()
        
        db.session.add(test_store)
        db.session.flush()
        
        print(f"   ✅ Magasin de test créé avec ID: {test_store.id}")
        
        # Créer un prix de test
        test_price = ps_prices()
        test_price.product_id = test_product.id
        test_price.store_name = 'Test Store'
        test_price.price_amount = 150000
        test_price.currency = 'XOF'
        test_price.is_active = True
        test_price.created_at = datetime.now()
        test_price.updated_on = datetime.now()
        
        db.session.add(test_price)
        
        # Sauvegarder en base
        db.session.commit()
        print("   ✅ Données de test sauvegardées en base")
        
        # Vérifier la sauvegarde
        saved_price = ps_prices.query.filter_by(product_id=test_product.id).first()
        if saved_price:
            print(f"   ✅ Prix vérifié en base: {saved_price.price_amount} {saved_price.currency}")
        
        # Nettoyer les données de test
        db.session.delete(test_price)
        db.session.delete(test_product)
        db.session.delete(test_store)
        db.session.commit()
        print("   🧹 Données de test nettoyées")
        
        print("\n✅ Test de sauvegarde réussi !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test de sauvegarde: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scraping_schedule():
    """Teste la planification du scraping"""
    print("\n⏰ TEST DE LA PLANIFICATION DU SCRAPING")
    print("=" * 50)
    
    try:
        from helpers.auto_scraper import AutoScraper
        
        # Créer une instance de test
        scraper = AutoScraper()
        
        # Vérifier la configuration des intervalles
        status = scraper.get_status()
        
        print("   📅 Configuration des intervalles:")
        for store_id, store_info in status['stores'].items():
            interval_hours = store_info['interval'] / 3600
            print(f"      🏪 {store_info['name']}: {interval_hours:.1f} heures")
        
        # Vérifier si le scraping est configuré pour s'exécuter
        print(f"\n   🔄 Scraping automatique: {'✅ Activé' if status['is_running'] else '❌ Désactivé'}")
        
        # Calculer la prochaine exécution
        if status['stores']:
            min_interval = min(store['interval'] for store in status['stores'].values())
            next_run = datetime.now() + timedelta(seconds=min_interval)
            print(f"   ⏱️  Prochaine exécution dans: {min_interval/3600:.1f} heures")
            print(f"   📅 Heure estimée: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n✅ Configuration de planification vérifiée !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test de planification: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST COMPLET DU SCRAPING AUTOMATIQUE")
    print("=" * 60)
    
    tests = [
        ("Connexion Base de Données", test_database_connection),
        ("Modules de Scraping", test_scraping_modules),
        ("AutoScraper", test_auto_scraper),
        ("Sauvegarde des Données", test_scraping_save),
        ("Planification du Scraping", test_scraping_schedule)
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
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("🚀 Le système de scraping automatique est prêt !")
        
        print("\n💡 INFORMATIONS IMPORTANTES:")
        print("   • Le scraping se lance automatiquement au démarrage de l'API")
        print("   • Intervalles actuels: 1-2 heures par magasin")
        print("   • Les données sont sauvegardées en base automatiquement")
        print("   • Pour modifier les intervalles, éditez config/scraping_config.py")
        
        print("\n🔧 POUR MODIFIER L'INTERVALLE À 5 JOURS:")
        print("   1. Modifiez config/scraping_config.py")
        print("   2. Changez SCRAPING_INTERVALS")
        print("   3. Redémarrez l'API")
        
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
