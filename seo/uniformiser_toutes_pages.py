#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour uniformiser l'affichage et le logo sur toutes les pages
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

def uniformiser_page(filepath):
    """Uniformise une page"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    modifie = False
    
    # 1. S'assurer que le CSS est styles.css
    if 'demenagement-zen.css' in content:
        content = re.sub(r'css/demenagement-zen\.css', 'css/styles.css', content)
        modifie = True
    
    # 2. Vérifier et corriger le header
    # Chercher le header actuel
    header_match = re.search(r'<!-- Header -->.*?</header>', content, re.DOTALL)
    if header_match:
        header_actuel = header_match.group(0)
        
        # Vérifier si le logo est présent
        if 'logo-demenagement-zen.svg' not in header_actuel or 'logo-demenagement-zen.png' not in header_actuel:
            # Remplacer le header
            content = re.sub(
                r'<!-- Header -->.*?</header>',
                HEADER_STANDARD,
                content,
                flags=re.DOTALL
            )
            modifie = True
        # Vérifier la structure du header
        elif 'nav-logo' not in header_actuel or '<img' not in header_actuel:
            # Remplacer le header
            content = re.sub(
                r'<!-- Header -->.*?</header>',
                HEADER_STANDARD,
                content,
                flags=re.DOTALL
            )
            modifie = True
        # Vérifier que le menu est correct
        elif 'btn-primary-nav' not in header_actuel:
            # Remplacer le header
            content = re.sub(
                r'<!-- Header -->.*?</header>',
                HEADER_STANDARD,
                content,
                flags=re.DOTALL
            )
            modifie = True
    
    # 3. S'assurer qu'il n'y a pas de breadcrumbs HTML visibles
    if '<nav aria-label="Fil d\'Ariane" class="breadcrumbs">' in content:
        breadcrumbs_match = re.search(
            r'<!-- Breadcrumbs -->\s*<nav aria-label="Fil d\'Ariane" class="breadcrumbs">.*?</nav>',
            content,
            re.DOTALL
        )
        if breadcrumbs_match:
            content = content.replace(breadcrumbs_match.group(0), '')
            modifie = True
    
    if modifie:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Uniformisation de l'affichage et du logo sur toutes les pages...\n")
    
    corriges = 0
    deja_ok = 0
    
    for page in sorted(PAGES):
        if uniformiser_page(page):
            print(f"  ✓ Corrigé: {page}")
            corriges += 1
        else:
            print(f"  → OK: {page}")
            deja_ok += 1
    
    print(f"\n{'='*60}")
    print(f"Résumé:")
    print(f"  - Pages corrigées: {corriges}")
    print(f"  - Pages déjà OK: {deja_ok}")
    print(f"  - Total: {len(PAGES)} pages")

if __name__ == '__main__':
    main()

