#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🏭 Script de Production PriceScan avec Gunicorn
Serveur de production optimisé et robuste
"""

import os
import sys
import signal
import subprocess
import time
import psutil
from pathlib import Path

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ProductionServer:
    """Serveur de production avec Gunicorn"""
    
    def __init__(self):
        self.gunicorn_process = None
        self.is_running = False
        
        # Configuration de l'environnement
        self.environment = os.getenv('FLASK_ENV', 'production')
        self.host = os.getenv('GUNICORN_BIND', '0.0.0.0')
        self.port = int(os.getenv('GUNICORN_PORT', 8000))
        self.workers = int(os.getenv('GUNICORN_WORKERS', 0))  # 0 = auto-détection
        
        # Configuration des logs
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        
        # Fichiers de log
        self.access_log = self.log_dir / 'gunicorn_access.log'
        self.error_log = self.log_dir / 'gunicorn_error.log'
        self.pid_file = self.log_dir / 'gunicorn.pid'
        
        print("🏭 Serveur de production PriceScan initialisé")
        print(f"🌍 Environnement: {self.environment}")
        print(f"📍 Host: {self.host}")
        print(f"🔌 Port: {self.port}")
        print(f"📊 Workers: {self.workers if self.workers > 0 else 'Auto-détection'}")
        print(f"📁 Logs: {self.log_dir}")
    
    def start(self):
        """Démarre le serveur de production"""
        try:
            self.is_running = True
            
            # Vérifier les prérequis
            self._check_prerequisites()
            
            # Démarrer Gunicorn
            self._start_gunicorn()
            
            # Boucle principale de monitoring
            self._monitor_loop()
            
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur fatale: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()
    
    def stop(self):
        """Arrête le serveur de production"""
        self.is_running = False
        
        if self.gunicorn_process:
            try:
                print("🔄 Arrêt gracieux de Gunicorn...")
                
                # Envoyer SIGTERM pour un arrêt gracieux
                self.gunicorn_process.terminate()
                
                # Attendre l'arrêt
                try:
                    self.gunicorn_process.wait(timeout=30)
                    print("✅ Gunicorn arrêté gracieusement")
                except subprocess.TimeoutExpired:
                    print("⚠️ Arrêt forcé de Gunicorn...")
                    self.gunicorn_process.kill()
                    self.gunicorn_process.wait()
                    print("✅ Gunicorn arrêté de force")
                
            except Exception as e:
                print(f"⚠️ Erreur lors de l'arrêt: {e}")
        
        # Nettoyer le fichier PID
        if self.pid_file.exists():
            try:
                self.pid_file.unlink()
                print("✅ Fichier PID supprimé")
            except Exception as e:
                print(f"⚠️ Erreur suppression PID: {e}")
        
        print("🛑 Serveur de production arrêté")
    
    def restart(self):
        """Redémarre le serveur de production"""
        print("🔄 Redémarrage du serveur de production...")
        self.stop()
        time.sleep(2)
        self.start()
    
    def reload(self):
        """Recharge l'application sans redémarrer le serveur"""
        if self.gunicorn_process and self.gunicorn_process.poll() is None:
            try:
                print("🔄 Rechargement de l'application...")
                self.gunicorn_process.send_signal(signal.SIGHUP)
                print("✅ Application rechargée")
            except Exception as e:
                print(f"❌ Erreur lors du rechargement: {e}")
        else:
            print("⚠️ Serveur non disponible pour le rechargement")
    
    def _check_prerequisites(self):
        """Vérifie les prérequis du serveur de production"""
        print("🔍 Vérification des prérequis...")
        
        # Vérifier que l'application peut être créée
        try:
            from launch_api import create_app
            app = create_app()
            if not app:
                raise Exception("Impossible de créer l'application Flask")
            print("✅ Application Flask vérifiée")
        except Exception as e:
            raise Exception(f"Erreur création application: {e}")
        
        # Vérifier Gunicorn
        try:
            import gunicorn
            print(f"✅ Gunicorn {gunicorn.__version__} disponible")
        except ImportError:
            raise Exception("Gunicorn non installé. Installez-le avec: pip install gunicorn")
        
        # Vérifier les dossiers de logs
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
            print("✅ Dossier de logs créé")
        
        print("✅ Tous les prérequis sont satisfaits")
    
    def _start_gunicorn(self):
        """Démarre Gunicorn"""
        try:
            # Configuration Gunicorn
            config_file = 'config/gunicorn_config.py'
            
            # Vérifier si le fichier de configuration existe
            if not Path(config_file).exists():
                print(f"⚠️ Fichier de configuration {config_file} non trouvé, utilisation des paramètres par défaut")
                config_file = None
            
            # Commande Gunicorn
            cmd = [
                sys.executable, '-m', 'gunicorn',
                '--bind', f'{self.host}:{self.port}',
                '--workers', str(self.workers) if self.workers > 0 else str(self._get_optimal_workers()),
                '--worker-class', 'sync',
                '--timeout', '120',
                '--keep-alive', '2',
                '--max-requests', '1000',
                '--max-requests-jitter', '100',
                '--preload',
                '--access-logfile', str(self.access_log),
                '--error-logfile', str(self.error_log),
                '--pid', str(self.pid_file),
                '--log-level', 'info',
                '--access-logformat', '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s',
                '--capture-output',
                '--enable-stdio-inheritance',
                'wsgi:app'
            ]
            
            # Ajouter le fichier de configuration si disponible
            if config_file:
                cmd.extend(['--config', config_file])
            
            # Variables d'environnement
            env = os.environ.copy()
            env['FLASK_ENV'] = 'production'
            env['FLASK_DEBUG'] = '0'
            env['PROD_MODE'] = 'true'
            
            print("🚀 Démarrage de Gunicorn...")
            print(f"📝 Commande: {' '.join(cmd)}")
            
            # Lancer Gunicorn
            self.gunicorn_process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            print(f"✅ Gunicorn démarré (PID: {self.gunicorn_process.pid})")
            
            # Attendre un peu pour vérifier le démarrage
            time.sleep(3)
            
            if self.gunicorn_process.poll() is not None:
                # Lire les erreurs si le processus s'est arrêté
                stdout, stderr = self.gunicorn_process.communicate()
                if stderr:
                    print(f"❌ Erreur Gunicorn: {stderr}")
                raise Exception("Gunicorn s'est arrêté immédiatement")
            
            # Démarrer la lecture des logs en arrière-plan
            self._start_log_reader()
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage de Gunicorn: {e}")
            raise
    
    def _get_optimal_workers(self):
        """Calcule le nombre optimal de workers"""
        try:
            cpu_count = psutil.cpu_count(logical=False) or 1
            optimal_workers = cpu_count * 2 + 1
            print(f"💻 CPU cores: {cpu_count}, Workers optimaux: {optimal_workers}")
            return optimal_workers
        except Exception:
            # Fallback si psutil n'est pas disponible
            return 4
    
    def _start_log_reader(self):
        """Démarre la lecture des logs en arrière-plan"""
        def read_logs():
            try:
                while self.gunicorn_process and self.gunicorn_process.poll() is None:
                    # Lire stdout
                    if self.gunicorn_process.stdout:
                        line = self.gunicorn_process.stdout.readline()
                        if line:
                            print(f"📝 Gunicorn: {line.strip()}")
                    
                    # Lire stderr
                    if self.gunicorn_process.stderr:
                        line = self.gunicorn_process.stderr.readline()
                        if line:
                            print(f"⚠️ Gunicorn: {line.strip()}")
                    
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"❌ Erreur lecture logs: {e}")
        
        # Démarrer le thread de lecture des logs
        import threading
        log_thread = threading.Thread(target=read_logs, daemon=True)
        log_thread.start()
    
    def _monitor_loop(self):
        """Boucle principale de monitoring"""
        try:
            print("📊 Monitoring du serveur de production...")
            print("💡 Utilisez Ctrl+C pour arrêter le serveur")
            
            while self.is_running:
                # Vérifier l'état du processus Gunicorn
                if self.gunicorn_process and self.gunicorn_process.poll() is not None:
                    print("⚠️ Gunicorn s'est arrêté de manière inattendue")
                    break
                
                # Afficher les statistiques périodiquement
                self._display_stats()
                
                # Attendre
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé")
    
    def _display_stats(self):
        """Affiche les statistiques du serveur"""
        try:
            if self.gunicorn_process and self.gunicorn_process.poll() is None:
                # Statistiques du processus
                process = psutil.Process(self.gunicorn_process.pid)
                memory_info = process.memory_info()
                cpu_percent = process.cpu_percent()
                
                print(f"📊 Stats - PID: {self.gunicorn_process.pid}, "
                      f"CPU: {cpu_percent:.1f}%, "
                      f"Mémoire: {memory_info.rss / 1024 / 1024:.1f} MB")
                
        except Exception as e:
            print(f"⚠️ Erreur affichage stats: {e}")

def signal_handler(signum, frame):
    """Gestionnaire des signaux système"""
    print(f"\n📡 Signal reçu: {signum}")
    if prod_server:
        prod_server.stop()
    sys.exit(0)

def main():
    """Fonction principale"""
    global prod_server
    
    print("🏭 DÉMARRAGE DU SERVEUR DE PRODUCTION PRICESCAN")
    print("=" * 60)
    
    try:
        # Créer le serveur de production
        prod_server = ProductionServer()
        
        # Configurer les gestionnaires de signaux
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Démarrer le serveur
        prod_server.start()
        
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    prod_server = None
    main()
