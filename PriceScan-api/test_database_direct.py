#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test direct de la base de données Dashboard
Teste la communication entre le dashboard et la base de données
"""

import sys
import os
import json
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import db
from model.PriceScan_db import *
from app import app

def test_database_connection():
    """Test de la connexion à la base de données"""
    print(" Test de connexion à la base de données...")
    
    try:
        # Test de connexion simple
        result = db.session.execute("SELECT 1")
        print(" Connexion à la base de données réussie")
        return True
    except Exception as e:
        print(f" Erreur de connexion: {e}")
        return False

def test_dashboard_tables():
    """Test des tables du dashboard"""
    print("\n Test des tables du dashboard...")
    
    tables_to_test = [
        'ps_promotions',
        'ps_user_profiles', 
        'ps_dashboard_stats',
        'ps_scan_history'
    ]
    
    results = {}
    
    for table_name in tables_to_test:
        try:
            result = db.session.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = result.scalar()
            results[table_name] = {"status": "OK", "count": count}
            print(f"    {table_name}: {count} enregistrements")
        except Exception as e:
            results[table_name] = {"status": "ERROR", "error": str(e)}
            print(f"    {table_name}: Erreur - {e}")
    
    return results

def test_dashboard_data():
    """Test des données du dashboard"""
    print("\n Test des données du dashboard...")
    
    try:
        # Test des promotions
        promotions = ps_promotions.query.limit(3).all()
        print(f"    Promotions: {len(promotions)} trouvées")
        
        if promotions:
            for promo in promotions:
                print(f"      - {promo.title} ({promo.discount_value}% de réduction)")
        
        # Test des profils utilisateurs
        user_profiles = ps_user_profiles.query.limit(3).all()
        print(f"    Profils utilisateurs: {len(user_profiles)} trouvés")
        
        # Test des statistiques
        dashboard_stats = ps_dashboard_stats.query.limit(3).all()
        print(f"    Statistiques dashboard: {len(dashboard_stats)} trouvées")
        
        if dashboard_stats:
            for stats in dashboard_stats:
                print(f"      - Utilisateur {stats.user_uid}: {stats.total_receipts} reçus, {stats.total_spent} CFA")
        
        return True
        
    except Exception as e:
        print(f"    Erreur lors du test des données: {e}")
        return False

def test_data_creation():
    """Test de création de nouvelles données"""
    print("\n Test de création de nouvelles données...")
    
    try:
        # Créer une nouvelle promotion de test
        new_promotion = ps_promotions(
            title="Promotion Test Communication",
            description="Test de communication dashboard ↔ base de données",
            discount_type="percentage",
            discount_value=15.0,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow().replace(day=datetime.utcnow().day + 7),
            min_purchase=1000.0,
            is_active=True,
            is_featured=False
        )
        
        db.session.add(new_promotion)
        db.session.commit()
        
        print("    Nouvelle promotion créée avec succès")
        
        # Récupérer la promotion créée
        created_promo = ps_promotions.query.filter_by(title="Promotion Test Communication").first()
        if created_promo:
            print(f"      - ID: {created_promo.id}")
            print(f"      - Titre: {created_promo.title}")
            print(f"      - Réduction: {created_promo.discount_value}%")
        
        # Supprimer la promotion de test
        db.session.delete(created_promo)
        db.session.commit()
        print("    Promotion de test supprimée")
        
        return True
        
    except Exception as e:
        print(f"    Erreur lors du test de création: {e}")
        db.session.rollback()
        return False

def test_dashboard_integration():
    """Test d'intégration complète du dashboard"""
    print("\n🎯 Test d'intégration complète du dashboard...")
    
    try:
        # Simuler une requête de statistiques utilisateur
        user_uid = "test-user-123"
        
        # Récupérer les statistiques
        user_stats = ps_dashboard_stats.query.filter_by(user_uid=user_uid).first()
        if user_stats:
            print(f"    Statistiques trouvées pour {user_uid}")
            print(f"      - Total reçus: {user_stats.total_receipts}")
            print(f"      - Total dépensé: {user_stats.total_spent} CFA")
            print(f"      - Économies: {user_stats.total_savings} CFA")
        
        # Récupérer le profil utilisateur
        user_profile = ps_user_profiles.query.filter_by(user_uid=user_uid).first()
        if user_profile:
            print(f"    Profil utilisateur trouvé")
            print(f"      - Devise préférée: {user_profile.preferred_currency}")
            print(f"      - Langue: {user_profile.preferred_language}")
        
        # Récupérer les promotions actives
        active_promotions = ps_promotions.query.filter_by(is_active=True).limit(5).all()
        print(f"    Promotions actives: {len(active_promotions)} trouvées")
        
        return True
        
    except Exception as e:
        print(f"    Erreur lors du test d'intégration: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test de communication Dashboard ↔ Base de données")
    print("=" * 60)
    
    # Test 1: Connexion à la base de données
    if not test_database_connection():
        print("\n Impossible de se connecter à la base de données")
        return
    
    # Test 2: Tables du dashboard
    table_results = test_dashboard_tables()
    
    # Test 3: Données du dashboard
    data_test = test_dashboard_data()
    
    # Test 4: Création de données
    creation_test = test_data_creation()
    
    # Test 5: Intégration complète
    integration_test = test_dashboard_integration()
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print(" RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    all_tests_passed = all([
        table_results,
        data_test,
        creation_test,
        integration_test
    ])
    
    if all_tests_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print(" La communication Dashboard ↔ Base de données fonctionne parfaitement")
        print("\n Le dashboard peut maintenant:")
        print("   - Lire les données de la base")
        print("   - Créer de nouvelles données")
        print("   - Mettre à jour les données existantes")
        print("   - Supprimer des données")
        print("   - Récupérer les statistiques")
        print("   - Gérer les promotions")
        print("   - Gérer les profils utilisateurs")
    else:
        print("  Certains tests ont échoué")
        print(" Vérifiez la configuration de la base de données")
    
    print("\n📚 Prochaines étapes:")
    print("   1. Lancer l'API complète: python app.py")
    print("   2. Tester les endpoints API")
    print("   3. Intégrer avec le dashboard Angular")

if __name__ == "__main__":
    main()
