#!/usr/bin/env python3
"""
Script pour optimiser toutes les pages avec volume > 1000
Génère les optimisations SEO : meta, breadcrumbs, FAQ, contenu enrichi
"""

import re
import os

# Configuration des villes avec volume > 1000
VILLES_CONFIG = {
    'paris': {
        'volume': 5400,
        'region': 'Île-de-France',
        'code_postal': '75001',
        'lat': '48.8566',
        'lon': '2.3522',
        'quartiers': ['tous les arrondissements', '1er au 20e arrondissement', 'Versailles', 'Nanterre', 'Créteil']
    },
    'toulouse': {
        'volume': 3600,
        'region': 'Occitanie',
        'code_postal': '31000',
        'lat': '43.6047',
        'lon': '1.4442',
        'quartiers': ['centre-ville', 'quartiers périphériques', 'Blagnac', 'Colomiers']
    },
    'lyon': {
        'volume': 2900,
        'region': 'Auvergne-Rhône-Alpes',
        'code_postal': '69000',
        'lat': '45.7640',
        'lon': '4.8357',
        'quartiers': ['centre-ville', 'Lyon 1er', 'Lyon 2e', 'Lyon 3e', 'Villeurbanne']
    },
    'bordeaux': {
        'volume': 2400,
        'region': 'Nouvelle-Aquitaine',
        'code_postal': '33000',
        'lat': '44.8378',
        'lon': '-0.5792',
        'quartiers': ['centre-ville', 'quartiers historiques', 'Mérignac', 'Pessac']
    },
    'grenoble': {
        'volume': 2400,
        'region': 'Auvergne-Rhône-Alpes',
        'code_postal': '38000',
        'lat': '45.1885',
        'lon': '5.7245',
        'quartiers': ['centre-ville', 'quartiers périphériques', 'Échirolles', 'Saint-Martin-d\'Hères']
    },
    'strasbourg': {
        'volume': 1900,
        'region': 'Grand Est',
        'code_postal': '67000',
        'lat': '48.5734',
        'lon': '7.7521',
        'quartiers': ['centre-ville', 'quartiers historiques', 'Schiltigheim', 'Illkirch-Graffenstaden']
    },
    'montpellier': {
        'volume': 1900,
        'region': 'Occitanie',
        'code_postal': '34000',
        'lat': '43.6108',
        'lon': '3.8767',
        'quartiers': ['centre-ville', 'quartiers périphériques', 'Lattes', 'Castelnau-le-Lez']
    },
    'nantes': {
        'volume': 1300,
        'region': 'Pays de la Loire',
        'code_postal': '44000',
        'lat': '47.2184',
        'lon': '-1.5536',
        'quartiers': ['centre-ville', 'quartiers périphériques', 'Saint-Herblain', 'Rezé']
    },
    'rennes': {
        'volume': 1000,
        'region': 'Bretagne',
        'code_postal': '35000',
        'lat': '48.1173',
        'lon': '-1.6778',
        'quartiers': ['centre-ville', 'quartiers périphériques', 'Cesson-Sévigné', 'Saint-Jacques-de-la-Lande']
    },
    'rouen': {
        'volume': 1000,
        'region': 'Normandie',
        'code_postal': '76000',
        'lat': '49.4431',
        'lon': '1.0993',
        'quartiers': ['centre-ville', 'quartiers historiques', 'Mont-Saint-Aignan', 'Sotteville-lès-Rouen']
    },
    'annecy': {
        'volume': 1000,
        'region': 'Auvergne-Rhône-Alpes',
        'code_postal': '74000',
        'lat': '45.8992',
        'lon': '6.1294',
        'quartiers': ['centre-ville', 'quartiers périphériques', 'Annecy-le-Vieux', 'Seynod']
    },
    'angers': {
        'volume': 1000,
        'region': 'Pays de la Loire',
        'code_postal': '49000',
        'lat': '47.4739',
        'lon': '-0.5517',
        'quartiers': ['centre-ville', 'quartiers périphériques', 'Avrillé', 'Trélazé']
    },
    'dijon': {
        'volume': 1000,
        'region': 'Bourgogne-Franche-Comté',
        'code_postal': '21000',
        'lat': '47.3220',
        'lon': '5.0415',
        'quartiers': ['centre-ville', 'quartiers historiques', 'Chenôve', 'Talant']
    }
}

def generate_faq_schema(ville, type_page='demenagement'):
    """Génère le schema FAQ pour une ville"""
    ville_cap = ville.capitalize()
    questions = [
        {
            'q': f'Combien coûte un {type_page} à {ville_cap} ?',
            'a': f'Le prix d\'un {type_page} à {ville_cap} dépend du volume à déménager, de la distance, de l\'étage et des services complémentaires. Nous proposons un devis gratuit et personnalisé pour chaque {type_page} à {ville_cap}.'
        },
        {
            'q': f'Quels services sont inclus dans un {type_page} à {ville_cap} ?',
            'a': f'Nos services de {type_page} à {ville_cap} incluent : emballage professionnel, transport sécurisé, montage et démontage de meubles, installation d\'électroménager. Nous intervenons pour les déménagements résidentiels et professionnels dans toute la région.'
        },
        {
            'q': f'Comment organiser un {type_page} à {ville_cap} ?',
            'a': f'Pour organiser un {type_page} à {ville_cap}, contactez-nous pour un devis gratuit. Nous planifions ensemble votre déménagement selon vos besoins : date, volume, services souhaités. Notre équipe intervient rapidement dans toute la région et vous recontacte sous 24h.'
        }
    ]
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    for qa in questions:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": qa['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": qa['a']
            }
        })
    
    return schema

def generate_breadcrumbs_schema(ville, type_page='demenagement'):
    """Génère le schema breadcrumbs"""
    ville_cap = ville.capitalize()
    type_cap = type_page.capitalize()
    
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Accueil",
                "item": "https://demenagement-zen.fr"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": f"{type_cap} {ville_cap}",
                "item": f"https://demenagement-zen.fr/{type_page}-{ville}"
            }
        ]
    }

if __name__ == '__main__':
    print("Script d'optimisation SEO pour pages volume > 1000")
    print("=" * 60)
    print(f"Villes à optimiser : {len(VILLES_CONFIG)}")
    for ville, config in VILLES_CONFIG.items():
        print(f"  - {ville.capitalize()} : Volume {config['volume']}")
    print("\nGénération des schémas FAQ et Breadcrumbs...")
    
    # Exemple de génération
    import json
    faq = generate_faq_schema('paris', 'demenagement')
    breadcrumbs = generate_breadcrumbs_schema('paris', 'demenagement')
    
    print("\nExemple FAQ Schema (Paris):")
    print(json.dumps(faq, indent=2, ensure_ascii=False))
    
    print("\nExemple Breadcrumbs Schema (Paris):")
    print(json.dumps(breadcrumbs, indent=2, ensure_ascii=False))

