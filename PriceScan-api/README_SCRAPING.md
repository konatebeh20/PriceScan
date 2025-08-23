# 🤖 Scraping Automatique PriceScan

Ce document explique le fonctionnement du système de scraping automatique intégré dans l'API PriceScan.

## 🚀 Fonctionnalités

- **Scraping automatique** au démarrage de l'API
- **Intervalles configurables** : 5 jours en production, 1-2 heures en développement
- **Support de 5 magasins** : Carrefour, Abidjan Mall, Prosuma, Playce, Jumia
- **Sauvegarde automatique** en base de données PostgreSQL
- **Gestion des erreurs** et retry automatique
- **Logs détaillés** pour le monitoring

## 🏪 Magasins Supportés

| Magasin | URL | Intervalle Production | Intervalle Dev |
|---------|-----|----------------------|----------------|
| Carrefour | carrefour.ci | 5 jours | 1 heure |
| Abidjan Mall | abidjanmall.org | 5 jours | 1 heure |
| Prosuma | groupeprosuma.com | 5 jours | 2 heures |
| Playce | playce.ci | 5 jours | 2 heures |
| Jumia | jumia.ci | 5 jours | 1 heure |

## ⚙️ Configuration

### Variables d'Environnement

```bash
# Mode d'environnement
ENVIRONMENT=production  # ou development

# Activation du scraping
SCRAPING_ENABLED=true

# Intervalles (en secondes)
SCRAPING_CARREFOUR_INTERVAL=432000      # 5 jours
SCRAPING_ABIDJANMALL_INTERVAL=432000    # 5 jours
SCRAPING_PROSUMA_INTERVAL=432000        # 5 jours
SCRAPING_PLACE_INTERVAL=432000          # 5 jours
SCRAPING_JUMIA_INTERVAL=432000          # 5 jours
```

### Fichiers de Configuration

- `config/scraping_config.py` - Configuration principale
- `config/production.env` - Variables d'environnement production

## 🚀 Lancement

### Mode Développement

```bash
# Lancer l'API avec scraping automatique (1-2 heures)
python app.py
```

### Mode Production

```bash
# Lancer l'API avec scraping automatique (5 jours)
python run_production.py

# Ou avec variables d'environnement
ENVIRONMENT=production python app.py
```

## 🧪 Tests

### Test Simple

```bash
# Test rapide du scraping
python test_simple_scraping.py
```

### Test Complet

```bash
# Test complet avec base de données
python test_auto_scraping.py
```

## 📊 Monitoring

### Logs

Les logs sont sauvegardés dans :
- `logger/auto_scraper.log` - Logs du scraping automatique
- `logger/app.log` - Logs de l'application

### Statut en Temps Réel

L'API expose des endpoints pour vérifier le statut :

```bash
# Vérifier le statut du scraping
curl http://localhost:5000/api/scraping/status

# Vérifier l'historique
curl http://localhost:5000/api/scraping/history
```

## 🔧 Dépannage

### Problèmes Courants

1. **Scraping ne démarre pas**
   - Vérifier `SCRAPING_ENABLED=true`
   - Vérifier les logs dans `logger/auto_scraper.log`

2. **Erreurs de connexion**
   - Vérifier la connectivité internet
   - Vérifier les timeouts dans la configuration

3. **Base de données inaccessible**
   - Vérifier la connexion PostgreSQL
   - Vérifier les permissions utilisateur

### Logs de Debug

Pour activer les logs de debug :

```bash
SCRAPING_DEBUG=true python app.py
```

## 📈 Performance

### Optimisations

- **Scraping parallèle** : 4 workers simultanés
- **Cache des données** : Évite les requêtes répétées
- **Gestion des erreurs** : Continue en cas d'échec partiel
- **Évitement des heures de pointe** : 9h-18h

### Métriques

- **Taux de succès** : Objectif > 80%
- **Temps de réponse** : < 30 secondes par magasin
- **Utilisation mémoire** : < 500MB
- **Utilisation CPU** : < 30% en moyenne

## 🔒 Sécurité

### Bonnes Pratiques

- **User-Agent rotation** pour éviter la détection
- **Délais aléatoires** entre requêtes
- **Limitation du nombre de requêtes** par session
- **Respect des robots.txt** des sites cibles

### Configuration Sécurisée

```python
# Headers HTTP sécurisés
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9...',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3'
}
```

## 📝 Contribution

### Ajouter un Nouveau Magasin

1. Créer le module de scraping dans `helpers/scrapper/`
2. Ajouter la configuration dans `config/scraping_config.py`
3. Intégrer dans `helpers/auto_scraper.py`
4. Tester avec `test_simple_scraping.py`

### Structure d'un Module de Scraping

```python
def scrape_magasin(query):
    """
    Scrape un magasin pour une requête donnée
    
    Args:
        query (str): Terme de recherche
        
    Returns:
        list: Liste des produits trouvés
    """
    # Implémentation du scraping
    pass
```

## 📞 Support

Pour toute question ou problème :

1. Vérifier les logs dans `logger/auto_scraper.log`
2. Exécuter `test_simple_scraping.py` pour diagnostiquer
3. Vérifier la configuration dans `config/scraping_config.py`
4. Consulter la documentation des modules de scraping

---

**Note** : Ce système est conçu pour fonctionner de manière autonome. Une fois configuré, il s'exécute automatiquement selon les intervalles définis.
