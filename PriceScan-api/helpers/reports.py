import csv
import json
import smtplib
import string
import time
import urllib.request
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
from flask import Flask, jsonify, request, session
from requests.auth import HTTPBasicAuth
from sqlalchemy import extract, func, desc
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest
from config.constant import *
from config.db import db
from helpers.mailer import *
from model.price_comparison import price_submissions, users, stores, products, user_activity_log
from apns2.client import APNsClient
from apns2.payload import Payload


def yearly_price_data():
    """
    Rapport annuel des soumissions de prix et activités utilisateurs
    """
    response = {}
    try:
        current_year = datetime.now().year
        
        # Statistiques des soumissions de prix pour l'année
        total_submissions = price_submissions.query.filter(
            extract('year', price_submissions.created_at) == current_year
        ).count()
        
        # Nombre d'utilisateurs actifs cette année
        active_users = users.query.join(price_submissions).filter(
            extract('year', price_submissions.created_at) == current_year
        ).distinct().count()
        
        # Nombre de nouveaux magasins ajoutés cette année
        new_stores = stores.query.filter(
            extract('year', stores.created_at) == current_year
        ).count()
        
        # Nombre de produits uniques scannés cette année
        unique_products = price_submissions.query.join(products).filter(
            extract('year', price_submissions.created_at) == current_year
        ).distinct(products.product_id).count()
        
        # Top 5 des magasins avec le plus de soumissions
        top_stores = db.session.query(
            stores.store_name,
            func.count(price_submissions.submission_id).label('submission_count')
        ).join(price_submissions).filter(
            extract('year', price_submissions.created_at) == current_year
        ).group_by(stores.store_id).order_by(
            desc('submission_count')
        ).limit(5).all()
        
        rs = {
            'year': current_year,
            'total_price_submissions': total_submissions,
            'active_users': active_users,
            'new_stores_added': new_stores,
            'unique_products_tracked': unique_products,
            'top_contributing_stores': [{'store_name': store[0], 'submissions': store[1]} for store in top_stores],
            'average_submissions_per_user': round(total_submissions / max(active_users, 1), 2)
        }
        
        response['response'] = 'success'
        response['data'] = rs
        
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Database Error'
        response['error_code'] = 'PSE01'
        response['error_description'] = str(e.__dict__['orig'])
        c = BadRequest(str(e.__dict__['orig']))
        c.data = response
        raise c
    
    return response


def monthly_price_data():
    """
    Rapport mensuel des activités de comparaison de prix
    """
    response = {}
    try:
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Soumissions de prix du mois actuel
        monthly_submissions = price_submissions.query.filter(
            extract('year', price_submissions.created_at) == current_year,
            extract('month', price_submissions.created_at) == current_month
        ).count()
        
        # Nouveaux utilisateurs ce mois
        new_users_this_month = users.query.filter(
            extract('year', users.created_at) == current_year,
            extract('month', users.created_at) == current_month
        ).count()
        
        # Comparaisons effectuées ce mois (utilisateurs ayant cherché des prix)
        monthly_searches = user_activity_log.query.filter(
            user_activity_log.activity_type == 'price_search',
            extract('year', user_activity_log.created_at) == current_year,
            extract('month', user_activity_log.created_at) == current_month
        ).count()
        
        # Économies potentielles générées (estimation basée sur les écarts de prix)
        price_differences = db.session.query(
            func.avg(price_submissions.price).label('avg_price')
        ).join(products).filter(
            extract('year', price_submissions.created_at) == current_year,
            extract('month', price_submissions.created_at) == current_month
        ).group_by(products.product_id).all()
        
        # Catégories de produits les plus populaires ce mois
        popular_categories = db.session.query(
            products.category,
            func.count(price_submissions.submission_id).label('submission_count')
        ).join(price_submissions).filter(
            extract('year', price_submissions.created_at) == current_year,
            extract('month', price_submissions.created_at) == current_month
        ).group_by(products.category).order_by(
            desc('submission_count')
        ).limit(10).all()
        
        # Évolution par rapport au mois précédent
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        
        prev_month_submissions = price_submissions.query.filter(
            extract('year', price_submissions.created_at) == prev_year,
            extract('month', price_submissions.created_at) == prev_month
        ).count()
        
        growth_rate = ((monthly_submissions - prev_month_submissions) / max(prev_month_submissions, 1)) * 100
        
        rs = {
            'year': current_year,
            'month': current_month,
            'total_price_submissions': monthly_submissions,
            'new_users': new_users_this_month,
            'price_searches_performed': monthly_searches,
            'popular_categories': [{'category': cat[0], 'submissions': cat[1]} for cat in popular_categories],
            'growth_rate_percent': round(growth_rate, 2),
            'previous_month_submissions': prev_month_submissions
        }
        
        response['response'] = 'success'
        response['data'] = rs
        
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Database Error'
        response['error_code'] = 'PSE02'
        response['error_description'] = str(e.__dict__['orig'])
        c = BadRequest(str(e.__dict__['orig']))
        c.data = response
        raise c
    
    return response


