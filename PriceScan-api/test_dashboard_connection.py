#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test de connexion du dashboard Angular à l'API Flask
"""

import requests
import json

def test_dashboard_connection():
    """Teste la connexion du dashboard à l'API"""
    base_url = "http://localhost:5000"
    
    print("🔌 Test de connexion du dashboard Angular à l'API Flask")
    print("=" * 60)
    
    # 1. Test de l'endpoint d'inscription avec les données du dashboard
    print("\n📝 Test d'inscription avec données du dashboard...")
    
    # Données exactes envoyées par le dashboard Angular
    dashboard_register_data = {
        "username": "dashboarduser2",
        "email": "dashboard2@test.com",
        "password": "dashboard123",
        "firstname": "Dashboard",
        "lastname": "Test2",
        "accountType": "particulier"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=dashboard_register_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print(" Inscription réussie avec données du dashboard !")
            
            # Test de connexion avec le nouvel utilisateur
            print("\n🔐 Test de connexion avec le nouvel utilisateur...")
            login_data = {
                "username": "dashboarduser2",
                "password": "dashboard123"
            }
            
            login_response = requests.post(
                f"{base_url}/api/auth/login",
                json=login_data,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                timeout=10
            )
            
            print(f"Login Status: {login_response.status_code}")
            print(f"Login Response: {login_response.text}")
            
            if login_response.status_code == 200:
                print(" Connexion réussie avec le nouvel utilisateur !")
            else:
                print(" Connexion échouée avec le nouvel utilisateur")
                
        else:
            print(" Inscription échouée avec données du dashboard")
            
    except Exception as e:
        print(f" Erreur test dashboard : {e}")
    
    # 2. Test de l'endpoint de connexion avec l'utilisateur existant
    print("\n🔐 Test de connexion avec utilisateur existant...")
    existing_user_login = {
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        login_response = requests.post(
            f"{base_url}/api/auth/login",
            json=existing_user_login,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=10
        )
        
        print(f"Status: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        
        if login_response.status_code == 200:
            print(" Connexion réussie avec utilisateur existant !")
        else:
            print(" Connexion échouée avec utilisateur existant")
            
    except Exception as e:
        print(f" Erreur test connexion existant : {e}")
    
    # 3. Test des headers CORS
    print("\n🌐 Test des headers CORS...")
    try:
        # Test OPTIONS (preflight request)
        options_response = requests.options(
            f"{base_url}/api/auth/register",
            headers={
                'Origin': 'http://localhost:4200',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        
        print(f"OPTIONS Status: {options_response.status_code}")
        print(f"CORS Headers: {dict(options_response.headers)}")
        
    except Exception as e:
        print(f" Erreur test CORS : {e}")

if __name__ == "__main__":
    test_dashboard_connection()
