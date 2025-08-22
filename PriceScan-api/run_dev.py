#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 Script de lancement pour DÉVELOPPEMENT
Configuration optimisée pour le développement avec rechargement automatique
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Lance l'API en mode développement"""
    try:
        print("🔧 Mode DÉVELOPPEMENT - PriceScan API")
        print("=" * 50)
        
        # Import de l'application
        from launch_api import create_app
        
        app = create_app()
        
        if app:
            print("\n🚀 Lancement en mode DÉVELOPPEMENT")
            print("   📍 URL : http://localhost:5000")
            print("   📍 Health Check : http://localhost:5000/health")
            print("   🔄 Rechargement automatique : ACTIVÉ")
            print("   🐛 Mode debug : ACTIVÉ")
            print("   ⚠️  Utilisation : DÉVELOPPEMENT UNIQUEMENT")
            print("\n   Appuyez sur Ctrl+C pour arrêter")
            print("=" * 50)
            
            # Configuration développement
            app.run(
                host='127.0.0.1',  # Localhost uniquement pour la sécurité
                port=5000,
                debug=True,         # Debug activé
                use_reloader=True,  # Rechargement automatique
                threaded=True       # Support multi-threading
            )
        else:
            print("❌ Impossible de créer l'application")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 API arrêtée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
