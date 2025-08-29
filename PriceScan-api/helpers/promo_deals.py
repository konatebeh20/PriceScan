#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎯 Helper pour la gestion des promotions et offres spéciales
Gère la création, modification et suppression des promotions
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from config.db import db
from model.PriceScan_db import ps_promotions, ps_stores, ps_products, ps_categories

logger = logging.getLogger(__name__)


class PromoDealsHelper:
    """Helper pour la gestion des promotions"""
    
    @staticmethod
    def create_promotion(
        title: str,
        description: str,
        discount_type: str,
        discount_value: float,
        start_date: datetime,
        end_date: datetime,
        store_id: Optional[int] = None,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        min_purchase: float = 0,
        max_discount: Optional[float] = None,
        is_featured: bool = False
    ) -> Optional[ps_promotions]:
        """
        Crée une nouvelle promotion
        
        Args:
            title: Titre de la promotion
            description: Description détaillée
            discount_type: Type de réduction (percentage, fixed_amount)
            discount_value: Valeur de la réduction
            start_date: Date de début
            end_date: Date de fin
            store_id: ID du magasin (optionnel)
            product_id: ID du produit (optionnel)
            category_id: ID de la catégorie (optionnel)
            min_purchase: Montant minimum d'achat
            max_discount: Réduction maximale
            is_featured: Si la promotion est mise en avant
            
        Returns:
            L'objet promotion créé ou None en cas d'erreur
        """
        try:
            # Validation des dates
            if start_date >= end_date:
                logger.error("La date de début doit être antérieure à la date de fin")
                return None
            
            # Validation du type de réduction
            if discount_type not in ['percentage', 'fixed_amount']:
                logger.error("Type de réduction invalide")
                return None
            
            # Validation de la valeur de réduction
            if discount_value <= 0:
                logger.error("La valeur de réduction doit être positive")
                return None
            
            # Création de la promotion
            promotion = ps_promotions(
                title=title,
                description=description,
                discount_type=discount_type,
                discount_value=discount_value,
                start_date=start_date,
                end_date=end_date,
                store_id=store_id,
                product_id=product_id,
                category_id=category_id,
                min_purchase=min_purchase,
                max_discount=max_discount,
                is_featured=is_featured
            )
            
            db.session.add(promotion)
            db.session.commit()
            
            logger.info(f"Promotion '{title}' créée avec succès")
            return promotion
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la promotion: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_active_promotions(
        store_id: Optional[int] = None,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        limit: int = 50
    ) -> List[ps_promotions]:
        """
        Récupère les promotions actives
        
        Args:
            store_id: Filtrer par magasin
            product_id: Filtrer par produit
            category_id: Filtrer par catégorie
            limit: Nombre maximum de promotions à retourner
            
        Returns:
            Liste des promotions actives
        """
        try:
            query = ps_promotions.query.filter(
                ps_promotions.is_active == True,
                ps_promotions.start_date <= datetime.utcnow(),
                ps_promotions.end_date >= datetime.utcnow()
            )
            
            if store_id:
                query = query.filter(ps_promotions.store_id == store_id)
            
            if product_id:
                query = query.filter(ps_promotions.product_id == product_id)
            
            if category_id:
                query = query.filter(ps_promotions.category_id == category_id)
            
            return query.order_by(ps_promotions.is_featured.desc(), ps_promotions.creation_date.desc()).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions: {str(e)}")
            return []
    
    @staticmethod
    def get_featured_promotions(limit: int = 10) -> List[ps_promotions]:
        """
        Récupère les promotions mises en avant
        
        Args:
            limit: Nombre maximum de promotions
            
        Returns:
            Liste des promotions mises en avant
        """
        try:
            return ps_promotions.query.filter(
                ps_promotions.is_active == True,
                ps_promotions.is_featured == True,
                ps_promotions.start_date <= datetime.utcnow(),
                ps_promotions.end_date >= datetime.utcnow()
            ).order_by(ps_promotions.creation_date.desc()).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions mises en avant: {str(e)}")
            return []
    
    @staticmethod
    def calculate_discount(
        original_price: float,
        discount_type: str,
        discount_value: float,
        max_discount: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Calcule le montant de la réduction et le prix final
        
        Args:
            original_price: Prix original
            discount_type: Type de réduction
            discount_value: Valeur de la réduction
            max_discount: Réduction maximale
            
        Returns:
            Dictionnaire avec le montant de la réduction et le prix final
        """
        try:
            if discount_type == 'percentage':
                discount_amount = (original_price * discount_value) / 100
                if max_discount:
                    discount_amount = min(discount_amount, max_discount)
            else:  # fixed_amount
                discount_amount = min(discount_value, original_price)
            
            final_price = original_price - discount_amount
            
            return {
                'original_price': original_price,
                'discount_amount': discount_amount,
                'final_price': final_price,
                'discount_percentage': (discount_amount / original_price) * 100
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la réduction: {str(e)}")
            return {
                'original_price': original_price,
                'discount_amount': 0,
                'final_price': original_price,
                'discount_percentage': 0
            }
    
    @staticmethod
    def update_promotion(
        promotion_id: int,
        **kwargs
    ) -> bool:
        """
        Met à jour une promotion
        
        Args:
            promotion_id: ID de la promotion
            **kwargs: Champs à mettre à jour
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        try:
            promotion = ps_promotions.query.get(promotion_id)
            if not promotion:
                logger.error(f"Promotion {promotion_id} non trouvée")
                return False
            
            # Mise à jour des champs
            for key, value in kwargs.items():
                if hasattr(promotion, key):
                    setattr(promotion, key, value)
            
            promotion.updated_on = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Promotion {promotion_id} mise à jour avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la promotion: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_promotion(promotion_id: int) -> bool:
        """
        Supprime une promotion (désactivation logique)
        
        Args:
            promotion_id: ID de la promotion
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        try:
            promotion = ps_promotions.query.get(promotion_id)
            if not promotion:
                logger.error(f"Promotion {promotion_id} non trouvée")
                return False
            
            promotion.is_active = False
            promotion.updated_on = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Promotion {promotion_id} supprimée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la promotion: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_promotions_by_date_range(
        start_date: datetime,
        end_date: datetime,
        limit: int = 100
    ) -> List[ps_promotions]:
        """
        Récupère les promotions dans une plage de dates
        
        Args:
            start_date: Date de début
            end_date: Date de fin
            limit: Nombre maximum de promotions
            
        Returns:
            Liste des promotions dans la plage de dates
        """
        try:
            return ps_promotions.query.filter(
                ps_promotions.is_active == True,
                ps_promotions.start_date <= end_date,
                ps_promotions.end_date >= start_date
            ).order_by(ps_promotions.start_date.asc()).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des promotions par date: {str(e)}")
            return []