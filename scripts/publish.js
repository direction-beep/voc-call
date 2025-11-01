/*
  Publish scheduled blog drafts.
  Draft structure:
  blog/_drafts/<slug>/meta.json
  blog/_drafts/<slug>/index.html

  meta.json example:
  {
    "slug": "backoffice-digital-delais-reponse",
    "title": "Back‑office digital : réduire les délais de réponse",
    "date": "2025-11-08",
    "category": "Technique",
    "image": "images/hero/hero-back-office.jpg",
    "excerpt": "Emails, chat, réseaux sociaux : méthodes et outils pour accuser réception et répondre vite.",
    "readTime": "6 min"
  }
*/

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DRAFTS_DIR = path.join(ROOT, 'blog', '_drafts');
const BLOG_DIR = path.join(ROOT, 'blog');
const BLOG_LIST = path.join(ROOT, 'blog.html');

function log(msg) { console.log(`[publish] ${msg}`); }

function loadJSON(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function formatDateLabel(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'long', year: 'numeric' });
}

function insertCardIntoBlogList(meta) {
  if (!fs.existsSync(BLOG_LIST)) {
    log('blog.html not found; skip card insertion');
    return;
  }
  const html = fs.readFileSync(BLOG_LIST, 'utf8');
  const marker = '<div class="articles-grid">';
  const idx = html.indexOf(marker);
  if (idx === -1) {
    log('articles-grid marker not found; skip');
    return;
  }

  const card = `\n                        <article class="blog-article">\n                            <div class="article-image">\n                                <img src="${meta.image}" alt="${meta.title}" loading="lazy">\n                                <div class="article-category">${meta.category || 'Blog'}</div>\n                            </div>\n                            <div class="article-content">\n                                <h3 class="article-title">\n                                    <a href="blog/${meta.slug}.html">${meta.title}</a>\n                                </h3>\n                                <p class="article-excerpt">${meta.excerpt || ''}</p>\n                                <div class="article-meta">\n                                    <span class="article-date"><i class="fas fa-calendar"></i> ${formatDateLabel(meta.date)}</span>\n                                    <span class="article-read-time"><i class="fas fa-clock"></i> ${meta.readTime || ''}</span>\n                                </div>\n                            </div>\n                        </article>`;

  const updated = html.slice(0, idx + marker.length) + card + html.slice(idx + marker.length);
  fs.writeFileSync(BLOG_LIST, updated, 'utf8');
  log(`Inserted card for ${meta.slug} in blog.html`);
}

function publishDraft(draftDir) {
  const metaPath = path.join(draftDir, 'meta.json');
  const htmlPath = path.join(draftDir, 'index.html');
  if (!fs.existsSync(metaPath) || !fs.existsSync(htmlPath)) {
    log(`skip ${draftDir} (missing meta/index)`);
    return false;
  }
  const meta = loadJSON(metaPath);
  const today = new Date();
  const due = new Date(meta.date);
  if (isNaN(due)) { log(`invalid date in ${metaPath}`); return false; }
  if (due > today) { return false; }

  const target = path.join(BLOG_DIR, `${meta.slug}.html`);
  if (fs.existsSync(target)) { log(`already published: ${meta.slug}`); return false; }

  fs.copyFileSync(htmlPath, target);
  insertCardIntoBlogList(meta);
  log(`published ${meta.slug}`);
  return true;
}

function main() {
  if (!fs.existsSync(DRAFTS_DIR)) {
    log('no drafts dir; nothing to do');
    return;
  }
  const entries = fs.readdirSync(DRAFTS_DIR, { withFileTypes: true }).filter(e => e.isDirectory());
  let publishedAny = false;
  for (const e of entries) {
    const ok = publishDraft(path.join(DRAFTS_DIR, e.name));
    if (ok) publishedAny = true;
  }
  log(publishedAny ? 'done with publications' : 'no draft due today');
}

main();


