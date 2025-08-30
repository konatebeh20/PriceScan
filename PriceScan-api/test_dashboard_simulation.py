#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de simulation du comportement du dashboard Angular
"""

import requests
import json
import time

def simulate_dashboard_behavior():
    """Simule le comportement exact du dashboard Angular"""
    base_url = "http://localhost:5000"
    
    print("🎭 SIMULATION DU COMPORTEMENT DU DASHBOARD ANGULAR")
    print("=" * 60)
    
    # Simuler l'inscription comme le fait le dashboard
    print("\n📝 1. Simulation d'inscription (comme dashboard)...")
    
    timestamp = int(time.time())
    dashboard_email = f"dashboard_user_{timestamp}@example.com"
    
    # Le dashboard génère un username unique basé sur l'email
    dashboard_username = f"dashboard_user_{timestamp}"
    
    dashboard_register_data = {
        "firstname": "Dashboard",
        "lastname": "User",
        "username": dashboard_username,
        "email": dashboard_email,
        "password": "dashboard123",
        "accountType": "particulier"
    }
    
    print(f"📤 Données envoyées par le dashboard:")
    print(f"   Username: {dashboard_username}")
    print(f"   Email: {dashboard_email}")
    print(f"   Firstname: {dashboard_register_data['firstname']}")
    print(f"   Lastname: {dashboard_register_data['lastname']}")
    print(f"   AccountType: {dashboard_register_data['accountType']}")
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=dashboard_register_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'http://localhost:4200'
            },
            timeout=10
        )
        
        print(f"\n📡 Réponse de l'API:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print(" Inscription réussie !")
            user_data = response.json()
            
            # Simuler la connexion comme le fait le dashboard
            print(f"\n🔐 2. Simulation de connexion (comme dashboard)...")
            
            # Le dashboard envoie email comme username
            dashboard_login_data = {
                "username": dashboard_email,  # Le dashboard envoie l'email
                "password": "dashboard123"
            }
            
            print(f"📤 Données de connexion envoyées par le dashboard:")
            print(f"   Username (email): {dashboard_email}")
            print(f"   Password: {dashboard_login_data['password']}")
            
            login_response = requests.post(
                f"{base_url}/api/auth/login",
                json=dashboard_login_data,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Origin': 'http://localhost:4200'
                },
                timeout=10
            )
            
            print(f"\n📡 Réponse de connexion:")
            print(f"   Status: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
            if login_response.status_code == 200:
                print(" Connexion réussie !")
                print("🎉 Le dashboard devrait maintenant rediriger vers le dashboard principal !")
            else:
                print(" Connexion échouée")
                
        else:
            print(" Inscription échouée")
            
    except Exception as e:
        print(f" Erreur simulation dashboard : {e}")
    
    # Test avec des données exactes du formulaire du dashboard
    print(f"\n📝 3. Test avec données exactes du formulaire dashboard...")
    
    form_email = f"form_test_{timestamp}@example.com"
    form_username = f"form_test_{timestamp}"
    
    form_data = {
        "firstname": "Form",
        "lastname": "Test",
        "username": form_username,
        "email": form_email,
        "password": "form123",
        "accountType": "particulier"
    }
    
    print(f"📤 Données du formulaire:")
    for key, value in form_data.items():
        print(f"   {key}: {value}")
    
    try:
        form_response = requests.post(
            f"{base_url}/api/auth/register",
            json=form_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'http://localhost:4200'
            },
            timeout=10
        )
        
        print(f"\n📡 Réponse formulaire:")
        print(f"   Status: {form_response.status_code}")
        print(f"   Response: {form_response.text}")
        
        if form_response.status_code == 200:
            print(" Formulaire traité avec succès !")
        else:
            print(" Échec traitement formulaire")
            
    except Exception as e:
        print(f" Erreur formulaire : {e}")

if __name__ == "__main__":
    simulate_dashboard_behavior()
