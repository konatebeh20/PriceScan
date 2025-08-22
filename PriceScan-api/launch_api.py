#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de lancement de l'API PriceScan
Évite les problèmes potentiels de app.py
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """Crée l'application Flask PriceScan"""
    try:
        print("🚀 Création de l'API PriceScan...")
        
        # Import des modules nécessaires
        from flask import Flask, request, render_template
        from flask_cors import CORS
        from flask_migrate import Migrate
        from flask_restful import Api
        from flask_sqlalchemy import SQLAlchemy
        
        print("   ✅ Modules Flask importés")
        
        # Import de la configuration
        from config.constant import SQL_DB_URL, UPLOAD_FOLDER
        from config.db import db
        
        print("   ✅ Configuration importée")
        
        # Import des modèles
        from model.PriceScan_db import ps_users, ps_stores, ps_products, ps_prices
        
        print("   ✅ Modèles importés")
        
        # Import des ressources
        from resources.auth import AuthApi
        from resources.users import UsersApi
        from resources.categories import CategoriesApi
        from resources.favorite import FavoriteApi
        from resources.device_tokens import DeviceTokens
        from resources.stores import StoresApi
        from resources.products import ProductsApi
        from resources.prices import PricesApi
        from resources.receipts import ReceiptsApi
        
        print("   ✅ Ressources importées")
        
        # Créer l'application Flask
        app = Flask(__name__)
        print("   ✅ Application Flask créée")
        
        # Configuration
        app.secret_key = os.urandom(24)
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        
        print("   ✅ Configuration appliquée")
        
        # Initialiser les extensions
        db.init_app(app)
        migrate = Migrate(app, db)
        CORS(app)
        api = Api(app)
        
        print("   ✅ Extensions initialisées")
        
        # Ajouter les ressources à l'API
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
        
        print("   ✅ Toutes les ressources ajoutées")
        
        # Routes spéciales
        @app.route('/')
        def hello():
            return render_template("index.html")
        
        @app.route('/health')
        def health_check():
            return {'status': 'healthy', 'message': 'PriceScan API is running'}, 200
        
        @app.route('/api/compare/<string:product_id>')
        def compare_prices_endpoint(product_id):
            """Endpoint pour comparer les prix d'un produit entre différents magasins"""
            try:
                from resources.prices import PricesApi
                prices_api = PricesApi()
                return prices_api.compare_prices(product_id)
            except Exception as e:
                return {'error': str(e)}, 500
        
        @app.route('/api/search')
        def search_products_endpoint():
            """Endpoint pour rechercher des produits"""
            try:
                query = request.args.get('q')
                if not query:
                    return {'error': 'Query parameter required'}, 400
                
                from resources.products import ProductsApi
                products_api = ProductsApi()
                return products_api.search_products(query)
            except Exception as e:
                return {'error': str(e)}, 500
        
        @app.route('/api/stats/user/<string:user_uid>')
        def user_stats_endpoint(user_uid):
            """Endpoint pour les statistiques d'un utilisateur"""
            try:
                from resources.users import UsersApi
                users_api = UsersApi()
                return users_api.get_user_stats(user_uid)
            except Exception as e:
                return {'error': str(e)}, 500
        
        print("   ✅ Routes spéciales ajoutées")
        
        print("\n🎉 API PriceScan créée avec succès !")
        return app
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la création de l'API : {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Fonction principale"""
    app = create_app()
    
    if app:
        print("\n🚀 Lancement de l'API sur http://localhost:5000")
        print("   Appuyez sur Ctrl+C pour arrêter")
        
        try:
            app.run(
                host='0.0.0.0',
                port=5000,
                debug=True,
                use_reloader=False
            )
        except KeyboardInterrupt:
            print("\n🛑 API arrêtée par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur lors du lancement : {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n🔧 Impossible de créer l'API")
        sys.exit(1)

if __name__ == "__main__":
    main()
