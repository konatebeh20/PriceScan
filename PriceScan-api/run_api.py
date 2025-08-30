#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de lancement simplifié de l'API PriceScan
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Lance l'API PriceScan"""
    try:
        print(" Lancement de l'API PriceScan...")
        
        # Import de l'application
        from app import app
        
        print(" Application importée avec succès")
        print("🌐 Démarrage du serveur sur http://localhost:5000")
        
        # Lancer l'application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False
        )
        
    except Exception as e:
        print(f" Erreur lors du lancement : {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
