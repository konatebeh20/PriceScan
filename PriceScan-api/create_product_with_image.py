#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer un produit avec une vraie image
"""

import pymysql
import uuid
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.database_config import SQL_DB_URL

def create_product_with_image():
    """Crée un produit avec une vraie image"""
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
        
        with connection.cursor() as cursor:
            # Récupérer la catégorie Électronique
            cursor.execute("SELECT id FROM ps_categories WHERE cat_label = 'Électronique'")
            category_id = cursor.fetchone()[0]
            
            # Récupérer le magasin Carrefour
            cursor.execute("SELECT id FROM ps_stores WHERE store_name = 'Carrefour Côte d''Ivoire'")
            store_id = cursor.fetchone()[0]
            
            # Créer un produit avec une vraie image
            product_name = "Smartphone Samsung Galaxy A54 - Test Image"
            product_image = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop"
            
            cursor.execute("""
                INSERT INTO ps_products (product_uid, product_name, product_description, category_id, product_image)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                product_name,
                "Smartphone Samsung Galaxy A54 avec une vraie image de test",
                category_id,
                product_image
            ))
            
            product_id = cursor.lastrowid
            print(f" Produit créé avec image: {product_name}")
            
            # Créer le prix
            cursor.execute("""
                INSERT INTO ps_prices (price_uid, product_id, store_id, price_amount, price_currency, price_source)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                product_id,
                store_id,
                250000.0,  # 250,000 CFA
                'CFA',
                'test_image'
            ))
            
            print(f" Prix créé: 250,000 CFA")
        
        connection.commit()
        connection.close()
        print(" Produit avec image créé avec succès !")
        
    except Exception as e:
        print(f" Erreur création produit avec image : {e}")

if __name__ == "__main__":
    create_product_with_image()
