#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de débogage pour identifier le problème exact de l'API
"""

import sys
import os
import traceback

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_app():
    """Débogue l'application étape par étape"""
    try:
        print(" Débogage de l'application PriceScan...")
        
        print("\n1️⃣ Import de la configuration...")
        from config.constant import *
        print("    Configuration importée")
        
        print("\n2️⃣ Import de la base de données...")
        from config.db import db
        print("    Base de données importée")
        
        print("\n3️⃣ Import des modèles...")
        from model.PriceScan_db import *
        print("    Modèles importés")
        
        print("\n4️⃣ Import des helpers...")
        from helpers.mailer import *
        print("    Helpers mailer importés")
        
        print("\n5️⃣ Import des ressources...")
        from resources.auth import AuthApi
        from resources.users import UsersApi
        from resources.categories import CategoriesApi
        from resources.favorite import FavoriteApi
        from resources.device_tokens import DeviceTokens
        from resources.stores import StoresApi
        from resources.products import ProductsApi
        from resources.prices import PricesApi
        from resources.receipts import ReceiptsApi
        print("    Toutes les ressources importées")
        
        print("\n6️⃣ Import de Flask et extensions...")
        from flask import Flask
        from flask_cors import CORS
        from flask_migrate import Migrate
        from flask_restful import Api
        print("    Flask et extensions importés")
        
        print("\n7️⃣ Création de l'application...")
        app = Flask(__name__)
        print("    Application Flask créée")
        
        print("\n8️⃣ Configuration de l'application...")
        app.secret_key = os.urandom(24)
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        print("    Configuration appliquée")
        
        print("\n9️⃣ Initialisation des extensions...")
        db.init_app(app)
        migrate = Migrate(app, db)
        CORS(app)
        api = Api(app)
        print("    Extensions initialisées")
        
        print("\n🔟 Ajout des ressources à l'API...")
        # Categories API
        api.add_resource(CategoriesApi, '/api/categories/<string:route>', endpoint='cat_all', methods=["GET","POST"])
        api.add_resource(CategoriesApi, '/api/categories/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])
        print("    Categories API ajoutée")
        
        # Users API
        api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='users_all', methods=["GET","POST"])
        api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='users_all_patch', methods=["PATCH","DELETE"])
        print("    Users API ajoutée")
        
        # Auth API
        api.add_resource(AuthApi, '/api/auth/<string:route>', endpoint='auth_all', methods=["GET","POST"])
        api.add_resource(AuthApi, '/api/auth/<string:route>', endpoint='auth_all_patch', methods=["PATCH","DELETE"])
        print("    Auth API ajoutée")
        
        # Stores API
        api.add_resource(StoresApi, '/api/stores/<string:route>', endpoint='stores_all', methods=["GET","POST"])
        api.add_resource(StoresApi, '/api/stores/<string:route>', endpoint='stores_all_patch', methods=["PATCH","DELETE"])
        print("    Stores API ajoutée")
        
        # Products API
        api.add_resource(ProductsApi, '/api/products/<string:route>', endpoint='products_all', methods=["GET","POST"])
        api.add_resource(ProductsApi, '/api/products/<string:route>', endpoint='products_all_patch', methods=["PATCH","DELETE"])
        print("    Products API ajoutée")
        
        # Prices API
        api.add_resource(PricesApi, '/api/prices/<string:route>', endpoint='prices_all', methods=["GET","POST"])
        api.add_resource(PricesApi, '/api/prices/<string:route>', endpoint='prices_all_patch', methods=["PATCH","DELETE"])
        print("    Prices API ajoutée")
        
        # Receipts API
        api.add_resource(ReceiptsApi, '/api/receipts/<string:route>', endpoint='receipts_all', methods=["GET","POST"])
        api.add_resource(ReceiptsApi, '/api/receipts/<string:route>', endpoint='receipts_all_patch', methods=["PATCH","DELETE"])
        print("    Receipts API ajoutée")
        
        # Favorite API
        api.add_resource(FavoriteApi, '/api/favorite/<string:route>', endpoint='favorite_all', methods=["GET","POST"])
        api.add_resource(FavoriteApi, '/api/favorite/<string:route>', endpoint='favorite_all_patch', methods=["PATCH","DELETE"])
        print("    Favorite API ajoutée")
        
        # Device Tokens
        api.add_resource(DeviceTokens, '/api/device_tokens/<string:route>', endpoint='device_tokens_all', methods=["GET","POST"])
        api.add_resource(DeviceTokens, '/api/device_tokens/<string:route>', endpoint='device_tokens_all_patch', methods=["PATCH","DELETE"])
        print("    Device Tokens API ajoutée")
        
        print("\n🎉 APPLICATION CRÉÉE AVEC SUCCÈS !")
        print(" Toutes les étapes sont passées !")
        
        return app
        
    except Exception as e:
        print(f"\n ERREUR LORS DU DÉBOGAGE : {e}")
        print("\n Traceback complet :")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    app = debug_app()
    if app:
        print("\n Lancement de l'API...")
        try:
            app.run(host='0.0.0.0', port=5000, debug=True)
        except Exception as e:
            print(f" Erreur lors du lancement : {e}")
            traceback.print_exc()
    else:
        print("\n🔧 Impossible de créer l'application")
        sys.exit(1)
