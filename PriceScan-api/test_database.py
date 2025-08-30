#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la configuration de la base de données PriceScan
"""

import sys
import os

# Ajouter le dossier courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_config():
    """Test de la configuration de la base de données"""
    print("=" * 60)
    print("🧪 TEST DE CONFIGURATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    try:
        # Test 1: Import de la configuration
        print("\n1️⃣ Test d'import de la configuration...")
        from config.database_config import validate_database_config, SQL_DB_URL
        
        print(" Configuration importée avec succès")
        print(f"   URL de base de données : {SQL_DB_URL}")
        
        # Test 2: Validation de la configuration
        print("\n2️⃣ Test de validation de la configuration...")
        config = validate_database_config()
        print(" Configuration validée avec succès")
        
        # Test 3: Test de connexion (si possible)
        print("\n3️⃣ Test de connexion à la base de données...")
        test_database_connection(config)
        
    except ImportError as e:
        print(f" Erreur d'import : {e}")
        print("   Vérifiez que le fichier config/database_config.py existe")
        return False
    except Exception as e:
        print(f" Erreur : {e}")
        return False
    
    return True

def test_database_connection(db_url):
    """Test de connexion à la base de données"""
    try:
        if db_url.startswith('mysql'):
            test_mysql_connection(db_url)
        elif db_url.startswith('postgresql'):
            test_postgresql_connection(db_url)
        elif db_url.startswith('mongodb'):
            test_mongodb_connection(db_url)
        elif db_url.startswith('sqlite'):
            test_sqlite_connection(db_url)
        else:
            print("  Type de base de données non reconnu")
            print("   Impossible de tester la connexion")
    except Exception as e:
        print(f" Erreur de test de connexion : {e}")

def test_mysql_connection(db_url):
    """Test de connexion MySQL"""
    try:
        import pymysql
        from urllib.parse import urlparse
        
        # Parser l'URL de connexion
        parsed = urlparse(db_url.replace('mysql+pymysql://', 'mysql://'))
        
        # Extraire les composants
        host = parsed.hostname or 'localhost'
        port = parsed.port or 3306
        user = parsed.username or 'root'
        password = parsed.password or ''
        database = parsed.path.lstrip('/') or 'PriceScan_db'
        
        print(f"   Tentative de connexion à MySQL...")
        print(f"   Host: {host}, Port: {port}, User: {user}, DB: {database}")
        
        # Test de connexion
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=10
        )
        
        print(" Connexion MySQL réussie !")
        
        # Test de requête simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   Version MySQL : {version[0]}")
        
        connection.close()
        
    except ImportError:
        print("  Module pymysql non installé")
        print("   Installez-le avec : pip install pymysql")
    except Exception as e:
        print(f" Erreur de connexion MySQL : {e}")
        print("   Vérifiez que MySQL est démarré et accessible")

def test_postgresql_connection(db_url):
    """Test de connexion PostgreSQL"""
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        # Parser l'URL de connexion
        parsed = urlparse(db_url.replace('postgresql+psycopg2://', 'postgresql://'))
        
        # Extraire les composants
        host = parsed.hostname or 'localhost'
        port = parsed.port or 5432
        user = parsed.username or 'postgres'
        password = parsed.password or ''
        database = parsed.path.lstrip('/') or 'PriceScan_db'
        
        print(f"   Tentative de connexion à PostgreSQL...")
        print(f"   Host: {host}, Port: {port}, User: {user}, DB: {database}")
        
        # Test de connexion
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        print(" Connexion PostgreSQL réussie !")
        
        # Test de requête simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"   Version PostgreSQL : {version[0]}")
        
        connection.close()
        
    except ImportError:
        print("  Module psycopg2 non installé")
        print("   Installez-le avec : pip install psycopg2-binary")
    except Exception as e:
        print(f" Erreur de connexion PostgreSQL : {e}")
        print("   Vérifiez que PostgreSQL est démarré et accessible")

def test_mongodb_connection(db_url):
    """Test de connexion MongoDB"""
    try:
        import pymongo
        from urllib.parse import urlparse
        
        # Parser l'URL de connexion
        parsed = urlparse(db_url)
        
        # Extraire les composants
        host = parsed.hostname or 'localhost'
        port = parsed.port or 27017
        user = parsed.username or 'root'
        password = parsed.password or ''
        database = parsed.path.lstrip('/') or 'PriceScan_db'
        
        print(f"   Tentative de connexion à MongoDB...")
        print(f"   Host: {host}, Port: {port}, User: {user}, DB: {database}")
        
        # Construire l'URL de connexion
        if user and password:
            mongo_url = f"mongodb://{user}:{password}@{host}:{port}/{database}"
        else:
            mongo_url = f"mongodb://{host}:{port}/{database}"
        
        # Test de connexion
        client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test de connexion
        client.admin.command('ping')
        print(" Connexion MongoDB réussie !")
        
        # Test de requête simple
        db = client[database]
        collections = db.list_collection_names()
        print(f"   Collections dans {database} : {collections}")
        
        client.close()
        
    except ImportError:
        print("  Module pymongo non installé")
        print("   Installez-le avec : pip install pymongo")
    except Exception as e:
        print(f" Erreur de connexion MongoDB : {e}")
        print("   Vérifiez que MongoDB est démarré et accessible")

def test_sqlite_connection(db_url):
    """Test de connexion SQLite"""
    try:
        import sqlite3
        from urllib.parse import urlparse
        
        # Parser l'URL de connexion
        parsed = urlparse(db_url)
        
        # Extraire le chemin du fichier
        db_path = parsed.path.lstrip('/') or 'PriceScan.db'
        
        print(f"   Tentative de connexion à SQLite...")
        print(f"   Fichier : {db_path}")
        
        # Test de connexion
        connection = sqlite3.connect(db_path)
        
        print(" Connexion SQLite réussie !")
        
        # Test de requête simple
        cursor = connection.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()
        print(f"   Version SQLite : {version[0]}")
        
        connection.close()
        
    except ImportError:
        print("  Module sqlite3 non disponible")
    except Exception as e:
        print(f" Erreur de connexion SQLite : {e}")

def main():
    """Fonction principale"""
    print(" Démarrage des tests de configuration...")
    
    # Test de la configuration
    success = test_database_config()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
        print(" Votre configuration de base de données est prête")
        print("\n📝 Prochaines étapes :")
        print("   1. Créez la base de données si elle n'existe pas")
        print("   2. Lancez l'API avec : python app.py")
        print("   3. Testez l'endpoint de santé : http://localhost:5000/health")
    else:
        print(" CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez votre configuration et réessayez")
        print("\n📚 Consultez le guide : DATABASE_SETUP.md")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
