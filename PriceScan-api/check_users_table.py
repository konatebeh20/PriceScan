#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la structure de la table ps_users
"""

import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.database_config import SQL_DB_URL

def check_users_table():
    """Vérifie la structure de la table ps_users"""
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
        
        print(" Vérification de la table ps_users...")
        
        with connection.cursor() as cursor:
            # Vérifier la structure de la table
            cursor.execute("DESCRIBE ps_users")
            columns = cursor.fetchall()
            
            print(f"\n Structure de la table ps_users ({len(columns)} colonnes):")
            for col in columns:
                print(f"   - {col[0]} ({col[1]}) - {col[2]} - {col[3]} - {col[4]} - {col[5]}")
            
            # Vérifier le contenu
            cursor.execute("SELECT COUNT(*) FROM ps_users")
            count = cursor.fetchone()[0]
            print(f"\n👥 Nombre d'utilisateurs: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM ps_users LIMIT 1")
                user = cursor.fetchone()
                print(f"Exemple d'utilisateur: {user}")
        
        connection.close()
        
    except Exception as e:
        print(f" Erreur vérification table: {e}")

if __name__ == "__main__":
    check_users_table()
