#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test de l'API d'authentification PriceScan
"""

import requests
import json

def test_auth_api():
    """Teste l'API d'authentification"""
    base_url = "http://localhost:5000"
    
    print("🧪 Test de l'API d'authentification PriceScan")
    print("=" * 50)
    
    # 1. Test d'inscription
    print("\n📝 Test d'inscription...")
    register_data = {
        "firstname": "Test",
        "lastname": "User",
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
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
            print(" Inscription réussie !")
            user_data = response.json()
            if 'token' in user_data:
                print(f"Token reçu: {user_data['token'][:20]}...")
            if 'user' in user_data:
                print(f"Utilisateur créé: {user_data['user']}")
        else:
            print(" Inscription échouée")
            
    except Exception as e:
        print(f" Erreur inscription: {e}")
    
    # 2. Test de connexion
    print("\n🔐 Test de connexion...")
    login_data = {
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print(" Connexion réussie !")
            login_data = response.json()
            if 'token' in login_data:
                print(f"Token reçu: {login_data['token'][:20]}...")
        else:
            print(" Connexion échouée")
            
    except Exception as e:
        print(f" Erreur connexion: {e}")
    
    # 3. Test avec un utilisateur inexistant
    print("\n🚫 Test connexion utilisateur inexistant...")
    fake_login_data = {
        "username": "fakeuser",
        "password": "fakepass"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=fake_login_data,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print(" Gestion d'erreur correcte pour utilisateur inexistant")
        else:
            print(" Réponse inattendue pour utilisateur inexistant")
            
    except Exception as e:
        print(f" Erreur test utilisateur inexistant: {e}")

if __name__ == "__main__":
    test_auth_api()
