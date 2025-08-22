#!/bin/bash

echo "====================================="
echo "  PRICESCAN API - MODE PRODUCTION"
echo "====================================="
echo

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

echo
echo "Lancement en mode production..."
python3 manage.py prod
