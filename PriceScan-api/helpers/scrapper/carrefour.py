# -*- coding: utf-8 -*-
"""
Scraper pour Carrefour Côte d'Ivoire
"""

import requests
from bs4 import BeautifulSoup
from .utils import fetch_page, clean_price
import logging

logger = logging.getLogger(__name__)

def scrape_carrefour(query):
    """
    Scraper les produits Carrefour
    """
    try:
        # URL de recherche Carrefour CI
        base_url = "https://www.carrefour.ci"
        search_url = f"{base_url}/recherche?q={query}"
        
        logger.info(f"Recherche Carrefour pour : {query}")
        logger.info(f"Accès à l'URL : {search_url}")
        
        # Récupérer la page
        response = fetch_page(search_url)
        if not response:
            logger.warning("Impossible de récupérer la page Carrefour")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Sélecteurs pour les produits (à adapter selon la structure réelle)
        products = soup.find_all('div', class_='product-item')
        
        if not products:
            logger.warning("Aucun produit trouvé sur Carrefour")
            return []
        
        logger.info(f"{len(products)} produits trouvés sur Carrefour")
        
        results = []
        for product in products[:10]:  # Limiter à 10 produits
            try:
                # Extraire les informations du produit
                name_elem = product.find('h3', class_='product-name')
                price_elem = product.find('span', class_='price')
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
                            'store': 'Carrefour'
                        })
                        
            except Exception as e:
                logger.warning(f"Erreur extraction produit Carrefour: {e}")
                continue
        
        logger.info(f"Scraping Carrefour terminé: {len(results)} résultats")
        return results
        
    except Exception as e:
        logger.error(f"Erreur scraping Carrefour: {e}")
        return []
