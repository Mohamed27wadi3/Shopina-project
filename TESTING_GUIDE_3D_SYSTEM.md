# 🧪 Guide de Test Complet - Shopina 3D System

## ✅ Checklist de Tests

### 1. **Dashboard** 📊
- [ ] Charger `/dashboard/` → Vérifier le layout sidebar + header
- [ ] Cliquer sur le logo "Shopina" → Doit rediriger vers `/`
- [ ] Vérifier que les 4 statistiques s'affichent (Orders, Clients, Products, Revenue)
- [ ] Cartes flottantes au hover → Transform translateY visible
- [ ] Ombres douces au hover → Box-shadow increase
- [ ] Menu sidebar:
  - [ ] "Tableau de bord" (active)
  - [ ] "Commandes" → Lien vers `/orders/`
  - [ ] "Clients" → Lien vers `/clients/`

### 2. **Theme Toggle** 🌓
- [ ] Cliquer sur bouton 🌓 en header
- [ ] Vérifier changement theme dark → light
- [ ] Vérifier localStorage `theme` est défini
- [ ] Recharger la page → Theme doit persister
- [ ] Tous les éléments changent de couleur:
  - [ ] Background change
  - [ ] Text change
  - [ ] Borders change
  - [ ] Shadows change

### 3. **Avatar Dropdown** 👤
- [ ] Avatar affiche initiale utilisateur (ou image si avatar existe)
- [ ] Cliquer sur avatar → Dropdown s'ouvre avec animation bounce
- [ ] Vérifier items:
  - [ ] "Profil" → Lien vers `{% url 'profile_dynamic' %}`
  - [ ] "Paramètres" → Lien vers `/profile-settings/`
  - [ ] "Déconnexion" → Lien vers `/accounts/logout/`
- [ ] Cliquer en dehors → Dropdown se ferme
- [ ] Dropdown animation smooth (cubic-bezier bounce)
- [ ] Hover sur items → Background change + color accent

### 4. **Page Commandes** 📦
- [ ] Charger `/orders/` → Vérifier layout identique au Dashboard
- [ ] Tableau affiche commandes avec colonnes:
  - [ ] Commande #
  - [ ] Client
  - [ ] Montant
  - [ ] Statut (chips avec couleurs)
  - [ ] Date
  - [ ] Actions (Voir/Éditer/Supprimer)
- [ ] Chips de statut:
  - [ ] completed → Vert
  - [ ] processing → Bleu
  - [ ] pending → Orange
  - [ ] cancelled → Rouge
- [ ] Boutons d'action:
  - [ ] Voir (blue primary)
  - [ ] Éditer (border)
  - [ ] Supprimer (red danger)
- [ ] Hover sur boutons → Transform + shadow
- [ ] Aucune commande → Empty state avec icône 📭
- [ ] Navigation sidebar actif sur "Commandes"

### 5. **Page Settings** ⚙️
- [ ] Charger `/profile-settings/` → Vérifier layout
- [ ] Affichage 3 sections:
  - [ ] 🔐 Changer le mot de passe
  - [ ] 👤 Informations du profil
  - [ ] ⚠️ Zone de danger
- [ ] Formulaire mot de passe:
  - [ ] Champ "Mot de passe actuel"
  - [ ] Champ "Nouveau mot de passe"
  - [ ] Champ "Confirmer le mot de passe"
  - [ ] Bouton "Enregistrer" (primary)
  - [ ] Bouton "Annuler"
- [ ] Formulaire profil:
  - [ ] Champs pré-remplis (first_name, last_name, email)
  - [ ] Modification possible
  - [ ] Boutons Enregistrer/Annuler
- [ ] Zone danger:
  - [ ] Gradient rouge visible
  - [ ] Bouton "Déconnexion" en rouge
  - [ ] Lien "Voir mon profil"
- [ ] Aucune redirection vers Django password_change

### 6. **Responsive Design** 📱
- [ ] Desktop (> 1024px):
  - [ ] Sidebar visible (280px)
  - [ ] Layout normal
  - [ ] All elements visible
- [ ] Tablet (768-1024px):
  - [ ] Sidebar width 240px
  - [ ] Layout adapté
- [ ] Mobile (< 768px):
  - [ ] Sidebar hidden (transform translateX)
  - [ ] Header responsive
  - [ ] Table compact (font-size 12px)
  - [ ] Buttons stack (flex-wrap)
  - [ ] Content padding réduit
- [ ] Rotate viewport:
  - [ ] Layout réarrange correctement
  - [ ] Pas de horizontal scroll

### 7. **Navigation** 🧭
- [ ] Depuis Dashboard:
  - [ ] Cliquer "Commandes" → `/orders/`
  - [ ] Cliquer "Clients" → `/clients/`
  - [ ] Cliquer logo → `/`
- [ ] Depuis Commandes:
  - [ ] Cliquer "Tableau de bord" → `/dashboard/`
  - [ ] Cliquer "Clients" → `/clients/`
  - [ ] Avatar Dropdown "Profil" → Profile dynamic page
  - [ ] Avatar Dropdown "Paramètres" → `/profile-settings/`

