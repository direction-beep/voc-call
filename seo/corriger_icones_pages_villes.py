#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour remplacer les émojis mal encodés par des icônes Font Awesome
"""

import os
import re
import glob

# Fichiers à modifier
PAGES = glob.glob("demenagement-*.html") + glob.glob("demenageur-*.html")
PAGES = [f for f in PAGES if f not in ["index.html", "carte-france.html"]]

def corriger_icones(filepath):
    """Corrige les icônes d'un fichier"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    modifie = False
    
    # Chercher toutes les divs avec advantage-icon qui contiennent du texte (pas des icônes Font Awesome)
    pattern = r'<div class="advantage-icon">([^<]+)</div>'
    
    def remplacer_icone(match):
        icon_text = match.group(1).strip()
        
        # Déterminer quelle icône utiliser selon le contexte (titre suivant)
        # On va chercher le h3 suivant pour déterminer l'icône
        return match.group(0)  # On retourne tel quel pour l'instant, on va faire le remplacement après
    
    # Remplacer selon le contexte (h3 suivant)
    # Connaissance locale
    content = re.sub(
        r'<div class="advantage-icon">[^<]*</div>\s*<h3>Connaissance locale</h3>',
        '<div class="advantage-icon"><i class="fas fa-map-marked-alt"></i></div>\n                        <h3>Connaissance locale</h3>',
        content
    )
    if content != original_content:
        modifie = True
        original_content = content
    
    # Réactivité maximale
    content = re.sub(
        r'<div class="advantage-icon">[^<]*</div>\s*<h3>Réactivité maximale</h3>',
        '<div class="advantage-icon"><i class="fas fa-bolt"></i></div>\n                        <h3>Réactivité maximale</h3>',
        content
    )
    if content != original_content:
        modifie = True
        original_content = content
    
    # Professionnels certifiés
    content = re.sub(
        r'<div class="advantage-icon">[^<]*</div>\s*<h3>Professionnels certifiés</h3>',
        '<div class="advantage-icon"><i class="fas fa-user-tie"></i></div>\n                        <h3>Professionnels certifiés</h3>',
        content
    )
    if content != original_content:
        modifie = True
        original_content = content
    
    # Assurance tous risques
    content = re.sub(
        r'<div class="advantage-icon">[^<]*</div>\s*<h3>Assurance tous risques</h3>',
        '<div class="advantage-icon"><i class="fas fa-shield-alt"></i></div>\n                        <h3>Assurance tous risques</h3>',
        content
    )
    if content != original_content:
        modifie = True
    
    # Vérifier si Font Awesome est inclus dans le head
    if 'font-awesome' not in content.lower() and 'fas fa-' in content:
        # Ajouter Font Awesome si nécessaire
        fontawesome_link = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'
        if '</head>' in content and fontawesome_link not in content:
            content = content.replace('</head>', f'    {fontawesome_link}\n</head>')
            modifie = True
    
    if modifie:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fonction principale"""
    print("Correction des icones sur toutes les pages villes...\n")
    
    corriges = 0
    deja_ok = 0
    
    for page in sorted(PAGES):
        if corriger_icones(page):
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
