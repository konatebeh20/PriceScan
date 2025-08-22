#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 Script de Développement Optimisé PriceScan
Développement avec rechargement automatique, gestion des erreurs et monitoring
"""

import os
import sys
import time
import signal
import threading
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class DevServer:
    """Serveur de développement optimisé"""
    
    def __init__(self):
        self.process = None
        self.observer = None
        self.is_running = False
        self.restart_count = 0
        self.max_restarts = 10
        self.restart_delay = 2
        
        # Configuration
        self.host = os.getenv('DEV_HOST', '0.0.0.0')
        self.port = int(os.getenv('DEV_PORT', 5000))
        self.debug = os.getenv('DEV_DEBUG', 'true').lower() == 'true'
        self.reload = os.getenv('DEV_RELOAD', 'true').lower() == 'true'
        
        # Fichiers à surveiller
        self.watch_patterns = [
            '*.py',
            '*.html',
            '*.css',
            '*.js',
            '*.json',
            '*.yml',
            '*.yaml'
        ]
        
        # Dossiers à ignorer
        self.ignore_dirs = {
            'venv', '__pycache__', '.git', 'logs', 
            'migrations', 'node_modules', '.pytest_cache'
        }
        
        print("🚀 Serveur de développement PriceScan initialisé")
        print(f"📍 Host: {self.host}")
        print(f"🔌 Port: {self.port}")
        print(f"🐛 Debug: {self.debug}")
        print(f"🔄 Auto-reload: {self.reload}")
    
    def start(self):
        """Démarre le serveur de développement"""
        try:
            self.is_running = True
            
            # Démarrer le serveur Flask
            self._start_flask_server()
            
            # Démarrer la surveillance des fichiers si activée
            if self.reload:
                self._start_file_watcher()
            
            # Boucle principale
            self._main_loop()
            
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur fatale: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Arrête le serveur de développement"""
        self.is_running = False
        
        # Arrêter le serveur Flask
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("✅ Serveur Flask arrêté")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("⚠️ Serveur Flask forcé à s'arrêter")
        
        # Arrêter la surveillance des fichiers
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("✅ Surveillance des fichiers arrêtée")
        
        print("🛑 Serveur de développement arrêté")
    
    def _start_flask_server(self):
        """Démarre le serveur Flask"""
        try:
            # Vérifier que l'API peut être créée
            from launch_api import create_app
            app = create_app()
            
            if not app:
                raise Exception("Impossible de créer l'application Flask")
            
            print("✅ Application Flask créée avec succès")
            
            # Démarrer le serveur en arrière-plan
            self._run_flask_background()
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage de Flask: {e}")
            raise
    
    def _run_flask_background(self):
        """Lance Flask en arrière-plan"""
        try:
            # Créer le processus Flask
            cmd = [
                sys.executable, 'launch_api.py'
            ]
            
            # Variables d'environnement
            env = os.environ.copy()
            env['FLASK_ENV'] = 'development'
            env['FLASK_DEBUG'] = '1'
            env['DEV_MODE'] = 'true'
            
            # Lancer le processus
            self.process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            print(f"🚀 Serveur Flask démarré (PID: {self.process.pid})")
            
            # Démarrer la lecture des logs en arrière-plan
            self._start_log_reader()
            
        except Exception as e:
            print(f"❌ Erreur lors du lancement de Flask: {e}")
            raise
    
    def _start_log_reader(self):
        """Démarre la lecture des logs en arrière-plan"""
        def read_logs():
            try:
                while self.process and self.process.poll() is None:
                    # Lire stdout
                    if self.process.stdout:
                        line = self.process.stdout.readline()
                        if line:
                            print(f"📝 Flask: {line.strip()}")
                    
                    # Lire stderr
                    if self.process.stderr:
                        line = self.process.stderr.readline()
                        if line:
                            print(f"⚠️ Flask: {line.strip()}")
                    
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"❌ Erreur lecture logs: {e}")
        
        # Démarrer le thread de lecture des logs
        log_thread = threading.Thread(target=read_logs, daemon=True)
        log_thread.start()
    
    def _start_file_watcher(self):
        """Démarre la surveillance des fichiers"""
        try:
            self.observer = Observer()
            
            # Créer l'événement handler
            event_handler = FileChangeHandler(self)
            
            # Ajouter les dossiers à surveiller
            for pattern in self.watch_patterns:
                self.observer.schedule(
                    event_handler, 
                    '.', 
                    recursive=True,
                    pattern=pattern
                )
            
            # Démarrer l'observateur
            self.observer.start()
            print("👀 Surveillance des fichiers activée")
            
        except Exception as e:
            print(f"⚠️ Erreur surveillance des fichiers: {e}")
    
    def _main_loop(self):
        """Boucle principale du serveur"""
        try:
            while self.is_running:
                # Vérifier l'état du processus Flask
                if self.process and self.process.poll() is not None:
                    print("⚠️ Serveur Flask arrêté, redémarrage...")
                    self._restart_flask_server()
                
                # Attendre un peu
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé")
    
    def _restart_flask_server(self):
        """Redémarre le serveur Flask"""
        try:
            if self.restart_count >= self.max_restarts:
                print(f"❌ Nombre maximum de redémarrages atteint ({self.max_restarts})")
                self.stop()
                return
            
            self.restart_count += 1
            print(f"🔄 Redémarrage #{self.restart_count}...")
            
            # Attendre un peu avant de redémarrer
            time.sleep(self.restart_delay)
            
            # Redémarrer le serveur
            self._run_flask_background()
            
            print("✅ Serveur Flask redémarré")
            
        except Exception as e:
            print(f"❌ Erreur lors du redémarrage: {e}")
    
    def restart(self):
        """Redémarre le serveur manuellement"""
        print("🔄 Redémarrage manuel demandé...")
        self._restart_flask_server()

