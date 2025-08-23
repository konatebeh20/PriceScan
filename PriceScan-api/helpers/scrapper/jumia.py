import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Fonction de Scraping (inchangée, elle est correcte) ---
def scraper_jumia(url):
    """
    Scrape les produits d'une page Jumia, corrige les URL des images,
    et retourne un DataFrame pandas.
    """
    print(f"Accès à la page : {url}")
    
    try:
        # Ajout d'un User-Agent pour simuler un navigateur et éviter un blocage
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Vérifie les erreurs HTTP (ex: 404, 503)
        soup = BeautifulSoup(response.text, "html.parser")

        produits = []
        # Le sélecteur CSS est le point le plus fragile. Il pourrait changer.
        items = soup.select("article.prd._fb.col.c-prd")
        
        if not items:
            print("Aucun produit trouvé avec le sélecteur actuel. Le site a peut-être changé ou le contenu est chargé dynamiquement.")
            return pd.DataFrame()

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
                    image_url_complete = urljoin(url, image_url_relative)
                else:
                    image_url_complete = image_url_relative

                produits.append({
                    "nom": nom_produit,
                    "prix": prix_produit,
                    "image_url": image_url_complete
                })

        return pd.DataFrame(produits)

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion pour {url} : {e}")
        return pd.DataFrame()


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