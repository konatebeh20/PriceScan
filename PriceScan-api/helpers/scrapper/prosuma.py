from .utils import fetch_page, clean_price

def scrape_prosuma(product_name):
    url = f"https://groupeprosuma.com/enseigne/cap-nord/?s={product_name.replace(' ', '+')}"
    soup = fetch_page(url)
    if not soup:
        return []

    results = []
    for product in soup.select(".product-wrapper"):  # adapter selon le site
        try:
            name = product.select_one(".product-title").text.strip()
            price = product.select_one(".price").text.strip()
            results.append({"store": "Prosuma", "name": name, "price": clean_price(price)})
        except:
            continue
    return results
