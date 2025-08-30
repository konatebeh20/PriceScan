#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test Rapide Jumia
Vérifie que le module Jumia fonctionne
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_jumia():
    """Test du module Jumia"""
    print("🧪 Test du module Jumia...")
    
    try:
        from helpers.scrapper.jumia import scraper_jumia
        
        # Test avec un produit simple
        print(" Recherche de 'smartphone'...")
        results = scraper_jumia("smartphone")
        
        if results:
            print(f" Succès! {len(results)} produits trouvés")
            print(f"📱 Premier produit: {results[0]}")
            return True
        else:
            print("  Aucun produit trouvé")
            return False
            
    except Exception as e:
        print(f" Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(" TEST RAPIDE JUMIA")
    print("=" * 30)
    
    success = test_jumia()
    
    if success:
        print("\n🎉 Test réussi !")
    else:
        print("\n Test échoué !")
