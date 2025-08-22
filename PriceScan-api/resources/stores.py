import json
from flask import request
from flask_restful import Resource
from sqlalchemy import func

from config.constant import *
from config.db import db
from model.PriceScan_db import ps_stores


class StoresApi(Resource):
    def get(self, route):
        if route == 'all':
            return self.get_all_stores()
        elif route == 'active':
            return self.get_active_stores()
        elif route == 'by_city':
            city = request.args.get('city')
            return self.get_stores_by_city(city)
        else:
            return {'error': 'Route invalide'}, 400
        
    def post(self, route):
        if route == 'create':
            return self.create_store()
        else:
            return {'error': 'Route invalide'}, 400
        
    def patch(self, route):
        if route == 'update':
            return self.update_store()
        elif route == 'activate':
            return self.activate_store()
        elif route == 'deactivate':
            return self.deactivate_store()
        else:
            return {'error': 'Route invalide'}, 400
        
    def delete(self, route):
        if route == 'delete':
            return self.delete_store()
        else:
            return {'error': 'Route invalide'}, 400

    def get_all_stores(self):
        try:
            stores = ps_stores.query.all()
            stores_list = []
            for store in stores:
                stores_list.append({
                    'id': store.id,
                    'store_uid': store.store_uid,
                    'store_name': store.store_name,
                    'store_address': store.store_address,
                    'store_city': store.store_city,
                    'store_country': store.store_country,
                    'store_phone': store.store_phone,
                    'store_email': store.store_email,
                    'store_website': store.store_website,
                    'store_logo': store.store_logo,
                    'store_is_active': store.store_is_active,
                    'creation_date': store.creation_date.isoformat() if store.creation_date else None,
                    'updated_on': store.updated_on.isoformat() if store.updated_on else None
                })
            return {'stores': stores_list, 'count': len(stores_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_active_stores(self):
        try:
            stores = ps_stores.query.filter_by(store_is_active=True).all()
            stores_list = []
            for store in stores:
                stores_list.append({
                    'id': store.id,
                    'store_uid': store.store_uid,
                    'store_name': store.store_name,
                    'store_address': store.store_address,
                    'store_city': store.store_city,
                    'store_country': store.store_country,
                    'store_phone': store.store_phone,
                    'store_email': store.store_email,
                    'store_website': store.store_website,
                    'store_logo': store.store_logo,
                    'creation_date': store.creation_date.isoformat() if store.creation_date else None
                })
            return {'stores': stores_list, 'count': len(stores_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_stores_by_city(self, city):
        try:
            if not city:
                return {'error': 'Ville requise'}, 400
            
            stores = ps_stores.query.filter(
                ps_stores.store_city.ilike(f'%{city}%'),
                ps_stores.store_is_active == True
            ).all()
            
            stores_list = []
            for store in stores:
                stores_list.append({
                    'id': store.id,
                    'store_uid': store.store_uid,
                    'store_name': store.store_name,
                    'store_address': store.store_address,
                    'store_city': store.store_city,
                    'store_country': store.store_country,
                    'store_phone': store.store_phone,
                    'store_email': store.store_email,
                    'store_website': store.store_website,
                    'store_logo': store.store_logo
                })
            return {'stores': stores_list, 'count': len(stores_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def create_store(self):
        try:
            data = request.get_json()
            
            # Validation des données requises
            required_fields = ['store_name', 'store_city']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Champ requis: {field}'}, 400
            
            # Création du magasin
            new_store = ps_stores(
                store_name=data['store_name'],
                store_address=data.get('store_address'),
                store_city=data['store_city'],
                store_country=data.get('store_country', "Côte d'Ivoire"),
                store_phone=data.get('store_phone'),
                store_email=data.get('store_email'),
                store_website=data.get('store_website'),
                store_logo=data.get('store_logo'),
                store_is_active=data.get('store_is_active', True)
            )
            
            db.session.add(new_store)
            db.session.commit()
            
            return {
                'message': 'Magasin créé avec succès',
                'store_uid': new_store.store_uid
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def update_store(self):
        try:
            data = request.get_json()
            store_uid = data.get('store_uid')
            
            if not store_uid:
                return {'error': 'store_uid requis'}, 400
            
            store = ps_stores.query.filter_by(store_uid=store_uid).first()
            if not store:
                return {'error': 'Magasin non trouvé'}, 404
            
            # Mise à jour des champs
            if 'store_name' in data:
                store.store_name = data['store_name']
            if 'store_address' in data:
                store.store_address = data['store_address']
            if 'store_city' in data:
                store.store_city = data['store_city']
            if 'store_country' in data:
                store.store_country = data['store_country']
            if 'store_phone' in data:
                store.store_phone = data['store_phone']
            if 'store_email' in data:
                store.store_email = data['store_email']
            if 'store_website' in data:
                store.store_website = data['store_website']
            if 'store_logo' in data:
                store.store_logo = data['store_logo']
            
            db.session.commit()
            
            return {'message': 'Magasin mis à jour avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def activate_store(self):
        try:
            data = request.get_json()
            store_uid = data.get('store_uid')
            
            if not store_uid:
                return {'error': 'store_uid requis'}, 400
            
            store = ps_stores.query.filter_by(store_uid=store_uid).first()
            if not store:
                return {'error': 'Magasin non trouvé'}, 404
            
            store.store_is_active = True
            db.session.commit()
            
            return {'message': 'Magasin activé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def deactivate_store(self):
        try:
            data = request.get_json()
            store_uid = data.get('store_uid')
            
            if not store_uid:
                return {'error': 'store_uid requis'}, 400
            
            store = ps_stores.query.filter_by(store_uid=store_uid).first()
            if not store:
                return {'error': 'Magasin non trouvé'}, 404
            
            store.store_is_active = False
            db.session.commit()
            
            return {'message': 'Magasin désactivé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete_store(self):
        try:
            data = request.get_json()
            store_uid = data.get('store_uid')
            
            if not store_uid:
                return {'error': 'store_uid requis'}, 400
            
            store = ps_stores.query.filter_by(store_uid=store_uid).first()
            if not store:
                return {'error': 'Magasin non trouvé'}, 404
            
            db.session.delete(store)
            db.session.commit()
            
            return {'message': 'Magasin supprimé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
