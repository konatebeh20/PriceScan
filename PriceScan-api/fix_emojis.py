#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger tous les emojis dans l'auto_scraper.py
"""

import re

def fix_emojis_in_file(file_path):
    """Corrige tous les emojis dans un fichier"""
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer tous les emojis par du texte simple
    replacements = {
        '': 'ERREUR',
        '': 'SUCCES',
        '💾': 'SAUVEGARDE',
        '': 'SYNC',
        '🎯': 'CIBLE',
        '': 'STATS',
        '🤖': 'ROBOT',
        '': 'DEMARRAGE',
        '🛑': 'ARRET',
        '': 'ATTENTION',
        'ℹ️': 'INFO',
        'ℹ': 'INFO'
    }
    
    # Appliquer les remplacements
    for emoji, replacement in replacements.items():
        content = content.replace(emoji, replacement)
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f" Fichier {file_path} corrigé avec succès")

if __name__ == '__main__':
    file_path = 'helpers/auto_scraper.py'
    fix_emojis_in_file(file_path)
