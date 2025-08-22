#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test simple pour identifier les problèmes d'import
"""

print("🧪 Test des imports critiques...")

try:
    print("1. Import de Flask...")
    from flask import Flask
    print("   ✅ Flask importé")
except Exception as e:
    print(f"   ❌ Erreur Flask: {e}")

try:
    print("2. Import de la configuration...")
    from config.constant import *
    print("   ✅ Configuration importée")
except Exception as e:
    print(f"   ❌ Erreur configuration: {e}")

try:
    print("3. Import de la base de données...")
    from config.db import db
    print("   ✅ Base de données importée")
except Exception as e:
    print(f"   ❌ Erreur base de données: {e}")

try:
    print("4. Import des modèles...")
    from model.PriceScan_db import *
    print("   ✅ Modèles importés")
except Exception as e:
    print(f"   ❌ Erreur modèles: {e}")

try:
    print("5. Import des helpers...")
    from helpers.mailer import *
    print("   ✅ Helpers mailer importés")
except Exception as e:
    print(f"   ❌ Erreur helpers mailer: {e}")

try:
    print("6. Import des ressources...")
    from resources.auth import AuthApi
    print("   ✅ Ressource auth importée")
except Exception as e:
    print(f"   ❌ Erreur ressource auth: {e}")

try:
    print("7. Import des autres ressources...")
    from resources.users import UsersApi
    from resources.categories import CategoriesApi
    from resources.favorite import FavoriteApi
    from resources.device_tokens import DeviceTokens
    from resources.stores import StoresApi
    from resources.products import ProductsApi
    from resources.prices import PricesApi
    from resources.receipts import ReceiptsApi
    print("   ✅ Toutes les ressources importées")
except Exception as e:
    print(f"   ❌ Erreur ressources: {e}")

print("\n🎯 Test terminé !")
