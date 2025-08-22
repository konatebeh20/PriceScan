import json
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime

from config.constant import *
from config.db import db
from model.PriceScan_db import ps_prices, ps_products, ps_stores


class PricesApi(Resource):
    def get(self, route):
        if route == 'all':
            return self.get_all_prices()
        elif route == 'by_product':
            product_id = request.args.get('product_id')
            return self.get_prices_by_product(product_id)
        elif route == 'by_store':
            store_id = request.args.get('store_id')
            return self.get_prices_by_store(store_id)
        elif route == 'compare':
            product_id = request.args.get('product_id')
            return self.compare_prices(product_id)
        elif route == 'latest':
            return self.get_latest_prices()
        else:
            return {'error': 'Route invalide'}, 400
        
    def post(self, route):
        if route == 'create':
            return self.create_price()
        else:
            return {'error': 'Route invalide'}, 400
        
    def patch(self, route):
        if route == 'update':
            return self.update_price()
        else:
            return {'error': 'Route invalide'}, 400
        
    def delete(self, route):
        if route == 'delete':
            return self.delete_price()
        else:
            return {'error': 'Route invalide'}, 400

    def get_all_prices(self):
        try:
            prices = ps_prices.query.all()
            prices_list = []
            for price in prices:
                prices_list.append({
                    'id': price.id,
                    'price_uid': price.price_uid,
                    'product_id': price.product_id,
                    'store_id': price.store_id,
                    'price_amount': price.price_amount,
                    'price_currency': price.price_currency,
                    'price_date': price.price_date.isoformat() if price.price_date else None,
                    'price_is_promo': price.price_is_promo,
                    'price_promo_end': price.price_promo_end.isoformat() if price.price_promo_end else None,
                    'price_source': price.price_source,
                    'creation_date': price.creation_date.isoformat() if price.creation_date else None
                })
            return {'prices': prices_list, 'count': len(prices_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_prices_by_product(self, product_id):
        try:
            if not product_id:
                return {'error': 'product_id requis'}, 400
            
            prices = ps_prices.query.filter_by(product_id=product_id).order_by(ps_prices.price_date.desc()).all()
            
            prices_list = []
            for price in prices:
                # Récupérer les informations du magasin
                store = ps_stores.query.get(price.store_id)
                store_info = {
                    'store_name': store.store_name if store else 'Magasin inconnu',
                    'store_city': store.store_city if store else None
                } if store else None
                
                prices_list.append({
                    'id': price.id,
                    'price_uid': price.price_uid,
                    'product_id': price.product_id,
                    'store_id': price.store_id,
                    'store_info': store_info,
                    'price_amount': price.price_amount,
                    'price_currency': price.price_currency,
                    'price_date': price.price_date.isoformat() if price.price_date else None,
                    'price_is_promo': price.price_is_promo,
                    'price_promo_end': price.price_promo_end.isoformat() if price.price_promo_end else None,
                    'price_source': price.price_source
                })
            return {'prices': prices_list, 'count': len(prices_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_prices_by_store(self, store_id):
        try:
            if not store_id:
                return {'error': 'store_id requis'}, 400
            
            prices = ps_prices.query.filter_by(store_id=store_id).order_by(ps_prices.price_date.desc()).all()
            
            prices_list = []
            for price in prices:
                # Récupérer les informations du produit
                product = ps_products.query.get(price.product_id)
                product_info = {
                    'product_name': product.product_name if product else 'Produit inconnu',
                    'product_brand': product.product_brand if product else None
                } if product else None
                
                prices_list.append({
                    'id': price.id,
                    'price_uid': price.price_uid,
                    'product_id': price.product_id,
                    'product_info': product_info,
                    'store_id': price.store_id,
                    'price_amount': price.price_amount,
                    'price_currency': price.price_currency,
                    'price_date': price.price_date.isoformat() if price.price_date else None,
                    'price_is_promo': price.price_is_promo,
                    'price_promo_end': price.price_promo_end.isoformat() if price.price_promo_end else None,
                    'price_source': price.price_source
                })
            return {'prices': prices_list, 'count': len(prices_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def compare_prices(self, product_id):
        try:
            if not product_id:
                return {'error': 'product_id requis'}, 400
            
            # Récupérer tous les prix pour ce produit
            prices = ps_prices.query.filter_by(product_id=product_id).order_by(ps_prices.price_amount.asc()).all()
            
            if not prices:
                return {'error': 'Aucun prix trouvé pour ce produit'}, 404
            
            comparison_data = []
            best_price = None
            best_store = None
            
            for price in prices:
                store = ps_stores.query.get(price.store_id)
                store_info = {
                    'store_name': store.store_name if store else 'Magasin inconnu',
                    'store_city': store.store_city if store else None,
                    'store_address': store.store_address if store else None
                } if store else None
                
                price_info = {
                    'price_uid': price.price_uid,
                    'store_info': store_info,
                    'price_amount': price.price_amount,
                    'price_currency': price.price_currency,
                    'price_date': price.price_date.isoformat() if price.price_date else None,
                    'price_is_promo': price.price_is_promo,
                    'price_promo_end': price.price_promo_end.isoformat() if price.price_promo_end else None,
                    'price_source': price.price_source
                }
                
                comparison_data.append(price_info)
                
                # Déterminer le meilleur prix
                if best_price is None or price.price_amount < best_price:
                    best_price = price.price_amount
                    best_store = store_info
            
            return {
                'product_id': product_id,
                'comparison_data': comparison_data,
                'best_price': best_price,
                'best_store': best_store,
                'price_range': {
                    'min': min([p['price_amount'] for p in comparison_data]),
                    'max': max([p['price_amount'] for p in comparison_data])
                },
                'count': len(comparison_data)
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

    def get_latest_prices(self):
        try:
            # Récupérer les prix les plus récents pour chaque produit
            latest_prices = db.session.query(
                ps_prices.product_id,
                func.max(ps_prices.price_date).label('latest_date')
            ).group_by(ps_prices.product_id).subquery()
            
            prices = db.session.query(ps_prices).join(
                latest_prices,
                (ps_prices.product_id == latest_prices.c.product_id) &
                (ps_prices.price_date == latest_prices.c.latest_date)
            ).all()
            
            prices_list = []
            for price in prices:
                # Récupérer les informations du produit et du magasin
                product = ps_products.query.get(price.product_id)
                store = ps_stores.query.get(price.store_id)
                
                product_info = {
                    'product_name': product.product_name if product else 'Produit inconnu',
                    'product_brand': product.product_brand if product else None
                } if product else None
                
                store_info = {
                    'store_name': store.store_name if store else 'Magasin inconnu',
                    'store_city': store.store_city if store else None
                } if store else None
                
                prices_list.append({
                    'price_uid': price.price_uid,
                    'product_info': product_info,
                    'store_info': store_info,
                    'price_amount': price.price_amount,
                    'price_currency': price.price_currency,
                    'price_date': price.price_date.isoformat() if price.price_date else None,
                    'price_is_promo': price.price_is_promo
                })
            
            return {'latest_prices': prices_list, 'count': len(prices_list)}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

    def create_price(self):
        try:
            data = request.get_json()
            
            # Validation des données requises
            required_fields = ['product_id', 'store_id', 'price_amount']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Champ requis: {field}'}, 400
            
            # Vérification de l'existence du produit et du magasin
            product = ps_products.query.get(data['product_id'])
            if not product:
                return {'error': 'Produit non trouvé'}, 404
            
            store = ps_stores.query.get(data['store_id'])
            if not store:
                return {'error': 'Magasin non trouvé'}, 404
            
            # Création du prix
            new_price = ps_prices(
                product_id=data['product_id'],
                store_id=data['store_id'],
                price_amount=data['price_amount'],
                price_currency=data.get('price_currency', 'CFA'),
                price_date=data.get('price_date', datetime.utcnow()),
                price_is_promo=data.get('price_is_promo', False),
                price_promo_end=data.get('price_promo_end'),
                price_source=data.get('price_source', 'manual')
            )
            
            db.session.add(new_price)
            db.session.commit()
            
            return {
                'message': 'Prix créé avec succès',
                'price_uid': new_price.price_uid
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def update_price(self):
        try:
            data = request.get_json()
            price_uid = data.get('price_uid')
            
            if not price_uid:
                return {'error': 'price_uid requis'}, 400
            
            price = ps_prices.query.filter_by(price_uid=price_uid).first()
            if not price:
                return {'error': 'Prix non trouvé'}, 404
            
            # Mise à jour des champs
            if 'price_amount' in data:
                price.price_amount = data['price_amount']
            if 'price_currency' in data:
                price.price_currency = data['price_currency']
            if 'price_date' in data:
                price.price_date = data['price_date']
            if 'price_is_promo' in data:
                price.price_is_promo = data['price_is_promo']
            if 'price_promo_end' in data:
                price.price_promo_end = data['price_promo_end']
            if 'price_source' in data:
                price.price_source = data['price_source']
            
            db.session.commit()
            
            return {'message': 'Prix mis à jour avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete_price(self):
        try:
            data = request.get_json()
            price_uid = data.get('price_uid')
            
            if not price_uid:
                return {'error': 'price_uid requis'}, 400
            
            price = ps_prices.query.filter_by(price_uid=price_uid).first()
            if not price:
                return {'error': 'Prix non trouvé'}, 404
            
            db.session.delete(price)
            db.session.commit()
            
            return {'message': 'Prix supprimé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
