import json
from flask import request
from flask_restful import Resource
from sqlalchemy import func

from config.constant import *
from config.db import db
from model.PriceScan_db import ps_products, ps_categories


class ProductsApi(Resource):
    def get(self, route):
        if route == 'all':
            return self.get_all_products()
        elif route == 'active':
            return self.get_active_products()
        elif route == 'by_category':
            category_id = request.args.get('category_id')
            return self.get_products_by_category(category_id)
        elif route == 'search':
            query = request.args.get('q')
            return self.search_products(query)
        else:
            return {'error': 'Route invalide'}, 400
        
    def post(self, route):
        if route == 'create':
            return self.create_product()
        else:
            return {'error': 'Route invalide'}, 400
        
    def patch(self, route):
        if route == 'update':
            return self.update_product()
        elif route == 'activate':
            return self.activate_product()
        elif route == 'deactivate':
            return self.deactivate_product()
        else:
            return {'error': 'Route invalide'}, 400
        
    def delete(self, route):
        if route == 'delete':
            return self.delete_product()
        else:
            return {'error': 'Route invalide'}, 400

    def get_all_products(self):
        try:
            products = ps_products.query.all()
            products_list = []
            for product in products:
                products_list.append({
                    'id': product.id,
                    'product_uid': product.product_uid,
                    'product_name': product.product_name,
                    'product_description': product.product_description,
                    'product_brand': product.product_brand,
                    'product_barcode': product.product_barcode,
                    'category_id': product.category_id,
                    'product_image': product.product_image,
                    'product_is_active': product.product_is_active,
                    'creation_date': product.creation_date.isoformat() if product.creation_date else None,
                    'updated_on': product.updated_on.isoformat() if product.updated_on else None
                })
            return {'products': products_list, 'count': len(products_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_active_products(self):
        try:
            products = ps_products.query.filter_by(product_is_active=True).all()
            products_list = []
            for product in products:
                products_list.append({
                    'id': product.id,
                    'product_uid': product.product_uid,
                    'product_name': product.product_name,
                    'product_description': product.product_description,
                    'product_brand': product.product_brand,
                    'product_barcode': product.product_barcode,
                    'category_id': product.category_id,
                    'product_image': product.product_image,
                    'creation_date': product.creation_date.isoformat() if product.creation_date else None
                })
            return {'products': products_list, 'count': len(products_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_products_by_category(self, category_id):
        try:
            if not category_id:
                return {'error': 'category_id requis'}, 400
            
            products = ps_products.query.filter(
                ps_products.category_id == category_id,
                ps_products.product_is_active == True
            ).all()
            
            products_list = []
            for product in products:
                products_list.append({
                    'id': product.id,
                    'product_uid': product.product_uid,
                    'product_name': product.product_name,
                    'product_description': product.product_description,
                    'product_brand': product.product_brand,
                    'product_barcode': product.product_barcode,
                    'category_id': product.category_id,
                    'product_image': product.product_image
                })
            return {'products': products_list, 'count': len(products_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def search_products(self, query):
        try:
            if not query:
                return {'error': 'Terme de recherche requis'}, 400
            
            products = ps_products.query.filter(
                ps_products.product_name.ilike(f'%{query}%'),
                ps_products.product_is_active == True
            ).all()
            
            products_list = []
            for product in products:
                products_list.append({
                    'id': product.id,
                    'product_uid': product.product_uid,
                    'product_name': product.product_name,
                    'product_description': product.product_description,
                    'product_brand': product.product_brand,
                    'product_barcode': product.product_barcode,
                    'category_id': product.category_id,
                    'product_image': product.product_image
                })
            return {'products': products_list, 'count': len(products_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def create_product(self):
        try:
            data = request.get_json()
            
            # Validation des données requises
            required_fields = ['product_name']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Champ requis: {field}'}, 400
            
            # Vérification de la catégorie si fournie
            if 'category_id' in data and data['category_id']:
                category = ps_categories.query.get(data['category_id'])
                if not category:
                    return {'error': 'Catégorie non trouvée'}, 404
            
            # Création du produit
            new_product = ps_products(
                product_name=data['product_name'],
                product_description=data.get('product_description'),
                product_brand=data.get('product_brand'),
                product_barcode=data.get('product_barcode'),
                category_id=data.get('category_id'),
                product_image=data.get('product_image'),
                product_is_active=data.get('product_is_active', True)
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            return {
                'message': 'Produit créé avec succès',
                'product_uid': new_product.product_uid
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def update_product(self):
        try:
            data = request.get_json()
            product_uid = data.get('product_uid')
            
            if not product_uid:
                return {'error': 'product_uid requis'}, 400
            
            product = ps_products.query.filter_by(product_uid=product_uid).first()
            if not product:
                return {'error': 'Produit non trouvé'}, 404
            
            # Vérification de la catégorie si fournie
            if 'category_id' in data and data['category_id']:
                category = ps_categories.query.get(data['category_id'])
                if not category:
                    return {'error': 'Catégorie non trouvée'}, 404
            
            # Mise à jour des champs
            if 'product_name' in data:
                product.product_name = data['product_name']
            if 'product_description' in data:
                product.product_description = data['product_description']
            if 'product_brand' in data:
                product.product_brand = data['product_brand']
            if 'product_barcode' in data:
                product.product_barcode = data['product_barcode']
            if 'category_id' in data:
                product.category_id = data['category_id']
            if 'product_image' in data:
                product.product_image = data['product_image']
            
            db.session.commit()
            
            return {'message': 'Produit mis à jour avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def activate_product(self):
        try:
            data = request.get_json()
            product_uid = data.get('product_uid')
            
            if not product_uid:
                return {'error': 'product_uid requis'}, 400
            
            product = ps_products.query.filter_by(product_uid=product_uid).first()
            if not product:
                return {'error': 'Produit non trouvé'}, 404
            
            product.product_is_active = True
            db.session.commit()
            
            return {'message': 'Produit activé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def deactivate_product(self):
        try:
            data = request.get_json()
            product_uid = data.get('product_uid')
            
            if not product_uid:
                return {'error': 'product_uid requis'}, 400
            
            product = ps_products.query.filter_by(product_uid=product_uid).first()
            if not product:
                return {'error': 'Produit non trouvé'}, 404
            
            product.product_is_active = False
            db.session.commit()
            
            return {'message': 'Produit désactivé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete_product(self):
        try:
            data = request.get_json()
            product_uid = data.get('product_uid')
            
            if not product_uid:
                return {'error': 'product_uid requis'}, 400
            
            product = ps_products.query.filter_by(product_uid=product_uid).first()
            if not product:
                return {'error': 'Produit non trouvé'}, 404
            
            db.session.delete(product)
            db.session.commit()
            
            return {'message': 'Produit supprimé avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
