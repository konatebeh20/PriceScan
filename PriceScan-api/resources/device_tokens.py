#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API pour la gestion des tokens de dispositifs mobiles
Gère les notifications push pour les utilisateurs
"""

from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db
from model.PriceScan_db import ps_device_tokens, ps_users

class DeviceTokens(Resource):
    """API pour la gestion des tokens de dispositifs"""
    
    def get(self, route):
        """Récupérer les tokens de dispositifs"""
        try:
            if route == "all":
                # Récupérer tous les tokens (admin seulement)
                tokens = ps_device_tokens.query.all()
                return {
                    "response": "success",
                    "tokens": [token.to_dict() for token in tokens]
                }
            
            elif route == "user":
                # Récupérer les tokens d'un utilisateur spécifique
                user_id = request.args.get('user_id')
                if not user_id:
                    return {"response": "error", "message": "user_id required"}, 400
                
                tokens = ps_device_tokens.query.filter_by(user_id=user_id).all()
                return {
                    "response": "success",
                    "tokens": [token.to_dict() for token in tokens]
                }
            
            else:
                return {"response": "error", "message": "Invalid route"}, 400
                
        except SQLAlchemyError as e:
            return {"response": "error", "message": str(e)}, 500
    
    def post(self, route):
        """Créer ou mettre à jour un token de dispositif"""
        try:
            if route == "create":
                data = request.get_json()
                
                # Vérifier les données requises
                required_fields = ['user_id', 'device_token', 'platform']
                for field in required_fields:
                    if field not in data:
                        return {"response": "error", "message": f"{field} required"}, 400
                
                # Vérifier si l'utilisateur existe
                user = ps_users.query.filter_by(user_id=data['user_id']).first()
                if not user:
                    return {"response": "error", "message": "User not found"}, 404
                
                # Vérifier si le token existe déjà
                existing_token = ps_device_tokens.query.filter_by(
                    user_id=data['user_id'],
                    device_token=data['device_token']
                ).first()
                
                if existing_token:
                    # Mettre à jour le token existant
                    existing_token.platform = data['platform']
                    existing_token.is_active = True
                    existing_token.last_used = func.now()
                    db.session.add(existing_token)
                else:
                    # Créer un nouveau token
                    new_token = ps_device_tokens()
                    new_token.user_id = data['user_id']
                    new_token.device_token = data['device_token']
                    new_token.platform = data['platform']
                    new_token.is_active = True
                    new_token.created_at = func.now()
                    new_token.last_used = func.now()
                    db.session.add(new_token)
                
                db.session.commit()
                
                return {
                    "response": "success",
                    "message": "Device token registered successfully"
                }
            
            elif route == "update":
                data = request.get_json()
                token_id = data.get('token_id')
                
                if not token_id:
                    return {"response": "error", "message": "token_id required"}, 400
                
                token = ps_device_tokens.query.filter_by(token_id=token_id).first()
                if not token:
                    return {"response": "error", "message": "Token not found"}, 404
                
                # Mettre à jour les champs fournis
                if 'platform' in data:
                    token.platform = data['platform']
                if 'is_active' in data:
                    token.is_active = data['is_active']
                
                token.last_used = func.now()
                db.session.add(token)
                db.session.commit()
                
                return {
                    "response": "success",
                    "message": "Device token updated successfully"
                }
            
            else:
                return {"response": "error", "message": "Invalid route"}, 400
                
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"response": "error", "message": str(e)}, 500
    
    def patch(self, route):
        """Mettre à jour partiellement un token"""
        return self.post(route)
    
    def delete(self, route):
        """Supprimer un token de dispositif"""
        try:
            if route == "delete":
                data = request.get_json()
                token_id = data.get('token_id')
                
                if not token_id:
                    return {"response": "error", "message": "token_id required"}, 400
                
                token = ps_device_tokens.query.filter_by(token_id=token_id).first()
                if not token:
                    return {"response": "error", "message": "Token not found"}, 404
                
                # Soft delete - désactiver le token
                token.is_active = False
                token.deleted_at = func.now()
                db.session.add(token)
                db.session.commit()
                
                return {
                    "response": "success",
                    "message": "Device token deactivated successfully"
                }
            
            else:
                return {"response": "error", "message": "Invalid route"}, 400
                
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"response": "error", "message": str(e)}, 500
