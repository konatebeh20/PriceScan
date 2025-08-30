import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Fonction de Scraping (modifiée pour fonctionner avec des termes de recherche) ---
def scrape_jumia(query):
    """
    Scrape les produits Jumia pour un terme de recherche donné.
    
    Args:
        query (str): Terme de recherche (ex: "smartphone", "laptop")
        
    Returns:
        list: Liste des produits trouvés
    """
    print(f"Recherche Jumia pour : {query}")
    
    try:
        # Construire l'URL de recherche
        search_url = f"https://www.jumia.ci/catalog/?q={query}"
        
        # Ajout d'un User-Agent pour simuler un navigateur et éviter un blocage
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        print(f"Accès à l'URL : {search_url}")
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()  # Vérifie les erreurs HTTP (ex: 404, 503)
        soup = BeautifulSoup(response.text, "html.parser")

        produits = []
        # Le sélecteur CSS est le point le plus fragile. Il pourrait changer.
        items = soup.select("article.prd._fb.col.c-prd")
        
        if not items:
            print("Aucun produit trouvé avec le sélecteur actuel. Le site a peut-être changé ou le contenu est chargé dynamiquement.")
            return []

        print(f"{len(items)} produits trouvés. Extraction des données...")

        for item in items:
            nom = item.select_one("h3.name")
            prix = item.select_one("div.prc")
            img = item.select_one("img.img")

            if nom and prix and img:
                nom_produit = nom.text.strip()
                prix_produit = prix.text.strip()
                # Gère les images qui se chargent plus tard (lazy loading)
                image_url_relative = img.get("data-src") or img.get("src")
                
                image_url_complete = None
                
                if image_url_relative and not image_url_relative.startswith("http"):
                    # On ne concatène pas, on utilise urljoin pour plus de robustesse
                    from urllib.parse import urljoin
                    image_url_complete = urljoin(search_url, image_url_relative)
                else:
                    image_url_complete = image_url_relative

                produits.append({
                    "nom": nom_produit,
                    "prix": prix_produit,
                    "image_url": image_url_complete
                })

        return produits

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion pour {query} : {e}")
        return []
    except Exception as e:
        print(f"Erreur générale pour {query} : {e}")
        return []


# --- Exécution du script (PARTIE CORRIGÉE) ---
if __name__ == "__main__":
    urls = [
        "https://www.jumia.ci/telephone-tablette/",
        "https://www.jumia.ci/electronique/",
        "https://www.jumia.ci/mlp-electromenager/",
        "https://www.jumia.ci/maison-cuisine-jardin/",
        "https://www.jumia.ci/ordinateurs-accessoires-informatique/",
        "https://www.jumia.ci/fashion-mode/", # Virgule manquante ajoutée ici
        "https://www.jumia.ci/epicerie/",
        "https://www.jumia.ci/beaute-hygiene-sante/",
        "https://www.jumia.ci/jardin-plein-air-ferme-ranch/"
    ]
    
    # On crée une liste pour stocker les DataFrames de chaque page
    tous_les_produits_dfs = []

    # On boucle sur la liste d'URLs
    for lien in urls:
        df_page = scraper_jumia(lien)
        if not df_page.empty:
            tous_les_produits_dfs.append(df_page)

    # On combine tous les DataFrames en un seul
    if tous_les_produits_dfs:
        df_final = pd.concat(tous_les_produits_dfs, ignore_index=True)
        
        if not df_final.empty:
            print("\n--- RÉSULTATS COMPLETS AVEC LIENS D'IMAGES ---")
            pd.set_option('display.max_colwidth', None)
            print(df_final)
            print(f"\nTotal de {len(df_final)} produits scrapés sur {len(urls)} catégories.")
            print("--------------------------------------------------\n")
    else:
        print("\nAucun produit n'a pu être scrapé sur l'ensemble des URLs fournies.")