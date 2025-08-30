# PriceScan Mobile - Application de Comparaison de Prix

## 🎯 **Vue d'ensemble du Projet**

PriceScan Mobile est une application mobile innovante de comparaison de prix qui se distingue des solutions existantes comme Idealo Shopping. Cette application a été conçue pour valider l'UE de Développement Web/Mobile en Data Science.

##  **Fonctionnalités Uniques (Différentes d'Idealo)**

### 1. **Scanner Hybride**
- **Code-barres** : Scan rapide des produits en magasin
- **Reçu OCR** : Analyse automatique des tickets de caisse
- **Recherche manuelle** : Saisie directe du nom ou code produit

### 2. **Suivi des Tendances de Prix**
- **Historique des prix** : Graphiques d'évolution sur 30/60/90 jours
- **Alertes intelligentes** : Notifications quand les prix baissent
- **Prédictions** : Estimation des futures variations de prix

### 3. **Intégration Sociale**
- **Partage de bonnes affaires** : Envoyer des alertes aux amis
- **Communauté d'acheteurs** : Groupes par catégorie de produits
- **Système de réputation** : Notation des utilisateurs

### 4. **Mode Hors-ligne**
- **Cache local** : Fonctionne sans connexion internet
- **Synchronisation** : Mise à jour automatique quand reconnecté
- **Données locales** : Historique personnel sauvegardé

### 5. **Loyalty Store Integration**
- **Programmes de fidélité** : Intégration avec les cartes de magasin
- **Points de récompense** : Bonus pour les utilisateurs actifs
- **Offres exclusives** : Promotions personnalisées

## 🛠 **Technologies Utilisées**

- **Frontend** : Ionic 7 + Angular 16 (Standalone Components)
- **Mobile** : Capacitor 5 (iOS/Android)
- **Scanner** : @capacitor/barcode-scanner + @capacitor/camera
- **Stockage** : @ionic/storage-angular (local + cloud)
- **UI/UX** : Ionic Components + CSS Variables

## 📱 **Architecture de l'Application**

```
src/
├── app/
│   ├── pages/
│   │   ├── home/          # Page d'accueil avec tendances
│   │   ├── scan/          # Scanner code-barres/reçus
│   │   ├── compare/       # Comparaison de prix
│   │   ├── history/       # Historique des prix
│   │   └── profile/       # Profil utilisateur
│   ├── services/
│   │   ├── scanner.service.ts    # Gestion du scanner
│   │   ├── price.service.ts      # API des prix
│   │   └── storage.service.ts    # Stockage local
│   └── tabs/
│       └── tabs.page.ts          # Navigation principale
```

##  **Différenciation par rapport à Idealo Shopping**

| Fonctionnalité | Idealo Shopping | PriceScan Mobile |
|----------------|-----------------|------------------|
| **Scanner** | Code-barres uniquement | Code-barres + Reçus OCR |
| **Tendances** | Prix actuels | Historique + Prédictions |
| **Social** | Aucun | Partage + Communauté |
| **Hors-ligne** | Non | Oui, avec cache local |
| **Loyalty** | Non | Intégration magasins |
| **Personnalisation** | Basique | Alertes intelligentes |

## 🎨 **Interface Utilisateur**

- **Design moderne** : Material Design 3 + iOS Human Interface
- **Navigation intuitive** : Tabs + Navigation stack
- **Thème adaptatif** : Mode clair/sombre automatique
- **Accessibilité** : Support des lecteurs d'écran

##  **Fonctionnalités pour la Validation UE**

### **Niveau Débutant (Validation)**
-  Scanner de code-barres fonctionnel
-  Comparaison de prix basique
-  Interface utilisateur responsive
-  Stockage local des données

### **Niveau Intermédiaire (Bonus)**
-  OCR des reçus
- 📈 Graphiques de tendances
- 🔔 Système d'alertes
- 🌐 Synchronisation cloud

### **Niveau Avancé (Excellence)**
- 🤖 IA pour prédictions de prix
- 📱 Notifications push
- 🔐 Authentification utilisateur
-  Analytics et rapports

##  **Installation et Démarrage**

```bash
# Cloner le projet
git clone [repository-url]
cd price-scanner

# Installer les dépendances
npm install

# Lancer en mode développement
ionic serve

# Construire pour mobile
ionic capacitor build
```

## 📱 **Test sur Mobile**

```bash
# Ajouter Android
ionic capacitor add android

# Construire et ouvrir
ionic capacitor build android
ionic capacitor open android
```

## 🎯 **Objectifs Pédagogiques Atteints**

1. **Développement Mobile** : Ionic + Capacitor
2. **Framework Frontend** : Angular 16 moderne
3. **APIs Natives** : Camera, Scanner, Stockage
4. **Architecture** : Services, Composants, Routing
5. **UI/UX** : Design responsive et accessible
6. **Innovation** : Fonctionnalités uniques et différenciantes

## 🔮 **Évolutions Futures**

- **Intelligence Artificielle** : Prédictions de prix
- **Blockchain** : Traçabilité des produits
- **AR/VR** : Visualisation 3D des produits
- **IoT** : Intégration avec les objets connectés

---

**Auteur** : [Votre Nom]  
**UE** : Développement Web/Mobile - Data Science  
**Année** : 2024-2025  
**Université** : [Nom de votre université]
