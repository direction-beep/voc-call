#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour optimiser automatiquement les pages restantes avec volume > 1000
"""

import re
import os

# Configuration des villes avec leurs informations
VILLES = {
    'nice': {
        'region': "Provence-Alpes-Côte d'Azur",
        'quartiers': "Promenade des Anglais, Vieux-Nice, Cimiez, ou vers les communes environnantes comme Cagnes-sur-Mer, Antibes, Cannes"
    },
    'rennes': {
        'region': "Bretagne",
        'quartiers': "centre-ville, quartiers historiques, ou vers les communes environnantes comme Saint-Jacques-de-la-Lande, Cesson-Sévigné, Bruz"
    },
    'rouen': {
        'region': "Normandie",
        'quartiers': "centre-ville historique, quartiers périphériques, ou vers les communes environnantes comme Mont-Saint-Aignan, Sotteville-lès-Rouen, Le Petit-Quevilly"
    },
    'annecy': {
        'region': "Auvergne-Rhône-Alpes",
        'quartiers': "centre-ville, quartiers périphériques, ou vers les communes environnantes comme Annecy-le-Vieux, Seynod, Cran-Gevrier"
    },
    'versailles': {
        'region': "Île-de-France",
        'quartiers': "centre-ville, quartiers résidentiels, ou vers les communes environnantes comme Viroflay, Le Chesnay, Buc"
    },
    'angers': {
        'region': "Pays de la Loire",
        'quartiers': "centre-ville, quartiers historiques, ou vers les communes environnantes comme Avrillé, Trélazé, Les Ponts-de-Cé"
    },
    'dijon': {
        'region': "Bourgogne-Franche-Comté",
        'quartiers': "centre-ville historique, quartiers périphériques, ou vers les communes environnantes comme Chenôve, Talant, Longvic"
    }
}

def optimiser_page_demenagement(ville, ville_capitalized):
    """Optimise une page demenagement-{ville}.html"""
    filename = f"demenagement-{ville}.html"
    
    if not os.path.exists(filename):
        print(f"⚠️  Fichier {filename} introuvable")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Meta title et description
    content = re.sub(
        r'<title>Déménagement [^|]* \| [^<]*</title>',
        f'<title>Déménagement {ville_capitalized} | Devis Gratuit - Déménagement Zen</title>',
        content
    )
    
    content = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="Déménagement professionnel à {ville_capitalized}. Équipe expérimentée, emballage soigné, transport sécurisé. Devis gratuit sous 24h. Intervention rapide dans toute la région."',
        content
    )
    
    # 2. H1
    content = re.sub(
        r'<h1 class="hero-title">([^<]*)</h1>',
        r'<h1>\1</h1>',
        content
    )
    
    # 3. Breadcrumbs Schema (après LocalBusiness)
    breadcrumbs_schema = f'''    </script>
    
    <!-- Breadcrumbs Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Accueil",
          "item": "https://demenagement-zen.fr"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Déménagement {ville_capitalized}",
          "item": "https://demenagement-zen.fr/demenagement-{ville}"
        }}
      ]
    }}
    </script>
    
    <!-- FAQ Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "Combien coûte un déménagement à {ville_capitalized} ?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Le prix d'un déménagement à {ville_capitalized} dépend du volume à déménager, de la distance, de l'étage et des services complémentaires. Nous proposons un devis gratuit et personnalisé pour chaque déménagement à {ville_capitalized}."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Quels services sont inclus dans un déménagement à {ville_capitalized} ?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Nos services de déménagement à {ville_capitalized} incluent : emballage professionnel, transport sécurisé, montage et démontage de meubles, installation d'électroménager. Nous intervenons pour les déménagements résidentiels et professionnels dans toute la région."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Comment organiser un déménagement à {ville_capitalized} ?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Pour organiser un déménagement à {ville_capitalized}, contactez-nous pour un devis gratuit. Nous planifions ensemble votre déménagement selon vos besoins : date, volume, services souhaités. Notre équipe intervient rapidement dans toute la région et vous recontacte sous 24h."
          }}
        }}
      ]
    }}
    </script>'''
    
    # Insérer après LocalBusiness schema
    content = re.sub(
        r'("description": "[^"]*")\s*\}\s*</script>',
        r'\1}\n' + breadcrumbs_schema,
        content,
        count=1
    )
    
    print(f"✅ {filename} optimisé")
    return True

if __name__ == "__main__":
    print("🚀 Optimisation des pages restantes...\n")
    
    for ville, infos in VILLES.items():
        ville_capitalized = ville.capitalize()
        optimiser_page_demenagement(ville, ville_capitalized)
    
    print("\n✨ Optimisation terminée !")

