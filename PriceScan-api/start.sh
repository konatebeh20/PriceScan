#!/bin/bash

echo "========================================"
echo "    PRICESCAN API - DEMARRAGE"
echo "========================================"
echo

echo "[1/5] Verification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python3 n'est pas installe"
    echo "Veuillez installer Python 3.8+ avec: sudo apt install python3 python3-pip"
    exit 1
fi
echo "Python OK: $(python3 --version)"

echo
echo "[2/5] Verification de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    echo "Creation de l'environnement virtuel..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERREUR: Impossible de creer l'environnement virtuel"
        exit 1
    fi
fi
echo "Environnement virtuel OK"

echo
echo "[3/5] Activation de l'environnement virtuel..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible d'activer l'environnement virtuel"
    exit 1
fi
echo "Environnement virtuel active"

echo
echo "[4/5] Installation des dependances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible d'installer les dependances"
    exit 1
fi
echo "Dependances installees"

echo
echo "[5/5] Demarrage de l'API..."
echo
echo "L'API sera accessible sur: http://localhost:5000"
echo "Health check: http://localhost:5000/health"
echo
echo "Appuyez sur Ctrl+C pour arreter l'API"
echo

python3 app.py

echo
echo "API arretee"
