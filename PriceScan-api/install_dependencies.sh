#!/bin/bash

echo "========================================"
echo "  PRICESCAN-API - INSTALLATION"
echo "========================================"
echo

echo "[1/4] Verification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python3 n'est pas installe"
    exit 1
fi
python3 --version

echo
echo "[2/4] Creation de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Environnement virtuel cree avec succes"
else
    echo "Environnement virtuel existe deja"
fi

echo
echo "[3/4] Activation de l'environnement virtuel..."
source venv/bin/activate

echo
echo "[4/4] Installation des dependances..."
echo "Installation des dependances principales..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "========================================"
echo "  INSTALLATION TERMINEE !"
echo "========================================"
echo
echo "Pour activer l'environnement virtuel:"
echo "  source venv/bin/activate"
echo
echo "Pour lancer l'API:"
echo "  python3 app.py"
echo
