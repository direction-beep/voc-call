#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour restaurer "Déménagement Zen" partout et remettre le logo
"""

import os
import re
import glob

# Fichiers à modifier
PAGES = glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html") + ["index.html"]

REPLACEMENTS = [
    # Nom de marque
    (r'Déménagement Facile', 'Déménagement Zen'),
    (r'demenagement-facile\.fr', 'demenagement-zen.fr'),
    (r'contact@demenagement-facile\.fr', 'contact@demenagement-zen.fr'),
    (r'logo\.(svg|png)', r'logo-demenagement-zen.\1'),
    (r'og-image\.jpg', 'demenagement-zen-og.jpg'),
    (r'css/styles\.css', 'css/demenagement-zen.css'),
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
    print("Restauration de Déménagement Zen et du logo...\n")
    
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

