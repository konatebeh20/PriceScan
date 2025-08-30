# 🏭 PRICESCAN API - GUIDE DE PRODUCTION

##  **VUE D'ENSEMBLE**

Ce guide détaille le déploiement et la gestion de l'API PriceScan en production avec Gunicorn, Docker et des outils de monitoring avancés.

##  **ARCHITECTURE DE PRODUCTION**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx (80/443)│    │   Load Balancer │    │   CDN/Cloud     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Gunicorn API   │    │   Redis Cache   │    │  MySQL Database │
│   (Port 8000)   │    │   (Port 6379)   │    │   (Port 3306)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Prometheus     │    │     Grafana     │    │   ELK Stack     │
│   (Port 9090)   │    │   (Port 3000)   │    │  (Ports 9200+) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 **PRÉREQUIS**

### **Système**
- **OS** : Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **RAM** : Minimum 4GB, Recommandé 8GB+
- **CPU** : Minimum 2 cores, Recommandé 4+ cores
- **Stockage** : Minimum 20GB, Recommandé 50GB+

### **Logiciels**
- **Docker** : 20.10+
- **Docker Compose** : 2.0+
- **Python** : 3.8+
- **Git** : 2.25+

## 📦 **INSTALLATION RAPIDE**

### **1. Cloner le projet**
```bash
git clone https://github.com/your-org/pricescan-api.git
cd pricescan-api
```

### **2. Configuration automatique**
```bash
# Configuration de l'environnement de production
python manage_prod.py setup

# Démarrage de tous les services
python manage_prod.py start
```

### **3. Vérification**
```bash
# Statut des services
python manage_prod.py status

# Logs en temps réel
python manage_prod.py monitor
```

## ⚙️ **CONFIGURATION MANUELLE**

### **1. Variables d'environnement**
Créer le fichier `.env.prod` :

```env
# ========================================
# CONFIGURATION PRODUCTION PRICESCAN
# ========================================

# Environnement
FLASK_ENV=production
FLASK_DEBUG=0

# Base de données
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=pricescan_user
DB_PASSWORD=VOTRE_MOT_DE_PASSE_SECURISE
DB_NAME=pricescan_prod

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=VOTRE_MOT_DE_PASSE_REDIS
REDIS_DB=0

# Sécurité
SECRET_KEY=VOTRE_CLE_SECRETE_TRES_LONGUE_ET_ALEATOIRE
JWT_SECRET_KEY=VOTRE_CLE_JWT_TRES_LONGUE_ET_ALEATOIRE

# Gunicorn
GUNICORN_BIND=0.0.0.0:8000
GUNICORN_PORT=8000
GUNICORN_WORKERS=4
GUNICORN_LOG_LEVEL=info

# Scraping
SCRAPING_ENABLED=true
SCRAPING_DEBUG=false

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true

# Logs
LOG_LEVEL=WARNING
LOG_FILE=logs/production.log

# Notifications
NOTIFICATIONS_ENABLED=true
EMAIL_ENABLED=true
SMS_ENABLED=false
PUSH_ENABLED=false
```

### **2. Configuration de la base de données**
```bash
# Créer la base de données
mysql -u root -p
CREATE DATABASE pricescan_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Créer l'utilisateur
CREATE USER 'pricescan_user'@'%' IDENTIFIED BY 'VOTRE_MOT_DE_PASSE';
GRANT ALL PRIVILEGES ON pricescan_prod.* TO 'pricescan_user'@'%';
FLUSH PRIVILEGES;
```

### **3. Configuration Redis**
```bash
# Installer Redis
sudo apt update
sudo apt install redis-server

# Configurer l'authentification
sudo nano /etc/redis/redis.conf
# Ajouter : requirepass VOTRE_MOT_DE_PASSE_REDIS

# Redémarrer Redis
sudo systemctl restart redis
```

## 🐳 **DÉPLOIEMENT AVEC DOCKER**

### **1. Construction des images**
```bash
# Construire l'image de production
docker build -f Dockerfile.prod -t pricescan-api:prod .

# Vérifier l'image
docker images | grep pricescan-api
```

### **2. Démarrage des services**
```bash
# Démarrer tous les services
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# Vérifier le statut
docker-compose -f docker-compose.prod.yml ps
```

