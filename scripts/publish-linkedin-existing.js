/*
  Script pour publier rétroactivement des articles existants sur LinkedIn.
  Usage: node scripts/publish-linkedin-existing.js [slug]
  Si aucun slug n'est fourni, publie tous les articles du dossier blog/
*/

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const BLOG_DIR = path.join(ROOT, 'blog');

// LinkedIn integration
let linkedInModule = null;
try {
  linkedInModule = require('./linkedin');
} catch (e) {
  console.error('[linkedin] Module LinkedIn non disponible:', e.message);
  process.exit(1);
}

function log(msg) { console.log(`[publish-linkedin] ${msg}`); }

function extractMetaFromHTML(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  
  // Extract title from <title> tag
  const titleMatch = html.match(/<title>(.*?)<\/title>/i);
  const title = titleMatch ? titleMatch[1].replace(/\s*\|.*$/, '').trim() : null;
  
  // Extract description from meta description
  const descMatch = html.match(/<meta\s+name=["']description["']\s+content=["'](.*?)["']/i);
  const description = descMatch ? descMatch[1] : null;
  
  // Extract slug from filename
  const slug = path.basename(htmlPath, '.html');
  
  // Try to extract category from article content or use default
  let category = 'Blog';
  const categoryMatch = html.match(/article-category["'][^>]*>([^<]+)</i) || 
                         html.match(/class=["']article-category["'][^>]*>([^<]+)</i);
  if (categoryMatch) {
    category = categoryMatch[1].trim();
  }
  
  // Try to extract read time
  let readTime = '5 min';
  const readTimeMatch = html.match(/(\d+)\s*min\s*(?:de\s*lecture|de lecture)/i);
  if (readTimeMatch) {
    readTime = `${readTimeMatch[1]} min`;
  }
  
  // Try to extract date from meta or content
  let date = new Date().toISOString().split('T')[0];
  const dateMatch = html.match(/<meta\s+property=["']article:published_time["']\s+content=["']([^"']+)["']/i);
  if (dateMatch) {
    date = new Date(dateMatch[1]).toISOString().split('T')[0];
  }
  
  // Extract image
  let image = 'images/hero/hero-call-center.jpg';
  const imgMatch = html.match(/<img[^>]+src=["']([^"']*hero[^"']*)["']/i);
  if (imgMatch) {
    image = imgMatch[1].replace(/^\.\.\//, '');
  }
  
  return {
    slug,
    title: title || slug,
    date,
    category,
    image,
    excerpt: description || '',
    readTime
  };
}

async function publishArticleToLinkedIn(slug) {
  const htmlPath = path.join(BLOG_DIR, `${slug}.html`);
  
  if (!fs.existsSync(htmlPath)) {
    log(`Article ${slug} non trouvé`);
    return false;
  }
  
  log(`Extraction des métadonnées pour ${slug}...`);
  const meta = extractMetaFromHTML(htmlPath);
  
  log(`Métadonnées extraites:`);
  log(`  - Titre: ${meta.title}`);
  log(`  - Catégorie: ${meta.category}`);
  log(`  - Date: ${meta.date}`);
  log(`  - Temps de lecture: ${meta.readTime}`);
  
  if (!linkedInModule || !linkedInModule.publishToLinkedIn) {
    log('Module LinkedIn non disponible');
    return false;
  }
  
  try {
    log(`Publication sur LinkedIn...`);
    const success = await linkedInModule.publishToLinkedIn(meta);
    
    if (success) {
      log(`✓ Article ${slug} publié avec succès sur LinkedIn`);
      return true;
    } else {
      log(`⚠ Échec de la publication sur LinkedIn pour ${slug}`);
      return false;
    }
  } catch (err) {
    log(`✗ Erreur lors de la publication sur LinkedIn: ${err.message}`);
    return false;
  }
}

async function main() {
  const slug = process.argv[2];
  
  if (slug) {
    // Publier un article spécifique
    await publishArticleToLinkedIn(slug);
  } else {
    // Publier tous les articles du dossier blog/
    log('Publication de tous les articles existants sur LinkedIn...');
    const files = fs.readdirSync(BLOG_DIR)
      .filter(f => f.endsWith('.html') && !f.startsWith('categorie'));
    
    log(`Trouvé ${files.length} articles`);
    
    for (const file of files) {
      const slug = path.basename(file, '.html');
      log(`\n--- Traitement de ${slug} ---`);
      await publishArticleToLinkedIn(slug);
      // Attendre 2 secondes entre chaque publication pour éviter les rate limits
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    log('\n✓ Traitement terminé');
  }
}

main().catch(err => {
  console.error('[publish-linkedin] Erreur fatale:', err);
  process.exit(1);
});

