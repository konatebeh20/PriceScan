from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify, request, session
from requests.auth import HTTPBasicAuth
from sqlalchemy import extract
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest
import datetime
from config.constant import *
from config.db import db
from helpers.mailer import *
from model.price_comparison import *


def ReadActivePromoDeals():
    """
    Récupère toutes les promotions actives pour les supermarchés et pharmacies
    """
    response = {}
    try:
        # Récupérer les promotions actives (is_active=1 et non expirées)
        current_date = datetime.datetime.now().date()
        active_promo_deals = promo_deals.query.filter_by(is_active=1).filter(
            promo_deals.end_date >= current_date
        ).all()
        
        promo_deals_info = []
        for promo_deal in active_promo_deals:
            deal = {}
            deal['promo_uid'] = promo_deal.promo_uid
            deal['store_uid'] = promo_deal.store_uid
            deal['store_name'] = promo_deal.store_name
            deal['store_type'] = promo_deal.store_type  # 'supermarket' ou 'pharmacy'
            deal['product_category'] = promo_deal.product_category
            deal['promo_title'] = promo_deal.promo_title
            deal['promo_description'] = promo_deal.promo_description
            deal['discount_type'] = promo_deal.discount_type  # 'percentage', 'fixed_amount', 'cashback'
            deal['discount_value'] = promo_deal.discount_value
            deal['min_purchase_amount'] = promo_deal.min_purchase_amount
            deal['max_discount_amount'] = promo_deal.max_discount_amount
            deal['promo_code'] = promo_deal.promo_code
            deal['start_date'] = promo_deal.start_date
            deal['end_date'] = promo_deal.end_date
            deal['usage_limit'] = promo_deal.usage_limit
            deal['current_usage_count'] = promo_deal.current_usage_count
            deal['target_user_segment'] = promo_deal.target_user_segment  # 'all', 'new', 'loyal', 'inactive'
            deal['promo_image'] = str(IMGHOSTNAME) + promo_deal.promo_image if promo_deal.promo_image else None
            deal['is_featured'] = promo_deal.is_featured
            deal['loyalty_points_bonus'] = promo_deal.loyalty_points_bonus
            
            promo_deals_info.append(deal)

        response['status'] = 'success'
        response['promo_deals'] = promo_deals_info
        response['total_deals'] = len(promo_deals_info)
        
    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetPersonalizedPromoDeals():
    """
    Récupère les promotions personnalisées pour l'utilisateur connecté
    basées sur ses habitudes d'achat et son segment de fidélité
    """
    response = {}
    try:
        user_uid = request.form.get('user_uid')
        if not user_uid:
            response['status'] = 'error'
            response['error_description'] = 'user_uid is required'
            return response
            
        # Récupérer le profil utilisateur pour déterminer son segment
        user_profile = users.query.filter_by(user_uid=user_uid).first()
        if not user_profile:
            response['status'] = 'error'
            response['error_description'] = 'User not found'
            return response
        
        # Déterminer le segment utilisateur
        user_segment = determine_user_segment(user_profile)
        
        # Récupérer les catégories préférées de l'utilisateur
        user_preferences = get_user_shopping_preferences(user_uid)
        
        current_date = datetime.datetime.now().date()
        
        # Requête pour les promotions personnalisées
        personalized_deals = promo_deals.query.filter(
            promo_deals.is_active == 1,
            promo_deals.end_date >= current_date,
            (promo_deals.target_user_segment == 'all') | 
            (promo_deals.target_user_segment == user_segment)
        ).all()
        
        # Filtrer par catégories préférées si disponibles
        if user_preferences:
            personalized_deals = [deal for deal in personalized_deals 
                                if deal.product_category in user_preferences or 
                                deal.product_category == 'all']
        
        # Trier par pertinence (promotions featured en premier, puis par discount_value)
        personalized_deals.sort(key=lambda x: (x.is_featured, x.discount_value), reverse=True)
        
        promo_deals_info = []
        for promo_deal in personalized_deals:
            deal = {}
            deal['promo_uid'] = promo_deal.promo_uid
            deal['store_uid'] = promo_deal.store_uid
            deal['store_name'] = promo_deal.store_name
            deal['store_type'] = promo_deal.store_type
            deal['product_category'] = promo_deal.product_category
            deal['promo_title'] = promo_deal.promo_title
            deal['promo_description'] = promo_deal.promo_description
            deal['discount_type'] = promo_deal.discount_type
            deal['discount_value'] = promo_deal.discount_value
            deal['min_purchase_amount'] = promo_deal.min_purchase_amount
            deal['max_discount_amount'] = promo_deal.max_discount_amount
            deal['promo_code'] = promo_deal.promo_code
            deal['start_date'] = promo_deal.start_date
            deal['end_date'] = promo_deal.end_date
            deal['days_remaining'] = (promo_deal.end_date - current_date).days
            deal['promo_image'] = str(IMGHOSTNAME) + promo_deal.promo_image if promo_deal.promo_image else None
            deal['loyalty_points_bonus'] = promo_deal.loyalty_points_bonus
            deal['estimated_savings'] = calculate_estimated_savings(promo_deal, user_profile)
            
            promo_deals_info.append(deal)

        response['status'] = 'success'
        response['personalized_deals'] = promo_deals_info
        response['user_segment'] = user_segment
        response['total_deals'] = len(promo_deals_info)
        
    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def CreatePromoDeal():
    """
    Créer une nouvelle promotion pour un magasin/pharmacie
    """
    response = {}
    try:
        new_promo = promo_deals()
        new_promo.store_uid = request.form.get('store_uid')
        new_promo.store_name = request.form.get('store_name')
        new_promo.store_type = request.form.get('store_type')  # 'supermarket' ou 'pharmacy'
        new_promo.product_category = request.form.get('product_category')
        new_promo.promo_title = request.form.get('promo_title')
        new_promo.promo_description = request.form.get('promo_description')
        new_promo.discount_type = request.form.get('discount_type')
        new_promo.discount_value = float(request.form.get('discount_value', 0))
        new_promo.min_purchase_amount = float(request.form.get('min_purchase_amount', 0))
        new_promo.max_discount_amount = float(request.form.get('max_discount_amount', 0))
        new_promo.promo_code = request.form.get('promo_code')
        new_promo.start_date = datetime.datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        new_promo.end_date = datetime.datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        new_promo.usage_limit = int(request.form.get('usage_limit', 0))
        new_promo.target_user_segment = request.form.get('target_user_segment', 'all')
        new_promo.promo_image = request.form.get('promo_image')
        new_promo.is_featured = bool(int(request.form.get('is_featured', 0)))
        new_promo.loyalty_points_bonus = int(request.form.get('loyalty_points_bonus', 0))
        new_promo.is_active = 1
        new_promo.current_usage_count = 0
        new_promo.created_at = datetime.datetime.now()

        db.session.add(new_promo)
        db.session.commit()

        response['status'] = 'success'
        response['message'] = 'Promotion créée avec succès'
        response['promo_uid'] = new_promo.promo_uid

    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def ClaimPromotion():
    """
    Permet à un utilisateur de réclamer/utiliser une promotion
    """
    response = {}
    try:
        user_uid = request.form.get('user_uid')
        promo_uid = request.form.get('promo_uid')
        purchase_amount = float(request.form.get('purchase_amount', 0))
        
        # Vérifier la promotion
        promo = promo_deals.query.filter_by(promo_uid=promo_uid, is_active=1).first()
        if not promo:
            response['status'] = 'error'
            response['error_description'] = 'Promotion non trouvée ou inactive'
            return response
        
        # Vérifier si la promotion n'a pas expiré
        current_date = datetime.datetime.now().date()
        if promo.end_date < current_date:
            response['status'] = 'error'
            response['error_description'] = 'Cette promotion a expiré'
            return response
        
        # Vérifier la limite d'utilisation
        if promo.usage_limit > 0 and promo.current_usage_count >= promo.usage_limit:
            response['status'] = 'error'
            response['error_description'] = 'Limite d\'utilisation de la promotion atteinte'
            return response
        
        # Vérifier le montant minimum d'achat
        if purchase_amount < promo.min_purchase_amount:
            response['status'] = 'error'
            response['error_description'] = f'Montant minimum d\'achat: {promo.min_purchase_amount}€'
            return response
        
        # Calculer la réduction
        discount_amount = calculate_discount(promo, purchase_amount)
        
        # Enregistrer l'utilisation de la promotion
        promo_usage = promo_usage_history()
        promo_usage.user_uid = user_uid
        promo_usage.promo_uid = promo_uid
        promo_usage.purchase_amount = purchase_amount
        promo_usage.discount_amount = discount_amount
        promo_usage.loyalty_points_earned = promo.loyalty_points_bonus
        promo_usage.used_at = datetime.datetime.now()
        
        db.session.add(promo_usage)
        
        # Mettre à jour le compteur d'utilisation de la promotion
        promo.current_usage_count += 1
        db.session.add(promo)
        
        # Mettre à jour les points de fidélité de l'utilisateur
        if promo.loyalty_points_bonus > 0:
            user = users.query.filter_by(user_uid=user_uid).first()
            if user:
                user.loyalty_points += promo.loyalty_points_bonus
                db.session.add(user)
        
        db.session.commit()
        
        response['status'] = 'success'
        response['message'] = 'Promotion utilisée avec succès'
        response['discount_amount'] = discount_amount
        response['loyalty_points_earned'] = promo.loyalty_points_bonus
        response['final_amount'] = purchase_amount - discount_amount

    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def AutoExpirePromotions():
    """
    Fonction automatique pour désactiver les promotions expirées
    À exécuter quotidiennement via un cron job
    """
    response = {}
    try:
        current_date = datetime.datetime.now().date()
        
        # Trouver toutes les promotions expirées
        expired_promotions = promo_deals.query.filter(
            promo_deals.is_active == 1,
            promo_deals.end_date < current_date
        ).all()
        
        expired_count = 0
        for promo in expired_promotions:
            promo.is_active = 0
            db.session.add(promo)
            expired_count += 1
        
        db.session.commit()
        
        response['status'] = 'success'
        response['message'] = f'{expired_count} promotions expirées ont été désactivées'
        response['expired_count'] = expired_count
        
    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


