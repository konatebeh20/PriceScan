#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper pour la gestion des produits PriceScan
"""

import uuid
from datetime import datetime
from config.db import db
from model.PriceScan_db import ps_products, ps_prices, ps_categories, ps_stores


def get_all_products():
    """Récupérer tous les produits avec leurs prix et catégories"""
    try:
        products = db.session.query(
            ps_products, ps_categories.cat_label, ps_prices.price_amount, ps_prices.price_currency
        ).join(
            ps_categories, ps_products.category_id == ps_categories.id, isouter=True
        ).join(
            ps_prices, ps_products.id == ps_prices.product_id, isouter=True
        ).all()
        
        products_list = []
        for product, cat_label, price_amount, price_currency in products:
            # Trouver le prix le plus récent pour ce produit
            latest_price = db.session.query(ps_prices).filter(
                ps_prices.product_id == product.id
            ).order_by(ps_prices.price_date.desc()).first()
            
            products_list.append({
                'id': product.id,
                'product_uid': product.product_uid,
                'product_name': product.product_name,
                'product_description': product.product_description,
                'product_brand': product.product_brand,
                'product_barcode': product.product_barcode,
                'category_id': product.category_id,
                'category_name': cat_label or 'Non catégorisé',
                'product_image': product.product_image,
                'product_is_active': product.product_is_active,
                'price_amount': latest_price.price_amount if latest_price else 0,
                'price_currency': latest_price.price_currency if latest_price else 'CFA',
                'creation_date': product.creation_date.isoformat() if product.creation_date else None,
                'updated_on': product.updated_on.isoformat() if product.updated_on else None
            })
        
        return products_list
        
    except Exception as e:
        print(f"Erreur lors de la récupération des produits: {e}")
        return []


def get_product_by_id(product_id):
    """Récupérer un produit par son ID"""
    try:
        product = db.session.query(
            ps_products, ps_categories.cat_label
        ).join(
            ps_categories, ps_products.category_id == ps_categories.id, isouter=True
        ).filter(ps_products.id == product_id).first()
        
        if not product:
            return None
        
        product_obj, cat_label = product
        
        # Trouver le prix le plus récent
        latest_price = db.session.query(ps_prices).filter(
            ps_prices.product_id == product_obj.id
        ).order_by(ps_prices.price_date.desc()).first()
        
        return {
            'id': product_obj.id,
            'product_uid': product_obj.product_uid,
            'product_name': product_obj.product_name,
            'product_description': product_obj.product_description,
            'product_brand': product_obj.product_brand,
            'product_barcode': product_obj.product_barcode,
            'category_id': product_obj.category_id,
            'category_name': cat_label or 'Non catégorisé',
            'product_image': product_obj.product_image,
            'product_is_active': product_obj.product_is_active,
            'price_amount': latest_price.price_amount if latest_price else 0,
            'price_currency': latest_price.price_currency if latest_price else 'CFA',
            'creation_date': product_obj.creation_date.isoformat() if product_obj.creation_date else None,
            'updated_on': product_obj.updated_on.isoformat() if product_obj.updated_on else None
        }
        
    except Exception as e:
        print(f"Erreur lors de la récupération du produit {product_id}: {e}")
        return None


def create_product(data):
    """Créer un nouveau produit avec son prix"""
    try:
        # Créer le produit
        new_product = ps_products(
            product_uid=str(uuid.uuid4()),
            product_name=data['product_name'],
            product_description=data.get('product_description'),
            product_brand=data.get('product_brand'),
            product_barcode=data.get('product_barcode'),
            category_id=data['category_id'],
            product_image=data.get('product_image'),
            product_is_active=data.get('product_is_active', True)
        )
        
        db.session.add(new_product)
        db.session.flush()  # Pour obtenir l'ID du produit
        
        # Créer le prix associé
        new_price = ps_prices(
            price_uid=str(uuid.uuid4()),
            product_id=new_product.id,
            store_id=data['store_id'],
            price_amount=float(data['price_amount']),
            price_currency=data.get('price_currency', 'CFA'),
            price_date=datetime.utcnow(),
            price_source='manual'
        )
        
        db.session.add(new_price)
        db.session.commit()
        
        # Retourner le produit créé avec ses informations
        return get_product_by_id(new_product.id)
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la création du produit: {e}")
        raise e


def update_product(product_id, data):
    """Mettre à jour un produit"""
    try:
        product = ps_products.query.get(product_id)
        if not product:
            return None
        
        # Mettre à jour les champs du produit
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
        if 'product_is_active' in data:
            product.product_is_active = data['product_is_active']
        
        product.updated_on = datetime.utcnow()
        
        # Si un nouveau prix est fourni, le créer
        if 'price_amount' in data and 'store_id' in data:
            new_price = ps_prices(
                price_uid=str(uuid.uuid4()),
                product_id=product.id,
                store_id=data['store_id'],
                price_amount=float(data['price_amount']),
                price_currency=data.get('price_currency', 'CFA'),
                price_date=datetime.utcnow(),
                price_source='manual'
            )
            db.session.add(new_price)
        
        db.session.commit()
        
        # Retourner le produit mis à jour
        return get_product_by_id(product_id)
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour du produit {product_id}: {e}")
        raise e


def delete_product(product_id):
    """Supprimer un produit"""
    try:
        product = ps_products.query.get(product_id)
        if not product:
            return False
        
        # Supprimer d'abord les prix associés
        db.session.query(ps_prices).filter(ps_prices.product_id == product_id).delete()
        
        # Supprimer le produit
        db.session.delete(product)
        db.session.commit()
        
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression du produit {product_id}: {e}")
        return False


def search_products(query, category_id=None):
    """Rechercher des produits par nom ou code-barres"""
    try:
        query_filter = db.session.query(
            ps_products, ps_categories.cat_label
        ).join(
            ps_categories, ps_products.category_id == ps_categories.id, isouter=True
        ).filter(
            ps_products.product_is_active == True
        )
        
        # Filtre par catégorie si spécifié
        if category_id:
            query_filter = query_filter.filter(ps_products.category_id == category_id)
        
        # Recherche par nom ou code-barres
        if query:
            query_filter = query_filter.filter(
                db.or_(
                    ps_products.product_name.ilike(f'%{query}%'),
                    ps_products.product_barcode.ilike(f'%{query}%')
                )
            )
        
        products = query_filter.all()
        
        products_list = []
        for product, cat_label in products:
            # Trouver le prix le plus récent
            latest_price = db.session.query(ps_prices).filter(
                ps_prices.product_id == product.id
            ).order_by(ps_prices.price_date.desc()).first()
            
            products_list.append({
                'id': product.id,
                'product_uid': product.product_uid,
                'product_name': product.product_name,
                'product_description': product.product_description,
                'product_brand': product.product_brand,
                'product_barcode': product.product_barcode,
                'category_id': product.category_id,
                'category_name': cat_label or 'Non catégorisé',
                'product_image': product.product_image,
                'price_amount': latest_price.price_amount if latest_price else 0,
                'price_currency': latest_price.price_currency if latest_price else 'CFA'
            })
        
        return products_list
        
    except Exception as e:
        print(f"Erreur lors de la recherche des produits: {e}")
        return []
