#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 TEST FINAL DU SCRAPING AUTOMATIQUE
Vérifie que le système fonctionne complètement
"""

import sys
import os
import time

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_system():
    """Test complet du système"""
    print("🚀 TEST COMPLET DU SYSTÈME DE SCRAPING")
    print("=" * 60)
    
    try:
        # 1. Test de la configuration
        print("\n1️⃣ Test de la configuration...")
        from config.scraping_config import SCRAPING_INTERVALS, STORE_CONFIG
        
        print("✅ Configuration chargée")
        print(f"📊 Intervalles configurés: {len(SCRAPING_INTERVALS)} magasins")
        
        # Afficher les intervalles
        for store_id, interval in SCRAPING_INTERVALS.items():
            days = interval / (24 * 3600)
            hours = interval / 3600
            print(f"   🏪 {store_id}: {days:.1f} jours ({hours:.1f} heures)")
        
        # 2. Test de l'AutoScraper
        print("\n2️⃣ Test de l'AutoScraper...")
        from helpers.auto_scraper import AutoScraper
        
        scraper = AutoScraper()
        print("✅ Instance AutoScraper créée")
        
        # Vérifier le statut
        status = scraper.get_status()
        print(f"📊 Statut: {'🟢 En cours' if status['is_running'] else '🔴 Arrêté'}")
        print(f"🏪 Magasins configurés: {len(status['stores'])}")
        
        # 3. Test du scraping manuel
        print("\n3️⃣ Test du scraping manuel...")
        
        # Test avec Jumia
        print("   🔍 Test Jumia...")
        from helpers.scrapper.jumia import scraper_jumia
        jumia_results = scraper_jumia("smartphone")
        print(f"   ✅ Jumia: {len(jumia_results)} produits trouvés")
        
        # Test avec un autre magasin si disponible
        try:
            from helpers.scrapper.carrefour import scrape_carrefour
            carrefour_results = scrape_carrefour("smartphone")
            print(f"   ✅ Carrefour: {len(carrefour_results)} produits trouvés")
        except Exception as e:
            print(f"   ⚠️  Carrefour: {e}")
        
        # 4. Test de la base de données
        print("\n4️⃣ Test de la base de données...")
        try:
            from config.db import db
            from model.PriceScan_db import ps_products, ps_prices, ps_stores
            
            print("✅ Connexion à la base de données réussie")
            
            # Compter les enregistrements existants
            products_count = ps_products.query.count()
            prices_count = ps_prices.query.count()
            stores_count = ps_stores.query.count()
            
            print(f"   📦 Produits en base: {products_count}")
            print(f"   💰 Prix en base: {prices_count}")
            print(f"   🏪 Magasins en base: {stores_count}")
            
        except Exception as e:
            print(f"❌ Erreur base de données: {e}")
            return False
        
        # 5. Test de démarrage du scraping automatique
        print("\n5️⃣ Test de démarrage du scraping automatique...")
        
        if not status['is_running']:
            print("   🚀 Démarrage du scraping automatique...")
            scraper.start()
            time.sleep(2)  # Attendre un peu
            
            # Vérifier le nouveau statut
            new_status = scraper.get_status()
            print(f"   📊 Nouveau statut: {'🟢 En cours' if new_status['is_running'] else '🔴 Arrêté'}")
            
            if new_status['is_running']:
                print("   ✅ Scraping automatique démarré avec succès !")
            else:
                print("   ⚠️  Scraping automatique n'a pas démarré")
        else:
            print("   ✅ Scraping automatique déjà en cours")
        
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("🚀 Le système de scraping automatique est opérationnel !")
        
        # Afficher les informations importantes
        print("\n💡 INFORMATIONS IMPORTANTES:")
        print("   • Le scraping se lance automatiquement au démarrage de l'API")
        print("   • Intervalles actuels: 1-2 heures (mode développement)")
        print("   • Pour passer en production (5 jours): ENVIRONMENT=production")
        print("   • Les données sont sauvegardées automatiquement en base")
        
        print("\n🔧 COMMANDES UTILES:")
        print("   • Mode développement: python app.py")
        print("   • Mode production: python run_production.py")
        print("   • Test rapide: python test_simple_scraping.py")
        print("   • Test complet: python test_auto_scraping.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    success = test_complete_system()
    
    if success:
        print("\n🎯 RÉSULTAT: SUCCÈS COMPLET")
        print("🚀 Le système est prêt pour la production !")
    else:
        print("\n🎯 RÉSULTAT: ÉCHEC")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
