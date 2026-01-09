# 🔍 Guide : Suivre l'Activité de Google sur Votre Site

**Objectif** : Savoir combien de fois Google a regardé votre site (pages indexées, crawls, requêtes)

---

## 🎯 Outil Principal : Google Search Console

**Google Search Console** est l'outil gratuit de Google pour suivre :
- ✅ Nombre de pages indexées
- ✅ Nombre de requêtes de crawl (Googlebot)
- ✅ Pages découvertes
- ✅ Erreurs de crawl
- ✅ Positions dans les résultats

**URL** : https://search.google.com/search-console

---

## 📋 Étape 1 : Configurer Google Search Console

### **1.1 Ajouter votre site**

1. Allez sur https://search.google.com/search-console
2. Cliquez sur **"Ajouter une propriété"**
3. Choisissez **"Préfixe d'URL"** ou **"Domaine"**
4. Entrez votre URL : `https://voc-call.fr` ou `https://voc-call.com`

### **1.2 Vérifier la propriété**

**Méthode recommandée** : **Balise HTML**

1. Google vous donne un code à placer dans votre `<head>`
2. Ajoutez-le dans `index.html` (ligne après `<head>`)
3. Exemple :
```html
<meta name="google-site-verification" content="VOTRE_CODE_ICI" />
```
4. Cliquez sur **"Vérifier"** dans Search Console

**Alternative** : **Fichier HTML**
- Téléchargez le fichier HTML fourni
- Uploadez-le à la racine de votre site
- Cliquez sur **"Vérifier"**

**Alternative** : **DNS** (si vous avez accès)
- Ajoutez un enregistrement TXT dans votre DNS

---

## 📊 Étape 2 : Voir les Statistiques de Crawl

### **2.1 Pages Indexées**

**Où** : Google Search Console → **"Couverture"** (Indexage)

**Ce que vous voyez** :
- ✅ **Pages valides** : Nombre de pages indexées par Google
- ⚠️ **Pages avec avertissements** : Pages indexées mais avec problèmes
- ❌ **Pages exclues** : Pages non indexées (avec raison)
- ❌ **Erreurs** : Pages avec erreurs de crawl

**Exemple** :
- Pages valides : 45
- Pages exclues : 3
- **Total indexé** : 45 pages

### **2.2 Statistiques de Crawl**

**Où** : Google Search Console → **"Paramètres"** → **"Statistiques d'exploration"**

**Ce que vous voyez** :
- **Requêtes par jour** : Nombre de fois que Googlebot visite votre site par jour
- **Temps de téléchargement** : Vitesse de chargement des pages
- **Taille des pages téléchargées** : Volume de données crawlé
- **Codes de réponse** : 200 (OK), 404 (erreur), etc.

**Exemple** :
- Requêtes par jour : 150-200
- Temps de téléchargement moyen : 0.5s
- Pages téléchargées : 50 pages

### **2.3 Pages Découvertes**

**Où** : Google Search Console → **"Couverture"** → **"Découvertes"**

**Ce que vous voyez** :
- Nombre de nouvelles pages découvertes par Google
- Pages découvertes mais non indexées
- Raisons de non-indexation

---

## 📈 Étape 3 : Voir les Requêtes de Crawl en Détail

### **3.1 Historique des Crawls**

**Où** : Google Search Console → **"Paramètres"** → **"Statistiques d'exploration"**

**Graphique disponible** :
- **Requêtes par jour** (derniers 90 jours)
- **Temps de téléchargement** (derniers 90 jours)
- **Taille des pages téléchargées** (derniers 90 jours)

### **3.2 Dernières Requêtes**

