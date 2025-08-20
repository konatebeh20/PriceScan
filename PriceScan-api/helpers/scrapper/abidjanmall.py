from .utils import fetch_page, clean_price

def scrape_abidjanmall(product_name):
    url = f"https://abidjanmall.org/catalogsearch/result/?q={product_name.replace(' ', '+')}"
    soup = fetch_page(url)
    if not soup:
        return []

    results = []
    for product in soup.select(".product-item"):
        try:
            name = product.select_one(".product-item-link").text.strip()
            price = product.select_one(".price").text.strip()
            results.append({"store": "Abidjan Mall", "name": name, "price": clean_price(price)})
        except:
            continue
    return results
