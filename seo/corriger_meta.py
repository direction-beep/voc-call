#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les meta descriptions et titles trop longues
"""

import re
import os

# Dictionnaire des corrections pour les meta descriptions
# Format: (fichier, ancienne description, nouvelle description)
CORRECTIONS_DESCRIPTION = {
    # Pages demenagement
    "demenagement-marseille.html": (
        "Déménagement professionnel à Marseille. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région marseillaise.",
        "Déménagement professionnel à Marseille. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-paris.html": (
        "Déménagement professionnel à Paris. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région parisienne.",
        "Déménagement professionnel à Paris. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-toulouse.html": (
        "Déménagement professionnel à Toulouse. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région toulousaine.",
        "Déménagement professionnel à Toulouse. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-lyon.html": (
        "Déménagement professionnel à Lyon. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région lyonnaise.",
        "Déménagement professionnel à Lyon. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-bordeaux.html": (
        "Déménagement professionnel à Bordeaux. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région bordelaise.",
        "Déménagement professionnel à Bordeaux. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-grenoble.html": (
        "Déménagement professionnel à Grenoble. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région grenobloise.",
        "Déménagement professionnel à Grenoble. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-strasbourg.html": (
        "Déménagement professionnel à Strasbourg. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région strasbourgeoise.",
        "Déménagement professionnel à Strasbourg. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-montpellier.html": (
        "Déménagement professionnel à Montpellier. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région montpelliéraine.",
        "Déménagement professionnel à Montpellier. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-nice.html": (
        "Déménagement professionnel à Nice. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région niçoise.",
        "Déménagement professionnel à Nice. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-nantes.html": (
        "Déménagement professionnel à Nantes. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région nantaise.",
        "Déménagement professionnel à Nantes. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-rennes.html": (
        "Déménagement professionnel à Rennes. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région rennaise.",
        "Déménagement professionnel à Rennes. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-rouen.html": (
        "Déménagement professionnel à Rouen. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région rouennaise.",
        "Déménagement professionnel à Rouen. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-annecy.html": (
        "Déménagement professionnel à Annecy. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région annécienne.",
        "Déménagement professionnel à Annecy. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-versailles.html": (
        "Déménagement professionnel à Versailles. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région versaillaise.",
        "Déménagement professionnel à Versailles. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-angers.html": (
        "Déménagement professionnel à Angers. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région angevine.",
        "Déménagement professionnel à Angers. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
    "demenagement-dijon.html": (
        "Déménagement professionnel à Dijon. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région dijonnaise.",
        "Déménagement professionnel à Dijon. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h."
    ),
}

# Corrections pour les meta titles des pages demenageur
CORRECTIONS_TITLE_DEMENAGEUR = {
    "demenageur-marseille.html": (
        "Déménageur Marseille | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Marseille | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-paris.html": (
        "Déménageur Paris | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Paris | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-toulouse.html": (
        "Déménageur Toulouse | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Toulouse | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-lyon.html": (
        "Déménageur Lyon | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Lyon | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-bordeaux.html": (
        "Déménageur Bordeaux | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Bordeaux | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-grenoble.html": (
        "Déménageur Grenoble | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Grenoble | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-strasbourg.html": (
        "Déménageur Strasbourg | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Strasbourg | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-montpellier.html": (
        "Déménageur Montpellier | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Montpellier | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-nice.html": (
        "Déménageur Nice | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Nice | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-nantes.html": (
        "Déménageur Nantes | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Nantes | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-rennes.html": (
        "Déménageur Rennes | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Rennes | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-rouen.html": (
        "Déménageur Rouen | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Rouen | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-annecy.html": (
        "Déménageur Annecy | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Annecy | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-versailles.html": (
        "Déménageur Versailles | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Versailles | Équipe Professionnelle - Devis Gratuit"
    ),
    "demenageur-angers.html": (
        "Déménageur Angers | Équipe Professionnelle - Devis Gratuit 7j/7",
        "Déménageur Angers | Équipe Professionnelle - Devis Gratuit"
    ),
}

# Corrections pour les meta descriptions des pages demenageur
CORRECTIONS_DESCRIPTION_DEMENAGEUR = {
    "demenageur-marseille.html": (
        "Déménageur professionnel à Marseille. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région marseillaise.",
        "Déménageur professionnel à Marseille. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-paris.html": (
        "Déménageur professionnel à Paris. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région parisienne.",
        "Déménageur professionnel à Paris. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-toulouse.html": (
        "Déménageur professionnel à Toulouse. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région toulousaine.",
        "Déménageur professionnel à Toulouse. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-lyon.html": (
        "Déménageur professionnel à Lyon. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région lyonnaise.",
        "Déménageur professionnel à Lyon. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-bordeaux.html": (
        "Déménageur professionnel à Bordeaux. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région bordelaise.",
        "Déménageur professionnel à Bordeaux. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-grenoble.html": (
        "Déménageur professionnel à Grenoble. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région grenobloise.",
        "Déménageur professionnel à Grenoble. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-strasbourg.html": (
        "Déménageur professionnel à Strasbourg. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région strasbourgeoise.",
        "Déménageur professionnel à Strasbourg. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-montpellier.html": (
        "Déménageur professionnel à Montpellier. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région montpelliéraine.",
        "Déménageur professionnel à Montpellier. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-nice.html": (
        "Déménageur professionnel à Nice. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région niçoise.",
        "Déménageur professionnel à Nice. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-nantes.html": (
        "Déménageur professionnel à Nantes. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région nantaise.",
        "Déménageur professionnel à Nantes. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-rennes.html": (
        "Déménageur professionnel à Rennes. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région rennaise.",
        "Déménageur professionnel à Rennes. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-rouen.html": (
        "Déménageur professionnel à Rouen. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région rouennaise.",
        "Déménageur professionnel à Rouen. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-annecy.html": (
        "Déménageur professionnel à Annecy. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région annécienne.",
        "Déménageur professionnel à Annecy. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-versailles.html": (
        "Déménageur professionnel à Versailles. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région versaillaise.",
        "Déménageur professionnel à Versailles. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
    "demenageur-angers.html": (
        "Déménageur professionnel à Angers. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide dans toute la région angevine.",
        "Déménageur professionnel à Angers. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h."
    ),
}

def corriger_meta_description(filepath, ancienne, nouvelle):
    """Corrige la meta description dans un fichier"""
    if not os.path.exists(filepath):
        print(f"Fichier introuvable: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Échapper les caractères spéciaux pour la regex
    ancienne_escaped = re.escape(ancienne)
    pattern = r'<meta\s+name=["\']description["\']\s+content=["\']' + ancienne_escaped + r'["\']'
    
    if re.search(pattern, content):
        content = re.sub(pattern, f'<meta name="description" content="{nouvelle}"', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    else:
        # Essayer avec des variations
        pattern_flexible = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*' + re.escape(ancienne[:50]) + r'[^"\']*)["\']'
        match = re.search(pattern_flexible, content)
        if match:
            content = re.sub(pattern_flexible, f'<meta name="description" content="{nouvelle}"', content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        print(f"Meta description non trouvee dans {filepath}")
        return False

def corriger_meta_title(filepath, ancienne, nouvelle):
    """Corrige le meta title dans un fichier"""
    if not os.path.exists(filepath):
        print(f"Fichier introuvable: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ancienne_escaped = re.escape(ancienne)
    pattern = r'<title>' + ancienne_escaped + r'</title>'
    
    if re.search(pattern, content):
        content = re.sub(pattern, f'<title>{nouvelle}</title>', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    else:
        print(f"Meta title non trouve dans {filepath}")
        return False

def main():
    """Fonction principale"""
    print("Correction des meta descriptions et titles...\n")
    
    # Corriger les meta descriptions des pages demenagement
    print("Correction des meta descriptions (pages demenagement)...")
    for filename, (ancienne, nouvelle) in CORRECTIONS_DESCRIPTION.items():
        if corriger_meta_description(filename, ancienne, nouvelle):
            print(f"  OK: {filename}")
        else:
            print(f"  ERREUR: {filename}")
    
    # Corriger les meta titles des pages demenageur
    print("\nCorrection des meta titles (pages demenageur)...")
    for filename, (ancienne, nouvelle) in CORRECTIONS_TITLE_DEMENAGEUR.items():
        if corriger_meta_title(filename, ancienne, nouvelle):
            print(f"  OK: {filename}")
        else:
            print(f"  ERREUR: {filename}")
    
    # Corriger les meta descriptions des pages demenageur
    print("\nCorrection des meta descriptions (pages demenageur)...")
    for filename, (ancienne, nouvelle) in CORRECTIONS_DESCRIPTION_DEMENAGEUR.items():
        if corriger_meta_description(filename, ancienne, nouvelle):
            print(f"  OK: {filename}")
        else:
            print(f"  ERREUR: {filename}")
    
    print("\nCorrections terminees!")

if __name__ == '__main__':
    main()

