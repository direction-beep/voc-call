# Positions Mots-Clés VOC-Call - N8N

**Dernière mise à jour** : 2025-12-15T15:35:33.465Z
**Source** : N8N Webhook

---

# ❌ Erreur de Configuration

Le nœud "Get row(s) in sheet" retourne des métadonnées au lieu des données.

**Métadonnées reçues:**
```json
{
  "success": true,
  "column": 8,
  "rowsUpdated": 230
}
```

**Solution:**

1. **Utilisez "Read Rows" au lieu de "Get row(s)"**
   - Nœud : Google Sheets → "Read Rows"
   - Sheet Tab/Name : `évolution`
   - Options → Use First Row as Headers : ✅ Activé
   - Range : Laissez vide

2. **OU corrigez "Get row(s) in sheet"**
   - Options → Use First Row as Headers : ✅ Activé
   - Options → Return All : ✅ Activé
   - Range : Laissez vide

**Voir le guide:** `seo/CORRECTION_GET_ROWS_SHEET_N8N.md`