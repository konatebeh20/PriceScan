import cv2
import numpy as np
# import matplotlib.pyplot as plt

import csv
import json
import smtplib
import string
import time
import urllib.request
import hashlib
from datetime import date, datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import lxml
import requests
import urllib3
import xmltodict
from bs4 import BeautifulSoup
from flask import jsonify, request
from requests.auth import HTTPBasicAuth
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from config.constant import *
# from config.constant import OCR_API_KEY, OCR_API_URL
from config.db import db


from model.PriceScan_db import *
from helpers.mailer import send_mailer_custom

from helpers.mailer import *




def create_user():
    """
    Créer un nouveau compte utilisateur PriceScan
    """
    response = {}
    try:
        # Vérifier si l'email existe déjà
        existing_user = ps_users.query.filter_by(email=request.json.get('email')).first()
        if existing_user:
            response['response'] = 'error'
            response['error_code'] = 'PSU01'
            response['error_description'] = 'Email already exists'
            return response

        # Vérifier si le username existe déjà
        existing_username = ps_users.query.filter_by(username=request.json.get('username')).first()
        if existing_username:
            response['response'] = 'error'
            response['error_code'] = 'PSU02'
            response['error_description'] = 'Username already taken'
            return response

        # Créer le nouvel utilisateur
        new_user = ps_users()
        
        new_user.first_name = request.json.get('first_name')
        new_user.last_name = request.json.get('last_name')
        new_user.username = request.json.get('username')
        new_user.email = request.json.get('email')
        new_user.phone = request.json.get('phone', '')
        new_user.address = request.json.get('address', '')
        new_user.city = request.json.get('city', '')
        new_user.country = request.json.get('country', '')
        new_user.postal_code = request.json.get('postal_code', '')
        new_user.profile_image = request.json.get('profile_image', '')
        new_user.date_of_birth = request.json.get('date_of_birth')
        
        # Hachage sécurisé du mot de passe
        password = request.json.get('password')
        new_user.password_hash = generate_password_hash(password)
        
        # Paramètres par défaut
        new_user.is_active = True
        new_user.is_verified = False
        new_user.loyalty_points = 0
        new_user.total_submissions = 0
        new_user.total_savings = 0.0
        new_user.notifications_enabled = True
        new_user.location_sharing = request.json.get('location_sharing', True)
        new_user.privacy_level = request.json.get('privacy_level', 'public')
        new_user.preferred_language = request.json.get('preferred_language', 'fr')
        new_user.preferred_currency = request.json.get('preferred_currency', 'EUR')
        new_user.push_token = request.json.get('push_token', '')
        new_user.created_at = datetime.now()
        new_user.last_active_at = datetime.now()

        db.session.add(new_user)
        db.session.commit()

        # Créer les préférences utilisateur par défaut
        create_default_user_preferences(new_user.user_id)

        # Enregistrer l'activité de création de compte
        log_user_activity(new_user.user_id, 'account_created')

        # Préparer la réponse
        user_data = {
            'user_id': new_user.user_id,
            'username': new_user.username,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'loyalty_points': new_user.loyalty_points,
            'is_verified': new_user.is_verified,
            'preferred_language': new_user.preferred_language
        }

        response['user'] = user_data
        response['response'] = 'success'
        response['message'] = 'Account created successfully'

        # Envoyer email de bienvenue
        send_welcome_email(new_user.email, new_user.first_name, new_user.user_id)

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error_code'] = 'PSU03'
        response['error_description'] = str(e.__dict__.get('orig', e))
        return response
    
    return response


