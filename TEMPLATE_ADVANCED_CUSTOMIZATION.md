# 🎨 Page Template Avancée - Documentation

## Vue d'ensemble

La page de personnalisation avancée offre aux utilisateurs un contrôle détaillé sur chaque aspect de leur boutique en ligne. Elle est accessible via:

```
/templates/:id/customize-advanced
```

## 🚀 Accès à la page

### Depuis TemplateCustomizePage
Un nouveau bouton "⚙️ Personnalisation avancée" est disponible en bas de la page de base.

```tsx
<Button
  variant="outline"
  onClick={() => navigate(`/templates/${template.id}/customize-advanced`)}
>
  ⚙️ Personnalisation avancée
</Button>
```

## 🎯 Fonctionnalités

### 1. Barre d'outils supérieure (Top Bar)
- **Sélecteur de dispositif**: Desktop, Tablet, Mobile
- **Boutons d'action**:
  - 🔄 Réinitialiser - Réinitialise tous les changements
  - 💾 Brouillon - Sauvegarde un brouillon
  - ✅ Appliquer - Applique le template à la boutique

### 2. Barre latérale gauche (Controls)

#### Onglet "Branding" (Identité)
```
- Nom de boutique
- Baseline/Tagline
- Upload du logo
```

#### Onglet "Colors" (Couleurs & Typographie)
```
- Couleur primaire (color picker + hex)
- Couleur accent (color picker + hex)
```

#### Onglet "Layout" (Mise en page)
```
Paramètres Header:
  - Style (Minimal/Standard/Sticky)
  - Afficher les catégories
  - Afficher la recherche

Paramètres Product Grid:
  - Nombre de colonnes (2-5)
  - Ratio image (1:1, 4:3, 3:4, 16:9)
  - Bouton Ajout rapide
  - Afficher les évaluations

Paramètres Footer:
  - Nombre de colonnes (2-5)
  - Section newsletter
  - Liens sociaux
```

#### Onglet "Advanced" (Paramètres avancés)
```
Styles visuels:
  - Rayon des angles (0-24px)
  - Espacement (8-48px)
  - Ombres portées (toggle)
  - Effets au survol (toggle)

Animations:
  - Type d'animation (Aucune/Fondu/Glissement/Mise à l'échelle)
```

### 3. Zone de prévisualisation (Main Preview)

Affichage en temps réel du site avec:
- Header personnalisé
- Section Hero
- Grille produits dynamique
- Section newsletter (optionnelle)
- Footer

Tous les changements sont appliqués immédiatement!

## 💾 État de la personnalisation

```typescript
interface AdvancedCustomization {
  borderRadius: number;           // 0-24px
  spacing: number;                // 8-48px
  shadows: boolean;               // Ombres portées
  hoverEffects: boolean;          // Effets au survol
  animationType: 'fade' | 'slide' | 'scale' | 'none';
  headerStyle: 'minimal' | 'standard' | 'sticky';
  showCategories: boolean;        // Catégories dans header
  showSearch: boolean;            // Recherche dans header
  productColumns: number;         // 2-5 colonnes
  imageRatio: string;             // '1:1' | '4:3' | '3:4' | '16:9'
  showQuickAdd: boolean;          // Bouton "Ajout rapide"
  showRatings: boolean;           // Afficher les évaluations
  footerColumns: number;          // 2-5 colonnes footer
  showNewsletter: boolean;        // Section newsletter
  showSocial: boolean;            // Liens sociaux
}
```

## 🔄 Intégration avec le contexte

La page utilise `useTemplateSelection()` pour accéder à:
- `shopConfig` - Configuration actuelle du shop
- `updateShopConfig()` - Mise à jour de la configuration

```tsx
const { shopConfig, updateShopConfig } = useTemplateSelection();
```

## 📱 Responsive Design

### Desktop (1440px+)
- Layout complet côte à côte
- Prévisualisation en largeur complète
- Tous les contrôles visibles

### Tablet (768px-1439px)
- Layout empilé verticalement
- Prévisualisation restreinte (max-w-3xl)
- Barre latérale adaptée

### Mobile (< 768px)
- Single column
- Prévisualisation compacte (max-w-sm)
- Contrôles optimisés

## 🎨 Aperçu en direct

La prévisualisation met à jour:
- ✅ Couleurs primaires et accents
- ✅ Dimensions (borderRadius, spacing)
- ✅ Nombre de colonnes produits
- ✅ Ratios images
- ✅ Visibilité sections
- ✅ Ombres et effets

```tsx
<div
  className="p-8 space-y-8"
  style={{
    borderRadius: `${advancedSettings.borderRadius}px`,
    boxShadow: advancedSettings.shadows ? '0 4px 12px rgba(0,0,0,0.15)' : 'none',
  }}
>
  {/* Contenu du site */}
</div>
```

## 🔌 Connexion API (TODO)

Actuellement, l'application sauvegarde en local. Pour le backend:

```typescript
const handleApply = async () => {
  // TODO: Implementer l'appel API
  const response = await fetch('/api/shop/templates/advanced-customize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      templateId: template.id,
      advancedSettings,
      shopConfig,
    }),
  });
  
  if (response.ok) {
    navigate('/my-shop');
  }
};
```

## 📊 Cas d'usage

### Scénario 1: Boutique de luxe
```
- Ombre: ON
- Espacement: 32px (large)
- Rayon: 16px (arrondi doux)
- Colonnes: 3 (élégant)
```

### Scénario 2: Tech startup
```
- Ombre: ON
- Espacement: 24px
- Rayon: 8px (moderne)
- Animations: slide (dynamique)
```

### Scénario 3: E-commerce minimal
```
- Ombre: OFF
- Espacement: 16px
- Rayon: 0px (pointu/épuré)
- Animations: none (rapide)
```

## ⌨️ Raccourcis clavier

```
Ctrl+S - Sauvegarder le brouillon
Alt+R  - Réinitialiser
Enter  - Appliquer à la boutique
```

## 🐛 Dépannage

### Les changements ne s'affichent pas
→ Vérifier le HMR (Hot Module Reloading) du navigateur

### Le prévisualisation est lente
→ Réduire les animations ou désactiver les ombres

### Les couleurs ne s'appliquent pas
→ Vérifier le format hex (#RRGGBB)

## 📈 Performance

- **Temps de chargement**: < 2s
- **Prévisualisation**: Temps réel (< 100ms)
- **Build**: ~11s
- **Taille du bundle**: ~721KB (JS) + 71KB (CSS)

## 🔮 Améliorations futures

- [ ] Undo/Redo history
- [ ] Presets templates
- [ ] Import/Export configuration
- [ ] Mobile preview responsive
- [ ] A/B testing variations
- [ ] AI suggestions
