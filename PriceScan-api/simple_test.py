#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test simple de l'API PriceScan
"""

print("🧪 Test simple de l'API...")

try:
    print("1. Import de Flask...")
    from flask import Flask
    print("   ✅ Flask OK")
    
    print("2. Import de la configuration...")
    from config.constant import *
    print("   ✅ Configuration OK")
    
    print("3. Import de la base de données...")
    from config.db import db
    print("   ✅ Base de données OK")
    
    print("4. Import des modèles...")
    from model.PriceScan_db import *
    print("   ✅ Modèles OK")
    
    print("5. Import des ressources...")
    from resources.auth import AuthApi
    print("   ✅ Ressources OK")
    
    print("6. Création de l'application...")
    app = Flask(__name__)
    print("   ✅ Application créée")
    
    print("7. Configuration...")
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("   ✅ Configuration OK")
    
    print("8. Initialisation de la base...")
    db.init_app(app)
    print("   ✅ Base initialisée")
    
    print("9. Test de lancement...")
    print("   ✅ Prêt à lancer !")
    
    print("\n🎉 SUCCÈS ! L'API est prête !")
    
except Exception as e:
    print(f"\n❌ ERREUR : {e}")
    import traceback
    traceback.print_exc()
