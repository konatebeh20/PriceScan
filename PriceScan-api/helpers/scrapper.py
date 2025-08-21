from flask_restful import Resource
from flask import request

import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from helpers.scrapper.carrefour import scrape_carrefour
from helpers.scrapper.abidjanmall import scrape_abidjanmall
from helpers.scrapper.prosuma import scrape_prosuma
from helpers.scrapper.playce import scrape_playce

from config.db import db
from model.PriceScan_db import *




class ScraperAPI(Resource):
    def get(self):
        product_name = request.args.get("product")
        max_results = request.args.get("max_results", 10, type=int)

        if not product_name:
            return {"response": "error", "message": "Product name required"}, 400


        results = []

        # Scraping parallèle pour plus de rapidité
        results = self.scrape_all_sites_parallel(product_name, max_results)

        # Enregistrer les résultats dans la base de données
        self.save_to_database(results, "scraping_bot")


        return {
            "response": "success", 
            "product": product_name, 
            "results": results,
            "count": len(results)
        }, 200
        
        # results.extend(scrape_carrefour(product_name))
        # results.extend(scrape_abidjanmall(product_name))
        # results.extend(scrape_prosuma(product_name))
        # results.extend(scrape_playce(product_name))

        # return {"response": "success", "product": product_name, "results": results}, 200

    def scrape_all_sites_parallel(self, product_name, max_results):
        """
        Exécuter le scraping sur tous les sites en parallèle
        """
        results = []
        sites = [
            ("carrefour", scrape_carrefour),
            ("abidjanmall", scrape_abidjanmall),
            ("prosuma", scrape_prosuma),
            ("playce", scrape_playce)
        ]
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Lancer tous les scrapers en parallèle
            future_to_site = {
                executor.submit(scraper, product_name, max_results): site_name 
                for site_name, scraper in sites
            }
            
            # Collecter les résultats au fur et à mesure
            for future in as_completed(future_to_site):
                site_name = future_to_site[future]
                try:
                    site_results = future.result()
                    # Ajouter l'identification du site
                    for result in site_results:
                        result["source_site"] = site_name
                    results.extend(site_results)
                except Exception as e:
                    print(f"Error scraping {site_name}: {e}")
        
        # Trier par prix
        results.sort(key=lambda x: x.get("price", float('inf')))
        
        return results[:max_results]

    def save_to_database(self, results, source="scraping_bot"):
        """
        Sauvegarder les résultats du scraping dans la base de données
        """
        try:
            # Trouver l'utilisateur bot pour les soumissions automatiques
            bot_user = ps_users.query.filter_by(username="scraping_bot").first()
            user_id = bot_user.user_id if bot_user else None
            
            for result in results:
                # Vérifier si ce prix existe déjà récemment
                existing = price_submissions.query.filter_by(
                    product_name=result.get("product_name"),
                    store_name=result.get("store_name"),
                    price=result.get("price")
                ).first()
                
                if not existing:
                    submission = price_submissions()
                    submission.user_id = user_id
                    submission.product_name = result.get("product_name")
                    submission.price = result.get("price")
                    submission.store_name = result.get("store_name")
                    submission.source = source
                    submission.submission_date = datetime.now()
                    submission.created_at = datetime.now()
                    submission.is_verified = False  # Les prix scrapés nécessitent vérification
                    
                    db.session.add(submission)
            
            db.session.commit()
            
        except Exception as e:
            print(f"Error saving scraping results to database: {e}")
            db.session.rollback()

class PriceTrendAPI(Resource):
    def get(self):
        """
        API pour obtenir les tendances de prix pour un produit
        """
        product_name = request.args.get("product")
        days = request.args.get("days", 30, type=int)
        
        if not product_name:
            return {"response": "error", "message": "Product name required"}, 400
        
        # Récupérer l'historique des prix pour ce produit
        trends = self.get_price_trends(product_name, days)
        
        return {
            "response": "success",
            "product": product_name,
            "trends": trends,
            "statistics": self.calculate_statistics(trends)
        }, 200
    
    def get_price_trends(self, product_name, days):
        """
        Récupérer l'historique des prix pour un produit
        """
        # Ici vous devriez implémenter la logique pour récupérer
        # les données historiques depuis votre base de données
        # Ceci est un exemple simplifié
        return [
            {"date": "2023-10-01", "price": 10.99, "store": "Carrefour"},
            {"date": "2023-10-05", "price": 9.99, "store": "Carrefour"},
            {"date": "2023-10-10", "price": 8.49, "store": "Prosuma"},
            # ... autres données
        ]
    
    def calculate_statistics(self, trends):
        """
        Calculer les statistiques sur les tendances de prix
        """
        if not trends:
            return {}
        
        prices = [item["price"] for item in trends]
        
        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": sum(prices) / len(prices),
            "price_range": max(prices) - min(prices)
        }

