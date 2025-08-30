#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test des imports pour identifier tous les problèmes
"""

import sys
import importlib

def test_import(module_name, description=""):
    """Teste l'import d'un module"""
    try:
        importlib.import_module(module_name)
        print(f" {module_name} - {description}")
        return True
    except ImportError as e:
        print(f" {module_name} - {description}: {e}")
        return False
    except Exception as e:
        print(f"  {module_name} - {description}: {e}")
        return False

def test_all_imports():
    """Teste tous les imports critiques"""
    print("=" * 60)
    print("🧪 TEST DES IMPORTS CRITIQUES")
    print("=" * 60)
    
    # Test des modules principaux
    print("\n📦 Modules principaux :")
    test_import("flask", "Framework web")
    test_import("flask_restful", "API REST")
    test_import("flask_sqlalchemy", "ORM")
    test_import("cv2", "OpenCV")
    test_import("PIL", "Pillow")
    test_import("pytesseract", "OCR")
    
    # Test des helpers
    print("\n🔧 Test des helpers :")
    test_import("helpers.mailer", "Module d'emails")
    test_import("helpers.users", "Module utilisateurs")
    test_import("helpers.auth", "Module d'authentification")
    test_import("helpers.receipt", "Module de reçus")
    test_import("helpers.scrapper", "Module de scraping")
    
    # Test des ressources
    print("\n📡 Test des ressources :")
    test_import("resources.users", "API utilisateurs")
    test_import("resources.auth", "API authentification")
    test_import("resources.stores", "API magasins")
    test_import("resources.products", "API produits")
    test_import("resources.prices", "API prix")
    test_import("resources.receipts", "API reçus")
    
    # Test des modèles
    print("\n🗄️ Test des modèles :")
    test_import("model.PriceScan_db", "Modèles de base de données")
    
    # Test de la configuration
    print("\n⚙️ Test de la configuration :")
    test_import("config.constant", "Constantes")
    test_import("config.db", "Base de données")
    test_import("config.database_config", "Configuration BDD")

def test_specific_functions():
    """Teste des fonctions spécifiques"""
    print("\n Test des fonctions spécifiques :")
    
    try:
        from helpers.mailer import send_mailer_custom
        print(" send_mailer_custom importée avec succès")
    except ImportError as e:
        print(f" send_mailer_custom: {e}")
    
    try:
        from helpers.users import create_user
        print(" create_user importée avec succès")
    except ImportError as e:
        print(f" create_user: {e}")
    
    try:
        from helpers.auth import login
        print(" login importée avec succès")
    except ImportError as e:
        print(f" login: {e}")

def main():
    """Fonction principale"""
    try:
        test_all_imports()
        test_specific_functions()
        
        print("\n" + "=" * 60)
        print("🎯 RÉSUMÉ DES TESTS D'IMPORT")
        print("=" * 60)
        
    except Exception as e:
        print(f" Erreur lors du test : {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
