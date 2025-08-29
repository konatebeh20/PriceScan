#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📊 Helper pour les données du dashboard
Gère l'agrégation et la récupération des statistiques utilisateur
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from sqlalchemy import func, extract, and_

from config.db import db
from model.PriceScan_db import (
    ps_users, ps_receipt, ps_receipt_items, ps_categories, 
    ps_stores, ps_prices, ps_dashboard_stats, ps_user_profiles
)

logger = logging.getLogger(__name__)


class DashboardDataHelper:
    """Helper pour la gestion des données du dashboard"""
    
    @staticmethod
    def get_user_dashboard_stats(user_uid: str, month: int = None, year: int = None) -> Dict:
        """
        Récupère les statistiques du dashboard pour un utilisateur
        
        Args:
            user_uid: UID de l'utilisateur
            month: Mois (1-12), si None utilise le mois actuel
            year: Année, si None utilise l'année actuelle
            
        Returns:
            Dictionnaire avec les statistiques
        """
        try:
            if month is None:
                month = datetime.utcnow().month
            if year is None:
                year = datetime.utcnow().year
            
            # Vérifier si les stats existent déjà
            existing_stats = ps_dashboard_stats.query.filter(
                ps_dashboard_stats.user_uid == user_uid,
                ps_dashboard_stats.month == month,
                ps_dashboard_stats.year == year
            ).first()
            
            if existing_stats:
                # Retourner les stats existantes
                return {
                    'total_receipts': existing_stats.total_receipts,
                    'total_spent': existing_stats.total_spent,
                    'avg_receipt_amount': existing_stats.avg_receipt_amount,
                    'top_categories': json.loads(existing_stats.top_categories) if existing_stats.top_categories else [],
                    'top_stores': json.loads(existing_stats.top_stores) if existing_stats.top_stores else [],
                    'total_savings': existing_stats.total_savings,
                    'savings_from_promos': existing_stats.savings_from_promos,
                    'savings_from_comparison': existing_stats.savings_from_comparison
                }
            
            # Calculer les stats en temps réel
            stats = DashboardDataHelper._calculate_real_time_stats(user_uid, month, year)
            
            # Sauvegarder les stats calculées
            DashboardDataHelper._save_dashboard_stats(user_uid, month, year, stats)
            
            return stats
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats dashboard: {str(e)}")
            return {}
    
    @staticmethod
    def _calculate_real_time_stats(user_uid: str, month: int, year: int) -> Dict:
        """Calcule les statistiques en temps réel"""
        try:
            # Date de début et fin du mois
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
            
            # Total des reçus et montants
            receipts_query = ps_receipt.query.filter(
                ps_receipt.u_uid == user_uid,
                ps_receipt.purchase_date >= start_date,
                ps_receipt.purchase_date <= end_date
            )
            
            total_receipts = receipts_query.count()
            total_spent = receipts_query.with_entities(func.sum(ps_receipt.total_amount)).scalar() or 0.0
            avg_receipt_amount = total_spent / total_receipts if total_receipts > 0 else 0.0
            
            # Top catégories
            top_categories = DashboardDataHelper._get_top_categories(user_uid, start_date, end_date)
            
            # Top magasins
            top_stores = DashboardDataHelper._get_top_stores(user_uid, start_date, end_date)
            
            # Économies (à calculer selon la logique métier)
            total_savings = DashboardDataHelper._calculate_total_savings(user_uid, start_date, end_date)
            
            return {
                'total_receipts': total_receipts,
                'total_spent': total_spent,
                'avg_receipt_amount': avg_receipt_amount,
                'top_categories': top_categories,
                'top_stores': top_stores,
                'total_savings': total_savings,
                'savings_from_promos': 0.0,  # À implémenter
                'savings_from_comparison': 0.0  # À implémenter
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul des stats temps réel: {str(e)}")
            return {}
    
    @staticmethod
    def _get_top_categories(user_uid: str, start_date: datetime, end_date: datetime, limit: int = 5) -> List[Dict]:
        """Récupère les catégories les plus achetées"""
        try:
            # Jointure entre reçus, articles et catégories
            categories_query = db.session.query(
                ps_categories.cat_label,
                func.sum(ps_receipt_items.total_price).label('total_spent'),
                func.count(ps_receipt_items.id).label('purchase_count')
            ).join(
                ps_receipt_items, ps_receipt_items.category_uid == ps_categories.cat_uid
            ).join(
                ps_receipt, ps_receipt.receipt_uid == ps_receipt_items.receipt_uid
            ).filter(
                ps_receipt.u_uid == user_uid,
                ps_receipt.purchase_date >= start_date,
                ps_receipt.purchase_date <= end_date
            ).group_by(
                ps_categories.cat_label
            ).order_by(
                func.sum(ps_receipt_items.total_price).desc()
            ).limit(limit)
            
            return [
                {
                    'category': row.cat_label,
                    'total_spent': float(row.total_spent),
                    'purchase_count': row.purchase_count
                }
                for row in categories_query.all()
            ]
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des top catégories: {str(e)}")
            return []
    
    @staticmethod
    def _get_top_stores(user_uid: str, start_date: datetime, end_date: datetime, limit: int = 5) -> List[Dict]:
        """Récupère les magasins les plus fréquentés"""
        try:
            stores_query = db.session.query(
                ps_receipt.store_name,
                func.sum(ps_receipt.total_amount).label('total_spent'),
                func.count(ps_receipt.id).label('visit_count')
            ).filter(
                ps_receipt.u_uid == user_uid,
                ps_receipt.purchase_date >= start_date,
                ps_receipt.purchase_date <= end_date
            ).group_by(
                ps_receipt.store_name
            ).order_by(
                func.sum(ps_receipt.total_amount).desc()
            ).limit(limit)
            
            return [
                {
                    'store_name': row.store_name,
                    'total_spent': float(row.total_spent),
                    'visit_count': row.visit_count
                }
                for row in stores_query.all()
            ]
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des top magasins: {str(e)}")
            return []
    
    @staticmethod
    def _calculate_total_savings(user_uid: str, start_date: datetime, end_date: datetime) -> float:
        """Calcule le total des économies réalisées"""
        try:
            # Logique pour calculer les économies
            # Pour l'instant, retourne 0
            # À implémenter selon la logique métier
            return 0.0
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul des économies: {str(e)}")
            return 0.0
    
    @staticmethod
    def _save_dashboard_stats(user_uid: str, month: int, year: int, stats: Dict) -> bool:
        """Sauvegarde les statistiques du dashboard"""
        try:
            # Vérifier si les stats existent déjà
            existing_stats = ps_dashboard_stats.query.filter(
                ps_dashboard_stats.user_uid == user_uid,
                ps_dashboard_stats.month == month,
                ps_dashboard_stats.year == year
            ).first()
            
            if existing_stats:
                # Mettre à jour les stats existantes
                existing_stats.total_receipts = stats.get('total_receipts', 0)
                existing_stats.total_spent = stats.get('total_spent', 0.0)
                existing_stats.avg_receipt_amount = stats.get('avg_receipt_amount', 0.0)
                existing_stats.top_categories = json.dumps(stats.get('top_categories', []))
                existing_stats.top_stores = json.dumps(stats.get('top_stores', []))
                existing_stats.total_savings = stats.get('total_savings', 0.0)
                existing_stats.savings_from_promos = stats.get('savings_from_promos', 0.0)
                existing_stats.savings_from_comparison = stats.get('savings_from_comparison', 0.0)
                existing_stats.updated_on = datetime.utcnow()
            else:
                # Créer de nouvelles stats
                new_stats = ps_dashboard_stats(
                    user_uid=user_uid,
                    month=month,
                    year=year,
                    total_receipts=stats.get('total_receipts', 0),
                    total_spent=stats.get('total_spent', 0.0),
                    avg_receipt_amount=stats.get('avg_receipt_amount', 0.0),
                    top_categories=json.dumps(stats.get('top_categories', [])),
                    top_stores=json.dumps(stats.get('top_stores', [])),
                    total_savings=stats.get('total_savings', 0.0),
                    savings_from_promos=stats.get('savings_from_promos', 0.0),
                    savings_from_comparison=stats.get('savings_from_comparison', 0.0)
                )
                db.session.add(new_stats)
            
            db.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des stats dashboard: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_user_profile_summary(user_uid: str) -> Dict:
        """Récupère un résumé du profil utilisateur"""
        try:
            user = ps_users.query.filter_by(u_uid=user_uid).first()
            if not user:
                return {}
            
            profile = ps_user_profiles.query.filter_by(user_uid=user_uid).first()
            
            # Statistiques globales
            total_receipts = ps_receipt.query.filter_by(u_uid=user_uid).count()
            total_spent = ps_receipt.query.with_entities(
                func.sum(ps_receipt.total_amount)
            ).filter_by(u_uid=user_uid).scalar() or 0.0
            
            # Dernière activité
            last_receipt = ps_receipt.query.filter_by(u_uid=user_uid).order_by(
                ps_receipt.purchase_date.desc()
            ).first()
            
            return {
                'user_info': {
                    'username': user.u_username,
                    'email': user.u_email,
                    'firstname': user.u_firstname,
                    'lastname': user.u_lastname
                },
                'profile': {
                    'birth_date': profile.birth_date.isoformat() if profile and profile.birth_date else None,
                    'gender': profile.gender if profile else None,
                    'preferred_currency': profile.preferred_currency if profile else 'CFA',
                    'preferred_language': profile.preferred_language if profile else 'fr'
                },
                'stats': {
                    'total_receipts': total_receipts,
                    'total_spent': float(total_spent),
                    'last_activity': last_receipt.purchase_date.isoformat() if last_receipt else None
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du profil utilisateur: {str(e)}")
            return {}
    
    @staticmethod
    def get_recent_activity(user_uid: str, limit: int = 10) -> List[Dict]:
        """Récupère l'activité récente de l'utilisateur"""
        try:
            recent_receipts = ps_receipt.query.filter_by(
                u_uid=user_uid
            ).order_by(
                ps_receipt.purchase_date.desc()
            ).limit(limit).all()
            
            activity = []
            for receipt in recent_receipts:
                activity.append({
                    'type': 'receipt',
                    'id': receipt.receipt_uid,
                    'store_name': receipt.store_name,
                    'amount': float(receipt.total_amount),
                    'date': receipt.purchase_date.isoformat(),
                    'currency': receipt.currency
                })
            
            return activity
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'activité récente: {str(e)}")
            return []
    
    @staticmethod
    def update_user_profile(user_uid: str, profile_data: Dict) -> bool:
        """Met à jour le profil utilisateur"""
        try:
            profile = ps_user_profiles.query.filter_by(user_uid=user_uid).first()
            
            if not profile:
                # Créer un nouveau profil
                profile = ps_user_profiles(user_uid=user_uid)
                db.session.add(profile)
            
            # Mettre à jour les champs
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            profile.updated_on = datetime.utcnow()
            db.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du profil: {str(e)}")
            db.session.rollback()
            return False
