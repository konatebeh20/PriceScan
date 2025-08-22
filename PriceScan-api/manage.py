#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎛️ Script de gestion unifié PriceScan API
Gère le lancement en développement et en production
"""

import sys
import os
import argparse

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_development():
    """Lance l'API en mode développement"""
    print("🔧 Lancement en mode DÉVELOPPEMENT")
    print("=" * 50)
    
    try:
        from launch_api import create_app
        app = create_app()
        
        if app:
            print("📍 URL : http://localhost:5000")
            print("📍 Health Check : http://localhost:5000/health")
            print("🔄 Rechargement automatique : ACTIVÉ")
            print("🐛 Mode debug : ACTIVÉ")
            print("\nAppuyez sur Ctrl+C pour arrêter")
            print("=" * 50)
            
            app.run(
                host='127.0.0.1',
                port=5000,
                debug=True,
                use_reloader=True,
                threaded=True
            )
        else:
            print("❌ Impossible de créer l'application")
            return False
            
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False
    
    return True

def run_production():
    """Lance l'API en mode production"""
    print("🚀 Lancement en mode PRODUCTION")
    print("=" * 50)
    
    try:
        # Vérifier Gunicorn
        try:
            import gunicorn
        except ImportError:
            print("📦 Installation de Gunicorn...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gunicorn"])
            print("✅ Gunicorn installé")
        
        # Test de l'application
        from launch_api import create_app
        app = create_app()
        
        if not app:
            print("❌ Impossible de créer l'application")
            return False
        
        print("✅ Application validée")
        
        # Créer le dossier logs
        os.makedirs("logs", exist_ok=True)
        
        print("📍 URL : http://localhost:5000")
        print("📍 Health Check : http://localhost:5000/health")
        print("👥 Workers : 4")
        print("📊 Logs : logs/")
        print("\nAppuyez sur Ctrl+C pour arrêter")
        print("=" * 50)
        
        # Lancer Gunicorn
        import subprocess
        cmd = [
            "gunicorn",
            "--bind", "0.0.0.0:5000",
            "--workers", "4",
            "--timeout", "120",
            "--keep-alive", "2",
            "--max-requests", "1000",
            "--max-requests-jitter", "100",
            "--preload-app",
            "--log-level", "info",
            "--access-logfile", "logs/access.log",
            "--error-logfile", "logs/error.log",
            "--log-file", "logs/gunicorn.log",
            "wsgi:app"
        ]
        
        subprocess.run(cmd)
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False
    
    return True

def run_tests():
    """Lance les tests"""
    print("🧪 Lancement des tests")
    print("=" * 30)
    
    try:
        import subprocess
        
        # Test des dépendances
        print("1. Test des dépendances...")
        result = subprocess.run([sys.executable, "test_dependencies.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Dépendances OK")
        else:
            print("   ❌ Problème avec les dépendances")
            print(result.stdout)
            return False
        
        # Test de l'API
        print("2. Test de l'API...")
        result = subprocess.run([sys.executable, "test_api_complete.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ API OK")
        else:
            print("   ❌ Problème avec l'API")
            print(result.stdout)
            return False
        
        print("\n🎉 Tous les tests sont passés !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests : {e}")
        return False

def show_status():
    """Affiche le statut de l'API"""
    print("📊 STATUT PRICESCAN API")
    print("=" * 30)
    
    try:
        # Test de la base de données
        print("🗄️ Base de données...")
        from config.database_config import SQL_DB_URL
        print(f"   URL : {SQL_DB_URL}")
        
        # Test des modules
        print("📦 Modules critiques...")
        modules = ['flask', 'sqlalchemy', 'cv2', 'pytesseract', 'pymysql']
        for module in modules:
            try:
                __import__(module)
                print(f"   ✅ {module}")
            except ImportError:
                print(f"   ❌ {module}")
        
        # Test de l'application
        print("🚀 Application...")
        from launch_api import create_app
        app = create_app()
        if app:
            print("   ✅ Application créée")
        else:
            print("   ❌ Erreur de création")
        
        print("\n✅ Statut vérifié")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='🎛️ Gestionnaire PriceScan API')
    parser.add_argument('command', choices=['dev', 'prod', 'test', 'status'], 
                       help='Commande à exécuter')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'dev':
            run_development()
        elif args.command == 'prod':
            run_production()
        elif args.command == 'test':
            run_tests()
        elif args.command == 'status':
            show_status()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Si aucun argument, afficher l'aide
        print("🎛️ GESTIONNAIRE PRICESCAN API")
        print("=" * 40)
        print("Utilisation :")
        print("  python manage.py dev     # Mode développement")
        print("  python manage.py prod    # Mode production")
        print("  python manage.py test    # Lancer les tests")
        print("  python manage.py status  # Afficher le statut")
        print("=" * 40)
    else:
        main()
