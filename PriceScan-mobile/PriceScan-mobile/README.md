# PriceScan Mobile

Une application mobile Ionic/Angular pour scanner des reçus et comparer les prix des produits.

## 🚀 Fonctionnalités

### 📸 Scanner de Reçus
- **Prise de photo** : Utilise la caméra de l'appareil pour capturer des reçus
- **Sélection d'image** : Importez des images existantes depuis la galerie
- **OCR automatique** : Analyse automatique du contenu des reçus via l'API backend
- **Édition manuelle** : Possibilité de corriger et compléter les informations extraites
- **Sauvegarde** : Stockage local et synchronisation avec le serveur

### 💰 Comparateur de Prix
- **Recherche de produits** : Trouvez des produits par nom, catégorie ou marque
- **Comparaison de prix** : Visualisez les prix dans différents magasins
- **Historique des prix** : Suivez l'évolution des prix dans le temps
- **Alertes de prix** : Recevez des notifications quand un produit atteint votre prix cible
- **Favoris** : Sauvegardez vos produits préférés

### 📱 Interface Utilisateur
- **Design moderne** : Interface intuitive et responsive
- **Mode sombre** : Thème sombre pour une meilleure expérience nocturne
- **Navigation intuitive** : Navigation par onglets et gestes
- **Responsive** : Optimisé pour tous les formats d'écran

## 🛠️ Technologies Utilisées

- **Frontend** : Ionic 8 + Angular 20
- **Stockage local** : Ionic Storage
- **Caméra** : Capacitor Camera
- **HTTP Client** : Angular HttpClient
- **Styles** : SCSS avec variables CSS personnalisées

## 📁 Structure du Projet

```
src/
├── app/
│   ├── components/
│   │   ├── receipt-scanner/          # Scanner de reçus
│   │   ├── receipt-detail-modal/     # Modal de détail des reçus
│   │   ├── receipt-list/             # Liste des reçus sauvegardés
│   │   └── price-comparison/         # Comparateur de prix
│   ├── services/
│   │   ├── api.service.ts            # Service API principal
│   │   ├── receipt.service.ts        # Gestion des reçus
│   │   ├── product.service.ts        # Gestion des produits
│   │   └── storage.service.ts        # Stockage local
│   ├── app.component.ts              # Composant principal
│   ├── app.routes.ts                 # Routes de l'application
│   └── app.config.ts                 # Configuration de l'app
├── environments/                      # Configuration par environnement
└── global.scss                       # Styles globaux
```

## 🔧 Installation et Configuration

### Prérequis
- Node.js 18+ et npm
- Ionic CLI
- Capacitor CLI

### Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd PriceScan-mobile
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```

3. **Configuration de l'environnement**
   - Modifiez `src/environments/environment.ts` avec l'URL de votre API backend
   - Ajustez les paramètres selon votre environnement

4. **Lancer l'application**
   ```bash
   # Mode développement
   npm start
   
   # Build pour production
   npm run build
   
   # Ajouter les plateformes mobiles
   ionic capacitor add android
   ionic capacitor add ios
   ```

## 🔌 Configuration de l'API

L'application nécessite un backend avec les endpoints suivants :

### Reçus
- `POST /api/receipts/scan` - Scanner un reçu (OCR)
- `POST /api/receipts` - Sauvegarder un reçu
- `GET /api/receipts/user/:userId` - Récupérer les reçus d'un utilisateur
- `PUT /api/receipts/:id` - Mettre à jour un reçu
- `DELETE /api/receipts/:id` - Supprimer un reçu

### Produits
- `GET /api/products/search` - Rechercher des produits
- `GET /api/products/:id/prices` - Comparaison de prix
- `GET /api/products/popular` - Produits populaires
- `GET /api/products/categories` - Catégories disponibles

### Favoris et Alertes
- `POST /api/favorites` - Ajouter aux favoris
- `DELETE /api/favorites/:id` - Supprimer des favoris
- `POST /api/price-alerts` - Créer une alerte de prix

## 📱 Utilisation

### Scanner un Reçu
1. Accédez à la page "Scanner"
2. Choisissez entre prendre une photo ou sélectionner une image
3. L'image est envoyée au serveur pour analyse OCR
4. Vérifiez et corrigez les informations extraites
5. Sauvegardez le reçu

### Comparer les Prix
1. Utilisez la barre de recherche pour trouver des produits
2. Consultez les détails et la comparaison de prix
3. Ajoutez des produits à vos favoris
4. Définissez des alertes de prix

### Gérer vos Reçus
1. Consultez la liste de vos reçus sauvegardés
2. Visualisez les statistiques de vos dépenses
3. Modifiez ou supprimez des reçus selon vos besoins

## 🎨 Personnalisation

### Thèmes et Couleurs
Les couleurs et thèmes sont définis dans les fichiers SCSS avec des variables CSS :
```scss
:root {
  --primary-color: #2a6bc9;
  --secondary-color: #f8f9fa;
  --text-color: #333;
  --border-color: #dee2e6;
}
```

### Styles Responsifs
L'application utilise des media queries pour s'adapter à différents formats d'écran :
```scss
@media (max-width: 576px) {
  // Styles pour mobile
}
```

## 🚀 Déploiement

### Android
```bash
ionic capacitor build android
ionic capacitor open android
```

### iOS
```bash
ionic capacitor build ios
ionic capacitor open ios
```

### Web
```bash
npm run build
# Déployer le dossier dist/ sur votre serveur web
```

## 🔒 Sécurité

- **Authentification** : Utilisation de tokens JWT pour l'API
- **Validation** : Validation côté client et serveur
- **Stockage sécurisé** : Utilisation d'Ionic Storage pour les données sensibles

## 📊 Performance

- **Lazy Loading** : Chargement à la demande des composants
- **Stockage local** : Mise en cache des données pour une meilleure performance
- **Optimisation des images** : Compression et redimensionnement automatiques

## 🐛 Dépannage

### Problèmes courants

1. **Erreur de caméra**
   - Vérifiez les permissions de l'appareil
   - Assurez-vous que Capacitor est correctement configuré

2. **Erreurs de synchronisation**
   - Vérifiez la connectivité internet
   - Contrôlez la configuration de l'API dans environment.ts

3. **Problèmes de stockage**
   - Vérifiez que Ionic Storage est correctement initialisé
   - Contrôlez les permissions de stockage

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Contactez l'équipe de développement

---

**PriceScan Mobile** - Votre compagnon intelligent pour la gestion des dépenses et la comparaison de prix ! 🎯
