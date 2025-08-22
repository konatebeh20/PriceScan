#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test complet de l'API PriceScan
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_creation():
    """Test de création de l'API Flask"""
    try:
        print("🧪 Test de création de l'API Flask...")
        
        # Import des modules nécessaires
        from flask import Flask
        from flask_cors import CORS
        from flask_migrate import Migrate
        from flask_sqlalchemy import SQLAlchemy
        from flask_restful import Api
        
        print("   ✅ Modules Flask importés")
        
        # Créer l'application Flask
        app = Flask(__name__)
        print("   ✅ Application Flask créée")
        
        # Configuration
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        print("   ✅ Configuration appliquée")
        
        # Initialiser les extensions
        db = SQLAlchemy()
        db.init_app(app)
        print("   ✅ Base de données initialisée")
        
        migrate = Migrate(app, db)
        print("   ✅ Migrations initialisées")
        
        CORS(app)
        print("   ✅ CORS activé")
        
        api = Api(app)
        print("   ✅ API REST initialisée")
        
        print("   ✅ API Flask créée avec succès !")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la création de l'API : {e}")
        return False

def test_resources_import():
    """Test de l'import des ressources"""
    try:
        print("\n🔧 Test de l'import des ressources...")
        
        from resources.auth import AuthApi
        from resources.users import UsersApi
        from resources.categories import CategoriesApi
        from resources.favorite import FavoriteApi
        from resources.device_tokens import DeviceTokens
        from resources.stores import StoresApi
        from resources.products import ProductsApi
        from resources.prices import PricesApi
        from resources.receipts import ReceiptsApi
        
        print("   ✅ Toutes les ressources importées")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de l'import des ressources : {e}")
        return False

def test_helpers_import():
    """Test de l'import des helpers"""
    try:
        print("\n🔧 Test de l'import des helpers...")
        
        from helpers.mailer import send_mailer_custom
        from helpers.users import create_user
        from helpers.auth import login
        from helpers.receipt import upload_receipt
        
        print("   ✅ Tous les helpers importés")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de l'import des helpers : {e}")
        return False

def test_models_import():
    """Test de l'import des modèles"""
    try:
        print("\n🗄️ Test de l'import des modèles...")
        
        from model.PriceScan_db import ps_users, ps_stores, ps_products, ps_prices
        
        print("   ✅ Tous les modèles importés")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de l'import des modèles : {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🧪 TEST COMPLET DE L'API PRICESCAN")
    print("=" * 60)
    
    success = True
    
    # Test 1: Création de l'API Flask
    if not test_api_creation():
        success = False
    
    # Test 2: Import des ressources
    if not test_resources_import():
        success = False
    
    # Test 3: Import des helpers
    if not test_helpers_import():
        success = False
    
    # Test 4: Import des modèles
    if not test_models_import():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ L'API PriceScan est prête à être lancée !")
        print("\n🚀 Lancez l'API avec : python app.py")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
