import json
from flask import request
from flask_restful import Resource
from sqlalchemy import func

from config.constant import *
from config.db import db
from model.PriceScan_db import ps_categories


class CategoriesApi(Resource):
    def get(self, route):
        if route == 'all':
            return self.get_all_categories()
        elif route == 'active':
            return self.get_active_categories()
        elif route == 'featured':
            return self.get_featured_categories()
        elif route == 'by_id':
            category_id = request.args.get('id')
            return self.get_category_by_id(category_id)
        else:
            return {'error': 'Route invalide'}, 400
        
    def post(self, route):
        if route == 'create':
            return self.create_category()
        else:
            return {'error': 'Route invalide'}, 400
        
    def patch(self, route):
        if route == 'update':
            return self.update_category()
        elif route == 'activate':
            return self.activate_category()
        elif route == 'deactivate':
            return self.deactivate_category()
        elif route == 'feature':
            return self.feature_category()
        elif route == 'unfeature':
            return self.unfeature_category()
        else:
            return {'error': 'Route invalide'}, 400
        
    def delete(self, route):
        if route == 'delete':
            return self.delete_category()
        else:
            return {'error': 'Route invalide'}, 400

    def get_all_categories(self):
        try:
            categories = ps_categories.query.all()
            categories_list = []
            for category in categories:
                categories_list.append({
                    'id': category.id,
                    'cat_uid': category.cat_uid,
                    'cat_label': category.cat_label,
                    'cat_description': category.cat_description,
                    'cat_is_featured': category.cat_is_featured,
                    'cat_is_active': category.cat_is_active,
                    'cat_banner': category.cat_banner,
                    'cat_icon': category.cat_icon,
                    'creation_date': category.creation_date.isoformat() if category.creation_date else None,
                    'updated_on': category.updated_on.isoformat() if category.updated_on else None
                })
            return {'categories': categories_list, 'count': len(categories_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_active_categories(self):
        try:
            categories = ps_categories.query.filter_by(cat_is_active=True).all()
            categories_list = []
            for category in categories:
                categories_list.append({
                    'id': category.id,
                    'cat_uid': category.cat_uid,
                    'cat_label': category.cat_label,
                    'cat_description': category.cat_description,
                    'cat_is_featured': category.cat_is_featured,
                    'cat_banner': category.cat_banner,
                    'cat_icon': category.cat_icon,
                    'creation_date': category.creation_date.isoformat() if category.creation_date else None
                })
            return {'categories': categories_list, 'count': len(categories_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_featured_categories(self):
        try:
            categories = ps_categories.query.filter_by(
                cat_is_active=True,
                cat_is_featured=True
            ).all()
            
            categories_list = []
            for category in categories:
                categories_list.append({
                    'id': category.id,
                    'cat_uid': category.cat_uid,
                    'cat_label': category.cat_label,
                    'cat_description': category.cat_description,
                    'cat_banner': category.cat_banner,
                    'cat_icon': category.cat_icon
                })
            return {'featured_categories': categories_list, 'count': len(categories_list)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def get_category_by_id(self, category_id):
        try:
            if not category_id:
                return {'error': 'id requis'}, 400
            
            category = ps_categories.query.get(category_id)
            if not category:
                return {'error': 'Catégorie non trouvée'}, 404
            
            category_data = {
                'id': category.id,
                'cat_uid': category.cat_uid,
                'cat_label': category.cat_label,
                'cat_description': category.cat_description,
                'cat_is_featured': category.cat_is_featured,
                'cat_is_active': category.cat_is_active,
                'cat_banner': category.cat_banner,
                'cat_icon': category.cat_icon,
                'creation_date': category.creation_date.isoformat() if category.creation_date else None,
                'updated_on': category.updated_on.isoformat() if category.updated_on else None
            }
            
            return {'category': category_data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def create_category(self):
        try:
            data = request.get_json()
            
            # Validation des données requises
            required_fields = ['cat_label']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Champ requis: {field}'}, 400
            
            # Vérification de l'unicité du label
            existing_category = ps_categories.query.filter_by(cat_label=data['cat_label']).first()
            if existing_category:
                return {'error': 'Une catégorie avec ce nom existe déjà'}, 409
            
            # Création de la catégorie
            new_category = ps_categories(
                cat_label=data['cat_label'],
                cat_description=data.get('cat_description'),
                cat_is_featured=data.get('cat_is_featured', False),
                cat_is_active=data.get('cat_is_active', True),
                cat_banner=data.get('cat_banner'),
                cat_icon=data.get('cat_icon')
            )
            
            db.session.add(new_category)
            db.session.commit()
            
            return {
                'message': 'Catégorie créée avec succès',
                'cat_uid': new_category.cat_uid
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def update_category(self):
        try:
            data = request.get_json()
            cat_uid = data.get('cat_uid')
            
            if not cat_uid:
                return {'error': 'cat_uid requis'}, 400
            
            category = ps_categories.query.filter_by(cat_uid=cat_uid).first()
            if not category:
                return {'error': 'Catégorie non trouvée'}, 404
            
            # Vérification de l'unicité du label si modifié
            if 'cat_label' in data and data['cat_label'] != category.cat_label:
                existing_category = ps_categories.query.filter_by(cat_label=data['cat_label']).first()
                if existing_category:
                    return {'error': 'Une catégorie avec ce nom existe déjà'}, 409
            
            # Mise à jour des champs
            if 'cat_label' in data:
                category.cat_label = data['cat_label']
            if 'cat_description' in data:
                category.cat_description = data['cat_description']
            if 'cat_banner' in data:
                category.cat_banner = data['cat_banner']
            if 'cat_icon' in data:
                category.cat_icon = data['cat_icon']
            
            db.session.commit()
            
            return {'message': 'Catégorie mise à jour avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def activate_category(self):
        try:
            data = request.get_json()
            cat_uid = data.get('cat_uid')
            
            if not cat_uid:
                return {'error': 'cat_uid requis'}, 400
            
            category = ps_categories.query.filter_by(cat_uid=cat_uid).first()
            if not category:
                return {'error': 'Catégorie non trouvée'}, 404
            
            category.cat_is_active = True
            db.session.commit()
            
            return {'message': 'Catégorie activée avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def deactivate_category(self):
        try:
            data = request.get_json()
            cat_uid = data.get('cat_uid')
            
            if not cat_uid:
                return {'error': 'cat_uid requis'}, 400
            
            category = ps_categories.query.filter_by(cat_uid=cat_uid).first()
            if not category:
                return {'error': 'Catégorie non trouvée'}, 404
            
            category.cat_is_active = False
            db.session.commit()
            
            return {'message': 'Catégorie désactivée avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def feature_category(self):
        try:
            data = request.get_json()
            cat_uid = data.get('cat_uid')
            
            if not cat_uid:
                return {'error': 'cat_uid requis'}, 400
            
            category = ps_categories.query.filter_by(cat_uid=cat_uid).first()
            if not category:
                return {'error': 'Catégorie non trouvée'}, 404
            
            category.cat_is_featured = True
            db.session.commit()
            
            return {'message': 'Catégorie mise en avant avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def unfeature_category(self):
        try:
            data = request.get_json()
            cat_uid = data.get('cat_uid')
            
            if not cat_uid:
                return {'error': 'cat_uid requis'}, 400
            
            category = ps_categories.query.filter_by(cat_uid=cat_uid).first()
            if not category:
                return {'error': 'Catégorie non trouvée'}, 404
            
            category.cat_is_featured = False
            db.session.commit()
            
            return {'message': 'Catégorie retirée de la mise en avant avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete_category(self):
        try:
            data = request.get_json()
            cat_uid = data.get('cat_uid')
            
            if not cat_uid:
                return {'error': 'cat_uid requis'}, 400
            
            category = ps_categories.query.filter_by(cat_uid=cat_uid).first()
            if not category:
                return {'error': 'Catégorie non trouvée'}, 404
            
            # Vérifier s'il y a des produits associés à cette catégorie
            from model.PriceScan_db import ps_products
            products_count = ps_products.query.filter_by(category_id=category.id).count()
            
            if products_count > 0:
                return {
                    'error': f'Impossible de supprimer cette catégorie. {products_count} produit(s) y sont associés.'
                }, 400
            
            db.session.delete(category)
            db.session.commit()
            
            return {'message': 'Catégorie supprimée avec succès'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
