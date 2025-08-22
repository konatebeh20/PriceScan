#!/bin/bash

echo "====================================="
echo "  PRICESCAN API - MODE DEVELOPPEMENT"
echo "====================================="
echo

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

echo
echo "Lancement en mode développement..."
python3 manage.py dev