def daily_price_data():
    """
    Rapport quotidien des activités de comparaison de prix
    """
    response = {}
    try:
        today = datetime.now().date()
        
        # Soumissions de prix aujourd'hui
        daily_submissions = price_submissions.query.filter(
            func.date(price_submissions.created_at) == today
        ).count()
        
        # Utilisateurs actifs aujourd'hui
        active_users_today = db.session.query(users.user_id).join(price_submissions).filter(
            func.date(price_submissions.created_at) == today
        ).distinct().count()
        
        # Nouveaux utilisateurs inscrits aujourd'hui
        new_users_today = users.query.filter(
            func.date(users.created_at) == today
        ).count()
        
        # Recherches de prix effectuées aujourd'hui
        daily_searches = user_activity_log.query.filter(
            user_activity_log.activity_type == 'price_search',
            func.date(user_activity_log.created_at) == today
        ).count()
        
        # Magasins les plus actifs aujourd'hui
        active_stores_today = db.session.query(
            stores.store_name,
            func.count(price_submissions.submission_id).label('submission_count')
        ).join(price_submissions).filter(
            func.date(price_submissions.created_at) == today
        ).group_by(stores.store_id).order_by(
            desc('submission_count')
        ).limit(5).all()
        
        # Évolution par rapport à hier
        yesterday = today - timedelta(days=1)
        yesterday_submissions = price_submissions.query.filter(
            func.date(price_submissions.created_at) == yesterday
        ).count()
        
        daily_change = daily_submissions - yesterday_submissions
        
        rs = {
            'date': today.strftime('%Y-%m-%d'),
            'daily_price_submissions': daily_submissions,
            'active_users': active_users_today,
            'new_users': new_users_today,
            'price_searches': daily_searches,
            'most_active_stores': [{'store_name': store[0], 'submissions': store[1]} for store in active_stores_today],
            'change_from_yesterday': daily_change,
            'yesterday_submissions': yesterday_submissions
        }
        
        response['response'] = 'success'
        response['data'] = rs
        
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Database Error'
        response['error_code'] = 'PSE03'
        response['error_description'] = str(e.__dict__['orig'])
        c = BadRequest(str(e.__dict__['orig']))
        c.data = response
        raise c
    
    return response


def user_engagement_report():
    """
    Rapport d'engagement des utilisateurs pour l'app de comparaison de prix
    """
    response = {}
    try:
        # Utilisateurs les plus actifs (top contributeurs)
        top_contributors = db.session.query(
            users.username,
            users.user_id,
            func.count(price_submissions.submission_id).label('total_submissions'),
            users.loyalty_points
        ).join(price_submissions).group_by(users.user_id).order_by(
            desc('total_submissions')
        ).limit(10).all()
        
        # Utilisateurs inactifs (pas d'activité depuis 30 jours)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        inactive_users = users.query.filter(
            users.last_active_at < thirty_days_ago
        ).count()
        
        # Taux de rétention (utilisateurs actifs ce mois parmi ceux inscrits le mois dernier)
        current_month = datetime.now().month
        current_year = datetime.now().year
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        
        users_registered_last_month = users.query.filter(
            extract('year', users.created_at) == prev_year,
            extract('month', users.created_at) == prev_month
        ).count()
        
        users_active_this_month_from_last_month = db.session.query(users.user_id).join(price_submissions).filter(
            extract('year', users.created_at) == prev_year,
            extract('month', users.created_at) == prev_month,
            extract('year', price_submissions.created_at) == current_year,
            extract('month', price_submissions.created_at) == current_month
        ).distinct().count()
        
        retention_rate = (users_active_this_month_from_last_month / max(users_registered_last_month, 1)) * 100
        
        rs = {
            'top_contributors': [
                {
                    'username': contrib[0],
                    'user_id': contrib[1],
                    'total_submissions': contrib[2],
                    'loyalty_points': contrib[3]
                } for contrib in top_contributors
            ],
            'inactive_users_count': inactive_users,
            'retention_rate_percent': round(retention_rate, 2),
            'users_registered_last_month': users_registered_last_month,
            'users_retained_this_month': users_active_this_month_from_last_month
        }
        
        response['response'] = 'success'
        response['data'] = rs
        
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Database Error'
        response['error_code'] = 'PSE04'
        response['error_description'] = str(e.__dict__['orig'])
        c = BadRequest(str(e.__dict__['orig']))
        c.data = response
        raise c
    
    return response


