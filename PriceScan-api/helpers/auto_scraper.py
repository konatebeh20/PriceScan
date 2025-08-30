#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 Scraping Automatique PriceScan
Système de lancement automatique du scraping au démarrage de l'API
"""

import threading
import time
import schedule
import logging
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

# Import des modules de scraping
from .scrapper.carrefour import scrape_carrefour
from .scrapper.kedjenou import scrape_kedjenou
from .scrapper.afrikmall import scrape_afrikmall
from .scrapper.bazart import scrape_bazart
from .scrapper.jumia import scrape_jumia

# Import de la base de données
from config.db import db
from model.PriceScan_db import ps_products, ps_prices, ps_stores
from config.scraping_config import SCRAPING_INTERVALS, STORE_CONFIG

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logger/auto_scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoScraper:
    """Gestionnaire de scraping automatique"""
    
    def __init__(self):
        self.is_running = False
        self.scraping_thread = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Configuration des magasins
        self.stores = {
            'carrefour': {
                'scraper': scrape_carrefour,
                'name': 'Carrefour',
                'enabled': STORE_CONFIG['carrefour']['enabled'],
                'interval': SCRAPING_INTERVALS['carrefour'],
                'last_run': None
            },
            'kedjenou': {
                'scraper': scrape_kedjenou,
                'name': 'Kedjenou',
                'enabled': STORE_CONFIG['kedjenou']['enabled'],
                'interval': SCRAPING_INTERVALS['kedjenou'],
                'last_run': None
            },
            'afrikmall': {
                'scraper': scrape_afrikmall,
                'name': 'AfrikMall',
                'enabled': STORE_CONFIG['afrikmall']['enabled'],
                'interval': SCRAPING_INTERVALS['afrikmall'],
                'last_run': None
            },
            'bazart': {
                'scraper': scrape_bazart,
                'name': 'Bazart',
                'enabled': STORE_CONFIG['bazart']['enabled'],
                'interval': SCRAPING_INTERVALS['bazart'],
                'last_run': None
            },
            'jumia': {
                'scraper': scrape_jumia,
                'name': 'Jumia',
                'enabled': STORE_CONFIG['jumia']['enabled'],
                'interval': SCRAPING_INTERVALS['jumia'],
                'last_run': None
            }
        }
        
        # Produits populaires à surveiller
        self.popular_products = [
            'smartphone', 'laptop', 'écran', 'clavier', 'souris',
            'casque', 'enceinte', 'câble', 'chargeur', 'adaptateur',
            'mémoire', 'disque dur', 'processeur', 'carte graphique'
        ]
        
        logger.info("AutoScraper initialisé")
        
        # Tester la disponibilité des magasins
        self.working_stores = self._test_store_availability()
    
    def _test_store_availability(self):
        """Teste la disponibilité des magasins et retourne ceux qui fonctionnent"""
        working_stores = []
        test_product = "test"
        
        for store_id, store_config in self.stores.items():
            if not store_config['enabled']:
                continue
                
            try:
                logger.info(f"Test de disponibilité pour {store_config['name']}...")
                # Test rapide avec timeout réduit
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError(f"Timeout pour {store_config['name']}")
                
                # Test simple de connectivité
                results = store_config['scraper'](test_product)
                if results and len(results) > 0:
                    working_stores.append(store_id)
                    logger.info(f" {store_config['name']} - DISPONIBLE")
                else:
                    logger.warning(f" {store_config['name']} - AUCUN RÉSULTAT")
                    
            except Exception as e:
                logger.warning(f" {store_config['name']} - NON DISPONIBLE: {e}")
                continue
        
        logger.info(f"Magasins disponibles: {[self.stores[s]['name'] for s in working_stores]}")
        return working_stores
    
    def start(self):
        """Démarre le scraping automatique"""
        if self.is_running:
            logger.warning("AutoScraper déjà en cours d'exécution")
            return
        
        self.is_running = True
        self.scraping_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scraping_thread.start()
        
        logger.info("AutoScraper démarré")
        
        # Premier scraping immédiat
        self._run_initial_scraping()
    
    def stop(self):
        """Arrête le scraping automatique"""
        self.is_running = False
        if self.scraping_thread:
            self.scraping_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        logger.info("AutoScraper arrêté")
    
    def _run_initial_scraping(self):
        """Lance le premier scraping au démarrage"""
        logger.info("Lancement du scraping initial...")
        
        # Scraping immédiat des produits populaires sur les magasins disponibles
        if not self.working_stores:
            logger.warning("Aucun magasin disponible - scraping initial annulé")
            return
            
        for product in self.popular_products[:3]:  # Limiter à 3 produits pour démarrer vite
            try:
                # Scraper seulement sur les magasins qui fonctionnent
                all_results = []
                for store_id in self.working_stores:
                    if store_id in self.stores and self.stores[store_id]['enabled']:
                        try:
                            results = self.stores[store_id]['scraper'](product)
                            if results:
                                all_results.extend(results)
                            time.sleep(random.uniform(1, 2))  # Délai réduit
                        except Exception as e:
                            logger.warning(f"Magasin {self.stores[store_id]['name']} non disponible pour {product}: {e}")
                            continue
                
                if all_results:
                    self._save_popular_products_data(all_results, product)
                    logger.info(f"Scraping initial {product} terminé: {len(all_results)} résultats")
                else:
                    logger.info(f"Aucun résultat pour {product} - magasins non disponibles")
                    
            except Exception as e:
                logger.error(f"Erreur scraping initial {product}: {e}")
                continue
    
    def _run_scheduler(self):
        """Boucle principale du planificateur"""
        while self.is_running:
            try:
                # Vérifier les magasins à scraper
                current_time = datetime.now()
                
                for store_id, store_config in self.stores.items():
                    if not store_config['enabled']:
                        continue
                    
                    # Vérifier si c'est le moment de scraper ce magasin
                    if (store_config['last_run'] is None or 
                        (current_time - store_config['last_run']).total_seconds() >= store_config['interval']):
                        
                        logger.info(f"Lancement scraping {store_config['name']}")
                        self._scrape_store(store_id, store_config)
                        store_config['last_run'] = current_time
                
                # Scraping des produits populaires toutes les 4 heures
                if current_time.hour % 4 == 0 and current_time.minute < 10:
                    logger.info("Scraping des produits populaires")
                    self._scrape_popular_products()
                
                # Attendre 1 minute avant la prochaine vérification
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Erreur dans le planificateur: {e}")
                time.sleep(60)
    
    def _scrape_store(self, store_id, store_config):
        """Scrape un magasin spécifique"""
        try:
            # Utiliser le contexte Flask pour accéder à la base de données
            from flask import current_app
            with current_app.app_context():
                # Récupérer les produits de ce magasin depuis la base
                store_products = ps_products.query.join(ps_stores).filter(
                    ps_stores.store_name == store_config['name']
                ).limit(20).all()
                
                if not store_products:
                    logger.info(f"Aucun produit trouvé pour {store_config['name']}")
                    return
                
                # Scraper chaque produit
                for product in store_products:
                    try:
                        results = store_config['scraper'](product.product_name)
                        
                        if results:
                            self._save_scraped_data(results, product, store_config['name'])
                        
                        time.sleep(random.uniform(0.5, 2))  # Délai aléatoire
                        
                    except Exception as e:
                        logger.error(f"Erreur scraping produit {product.product_name}: {e}")
                        continue
                
                logger.info(f"Scraping {store_config['name']} terminé")
                
        except Exception as e:
            logger.error(f"Erreur scraping magasin {store_config['name']}: {e}")
            # Continuer avec les autres magasins
            pass
    
    def _scrape_popular_products(self):
        """Scrape les produits populaires"""
        try:
            for product_name in self.popular_products:
                try:
                    # Scraper sur tous les magasins
                    all_results = []
                    
                    for store_id, store_config in self.stores.items():
                        if store_config['enabled']:
                            try:
                                results = store_config['scraper'](product_name)
                                if results:
                                    all_results.extend(results)
                                time.sleep(random.uniform(1, 3))
                            except Exception as e:
                                logger.error(f"Erreur scraping {store_config['name']} pour {product_name}: {e}"),
                    
                    # Sauvegarder les résultats
                    if all_results:
                        self._save_popular_products_data(all_results, product_name)
                    
                except Exception as e:
                    logger.error(f"Erreur scraping produit populaire {product_name}: {e}")
                    continue
            
            logger.info("Scraping des produits populaires terminé")
            
        except Exception as e:
            logger.error(f"Erreur scraping produits populaires: {e}")
            # Continuer avec les autres produits
            pass
    
    def _scrape_product(self, product_name):
        """Scrape un produit spécifique sur tous les magasins"""
        try:
            all_results = []
            
            for store_id, store_config in self.stores.items():
                if store_config['enabled']:
                    try:
                        results = store_config['scraper'](product_name)
                        if results:
                            all_results.extend(results)
                        time.sleep(random.uniform(0.5, 1.5))
                    except Exception as e:
                        logger.error(f"Erreur scraping {store_config['name']}: {e}")
            
            if all_results:
                self._save_popular_products_data(all_results, product_name)
                logger.info(f"Scraping {product_name} terminé: {len(all_results)} résultats")
            
        except Exception as e:
            logger.error(f"Erreur scraping produit {product_name}: {e}")
            # Continuer avec les autres produits
            pass
    
    def _save_scraped_data(self, results, product, store):
        """Sauvegarde les données scrapées"""
        try:
            # Utiliser le contexte Flask pour accéder à la base de données
            from flask import current_app
            with current_app.app_context():
                for result in results:
                    if not isinstance(result, dict) or 'prix' not in result:
                        logger.warning(f"Format de résultat invalide pour prix: {result}")
                        continue
                    
                    # Extraire le prix et le convertir en nombre
                    try:
                        price_str = result['prix']
                        # Nettoyer le prix (enlever "FCFA", espaces, etc.)
                        price_clean = price_str.replace('FCFA', '').replace(' ', '').replace(',', '')
                        price_amount = float(price_clean)
                    except (ValueError, KeyError):
                        logger.warning(f"Prix invalide: {result.get('prix', 'N/A')}")
                        continue
                        
                    # Vérifier si le prix existe déjà
                    existing_price = ps_prices.query.filter_by(
                        product_id=product.id,
                        store_id=store.id
                    ).first()
                    
                    if existing_price:
                        # Mettre à jour le prix existant
                        existing_price.price_amount = price_amount
                        existing_price.updated_on = datetime.now()
                        db.session.add(existing_price)
                    else:
                        # Créer un nouveau prix
                        new_price = ps_prices()
                        new_price.product_id = product.id
                        new_price.store_id = store.id
                        new_price.price_amount = price_amount
                        new_price.price_currency = 'CFA'  # Franc CFA
                        new_price.price_is_promo = False
                        new_price.price_source = 'scraper'
                        db.session.add(new_price)
                
                db.session.commit()
                logger.info(f"{len(results)} prix sauvegardés pour {product.product_name}")
                
        except Exception as e:
            logger.error(f"Erreur sauvegarde données: {e}")
            if 'db' in locals():
                db.session.rollback()
    
    def _save_popular_products_data(self, results, product_name):
        """Sauvegarde les données des produits populaires"""
        try:
            # Utiliser le contexte Flask pour accéder à la base de données
            from flask import current_app
            with current_app.app_context():
                # Filtrer les résultats valides (ignorer les métadonnées)
                valid_results = []
                for result in results:
                    if isinstance(result, dict) and 'nom' in result and 'prix' in result:
                        # Ajouter le nom du magasin s'il n'est pas présent
                        if 'store' not in result:
                            result['store'] = 'Jumia'  # Par défaut pour Jumia
                        valid_results.append(result)
                    elif isinstance(result, dict) and 'store' in result:
                        # Résultat avec store déjà défini
                        valid_results.append(result)
                    # Ignorer les métadonnées (store, products, status, message)
                
                if not valid_results:
                    logger.info(f"Aucun résultat valide trouvé pour {product_name}")
                    return
                
                # Grouper par magasin
                store_results = {}
                for result in valid_results:
                    store = result.get('store', 'Jumia')
                    if store not in store_results:
                        store_results[store] = []
                    store_results[store].append(result)
                
                # Sauvegarder pour chaque magasin
                for store_name, store_data in store_results.items():
                    # Vérifier si le magasin existe
                    store = ps_stores.query.filter_by(store_name=store_name).first()
                    if not store:
                        # Créer le magasin s'il n'existe pas
                        store = ps_stores()
                        store.store_name = store_name
                        store.store_description = f"Magasin {store_name}"
                        store.is_active = True
                        store.created_at = datetime.now()
                        store.updated_on = datetime.now()
                        db.session.add(store)
                        db.session.flush()  # Pour obtenir l'ID
                    
                    # Sauvegarder les produits et prix
                    for result in store_data:
                        if isinstance(result, dict) and 'nom' in result:
                            # Vérifier si le produit existe
                            product = ps_products.query.filter_by(product_name=result['nom']).first()
                            if not product:
                                # Créer le produit s'il n'existe pas
                                product = ps_products()
                                product.product_name = result['nom']
                                product.product_description = f"Produit trouvé via scraping: {result['nom']}"
                                product.is_active = True
                                product.created_at = datetime.now()
                                product.updated_on = datetime.now()
                                db.session.add(product)
                                db.session.flush()  # Pour obtenir l'ID
                            
                            # Sauvegarder le prix
                            self._save_scraped_data([result], product, store)
                        elif isinstance(result, dict) and 'name' in result:
                            # Format alternatif avec 'name' au lieu de 'nom'
                            product = ps_products.query.filter_by(product_name=result['name']).first()
                            if not product:
                                # Créer le produit s'il n'existe pas
                                product = ps_products()
                                product.product_name = result['name']
                                product.product_description = f"Produit trouvé via scraping: {result['name']}"
                                product.is_active = True
                                product.created_at = datetime.now()
                                product.updated_on = datetime.now()
                                db.session.add(product)
                                db.session.flush()  # Pour obtenir l'ID
                            
                            # Sauvegarder le prix
                            self._save_scraped_data([result], product, store)
                        else:
                            logger.warning(f"Format de résultat invalide pour produit: {result}")
                            continue
                
                logger.info(f"Données sauvegardées pour {product_name}: {len(results)} résultats")
                
        except Exception as e:
            logger.error(f"Erreur sauvegarde produits populaires: {e}")
            if 'db' in locals():
                db.session.rollback()
    
    def get_status(self):
        """Retourne le statut du scraping automatique"""
        return {
            'is_running': self.is_running,
            'stores': {
                store_id: {
                    'name': config['name'],
                    'enabled': config['enabled'],
                    'interval': config['interval'],
                    'last_run': config['last_run'].isoformat() if config['last_run'] else None
                }
                for store_id, config in self.stores.items()
            },
            'popular_products_count': len(self.popular_products)
        }
    
    def manual_scrape(self, product_name=None, store_id=None):
        """Lance un scraping manuel"""
        try:
            if product_name and store_id:
                # Scraping d'un produit spécifique sur un magasin
                if store_id in self.stores:
                    store_config = self.stores[store_id]
                    results = store_config['scraper'](product_name)
                    if results:
                        self._save_scraped_data(results, None, store_config['name'])
                        return f" Scraping manuel terminé: {len(results)} résultats"
                    else:
                        return "ℹ Aucun résultat trouvé"
                else:
                    return " Magasin non trouvé"
            
            elif product_name:
                # Scraping d'un produit sur tous les magasins
                self._scrape_product(product_name)
                return f" Scraping manuel de {product_name} terminé"
            
            else:
                # Scraping de tous les magasins
                for store_id, store_config in self.stores.items():
                    if store_config['enabled']:
                        self._scrape_store(store_id, store_config)
                return " Scraping manuel de tous les magasins terminé"
                
        except Exception as e:
            logger.error(f" Erreur scraping manuel: {e}")
            return f" Erreur: {e}"

# Instance globale
auto_scraper = AutoScraper()

def start_auto_scraper():
    """Démarre le scraping automatique"""
    auto_scraper.start()

def stop_auto_scraper():
    """Arrête le scraping automatique"""
    auto_scraper.stop()

def get_scraper_status():
    """Retourne le statut du scraping"""
    return auto_scraper.get_status()

def manual_scrape(product_name=None, store_id=None):
    """Lance un scraping manuel"""
    return auto_scraper.manual_scrape(product_name, store_id)