def authenticate_user():
    """
    Authentifier un utilisateur et générer un token JWT
    """
    response = {}
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            response['response'] = 'error'
            response['error_code'] = 'PSU04'
            response['error_description'] = 'Email and password required'
            return response

        # Trouver l'utilisateur par email
        user = ps_users.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            response['response'] = 'error'
            response['error_code'] = 'PSU05'
            response['error_description'] = 'Invalid credentials'
            return response

        if not user.is_active:
            response['response'] = 'error'
            response['error_code'] = 'PSU06'
            response['error_description'] = 'Account is deactivated'
            return response

        # Mettre à jour la dernière activité
        user.last_active_at = datetime.now()
        user.login_count += 1
        db.session.add(user)
        db.session.commit()

        # Générer le token JWT
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=7))

        # Enregistrer l'activité de connexion
        log_user_activity(user.user_id, 'login')

        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'loyalty_points': user.loyalty_points,
            'total_submissions': user.total_submissions,
            'total_savings': user.total_savings,
            'is_verified': user.is_verified,
            'profile_image': user.profile_image,
            'preferred_language': user.preferred_language,
            'preferred_currency': user.preferred_currency
        }

        response['user'] = user_data
        response['access_token'] = access_token
        response['response'] = 'success'
        response['message'] = 'Login successful'

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error_code'] = 'PSU07'
        response['error_description'] = str(e.__dict__.get('orig', e))
        
    return response


# @jwt_required()
def get_user_profile():
    """
    Récupérer le profil complet de l'utilisateur connecté
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        user = ps_users.query.filter_by(user_id=current_user_id).first()
        
        if not user:
            response['response'] = 'error'
            response['error_code'] = 'PSU08'
            response['error_description'] = 'User not found'
            return response

        # Statistiques utilisateur
        recent_submissions = price_submissions.query.filter_by(
            user_id=current_user_id
        ).order_by(price_submissions.created_at.desc()).limit(10).all()

        user_preferences_data = user_preferences.query.filter_by(
            user_id=current_user_id
        ).first()

        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'city': user.city,
            'country': user.country,
            'postal_code': user.postal_code,
            'profile_image': user.profile_image,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
            'loyalty_points': user.loyalty_points,
            'total_submissions': user.total_submissions,
            'total_savings': user.total_savings,
            'is_verified': user.is_verified,
            'notifications_enabled': user.notifications_enabled,
            'location_sharing': user.location_sharing,
            'privacy_level': user.privacy_level,
            'preferred_language': user.preferred_language,
            'preferred_currency': user.preferred_currency,
            'member_since': user.created_at.strftime('%Y-%m-%d'),
            'last_active': user.last_active_at.strftime('%Y-%m-%d %H:%M:%S'),
            'login_count': user.login_count,
            'recent_submissions_count': len(recent_submissions),
            'user_level': calculate_user_level(user.loyalty_points)
        }

        # Ajouter les préférences si elles existent
        if user_preferences_data:
            user_data['preferences'] = {
                'favorite_stores': user_preferences_data.favorite_stores,
                'favorite_categories': user_preferences_data.favorite_categories,
                'price_alert_threshold': user_preferences_data.price_alert_threshold,
                'max_distance_km': user_preferences_data.max_distance_km
            }

        response['user'] = user_data
        response['response'] = 'success'

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error_code'] = 'PSU09'
        response['error_description'] = str(e.__dict__.get('orig', e))
        
    return response


# @jwt_required()
def update_user_profile():
    """
    Mettre à jour le profil utilisateur
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        user = ps_users.query.filter_by(user_id=current_user_id).first()
        
        if not user:
            response['response'] = 'error'
            response['error_code'] = 'PSU10'
            response['error_description'] = 'User not found'
            return response

        # Mettre à jour les champs fournis
        updatable_fields = [
            'first_name', 'last_name', 'phone', 'address', 'city', 
            'country', 'postal_code', 'profile_image', 'date_of_birth',
            'notifications_enabled', 'location_sharing', 'privacy_level',
            'preferred_language', 'preferred_currency'
        ]

        for field in updatable_fields:
            if field in request.json:
                setattr(user, field, request.json.get(field))

        # Mettre à jour le timestamp de modification
        user.updated_at = datetime.now()

        db.session.add(user)
        db.session.commit()

        # Enregistrer l'activité de mise à jour
        log_user_activity(current_user_id, 'profile_updated')

        response['response'] = 'success'
        response['message'] = 'Profile updated successfully'

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error_code'] = 'PSU11'
        response['error_description'] = str(e.__dict__.get('orig', e))
        
    return response


