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

# Header standard avec logo
HEADER_STANDARD = '''    <!-- Header -->
    <header class="header">
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

def corriger_logo(filepath):
    """Corrige le logo d'un fichier"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Vérifier si le logo image est présent dans le header
    header_match = re.search(r'<!-- Header -->.*?</header>', content, re.DOTALL)
    if header_match:
        header_actuel = header_match.group(0)
        
        # Si le logo image n'est pas présent, remplacer le header
        if 'logo-demenagement-zen.svg' not in header_actuel and 'logo-demenagement-zen.png' not in header_actuel:
            # Remplacer le header
            content = re.sub(
                r'<!-- Header -->.*?</header>',
                HEADER_STANDARD,
                content,
                flags=re.DOTALL
            )
        # Si le menu n'est pas standard, corriger
        elif 'carte-france.html' not in header_actuel or 'index.html#devis' not in header_actuel:
            # Remplacer le header
            content = re.sub(
                r'<!-- Header -->.*?</header>',
                HEADER_STANDARD,
                content,
                flags=re.DOTALL
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
    deja_ok = 0
    
    for page in sorted(PAGES):
        if corriger_logo(page):
            print(f"  CORRIGE: {page}")
            corriges += 1
        else:
            deja_ok += 1
    
    print(f"\n{'='*60}")
    print(f"Resume:")
    print(f"  - Pages corrigees: {corriges}")
    print(f"  - Pages deja OK: {deja_ok}")
    print(f"  - Total: {len(PAGES)} pages")

if __name__ == '__main__':
    main()

