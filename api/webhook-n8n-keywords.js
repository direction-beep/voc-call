/**
 * Webhook endpoint pour recevoir les positions de mots-clés depuis N8N
 * 
 * Usage: POST /api/webhook-n8n-keywords
 * 
 * Headers requis:
 * - Content-Type: application/json (ou text/markdown)
 * - X-Webhook-Secret: (votre secret pour sécuriser le webhook)
 * 
 * Body attendu (format JSON):
 * {
 *   "content": "# Positions Mots-Clés...\n\n## Priorité 1\n...",
 *   "format": "markdown"
 * }
 * 
 * OU (format markdown direct):
 * Content-Type: text/markdown
 * Body: "# Positions Mots-Clés...\n\n## Priorité 1\n..."
 */

const fs = require('fs');
const path = require('path');

// Configuration depuis les variables d'environnement
const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET || 'your-secret-key-change-this';

// Sur Vercel, on ne peut pas écrire dans le système de fichiers du projet
// On retourne le contenu pour qu'il soit sauvegardé côté client ou via API
// Pour l'instant, on utilise /tmp (temporaire) ou on retourne juste le contenu
const IS_VERCEL = process.env.VERCEL === '1';
const OUTPUT_FILE = IS_VERCEL 
  ? path.join('/tmp', 'positions-keywords-n8n.md')
  : path.join(process.cwd(), 'seo', 'positions-keywords-n8n.md');

/**
 * Sauvegarder le contenu markdown dans le fichier
 */
function saveKeywordsFile(content, withDate = false) {
  try {
    // Créer le dossier seo s'il n'existe pas
    const seoDir = path.dirname(OUTPUT_FILE);
    if (!fs.existsSync(seoDir)) {
      fs.mkdirSync(seoDir, { recursive: true });
    }

    // Déterminer le nom du fichier
    let filePath = OUTPUT_FILE;
    if (withDate) {
      const date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
      const dir = path.dirname(OUTPUT_FILE);
      const name = path.basename(OUTPUT_FILE, '.md');
      filePath = path.join(dir, `${name}-${date}.md`);
    }

    // Ajouter un en-tête avec la date de mise à jour
    const header = `# Positions Mots-Clés VOC-Call - N8N

**Dernière mise à jour** : ${new Date().toISOString()}
**Source** : N8N Webhook

---

`;
    
    const fullContent = header + content;

    // Sauvegarder le fichier
    fs.writeFileSync(filePath, fullContent, 'utf8');

    return {
      success: true,
      filePath: filePath,
      size: fullContent.length,
      message: 'Keywords file saved successfully'
    };
  } catch (error) {
    throw new Error(`Failed to save file: ${error.message}`);
  }
}

/**
 * Handler principal du webhook (format Vercel)
 */
export default async function handler(req, res) {
  // Seulement POST
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      error: 'Method not allowed',
      message: 'Only POST requests are allowed'
    });
  }

  // Vérifier le secret du webhook
  const webhookSecret = req.headers['x-webhook-secret'];
  if (!webhookSecret || webhookSecret !== WEBHOOK_SECRET) {
    return res.status(401).json({ 
      error: 'Unauthorized',
      message: 'Invalid or missing webhook secret'
    });
  }

  try {
    const contentType = req.headers['content-type'] || '';
    let markdownContent = '';

    // Gérer deux formats : JSON ou Markdown direct
    if (contentType.includes('application/json')) {
      // Format JSON : { "content": "...", "format": "markdown", "withDate": false }
      const { content, format, withDate } = req.body;

      if (!content) {
        return res.status(400).json({ 
          error: 'Bad request',
          message: 'Missing required field: content'
        });
      }

      if (format === 'markdown' || typeof content === 'string') {
        markdownContent = content;
      } else {
        return res.status(400).json({ 
          error: 'Bad request',
          message: 'Content must be a markdown string or format must be "markdown"'
        });
      }

      // Sur Vercel, on ne peut pas écrire dans le système de fichiers
      // On retourne le contenu pour qu'il soit sauvegardé côté client
      try {
        const result = saveKeywordsFile(markdownContent, withDate || false);
        return res.status(200).json({
          success: true,
          message: 'Keywords data received and saved successfully',
          data: result,
          content: markdownContent // Inclure le contenu pour sauvegarde alternative
        });
      } catch (fileError) {
        // Si l'écriture échoue (Vercel), on retourne quand même le contenu
        return res.status(200).json({
          success: true,
          message: 'Keywords data received (file write may have failed on Vercel)',
          content: markdownContent,
          warning: 'File system is read-only on Vercel. Use the content field to save locally.'
        });
      }

    } else if (contentType.includes('text/markdown') || contentType.includes('text/plain')) {
      // Format Markdown direct : le body est directement le markdown
      markdownContent = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);

      // Sur Vercel, on ne peut pas écrire dans le système de fichiers
      try {
        const result = saveKeywordsFile(markdownContent, false);
        return res.status(200).json({
          success: true,
          message: 'Keywords data received and saved successfully',
          data: result,
          content: markdownContent
        });
      } catch (fileError) {
        // Si l'écriture échoue (Vercel), on retourne quand même le contenu
        return res.status(200).json({
          success: true,
          message: 'Keywords data received (file write may have failed on Vercel)',
          content: markdownContent,
          warning: 'File system is read-only on Vercel. Use the content field to save locally.'
        });
      }

    } else {
      return res.status(400).json({ 
        error: 'Bad request',
        message: 'Content-Type must be application/json or text/markdown'
      });
    }

  } catch (error) {
    console.error('Webhook error:', error);
    
    return res.status(500).json({
      error: 'Internal server error',
      message: error.message || 'Failed to save keywords data'
    });
  }
}

// Support pour les serveurs Node.js locaux (non-Vercel)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = handler;
}


