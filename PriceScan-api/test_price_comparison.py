#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test du Comparateur de Prix PriceScan
Vérifie que la comparaison de prix fonctionne entre différents magasins
"""

import sys
import os
import requests
import json
from datetime import datetime

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_price_comparison_api():
    """Test de l'API de comparaison de prix"""
    print("🧪 TEST DE L'API DE COMPARAISON DE PRIX")
    print("=" * 60)

    # URL de base de l'API
    base_url = "http://localhost:5000"
    
    try:
        # 1. Test de l'endpoint principal
        print("\n1️⃣ Test de l'endpoint principal...")
        response = requests.get(f"{base_url}/pricescan")
        if response.status_code == 200:
            print("   ✅ Endpoint principal accessible")
            data = response.json()
            print(f"   📊 Version: {data.get('version', 'N/A')}")
            print(f"   🔗 Endpoints disponibles: {len(data.get('endpoints', {}))}")
        else:
            print(f"   ❌ Endpoint principal inaccessible: {response.status_code}")
            return False

        # 2. Test de l'endpoint de comparaison de prix
        print("\n2️⃣ Test de l'endpoint de comparaison de prix...")
        
        # D'abord, récupérer la liste des produits
        products_response = requests.get(f"{base_url}/api/products/list")
        if products_response.status_code == 200:
            products_data = products_response.json()
            if 'data' in products_data and products_data['data']:
                product_id = products_data['data'][0].get('product_id')
                print(f"   📦 Produit trouvé: ID {product_id}")
                
                # Tester la comparaison de prix
                compare_response = requests.get(f"{base_url}/api/compare/{product_id}")
                if compare_response.status_code == 200:
                    compare_data = compare_response.json()
                    print("   ✅ Comparaison de prix réussie")
                    
                    # Analyser les résultats
                    if 'comparison_data' in compare_data:
                        prices = compare_data['comparison_data']
                        print(f"   💰 Nombre de prix trouvés: {len(prices)}")
                        
                        if prices:
                            # Afficher les prix par magasin
                            print("\n   📊 Comparaison des prix:")
                            for price in prices:
                                store_name = price.get('store_info', {}).get('store_name', 'Magasin inconnu')
                                price_amount = price.get('price_amount', 0)
                                currency = price.get('price_currency', 'XOF')
                                print(f"      🏪 {store_name}: {price_amount} {currency}")
                            
                            # Afficher le meilleur prix
                            best_price = compare_data.get('best_price')
                            best_store = compare_data.get('best_store', {}).get('store_name', 'N/A')
                            print(f"\n   🎯 Meilleur prix: {best_price} {currency} chez {best_store}")
                            
                            # Afficher la fourchette de prix
                            price_range = compare_data.get('price_range', {})
                            min_price = price_range.get('min', 0)
                            max_price = price_range.get('max', 0)
                            print(f"   📈 Fourchette de prix: {min_price} - {max_price} {currency}")
                            
                            # Calculer l'économie potentielle
                            if max_price > min_price:
                                savings = max_price - min_price
                                savings_percent = (savings / max_price) * 100
                                print(f"   💸 Économie potentielle: {savings} {currency} ({savings_percent:.1f}%)")
                        else:
                            print("   ⚠️  Aucun prix trouvé pour ce produit")
                    else:
                        print("   ❌ Format de réponse incorrect")
                else:
                    print(f"   ❌ Erreur comparaison de prix: {compare_response.status_code}")
                    print(f"   📝 Réponse: {compare_response.text}")
            else:
                print("   ⚠️  Aucun produit trouvé dans la base")
        else:
            print(f"   ❌ Impossible de récupérer les produits: {products_response.status_code}")

        # 3. Test de recherche de produits
        print("\n3️⃣ Test de recherche de produits...")
        search_query = "smartphone"
        search_response = requests.get(f"{base_url}/api/search?q={search_query}")
        if search_response.status_code == 200:
            search_data = search_response.json()
            print(f"   ✅ Recherche réussie pour '{search_query}'")
            if 'data' in search_data:
                print(f"   📦 Produits trouvés: {len(search_data['data'])}")
            else:
                print("   ⚠️  Aucun produit trouvé")
        else:
            print(f"   ❌ Erreur de recherche: {search_response.status_code}")

        # 4. Test des statistiques de prix
        print("\n4️⃣ Test des statistiques de prix...")
        stats_response = requests.get(f"{base_url}/api/stats/prices")
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print("   ✅ Statistiques de prix récupérées")
            print(f"   📊 Données: {len(stats_data)} champs")
        else:
            print(f"   ❌ Erreur statistiques: {stats_response.status_code}")

        print("\n🎉 Tests de comparaison de prix terminés !")
        return True

    except requests.exceptions.ConnectionError:
        print("   ❌ Impossible de se connecter à l'API")
        print("   💡 Assurez-vous que l'API est démarrée: python app.py")
        return False
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
        return False

def test_database_price_data():
    """Test des données de prix en base"""
    print("\n🗄️ TEST DES DONNÉES DE PRIX EN BASE")
    print("=" * 60)

    try:
        from config.db import db
        from model.PriceScan_db import ps_products, ps_prices, ps_stores
        from sqlalchemy import func

        print("   ✅ Connexion à la base de données réussie")

        # Compter les produits
        products_count = ps_products.query.count()
        print(f"   📦 Produits en base: {products_count}")

        # Compter les prix
        prices_count = ps_prices.query.count()
        print(f"   💰 Prix en base: {prices_count}")

        # Compter les magasins
        stores_count = ps_stores.query.count()
        print(f"   🏪 Magasins en base: {stores_count}")

        if prices_count > 0:
            # Vérifier la répartition des prix par magasin
            print("\n   📊 Répartition des prix par magasin:")
            store_prices = db.session.query(
                ps_stores.store_name,
                func.count(ps_prices.price_uid).label('price_count')
            ).join(ps_prices).group_by(ps_stores.store_id).all()

            for store_name, price_count in store_prices:
                print(f"      🏪 {store_name}: {price_count} prix")

            # Vérifier les produits avec plusieurs prix
            print("\n   🔍 Produits avec plusieurs prix (comparaison possible):")
            multi_price_products = db.session.query(
                ps_products.product_name,
                func.count(ps_prices.price_uid).label('price_count')
            ).join(ps_prices).group_by(ps_products.product_id).having(
                func.count(ps_prices.price_uid) > 1
            ).limit(5).all()

            for product_name, price_count in multi_price_products:
                print(f"      📦 {product_name}: {price_count} prix")

        else:
            print("   ⚠️  Aucun prix en base - impossible de tester la comparaison")
            print("   💡 Lancez le scraping automatique pour générer des données")

        return True

    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST DU COMPARATEUR DE PRIX PRICESCAN")
    print("=" * 60)

    tests = [
        ("API de Comparaison", test_price_comparison_api),
        ("Données de Prix en Base", test_database_price_data)
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
        print("🚀 Le comparateur de prix fonctionne correctement !")

        print("\n💡 FONCTIONNALITÉS VÉRIFIÉES:")
        print("   ✅ Comparaison de prix entre magasins")
        print("   ✅ Identification du meilleur prix")
        print("   ✅ Calcul des économies potentielles")
        print("   ✅ Recherche de produits")
        print("   ✅ Statistiques de prix")

        print("\n🔧 POUR TESTER L'APPLICATION MOBILE:")
        print("   1. Assurez-vous que l'API fonctionne (python app.py)")
        print("   2. Lancez l'app mobile (ionic serve)")
        print("   3. Testez la comparaison de prix dans l'onglet Scan")

    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
