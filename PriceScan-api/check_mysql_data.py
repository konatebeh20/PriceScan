#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des données MySQL PriceScan
"""

import pymysql
from config.database_config import SQL_DB_URL

def check_mysql_data():
    """Vérifie les données enregistrées dans MySQL"""
    try:
        # Extraire les informations de connexion
        parts = SQL_DB_URL.replace("mysql+pymysql://", "").split("@")
        user_pass = parts[0].split(":")
        host_port_db = parts[1].split("/")
        
        user = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ""
        host_port = host_port_db[0].split(":")
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 3306
        database = host_port_db[1]
        
        # Connexion à MySQL
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        print(" Vérification des données MySQL PriceScan...")
        
        with connection.cursor() as cursor:
            # 1. Vérifier les magasins
            print("\n🏪 MAGASINS :")
            cursor.execute("SELECT id, store_name, store_city, store_country FROM ps_stores")
            stores = cursor.fetchall()
            for store in stores:
                print(f"   - ID: {store[0]}, Nom: {store[1]}, Ville: {store[2]}, Pays: {store[3]}")
            
            # 2. Vérifier les catégories
            print("\n📂 CATÉGORIES :")
            cursor.execute("SELECT id, cat_label, cat_description FROM ps_categories")
            categories = cursor.fetchall()
            for cat in categories:
                print(f"   - ID: {cat[0]}, Nom: {cat[1]}, Description: {cat[2]}")
            
            # 3. Vérifier les produits
            print("\n📦 PRODUITS :")
            cursor.execute("SELECT id, product_name, category_id FROM ps_products")
            products = cursor.fetchall()
            for prod in products:
                print(f"   - ID: {prod[0]}, Nom: {prod[1]}, Catégorie ID: {prod[2]}")
            
            # 4. Vérifier les prix
            print("\n💰 PRIX :")
            cursor.execute("""
                SELECT p.id, p.price_amount, p.price_currency, p.price_source,
                       pr.product_name, s.store_name
                FROM ps_prices p
                JOIN ps_products pr ON p.product_id = pr.id
                JOIN ps_stores s ON p.store_id = s.id
            """)
            prices = cursor.fetchall()
            for price in prices:
                print(f"   - ID: {price[0]}, Prix: {price[1]} {price[2]}, Source: {price[3]}")
                print(f"     Produit: {price[4]}, Magasin: {price[5]}")
            
            # 5. Statistiques générales
            print("\n STATISTIQUES :")
            cursor.execute("SELECT COUNT(*) FROM ps_stores")
            stores_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ps_categories")
            categories_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ps_products")
            products_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ps_prices")
            prices_count = cursor.fetchone()[0]
            
            print(f"   - Magasins: {stores_count}")
            print(f"   - Catégories: {categories_count}")
            print(f"   - Produits: {products_count}")
            print(f"   - Prix: {prices_count}")
        
        connection.close()
        print("\n Vérification terminée avec succès !")
        
    except Exception as e:
        print(f" Erreur lors de la vérification : {e}")

if __name__ == "__main__":
    check_mysql_data()
