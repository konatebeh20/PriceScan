import logging
import os
import sys
from urllib import response

from config.constant import *
import pdfkit
import qrcode
import sentry_sdk
from flask import (Flask, make_response, redirect, render_template, request,session)
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sentry_sdk.integrations.flask import FlaskIntegration

from config.constant import *
from config.db import db
from helpers.mailer import *
from model.PriceScan_db import *
from resources.auth import AuthApi
from resources.categories import CategoriesApi
from resources.favorite import FavoriteApi
from resources.users import UsersApi
from resources.device_tokens import DeviceTokens
from resources.stores import StoresApi
from resources.products import ProductsApi
from resources.prices import PricesApi
from resources.receipts import ReceiptsApi

sentry_sdk.init(
    dsn="https://e55540efdb25abee9b6509335cfb5bae@o295794.ingest.sentry.io/4506298354499584",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

handler = logging.FileHandler('logger/app.log')  # errors logged to this file
handler.setLevel(logging.ERROR)  # only log errors and above
app.logger.addHandler(handler)

api = Api(app)

db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

# Categories API
api.add_resource(CategoriesApi, '/api/categories/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(CategoriesApi, '/api/categories/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

# Users API
api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='users_all', methods=["GET","POST"])
api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='users_all_patch', methods=["PATCH","DELETE"])

# Auth API
api.add_resource(AuthApi, '/api/auth/<string:route>', endpoint='auth_all', methods=["GET","POST"])
api.add_resource(AuthApi, '/api/auth/<string:route>', endpoint='auth_all_patch', methods=["PATCH","DELETE"])

# Stores API
api.add_resource(StoresApi, '/api/stores/<string:route>', endpoint='stores_all', methods=["GET","POST"])
api.add_resource(StoresApi, '/api/stores/<string:route>', endpoint='stores_all_patch', methods=["PATCH","DELETE"])

# Products API
api.add_resource(ProductsApi, '/api/products/<string:route>', endpoint='products_all', methods=["GET","POST"])
api.add_resource(ProductsApi, '/api/products/<string:route>', endpoint='products_all_patch', methods=["PATCH","DELETE"])

# Prices API
api.add_resource(PricesApi, '/api/prices/<string:route>', endpoint='prices_all', methods=["GET","POST"])
api.add_resource(PricesApi, '/api/prices/<string:route>', endpoint='prices_all_patch', methods=["PATCH","DELETE"])

# Receipts API
api.add_resource(ReceiptsApi, '/api/receipts/<string:route>', endpoint='receipts_all', methods=["GET","POST"])
api.add_resource(ReceiptsApi, '/api/receipts/<string:route>', endpoint='receipts_all_patch', methods=["PATCH","DELETE"])

# Favorite API
api.add_resource(FavoriteApi, '/api/favorite/<string:route>', endpoint='favorite_all', methods=["GET","POST"])
api.add_resource(FavoriteApi, '/api/favorite/<string:route>', endpoint='favorite_all_patch', methods=["PATCH","DELETE"])

# Device Tokens
api.add_resource(DeviceTokens, '/api/device_tokens/<string:route>', endpoint='device_tokens_all', methods=["GET","POST"])
api.add_resource(DeviceTokens, '/api/device_tokens/<string:route>', endpoint='device_tokens_all_patch', methods=["PATCH","DELETE"])

@app.route(BASE_URL + '/')
def hello():
    return render_template("index.html")

@app.route(BASE_URL + '/pricescan')
def pricescan_main():
    """Endpoint principal de l'API PriceScan"""
    return {
        'status': 'success',
        'message': 'Bienvenue sur l\'API PriceScan !',
        'version': '1.0.0',
        'description': 'API de comparaison de prix et de gestion des produits',
        'endpoints': {
            'main': '/pricescan',
            'api_base': '/api',
            'categories': '/api/categories',
            'users': '/api/users',
            'auth': '/api/auth',
            'stores': '/api/stores',
            'products': '/api/products',
            'prices': '/api/prices',
            'receipts': '/api/receipts',
            'favorites': '/api/favorite',
            'device_tokens': '/api/device_tokens',
            'compare': '/api/compare/<product_id>',
            'search': '/api/search',
            'stats': '/api/stats/user/<user_uid>'
        },
        'database': 'PostgreSQL',
        'status_code': 200
    }, 200

@app.route(BASE_URL + '/api/compare/<string:product_id>')
def compare_prices_endpoint(product_id):
    """Endpoint pour comparer les prix d'un produit entre différents magasins"""
    try:
        from resources.prices import PricesApi
        prices_api = PricesApi()
        return prices_api.compare_prices(product_id)
    except Exception as e:
        return {'error': str(e)}, 500

@app.route(BASE_URL + '/api/search')
def search_products_endpoint():
    """Endpoint pour rechercher des produits"""
    try:
        query = request.args.get('q')
        if not query:
            return {'error': 'Paramètre de recherche requis'}, 400
        
        from resources.products import ProductsApi
        products_api = ProductsApi()
        return products_api.search_products(query)
    except Exception as e:
        return {'error': str(e)}, 500

@app.route(BASE_URL + '/api/stats/user/<string:user_uid>')
def user_stats_endpoint(user_uid):
    """Endpoint pour obtenir les statistiques d'un utilisateur"""
    try:
        from resources.receipts import ReceiptsApi
        receipts_api = ReceiptsApi()
        return receipts_api.get_receipt_stats(user_uid)
    except Exception as e:
        return {'error': str(e)}, 500

@app.route("/authenticate/")
def authenticate():
    return "authentication"

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")