# @jwt_required()
def change_password():
    """
    Changer le mot de passe utilisateur
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        user = ps_users.query.filter_by(user_id=current_user_id).first()
        
        if not user:
            response['response'] = 'error'
            response['error_code'] = 'PSU12'
            response['error_description'] = 'User not found'
            return response

        current_password = request.json.get('current_password')
        new_password = request.json.get('new_password')

        if not current_password or not new_password:
            response['response'] = 'error'
            response['error_code'] = 'PSU13'
            response['error_description'] = 'Current and new password required'
            return response

        # Vérifier le mot de passe actuel
        if not check_password_hash(user.password_hash, current_password):
            response['response'] = 'error'
            response['error_code'] = 'PSU14'
            response['error_description'] = 'Current password is incorrect'
            return response

        # Mettre à jour avec le nouveau mot de passe
        user.password_hash = generate_password_hash(new_password)
        user.updated_at = datetime.now()

        db.session.add(user)
        db.session.commit()

        # Enregistrer l'activité de changement de mot de passe
        log_user_activity(current_user_id, 'password_changed')

        response['response'] = 'success'
        response['message'] = 'Password changed successfully'

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error_code'] = 'PSU15'
        response['error_description'] = str(e.__dict__.get('orig', e))
        
    return response


def verify_email():
    """
    Vérifier l'email d'un utilisateur
    """
    response = {}
    try:
        user_id = request.json.get('user_id')
        verification_code = request.json.get('verification_code')
        
        user = ps_users.query.filter_by(user_id=user_id).first()
        if not user:
            response['response'] = 'error'
            response['error_code'] = 'PSU16'
            response['error_description'] = 'User not found'
            return response

        if user.is_verified:
            response['response'] = 'success'
            response['message'] = 'Email already verified'
            response['code'] = '002'
            return response

        # Vérifier le code (ici on peut implémenter la logique de vérification)
        # Pour l'exemple, on accepte n'importe quel code
        user.is_verified = True
        user.email_verified_at = datetime.now()
        user.loyalty_points += 100  # Bonus de vérification
        
        db.session.add(user)
        db.session.commit()

        # Enregistrer l'activité de vérification
        log_user_activity(user_id, 'email_verified')

        response['response'] = 'success'
        response['message'] = 'Email verified successfully! +100 loyalty points'
        response['code'] = '001'
        response['loyalty_points_earned'] = 100

        # Envoyer email de confirmation
        send_verification_success_email(user.email, user.first_name)

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error_code'] = 'PSU17'
        response['error_description'] = str(e.__dict__.get('orig', e))
        
    return response


# @jwt_required()
def delete_account():
    """
    Supprimer le compte utilisateur (soft delete)
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        user = ps_users.query.filter_by(user_id=current_user_id).first()
        
        if not user:
            response['response'] = 'error'
            response['error_code'] = 'PSU18'
            response['error_description'] = 'User not found'
            return response

        # Soft delete - désactiver le compte au lieu de le supprimer
        user.is_active = False
        user.deleted_at = datetime.now()
        
        db.session.add(user)
        db.session.commit()

        # Enregistrer l'activité de suppression
        log_user_activity(current_user_id, 'account_deleted')

        response['response'] = 'success'
        response['message'] = 'Account deactivated successfully'

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error_code'] = 'PSU19'
        response['error_description'] = str(e.__dict__.get('orig', e))
        
    return response


