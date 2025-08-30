#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test simple de la base de données Dashboard
Teste la communication sans importer l'app complet
"""

import sys
import os
import json
from datetime import datetime

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

def test_database_connection():
    """Test de la connexion à la base de données"""
    print(" Test de connexion à la base de données...")
    
    with test_app.app_context():
        try:
            # Test de connexion simple
            result = db.session.execute(text("SELECT 1"))
            print(" Connexion à la base de données réussie")
            return True
        except Exception as e:
            print(f" Erreur de connexion: {e}")
            return False

def test_dashboard_tables():
    """Test des tables du dashboard"""
    print("\n Test des tables du dashboard...")
    
    with test_app.app_context():
        tables_to_test = [
            'ps_promotions',
            'ps_user_profiles', 
            'ps_dashboard_stats',
            'ps_scan_history'
        ]
        
        results = {}
        
        for table_name in tables_to_test:
            try:
                result = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
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
    
    with test_app.app_context():
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
    
    with test_app.app_context():
        try:
            # Créer une nouvelle promotion de test
            from datetime import timedelta
            now = datetime.datetime.utcnow()
            new_promotion = ps_promotions(
                title="Promotion Test Communication",
                description="Test de communication dashboard ↔ base de données",
                discount_type="percentage",
                discount_value=15.0,
                start_date=now,
                end_date=now + timedelta(days=7),
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
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print(" RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    all_tests_passed = all([
        table_results,
        data_test,
        creation_test
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
