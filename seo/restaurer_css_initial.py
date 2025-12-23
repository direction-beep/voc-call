#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour restaurer le CSS initial (styles.css) dans toutes les pages
"""

import os
import re
import glob

# Fichiers à modifier
PAGES = glob.glob("*.html") + glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html")

def restaurer_css(filepath):
    """Remplace demenagement-zen.css par styles.css"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remplacer le CSS
    content = re.sub(
        r'css/demenagement-zen\.css',
        r'css/styles.css',
        content
    )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Restauration du CSS initial (styles.css) dans toutes les pages...\n")
    
    corriges = 0
    for page in PAGES:
        if restaurer_css(page):
            print(f"  OK: {page}")
            corriges += 1
    
    print(f"\n{corriges} fichiers modifiés!")

if __name__ == '__main__':
    main()

