# -*- coding: utf-8 -*-
"""
Utilitaires pour le scraping
"""

import requests
import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def fetch_page(url: str, timeout: int = 15) -> Optional[requests.Response]:
    """
    Récupérer une page web avec gestion d'erreurs
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
        
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout pour l'URL: {url}")
        return None
    except requests.exceptions.RequestException as e:
        logger.warning(f"Erreur requête pour {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erreur inattendue pour {url}: {e}")
        return None

def clean_price(price_text: str) -> str:
    """
    Nettoyer et formater le texte de prix
    """
    if not price_text:
        return "Prix non disponible"
    
    # Supprimer les espaces et caractères spéciaux
    cleaned = re.sub(r'[^\d\s,.]', '', price_text.strip())
    
    # Formater le prix
    if cleaned:
        # Ajouter FCFA si pas déjà présent
        if 'FCFA' not in price_text.upper():
            cleaned += ' FCFA'
        return cleaned
    
    return "Prix non disponible"