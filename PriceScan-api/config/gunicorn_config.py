#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
⚙️ Configuration Gunicorn pour PriceScan API
Configuration optimisée pour la production
"""

import multiprocessing
import os

# ========================================
# CONFIGURATION GÉNÉRALE
# ========================================

# Nom de l'application
app_name = "PriceScan API"

# Module WSGI à charger
wsgi_app = "wsgi:app"

# Interface et port
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')

# Nombre de workers
workers = os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1)

# Type de workers
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')

# ========================================
# CONFIGURATION DES WORKERS
# ========================================

# Timeout des workers
worker_timeout = int(os.getenv('GUNICORN_WORKER_TIMEOUT', 120))

# Connexions simultanées par worker
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', 1000))

# Mémoire maximale par worker (en bytes)
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 100))

# Redémarrage automatique des workers
preload_app = os.getenv('GUNICORN_PRELOAD_APP', 'true').lower() == 'true'

# ========================================
# CONFIGURATION DES TIMEOUTS
# ========================================

# Timeout de démarrage
timeout = int(os.getenv('GUNICORN_TIMEOUT', 30))

# Timeout de lecture
read_timeout = int(os.getenv('GUNICORN_READ_TIMEOUT', 60))

# Timeout d'écriture
write_timeout = int(os.getenv('GUNICORN_WRITE_TIMEOUT', 60))

# Timeout de connexion
connect_timeout = int(os.getenv('GUNICORN_CONNECT_TIMEOUT', 10))

# ========================================
# CONFIGURATION DE LA SÉCURITÉ
# ========================================

# Utilisateur et groupe (Linux uniquement)
user = os.getenv('GUNICORN_USER', None)
group = os.getenv('GUNICORN_GROUP', None)

# Changer de répertoire
chdir = os.getenv('GUNICORN_CHDIR', None)

# Limiter les permissions
umask = int(os.getenv('GUNICORN_UMASK', '0o22'), 8)

# ========================================
# CONFIGURATION DES LOGS
# ========================================

# Niveau de log
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')

# Format des logs
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Fichiers de log
accesslog = os.getenv('GUNICORN_ACCESS_LOG', 'logs/gunicorn_access.log')
errorlog = os.getenv('GUNICORN_ERROR_LOG', 'logs/gunicorn_error.log')

# Rotation des logs
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# ========================================
# CONFIGURATION DES PERFORMANCES
# ========================================

# Buffer de lecture
buffer_size = int(os.getenv('GUNICORN_BUFFER_SIZE', 8192))

# Keep-alive
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 2))

# Limite de requêtes par seconde
limit_request_line = int(os.getenv('GUNICORN_LIMIT_REQUEST_LINE', 4094))
limit_request_fields = int(os.getenv('GUNICORN_LIMIT_REQUEST_FIELDS', 100))
limit_request_field_size = int(os.getenv('GUNICORN_LIMIT_REQUEST_FIELD_SIZE', 8190))

# ========================================
# CONFIGURATION DU PROCESSUS
# ========================================

# PID file
pidfile = os.getenv('GUNICORN_PID_FILE', 'logs/gunicorn.pid')

# Daemon mode
daemon = os.getenv('GUNICORN_DAEMON', 'false').lower() == 'true'

# Répertoire de travail
working_dir = os.getenv('GUNICORN_WORKING_DIR', None)

# ========================================
# CONFIGURATION DES SIGNALS
# ========================================

# Graceful shutdown
graceful_timeout = int(os.getenv('GUNICORN_GRACEFUL_TIMEOUT', 30))

# Signal de redémarrage
reload = os.getenv('GUNICORN_RELOAD', 'false').lower() == 'true'

# ========================================
# CONFIGURATION SPÉCIFIQUE À L'ENVIRONNEMENT
# ========================================

def when_ready(server):
    """Appelé quand le serveur est prêt"""
    server.log.info(f"🚀 {app_name} démarré sur {bind}")
    server.log.info(f"📊 {workers} workers démarrés")
    server.log.info(f"⚙️ Mode: {'Production' if not reload else 'Développement'}")

def on_starting(server):
    """Appelé au démarrage du serveur"""
    server.log.info(f"🔄 Démarrage de {app_name}...")

def on_reload(server):
    """Appelé lors du rechargement"""
    server.log.info("🔄 Rechargement de l'application...")

def worker_int(worker):
    """Appelé quand un worker est interrompu"""
    worker.log.info("⚠️ Worker interrompu")

def pre_fork(server, worker):
    """Appelé avant la création d'un worker"""
    server.log.info(f"🔄 Création du worker {worker.pid}")

def post_fork(server, worker):
    """Appelé après la création d'un worker"""
    server.log.info(f"✅ Worker {worker.pid} créé")

def pre_exec(server):
    """Appelé avant l'exécution du serveur"""
    server.log.info("🚀 Exécution du serveur...")

def when_worker_abort(worker):
    """Appelé quand un worker est interrompu de manière anormale"""
    worker.log.warning(f"⚠️ Worker {worker.pid} interrompu de manière anormale")

# ========================================
# CONFIGURATION DES ENVIRONNEMENTS
# ========================================

# Configuration par défaut
default_config = {
    'bind': bind,
    'workers': workers,
    'worker_class': worker_class,
    'worker_timeout': worker_timeout,
    'worker_connections': worker_connections,
    'max_requests': max_requests,
    'max_requests_jitter': max_requests_jitter,
    'preload_app': preload_app,
    'timeout': timeout,
    'read_timeout': read_timeout,
    'write_timeout': write_timeout,
    'connect_timeout': connect_timeout,
    'user': user,
    'group': group,
    'chdir': chdir,
    'umask': umask,
    'loglevel': loglevel,
    'access_log_format': access_log_format,
    'accesslog': accesslog,
    'errorlog': errorlog,
    'buffer_size': buffer_size,
    'keepalive': keepalive,
    'limit_request_line': limit_request_line,
    'limit_request_fields': limit_request_fields,
    'limit_request_field_size': limit_request_field_size,
    'pidfile': pidfile,
    'daemon': daemon,
    'working_dir': working_dir,
    'graceful_timeout': graceful_timeout,
    'reload': reload,
    'when_ready': when_ready,
    'on_starting': on_starting,
    'on_reload': on_reload,
    'worker_int': worker_int,
    'pre_fork': pre_fork,
    'post_fork': post_fork,
    'pre_exec': pre_exec,
    'when_worker_abort': when_worker_abort,
}

# Configuration de développement
dev_config = {
    **default_config,
    'workers': 1,
    'reload': True,
    'loglevel': 'debug',
    'daemon': False,
}

# Configuration de production
prod_config = {
    **default_config,
    'workers': max(4, multiprocessing.cpu_count() * 2),
    'reload': False,
    'loglevel': 'info',
    'daemon': True,
    'preload_app': True,
    'max_requests': 1000,
    'worker_timeout': 120,
}

# Configuration de staging
staging_config = {
    **default_config,
    'workers': max(2, multiprocessing.cpu_count()),
    'reload': False,
    'loglevel': 'info',
    'daemon': False,
    'preload_app': True,
}

def get_config(environment='production'):
    """Retourne la configuration selon l'environnement"""
    configs = {
        'development': dev_config,
        'staging': staging_config,
        'production': prod_config,
    }
    return configs.get(environment, prod_config)
