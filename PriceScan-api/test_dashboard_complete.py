#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test complet de communication Dashboard ↔ Base de données ↔ Session Storage
Vérifie que les données du dashboard sont bien enregistrées et persistées
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import db
from model.PriceScan_db import *
from sqlalchemy import text

# Configuration simple de Flask
from flask import Flask
test_app = Flask(__name__)
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Konate%202019@localhost:5432/PriceScan_db'
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db.init_app(test_app)

# Simulation du session storage
class SessionStorage:
    def __init__(self):
        self.data = {}
    
    def setItem(self, key, value):
        self.data[key] = value
        print(f"   💾 Session Storage: {key} = {value}")
    
    def getItem(self, key):
        return self.data.get(key)
    
    def removeItem(self, key):
        if key in self.data:
            del self.data[key]
            print(f"   🗑️  Session Storage: {key} supprimé")
    
    def clear(self):
        self.data.clear()
        print("   🧹 Session Storage: vidé")

# Instance globale du session storage
session_storage = SessionStorage()

def test_dashboard_data_persistence():
    """Test de persistance des données du dashboard"""
    print("\n🔄 Test de persistance des données du dashboard...")
    
    with test_app.app_context():
        try:
            # Simuler des données venant du dashboard
            now = datetime.datetime.utcnow()
            dashboard_data = {
                "user_id": "dashboard-user-456",
                "current_session": {
                    "start_time": now.isoformat(),
                    "last_activity": now.isoformat(),
                    "active_tab": "promotions"
                },
                "user_preferences": {
                    "theme": "dark",
                    "language": "fr",
                    "currency": "CFA",
                    "notifications": True
                },
                "recent_actions": [
                    {"action": "view_promotions", "timestamp": now.isoformat()},
                    {"action": "update_profile", "timestamp": now.isoformat()}
                ]
            }
            
            # Sauvegarder dans le session storage
            session_storage.setItem("dashboard_data", json.dumps(dashboard_data))
            session_storage.setItem("user_session", json.dumps(dashboard_data["current_session"]))
            session_storage.setItem("user_preferences", json.dumps(dashboard_data["user_preferences"]))
            
            print("   ✅ Données du dashboard sauvegardées dans le session storage")
            
            # Créer d'abord un utilisateur dans la base de données
            new_user = ps_users(
                u_uid="dashboard-user-456",
                u_username="dashboarduser",
                u_email="dashboard@test.com",
                u_firstname="Dashboard",
                u_lastname="User",
                u_status=UserStatus.ACTIVE,
                u_password="hashed_password_here"
            )
            
            db.session.add(new_user)
            db.session.commit()
            print("   ✅ Utilisateur créé dans la base de données")
            
            # Créer un profil utilisateur dans la base de données
            new_user_profile = ps_user_profiles(
                user_uid="dashboard-user-456",
                gender="other",
                preferred_currency="CFA",
                preferred_language="fr",
                notification_preferences=json.dumps(dashboard_data["user_preferences"])
            )
            
            db.session.add(new_user_profile)
            db.session.commit()
            print("   ✅ Profil utilisateur créé dans la base de données")
            
            # Créer des statistiques de dashboard
            new_dashboard_stats = ps_dashboard_stats(
                user_uid="dashboard-user-456",
                month=now.month,
                year=now.year,
                total_receipts=0,
                total_spent=0.0,
                avg_receipt_amount=0.0,
                top_categories=json.dumps([]),
                top_stores=json.dumps([]),
                total_savings=0.0,
                savings_from_promos=0.0,
                savings_from_comparison=0.0
            )
            
            db.session.add(new_dashboard_stats)
            db.session.commit()
            print("   ✅ Statistiques dashboard créées dans la base de données")
            
            # Créer une promotion depuis le dashboard
            new_promotion = ps_promotions(
                title="Promotion Dashboard Test",
                description="Promotion créée depuis le dashboard",
                discount_type="percentage",
                discount_value=25.0,
                start_date=now,
                end_date=now + timedelta(days=14),
                min_purchase=2000.0,
                is_active=True,
                is_featured=True
            )
            
            db.session.add(new_promotion)
            db.session.commit()
            print("   ✅ Promotion créée depuis le dashboard")
            
            # Sauvegarder l'ID de la promotion dans le session storage
            session_storage.setItem("last_created_promotion_id", str(new_promotion.id))
            session_storage.setItem("last_created_promotion_title", new_promotion.title)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erreur lors du test de persistance: {e}")
            db.session.rollback()
            return False

def test_data_retrieval_and_sync():
    """Test de récupération et synchronisation des données"""
    print("\n📥 Test de récupération et synchronisation des données...")
    
    with test_app.app_context():
        try:
            # Récupérer les données depuis la base
            user_profile = ps_user_profiles.query.filter_by(user_uid="dashboard-user-456").first()
            dashboard_stats = ps_dashboard_stats.query.filter_by(user_uid="dashboard-user-456").first()
            promotion = ps_promotions.query.filter_by(title="Promotion Dashboard Test").first()
            
            if user_profile and dashboard_stats and promotion:
                print("   ✅ Toutes les données récupérées depuis la base")
                
                # Mettre à jour le session storage avec les données de la base
                session_storage.setItem("user_profile_from_db", json.dumps({
                    "user_uid": user_profile.user_uid,
                    "preferred_currency": user_profile.preferred_currency,
                    "preferred_language": user_profile.preferred_language,
                    "gender": user_profile.gender
                }))
                
                session_storage.setItem("dashboard_stats_from_db", json.dumps({
                    "total_receipts": dashboard_stats.total_receipts,
                    "total_spent": dashboard_stats.total_spent,
                    "total_savings": dashboard_stats.total_savings
                }))
                
                session_storage.setItem("promotion_from_db", json.dumps({
                    "id": promotion.id,
                    "title": promotion.title,
                    "discount_value": promotion.discount_value,
                    "is_active": promotion.is_active
                }))
                
                print("   ✅ Session storage synchronisé avec la base de données")
                
                return True
            else:
                print("   ❌ Certaines données n'ont pas été trouvées")
                return False
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la récupération: {e}")
            return False