class FileChangeHandler(FileSystemEventHandler):
    """Gestionnaire des changements de fichiers"""
    
    def __init__(self, dev_server):
        self.dev_server = dev_server
        self.last_restart = 0
        self.restart_cooldown = 2  # Délai minimum entre redémarrages
    
    def on_modified(self, event):
        """Appelé quand un fichier est modifié"""
        if event.is_directory:
            return
        
        # Ignorer les fichiers temporaires
        if self._should_ignore_file(event.src_path):
            return
        
        # Vérifier le délai de redémarrage
        current_time = time.time()
        if current_time - self.last_restart < self.restart_cooldown:
            return
        
        print(f"📝 Fichier modifié: {event.src_path}")
        print("🔄 Redémarrage automatique...")
        
        # Redémarrer le serveur
        self.dev_server.restart()
        self.last_restart = current_time
    
    def _should_ignore_file(self, file_path):
        """Vérifie si un fichier doit être ignoré"""
        path = Path(file_path)
        
        # Ignorer les dossiers spécifiés
        for ignore_dir in self.dev_server.ignore_dirs:
            if ignore_dir in path.parts:
                return True
        
        # Ignorer les fichiers temporaires
        temp_extensions = {'.tmp', '.swp', '.swo', '~'}
        if path.suffix in temp_extensions:
            return True
        
        # Ignorer les fichiers de log
        if 'log' in path.name.lower():
            return True
        
        return False

def signal_handler(signum, frame):
    """Gestionnaire des signaux système"""
    print(f"\n📡 Signal reçu: {signum}")
    if dev_server:
        dev_server.stop()
    sys.exit(0)

def main():
    """Fonction principale"""
    global dev_server
    
    print("🚀 DÉMARRAGE DU SERVEUR DE DÉVELOPPEMENT PRICESCAN")
    print("=" * 60)
    
    try:
        # Créer le serveur de développement
        dev_server = DevServer()
        
        # Configurer les gestionnaires de signaux
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Démarrer le serveur
        dev_server.start()
        
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dev_server = None
    main()
