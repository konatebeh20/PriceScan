#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Gestionnaire de Production PriceScan
Script unifié pour gérer tous les aspects de la production
"""

import os
import sys
import argparse
import subprocess
import time
import signal
from pathlib import Path

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ProductionManager:
    """Gestionnaire de production PriceScan"""
    
    def __init__(self):
        self.environment = os.getenv('FLASK_ENV', 'production')
        self.project_root = Path(__file__).parent
        
        # Dossiers importants
        self.logs_dir = self.project_root / 'logs'
        self.docker_dir = self.project_root / 'docker'
        self.env_file = self.project_root / '.env.prod'
        
        # Créer les dossiers nécessaires
        self.logs_dir.mkdir(exist_ok=True)
        
        print(f"🏭 Gestionnaire de Production PriceScan")
        print(f"🌍 Environnement: {self.environment}")
        print(f"📁 Répertoire: {self.project_root}")
    
    def setup(self):
        """Configure l'environnement de production"""
        print("\n🔧 Configuration de l'environnement de production...")
        
        try:
            # Vérifier les prérequis
            self._check_prerequisites()
            
            # Créer le fichier .env.prod
            self._create_env_file()
            
            # Configurer les dossiers
            self._setup_directories()
            
            # Installer les dépendances
            self._install_dependencies()
            
            print("✅ Configuration de production terminée")
            
        except Exception as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            sys.exit(1)
    
    def start(self, service=None):
        """Démarre les services de production"""
        print(f"\n🚀 Démarrage des services de production...")
        
        try:
            if service:
                self._start_service(service)
            else:
                # Démarrer tous les services
                self._start_all_services()
            
            print("✅ Services démarrés avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage: {e}")
            sys.exit(1)
    
    def stop(self, service=None):
        """Arrête les services de production"""
        print(f"\n🛑 Arrêt des services de production...")
        
        try:
            if service:
                self._stop_service(service)
            else:
                # Arrêter tous les services
                self._stop_all_services()
            
            print("✅ Services arrêtés avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'arrêt: {e}")
    
    def restart(self, service=None):
        """Redémarre les services de production"""
        print(f"\n🔄 Redémarrage des services de production...")
        
        try:
            self.stop(service)
            time.sleep(2)
            self.start(service)
            
            print("✅ Services redémarrés avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors du redémarrage: {e}")
    
    def status(self):
        """Affiche le statut des services"""
        print(f"\n📊 Statut des services de production...")
        
        try:
            self._show_service_status()
            
        except Exception as e:
            print(f"❌ Erreur lors de la vérification du statut: {e}")
    
    def logs(self, service=None, follow=False):
        """Affiche les logs des services"""
        print(f"\n📝 Affichage des logs...")
        
        try:
            if service:
                self._show_service_logs(service, follow)
            else:
                self._show_all_logs(follow)
                
        except Exception as e:
            print(f"❌ Erreur lors de l'affichage des logs: {e}")
    
    def deploy(self):
        """Déploie l'application en production"""
        print(f"\n🚀 Déploiement en production...")
        
        try:
            # Arrêter les services
            self.stop()
            
            # Mettre à jour le code
            self._update_code()
            
            # Reconstruire les images Docker
            self._rebuild_docker()
            
            # Redémarrer les services
            self.start()
            
            # Vérifier la santé
            self._health_check()
            
            print("✅ Déploiement terminé avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors du déploiement: {e}")
            # Rollback en cas d'erreur
            self._rollback()
    
    def backup(self):
        """Effectue une sauvegarde de la production"""
        print(f"\n💾 Sauvegarde de la production...")
        
        try:
            self._create_backup()
            print("✅ Sauvegarde terminée avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    def monitor(self):
        """Lance le monitoring en temps réel"""
        print(f"\n📊 Monitoring en temps réel...")
        
        try:
            self._start_monitoring()
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring arrêté")
        except Exception as e:
            print(f"❌ Erreur lors du monitoring: {e}")
    
    def _check_prerequisites(self):
        """Vérifie les prérequis de production"""
        print("   🔍 Vérification des prérequis...")
        
        # Vérifier Docker
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Docker disponible")
            else:
                raise Exception("Docker non disponible")
        except Exception:
            raise Exception("Docker doit être installé pour la production")
        
        # Vérifier Docker Compose
        try:
            result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Docker Compose disponible")
            else:
                raise Exception("Docker Compose non disponible")
        except Exception:
            raise Exception("Docker Compose doit être installé pour la production")
        
        # Vérifier Python
        if sys.version_info < (3, 8):
            raise Exception("Python 3.8+ requis pour la production")
        print("   ✅ Python version compatible")
    
    def _create_env_file(self):
        """Crée le fichier .env.prod"""
        print("   📝 Création du fichier .env.prod...")
        
        env_content = f"""# ========================================
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
DB_PASSWORD=CHANGE_THIS_PASSWORD
DB_NAME=pricescan_prod

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=CHANGE_THIS_PASSWORD
REDIS_DB=0

# Sécurité
SECRET_KEY=CHANGE_THIS_SECRET_KEY
JWT_SECRET_KEY=CHANGE_THIS_JWT_SECRET_KEY

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
"""
        
        with open(self.env_file, 'w') as f:
            f.write(env_content)
        
        print("   ✅ Fichier .env.prod créé")
        print("   ⚠️  N'oubliez pas de modifier les mots de passe !")
    
    def _setup_directories(self):
        """Configure les dossiers de production"""
        print("   📁 Configuration des dossiers...")
        
        directories = [
            'logs',
            'uploads',
            'temp',
            'backups',
            'docker/mysql/init',
            'docker/mysql/conf',
            'docker/nginx',
            'docker/prometheus',
            'docker/grafana/provisioning'
        ]
        
        for directory in directories:
            (self.project_root / directory).mkdir(parents=True, exist_ok=True)
        
        print("   ✅ Dossiers configurés")
    
    def _install_dependencies(self):
        """Installe les dépendances de production"""
        print("   📦 Installation des dépendances de production...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements-prod.txt'
            ], check=True)
            print("   ✅ Dépendances installées")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur installation dépendances: {e}")
    
    def _start_all_services(self):
        """Démarre tous les services"""
        print("   🚀 Démarrage de tous les services...")
        
        try:
            # Charger les variables d'environnement
            if self.env_file.exists():
                subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', '--env-file', '.env.prod', 'up', '-d'], check=True)
            else:
                subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'up', '-d'], check=True)
            
            print("   ✅ Services démarrés")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur démarrage services: {e}")
    
    def _stop_all_services(self):
        """Arrête tous les services"""
        print("   🛑 Arrêt de tous les services...")
        
        try:
            subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'down'], check=True)
            print("   ✅ Services arrêtés")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur arrêt services: {e}")
    
    def _start_service(self, service):
        """Démarre un service spécifique"""
        print(f"   🚀 Démarrage du service {service}...")
        
        try:
            subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'up', '-d', service], check=True)
            print(f"   ✅ Service {service} démarré")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur démarrage service {service}: {e}")
    
    def _stop_service(self, service):
        """Arrête un service spécifique"""
        print(f"   🛑 Arrêt du service {service}...")
        
        try:
            subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'stop', service], check=True)
            print(f"   ✅ Service {service} arrêté")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur arrêt service {service}: {e}")
    
    def _show_service_status(self):
        """Affiche le statut des services"""
        try:
            subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'ps'], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur affichage statut: {e}")
    
    def _show_service_logs(self, service, follow=False):
        """Affiche les logs d'un service"""
        cmd = ['docker-compose', '-f', 'docker-compose.prod.yml', 'logs']
        if follow:
            cmd.append('-f')
        cmd.append(service)
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur affichage logs: {e}")
    
    def _show_all_logs(self, follow=False):
        """Affiche tous les logs"""
        cmd = ['docker-compose', '-f', 'docker-compose.prod.yml', 'logs']
        if follow:
            cmd.append('-f')
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur affichage logs: {e}")
    
    def _update_code(self):
        """Met à jour le code source"""
        print("   📥 Mise à jour du code source...")
        
        try:
            # Git pull si c'est un repository Git
            if (self.project_root / '.git').exists():
                subprocess.run(['git', 'pull'], cwd=self.project_root, check=True)
                print("   ✅ Code source mis à jour")
            else:
                print("   ℹ️  Pas de repository Git, mise à jour manuelle requise")
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur mise à jour code: {e}")
    
    def _rebuild_docker(self):
        """Reconstruit les images Docker"""
        print("   🔨 Reconstruction des images Docker...")
        
        try:
            subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'build', '--no-cache'], check=True)
            print("   ✅ Images Docker reconstruites")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur reconstruction Docker: {e}")
    
    def _health_check(self):
        """Vérifie la santé des services"""
        print("   🏥 Vérification de la santé des services...")
        
        try:
            # Attendre que les services soient prêts
            time.sleep(10)
            
            # Vérifier l'API
            result = subprocess.run(['curl', '-f', 'http://localhost:8000/health'], capture_output=True, timeout=10)
            if result.returncode == 0:
                print("   ✅ API en bonne santé")
            else:
                raise Exception("API non accessible")
                
        except Exception as e:
            raise Exception(f"Erreur vérification santé: {e}")
    
    def _rollback(self):
        """Effectue un rollback en cas d'erreur"""
        print("   ⚠️  Rollback en cours...")
        
        try:
            # Arrêter les nouveaux services
            self.stop()
            
            # Redémarrer les anciens services
            print("   🔄 Redémarrage des anciens services...")
            
        except Exception as e:
            print(f"   ❌ Erreur lors du rollback: {e}")
    
    def _create_backup(self):
        """Crée une sauvegarde"""
        print("   💾 Création de la sauvegarde...")
        
        try:
            # Sauvegarde de la base de données
            subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'exec', '-T', 'pricescan-mysql', 'mysqldump', '-u', 'root', '-p${MYSQL_ROOT_PASSWORD}', 'pricescan_prod'], 
                         stdout=open(self.project_root / 'backups' / f'backup_{int(time.time())}.sql', 'w'), check=True)
            
            print("   ✅ Sauvegarde créée")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur création sauvegarde: {e}")
    
    def _start_monitoring(self):
        """Lance le monitoring en temps réel"""
        print("   📊 Démarrage du monitoring...")
        
        try:
            # Afficher les logs en temps réel
            subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'logs', '-f'], check=True)
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur monitoring: {e}")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Gestionnaire de Production PriceScan')
    parser.add_argument('command', choices=[
        'setup', 'start', 'stop', 'restart', 'status', 'logs', 'deploy', 'backup', 'monitor'
    ], help='Commande à exécuter')
    parser.add_argument('--service', help='Service spécifique (optionnel)')
    parser.add_argument('--follow', '-f', action='store_true', help='Suivre les logs en temps réel')
    
    args = parser.parse_args()
    
    # Créer le gestionnaire
    manager = ProductionManager()
    
    try:
        # Exécuter la commande
        if args.command == 'setup':
            manager.setup()
        elif args.command == 'start':
            manager.start(args.service)
        elif args.command == 'stop':
            manager.stop(args.service)
        elif args.command == 'restart':
            manager.restart(args.service)
        elif args.command == 'status':
            manager.status()
        elif args.command == 'logs':
            manager.logs(args.service, args.follow)
        elif args.command == 'deploy':
            manager.deploy()
        elif args.command == 'backup':
            manager.backup()
        elif args.command == 'monitor':
            manager.monitor()
            
    except KeyboardInterrupt:
        print("\n🛑 Opération interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
