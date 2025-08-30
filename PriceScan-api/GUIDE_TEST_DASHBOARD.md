# 🧪 GUIDE DE TEST DU DASHBOARD PRICESCAN

##  État actuel
- **API Flask** :  Fonctionne parfaitement
- **Base de données MySQL** :  Connectée et fonctionnelle
- **Endpoints d'authentification** :  Testés et validés
- **Dashboard Angular** :  En cours de démarrage

## 🔧 Corrections appliquées

### 1. API Flask (`PriceScan-api/helpers/auth.py`)
-  Correction du champ `username` dans `login()` et `register()`
-  Suppression des champs obsolètes (`u_name`, `u_mobile`, etc.)
-  Ajout du champ `u_account_type`

### 2. Modèle de base de données (`PriceScan-api/model/PriceScan_db.py`)
-  Synchronisation avec la structure MySQL
-  Suppression des colonnes inexistantes
-  Ajout des nouvelles colonnes (`u_account_type`, `u_business_name`, etc.)

### 3. Service Angular (`PriceScan-dashboard/src/app/dashboard/services/auth/auth.ts`)
-  Correction de l'envoi du champ `username` lors de la connexion
-  Envoi de `username: credentials.email` à l'API

### 4. Composant Angular (`PriceScan-dashboard/src/app/auth/auth.ts`)
-  Génération d'un `username` unique basé sur l'email
-  Format : `email.split('@')[0] + '_' + timestamp`

## 🧪 Tests à effectuer

### Étape 1 : Vérifier que l'API fonctionne
```bash
cd PriceScan-api
python test_complete_flow.py
```
**Résultat attendu** : Tous les tests  réussis

### Étape 2 : Vérifier la simulation du dashboard
```bash
cd PriceScan-api
python test_dashboard_simulation.py
```
**Résultat attendu** : Simulation réussie avec redirection

### Étape 3 : Tester le dashboard Angular

#### 3.1 Inscription d'un nouvel utilisateur
1. Ouvrir http://localhost:4200 dans le navigateur
2. Cliquer sur "Créer un compte"
3. Remplir le formulaire :
   - **Prénom** : Test
   - **Nom** : User
   - **Email** : test@example.com
   - **Mot de passe** : test123
   - **Type de compte** : Particulier
4. Cliquer sur "Créer un compte"

**Résultat attendu** :
-  Message de succès
-  Redirection automatique vers le dashboard
-  Utilisateur créé dans la base MySQL

#### 3.2 Connexion avec l'utilisateur créé
1. Se déconnecter du dashboard
2. Retourner à la page de connexion
3. Se connecter avec :
   - **Email/Username** : test@example.com
   - **Mot de passe** : test123
4. Cliquer sur "Se connecter"

**Résultat attendu** :
-  Connexion réussie
-  Redirection vers le dashboard
-  Affichage des informations utilisateur

#### 3.3 Vérification en base de données
```bash
cd PriceScan-api
python check_users_table.py
```
**Résultat attendu** : Nouvel utilisateur visible dans la table `ps_users`

## 🚨 Problèmes potentiels et solutions

### Problème 1 : "Erreur de connexion" persistante
**Cause possible** : Mismatch entre les champs envoyés par Angular et attendus par l'API
**Solution** : Vérifier que `auth.ts` envoie bien `username` et non `email`

### Problème 2 : Aucun utilisateur créé lors de l'inscription
**Cause possible** : Erreur CORS ou problème de proxy
**Solution** : Vérifier `proxy.conf.json` et les headers CORS de l'API

### Problème 3 : Dashboard ne se charge pas
**Cause possible** : Erreur de compilation TypeScript
**Solution** : Vérifier la console du navigateur et les logs `ng serve`

##  Vérification finale

Après tous les tests réussis, vous devriez avoir :
-  Un utilisateur créé dans MySQL
-  Une connexion fonctionnelle
-  Un dashboard accessible
-  Une redirection automatique après inscription

##  Debugging avancé

### Vérifier les logs de l'API
```bash
cd PriceScan-api
python app.py
```

### Vérifier les logs du dashboard
```bash
cd PriceScan-dashboard/PriceScan-dashboard/TicketScan-dashboard
npm start
```

### Vérifier la base de données
```bash
cd PriceScan-api
python check_users_table.py
```

## 📝 Notes importantes

- L'API accepte soit `username` soit `email` pour la connexion
- Le dashboard génère automatiquement un `username` unique
- Tous les utilisateurs sont créés avec le statut `ACTIVE`
- La base de données utilise MySQL/MariaDB via XAMPP

---

**🎯 Objectif** : Avoir un système d'authentification complet et fonctionnel où chaque utilisateur créé via le dashboard est enregistré en base et peut se connecter immédiatement.
