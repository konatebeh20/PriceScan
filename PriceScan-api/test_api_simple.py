#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test simple de l'API Dashboard
Lance une version simplifiée de l'API pour les tests
"""

import sys
import os
import time
import requests
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import db
from model.PriceScan_db import *

# Créer une application Flask simple pour les tests
test_app = Flask(__name__)
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Konate%202019@localhost:5432/PriceScan_db'
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db.init_app(test_app)

# Activer CORS
CORS(test_app)

# Créer l'API
test_api = Api(test_app)

# Routes de test simples
@test_app.route('/api/health')
def health_check():
    return jsonify({"status": "OK", "message": "API Dashboard fonctionnelle"})

@test_app.route('/api/test')
def test_endpoint():
    return jsonify({"message": "Endpoint de test accessible"})

# Test des modèles
@test_app.route('/api/test/models')
def test_models():
    try:
        with test_app.app_context():
            # Test des nouvelles tables
            tables = ['ps_promotions', 'ps_user_profiles', 'ps_dashboard_stats', 'ps_scan_history']
            results = {}
            
            for table in tables:
                try:
                    result = db.session.execute(f"SELECT COUNT(*) FROM {table}")
                    count = result.scalar()
                    results[table] = {"status": "OK", "count": count}
                except Exception as e:
                    results[table] = {"status": "ERROR", "error": str(e)}
            
            return jsonify({
                "status": "OK",
                "message": "Test des modèles terminé",
                "results": results
            })
    except Exception as e:
        return jsonify({"status": "ERROR", "error": str(e)})

# Test des données
@test_app.route('/api/test/data')
def test_data():
    try:
        with test_app.app_context():
            # Récupérer quelques données de test
            promotions = ps_promotions.query.limit(5).all()
            user_profiles = ps_user_profiles.query.limit(5).all()
            dashboard_stats = ps_dashboard_stats.query.limit(5).all()
            
            return jsonify({
                "status": "OK",
                "message": "Données de test récupérées",
                "data": {
                    "promotions_count": len(promotions),
                    "user_profiles_count": len(user_profiles),
                    "dashboard_stats_count": len(dashboard_stats)
                }
            })
    except Exception as e:
        return jsonify({"status": "ERROR", "error": str(e)})

def run_test_api():
    """Lance l'API de test"""
    print("🚀 Lancement de l'API de test...")
    print("📍 Endpoints disponibles:")
    print("   - /api/health - Vérification de santé")
    print("   - /api/test - Endpoint de test")
    print("   - /api/test/models - Test des modèles")
    print("   - /api/test/data - Test des données")
    print("\n🌐 API accessible sur: http://localhost:5001")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    
    try:
        test_app.run(host='0.0.0.0', port=5001, debug=False)
    except KeyboardInterrupt:
        print("\n✅ API de test arrêtée")

if __name__ == "__main__":
    run_test_api()
