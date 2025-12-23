#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour remplacer "Déménagement Zen" par "Déménagement Facile" 
dans toutes les pages de villes tout en conservant les optimisations SEO
"""

import os
import re
import glob

# Fichiers à modifier
PAGES = glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html")

REPLACEMENTS = [
    # Meta tags et titres
    (r'Déménagement Zen', 'Déménagement Facile'),
    (r'demenagement-zen\.fr', 'demenagement-facile.fr'),
    (r'contact@demenagement-zen\.fr', 'contact@demenagement-facile.fr'),
    (r'logo-demenagement-zen', 'logo-demenagement-facile'),
    (r'css/demenagement-zen\.css', 'css/styles.css'),
]

def corriger_fichier(filepath):
    """Corrige un fichier"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Appliquer les remplacements
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Correction du nom de marque dans les pages de villes...\n")
    
    corriges = 0
    for page in PAGES:
        if corriger_fichier(page):
            print(f"  OK: {page}")
            corriges += 1
        else:
            print(f"  (deja OK): {page}")
    
    print(f"\n{corriges} fichiers corriges!")

if __name__ == '__main__':
    main()

