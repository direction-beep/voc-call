#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour uniformiser le header sur toutes les pages
"""

import os
import re
import glob

# Fichiers à modifier (exclure index.html et carte-france.html qui sont déjà corrects)
PAGES = [f for f in glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html") 
         if f not in ["index.html", "carte-france.html"]]

HEADER_OLD = r'''<header class="header">
\s*<nav class="navbar">
\s*<div class="nav-container">
\s*<div class="nav-logo">
\s*<a href="index\.html" class="logo">
\s*<img[^>]*>
\s*<span>Déménagement Zen</span>
\s*</a>
\s*</div>
\s*<div class="nav-menu"[^>]*>
\s*<ul class="nav-list">
\s*.*?
\s*</ul>
\s*</div>
\s*<button class="nav-toggle"[^>]*>.*?</button>
\s*</div>
\s*</nav>
\s*</header>'''

HEADER_NEW = '''    <header class="header">
        <nav class="navbar">
            <div class="container">
                <div class="nav-logo">
                    <a href="index.html" class="logo">
                        <img src="images/logo-demenagement-zen.svg" onerror="this.onerror=null; this.src='images/logo-demenagement-zen.png'" alt="Déménagement Zen Logo" width="150" height="40">
                    </a>
                </div>
                <div class="nav-menu">
                    <ul class="nav-list">
                        <li><a href="index.html">Accueil</a></li>
                        <li><a href="index.html#services">Services</a></li>
                        <li><a href="carte-france.html">Nos villes</a></li>
                        <li><a href="index.html#contact">Contact</a></li>
                    </ul>
                    <a href="index.html#devis" class="btn btn-primary-nav">Devis gratuit</a>
                </div>
                <button class="mobile-menu-toggle" aria-label="Menu mobile">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </nav>
    </header>'''

def uniformiser_header(filepath):
    """Uniformise le header d'un fichier"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remplacer le header
    content = re.sub(HEADER_OLD, HEADER_NEW, content, flags=re.DOTALL)
    
    # Si le remplacement n'a pas fonctionné, essayer une approche plus simple
    if content == original_content:
        # Chercher juste la div nav-container
        content = re.sub(
            r'<div class="nav-container">',
            r'<div class="container">',
            content
        )
        # Retirer le span Déménagement Zen
        content = re.sub(
            r'<span>Déménagement Zen</span>',
            r'',
            content
        )
        # Remplacer nav-toggle par mobile-menu-toggle
        content = re.sub(
            r'<button class="nav-toggle"[^>]*>',
            r'<button class="mobile-menu-toggle" aria-label="Menu mobile">',
            content
        )
        # Remplacer les bar par span
        content = re.sub(
            r'<span class="bar"></span>',
            r'<span></span>',
            content
        )
        # S'assurer que le menu a la bonne structure
        if 'btn-primary-nav' not in content:
            # Chercher la fin de </ul> dans nav-menu et ajouter le bouton
            content = re.sub(
                r'(</ul>\s*</div>\s*<button class="mobile-menu-toggle")',
                r'</ul>\n                    <a href="index.html#devis" class="btn btn-primary-nav">Devis gratuit</a>\n                </div>\n                <button class="mobile-menu-toggle"',
                content
            )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Uniformisation du header sur toutes les pages...\n")
    
    corriges = 0
    for page in PAGES:
        if uniformiser_header(page):
            print(f"  OK: {page}")
            corriges += 1
        else:
            print(f"  (déjà OK ou non modifié): {page}")
    
    print(f"\n{corriges} fichiers modifiés!")

if __name__ == '__main__':
    main()

