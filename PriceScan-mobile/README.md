# PriceScan-mobile
Applicaytion mobile de comparateur de prix

# Installation et Configuration

---

# Dépendances à installer
npm install -g @ionic/cli
ionic start receipt-scanner tabs --type=angular
cd receipt-scanner

## Capacitor pour les fonctionnalités natives
npm install @capacitor/core @capacitor/cli
npm install @capacitor/camera
npm install @capacitor/storage

## Autres dépendances utiles
npm install @angular/common/http
npm install rxjs

---

# Configuration Capacitor
ionic build
ionic cap add android
ionic cap add ios
ionic cap sync

---

# Fonctionnalités Clés à Implémenter

    - Authentification utilisateur
    - Scan de reçus avec appareil photo
    - Traitement OCR des images
    - Validation et correction manuelle
    - Historique des reçus
    - Géolocalisation des magasins
    - Mode hors ligne avec synchronisation
    - Notifications push

---

# Considérations Techniques

État hors ligne : Utiliser Capacitor Storage pour la persistence locale
Performance : Optimiser les images avant envoi OCR
UX : Prévoir des états de chargement et des messages d'erreur
Sécurité : Chiffrer les données sensibles
Tests : Implémenter des tests unitaires et e2e