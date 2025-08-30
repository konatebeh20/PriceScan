#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test de connexion à l'API Flask PriceScan
"""

import requests
import json

def test_api_connection():
    """Teste la connexion à l'API Flask"""
    base_url = "http://localhost:5000"
    
    print("🔌 Test de connexion à l'API Flask PriceScan")
    print("=" * 50)
    
    # 1. Test de connexion basique
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f" API accessible - Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(" API non accessible - Vérifiez que Flask est démarré")
        return False
    except Exception as e:
        print(f" Erreur connexion : {e}")
        return False
    
    # 2. Test de l'endpoint d'authentification
    try:
        response = requests.get(f"{base_url}/api/auth/login", timeout=5)
        print(f" Endpoint auth accessible - Status: {response.status_code}")
    except Exception as e:
        print(f" Erreur endpoint auth : {e}")
    
    # 3. Test d'inscription avec de nouvelles données
    print("\n📝 Test d'inscription avec nouvelles données...")
    register_data = {
        "firstname": "Dashboard",
        "lastname": "Test",
        "username": "dashboarduser",
        "email": "dashboard@test.com",
        "password": "dashboard123",
        "accountType": "particulier"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=register_data,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print(" Inscription réussie depuis l'API !")
            return True
        else:
            print(" Inscription échouée depuis l'API")
            return False
            
    except Exception as e:
        print(f" Erreur test inscription : {e}")
        return False

if __name__ == "__main__":
    test_api_connection()
