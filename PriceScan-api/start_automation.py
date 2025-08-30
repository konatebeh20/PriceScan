#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démarrage rapide pour l'automatisation PriceScan
"""

import os
import sys
import subprocess
from datetime import datetime

def start_automation():
    """Démarre l'automatisation PriceScan"""
    print(" Démarrage de l'automatisation PriceScan")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('automation/daily_scraping.py'):
        print(" Erreur : Le script d'automatisation n'est pas trouvé")
        print("Assurez-vous d'être dans le répertoire PriceScan-api")
        return
    
    # Installer les dépendances si nécessaire
    print("📦 Vérification des dépendances...")
    try:
        import schedule
        print(" Module 'schedule' disponible")
    except ImportError:
        print(" Installation de 'schedule'...")
        subprocess.run([sys.executable, "-m", "pip", "install", "schedule"])
    
    # Créer le dossier automation s'il n'existe pas
    os.makedirs('automation/reports', exist_ok=True)
    
    print(" Configuration terminée")
    print("\n Démarrage du scraping intelligent...")
    
    # Démarrer l'automatisation
    try:
        subprocess.run([sys.executable, "automation/daily_scraping.py"])
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'automatisation")
    except Exception as e:
        print(f" Erreur : {e}")

def run_single_scraping():
    """Exécute un seul scraping (pour test)"""
    print("🧪 Exécution d'un scraping unique...")
    
    try:
        from helpers.scrapper.smart_scraper import SmartScraper
        
        scraper = SmartScraper()
        total_products = scraper.run_smart_scraping()
        
        print(f" Scraping terminé : {total_products} produits traités")
        
    except Exception as e:
        print(f" Erreur scraping : {e}")

def show_menu():
    """Affiche le menu principal"""
    print("\n🎯 MENU PRINCIPAL PRICESCAN")
    print("1. Démarrer l'automatisation quotidienne")
    print("2. Exécuter un scraping unique (test)")
    print("3. Vérifier la base de données")
    print("4. Quitter")
    
    choice = input("\nChoisissez une option (1-4) : ")
    
    if choice == "1":
        start_automation()
    elif choice == "2":
        run_single_scraping()
    elif choice == "3":
        check_database()
    elif choice == "4":
        print("👋 Au revoir !")
        return False
    else:
        print(" Option invalide")
    
    return True

def check_database():
    """Vérifie l'état de la base de données"""
    print(" Vérification de la base de données...")
    
    try:
        from check_mysql_data import check_mysql_data
        check_mysql_data()
    except Exception as e:
        print(f" Erreur vérification base : {e}")

def main():
    """Fonction principale"""
    print("🎉 BIENVENUE DANS PRICESCAN AUTOMATION")
    print(f"📅 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Boucle du menu
    while show_menu():
        pass

if __name__ == "__main__":
    main()
