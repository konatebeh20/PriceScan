#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎛️ API de Contrôle du Scraping Automatique
Gère le démarrage, arrêt et contrôle du scraping
"""

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

# Import du scraping automatique
from helpers.auto_scraper import (
    start_auto_scraper, 
    stop_auto_scraper, 
    get_scraper_status, 
    manual_scrape
)

logger = logging.getLogger(__name__)

class ScraperControlAPI(Resource):
    """API de contrôle du scraping automatique"""
    
    @jwt_required()
    def get(self, route):
        """Récupère le statut du scraping"""
        try:
            if route == "status":
                status = get_scraper_status()
                return {
                    "response": "success",
                    "scraper_status": status
                }, 200
            
            elif route == "stores":
                status = get_scraper_status()
                return {
                    "response": "success",
                    "stores": status.get('stores', {})
                }, 200
            
            else:
                return {"response": "error", "message": "Route invalide"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du statut: {e}")
            return {"response": "error", "message": str(e)}, 500
    
    @jwt_required()
    def post(self, route):
        """Contrôle le scraping automatique"""
        try:
            if route == "start":
                # Démarrer le scraping automatique
                start_auto_scraper()
                return {
                    "response": "success",
                    "message": "Scraping automatique démarré"
                }, 200
            
            elif route == "stop":
                # Arrêter le scraping automatique
                stop_auto_scraper()
                return {
                    "response": "success",
                    "message": "Scraping automatique arrêté"
                }, 200
            
            elif route == "manual":
                # Scraping manuel
                data = request.get_json() or {}
                product_name = data.get('product_name')
                store_id = data.get('store_id')
                
                if not product_name and not store_id:
                    return {
                        "response": "error", 
                        "message": "product_name ou store_id requis"
                    }, 400
                
                result = manual_scrape(product_name, store_id)
                return {
                    "response": "success",
                    "message": result
                }, 200
            
            elif route == "scrape_product":
                # Scraping d'un produit spécifique
                data = request.get_json()
                if not data or 'product_name' not in data:
                    return {
                        "response": "error",
                        "message": "product_name requis"
                    }, 400
                
                result = manual_scrape(product_name=data['product_name'])
                return {
                    "response": "success",
                    "message": result
                }, 200
            
            elif route == "scrape_store":
                # Scraping d'un magasin spécifique
                data = request.get_json()
                if not data or 'store_id' not in data:
                    return {
                        "response": "error",
                        "message": "store_id requis"
                    }, 400
                
                result = manual_scrape(store_id=data['store_id'])
                return {
                    "response": "success",
                    "message": result
                }, 200
            
            else:
                return {"response": "error", "message": "Route invalide"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors du contrôle du scraping: {e}")
            return {"response": "error", "message": str(e)}, 500
    
    @jwt_required()
    def patch(self, route):
        """Met à jour la configuration du scraping"""
        try:
            if route == "config":
                data = request.get_json()
                if not data:
                    return {"response": "error", "message": "Données requises"}, 400
                
                # Ici vous pouvez ajouter la logique pour modifier la configuration
                # Par exemple, activer/désactiver des magasins, changer les intervalles
                
                return {
                    "response": "success",
                    "message": "Configuration mise à jour"
                }, 200
            
            else:
                return {"response": "error", "message": "Route invalide"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la configuration: {e}")
            return {"response": "error", "message": str(e)}, 500

class ScrapingStatsAPI(Resource):
    """API pour les statistiques de scraping"""
    
    @jwt_required()
    def get(self, route):
        """Récupère les statistiques de scraping"""
        try:
            if route == "overview":
                # Statistiques générales
                from config.db import db
                from model.PriceScan_db import ps_prices, ps_products, ps_stores
                from sqlalchemy import func
                
                # Nombre total de prix
                total_prices = db.session.query(func.count(ps_prices.id)).scalar()
                
                # Nombre de produits
                total_products = db.session.query(func.count(ps_products.id)).scalar()
                
                # Nombre de magasins
                total_stores = db.session.query(func.count(ps_stores.id)).scalar()
                
                # Prix mis à jour aujourd'hui
                from datetime import datetime, timedelta
                today = datetime.now().date()
                prices_today = db.session.query(func.count(ps_prices.id)).filter(
                    func.date(ps_prices.updated_on) == today
                ).scalar()
                
                return {
                    "response": "success",
                    "stats": {
                        "total_prices": total_prices,
                        "total_products": total_products,
                        "total_stores": total_stores,
                        "prices_updated_today": prices_today,
                        "scraping_status": get_scraper_status()
                    }
                }, 200
            
            elif route == "recent":
                # Prix récemment mis à jour
                from config.db import db
                from model.PriceScan_db import ps_prices, ps_products
                from sqlalchemy import desc
                
                recent_prices = db.session.query(ps_prices, ps_products.product_name).join(
                    ps_products, ps_prices.product_id == ps_products.id
                ).order_by(desc(ps_prices.updated_on)).limit(10).all()
                
                recent_data = []
                for price, product_name in recent_prices:
                    recent_data.append({
                        "product_name": product_name,
                        "store_name": price.store_name,
                        "price_amount": price.price_amount,
                        "currency": price.currency,
                        "updated_on": price.updated_on.isoformat() if price.updated_on else None
                    })
                
                return {
                    "response": "success",
                    "recent_prices": recent_data
                }, 200
            
            else:
                return {"response": "error", "message": "Route invalide"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {"response": "error", "message": str(e)}, 500
