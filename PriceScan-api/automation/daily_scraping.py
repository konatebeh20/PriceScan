#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'automatisation quotidienne pour PriceScan
Exécute le scraping automatiquement et génère des rapports
"""

import schedule
import time
import logging
import sys
import os
from datetime import datetime, timedelta
import json

# Ajouter le chemin pour les imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_scraping.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_daily_scraping():
    """Exécute le scraping quotidien"""
    try:
        logger.info(" Démarrage du scraping quotidien PriceScan")
        
        # Importer et exécuter le scraper intelligent
        from helpers.scrapper.smart_scraper import SmartScraper
        
        scraper = SmartScraper()
        total_products = scraper.run_smart_scraping()
        
        # Générer le rapport
        report = generate_daily_report(total_products)
        
        # Sauvegarder le rapport
        save_report(report)
        
        logger.info(f" Scraping quotidien terminé : {total_products} produits traités")
        return total_products
        
    except Exception as e:
        logger.error(f" Erreur lors du scraping quotidien : {e}")
        return 0

def generate_daily_report(total_products):
    """Génère un rapport quotidien"""
    try:
        from helpers.scrapper.smart_scraper import SmartScraper
        from config.database_config import SQL_DB_URL
        import pymysql
        
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
        
        report = {
            'date': datetime.now().isoformat(),
            'total_products': total_products,
            'statistics': {},
            'stores': [],
            'categories': [],
            'recent_products': []
        }
        
        with connection.cursor() as cursor:
            # Statistiques générales
            cursor.execute("SELECT COUNT(*) FROM ps_stores")
            stores_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ps_categories")
            categories_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ps_products")
            products_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ps_prices")
            prices_count = cursor.fetchone()[0]
            
            report['statistics'] = {
                'stores': stores_count,
                'categories': categories_count,
                'products': products_count,
                'prices': prices_count
            }
            
            # Magasins
            cursor.execute("SELECT store_name, store_city, store_country FROM ps_stores")
            stores = cursor.fetchall()
            report['stores'] = [
                {'name': store[0], 'city': store[1], 'country': store[2]}
                for store in stores
            ]
            
            # Catégories
            cursor.execute("SELECT cat_label, cat_description FROM ps_categories")
            categories = cursor.fetchall()
            report['categories'] = [
                {'name': cat[0], 'description': cat[1]}
                for cat in categories
            ]
            
            # Produits récents (derniers 10)
            cursor.execute("""
                SELECT p.product_name, c.cat_label, s.store_name, pr.price_amount
                FROM ps_products p
                JOIN ps_categories c ON p.category_id = c.id
                JOIN ps_prices pr ON p.id = pr.product_id
                JOIN ps_stores s ON pr.store_id = s.id
                ORDER BY p.id DESC
                LIMIT 10
            """)
            recent_products = cursor.fetchall()
            report['recent_products'] = [
                {
                    'name': prod[0],
                    'category': prod[1],
                    'store': prod[2],
                    'price': prod[3]
                }
                for prod in recent_products
            ]
        
        connection.close()
        return report
        
    except Exception as e:
        logger.error(f" Erreur génération rapport : {e}")
        return {
            'date': datetime.now().isoformat(),
            'error': str(e)
        }

def save_report(report):
    """Sauvegarde le rapport dans un fichier JSON"""
    try:
        # Créer le dossier automation s'il n'existe pas
        os.makedirs('automation/reports', exist_ok=True)
        
        # Nom du fichier avec la date
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'automation/reports/daily_report_{date_str}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f" Rapport sauvegardé : {filename}")
        
    except Exception as e:
        logger.error(f" Erreur sauvegarde rapport : {e}")

def cleanup_old_reports(days_to_keep=30):
    """Nettoie les anciens rapports"""
    try:
        reports_dir = 'automation/reports'
        if not os.path.exists(reports_dir):
            return
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for filename in os.listdir(reports_dir):
            if filename.startswith('daily_report_') and filename.endswith('.json'):
                file_path = os.path.join(reports_dir, filename)
                file_date_str = filename.replace('daily_report_', '').replace('.json', '')
                
                try:
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                    if file_date < cutoff_date:
                        os.remove(file_path)
                        logger.info(f"🗑️ Ancien rapport supprimé : {filename}")
                except ValueError:
                    # Ignorer les fichiers avec des noms incorrects
                    continue
                    
    except Exception as e:
        logger.error(f" Erreur nettoyage rapports : {e}")

def send_notification(message):
    """Envoie une notification (peut être étendue avec email/SMS)"""
    logger.info(f"📢 NOTIFICATION: {message}")

def main():
    """Fonction principale"""
    logger.info(" Démarrage de l'automatisation PriceScan")
    
    # Nettoyer les anciens rapports
    cleanup_old_reports()
    
    # Exécuter le scraping immédiatement
    total_products = run_daily_scraping()
    
    if total_products > 0:
        send_notification(f"Scraping quotidien terminé avec succès : {total_products} produits traités")
    else:
        send_notification("Scraping quotidien terminé mais aucun produit traité")
    
    # Programmer l'exécution quotidienne à 2h du matin
    schedule.every().day.at("02:00").do(run_daily_scraping)
    
    logger.info("⏰ Scraping programmé quotidiennement à 2h00")
    
    # Boucle principale pour maintenir le script actif
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérifier toutes les minutes
    except KeyboardInterrupt:
        logger.info("🛑 Arrêt de l'automatisation")
    except Exception as e:
        logger.error(f" Erreur dans la boucle principale : {e}")

if __name__ == "__main__":
    main()
