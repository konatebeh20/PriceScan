#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🗄️ Script de création des tables du dashboard
Crée les nouvelles tables nécessaires pour le dashboard
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import datetime
from datetime import timedelta
from sqlalchemy import text
from config.db import db
from model.PriceScan_db import *
from config.environment import get_config
from app import app

def create_dashboard_tables():
    """Crée les nouvelles tables du dashboard"""
    print(" Création des tables du dashboard...")
    
    with app.app_context():
        try:
            # Créer toutes les tables
            db.create_all()
            print(" Toutes les tables ont été créées avec succès!")
            
            # Vérifier que les nouvelles tables existent
            new_tables = [
                'ps_promotions',
                'ps_user_profiles', 
                'ps_dashboard_stats',
                'ps_scan_history'
            ]
            
            print("\n Vérification des nouvelles tables:")
            for table_name in new_tables:
                try:
                    # Vérifier si la table existe en essayant une requête simple
                    result = db.session.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
                    print(f"    {table_name} - Table créée et accessible")
                except Exception as e:
                    print(f"    {table_name} - Erreur: {e}")
            
            print("\n🎯 Tables du dashboard prêtes!")
            return True
            
        except Exception as e:
            print(f" Erreur lors de la création des tables: {e}")
            return False

def insert_sample_data():
    """Insère des données d'exemple pour tester le dashboard"""
    print("\n Insertion de données d'exemple...")
    
    with app.app_context():
        try:
            # Créer une catégorie d'exemple
            sample_category = ps_categories(
                cat_label="Électronique",
                cat_description="Produits électroniques et gadgets",
                cat_is_featured=True,
                cat_is_active=True,
                cat_icon="phone-portrait"
            )
            db.session.add(sample_category)
            
            # Créer un magasin d'exemple
            sample_store = ps_stores(
                store_name="ElectroShop",
                store_address="123 Avenue des Technologies",
                store_city="Abidjan",
                store_country="Côte d'Ivoire",
                store_phone="+225 0123456789",
                store_email="contact@electroshop.ci",
                store_is_active=True
            )
            db.session.add(sample_store)
            
            # Créer un produit d'exemple
            sample_product = ps_products(
                product_name="Smartphone Test",
                product_description="Smartphone de test pour le dashboard",
                product_brand="TestBrand",
                product_barcode="1234567890123",
                product_is_active=True
            )
            db.session.add(sample_product)
            
            # Créer une promotion d'exemple
            sample_promotion = ps_promotions(
                title="Promotion Test Dashboard",
                description="Promotion de test pour vérifier le fonctionnement",
                discount_type="percentage",
                discount_value=20.0,
                start_date=datetime.datetime.utcnow(),
                end_date=datetime.datetime.utcnow() + timedelta(days=30),
                min_purchase=5000.0,
                is_active=True,
                is_featured=True
            )
            db.session.add(sample_promotion)
            
            # Créer un utilisateur de test
            sample_user = ps_users(
                u_uid="test-user-123",
                u_username="testuser",
                u_email="test@dashboard.com",
                u_firstname="Test",
                u_lastname="User",
                u_status=UserStatus.ACTIVE,
                u_password="hashed_password_here"
            )
            db.session.add(sample_user)
            
            # Créer un profil utilisateur de test
            sample_profile = ps_user_profiles(
                user_uid="test-user-123",
                gender="other",
                preferred_currency="CFA",
                preferred_language="fr",
                notification_preferences=json.dumps({
                    "email_notifications": True,
                    "push_notifications": True,
                    "price_alerts": True
                })
            )
            db.session.add(sample_profile)
            
            # Créer des statistiques de test
            sample_stats = ps_dashboard_stats(
                user_uid="test-user-123",
                month=datetime.datetime.utcnow().month,
                year=datetime.datetime.utcnow().year,
                total_receipts=5,
                total_spent=25000.0,
                avg_receipt_amount=5000.0,
                top_categories=json.dumps([
                    {"category": "Électronique", "total_spent": 15000.0, "purchase_count": 3},
                    {"category": "Alimentation", "total_spent": 10000.0, "purchase_count": 2}
                ]),
                top_stores=json.dumps([
                    {"store_name": "ElectroShop", "total_spent": 15000.0, "visit_count": 3},
                    {"store_name": "SuperMarché", "total_spent": 10000.0, "visit_count": 2}
                ]),
                total_savings=2500.0,
                savings_from_promos=1500.0,
                savings_from_comparison=1000.0
            )
            db.session.add(sample_stats)
            
            # Valider toutes les modifications
            db.session.commit()
            print(" Données d'exemple insérées avec succès!")
            
            # Afficher un résumé
            print("\n Résumé des données créées:")
            print(f"   - Catégorie: {sample_category.cat_label}")
            print(f"   - Magasin: {sample_store.store_name}")
            print(f"   - Produit: {sample_product.product_name}")
            print(f"   - Promotion: {sample_promotion.title}")
            print(f"   - Utilisateur: {sample_user.u_username}")
            print(f"   - Profil: {sample_profile.user_uid}")
            print(f"   - Stats: {sample_stats.total_receipts} reçus, {sample_stats.total_spent} CFA")
            
            return True
            
        except Exception as e:
            print(f" Erreur lors de l'insertion des données: {e}")
            db.session.rollback()
            return False

def main():
    """Fonction principale"""
    print("🗄️  Script de création des tables du dashboard")
    print("=" * 50)
    
    # Créer les tables
    if create_dashboard_tables():
        print("\n Tables créées avec succès!")
        
        # Demander si l'utilisateur veut insérer des données d'exemple
        response = input("\n🤔 Voulez-vous insérer des données d'exemple? (y/n): ")
        if response.lower() in ['y', 'yes', 'o', 'oui']:
            if insert_sample_data():
                print("\n🎉 Configuration du dashboard terminée!")
                print("\n Prochaines étapes:")
                print("   1. Lancer l'API: python app.py")
                print("   2. Tester la communication: python test_dashboard_communication.py")
                print("   3. Lancer le dashboard Angular")
            else:
                print("\n  Erreur lors de l'insertion des données d'exemple")
        else:
            print("\n Configuration terminée sans données d'exemple")
    else:
        print("\n Erreur lors de la création des tables")

if __name__ == "__main__":
    main()
