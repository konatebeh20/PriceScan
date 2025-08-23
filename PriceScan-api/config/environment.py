#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌍 Configuration des environnements
Gère les configurations de développement et de production
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration d'upload
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Configuration CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS') or '*'
    
    # Configuration JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure
    
    # Configuration de base de données (depuis database_config.py)
    try:
        from .database_config import SQL_DB_URL
        SQLALCHEMY_DATABASE_URI = SQL_DB_URL
    except ImportError:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pricescan.db'

class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False
    
    # Logging plus verbeux en développement
    LOG_LEVEL = 'DEBUG'
    
    # Base de données de développement
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI
    
    # Désactiver le cache en développement
    SEND_FILE_MAX_AGE_DEFAULT = 0

class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False
    
    # Logging moins verbeux en production
    LOG_LEVEL = 'INFO'
    
    # Configuration de sécurité renforcée
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuration de base de données de production
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI
    
    # Pool de connexions optimisé pour la production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }

class TestingConfig(Config):
    """Configuration de test"""
    DEBUG = True
    TESTING = True
    
    # Base de données en mémoire pour les tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Désactiver la protection CSRF pour les tests
    WTF_CSRF_ENABLED = False

# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env_name=None):
    """Obtenir la configuration pour un environnement donné"""
    if env_name is None:
        env_name = os.environ.get('FLASK_ENV', 'development')
    
    return config.get(env_name, config['default'])
