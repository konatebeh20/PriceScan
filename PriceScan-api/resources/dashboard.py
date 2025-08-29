#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📊 API Resource pour les données du dashboard
Gère la récupération des statistiques et données utilisateur
"""

import json
import logging
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource

from config.db import db
from model.PriceScan_db import ps_users, ps_user_profiles, ps_dashboard_stats
from helpers.dashboard_data import DashboardDataHelper

logger = logging.getLogger(__name__)


class DashboardApi(Resource):
    """API Resource pour les données du dashboard"""
    
    def get(self, route):
        """
        GET /api/dashboard/<route>
        
        Routes disponibles:
        - stats/<user_uid>: Statistiques du dashboard pour un utilisateur
        - profile/<user_uid>: Profil utilisateur et résumé
        - activity/<user_uid>: Activité récente de l'utilisateur
        - monthly/<user_uid>/<month>/<year>: Stats mensuelles spécifiques
        """
        try:
            if route.startswith("stats/"):
                user_uid = route.split("/")[1]
                return self._get_user_stats(user_uid)
            elif route.startswith("profile/"):
                user_uid = route.split("/")[1]
                return self._get_user_profile(user_uid)
            elif route.startswith("activity/"):
                user_uid = route.split("/")[1]
                return self._get_user_activity(user_uid)
            elif route.startswith("monthly/"):
                parts = route.split("/")
                if len(parts) == 4:
                    user_uid = parts[1]
                    month = int(parts[2])
                    year = int(parts[3])
                    return self._get_monthly_stats(user_uid, month, year)
                else:
                    return {"error": "Format de route invalide pour monthly"}, 400
            else:
                return {"error": "Route non reconnue"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données dashboard: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
    
    def post(self, route):
        """
        POST /api/dashboard/<route>
        
        Routes disponibles:
        - profile/update/<user_uid>: Met à jour le profil utilisateur
        """
        try:
            if route.startswith("profile/update/"):
                user_uid = route.split("/")[2]
                return self._update_user_profile(user_uid)
            else:
                return {"error": "Route non reconnue"}, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du profil: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
    
    def _get_user_stats(self, user_uid):
        """Récupère les statistiques du dashboard pour un utilisateur"""
        try:
            # Vérifier que l'utilisateur existe
            user = ps_users.query.filter_by(u_uid=user_uid).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}, 404
            
            # Récupérer les stats du mois actuel
            stats = DashboardDataHelper.get_user_dashboard_stats(user_uid)
            
            if not stats:
                return {"error": "Erreur lors de la récupération des statistiques"}, 500
            
            return {
                "status": "success",
                "user_uid": user_uid,
                "stats": stats,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats utilisateur: {str(e)}")
            return {"error": "Erreur lors de la récupération des statistiques"}, 500
    
    def _get_user_profile(self, user_uid):
        """Récupère le profil utilisateur et résumé"""
        try:
            # Vérifier que l'utilisateur existe
            user = ps_users.query.filter_by(u_uid=user_uid).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}, 404
            
            # Récupérer le profil
            profile_summary = DashboardDataHelper.get_user_profile_summary(user_uid)
            
            if not profile_summary:
                return {"error": "Erreur lors de la récupération du profil"}, 500
            
            return {
                "status": "success",
                "user_uid": user_uid,
                "profile": profile_summary,
                "retrieved_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du profil utilisateur: {str(e)}")
            return {"error": "Erreur lors de la récupération du profil"}, 500
    
    def _get_user_activity(self, user_uid):
        """Récupère l'activité récente de l'utilisateur"""
        try:
            # Vérifier que l'utilisateur existe
            user = ps_users.query.filter_by(u_uid=user_uid).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}, 404
            
            # Récupérer l'activité récente
            limit = request.args.get('limit', 10, type=int)
            if limit > 50:  # Limiter à 50 pour éviter la surcharge
                limit = 50
            
            recent_activity = DashboardDataHelper.get_recent_activity(user_uid, limit)
            
            return {
                "status": "success",
                "user_uid": user_uid,
                "recent_activity": recent_activity,
                "total_activities": len(recent_activity),
                "retrieved_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'activité utilisateur: {str(e)}")
            return {"error": "Erreur lors de la récupération de l'activité"}, 500
    
    def _get_monthly_stats(self, user_uid, month, year):
        """Récupère les statistiques mensuelles spécifiques"""
        try:
            # Vérifier que l'utilisateur existe
            user = ps_users.query.filter_by(u_uid=user_uid).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}, 404
            
            # Validation des paramètres
            if month < 1 or month > 12:
                return {"error": "Mois invalide (doit être entre 1 et 12)"}, 400
            
            if year < 2020 or year > 2030:
                return {"error": "Année invalide (doit être entre 2020 et 2030)"}, 400
            
            # Récupérer les stats du mois spécifié
            stats = DashboardDataHelper.get_user_dashboard_stats(user_uid, month, year)
            
            if not stats:
                return {"error": "Erreur lors de la récupération des statistiques mensuelles"}, 500
            
            return {
                "status": "success",
                "user_uid": user_uid,
                "month": month,
                "year": year,
                "stats": stats,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats mensuelles: {str(e)}")
            return {"error": "Erreur lors de la récupération des statistiques mensuelles"}, 500
    
    def _update_user_profile(self, user_uid):
        """Met à jour le profil utilisateur"""
        try:
            # Vérifier que l'utilisateur existe
            user = ps_users.query.filter_by(u_uid=user_uid).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}, 404
            
            data = request.get_json()
            if not data:
                return {"error": "Données de mise à jour manquantes"}, 400
            
            # Validation des champs
            allowed_fields = [
                'birth_date', 'gender', 'preferred_currency', 
                'preferred_language', 'notification_preferences'
            ]
            
            profile_data = {}
            for field in allowed_fields:
                if field in data:
                    if field == 'birth_date' and data[field]:
                        try:
                            # Convertir la date ISO en objet date
                            birth_date = datetime.fromisoformat(data[field].replace('Z', '+00:00')).date()
                            profile_data[field] = birth_date
                        except ValueError:
                            return {"error": "Format de date de naissance invalide"}, 400
                    elif field == 'notification_preferences':
                        # Valider que c'est un JSON valide
                        try:
                            json.dumps(data[field])
                            profile_data[field] = json.dumps(data[field])
                        except (TypeError, ValueError):
                            return {"error": "Préférences de notification invalides"}, 400
                    else:
                        profile_data[field] = data[field]
            
            # Mettre à jour le profil
            if profile_data:
                success = DashboardDataHelper.update_user_profile(user_uid, profile_data)
                if success:
                    return {
                        "status": "success",
                        "message": "Profil mis à jour avec succès",
                        "updated_fields": list(profile_data.keys())
                    }
                else:
                    return {"error": "Erreur lors de la mise à jour du profil"}, 500
            else:
                return {"error": "Aucun champ valide à mettre à jour"}, 400
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du profil: {str(e)}")
            return {"error": "Erreur lors de la mise à jour du profil"}, 500
    
    def _get_dashboard_overview(self, user_uid):
        """Récupère un aperçu complet du dashboard"""
        try:
            # Vérifier que l'utilisateur existe
            user = ps_users.query.filter_by(u_uid=user_uid).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}, 404
            
            # Récupérer toutes les données en parallèle
            current_stats = DashboardDataHelper.get_user_dashboard_stats(user_uid)
            profile_summary = DashboardDataHelper.get_user_profile_summary(user_uid)
            recent_activity = DashboardDataHelper.get_recent_activity(user_uid, 5)
            
            # Calculer les tendances (comparaison avec le mois précédent)
            current_month = datetime.utcnow().month
            current_year = datetime.utcnow().year
            
            if current_month == 1:
                prev_month = 12
                prev_year = current_year - 1
            else:
                prev_month = current_month - 1
                prev_year = current_year
            
            previous_stats = DashboardDataHelper.get_user_dashboard_stats(user_uid, prev_month, prev_year)
            
            # Calculer les variations
            trends = {}
            if current_stats and previous_stats:
                if previous_stats.get('total_spent', 0) > 0:
                    spending_change = ((current_stats.get('total_spent', 0) - previous_stats.get('total_spent', 0)) / 
                                    previous_stats.get('total_spent', 0)) * 100
                    trends['spending_change_percent'] = round(spending_change, 2)
                else:
                    trends['spending_change_percent'] = 0
                
                trends['receipts_change'] = current_stats.get('total_receipts', 0) - previous_stats.get('total_receipts', 0)
                trends['avg_receipt_change'] = current_stats.get('avg_receipt_amount', 0) - previous_stats.get('avg_receipt_amount', 0)
            
            return {
                "status": "success",
                "user_uid": user_uid,
                "dashboard_overview": {
                    "current_month": {
                        "month": current_month,
                        "year": current_year,
                        "stats": current_stats
                    },
                    "previous_month": {
                        "month": prev_month,
                        "year": prev_year,
                        "stats": previous_stats
                    },
                    "trends": trends,
                    "profile": profile_summary,
                    "recent_activity": recent_activity
                },
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'aperçu dashboard: {str(e)}")
            return {"error": "Erreur lors de la récupération de l'aperçu dashboard"}, 500
