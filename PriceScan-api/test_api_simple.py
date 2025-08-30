#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API PriceScan simplifiée pour les tests du dashboard
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_secret_key_12345'
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "PriceScan API de test",
        "status": "running",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route('/api/promotions', methods=['GET'])
def get_promotions():
    test_promotions = [
        {
            'id': 1,
            'title': 'Promotion Carrefour',
            'description': '20% sur tous les produits',
            'discount_type': 'percentage',
            'discount_value': 20,
            'is_featured': True
        }
    ]
    return jsonify(test_promotions)

@app.route('/api/dashboard/stats/<user_uid>', methods=['GET'])
def get_dashboard_stats(user_uid):
    return jsonify({
        'total_receipts': 5,
        'total_spent': 125000.0,
        'this_month_spent': 45000.0,
        'avg_receipt_amount': 25000.0,
        'total_savings': 15000.0
    })

@app.route('/api/receipts', methods=['GET'])
def get_receipts():
    test_receipts = [
        {
            'id': 1,
            'store': 'Carrefour Market',
            'address': 'Bamako, Mali',
            'date': '2024-11-15',
            'time': '14:30',
            'ticket_number': 'TK001',
            'status': 'analyzed',
            'items': [
                {'name': 'Pain de mie', 'qty': 2, 'price': 1500},
                {'name': 'Lait UHT 1L', 'qty': 3, 'price': 2250}
            ],
            'total': '18 450 F CFA',
            'type': 'scanned'
        }
    ]
    return jsonify(test_receipts)

if __name__ == '__main__':
    print(" API PriceScan de test démarrée sur http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
