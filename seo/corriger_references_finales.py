#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger toutes les références restantes à Déménagement Zen
"""

import os
import re
import glob

PAGES = glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html")

def corriger_fichier(filepath):
    """Corrige un fichier"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remplacements
    replacements = [
        (r'Déménageur Zen', 'Déménagement Facile'),
        (r'demenagement-zen-og\.jpg', 'og-image.jpg'),
        (r'logo-demenagement-zen\.(svg|png)', r'logo.\1'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Correction des références finales...\n")
    
    corriges = 0
    for page in PAGES:
        if corriger_fichier(page):
            print(f"  OK: {page}")
            corriges += 1
    
    print(f"\n{corriges} fichiers corriges!")

if __name__ == '__main__':
    main()

