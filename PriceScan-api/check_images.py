#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des images et test de scraping d'images
"""

import pymysql
import requests
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.database_config import SQL_DB_URL

def check_images_in_db():
    """Vérifie les images stockées dans la base de données"""
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
        
        print(" Vérification des images dans MySQL...")
        
        with connection.cursor() as cursor:
            # Vérifier les produits avec leurs images
            cursor.execute("""
                SELECT p.id, p.product_name, p.product_image, c.cat_label
                FROM ps_products p
                JOIN ps_categories c ON p.category_id = c.id
            """)
            products = cursor.fetchall()
            
            print(f"\n📦 PRODUITS ET IMAGES ({len(products)} trouvés):")
            for prod in products:
                image_url = prod[2] if prod[2] else "AUCUNE IMAGE"
                print(f"   - ID: {prod[0]}, Nom: {prod[1]}")
                print(f"     Image: {image_url}")
                print(f"     Catégorie: {prod[3]}")
                print()
        
        connection.close()
        
    except Exception as e:
        print(f" Erreur vérification images : {e}")

if __name__ == "__main__":
    check_images_in_db()