# @jwt_required()
def update_loyalty_points():
    """
    Mettre à jour les points de fidélité d'un utilisateur
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        user = ps_users.query.filter_by(user_id=current_user_id).first()
        
        if not user:
            response['response'] = 'error'
            response['error_code'] = 'PSU20'
            response['error_description'] = 'User not found'
            return response

        points_to_add = request.json.get('points', 0)
        activity_type = request.json.get('activity_type', 'manual_adjustment')
        
        user.loyalty_points += points_to_add
        user.updated_at = datetime.now()
        
        db.session.add(user)
        db.session.commit()

        # Enregistrer l'activité d'ajout de points
        log_user_activity(current_user_id, f'points_earned_{activity_type}', {'points': points_to_add})

        response['response'] = 'success'
        response['message'] = f'{points_to_add} loyalty points added'
        response['total_points'] = user.loyalty_points
        response['user_level'] = calculate_user_level(user.loyalty_points)

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error_code'] = 'PSU21'
        response['error_description'] = str(e.__dict__.get('orig', e))
        
    return response


# Fonctions utilitaires

def create_default_user_preferences(user_id):
    """
    Créer les préférences par défaut pour un nouvel utilisateur
    """
    try:
        preferences = user_preferences()
        preferences.user_id = user_id
        preferences.favorite_stores = []
        preferences.favorite_categories = ['alimentaire', 'hygiene']
        preferences.price_alert_threshold = 10.0  # 10% de réduction
        preferences.max_distance_km = 5.0
        preferences.notification_frequency = 'daily'
        preferences.created_at = datetime.now()
        
        db.session.add(preferences)
        db.session.commit()
    except Exception as e:
        print(f"Error creating user preferences: {e}")


def log_user_activity(user_id, activity_type, metadata=None):
    """
    Enregistrer l'activité utilisateur
    """
    try:
        activity = ps_user_activity_log()
        activity.user_id = user_id
        activity.activity_type = activity_type
        activity.metadata = json.dumps(metadata) if metadata else None
        activity.created_at = datetime.now()
        
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging user activity: {e}")


def calculate_user_level(loyalty_points):
    """
    Calculer le niveau utilisateur basé sur les points de fidélité
    """
    if loyalty_points >= 10000:
        return 'platinum'
    elif loyalty_points >= 5000:
        return 'gold'
    elif loyalty_points >= 1000:
        return 'silver'
    else:
        return 'bronze'


def send_welcome_email(email, first_name, user_id):
    """
    Envoyer email de bienvenue avec lien de vérification
    """
    try:
        subject = "Bienvenue sur PriceScan! 🛒"
        verification_link = f"{FRONTEND_URL}/verify-email?user_id={user_id}"
        
        body = f"""
        Bonjour {first_name},
        
        Bienvenue sur PriceScan ! 🎉
        
        Votre compte a été créé avec succès. Pour commencer à économiser avec nous :
        
        1. Vérifiez votre email en cliquant ici : {verification_link}
        2. Téléchargez l'app PriceScan sur votre téléphone
        3. Commencez à scanner et comparer les prix !
        
        En cadeau de bienvenue, vous avez déjà gagné vos premiers points de fidélité.
        
        L'équipe PriceScan 🛍️
        """
        
        # Utiliser la fonction mailer existante
        send_mailer_custom(email, subject, body)
    except Exception as e:
        print(f"Error sending welcome email: {e}")


def send_verification_success_email(email, first_name):
    """
    Envoyer email de confirmation de vérification
    """
    try:
        subject = "Email vérifié avec succès! ✅"
        
        body = f"""
        Félicitations {first_name} !
        
        Votre email a été vérifié avec succès. 
        Vous avez gagné 100 points de fidélité ! 🎯
        
        Vous pouvez maintenant profiter pleinement de toutes les fonctionnalités PriceScan.
        
        Bonne chasse aux bonnes affaires ! 🛒
        
        L'équipe PriceScan
        """
        
        send_mailer_custom(email, subject, body)
    except Exception as e:
        print(f"Error sending verification email: {e}")