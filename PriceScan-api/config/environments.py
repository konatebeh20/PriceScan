#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌍 Configurations d'Environnement PriceScan
Configurations séparées pour développement, staging et production
"""

import os
from pathlib import Path

class BaseConfig:
    """Configuration de base commune à tous les environnements"""
    
    # Informations de base
    APP_NAME = "PriceScan API"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "API de comparaison de prix intelligente"
    
    # Sécurité
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure
    JWT_REFRESH_TOKEN_EXPIRES = 604800  # 7 jours
    
    # Base de données
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 10,
        'pool_size': 10
    }
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'logs/app.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # CORS
    CORS_ORIGINS = ['*']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With']
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = '200 per day;50 per hour;10 per minute'
    
    # Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Scraping
    SCRAPING_ENABLED = True
    SCRAPING_DEBUG = False
    SCRAPING_MAX_WORKERS = 4
    SCRAPING_TIMEOUT = 30
    
    # Notifications
    NOTIFICATIONS_ENABLED = False
    EMAIL_ENABLED = False
    SMS_ENABLED = False
    PUSH_ENABLED = False

class DevelopmentConfig(BaseConfig):
    """Configuration de développement"""
    
    ENV = 'development'
    DEBUG = True
    TESTING = False
    
    # Base de données
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
    if DB_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev_pricescan.db')
    elif DB_TYPE == 'mysql':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost:3306/pricescan_dev')
    elif DB_TYPE == 'postgresql':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/pricescan_dev')
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'logs/dev.log'
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:8080']
    
    # Cache
    CACHE_TYPE = 'simple'
    
    # Scraping
    SCRAPING_DEBUG = True
    SCRAPING_MAX_WORKERS = 2
    
    # Notifications
    NOTIFICATIONS_ENABLED = True
    EMAIL_ENABLED = True

class StagingConfig(BaseConfig):
    """Configuration de staging"""
    
    ENV = 'staging'
    DEBUG = False
    TESTING = False
    
    # Base de données
    DB_TYPE = os.getenv('DB_TYPE', 'mysql')
    if DB_TYPE == 'mysql':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://pricescan_user:password@localhost:3306/pricescan_staging')
    elif DB_TYPE == 'postgresql':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://pricescan_user:password@localhost:5432/pricescan_staging')
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/staging.log'
    
    # CORS
    CORS_ORIGINS = ['https://staging.pricescan.com', 'https://staging-api.pricescan.com']
    
    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
    
    # Scraping
    SCRAPING_MAX_WORKERS = 4
    
    # Notifications
    NOTIFICATIONS_ENABLED = True
    EMAIL_ENABLED = True

class ProductionConfig(BaseConfig):
    """Configuration de production"""
    
    ENV = 'production'
    DEBUG = False
    TESTING = False
    
    # Sécurité renforcée
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY doit être définie en production")
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY doit être définie en production")
    
    # Base de données
    DB_TYPE = os.getenv('DB_TYPE', 'mysql')
    if DB_TYPE == 'mysql':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://pricescan_user:password@localhost:3306/pricescan_prod')
    elif DB_TYPE == 'postgresql':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://pricescan_user:password@localhost:5432/pricescan_prod')
    
    # Logging
    LOG_LEVEL = 'WARNING'
    LOG_FILE = 'logs/production.log'
    
    # CORS
    CORS_ORIGINS = ['https://pricescan.com', 'https://api.pricescan.com']
    
    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Scraping
    SCRAPING_MAX_WORKERS = 8
    SCRAPING_DEBUG = False
    
    # Notifications
    NOTIFICATIONS_ENABLED = True
    EMAIL_ENABLED = True
    SMS_ENABLED = True
    PUSH_ENABLED = True

class TestingConfig(BaseConfig):
    """Configuration de test"""
    
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    
    # Base de données de test
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'logs/test.log'
    
    # CORS
    CORS_ORIGINS = ['*']
    
    # Cache
    CACHE_TYPE = 'simple'
    
    # Scraping
    SCRAPING_ENABLED = False
    
    # Notifications
    NOTIFICATIONS_ENABLED = False

# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Retourne la configuration selon l'environnement"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(config_name, config['default'])

def get_database_config():
    """Retourne la configuration de la base de données selon l'environnement"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return {
            'type': 'mysql',
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'pricescan_user'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME', 'pricescan_prod'),
            'charset': 'utf8mb4',
            'pool_size': 20,
            'max_overflow': 30,
            'pool_recycle': 3600,
            'pool_pre_ping': True
        }
    elif env == 'staging':
        return {
            'type': 'mysql',
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'pricescan_user'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME', 'pricescan_staging'),
            'charset': 'utf8mb4',
            'pool_size': 10,
            'max_overflow': 20,
            'pool_recycle': 1800,
            'pool_pre_ping': True
        }
    else:  # development
        return {
            'type': 'sqlite',
            'database': 'dev_pricescan.db',
            'pool_size': 5,
            'max_overflow': 10,
            'pool_recycle': 900,
            'pool_pre_ping': True
        }

def get_redis_config():
    """Retourne la configuration Redis selon l'environnement"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env in ['production', 'staging']:
        return {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'password': os.getenv('REDIS_PASSWORD'),
            'db': int(os.getenv('REDIS_DB', 0)),
            'decode_responses': True,
            'socket_connect_timeout': 5,
            'socket_timeout': 5,
            'retry_on_timeout': True
        }
    else:
        return {
            'host': 'localhost',
            'port': 6379,
            'db': 1,
            'decode_responses': True
        }

def get_scraping_config():
    """Retourne la configuration du scraping selon l'environnement"""
    env = os.getenv('FLASK_ENV', 'development')
    
    base_config = {
        'enabled': True,
        'max_workers': 4,
        'timeout': 30,
        'retry_count': 3,
        'delay_between_requests': 1.0
    }
    
    if env == 'production':
        base_config.update({
            'max_workers': 8,
            'timeout': 60,
            'retry_count': 5,
            'delay_between_requests': 0.5
        })
    elif env == 'staging':
        base_config.update({
            'max_workers': 4,
            'timeout': 45,
            'retry_count': 3,
            'delay_between_requests': 1.0
        })
    else:  # development
        base_config.update({
            'max_workers': 2,
            'timeout': 30,
            'retry_count': 2,
            'delay_between_requests': 2.0
        })
    
    return base_config

def get_logging_config():
    """Retourne la configuration du logging selon l'environnement"""
    env = os.getenv('FLASK_ENV', 'development')
    
    base_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
    
    if env == 'production':
        base_config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'standard',
            'filename': 'logs/production.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5
        }
        base_config['root']['handlers'] = ['console', 'file']
        base_config['root']['level'] = 'WARNING'
        
    elif env == 'staging':
        base_config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': 'logs/staging.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 3
        }
        base_config['root']['handlers'] = ['console', 'file']
        base_config['root']['level'] = 'INFO'
        
    else:  # development
        base_config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'logs/development.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 2
        }
        base_config['root']['handlers'] = ['console', 'file']
        base_config['root']['level'] = 'DEBUG'
    
    return base_config
