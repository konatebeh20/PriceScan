#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎯 API Resource pour la gestion des promotions
Gère les opérations CRUD sur les promotions
"""

import json
import logging
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource

from config.db import db
from model.PriceScan_db import ps_promotions, ps_stores, ps_products, ps_categories
from helpers.promo_deals import PromoDealsHelper

logger = logging.getLogger(__name__)


class PromotionsApi(Resource):
    """API Resource pour la gestion des promotions"""
    
    def get(self, route):
        """
        GET /api/promotions/<route>
        
        Routes disponibles:
        - all: Récupère toutes les promotions
        - active: Récupère les promotions actives
        - featured: Récupère les promotions mises en avant
        - store/<store_id>: Promotions d'un magasin spécifique
        - product/<product_id>: Promotions d'un produit spécifique
        - category/<category_id>: Promotions d'une catégorie spécifique
        """
        try:
            if route == "all":
                return self._get_all_promotions()
            elif route == "active":
                return self._get_active_promotions()
            elif route == "featured":
                return self._get_featured_promotions()
            elif route.startswith("store/"):
                store_id = int(route.split("/")[1])
                return self._get_promotions_by_store(store_id)
            elif route.startswith("product/"):
                product_id = int(route.split("/")[1])
                return self._get_promotions_by_product(product_id)
            elif route.startswith("category/"):
                category_id = int(route.split("/")[1])
                return self._get_promotions_by_category(category_id)
            else:
                return {"error": "Route non reconnue"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
    
    def post(self, route):
        """
        POST /api/promotions/<route>
        
        Routes disponibles:
        - create: Crée une nouvelle promotion
        """
        try:
            if route == "create":
                return self._create_promotion()
            else:
                return {"error": "Route non reconnue"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la création de la promotion: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
    
    def patch(self, route):
        """
        PATCH /api/promotions/<route>
        
        Routes disponibles:
        - update/<promotion_id>: Met à jour une promotion
        """
        try:
            if route.startswith("update/"):
                promotion_id = int(route.split("/")[1])
                return self._update_promotion(promotion_id)
            else:
                return {"error": "Route non reconnue"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la promotion: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
    
    def delete(self, route):
        """
        DELETE /api/promotions/<route>
        
        Routes disponibles:
        - delete/<promotion_id>: Supprime une promotion
        """
        try:
            if route.startswith("delete/"):
                promotion_id = int(route.split("/")[1])
                return self._delete_promotion(promotion_id)
            else:
                return {"error": "Route non reconnue"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la promotion: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
    
    def _get_all_promotions(self):
        """Récupère toutes les promotions"""
        try:
            promotions = ps_promotions.query.order_by(
                ps_promotions.creation_date.desc()
            ).all()
            
            promotions_data = []
            for promo in promotions:
                promo_data = {
                    'id': promo.id,
                    'promotion_uid': promo.promotion_uid,
                    'title': promo.title,
                    'description': promo.description,
                    'discount_type': promo.discount_type,
                    'discount_value': promo.discount_value,
                    'min_purchase': promo.min_purchase,
                    'max_discount': promo.max_discount,
                    'start_date': promo.start_date.isoformat() if promo.start_date else None,
                    'end_date': promo.end_date.isoformat() if promo.end_date else None,
                    'store_id': promo.store_id,
                    'product_id': promo.product_id,
                    'category_id': promo.category_id,
                    'is_active': promo.is_active,
                    'is_featured': promo.is_featured,
                    'creation_date': promo.creation_date.isoformat() if promo.creation_date else None,
                    'updated_on': promo.updated_on.isoformat() if promo.updated_on else None
                }
                
                # Ajouter les informations du magasin si disponible
                if promo.store_id:
                    store = ps_stores.query.get(promo.store_id)
                    if store:
                        promo_data['store_name'] = store.store_name
                
                # Ajouter les informations du produit si disponible
                if promo.product_id:
                    product = ps_products.query.get(promo.product_id)
                    if product:
                        promo_data['product_name'] = product.product_name
                
                # Ajouter les informations de la catégorie si disponible
                if promo.category_id:
                    category = ps_categories.query.get(promo.category_id)
                    if category:
                        promo_data['category_name'] = category.cat_label
                
                promotions_data.append(promo_data)
            
            return {
                "status": "success",
                "promotions": promotions_data,
                "total": len(promotions_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de toutes les promotions: {str(e)}")
            return {"error": "Erreur lors de la récupération des promotions"}, 500
    
    def _get_active_promotions(self):
        """Récupère les promotions actives"""
        try:
            active_promotions = PromoDealsHelper.get_active_promotions()
            
            promotions_data = []
            for promo in active_promotions:
                promo_data = {
                    'id': promo.id,
                    'promotion_uid': promo.promotion_uid,
                    'title': promo.title,
                    'description': promo.description,
                    'discount_type': promo.discount_type,
                    'discount_value': promo.discount_value,
                    'min_purchase': promo.min_purchase,
                    'max_discount': promo.max_discount,
                    'start_date': promo.start_date.isoformat() if promo.start_date else None,
                    'end_date': promo.end_date.isoformat() if promo.end_date else None,
                    'store_id': promo.store_id,
                    'product_id': promo.product_id,
                    'category_id': promo.category_id,
                    'is_featured': promo.is_featured
                }
                
                # Ajouter les informations du magasin si disponible
                if promo.store_id:
                    store = ps_stores.query.get(promo.store_id)
                    if store:
                        promo_data['store_name'] = store.store_name
                
                promotions_data.append(promo_data)
            
            return {
                "status": "success",
                "active_promotions": promotions_data,
                "total": len(promotions_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions actives: {str(e)}")
            return {"error": "Erreur lors de la récupération des promotions actives"}, 500
    
    def _get_featured_promotions(self):
        """Récupère les promotions mises en avant"""
        try:
            featured_promotions = PromoDealsHelper.get_featured_promotions()
            
            promotions_data = []
            for promo in featured_promotions:
                promo_data = {
                    'id': promo.id,
                    'promotion_uid': promo.promotion_uid,
                    'title': promo.title,
                    'description': promo.description,
                    'discount_type': promo.discount_type,
                    'discount_value': promo.discount_value,
                    'min_purchase': promo.min_purchase,
                    'max_discount': promo.max_discount,
                    'start_date': promo.start_date.isoformat() if promo.start_date else None,
                    'end_date': promo.end_date.isoformat() if promo.end_date else None,
                    'store_id': promo.store_id,
                    'product_id': promo.product_id,
                    'category_id': promo.category_id
                }
                
                # Ajouter les informations du magasin si disponible
                if promo.store_id:
                    store = ps_stores.query.get(promo.store_id)
                    if store:
                        promo_data['store_name'] = store.store_name
                
                promotions_data.append(promo_data)
            
            return {
                "status": "success",
                "featured_promotions": promotions_data,
                "total": len(promotions_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions mises en avant: {str(e)}")
            return {"error": "Erreur lors de la récupération des promotions mises en avant"}, 500
    
    def _get_promotions_by_store(self, store_id):
        """Récupère les promotions d'un magasin spécifique"""
        try:
            promotions = ps_promotions.query.filter(
                ps_promotions.store_id == store_id,
                ps_promotions.is_active == True
            ).order_by(ps_promotions.creation_date.desc()).all()
            
            promotions_data = []
            for promo in promotions:
                promo_data = {
                    'id': promo.id,
                    'promotion_uid': promo.promotion_uid,
                    'title': promo.title,
                    'description': promo.description,
                    'discount_type': promo.discount_type,
                    'discount_value': promo.discount_value,
                    'min_purchase': promo.min_purchase,
                    'max_discount': promo.max_discount,
                    'start_date': promo.start_date.isoformat() if promo.start_date else None,
                    'end_date': promo.end_date.isoformat() if promo.end_date else None,
                    'is_featured': promo.is_featured
                }
                promotions_data.append(promo_data)
            
            return {
                "status": "success",
                "store_promotions": promotions_data,
                "total": len(promotions_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions du magasin: {str(e)}")
            return {"error": "Erreur lors de la récupération des promotions du magasin"}, 500
    
    def _get_promotions_by_product(self, product_id):
        """Récupère les promotions d'un produit spécifique"""
        try:
            promotions = ps_promotions.query.filter(
                ps_promotions.product_id == product_id,
                ps_promotions.is_active == True
            ).order_by(ps_promotions.creation_date.desc()).all()
            
            promotions_data = []
            for promo in promotions:
                promo_data = {
                    'id': promo.id,
                    'promotion_uid': promo.promotion_uid,
                    'title': promo.title,
                    'description': promo.description,
                    'discount_type': promo.discount_type,
                    'discount_value': promo.discount_value,
                    'min_purchase': promo.min_purchase,
                    'max_discount': promo.max_discount,
                    'start_date': promo.start_date.isoformat() if promo.start_date else None,
                    'end_date': promo.end_date.isoformat() if promo.end_date else None,
                    'is_featured': promo.is_featured
                }
                promotions_data.append(promo_data)
            
            return {
                "status": "success",
                "product_promotions": promotions_data,
                "total": len(promotions_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions du produit: {str(e)}")
            return {"error": "Erreur lors de la récupération des promotions du produit"}, 500
    
    def _get_promotions_by_category(self, category_id):
        """Récupère les promotions d'une catégorie spécifique"""
        try:
            promotions = ps_promotions.query.filter(
                ps_promotions.category_id == category_id,
                ps_promotions.is_active == True
            ).order_by(ps_promotions.creation_date.desc()).all()
            
            promotions_data = []
            for promo in promotions:
                promo_data = {
                    'id': promo.id,
                    'promotion_uid': promo.promotion_uid,
                    'title': promo.title,
                    'description': promo.description,
                    'discount_type': promo.discount_type,
                    'discount_value': promo.discount_value,
                    'min_purchase': promo.min_purchase,
                    'max_discount': promo.max_discount,
                    'start_date': promo.start_date.isoformat() if promo.start_date else None,
                    'end_date': promo.end_date.isoformat() if promo.end_date else None,
                    'is_featured': promo.is_featured
                }
                promotions_data.append(promo_data)
            
            return {
                "status": "success",
                "category_promotions": promotions_data,
                "total": len(promotions_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions de la catégorie: {str(e)}")
            return {"error": "Erreur lors de la récupération des promotions de la catégorie"}, 500
    
    def _create_promotion(self):
        """Crée une nouvelle promotion"""
        try:
            data = request.get_json()
            
            # Validation des données requises
            required_fields = ['title', 'description', 'discount_type', 'discount_value', 'start_date', 'end_date']
            for field in required_fields:
                if field not in data:
                    return {"error": f"Champ requis manquant: {field}"}, 400
            
            # Conversion des dates
            try:
                start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
                end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
            except ValueError:
                return {"error": "Format de date invalide. Utilisez ISO 8601 (YYYY-MM-DDTHH:MM:SS)"}, 400
            
            # Création de la promotion
            promotion = PromoDealsHelper.create_promotion(
                title=data['title'],
                description=data['description'],
                discount_type=data['discount_type'],
                discount_value=float(data['discount_value']),
                start_date=start_date,
                end_date=end_date,
                store_id=data.get('store_id'),
                product_id=data.get('product_id'),
                category_id=data.get('category_id'),
                min_purchase=float(data.get('min_purchase', 0)),
                max_discount=float(data.get('max_discount')) if data.get('max_discount') else None,
                is_featured=bool(data.get('is_featured', False))
            )
            
            if not promotion:
                return {"error": "Erreur lors de la création de la promotion"}, 500
            
            return {
                "status": "success",
                "message": "Promotion créée avec succès",
                "promotion_id": promotion.id,
                "promotion_uid": promotion.promotion_uid
            }, 201
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la promotion: {str(e)}")
            return {"error": "Erreur lors de la création de la promotion"}, 500
    
    def _update_promotion(self, promotion_id):
        """Met à jour une promotion"""
        try:
            data = request.get_json()
            
            # Vérifier que la promotion existe
            promotion = ps_promotions.query.get(promotion_id)
            if not promotion:
                return {"error": "Promotion non trouvée"}, 404
            
            # Mise à jour des champs
            update_fields = ['title', 'description', 'discount_type', 'discount_value', 
                           'start_date', 'end_date', 'min_purchase', 'max_discount', 
                           'is_featured', 'is_active']
            
            for field in update_fields:
                if field in data:
                    if field in ['start_date', 'end_date'] and data[field]:
                        try:
                            date_value = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                            setattr(promotion, field, date_value)
                        except ValueError:
                            return {"error": f"Format de date invalide pour {field}"}, 400
                    elif field in ['discount_value', 'min_purchase', 'max_discount']:
                        setattr(promotion, field, float(data[field]))
                    elif field in ['is_featured', 'is_active']:
                        setattr(promotion, field, bool(data[field]))
                    else:
                        setattr(promotion, field, data[field])
            
            promotion.updated_on = datetime.utcnow()
            db.session.commit()
            
            return {
                "status": "success",
                "message": "Promotion mise à jour avec succès"
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la promotion: {str(e)}")
            db.session.rollback()
            return {"error": "Erreur lors de la mise à jour de la promotion"}, 500
    
    def _delete_promotion(self, promotion_id):
        """Supprime une promotion"""
        try:
            if PromoDealsHelper.delete_promotion(promotion_id):
                return {
                    "status": "success",
                    "message": "Promotion supprimée avec succès"
                }
            else:
                return {"error": "Erreur lors de la suppression de la promotion"}, 500
                
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la promotion: {str(e)}")
            return {"error": "Erreur lors de la suppression de la promotion"}, 500
