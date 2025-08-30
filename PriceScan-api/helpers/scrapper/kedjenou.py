# -*- coding: utf-8 -*-
"""
Scraper pour Kedjenou Côte d'Ivoire
"""

import requests
from bs4 import BeautifulSoup
from .utils import fetch_page, clean_price
import logging

logger = logging.getLogger(__name__)

def scrape_kedjenou(query):
    """
    Scraper les produits Kedjenou
    """
    try:
        # URL de recherche Kedjenou
        base_url = "https://www.kedjenou.ci"
        search_url = f"{base_url}/recherche?q={query}"
        
        logger.info(f"Recherche Kedjenou pour : {query}")
        logger.info(f"Accès à l'URL : {search_url}")
        
        # Récupérer la page
        response = fetch_page(search_url)
        if not response:
            logger.warning("Impossible de récupérer la page Kedjenou")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Sélecteurs pour les produits
        products = soup.find_all('div', class_='product-card')
        
        if not products:
            logger.warning("Aucun produit trouvé sur Kedjenou")
            return []
        
        logger.info(f"{len(products)} produits trouvés sur Kedjenou")
        
        results = []
        for product in products[:10]:  # Limiter à 10 produits
            try:
                # Extraire les informations du produit
                name_elem = product.find('h3', class_='product-title')
                price_elem = product.find('span', class_='product-price')
                image_elem = product.find('img')
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price = clean_price(price_elem.get_text(strip=True))
                    image_url = image_elem.get('src') if image_elem else ""
                    
                    if name and price:
                        results.append({
                            'nom': name,
                            'prix': price,
                            'image_url': image_url,
                            'store': 'Kedjenou'
                        })
                        
            except Exception as e:
                logger.warning(f"Erreur extraction produit Kedjenou: {e}")
                continue
        
        logger.info(f"Scraping Kedjenou terminé: {len(results)} résultats")
        return results
        
    except Exception as e:
        logger.error(f"Erreur scraping Kedjenou: {e}")
        return []
