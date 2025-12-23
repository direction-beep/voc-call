#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajuster les meta descriptions à la bonne longueur (150-160 caractères)
"""

import re
import os

# Nouvelles meta descriptions optimisées (150-160 caractères)
CORRECTIONS_FINALES = {
    "demenagement-marseille.html": "Déménagement professionnel à Marseille. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-paris.html": "Déménagement professionnel à Paris. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-toulouse.html": "Déménagement professionnel à Toulouse. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-lyon.html": "Déménagement professionnel à Lyon. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-bordeaux.html": "Déménagement professionnel à Bordeaux. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-grenoble.html": "Déménagement professionnel à Grenoble. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-strasbourg.html": "Déménagement professionnel à Strasbourg. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-montpellier.html": "Déménagement professionnel à Montpellier. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-nice.html": "Déménagement professionnel à Nice. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-nantes.html": "Déménagement professionnel à Nantes. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-rennes.html": "Déménagement professionnel à Rennes. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-rouen.html": "Déménagement professionnel à Rouen. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-annecy.html": "Déménagement professionnel à Annecy. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-versailles.html": "Déménagement professionnel à Versailles. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-angers.html": "Déménagement professionnel à Angers. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenagement-dijon.html": "Déménagement professionnel à Dijon. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région.",
    "demenageur-marseille.html": "Déménageur professionnel à Marseille. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-paris.html": "Déménageur professionnel à Paris. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-toulouse.html": "Déménageur professionnel à Toulouse. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-lyon.html": "Déménageur professionnel à Lyon. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-bordeaux.html": "Déménageur professionnel à Bordeaux. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-grenoble.html": "Déménageur professionnel à Grenoble. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-strasbourg.html": "Déménageur professionnel à Strasbourg. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-montpellier.html": "Déménageur professionnel à Montpellier. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-nice.html": "Déménageur professionnel à Nice. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-nantes.html": "Déménageur professionnel à Nantes. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-rennes.html": "Déménageur professionnel à Rennes. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-rouen.html": "Déménageur professionnel à Rouen. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-annecy.html": "Déménageur professionnel à Annecy. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-versailles.html": "Déménageur professionnel à Versailles. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
    "demenageur-angers.html": "Déménageur professionnel à Angers. Équipe expérimentée et soigneuse. Déménagement résidentiel et professionnel. Devis gratuit sous 24h. Intervention rapide.",
}

def corriger_meta_description(filepath, nouvelle):
    """Corrige la meta description dans un fichier"""
    if not os.path.exists(filepath):
        print(f"Fichier introuvable: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver la meta description
    pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']'
    
    def replacer(match):
        return f'<meta name="description" content="{nouvelle}"'
    
    new_content = re.sub(pattern, replacer, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    else:
        print(f"Meta description non trouvee dans {filepath}")
        return False

def main():
    """Fonction principale"""
    print("Ajustement final des meta descriptions...\n")
    
    for filename, nouvelle_desc in CORRECTIONS_FINALES.items():
        longueur = len(nouvelle_desc)
        if corriger_meta_description(filename, nouvelle_desc):
            print(f"  OK: {filename} ({longueur} caracteres)")
        else:
            print(f"  ERREUR: {filename}")
    
    print("\nCorrections terminees!")

if __name__ == '__main__':
    main()

