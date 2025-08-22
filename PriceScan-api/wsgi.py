#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📡 Point d'entrée WSGI pour Gunicorn
Configuration de production pour PriceScan API
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import de l'application
from launch_api import create_app

# Créer l'application
app = create_app()

if app is None:
    raise RuntimeError("Impossible de créer l'application Flask")

# Point d'entrée pour Gunicorn
application = app

if __name__ == "__main__":
    # Pour les tests en développement
    app.run(host='0.0.0.0', port=5000, debug=False)
