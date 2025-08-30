#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test de l'API des produits PriceScan
"""

import requests
import json

def test_products_api():
    """Teste l'API des produits"""
    base_url = "http://localhost:5000"
    
    print("🧪 TEST DE L'API DES PRODUITS PRICESCAN")
    print("=" * 50)
    
    # 1. Test de récupération des catégories
    print("\n📂 1. Test de récupération des catégories...")
    try:
        response = requests.get(f"{base_url}/api/categories", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            print(f" {len(categories.get('categories', []))} catégories récupérées")
            for cat in categories.get('categories', [])[:3]:  # Afficher les 3 premières
                print(f"   - {cat.get('cat_label', 'N/A')} (ID: {cat.get('id', 'N/A')})")
        else:
            print(f" Échec: {response.text}")
    except Exception as e:
        print(f" Erreur: {e}")
    
    # 2. Test de récupération des magasins
    print("\n🏪 2. Test de récupération des magasins...")
    try:
        response = requests.get(f"{base_url}/api/stores", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            stores = response.json()
            print(f" {len(stores.get('stores', []))} magasins récupérés")
            for store in stores.get('stores', [])[:3]:  # Afficher les 3 premiers
                print(f"   - {store.get('store_name', 'N/A')} (ID: {store.get('id', 'N/A')})")
        else:
            print(f" Échec: {response.text}")
    except Exception as e:
        print(f" Erreur: {e}")
    
    # 3. Test de récupération des produits
    print("\n📦 3. Test de récupération des produits...")
    try:
        response = requests.get(f"{base_url}/api/products", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            print(f" {len(products.get('products', []))} produits récupérés")
            for product in products.get('products', [])[:3]:  # Afficher les 3 premiers
                print(f"   - {product.get('product_name', 'N/A')} - {product.get('price_amount', 0)} {product.get('price_currency', 'CFA')}")
        else:
            print(f" Échec: {response.text}")
    except Exception as e:
        print(f" Erreur: {e}")
    
    # 4. Test de création d'un produit
    print("\n 4. Test de création d'un produit...")
    
    # D'abord récupérer une catégorie et un magasin
    try:
        cat_response = requests.get(f"{base_url}/api/categories", timeout=10)
        store_response = requests.get(f"{base_url}/api/stores", timeout=10)
        
        if cat_response.status_code == 200 and store_response.status_code == 200:
            categories = cat_response.json().get('categories', [])
            stores = store_response.json().get('stores', [])
            
            if categories and stores:
                category_id = categories[0]['id']
                store_id = stores[0]['id']
                
                product_data = {
                    "product_name": "Produit Test API",
                    "product_description": "Description du produit test",
                    "product_brand": "Marque Test",
                    "product_barcode": "1234567890123",
                    "category_id": category_id,
                    "store_id": store_id,
                    "price_amount": 1500.0,
                    "price_currency": "CFA",
                    "product_image": "https://example.com/image.jpg"
                }
                
                response = requests.post(
                    f"{base_url}/api/products",
                    json=product_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                print(f"Status: {response.status_code}")
                if response.status_code == 201:
                    result = response.json()
                    print(" Produit créé avec succès !")
                    print(f"   ID: {result.get('product', {}).get('id', 'N/A')}")
                    print(f"   Nom: {result.get('product', {}).get('product_name', 'N/A')}")
                    print(f"   Prix: {result.get('product', {}).get('price_amount', 0)} {result.get('product', {}).get('price_currency', 'CFA')}")
                    
                    # Sauvegarder l'ID pour les tests suivants
                    product_id = result.get('product', {}).get('id')
                    
                    # 5. Test de récupération du produit créé
                    print(f"\n 5. Test de récupération du produit {product_id}...")
                    get_response = requests.get(f"{base_url}/api/products/{product_id}", timeout=10)
                    print(f"Status: {get_response.status_code}")
                    if get_response.status_code == 200:
                        print(" Produit récupéré avec succès !")
                    else:
                        print(f" Échec récupération: {get_response.text}")
                    
                    # 6. Test de mise à jour du produit
                    print(f"\n✏️ 6. Test de mise à jour du produit {product_id}...")
                    update_data = {
                        "product_name": "Produit Test API - Modifié",
                        "price_amount": 2000.0
                    }
                    update_response = requests.put(
                        f"{base_url}/api/products/{product_id}",
                        json=update_data,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    print(f"Status: {update_response.status_code}")
                    if update_response.status_code == 200:
                        print(" Produit mis à jour avec succès !")
                    else:
                        print(f" Échec mise à jour: {update_response.text}")
                    
                    # 7. Test de suppression du produit
                    print(f"\n🗑️ 7. Test de suppression du produit {product_id}...")
                    delete_response = requests.delete(f"{base_url}/api/products/{product_id}", timeout=10)
                    print(f"Status: {delete_response.status_code}")
                    if delete_response.status_code == 200:
                        print(" Produit supprimé avec succès !")
                    else:
                        print(f" Échec suppression: {delete_response.text}")
                    
                else:
                    print(f" Échec création: {response.text}")
            else:
                print(" Aucune catégorie ou magasin trouvé pour le test")
        else:
            print(" Impossible de récupérer catégories ou magasins")
            
    except Exception as e:
        print(f" Erreur lors du test de création: {e}")

if __name__ == "__main__":
    test_products_api()
