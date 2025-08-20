from flask_restful import Resource
from flask import request

from helpers.scrapper.carrefour import scrape_carrefour
from helpers.scrapper.abidjanmall import scrape_abidjanmall
from helpers.scrapper.prosuma import scrape_prosuma
from helpers.scrapper.playce import scrape_playce

class ScraperAPI(Resource):
    def get(self):
        product_name = request.args.get("product")
        if not product_name:
            return {"response": "error", "message": "Product name required"}, 400

        results = []
        results.extend(scrape_carrefour(product_name))
        results.extend(scrape_abidjanmall(product_name))
        results.extend(scrape_prosuma(product_name))
        results.extend(scrape_playce(product_name))

        return {"response": "success", "product": product_name, "results": results}, 200
