#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour optimiser les URLs mal formatées pour le SEO
Remplace les URLs anglaises par des URLs françaises optimisées
"""

import os
import re
from pathlib import Path

# Mapping des URLs à optimiser (anglais -> français SEO-friendly)
URL_MAPPING = {
    "/partners": "/partenaires",
    "/resources": "/ressources",
    "/testimonials": "/temoignages",
    
    # Variantes avec domaines
    "https://voc-call.fr/partners": "https://voc-call.fr/partenaires",
    "https://voc-call.fr/resources": "https://voc-call.fr/ressources",
    "https://voc-call.fr/testimonials": "https://voc-call.fr/temoignages",
    
    # Variantes en fin d'URL
    "partners": "partenaires",
    "resources": "ressources",
    "testimonials": "temoignages",
}

# Patterns pour trouver les références dans différents contextes
PATTERNS = [
    r'href=["\']([^"\']*/(?:partners|resources|testimonials)(?:/|["\']|[\s>]|$))',
    r'action=["\']([^"\']*/(?:partners|resources|testimonials))',
    r'src=["\']([^"\']*/(?:partners|resources|testimonials))',
    r'url\(["\']?([^"\')]*/(?:partners|resources|testimonials))',
    r'canonical["\']?\s*content=["\']([^"\']*/(?:partners|resources|testimonials))',
    r'<loc>([^<]*/(?:partners|resources|testimonials))</loc>',
]


def find_html_files(root_dir="."):
    """Trouve tous les fichiers HTML dans le répertoire"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Ignorer les dossiers à exclure
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv']]
        for file in files:
            if file.endswith(('.html', '.htm')):
                html_files.append(os.path.join(root, file))
    return html_files


def find_url_references(content):
    """Trouve toutes les références aux URLs à optimiser"""
    references = []
    
    for pattern in PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            url = match.group(1) if match.groups() else match.group(0)
            references.append({
                'url': url,
                'start': match.start(),
                'end': match.end(),
                'full_match': match.group(0)
            })
    
    # Recherche simple aussi
    for old_url, new_url in URL_MAPPING.items():
        if old_url in content.lower():
            # Trouver toutes les occurrences
            for match in re.finditer(re.escape(old_url), content, re.IGNORECASE):
                references.append({
                    'url': old_url,
                    'start': match.start(),
                    'end': match.end(),
                    'full_match': match.group(0)
                })
    
    return references


def fix_urls_in_file(filepath, dry_run=True):
    """Corrige les URLs dans un fichier HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath}: {e}")
        return False
    
    original_content = content
    references = find_url_references(content)
    
    if not references:
        return False
    
    print(f"\nFichier: {filepath}")
    print(f"  {len(references)} reference(s) trouvee(s)")
    
    # Remplacer les URLs
    replacements = 0
    for old_url, new_url in URL_MAPPING.items():
        # Compter les occurrences
        count = len(re.findall(re.escape(old_url), content, re.IGNORECASE))
        if count > 0:
            print(f"  - '{old_url}' -> '{new_url}' ({count} occurrence(s))")
            if not dry_run:
                # Remplacer en préservant la casse
                def replace_func(match):
                    matched = match.group(0)
                    # Préserver la casse du début si nécessaire
                    if matched[0].isupper():
                        return new_url.capitalize() if len(new_url) > 0 else new_url
                    return new_url
                
                content = re.sub(re.escape(old_url), new_url, content, flags=re.IGNORECASE)
                replacements += count
    
    if not dry_run and content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] {replacements} remplacement(s) effectue(s)")
            return True
        except Exception as e:
            print(f"  [ERREUR] Erreur lors de l'ecriture: {e}")
            return False
    elif dry_run:
        print(f"  [DRY-RUN] Aucune modification")
        return True
    
    return False


def create_redirect_mapping():
    """Génère un fichier de mapping pour les redirections (vercel.json ou .htaccess)"""
    redirect_rules = []
    
    redirect_rules.append("\n# Redirections SEO - URLs optimisées")
    redirect_rules.append("# Ajouter ces règles dans vercel.json ou .htaccess\n")
    
    for old_url, new_url in [("/partners", "/partenaires"),
                              ("/resources", "/ressources"),
                              ("/testimonials", "/temoignages")]:
        redirect_rules.append(f"{old_url} -> {new_url}")
    
    redirect_content = "\n".join(redirect_rules)
    
    # Format pour vercel.json
    vercel_redirects = {
        "redirects": [
            {
                "source": "/partners",
                "destination": "/partenaires",
                "permanent": True
            },
            {
                "source": "/resources",
                "destination": "/ressources",
                "permanent": True
            },
            {
                "source": "/testimonials",
                "destination": "/temoignages",
                "permanent": True
            }
        ]
    }
    
    return redirect_content, vercel_redirects


def main():
    """Fonction principale"""
    import sys
    import io
    import json
    
    # Configurer l'encodage UTF-8 pour Windows
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("Optimisation des URLs pour le SEO")
    print("=" * 70)
    print("\nURLs a optimiser:")
    for old, new in [("/partners", "/partenaires"),
                     ("/resources", "/ressources"),
                     ("/testimonials", "/temoignages")]:
        print(f"  {old} -> {new}")
    print()
    
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
        if fix_urls_in_file(filepath, dry_run=dry_run):
            fixed_count += 1
    
    print("\n" + "=" * 70)
    if dry_run:
        print(f"Analyse terminee: {fixed_count} fichier(s) avec URLs a optimiser detecte(s)")
        print("Pour appliquer les corrections, executez: python fix_urls_seo.py --apply")
    else:
        print(f"Correction terminee: {fixed_count} fichier(s) modifie(s)")
    
    # Générer les règles de redirection
    redirect_text, vercel_redirects = create_redirect_mapping()
    print("\n" + "=" * 70)
    print("REGLES DE REDIRECTION RECOMMANDEES")
    print("=" * 70)
    print("\nPour vercel.json, ajouter dans la section redirects:")
    print(json.dumps(vercel_redirects["redirects"], indent=2, ensure_ascii=False))
    print("\nPour .htaccess, ajouter:")
    print("Redirect 301 /partners /partenaires")
    print("Redirect 301 /resources /ressources")
    print("Redirect 301 /testimonials /temoignages")
    print("=" * 70)


if __name__ == "__main__":
    main()

