#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test de connexion MySQL avec XAMPP
"""

import pymysql
from config.database_config import SQL_DB_URL

def test_mysql_connection():
    """Test de connexion à la base de données MySQL"""
    try:
        print(" Test de connexion MySQL...")
        print(f"URL de connexion: {SQL_DB_URL}")
        
        # Extraire les informations de connexion
        if SQL_DB_URL.startswith("mysql+pymysql://"):
            # mysql+pymysql://root:@localhost:3306/PriceScan_db
            parts = SQL_DB_URL.replace("mysql+pymysql://", "").split("@")
            user_pass = parts[0].split(":")
            host_port_db = parts[1].split("/")
            
            user = user_pass[0]
            password = user_pass[1] if len(user_pass) > 1 else ""
            host_port = host_port_db[0].split(":")
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 3306
            database = host_port_db[1]
            
            print(f"Host: {host}")
            print(f"Port: {port}")
            print(f"User: {user}")
            print(f"Password: {'***' if password else '(aucun)'}")
            print(f"Database: {database}")
            
            # Test de connexion
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            print(" Connexion MySQL réussie !")
            
            # Test de requête simple
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f" Version MySQL: {version[0]}")
                
                # Lister les tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f" Tables trouvées: {len(tables)}")
                for table in tables:
                    print(f"   - {table[0]}")
            
            connection.close()
            print(" Test de connexion MySQL terminé avec succès !")
            return True
            
    except Exception as e:
        print(f" Erreur de connexion MySQL: {e}")
        return False

if __name__ == "__main__":
    test_mysql_connection()
