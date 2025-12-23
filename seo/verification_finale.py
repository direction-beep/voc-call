#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification finale des optimisations SEO
Vérifie toutes les 32 pages optimisées
"""

import os
import re
from pathlib import Path

# Liste des 32 pages à vérifier
PAGES_DEMENAGEMENT = [
    "demenagement-marseille.html",
    "demenagement-paris.html",
    "demenagement-toulouse.html",
    "demenagement-lyon.html",
    "demenagement-bordeaux.html",
    "demenagement-grenoble.html",
    "demenagement-strasbourg.html",
    "demenagement-montpellier.html",
    "demenagement-nice.html",
    "demenagement-nantes.html",
    "demenagement-rennes.html",
    "demenagement-rouen.html",
    "demenagement-annecy.html",
    "demenagement-versailles.html",
    "demenagement-angers.html",
    "demenagement-dijon.html",
]

PAGES_DEMENAGEUR = [
    "demenageur-marseille.html",
    "demenageur-paris.html",
    "demenageur-toulouse.html",
    "demenageur-lyon.html",
    "demenageur-bordeaux.html",
    "demenageur-grenoble.html",
    "demenageur-strasbourg.html",
    "demenageur-montpellier.html",
    "demenageur-nice.html",
    "demenageur-nantes.html",
    "demenageur-rennes.html",
    "demenageur-rouen.html",
    "demenageur-annecy.html",
    "demenageur-versailles.html",
    "demenageur-angers.html",
    "demenageur-dijon.html",
]

ALL_PAGES = PAGES_DEMENAGEMENT + PAGES_DEMENAGEUR

def check_file_exists(filepath):
    """Vérifie si le fichier existe"""
    return os.path.exists(filepath)

def check_meta_title(content):
    """Vérifie la présence et la longueur du meta title"""
    match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if match:
        title = match.group(1).strip()
        length = len(title)
        return {
            'present': True,
            'content': title,
            'length': length,
            'valid': 50 <= length <= 60
        }
    return {'present': False, 'content': '', 'length': 0, 'valid': False}

def check_meta_description(content):
    """Vérifie la présence et la longueur de la meta description"""
    match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
    if match:
        desc = match.group(1).strip()
        length = len(desc)
        return {
            'present': True,
            'content': desc,
            'length': length,
            'valid': 150 <= length <= 160
        }
    return {'present': False, 'content': '', 'length': 0, 'valid': False}

def check_h1(content):
    """Vérifie la présence d'un H1 unique"""
    matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if matches:
        h1_text = [m.strip() for m in matches]
        return {
            'present': True,
            'count': len(h1_text),
            'content': h1_text[0] if h1_text else '',
            'unique': len(h1_text) == 1
        }
    return {'present': False, 'count': 0, 'content': '', 'unique': False}

def check_canonical(content):
    """Vérifie la présence d'une URL canonique"""
    match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', content, re.IGNORECASE)
    if match:
        url = match.group(1)
        return {
            'present': True,
            'url': url,
            'has_html': '.html' in url
        }
    return {'present': False, 'url': '', 'has_html': False}

def check_breadcrumbs_schema(content):
    """Vérifie la présence du Schema.org BreadcrumbList"""
    return '@type": "BreadcrumbList' in content or '"@type": "BreadcrumbList' in content

def check_breadcrumbs_html(content):
    """Vérifie la présence des breadcrumbs HTML"""
    return 'breadcrumb' in content.lower() or 'Fil d\'Ariane' in content

def check_faq_schema(content):
    """Vérifie la présence du Schema.org FAQPage"""
    return '@type": "FAQPage' in content or '"@type": "FAQPage' in content

def check_faq_html(content):
    """Vérifie la présence de la section FAQ HTML"""
    return 'faq' in content.lower() or 'Questions fréquentes' in content

def check_footer_links(content):
    """Vérifie la présence des liens footer"""
    return 'footer-col' in content or 'Liens utiles' in content

