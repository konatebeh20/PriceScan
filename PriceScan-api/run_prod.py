#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 Script de lancement pour PRODUCTION
Configuration optimisée pour la production avec Gunicorn
"""

import sys
import os
import subprocess

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_gunicorn():
    """Vérifie si Gunicorn est installé"""
    try:
        import gunicorn
        return True
    except ImportError:
        return False

def install_gunicorn():
    """Installe Gunicorn si nécessaire"""
    print("📦 Installation de Gunicorn...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gunicorn"])
        print("✅ Gunicorn installé avec succès")
        return True
    except subprocess.CalledProcessError:
        print("❌ Échec de l'installation de Gunicorn")
        return False

def main():
    """Lance l'API en mode production"""
    try:
        print("🚀 Mode PRODUCTION - PriceScan API")
        print("=" * 50)
        
        # Vérifier et installer Gunicorn si nécessaire
        if not check_gunicorn():
            print("⚠️  Gunicorn non trouvé")
            if not install_gunicorn():
                print("❌ Impossible d'installer Gunicorn")
                sys.exit(1)
        
        # Test de l'application
        print("🧪 Test de l'application...")
        from launch_api import create_app
        app = create_app()
        
        if not app:
            print("❌ Impossible de créer l'application")
            sys.exit(1)
        
        print("✅ Application validée")
        
        # Configuration Gunicorn
        gunicorn_cmd = [
            "gunicorn",
            "--bind", "0.0.0.0:5000",
            "--workers", "4",                    # 4 workers pour de meilleures performances
            "--worker-class", "sync",            # Type de worker
            "--timeout", "120",                  # Timeout de 2 minutes
            "--keep-alive", "2",                 # Keep-alive de 2 secondes
            "--max-requests", "1000",            # Max 1000 requêtes par worker
            "--max-requests-jitter", "100",      # Jitter pour éviter la synchronisation
            "--preload-app",                     # Précharger l'application
            "--log-level", "info",               # Level de log
            "--access-logfile", "logs/access.log",     # Log des accès
            "--error-logfile", "logs/error.log",       # Log des erreurs
            "--log-file", "logs/gunicorn.log",         # Log principal
            "--capture-output",                  # Capturer la sortie
            "--enable-stdio-inheritance",        # Hériter stdio
            "wsgi:app"                          # Module WSGI
        ]
        
        # Créer le dossier logs si nécessaire
        os.makedirs("logs", exist_ok=True)
        
        print("\n🚀 Lancement en mode PRODUCTION")
        print("   📍 URL : http://localhost:5000")
        print("   📍 Health Check : http://localhost:5000/health")
        print("   👥 Workers : 4")
        print("   🔒 Sécurité : ACTIVÉE")
        print("   📊 Logs : logs/")
        print("   ⚡ Performance : OPTIMISÉE")
        print("\n   Appuyez sur Ctrl+C pour arrêter")
        print("=" * 50)
        
        # Lancer Gunicorn
        subprocess.run(gunicorn_cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 API arrêtée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