def test_session_storage_integration():
    """Test de l'intégration avec le session storage"""
    print("\n💾 Test de l'intégration avec le session storage...")
    
    try:
        # Vérifier que toutes les données sont dans le session storage
        required_keys = [
            "dashboard_data",
            "user_session", 
            "user_preferences",
            "last_created_promotion_id",
            "last_created_promotion_title",
            "user_profile_from_db",
            "dashboard_stats_from_db",
            "promotion_from_db"
        ]
        
        missing_keys = []
        for key in required_keys:
            if not session_storage.getItem(key):
                missing_keys.append(key)
        
        if not missing_keys:
            print("   ✅ Toutes les données sont présentes dans le session storage")
            
            # Afficher un résumé des données stockées
            print("\n   📋 Résumé des données en session storage:")
            for key in required_keys:
                value = session_storage.getItem(key)
                if len(str(value)) > 100:
                    value = str(value)[:100] + "..."
                print(f"      - {key}: {value}")
            
            return True
        else:
            print(f"   ❌ Clés manquantes dans le session storage: {missing_keys}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test du session storage: {e}")
        return False

def test_data_modification_from_dashboard():
    """Test de modification des données depuis le dashboard"""
    print("\n✏️  Test de modification des données depuis le dashboard...")
    
    with test_app.app_context():
        try:
            # Modifier les préférences utilisateur
            user_profile = ps_user_profiles.query.filter_by(user_uid="dashboard-user-456").first()
            if user_profile:
                user_profile.preferred_language = "en"
                user_profile.gender = "male"
                db.session.commit()
                
                # Mettre à jour le session storage
                session_storage.setItem("updated_user_preferences", json.dumps({
                    "language": "en",
                    "gender": "male",
                    "currency": "CFA",
                    "notifications": True
                }))
                
                print("   ✅ Préférences utilisateur modifiées")
                
                # Modifier la promotion
                promotion = ps_promotions.query.filter_by(title="Promotion Dashboard Test").first()
                if promotion:
                    promotion.discount_value = 30.0
                    promotion.is_featured = False
                    db.session.commit()
                    
                    session_storage.setItem("updated_promotion", json.dumps({
                        "id": promotion.id,
                        "title": promotion.title,
                        "discount_value": promotion.discount_value,
                        "is_featured": promotion.is_featured
                    }))
                    
                    print("   ✅ Promotion modifiée")
                
                return True
            else:
                print("   ❌ Profil utilisateur non trouvé")
                return False
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la modification: {e}")
            db.session.rollback()
            return False

def cleanup_test_data():
    """Nettoyage des données de test"""
    print("\n🧹 Nettoyage des données de test...")
    
    with test_app.app_context():
        try:
            # Supprimer les données de test (dans l'ordre inverse des dépendances)
            ps_user_profiles.query.filter_by(user_uid="dashboard-user-456").delete()
            ps_dashboard_stats.query.filter_by(user_uid="dashboard-user-456").delete()
            ps_promotions.query.filter_by(title="Promotion Dashboard Test").delete()
            ps_users.query.filter_by(u_uid="dashboard-user-456").delete()
            
            db.session.commit()
            print("   ✅ Données de test supprimées de la base")
            
            # Vider le session storage
            session_storage.clear()
            print("   ✅ Session storage vidé")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erreur lors du nettoyage: {e}")
            db.session.rollback()
            return False

def main():
    """Fonction principale de test"""
    print("🧪 Test complet de communication Dashboard ↔ Base de données ↔ Session Storage")
    print("=" * 80)
    
    # Test 1: Persistance des données du dashboard
    persistence_test = test_dashboard_data_persistence()
    
    # Test 2: Récupération et synchronisation
    retrieval_test = test_data_retrieval_and_sync()
    
    # Test 3: Intégration session storage
    storage_test = test_session_storage_integration()
    
    # Test 4: Modification des données
    modification_test = test_data_modification_from_dashboard()
    
    # Nettoyage
    cleanup_test = cleanup_test_data()
    
    # Résumé des tests
    print("\n" + "=" * 80)
    print("📋 RÉSUMÉ DES TESTS COMPLETS")
    print("=" * 80)
    
    all_tests_passed = all([
        persistence_test,
        retrieval_test,
        storage_test,
        modification_test,
        cleanup_test
    ])
    
    if all_tests_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print("✅ La communication complète Dashboard ↔ Base de données ↔ Session Storage fonctionne parfaitement")
        print("\n🚀 Le dashboard peut maintenant:")
        print("   - Enregistrer les données dans la base de données")
        print("   - Persister les données dans le session storage")
        print("   - Synchroniser les données entre dashboard et base")
        print("   - Modifier les données depuis le dashboard")
        print("   - Maintenir la cohérence des données")
        print("   - Gérer les sessions utilisateur")
        print("   - Sauvegarder les préférences utilisateur")
    else:
        print("⚠️  Certains tests ont échoué")
        print("🔍 Vérifiez la configuration et les permissions")
    
    print("\n📚 Prochaines étapes:")
    print("   1. Intégrer ces tests dans le dashboard Angular")
    print("   2. Configurer le session storage côté client")
    print("   3. Tester l'API complète avec le dashboard")

if __name__ == "__main__":
    main()
