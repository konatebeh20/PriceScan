#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création des tables PriceScan dans MySQL
"""

import pymysql
from config.database_config import SQL_DB_URL

def create_mysql_tables():
    """Créer toutes les tables PriceScan dans MySQL"""
    try:
        print(" Création des tables PriceScan dans MySQL...")
        
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
        
        print(" Connexion MySQL établie")
        
        with connection.cursor() as cursor:
            # Table ps_categories
            print(" Création de la table ps_categories...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cat_uid VARCHAR(128) UNIQUE,
                    cat_label VARCHAR(128) NOT NULL,
                    cat_description TEXT,
                    cat_is_featured BOOLEAN DEFAULT TRUE NOT NULL,
                    cat_is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    cat_banner VARCHAR(256),
                    cat_icon VARCHAR(256) UNIQUE DEFAULT '',
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_on DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
                )
            """)
            print(" Table ps_categories créée")
            
            # Table ps_stores
            print(" Création de la table ps_stores...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_stores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    store_uid VARCHAR(128) UNIQUE,
                    store_name VARCHAR(255) NOT NULL,
                    store_address VARCHAR(255),
                    store_city VARCHAR(128),
                    store_country VARCHAR(128) DEFAULT 'Côte d''Ivoire',
                    store_phone VARCHAR(128),
                    store_email VARCHAR(128),
                    store_website VARCHAR(255),
                    store_logo VARCHAR(255),
                    store_is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_on DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
                )
            """)
            print(" Table ps_stores créée")
            
            # Table ps_products
            print(" Création de la table ps_products...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_uid VARCHAR(128) UNIQUE,
                    product_name VARCHAR(255) NOT NULL,
                    product_description TEXT,
                    product_brand VARCHAR(128),
                    product_barcode VARCHAR(128),
                    category_id INT,
                    product_image VARCHAR(255),
                    product_is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_on DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES ps_categories(id)
                )
            """)
            print(" Table ps_products créée")
            
            # Table ps_prices
            print(" Création de la table ps_prices...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    price_uid VARCHAR(128) UNIQUE,
                    product_id INT NOT NULL,
                    store_id INT NOT NULL,
                    price_amount FLOAT NOT NULL,
                    price_currency VARCHAR(10) DEFAULT 'CFA',
                    price_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    price_is_promo BOOLEAN DEFAULT FALSE,
                    price_promo_end DATETIME,
                    price_source VARCHAR(50) DEFAULT 'manual',
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_on DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES ps_products(id),
                    FOREIGN KEY (store_id) REFERENCES ps_stores(id)
                )
            """)
            print(" Table ps_prices créée")
            
            # Table ps_users
            print(" Création de la table ps_users...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    u_uid VARCHAR(128) UNIQUE,
                    u_username VARCHAR(128) UNIQUE NOT NULL,
                    u_email VARCHAR(128) UNIQUE NOT NULL,
                    u_password VARCHAR(255) NOT NULL,
                    u_firstname VARCHAR(128) NOT NULL,
                    u_lastname VARCHAR(128) NOT NULL,
                    u_status ENUM('ACTIVE', 'INACTIVE', 'BANNED') DEFAULT 'ACTIVE',
                    u_first_login BOOLEAN DEFAULT TRUE,
                    u_account_type ENUM('particulier', 'supermarche', 'pharmacie', 'quincaillerie', 'autre') DEFAULT 'particulier',
                    u_business_name VARCHAR(255),
                    u_business_address TEXT,
                    u_business_location VARCHAR(255),
                    u_phone VARCHAR(128),
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_on DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
                )
            """)
            print(" Table ps_users créée")
            
            # Table ps_scans
            print(" Création de la table ps_scans...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_scans (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    scan_uid VARCHAR(128) UNIQUE,
                    store_id INT NOT NULL,
                    total_amount FLOAT NOT NULL,
                    purchase_date DATETIME NOT NULL,
                    scan_image VARCHAR(256),
                    category_id INT,
                    user_id INT,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_on DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (store_id) REFERENCES ps_stores(id),
                    FOREIGN KEY (category_id) REFERENCES ps_categories(id),
                    FOREIGN KEY (user_id) REFERENCES ps_users(id)
                )
            """)
            print(" Table ps_scans créée")
            
            # Table ps_favorite
            print(" Création de la table ps_favorite...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_favorite (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fav_uid VARCHAR(128) UNIQUE,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES ps_users(id),
                    FOREIGN KEY (product_id) REFERENCES ps_products(id),
                    UNIQUE KEY unique_user_product (user_id, product_id)
                )
            """)
            print(" Table ps_favorite créée")
            
            # Table ps_notification
            print(" Création de la table ps_notification...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_notification (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    notif_uid VARCHAR(128) UNIQUE,
                    user_id INT NOT NULL,
                    notif_title VARCHAR(255) NOT NULL,
                    notif_message TEXT NOT NULL,
                    notif_type ENUM('info', 'success', 'warning', 'error') DEFAULT 'info',
                    notif_is_read BOOLEAN DEFAULT FALSE,
                    notif_data JSON,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES ps_users(id)
                )
            """)
            print(" Table ps_notification créée")
            
            # Table ps_price_alerts
            print(" Création de la table ps_price_alerts...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_price_alerts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alert_uid VARCHAR(128) UNIQUE,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    target_price FLOAT NOT NULL,
                    alert_is_active BOOLEAN DEFAULT TRUE,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES ps_users(id),
                    FOREIGN KEY (product_id) REFERENCES ps_products(id)
                )
            """)
            print(" Table ps_price_alerts créée")
            
            # Table ps_dashboard_stats
            print(" Création de la table ps_dashboard_stats...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_dashboard_stats (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    stats_uid VARCHAR(128) UNIQUE,
                    stat_date DATE NOT NULL,
                    total_scans INT DEFAULT 0,
                    total_products INT DEFAULT 0,
                    total_stores INT DEFAULT 0,
                    total_users INT DEFAULT 0,
                    avg_price_change FLOAT DEFAULT 0,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                )
            """)
            print(" Table ps_dashboard_stats créée")
            
            # Table ps_device_tokens
            print(" Création de la table ps_device_tokens...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_device_tokens (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    token_uid VARCHAR(128) UNIQUE,
                    user_id INT NOT NULL,
                    device_token VARCHAR(255) NOT NULL,
                    device_type ENUM('android', 'ios', 'web') DEFAULT 'web',
                    device_info JSON,
                    is_active BOOLEAN DEFAULT TRUE,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES ps_users(id)
                )
            """)
            print(" Table ps_device_tokens créée")
            
            # Table ps_comparison_history
            print(" Création de la table ps_comparison_history...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ps_comparison_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    comp_uid VARCHAR(128) UNIQUE,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    store_ids JSON NOT NULL,
                    comparison_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    best_price FLOAT NOT NULL,
                    best_store_id INT NOT NULL,
                    price_difference FLOAT DEFAULT 0,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES ps_users(id),
                    FOREIGN KEY (product_id) REFERENCES ps_products(id),
                    FOREIGN KEY (best_store_id) REFERENCES ps_stores(id)
                )
            """)
            print(" Table ps_comparison_history créée")
            
            # Valider les changements
            connection.commit()
            print(" Toutes les tables ont été créées avec succès !")
            
            # Lister les tables créées
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n Tables disponibles: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f" Erreur lors de la création des tables: {e}")
        return False

if __name__ == "__main__":
    create_mysql_tables()