### **3. Vérification de la santé**
```bash
# Test de l'API
curl -f http://localhost:8000/health

# Test de la base de données
docker-compose -f docker-compose.prod.yml exec pricescan-mysql mysqladmin ping

# Test de Redis
docker-compose -f docker-compose.prod.yml exec pricescan-redis redis-cli ping
```

##  **GESTION DES SERVICES**

### **Commandes principales**
```bash
# Démarrage
python manage_prod.py start

# Arrêt
python manage_prod.py stop

# Redémarrage
python manage_prod.py restart

# Statut
python manage_prod.py status

# Logs
python manage_prod.py logs

# Monitoring en temps réel
python manage_prod.py monitor
```

### **Gestion par service**
```bash
# Démarrer un service spécifique
python manage_prod.py start --service pricescan-api

# Arrêter un service spécifique
python manage_prod.py stop --service pricescan-mysql

# Logs d'un service spécifique
python manage_prod.py logs --service pricescan-api --follow
```

##  **MONITORING ET OBSERVABILITÉ**

### **1. Prometheus (Métriques)**
- **URL** : http://localhost:9090
- **Métriques collectées** :
  - Requêtes HTTP (nombre, durée, codes de statut)
  - Utilisation des ressources (CPU, mémoire, disque)
  - Performance de la base de données
  - Métriques du scraping

### **2. Grafana (Visualisation)**
- **URL** : http://localhost:3000
- **Login** : admin / VOTRE_MOT_DE_PASSE_GRAFANA
- **Dashboards disponibles** :
  - Vue d'ensemble de l'API
  - Performance de la base de données
  - Métriques du scraping
  - Alertes système

### **3. ELK Stack (Logs)**
- **Elasticsearch** : http://localhost:9200
- **Kibana** : http://localhost:5601
- **Logstash** : Port 5044

## 🔒 **SÉCURITÉ**

### **1. Firewall**
```bash
# Configuration UFW
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # API (si exposée directement)
sudo ufw allow 3306/tcp  # MySQL (si exposée)
sudo ufw allow 6379/tcp  # Redis (si exposée)
```

### **2. SSL/TLS**
```bash
# Installation Certbot
sudo apt install certbot python3-certbot-nginx

# Génération du certificat
sudo certbot --nginx -d api.pricescan.com

# Renouvellement automatique
sudo crontab -e
# Ajouter : 0 12 * * * /usr/bin/certbot renew --quiet
```

### **3. Sécurité de la base de données**
```bash
# Restriction d'accès MySQL
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# bind-address = 127.0.0.1

# Redémarrer MySQL
sudo systemctl restart mysql
```

## 📈 **PERFORMANCE ET OPTIMISATION**

### **1. Configuration Gunicorn**
```python
# config/gunicorn_config.py
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
max_requests = 1000
max_requests_jitter = 100
timeout = 120
keepalive = 2
```

### **2. Optimisation de la base de données**
```sql
-- Index pour les requêtes fréquentes
CREATE INDEX idx_product_name ON ps_products(product_name);
CREATE INDEX idx_price_store ON ps_prices(store_name);
CREATE INDEX idx_user_email ON ps_users(u_email);

-- Configuration MySQL
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
query_cache_size = 128M
```

### **3. Cache Redis**
```python
# Configuration du cache
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6379/0'
CACHE_DEFAULT_TIMEOUT = 300
CACHE_KEY_PREFIX = 'pricescan:'
```

## 🚨 **ALERTES ET NOTIFICATIONS**

### **1. Configuration des alertes**
```yaml
# docker/prometheus/alerts.yml
groups:
  - name: pricescan_alerts
    rules:
      - alert: APIHighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Taux d'erreur élevé sur l'API"
```

### **2. Notifications**
- **Email** : Via SMTP configuré
- **Slack** : Webhook configuré
- **Telegram** : Bot configuré
- **SMS** : Via service tiers

## 💾 **SAUVEGARDE ET RÉCUPÉRATION**

### **1. Sauvegarde automatique**
```bash
# Créer une sauvegarde
python manage_prod.py backup

# Sauvegarde manuelle de la base
docker-compose -f docker-compose.prod.yml exec pricescan-mysql \
  mysqldump -u root -p${MYSQL_ROOT_PASSWORD} pricescan_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

### **2. Récupération**
```bash
# Restaurer la base de données
docker-compose -f docker-compose.prod.yml exec -T pricescan-mysql \
  mysql -u root -p${MYSQL_ROOT_PASSWORD} pricescan_prod < backup_file.sql