def price_trend_analysis():
    """
    Analyse des tendances de prix pour identifier les fluctuations importantes
    """
    response = {}
    try:
        # Produits avec les plus grandes variations de prix (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        price_variations = db.session.query(
            products.product_name,
            products.barcode,
            func.min(price_submissions.price).label('min_price'),
            func.max(price_submissions.price).label('max_price'),
            func.avg(price_submissions.price).label('avg_price'),
            func.count(price_submissions.submission_id).label('price_points')
        ).join(price_submissions).filter(
            price_submissions.created_at >= thirty_days_ago
        ).group_by(products.product_id).having(
            func.count(price_submissions.submission_id) >= 5  # Au moins 5 points de prix
        ).order_by(
            desc(func.max(price_submissions.price) - func.min(price_submissions.price))
        ).limit(20).all()
        
        # Magasins les plus compétitifs (prix moyens les plus bas)
        competitive_stores = db.session.query(
            stores.store_name,
            stores.store_type,
            func.avg(price_submissions.price).label('avg_price'),
            func.count(price_submissions.submission_id).label('total_submissions')
        ).join(price_submissions).filter(
            price_submissions.created_at >= thirty_days_ago
        ).group_by(stores.store_id).having(
            func.count(price_submissions.submission_id) >= 10  # Au moins 10 soumissions
        ).order_by('avg_price').limit(10).all()
        
        rs = {
            'analysis_period': '30 days',
            'high_variation_products': [
                {
                    'product_name': prod[0],
                    'barcode': prod[1],
                    'min_price': float(prod[2]),
                    'max_price': float(prod[3]),
                    'avg_price': round(float(prod[4]), 2),
                    'price_difference': round(float(prod[3]) - float(prod[2]), 2),
                    'data_points': prod[5]
                } for prod in price_variations
            ],
            'most_competitive_stores': [
                {
                    'store_name': store[0],
                    'store_type': store[1],
                    'average_price': round(float(store[2]), 2),
                    'total_submissions': store[3]
                } for store in competitive_stores
            ]
        }
        
        response['response'] = 'success'
        response['data'] = rs
        
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Database Error'
        response['error_code'] = 'PSE05'
        response['error_description'] = str(e.__dict__['orig'])
        c = BadRequest(str(e.__dict__['orig']))
        c.data = response
        raise c
    
    return response


def send_ios_push_notification(device_token, message, notification_type="price_alert"):
    """
    Envoie une notification push iOS adaptée pour PriceScan
    :param device_token: Token APNs de l'appareil cible
    :param message: Message à envoyer
    :param notification_type: Type de notification (price_alert, promo, weekly_report, etc.)
    """
    # Créer le payload personnalisé selon le type
    if notification_type == "price_alert":
        payload = Payload(
            alert=message,
            sound="default",
            badge=1,
            custom_data={
                "type": "price_alert",
                "action": "open_price_comparison"
            }
        )
    elif notification_type == "promo":
        payload = Payload(
            alert=message,
            sound="promo_sound.wav",
            badge=1,
            custom_data={
                "type": "promotion",
                "action": "open_promotions"
            }
        )
    elif notification_type == "weekly_report":
        payload = Payload(
            alert=message,
            sound="default",
            badge=1,
            custom_data={
                "type": "report",
                "action": "open_savings_report"
            }
        )
    else:
        payload = Payload(alert=message, sound="default", badge=1)
    
    # Choisir le serveur APNs
    server = "api.push.apple.com" if IS_PRODUCTION else "api.sandbox.push.apple.com"
    
    try:
        # Initialiser le client APNs
        client = APNsClient(
            APNS_KEY_PATH,
            team_id=TEAM_ID,
            key_id=APNS_KEY_ID,
            use_sandbox=not IS_PRODUCTION
        )
        
        # Envoyer la notification
        client.send_notification(device_token, payload, APNS_TOPIC)
        print(f"PriceScan notification sent successfully to {device_token}: {notification_type}")
        
        # Log de la notification envoyée
        log_notification_sent(device_token, message, notification_type)
        
    except Exception as e:
        print(f"Failed to send PriceScan notification: {e}")


def send_weekly_report_notifications():
    """
    Envoie les rapports hebdomadaires aux utilisateurs actifs
    """
    try:
        # Récupérer les utilisateurs actifs avec des tokens de notification
        active_users = users.query.filter(
            users.push_token.isnot(None),
            users.notifications_enabled == True,
            users.last_active_at >= (datetime.now() - timedelta(days=30))
        ).all()
        
        for user in active_users:
            # Calculer les économies de l'utilisateur cette semaine
            user_savings = calculate_user_weekly_savings(user.user_id)
            
            message = f"📊 Votre rapport PriceScan: {user_savings}€ économisés cette semaine ! Découvrez vos meilleures affaires."
            
            send_ios_push_notification(
                user.push_token,
                message,
                "weekly_report"
            )
        
        print(f"Weekly reports sent to {len(active_users)} users")
        
    except Exception as e:
        print(f"Error sending weekly reports: {e}")


def calculate_user_weekly_savings(user_id):
    """
    Calcule les économies potentielles d'un utilisateur sur la semaine
    """
    # Logique pour calculer les économies basées sur les comparaisons de prix
    # Cette fonction analyserait les recherches de l'utilisateur et calculerait
    # les économies potentielles en comparant les prix qu'il a vus
    return 12.45  # Exemple de retour


def log_notification_sent(device_token, message, notification_type):
    """
    Enregistre les notifications envoyées pour le suivi
    """
    # Ici on pourrait enregistrer dans une table de logs
    pass