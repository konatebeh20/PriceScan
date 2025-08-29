# TicketScan Dashboard

Un tableau de bord moderne et ergonomique pour la gestion des reçus et des dépenses, construit avec Angular 17 et des composants standalone.

## 🏗️ Architecture du Projet

### Structure des Dossiers

```
src/app/dashboard/
├── dashboard.html                 # Template principal du dashboard
├── dashboard.ts                   # Composant principal du dashboard
├── dashboard.scss                 # Styles du dashboard
├── includes/                      # Composants inclus
│   ├── sidebar/                   # Barre latérale de navigation
│   │   ├── sidebar.html
│   │   ├── sidebar.ts
│   │   └── sidebar.scss
│   └── quick-actions/             # Actions rapides
│       ├── quick-actions.html
│       ├── quick-actions.ts
│       └── quick-actions.scss
├── main/                          # Composants principaux
│   ├── main-layout/               # Layout principal avec header
│   │   ├── main-layout.html
│   │   ├── main-layout.ts
│   │   └── main-layout.scss
│   └── main-content/              # Contenu principal avec navigation des pages
│       ├── main-content.html
│       ├── main-content.ts
│       └── main-content.scss
└── pages/                         # Pages individuelles
    ├── dashboard-page/             # Page d'accueil du dashboard
    │   ├── dashboard-page.html
    │   ├── dashboard-page.ts
    │   └── dashboard-page.scss
    ├── receipts/                   # Gestion des reçus
    │   └── receipts-list/          # Liste des reçus
    │       ├── receipts-list.html
    │       ├── receipts-list.ts
    │       └── receipts-list.scss
    ├── products/                   # Gestion des produits
    │   └── products-list/          # Liste des produits
    │       ├── products-list.html
    │       ├── products-list.ts
    │       └── products-list.scss
    ├── stores/                     # Gestion des magasins
    │   └── stores-list/            # Liste des magasins
    │       ├── stores-list.html
    │       ├── stores-list.ts
    │       └── stores-list.scss
    └── settings/                   # Paramètres
        └── settings-page/          # Page des paramètres
            ├── settings-page.html
            ├── settings-page.ts
            └── settings-page.scss
```

## 🚀 Technologies Utilisées

- **Angular 17** - Framework principal avec composants standalone
- **TypeScript** - Langage de programmation
- **SCSS** - Préprocesseur CSS
- **Font Awesome** - Icônes
- **CSS Variables** - Système de thème (clair/sombre)

## ✨ Fonctionnalités

### Dashboard Principal
- Vue d'ensemble des statistiques (reçus, dépenses, moyennes)
- Activité récente
- Actions rapides

### Gestion des Reçus
- Liste des reçus avec filtres avancés
- Onglets (Tous, Récents, Archivés)
- Filtres par magasin, période, montant, statut
- Actions (Voir, Archiver, Imprimer)

### Gestion des Produits
- Liste des produits avec filtres
- Statistiques (Total, Actifs, Archivés)
- Filtres par catégorie, statut, prix
- Actions (Modifier, Archiver, Restaurer, Supprimer)

### Gestion des Magasins
- Liste des magasins avec filtres
- Statistiques par magasin
- Filtres par type, statut, ville
- Actions (Modifier, Archiver, Restaurer, Supprimer)

### Paramètres
- Paramètres du compte (notifications, thème)
- Gestion des données (export, import, réinitialisation)
- Aide et support
- Informations du compte

## 🎨 Système de Thème

Le projet utilise un système de thème basé sur les variables CSS avec support du mode sombre :

```scss
:root {
  --bg-primary: #F9FAFB;
  --bg-secondary: #FFFFFF;
  --text-primary: #1F2937;
  --accent-primary: #10B981;
  // ... autres variables
}

[data-theme="dark"] {
  --bg-primary: #111827;
  --bg-secondary: #1F2937;
  --text-primary: #F9FAFB;
  // ... variables du thème sombre
}
```

## 📱 Design Responsive

Tous les composants sont conçus pour être responsifs avec des breakpoints pour :
- **Desktop** : ≥ 1200px
- **Tablet** : 768px - 1199px  
- **Mobile** : < 768px

## 🔧 Installation et Démarrage

1. **Cloner le projet**
   ```bash
   git clone [url-du-repo]
   cd TicketScan-dashboard
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```

3. **Démarrer le serveur de développement**
   ```bash
   ng serve
   ```

4. **Ouvrir dans le navigateur**
   ```
   http://localhost:4200
   ```

## 🏗️ Construction du Projet

```bash
# Build de développement
ng build --configuration development

# Build de production
ng build --configuration production
```

## 📁 Composants Standalone

Tous les composants sont créés en tant que composants standalone Angular 17, ce qui signifie :
- Pas de NgModules requis
- Import direct dans les composants parents
- Meilleure tree-shaking
- Configuration simplifiée

## 🔄 Communication entre Composants

La communication entre composants se fait via :
- **@Input()** : Passage de données du parent vers l'enfant
- **@Output()** : Émission d'événements de l'enfant vers le parent
- **EventEmitter** : Gestion des événements personnalisés

## 🎯 Prochaines Étapes

- [ ] Implémentation des modales (ajout/édition)
- [ ] Intégration de la base de données
- [ ] Système d'authentification complet
- [ ] Tests unitaires et d'intégration
- [ ] Optimisation des performances
- [ ] PWA (Progressive Web App)

## 📝 Notes de Développement

- Tous les composants utilisent `standalone: true`
- Les styles sont organisés par composant avec préfixes
- Les interfaces TypeScript sont définies localement dans chaque composant
- Les méthodes sont préparées avec des TODO pour l'implémentation future