### 8. **Curseur Personnalisé** 🎯
- [ ] Curseur par défaut bleu
- [ ] Hover sur boutons → Curseur violet
- [ ] Hover sur liens → Curseur violet
- [ ] Hover sur stat cards → Curseur violet
- [ ] Exit hover → Retour curseur bleu

### 9. **CSS Effects** ✨
- [ ] Glassmorphism visible:
  - [ ] Backdrop blur sur cartes
  - [ ] Semi-transparent background
  - [ ] Border subtle
- [ ] Shadows:
  - [ ] Shadow-md : `0 4px 12px rgba(...)`
  - [ ] Shadow-lg : `0 10px 28px rgba(...)`
  - [ ] Increase on hover
- [ ] Transforms:
  - [ ] translateY(-8px) on stat cards
  - [ ] scale(1.02) on stat cards
  - [ ] translateY(-2px) on buttons
  - [ ] rotate(15deg) on theme toggle
- [ ] Colors:
  - [ ] Text primary lisible
  - [ ] Accents cohérents
  - [ ] Borders subtle
  - [ ] Hover states clairs

### 10. **Accessibility** ♿
- [ ] Theme persiste sur reload
- [ ] Focus visible sur inputs
- [ ] Focus visible sur buttons
- [ ] Keyboard navigation fonctionne
- [ ] Alt text sur images (si utilisé)
- [ ] Color contrast acceptable

### 11. **Performance** ⚡
- [ ] Page dashboard charge en < 2s
- [ ] Pas de lag au hover
- [ ] Animations smooth (60fps)
- [ ] Pas d'erreurs console
- [ ] LocalStorage fonctionne
- [ ] Images optimisées

### 12. **Browser Compatibility** 🌐
- [ ] Chrome ✅
- [ ] Firefox ✅
- [ ] Safari ✅
- [ ] Edge ✅
- [ ] Mobile Safari ✅
- [ ] Chrome Mobile ✅

---

## 🐛 Bug Fixes Verification

### Previously Fixed Issues:
- [ ] Avatar dropdown n'était pas fonctionnel → **FIXED** (JavaScript event listeners)
- [ ] Logo non cliquable → **FIXED** (href="/")
- [ ] Redirection Django sur Settings → **FIXED** (Custom profile_settings.html)
- [ ] Boutons Orders non fonctionnels → **FIXED** (URL routing)
- [ ] Pas de curseur 3D → **FIXED** (SVG data-uri)
- [ ] Design inconsistent → **FIXED** (CSS variables)
- [ ] Pas de theme toggle → **FIXED** (localStorage + data-theme)

---

## 📋 Form Validation Tests

### Password Change Form:
```
- [ ] Submit empty form → Show validation error
- [ ] Submit with mismatched passwords → Error
- [ ] Submit valid → Redirect ou message success
- [ ] CSRF token présent
```

### Profile Form:
```
- [ ] Pre-filled fields work
- [ ] Can modify and save
- [ ] Email validation
- [ ] CSRF token présent
```

---

## 🔍 Console Tests

```javascript
// Theme Management
console.log(localStorage.getItem('theme'))           // dark|light
console.log(document.documentElement.getAttribute('data-theme'))

// Profile Dropdown
console.log(document.getElementById('profileDropdown').classList)

// Sidebar State
console.log(document.getElementById('sidebar').classList)
```

---

## 🎯 Visual Regression Tests

**Compare before & after:**
1. Screenshot Dashboard (dark mode)
2. Screenshot Dashboard (light mode)
3. Screenshot Orders page
4. Screenshot Settings page
5. Screenshot Mobile (all pages)
6. Screenshot Dropdown interaction
7. Screenshot Hover effects

---

## ✅ Final Checklist

- [ ] All pages load correctly
- [ ] All links functional
- [ ] Theme toggle works
- [ ] Responsive on all devices
- [ ] No console errors
- [ ] Accessibility acceptable
- [ ] Performance good (< 2s load)
- [ ] No broken images
- [ ] All buttons clickable
- [ ] All forms submittable
- [ ] Navigation complete
- [ ] Design consistent
- [ ] Animations smooth
- [ ] Colors correct
- [ ] Fonts correct
- [ ] Spacing consistent

---

## 🚀 Deployment Checklist

- [ ] Remove console.log statements
- [ ] Minify CSS (optional, Vite handles it)
- [ ] Test in production mode
- [ ] Verify Django DEBUG = False works
- [ ] Check static files served correctly
- [ ] Test with different user roles
- [ ] Verify CSRF protection works
- [ ] Test on real devices
- [ ] Check SEO meta tags
- [ ] Verify 404/500 error pages
- [ ] Test with slow network (3G)
- [ ] Test with disabled JavaScript

---

## 📞 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Theme not persisting | Check localStorage in DevTools |
| Dropdown not opening | Check `#profileDropdown` element exists |
| Sidebar not responsive | Check viewport meta tag |
| Curseur not changing | Clear browser cache |
| Styling broken | Verify CSS variables defined |
| Links broken | Check URL names in Django |
| Forms not submitting | Check CSRF token + action URL |
| No shadow on cards | Check browser supports box-shadow |
| Blur not working | Check `backdrop-filter` support |
| Mobile issues | Check `<meta name="viewport">` |

---

**Test Version:** 2024  
**Status:** Ready for Testing  
**Estimated Time:** 30-45 minutes