```

### **3. Plan de reprise d'activité**
1. **Détection** : Monitoring automatique
2. **Notification** : Alertes immédiates
3. **Diagnostic** : Analyse des logs
4. **Récupération** : Restauration automatique
5. **Vérification** : Tests de santé
6. **Documentation** : Rapport d'incident

##  **DÉPLOIEMENT CONTINU**

### **1. Pipeline CI/CD**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          ssh user@server "cd /opt/pricescan && git pull && python manage_prod.py deploy"
```

### **2. Déploiement manuel**
```bash
# Mise à jour et redéploiement
python manage_prod.py deploy

# Vérification post-déploiement
python manage_prod.py status
curl -f http://localhost:8000/health
```

## 📚 **MAINTENANCE**

### **1. Mises à jour**
```bash
# Mise à jour du code
git pull origin main

# Mise à jour des dépendances
pip install -r requirements-prod.txt

# Redémarrage des services
python manage_prod.py restart
```

### **2. Nettoyage**
```bash
# Nettoyage des logs anciens
find logs/ -name "*.log" -mtime +30 -delete

# Nettoyage des images Docker
docker image prune -f

# Nettoyage des volumes
docker volume prune -f
```

### **3. Surveillance**
```bash
# Vérification de l'espace disque
df -h

# Vérification de la mémoire
free -h

# Vérification des processus
htop
```

## 🆘 **DÉPANNAGE**

### **1. Problèmes courants**

#### **API non accessible**
```bash
# Vérifier le statut des services
python manage_prod.py status

# Vérifier les logs
python manage_prod.py logs --service pricescan-api

# Vérifier la connectivité
curl -v http://localhost:8000/health
```

#### **Base de données inaccessible**
```bash
# Vérifier le statut MySQL
docker-compose -f docker-compose.prod.yml exec pricescan-mysql mysqladmin ping

# Vérifier les logs MySQL
docker-compose -f docker-compose.prod.yml logs pricescan-mysql

# Vérifier la configuration
docker-compose -f docker-compose.prod.yml exec pricescan-mysql mysql -u root -p -e "SHOW VARIABLES LIKE 'bind_address';"
```

#### **Problèmes de performance**
```bash
# Vérifier les métriques Prometheus
curl http://localhost:9090/api/v1/query?query=up

# Vérifier l'utilisation des ressources
docker stats

# Analyser les logs de performance
python manage_prod.py logs --service pricescan-api | grep "slow"
```

### **2. Logs et diagnostics**
```bash
# Logs complets
python manage_prod.py logs --follow

# Logs d'erreur uniquement
docker-compose -f docker-compose.prod.yml logs --tail=100 | grep ERROR

# Métriques système
docker-compose -f docker-compose.prod.yml exec pricescan-api top
```

## 📞 **SUPPORT ET CONTACT**

### **1. Documentation**
- **API** : http://localhost:8000/docs
- **Grafana** : http://localhost:3000
- **Prometheus** : http://localhost:9090
- **Kibana** : http://localhost:5601

### **2. Contacts**
- **Développement** : dev@pricescan.com
- **Production** : ops@pricescan.com
- **Support** : support@pricescan.com

### **3. Escalade**
1. **Niveau 1** : Développeurs (2h)
2. **Niveau 2** : DevOps (4h)
3. **Niveau 3** : Architecte (8h)

## 📝 **CHANGELOG**

### **Version 1.0.0** (Décembre 2024)
-  Configuration de production complète
-  Intégration Gunicorn
-  Monitoring Prometheus/Grafana
-  Logs centralisés ELK
-  Déploiement Docker automatisé
-  Gestionnaire de production unifié

---

## 🎯 **PROCHAINES ÉTAPES**

- [ ] Intégration Kubernetes
- [ ] Auto-scaling basé sur les métriques
- [ ] Backup automatique vers le cloud
- [ ] Tests de charge automatisés
- [ ] Documentation API interactive
- [ ] Intégration Slack/Teams pour les alertes

---

**🏭 PriceScan API - Prêt pour la production !**