def verify_page(filepath):
    """Vérifie une page complète"""
    if not check_file_exists(filepath):
        return {
            'file': filepath,
            'exists': False,
            'errors': ['Fichier introuvable']
        }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'file': filepath,
        'exists': True,
        'meta_title': check_meta_title(content),
        'meta_description': check_meta_description(content),
        'h1': check_h1(content),
        'canonical': check_canonical(content),
        'breadcrumbs_schema': check_breadcrumbs_schema(content),
        'breadcrumbs_html': check_breadcrumbs_html(content),
        'faq_schema': check_faq_schema(content),
        'faq_html': check_faq_html(content),
        'footer_links': check_footer_links(content),
    }
    
    # Compter les erreurs
    errors = []
    if not results['meta_title']['present']:
        errors.append('Meta title manquante')
    elif not results['meta_title']['valid']:
        errors.append(f"Meta title trop {'longue' if results['meta_title']['length'] > 60 else 'courte'} ({results['meta_title']['length']} caractères)")
    
    if not results['meta_description']['present']:
        errors.append('Meta description manquante')
    elif not results['meta_description']['valid']:
        errors.append(f"Meta description trop {'longue' if results['meta_description']['length'] > 160 else 'courte'} ({results['meta_description']['length']} caractères)")
    
    if not results['h1']['present']:
        errors.append('H1 manquant')
    elif not results['h1']['unique']:
        errors.append(f"Plusieurs H1 trouvés ({results['h1']['count']})")
    
    if not results['canonical']['present']:
        errors.append('URL canonique manquante')
    
    if not results['breadcrumbs_schema']:
        errors.append('Breadcrumbs Schema.org manquant')
    
    if not results['breadcrumbs_html']:
        errors.append('Breadcrumbs HTML manquant')
    
    if not results['faq_schema']:
        errors.append('FAQ Schema.org manquant')
    
    if not results['faq_html']:
        errors.append('FAQ HTML manquant')
    
    if not results['footer_links']:
        errors.append('Liens footer manquants')
    
    results['errors'] = errors
    results['valid'] = len(errors) == 0
    
    return results

def generate_report(results):
    """Génère un rapport de vérification"""
    report = []
    report.append("# Rapport de Vérification Finale - SEO\n")
    report.append(f"Date : {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    total_pages = len(results)
    valid_pages = sum(1 for r in results if r['valid'])
    invalid_pages = total_pages - valid_pages
    
    report.append(f"## Statistiques Globales\n\n")
    report.append(f"- **Total de pages verifiees :** {total_pages}\n")
    report.append(f"- **Pages valides :** {valid_pages} ({valid_pages*100//total_pages}%)\n")
    report.append(f"- **Pages avec erreurs :** {invalid_pages} ({invalid_pages*100//total_pages}%)\n\n")
    
    # Details par page
    report.append("## Details par Page\n\n")
    
    for result in results:
        status = "[OK]" if result['valid'] else "[ERREUR]"
        report.append(f"### {status} {result['file']}\n\n")
        
        if not result['exists']:
            report.append("- **Erreur :** Fichier introuvable\n\n")
            continue
        
        report.append(f"- **Meta title :** {'[OK]' if result['meta_title']['valid'] else '[ERREUR]'} ({result['meta_title']['length']} caracteres)\n")
        report.append(f"- **Meta description :** {'[OK]' if result['meta_description']['valid'] else '[ERREUR]'} ({result['meta_description']['length']} caracteres)\n")
        report.append(f"- **H1 :** {'[OK]' if result['h1']['unique'] else '[ERREUR]'} ({result['h1']['count']} trouve(s))\n")
        report.append(f"- **URL canonique :** {'[OK]' if result['canonical']['present'] else '[ERREUR]'}\n")
        report.append(f"- **Breadcrumbs Schema :** {'[OK]' if result['breadcrumbs_schema'] else '[ERREUR]'}\n")
        report.append(f"- **Breadcrumbs HTML :** {'[OK]' if result['breadcrumbs_html'] else '[ERREUR]'}\n")
        report.append(f"- **FAQ Schema :** {'[OK]' if result['faq_schema'] else '[ERREUR]'}\n")
        report.append(f"- **FAQ HTML :** {'[OK]' if result['faq_html'] else '[ERREUR]'}\n")
        report.append(f"- **Liens footer :** {'[OK]' if result['footer_links'] else '[ERREUR]'}\n")
        
        if result['errors']:
            report.append(f"\n**Erreurs detectees :**\n")
            for error in result['errors']:
                report.append(f"- {error}\n")
        
        report.append("\n")
    
    # Résumé des erreurs communes
    all_errors = []
    for result in results:
        all_errors.extend(result.get('errors', []))
    
    if all_errors:
        error_counts = {}
        for error in all_errors:
            error_counts[error] = error_counts.get(error, 0) + 1
        
        report.append("## Erreurs Communes\n\n")
        for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- **{error}** : {count} page(s)\n")
        report.append("\n")
    
    return ''.join(report)

def main():
    """Fonction principale"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Debut de la verification finale...\n")
    
    results = []
    for page in ALL_PAGES:
        print(f"Verification de {page}...")
        result = verify_page(page)
        results.append(result)
        if result['valid']:
            print(f"  OK - {page}")
        else:
            print(f"  ERREUR - {page} - {len(result['errors'])} erreur(s)")
    
    # Générer le rapport
    report = generate_report(results)
    
    # Sauvegarder le rapport
    report_path = 'seo/RAPPORT_VERIFICATION_FINALE.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nRapport genere : {report_path}\n")
    
    # Afficher le resume
    valid_count = sum(1 for r in results if r['valid'])
    print(f"Resume : {valid_count}/{len(results)} pages valides")
    
    if valid_count < len(results):
        print("\nATTENTION : Des erreurs ont ete detectees. Consultez le rapport pour plus de details.")

if __name__ == '__main__':
    main()

