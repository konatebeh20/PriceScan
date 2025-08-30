#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test des dépendances PriceScan-API
Vérifie que toutes les bibliothèques requises sont installées
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Teste l'import d'un module"""
    try:
        if package_name:
            importlib.import_module(package_name)
        else:
            importlib.import_module(module_name)
        return True, f" {module_name}"
    except ImportError as e:
        return False, f" {module_name}: {e}"

def test_dependencies():
    """Teste toutes les dépendances principales"""
    print("=" * 60)
    print("🧪 TEST DES DÉPENDANCES PRICESCAN-API")
    print("=" * 60)
    
    # Dépendances principales
    dependencies = [
        # Flask et extensions
        ("Flask", "flask"),
        ("Flask-RESTful", "flask_restful"),
        ("Flask-SQLAlchemy", "flask_sqlalchemy"),
        ("Flask-Migrate", "flask_migrate"),
        ("Flask-CORS", "flask_cors"),
        ("Flask-JWT-Extended", "flask_jwt_extended"),
        ("Werkzeug", "werkzeug"),
        
        # Base de données
        ("SQLAlchemy", "sqlalchemy"),
        ("PyMySQL", "pymysql"),
        ("psycopg2", "psycopg2"),
        ("pymongo", "pymongo"),
        ("alembic", "alembic"),
        
        # Authentification et sécurité
        ("PyJWT", "jwt"),
        ("bcrypt", "bcrypt"),
        ("cryptography", "cryptography"),
        ("python-multipart", "multipart"),
        ("email-validator", "email_validator"),
        
        # Traitement d'images et OCR
        ("OpenCV", "cv2"),
        ("Pillow", "PIL"),
        ("pytesseract", "pytesseract"),
        ("numpy", "numpy"),
        
        # Web scraping et parsing
        ("requests", "requests"),
        ("BeautifulSoup", "bs4"),
        ("lxml", "lxml"),
        ("urllib3", "urllib3"),
        ("xmltodict", "xmltodict"),
        
        # Génération de documents
        ("pdfkit", "pdfkit"),
        ("qrcode", "qrcode"),
        
        # Monitoring et logging
        ("sentry-sdk", "sentry_sdk"),
        ("gunicorn", "gunicorn"),
        
        # Cache et tasks asynchrones
        ("redis", "redis"),
        ("celery", "celery"),
        
        # Tests et qualité
        ("pytest", "pytest"),
        ("pytest-cov", "pytest_cov"),
        ("black", "black"),
        ("flake8", "flake8"),
        
        # Sérialisation et validation
        ("marshmallow", "marshmallow"),
        ("marshmallow-sqlalchemy", "marshmallow_sqlalchemy"),
        
        # Utilitaires
        ("python-dotenv", "dotenv"),
        
        # Notifications push
        ("apns2", "apns2"),
    ]
    
    print("\n📦 Test des dépendances principales...")
    print("-" * 40)
    
    success_count = 0
    total_count = len(dependencies)
    
    for name, module in dependencies:
        success, message = test_import(name, module)
        print(message)
        if success:
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f" RÉSULTATS: {success_count}/{total_count} dépendances installées")
    print("=" * 60)
    
    if success_count == total_count:
        print("🎉 Toutes les dépendances sont installées avec succès !")
        print(" L'API PriceScan est prête à être lancée.")
        return True
    else:
        print("  Certaines dépendances sont manquantes.")
        print("🔧 Exécutez: pip install -r requirements.txt")
        return False

def test_optional_dependencies():
    """Teste les dépendances optionnelles"""
    print("\n Test des dépendances optionnelles...")
    print("-" * 40)
    
    optional_deps = [
        ("matplotlib", "matplotlib"),
        ("pandas", "pandas"),
        ("scikit-learn", "sklearn"),
        ("tensorflow", "tensorflow"),
    ]
    
    for name, module in optional_deps:
        success, message = test_import(name, module)
        if success:
            print(f" {name} (optionnel)")
        else:
            print(f"  {name} (optionnel) - non installé")

def main():
    """Fonction principale"""
    try:
        # Test des dépendances principales
        main_success = test_dependencies()
        
        # Test des dépendances optionnelles
        test_optional_dependencies()
        
        print("\n" + "=" * 60)
        if main_success:
            print(" PRÊT À LANCER L'API !")
            print("   python app.py")
        else:
            print("🔧 INSTALLATION INCOMPLÈTE")
            print("   Vérifiez les erreurs ci-dessus")
        print("=" * 60)
        
    except Exception as e:
        print(f" Erreur lors du test: {e}")
        return False
    
    return main_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
