#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test complet du flux d'authentification PriceScan
"""

import requests
import json
import time

def test_complete_flow():
    """Teste le flux complet d'authentification"""
    base_url = "http://localhost:5000"
    
    print("🧪 TEST COMPLET DU FLUX D'AUTHENTIFICATION PRICESCAN")
    print("=" * 60)
    
    # 1. Test d'inscription avec données du dashboard
    print("\n📝 1. Test d'inscription avec données du dashboard...")
    
    # Créer un email unique pour éviter les conflits
    timestamp = int(time.time())
    unique_email = f"dashboard_test_{timestamp}@example.com"
    unique_username = f"dashboard_test_{timestamp}"
    
    register_data = {
        "firstname": "Dashboard",
        "lastname": "Test",
        "username": unique_username,
        "email": unique_email,
        "password": "dashboard123",
        "accountType": "particulier"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=register_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print(" Inscription réussie !")
            user_data = response.json()
            
            # 2. Test de connexion avec le nouvel utilisateur
            print(f"\n🔐 2. Test de connexion avec {unique_username}...")
            
            login_data = {
                "username": unique_username,
                "password": "dashboard123"
            }
            
            login_response = requests.post(
                f"{base_url}/api/auth/login",
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"Login Status: {login_response.status_code}")
            print(f"Login Response: {login_response.text}")
            
            if login_response.status_code == 200:
                print(" Connexion réussie !")
                
                # 3. Test de connexion avec l'email
                print(f"\n🔐 3. Test de connexion avec l'email {unique_email}...")
                
                email_login_data = {
                    "username": unique_email,
                    "password": "dashboard123"
                }
                
                email_login_response = requests.post(
                    f"{base_url}/api/auth/login",
                    json=email_login_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                print(f"Email Login Status: {email_login_response.status_code}")
                print(f"Email Login Response: {email_login_response.text}")
                
                if email_login_response.status_code == 200:
                    print(" Connexion avec email réussie !")
                else:
                    print(" Connexion avec email échouée")
                    
            else:
                print(" Connexion échouée")
                
        else:
            print(" Inscription échouée")
            
    except Exception as e:
        print(f" Erreur test complet : {e}")
    
    # 4. Test de connexion avec utilisateur existant
    print(f"\n🔐 4. Test de connexion avec utilisateur existant...")
    
    existing_login = {
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        existing_response = requests.post(
            f"{base_url}/api/auth/login",
            json=existing_login,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Existing User Login Status: {existing_response.status_code}")
        print(f"Existing User Login Response: {existing_response.text}")
        
        if existing_response.status_code == 200:
            print(" Connexion utilisateur existant réussie !")
        else:
            print(" Connexion utilisateur existant échouée")
            
    except Exception as e:
        print(f" Erreur test utilisateur existant : {e}")
    
    # 5. Vérification des utilisateurs dans la base
    print(f"\n👥 5. Vérification des utilisateurs dans la base...")
    
    try:
        # Créer un utilisateur de test pour vérifier
        test_user_data = {
            "firstname": "Test",
            "lastname": "User",
            "username": f"testuser_{timestamp}",
            "email": f"testuser_{timestamp}@example.com",
            "password": "test123",
            "accountType": "particulier"
        }
        
        test_response = requests.post(
            f"{base_url}/api/auth/register",
            json=test_user_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if test_response.status_code == 200:
            print(" Utilisateur de test créé avec succès !")
            print(f"   Username: {test_user_data['username']}")
            print(f"   Email: {test_user_data['email']}")
        else:
            print(" Échec création utilisateur de test")
            
    except Exception as e:
        print(f" Erreur création utilisateur de test : {e}")

if __name__ == "__main__":
    test_complete_flow()
