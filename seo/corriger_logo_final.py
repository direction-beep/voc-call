#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger le logo sur toutes les pages qui n'ont que le texte
"""

import os
import re
import glob

# Fichiers à modifier
PAGES = glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html")
PAGES = [f for f in PAGES if f not in ["index.html", "carte-france.html"]]

def corriger_logo(filepath):
    """Corrige le logo d'un fichier"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Chercher le pattern exact du logo texte
    pattern_logo_texte = r'<div class="nav-logo">\s*<a href="index\.html" class="logo">Déménagement Zen</a>\s*</div>'
    
    if re.search(pattern_logo_texte, content):
        # Remplacer par le logo image
        nouveau_logo = '''<div class="nav-logo">
                    <a href="index.html" class="logo">
                        <img src="images/logo-demenagement-zen.svg" onerror="this.onerror=null; this.src='images/logo-demenagement-zen.png'" alt="Déménagement Zen Logo" width="150" height="40">
                    </a>
                </div>'''
        content = re.sub(pattern_logo_texte, nouveau_logo, content)
    
    # Corriger le menu si nécessaire
    if 'carte-france.html' not in content[:5000] or 'index.html#devis' not in content[:5000]:
        # Chercher et remplacer le menu
        pattern_menu = r'<ul class="nav-list">.*?</ul>'
        menu_match = re.search(pattern_menu, content[:5000], re.DOTALL)
        if menu_match:
            nouveau_menu = '''<ul class="nav-list">
                        <li><a href="index.html">Accueil</a></li>
                        <li><a href="index.html#services">Services</a></li>
                        <li><a href="carte-france.html">Nos villes</a></li>
                        <li><a href="index.html#contact">Contact</a></li>
                    </ul>'''
            # Remplacer seulement dans le header
            header_section = content[:5000]
            header_section = re.sub(pattern_menu, nouveau_menu, header_section, flags=re.DOTALL)
            content = header_section + content[5000:]
        
        # Corriger le bouton devis
        if 'devis-' in content[:5000] and 'index.html#devis' not in content[:5000]:
            content = re.sub(
                r'<a href="devis-[^"]*\.html" class="btn btn-primary-nav">Devis gratuit</a>',
                r'<a href="index.html#devis" class="btn btn-primary-nav">Devis gratuit</a>',
                content
            )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Correction du logo sur toutes les pages...\n")
    
    corriges = 0
    
    for page in sorted(PAGES):
        if corriger_logo(page):
            print(f"  CORRIGE: {page}")
            corriges += 1
    
    print(f"\n{'='*60}")
    print(f"Resume:")
    print(f"  - Pages corrigees: {corriges}")
    print(f"  - Total: {len(PAGES)} pages")

if __name__ == '__main__':
    main()

