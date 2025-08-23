import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None
    except Exception as e:
        print(f"Erreur fetch {url}: {e}")
        return None

def clean_price(price_str):
    try:
        return float(price_str.replace("F", "").replace("CFA", "").replace(",", "").strip())
    except:
        return None

def scrape_carrefour(product_name=None, max_results=10):
    """
    Fonction de scraping pour Carrefour
    """
    try:
        # Placeholder pour le scraping Carrefour
        return {
            "store": "Carrefour",
            "products": [],
            "status": "success",
            "message": "Scraping Carrefour en cours de développement"
        }
    except Exception as e:
        return {
            "store": "Carrefour",
            "products": [],
            "status": "error",
            "message": str(e)
        }