**Où** : Google Search Console → **"URL Inspection"** (Inspection d'URL)

**Fonctionnalité** :
1. Entrez une URL de votre site
2. Cliquez sur **"Tester l'URL en direct"**
3. Vous voyez :
   - Dernière fois que Google a crawlé cette page
   - Statut d'indexation
   - Problèmes détectés

---

## 🔍 Étape 4 : Voir les Pages Indexées

### **4.1 Liste Complète des Pages Indexées**

**Où** : Google Search Console → **"Couverture"** → **"Pages valides"**

**Ce que vous voyez** :
- Liste de toutes les pages indexées
- Date de dernière découverte
- Date de dernière mise à jour
- Raison d'indexation

### **4.2 Recherche dans Google**

**Méthode rapide** : Recherche Google avec opérateur

**Recherche** : `site:voc-call.fr` ou `site:voc-call.com`

**Résultat** : Google affiche toutes les pages indexées de votre site

**Nombre de résultats** : En haut à droite, Google affiche "Environ X résultats"

---

## 📊 Étape 5 : Statistiques Détaillées

### **5.1 Rapport de Performance**

**Où** : Google Search Console → **"Performance"**

**Ce que vous voyez** :
- **Impressions** : Nombre de fois que votre site apparaît dans les résultats
- **Clics** : Nombre de clics depuis Google
- **CTR** : Taux de clic (clics / impressions)
- **Position moyenne** : Position moyenne dans les résultats

### **5.2 Requêtes (Mots-clés)**

**Où** : Google Search Console → **"Performance"** → **"Requêtes"**

**Ce que vous voyez** :
- Mots-clés pour lesquels votre site apparaît
- Nombre d'impressions par mot-clé
- Position moyenne par mot-clé
- Nombre de clics par mot-clé

---

## 🛠️ Outils Complémentaires

### **1. Google Analytics 4**

**Pour** : Voir le trafic organique (visiteurs venant de Google)

**Où** : https://analytics.google.com

**Métriques** :
- Visiteurs organiques (Google)
- Pages vues
- Taux de rebond
- Temps sur site

### **2. Outils en Ligne**

**SEMrush** (payant) :
- Nombre de pages indexées
- Backlinks
- Positions mots-clés

**Ahrefs** (payant) :
- Pages indexées
- Crawl budget
- Backlinks

**Ubersuggest** (gratuit limité) :
- Pages indexées
- Positions mots-clés

---

## 📋 Checklist : Configuration Initiale

### **À Faire Maintenant**

- [ ] **Créer un compte Google Search Console**
  - Aller sur https://search.google.com/search-console
  - Se connecter avec votre compte Google

- [ ] **Ajouter votre propriété**
  - Ajouter `https://voc-call.fr` ou `https://voc-call.com`
  - Choisir méthode de vérification

- [ ] **Vérifier la propriété**
  - Ajouter la balise meta dans `index.html`
  - Ou uploader le fichier HTML
  - Cliquer sur "Vérifier"

- [ ] **Soumettre le sitemap**
  - Aller dans **"Sitemaps"** dans Search Console
  - Entrer : `https://voc-call.fr/sitemap.xml`
  - Cliquer sur **"Envoyer"**

- [ ] **Attendre 24-48h**
  - Google commence à crawler votre site
  - Les données apparaissent progressivement

---

## 📊 Métriques à Surveiller

### **Métriques Importantes**

1. **Pages Indexées** (Couverture → Pages valides)
   - Objectif : Toutes vos pages importantes
   - Vérifier : Mensuellement

2. **Requêtes de Crawl** (Paramètres → Statistiques d'exploration)
   - Objectif : 50-200 requêtes/jour (selon taille site)
   - Vérifier : Hebdomadairement

3. **Temps de Téléchargement** (Paramètres → Statistiques d'exploration)
   - Objectif : < 1 seconde
   - Vérifier : Mensuellement

4. **Erreurs de Crawl** (Couverture → Erreurs)
   - Objectif : 0 erreur
   - Vérifier : Hebdomadairement

5. **Impressions** (Performance)
   - Objectif : Augmentation régulière
   - Vérifier : Hebdomadairement

---

## 🎯 Questions Fréquentes

### **Q1 : Combien de fois Google visite mon site ?**

**Réponse** : 
- Allez dans **Search Console → Paramètres → Statistiques d'exploration**
- Regardez le graphique **"Requêtes par jour"**
- Vous verrez le nombre exact de requêtes par jour

**Exemple** : 150-200 requêtes/jour = Google visite votre site 150-200 fois par jour

---

### **Q2 : Combien de pages Google a indexées ?**

**Réponse** :
- **Méthode 1** : Search Console → **Couverture → Pages valides**
- **Méthode 2** : Recherche Google `site:voc-call.fr`
- **Méthode 3** : Search Console → **Sitemaps** (nombre de pages soumises)

---

### **Q3 : Quand Google a crawlé ma page la dernière fois ?**

**Réponse** :
- Search Console → **Inspection d'URL**
- Entrez l'URL de votre page
- Cliquez sur **"Tester l'URL en direct"**
- Vous verrez la date du dernier crawl

---

### **Q4 : Pourquoi Google ne visite pas mon site souvent ?**

**Causes possibles** :
- Site récent (sandbox Google)
- Peu de contenu nouveau
- Problèmes techniques (vitesse, erreurs)
- Peu de backlinks

**Solutions** :
- Publier du contenu régulièrement (blog)
- Obtenir des backlinks
- Optimiser la vitesse
- Soumettre le sitemap

---

### **Q5 : Comment augmenter le nombre de crawls ?**

**Actions** :
1. **Publier du contenu régulièrement** (2-3x/semaine)
2. **Soumettre le sitemap** dans Search Console
3. **Obtenir des backlinks** (Google suit les liens)
4. **Optimiser la vitesse** (Google aime les sites rapides)
5. **Créer des liens internes** (Google suit les liens internes)

---

## 📱 Accès Rapide

### **Liens Utiles**

- **Google Search Console** : https://search.google.com/search-console
- **Google Analytics** : https://analytics.google.com
- **Test Rich Results** : https://search.google.com/test/rich-results
- **PageSpeed Insights** : https://pagespeed.web.dev/

---

## 🚀 Actions Immédiates

### **Cette Semaine**

1. [ ] **Créer compte Search Console** (si pas encore fait)
2. [ ] **Ajouter propriété** voc-call.fr ou voc-call.com
3. [ ] **Vérifier propriété** (balise meta ou fichier HTML)
4. [ ] **Soumettre sitemap** : `https://voc-call.fr/sitemap.xml`
5. [ ] **Attendre 24-48h** pour voir les premières données

### **Dans 1 Semaine**

1. [ ] **Vérifier pages indexées** (Couverture)
2. [ ] **Vérifier statistiques de crawl** (Paramètres)
3. [ ] **Vérifier erreurs** (Couverture → Erreurs)
4. [ ] **Vérifier impressions** (Performance)

---

## 💡 Conseils

### ✅ **À FAIRE**
- Vérifier Search Console **1x/semaine minimum**
- Surveiller les **erreurs de crawl**
- **Soumettre le sitemap** après chaque modification importante
- **Publier du contenu régulièrement** pour augmenter les crawls

### ❌ **À ÉVITER**
- Ignorer les erreurs de crawl
- Ne pas soumettre le sitemap
- Publier du contenu dupliqué
- Bloquer Google dans robots.txt (sauf si nécessaire)

---

## 📊 Exemple de Rapport

### **Statistiques Typiques (Site Moyen)**

- **Pages indexées** : 45-60 pages
- **Requêtes de crawl/jour** : 100-200
- **Temps de téléchargement** : 0.3-0.8s
- **Impressions/jour** : 500-2000
- **Clics/jour** : 20-100
- **CTR moyen** : 2-5%

---

**Dernière mise à jour** : Décembre 2024

