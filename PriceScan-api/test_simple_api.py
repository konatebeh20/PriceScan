#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test simple de l'API PriceScan
Vérifie l'accessibilité et teste les endpoints
"""

import requests
import json
import time

def test_api_accessibility():
    """Teste l'accessibilité de l'API"""
    base_url = "http://localhost:5000"
    
    print("🧪 TEST D'ACCESSIBILITÉ DE L'API PRICESCAN")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Test Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("    Health Check OK")
            print(f"    Réponse: {response.json()}")
        else:
            print(f"    Health Check échoué: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("    Impossible de se connecter à l'API")
        print("   💡 L'API n'est pas en cours d'exécution")
        return False
    except Exception as e:
        print(f"    Erreur: {e}")
        return False
    
    # Test 2: Endpoint racine
    print("\n2️⃣ Test Endpoint racine...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("    Endpoint racine OK")
        else:
            print(f"    Endpoint racine échoué: {response.status_code}")
    except Exception as e:
        print(f"    Erreur: {e}")
    
    # Test 3: Test des APIs principales
    print("\n3️⃣ Test des APIs principales...")
    
    apis_to_test = [
        ("/api/users/all", "Users API"),
        ("/api/categories/all", "Categories API"),
        ("/api/products/all", "Products API"),
        ("/api/prices/all", "Prices API"),
        ("/api/receipts/all", "Receipts API"),
        ("/api/stores/all", "Stores API"),
        ("/api/favorite/all", "Favorites API"),
        ("/api/device_tokens/all", "Device Tokens API")
    ]
    
    for endpoint, name in apis_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"    {name} OK")
            elif response.status_code == 404:
                print(f"     {name} - Endpoint non trouvé (normal si pas de données)")
            else:
                print(f"    {name} - Status: {response.status_code}")
        except Exception as e:
            print(f"    {name} - Erreur: {e}")
    
    # Test 4: Test des endpoints spéciaux
    print("\n4️⃣ Test des endpoints spéciaux...")
    
    special_endpoints = [
        ("/api/compare/test123", "Compare Prices"),
        ("/api/search?q=test", "Search Products"),
        ("/api/stats/user/test123", "User Stats")
    ]
    
    for endpoint, name in special_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 404, 400]:
                print(f"    {name} OK (Status: {response.status_code})")
            else:
                print(f"    {name} - Status inattendu: {response.status_code}")
        except Exception as e:
            print(f"    {name} - Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    return True

def show_api_info():
    """Affiche les informations sur l'API"""
    print("\n📡 INFORMATIONS SUR L'API")
    print("=" * 30)
    
    print("📍 URL de base: http://localhost:5000")
    print("🏥 Health Check: http://localhost:5000/health")
    print("📚 Documentation: http://localhost:5000/")
    
    print("\n🔗 Endpoints disponibles:")
    endpoints = [
        "GET  /health                    - Vérification de l'état de l'API",
        "GET  /                          - Page d'accueil",
        "GET  /api/users/{route}         - Gestion des utilisateurs",
        "GET  /api/categories/{route}    - Gestion des catégories",
        "GET  /api/products/{route}      - Gestion des produits",
        "GET  /api/prices/{route}        - Gestion des prix",
        "GET  /api/receipts/{route}      - Gestion des reçus",
        "GET  /api/stores/{route}        - Gestion des magasins",
        "GET  /api/favorite/{route}      - Gestion des favoris",
        "GET  /api/device_tokens/{route} - Gestion des tokens mobiles",
        "GET  /api/compare/{product_id}  - Comparaison des prix",
        "GET  /api/search?q={query}      - Recherche de produits",
        "GET  /api/stats/user/{user_uid} - Statistiques utilisateur"
    ]
    
    for endpoint in endpoints:
        print(f"   {endpoint}")
    
    print("\n📝 Routes disponibles pour chaque API:")
    routes = ["all", "create", "update", "delete", "user", "product", "category", "price", "receipt", "store"]
    print(f"   Routes: {', '.join(routes)}")
    
    print("\n💡 Exemples d'utilisation:")
    print("   http://localhost:5000/api/users/all")
    print("   http://localhost:5000/api/products/create")
    print("   http://localhost:5000/api/prices/compare")

def main():
    """Fonction principale"""
    print(" TEST DE L'API PRICESCAN")
    print("=" * 40)
    
    # Vérifier si l'API est accessible
    if test_api_accessibility():
        print("\n L'API est accessible et fonctionne !")
        show_api_info()
        
        print("\n🌐 Pour tester l'interface web:")
        print("   1. Ouvrez http://localhost:5000 dans votre navigateur")
        print("   2. Utilisez les boutons de test")
        print("   3. Vérifiez les réponses de l'API")
        
    else:
        print("\n L'API n'est pas accessible")
        print("💡 Solutions:")
        print("   1. Vérifiez que l'API est en cours d'exécution")
        print("   2. Lancez: python manage.py dev")
        print("   3. Ou: python manage.py prod")
        print("   4. Vérifiez le port 5000")

if __name__ == "__main__":
    main()
