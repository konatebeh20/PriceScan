import json
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime

from config.constant import *
from config.db import db
from model.PriceScan_db import ps_receipt, ps_receipt_items, ps_users, ps_categories


class ReceiptsApi(Resource):
    def get(self, route):
        if route == 'all':
            return self.get_all_receipts()
        elif route == 'by_user':
            user_uid = request.args.get('user_uid')
            return self.get_receipts_by_user(user_uid)
        elif route == 'by_store':
            store_name = request.args.get('store_name')
            return self.get_receipts_by_store(store_name)
        elif route == 'by_date_range':
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            return self.get_receipts_by_date_range(start_date, end_date)
        elif route == 'stats':
            user_uid = request.args.get('user_uid')
            return self.get_receipt_stats(user_uid)
        else:
            return {'error': 'Route invalide'}, 400
        
    def post(self, route):
        if route == 'create':
            return self.create_receipt()
        elif route == 'scan':
            return self.scan_receipt()
        else:
            return {'error': 'Route invalide'}, 400
        
    def patch(self, route):
        if route == 'update':
            return self.update_receipt()
        elif route == 'verify':
            return self.verify_receipt()
        elif route == 'reject':
            return self.reject_receipt()
        else:
            return {'error': 'Route invalide'}, 400
        
    def delete(self, route):
        if route == 'delete':
            return self.delete_receipt()
        else:
            return {'error': 'Route invalide'}, 400

    def get_all_receipts(self):
        try:
            receipts = ps_receipt.query.all()
            receipts_list = []
            for receipt in receipts:
                # Récupérer les informations de l'utilisateur
                user = ps_users.query.filter_by(u_uid=receipt.u_uid).first()
                user_info = {
                    'username': user.u_username if user else 'Utilisateur inconnu',
                    'full_name': f"{user.u_firstname} {user.u_lastname}" if user else None
                } if user else None
                
                receipts_list.append({
                    'id': receipt.id,
                    'receipt_uid': receipt.receipt_uid,
                    'user_info': user_info,
                    'store_name': receipt.store_name,
                    'store_address': receipt.store_address,
                    'purchase_date': receipt.purchase_date.isoformat() if receipt.purchase_date else None,
                    'total_amount': receipt.total_amount,
                    'currency': receipt.currency,
                    'receipt_image': receipt.receipt_image,
                    'status': receipt.status,
                    'created_at': receipt.created_at.isoformat() if receipt.created_at else None,
                    'updated_at': receipt.updated_at.isoformat() if receipt.updated_at else None
                })
            return {'receipts': receipts_list, 'count': len(receipts_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_receipts_by_user(self, user_uid):
        try:
            if not user_uid:
                return {'error': 'user_uid requis'}, 400
            
            receipts = ps_receipt.query.filter_by(u_uid=user_uid).order_by(ps_receipt.created_at.desc()).all()
            
            receipts_list = []
            for receipt in receipts:
                receipts_list.append({
                    'id': receipt.id,
                    'receipt_uid': receipt.receipt_uid,
                    'store_name': receipt.store_name,
                    'store_address': receipt.store_address,
                    'purchase_date': receipt.purchase_date.isoformat() if receipt.purchase_date else None,
                    'total_amount': receipt.total_amount,
                    'currency': receipt.currency,
                    'receipt_image': receipt.receipt_image,
                    'status': receipt.status,
                    'created_at': receipt.created_at.isoformat() if receipt.created_at else None
                })
            return {'receipts': receipts_list, 'count': len(receipts_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_receipts_by_store(self, store_name):
        try:
            if not store_name:
                return {'error': 'store_name requis'}, 400
            
            receipts = ps_receipt.query.filter(
                ps_receipt.store_name.ilike(f'%{store_name}%')
            ).order_by(ps_receipt.created_at.desc()).all()
            
            receipts_list = []
            for receipt in receipts:
                receipts_list.append({
                    'id': receipt.id,
                    'receipt_uid': receipt.receipt_uid,
                    'store_name': receipt.store_name,
                    'store_address': receipt.store_address,
                    'purchase_date': receipt.purchase_date.isoformat() if receipt.purchase_date else None,
                    'total_amount': receipt.total_amount,
                    'currency': receipt.currency,
                    'status': receipt.status,
                    'created_at': receipt.created_at.isoformat() if receipt.created_at else None
                })
            return {'receipts': receipts_list, 'count': len(receipts_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_receipts_by_date_range(self, start_date, end_date):
        try:
            if not start_date or not end_date:
                return {'error': 'start_date et end_date requis'}, 400
            
            try:
                start = datetime.fromisoformat(start_date)
                end = datetime.fromisoformat(end_date)
            except ValueError:
                return {'error': 'Format de date invalide. Utilisez ISO format (YYYY-MM-DD)'}, 400
            
            receipts = ps_receipt.query.filter(
                ps_receipt.created_at >= start,
                ps_receipt.created_at <= end
            ).order_by(ps_receipt.created_at.desc()).all()
            
            receipts_list = []
            for receipt in receipts:
                receipts_list.append({
                    'id': receipt.id,
                    'receipt_uid': receipt.receipt_uid,
                    'store_name': receipt.store_name,
                    'total_amount': receipt.total_amount,
                    'currency': receipt.currency,
                    'status': receipt.status,
                    'created_at': receipt.created_at.isoformat() if receipt.created_at else None
                })
            return {'receipts': receipts_list, 'count': len(receipts_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_receipt_stats(self, user_uid):
        try:
            if not user_uid:
                return {'error': 'user_uid requis'}, 400
            
            # Statistiques des reçus de l'utilisateur
            total_receipts = ps_receipt.query.filter_by(u_uid=user_uid).count()
            total_amount = db.session.query(func.sum(ps_receipt.total_amount)).filter_by(u_uid=user_uid).scalar() or 0
            
            # Reçus par statut
            pending_receipts = ps_receipt.query.filter_by(u_uid=user_uid, status='pending').count()
            verified_receipts = ps_receipt.query.filter_by(u_uid=user_uid, status='verified').count()
            rejected_receipts = ps_receipt.query.filter_by(u_uid=user_uid, status='rejected').count()
            
            # Reçus par magasin (top 5)
            store_stats = db.session.query(
                ps_receipt.store_name,
                func.count(ps_receipt.id).label('count'),
                func.sum(ps_receipt.total_amount).label('total')
            ).filter_by(u_uid=user_uid).group_by(ps_receipt.store_name).order_by(
                func.count(ps_receipt.id).desc()
            ).limit(5).all()
            
            store_list = []
            for store in store_stats:
                store_list.append({
                    'store_name': store.store_name,
                    'receipt_count': store.count,
                    'total_amount': float(store.total) if store.total else 0
                })
            
            return {
                'total_receipts': total_receipts,
                'total_amount': float(total_amount),
                'status_breakdown': {
                    'pending': pending_receipts,
                    'verified': verified_receipts,
                    'rejected': rejected_receipts
                },
                'top_stores': store_list
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

    def create_receipt(self):
        try:
            data = request.get_json()
            
            # Validation des données requises
            required_fields = ['u_uid', 'store_name', 'total_amount']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Champ requis: {field}'}, 400
            
            # Vérification de l'existence de l'utilisateur
            user = ps_users.query.filter_by(u_uid=data['u_uid']).first()
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404
            
            # Création du reçu
            new_receipt = ps_receipt(
                u_uid=data['u_uid'],
                store_name=data['store_name'],
                store_address=data.get('store_address'),
                purchase_date=data.get('purchase_date'),
                total_amount=data['total_amount'],
                currency=data.get('currency', 'CFA'),
                receipt_image=data.get('receipt_image'),
                status=data.get('status', 'pending')
            )
            
            db.session.add(new_receipt)
            db.session.commit()
            
            return {
                'message': 'Reçu créé avec succès',
                'receipt_uid': new_receipt.receipt_uid
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def scan_receipt(self):
        try:
            data = request.get_json()
            
            # Validation des données requises
            required_fields = ['u_uid', 'receipt_image']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Champ requis: {field}'}, 400
            
            # Vérification de l'existence de l'utilisateur
            user = ps_users.query.filter_by(u_uid=data['u_uid']).first()
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404
            
            # Ici, vous pouvez ajouter la logique OCR pour extraire les informations du reçu
            # Pour l'instant, on crée un reçu avec les données de base
            new_receipt = ps_receipt(
                u_uid=data['u_uid'],
                store_name=data.get('store_name', 'Magasin à identifier'),
                store_address=data.get('store_address'),
                purchase_date=data.get('purchase_date'),
                total_amount=data.get('total_amount', 0.0),
                currency=data.get('currency', 'CFA'),
                receipt_image=data['receipt_image'],
                status='pending'
            )
            
            db.session.add(new_receipt)
            db.session.commit()
            
            return {
                'message': 'Reçu scanné et créé avec succès',
                'receipt_uid': new_receipt.receipt_uid,
                'status': 'pending',
                'note': 'Le reçu a été créé et est en attente de vérification manuelle'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def update_receipt(self):
        try:
            data = request.get_json()
            receipt_uid = data.get('receipt_uid')
            
            if not receipt_uid:
                return {'error': 'receipt_uid requis'}, 400
            
            receipt = ps_receipt.query.filter_by(receipt_uid=receipt_uid).first()
            if not receipt:
                return {'error': 'Reçu non trouvé'}, 404
            
            # Mise à jour des champs
            if 'store_name' in data:
                receipt.store_name = data['store_name']
            if 'store_address' in data:
                receipt.store_address = data['store_address']
            if 'purchase_date' in data:
                receipt.purchase_date = data['purchase_date']
            if 'total_amount' in data:
                receipt.total_amount = data['total_amount']
            if 'currency' in data:
                receipt.currency = data['currency']
            if 'receipt_image' in data:
                receipt.receipt_image = data['receipt_image']
            
            db.session.commit()
            
            return {'message': 'Reçu mis à jour avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def verify_receipt(self):
        try:
            data = request.get_json()
            receipt_uid = data.get('receipt_uid')
            
            if not receipt_uid:
                return {'error': 'receipt_uid requis'}, 400
            
            receipt = ps_receipt.query.filter_by(receipt_uid=receipt_uid).first()
            if not receipt:
                return {'error': 'Reçu non trouvé'}, 404
            
            receipt.status = 'verified'
            db.session.commit()
            
            return {'message': 'Reçu vérifié avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def reject_receipt(self):
        try:
            data = request.get_json()
            receipt_uid = data.get('receipt_uid')
            reason = data.get('reason', 'Rejeté par l\'utilisateur')
            
            if not receipt_uid:
                return {'error': 'receipt_uid requis'}, 400
            
            receipt = ps_receipt.query.filter_by(receipt_uid=receipt_uid).first()
            if not receipt:
                return {'error': 'Reçu non trouvé'}, 404
            
            receipt.status = 'rejected'
            db.session.commit()
            
            return {'message': 'Reçu rejeté avec succès', 'reason': reason}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete_receipt(self):
        try:
            data = request.get_json()
            receipt_uid = data.get('receipt_uid')
            
            if not receipt_uid:
                return {'error': 'receipt_uid requis'}, 400
            
            receipt = ps_receipt.query.filter_by(receipt_uid=receipt_uid).first()
            if not receipt:
                return {'error': 'Reçu non trouvé'}, 404
            
            # Supprimer d'abord les éléments du reçu
            ps_receipt_items.query.filter_by(receipt_uid=receipt_uid).delete()
            
            # Puis supprimer le reçu
            db.session.delete(receipt)
            db.session.commit()
            
            return {'message': 'Reçu supprimé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