# Fonctions utilitaires

def determine_user_segment(user_profile):
    """
    Détermine le segment de l'utilisateur basé sur son profil
    """
    # Logique pour déterminer le segment utilisateur
    # Par exemple, basé sur la fréquence d'utilisation, les achats, etc.
    days_since_registration = (datetime.datetime.now().date() - user_profile.created_at.date()).days
    
    if days_since_registration <= 7:
        return 'new'
    elif user_profile.loyalty_points >= 1000:
        return 'loyal'
    elif days_since_registration > 90 and user_profile.last_active_at < (datetime.datetime.now() - datetime.timedelta(days=30)):
        return 'inactive'
    else:
        return 'all'


def get_user_shopping_preferences(user_uid):
    """
    Récupère les catégories de produits préférées de l'utilisateur
    basées sur son historique d'achats/recherches
    """
    # Cette fonction analyserait l'historique de l'utilisateur
    # et retournerait ses catégories préférées
    # Pour l'exemple, on retourne une liste statique
    return ['alimentaire', 'hygiene', 'sante']


def calculate_discount(promo, purchase_amount):
    """
    Calcule le montant de la réduction basé sur le type de promotion
    """
    if promo.discount_type == 'percentage':
        discount = purchase_amount * (promo.discount_value / 100)
        if promo.max_discount_amount > 0:
            discount = min(discount, promo.max_discount_amount)
        return discount
    elif promo.discount_type == 'fixed_amount':
        return min(promo.discount_value, purchase_amount)
    elif promo.discount_type == 'cashback':
        return promo.discount_value
    else:
        return 0


def calculate_estimated_savings(promo_deal, user_profile):
    """
    Estime les économies potentielles pour un utilisateur donné
    basées sur ses habitudes d'achat
    """
    # Logique pour estimer les économies basées sur l'historique utilisateur
    # Pour l'exemple, on retourne une estimation simple
    avg_purchase = getattr(user_profile, 'average_purchase_amount', 50.0)
    
    if promo_deal.discount_type == 'percentage':
        estimated_savings = avg_purchase * (promo_deal.discount_value / 100)
        if promo_deal.max_discount_amount > 0:
            estimated_savings = min(estimated_savings, promo_deal.max_discount_amount)
        return estimated_savings
    elif promo_deal.discount_type == 'fixed_amount':
        return min(promo_deal.discount_value, avg_purchase)
    else:
        return promo_deal.discount_value