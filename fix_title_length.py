#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les balises title trop longues dans les fichiers HTML
Objectif: réduire les titres à maximum 60 caractères pour optimiser le SEO
"""

import os
import re
from pathlib import Path

# Longueur maximale recommandée pour les titres SEO (60 caractères)
MAX_TITLE_LENGTH = 60

# Mapping des corrections spécifiques pour les 17 pages identifiées dans l'audit SEO
TITLE_CORRECTIONS = {
    # Articles de blog - basés sur les URLs de l'audit
    "accueil-telephonique-professionnel": "Accueil Téléphonique Professionnel 2024 | VOC-Call",
    "centre-appels-france-support-utilisateurs": "Centre d'Appels France & Support 2025 | VOC-Call",
    "comment-choisir-call-center-france-2025": "Comment Choisir un Call Center 2025 | VOC-Call",
    "devenir-teleconseiller-independant": "Devenir Téléconseiller Indépendant | VOC-Call",
    "guide-homeshoring-recrutement": "Guide Homeshoring Recrutement | VOC-Call",
    "permanence-telephonique-distance": "Permanence Téléphonique à Distance 2024 | VOC-Call",
    "permanence-telephonique-sla": "Permanence Téléphonique & SLA | VOC-Call",
    "prospection-telephonique-b2b-script-kpi": "Prospection B2B : Script & KPI 2025 | VOC-Call",
    "standard-externalise-combien-ca-coute": "Standard Externalisé : Tarifs 2025 | VOC-Call",
    
    # Pages villes (centre-appel-*) - format optimisé
    "centre-appel-bordeaux": "Centre d'Appel Bordeaux | VOC-Call",
    "centre-appel-lille": "Centre d'Appel Lille | VOC-Call",
    "centre-appel-lyon": "Centre d'Appel Lyon | VOC-Call",
    "centre-appel-marseille": "Centre d'Appel Marseille | VOC-Call",
    "centre-appel-nantes": "Centre d'Appel Nantes | VOC-Call",
    "centre-appel-paris": "Centre d'Appel Paris | VOC-Call",
    "centre-appel-strasbourg": "Centre d'Appel Strasbourg | VOC-Call",
    "centre-appel-toulouse": "Centre d'Appel Toulouse | VOC-Call",
}


def find_html_files(root_dir="."):
    """Trouve tous les fichiers HTML dans le répertoire"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Ignorer les dossiers à exclure
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files


def extract_title_from_content(content):
    """Extrait la balise title du contenu HTML"""
    pattern = r'<title>(.*?)</title>'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def get_suggested_title(filepath, current_title):
    """Suggère un nouveau titre basé sur le nom du fichier ou les corrections pré-définies"""
    filename = os.path.basename(filepath).replace('.html', '')
    filepath_normalized = filepath.replace('\\', '/').lower()
    
    # Chercher dans les corrections pré-définies (priorité aux correspondances exactes)
    for key, suggested_title in TITLE_CORRECTIONS.items():
        if key.lower() in filename.lower() or key.lower() in filepath_normalized:
            return suggested_title
    
    # Si pas de correspondance, raccourcir le titre actuel intelligemment
    if len(current_title) <= MAX_TITLE_LENGTH:
        return None
    
    # Raccourcir en gardant les mots-clés importants
    parts = current_title.split('|')
    if len(parts) == 2:
        main_part = parts[0].strip()
        brand_part = parts[1].strip()
        
        # Si la partie principale est trop longue, la raccourcir
        if len(main_part) > MAX_TITLE_LENGTH - len(brand_part) - 3:
            # Prendre les premiers mots jusqu'à la limite
            words = main_part.split()
            shortened = []
            current_length = len(brand_part) + 3  # " | "
            for word in words:
                if current_length + len(word) + 1 <= MAX_TITLE_LENGTH:
                    shortened.append(word)
                    current_length += len(word) + 1
                else:
                    break
            main_part = ' '.join(shortened)
        
        return f"{main_part} | {brand_part}"
    
    # Si pas de séparateur |, simplement tronquer
    return current_title[:MAX_TITLE_LENGTH - 3] + "..."


def fix_title_in_file(filepath, dry_run=True):
    """Corrige la balise title dans un fichier HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath}: {e}")
        return False
    
    current_title = extract_title_from_content(content)
    if not current_title:
        return False
    
    title_length = len(current_title)
    
    # Vérifier si le titre est trop long
    if title_length > MAX_TITLE_LENGTH:
        suggested_title = get_suggested_title(filepath, current_title)
        
        if suggested_title and suggested_title != current_title:
            print(f"\nFichier: {filepath}")
            print(f"   Titre actuel ({title_length} chars): {current_title}")
            print(f"   Titre suggere ({len(suggested_title)} chars): {suggested_title}")
            
            if not dry_run:
                # Remplacer le titre
                new_content = re.sub(
                    r'<title>.*?</title>',
                    f'<title>{suggested_title}</title>',
                    content,
                    flags=re.IGNORECASE | re.DOTALL
                )
                
                # Sauvegarder
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"   [OK] Corrige")
                    return True
                except Exception as e:
                    print(f"   [ERREUR] Erreur lors de l'ecriture: {e}")
                    return False
            else:
                print(f"   [DRY-RUN] Aucune modification")
            return True
    
    return False


def main():
    """Fonction principale"""
    import sys
    import io
    
    # Configurer l'encodage UTF-8 pour Windows
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("Recherche des balises title trop longues dans les fichiers HTML")
    print("=" * 70)
    print(f"Longueur maximale recommandee: {MAX_TITLE_LENGTH} caracteres\n")
    
    # Mode dry-run par défaut
    dry_run = True
    
    # Vérifier si l'utilisateur veut vraiment modifier
    if len(sys.argv) > 1 and sys.argv[1] == '--apply':
        dry_run = False
        print("MODE APPLICATION: Les fichiers seront modifies\n")
    else:
        print("MODE DRY-RUN: Aucun fichier ne sera modifie (utilisez --apply pour appliquer)\n")
    
    html_files = find_html_files()
    print(f"Fichiers HTML trouves: {len(html_files)}\n")
    
    fixed_count = 0
    for filepath in html_files:
        if fix_title_in_file(filepath, dry_run=dry_run):
            fixed_count += 1
    
    print("\n" + "=" * 70)
    if dry_run:
        print(f"Analyse terminee: {fixed_count} fichier(s) avec titre trop long detecte(s)")
        print("Pour appliquer les corrections, executez: python fix_title_length.py --apply")
    else:
        print(f"Correction terminee: {fixed_count} fichier(s) modifie(s)")
    print("=" * 70)


if __name__ == "__main__":
    main()

