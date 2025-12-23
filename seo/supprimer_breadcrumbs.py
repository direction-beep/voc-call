#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour supprimer les breadcrumbs HTML des pages villes
"""

import os
import re
import glob

# Fichiers à modifier (exclure index.html)
PAGES = [f for f in glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html") 
         if f not in ["index.html", "carte-france.html"]]

BREADCRUMBS_PATTERN = r'<!-- Breadcrumbs -->\s*<nav aria-label="Fil d\'Ariane" class="breadcrumbs">.*?</nav>\s*'

def supprimer_breadcrumbs(filepath):
    """Supprime les breadcrumbs HTML d'un fichier"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Supprimer les breadcrumbs HTML (garder le Schema.org dans le head)
    content = re.sub(BREADCRUMBS_PATTERN, '', content, flags=re.DOTALL)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Suppression des breadcrumbs HTML des pages villes...\n")
    
    corriges = 0
    for page in PAGES:
        if supprimer_breadcrumbs(page):
            print(f"  OK: {page}")
            corriges += 1
    
    print(f"\n{corriges} fichiers modifiés!")

if __name__ == '__main__':
    main()

