#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API pour la gestion des produits PriceScan
"""

from flask import request, jsonify
from flask_restful import Resource
from helpers.products import get_all_products, get_product_by_id, create_product, update_product, delete_product
from helpers.categories import get_all_categories
from helpers.stores import get_all_stores


class ProductsApi(Resource):
    """API pour la gestion des produits"""
    
    def get(self, product_id=None):
        """Récupérer un produit ou tous les produits"""
        try:
            if product_id:
                # Récupérer un produit spécifique
                product = get_product_by_id(product_id)
                if product:
                    return {
                        'response': 'success',
                        'product': product
                    }, 200
                else:
                    return {
                        'response': 'error',
                        'message': 'Produit non trouvé'
                    }, 404
            else:
                # Récupérer tous les produits
                products = get_all_products()
                return {
                    'response': 'success',
                    'products': products,
                    'total': len(products)
                }, 200
                
        except Exception as e:
            return {
                'response': 'error',
                'message': f'Erreur lors de la récupération des produits: {str(e)}'
            }, 500
    
    def post(self):
        """Créer un nouveau produit"""
        try:
            data = request.json
            required_fields = ['product_name', 'category_id', 'store_id', 'price_amount']
            
            # Vérifier les champs requis
            for field in required_fields:
                if not data.get(field):
                    return {
                        'response': 'error',
                        'message': f'Le champ {field} est requis'
                    }, 400
            
            # Créer le produit
            product = create_product(data)
            
            return {
                'response': 'success',
                'message': 'Produit créé avec succès',
                'product': product
            }, 201
            
        except Exception as e:
            return {
                'response': 'error',
                'message': f'Erreur lors de la création du produit: {str(e)}'
            }, 500
    
    def put(self, product_id):
        """Mettre à jour un produit"""
        try:
            if not product_id:
                return {
                    'response': 'error',
                    'message': 'ID du produit requis'
                }, 400
            
            data = request.json
            product = update_product(product_id, data)
            
            if product:
                return {
                    'response': 'success',
                    'message': 'Produit mis à jour avec succès',
                    'product': product
                }, 200
            else:
                return {
                    'response': 'error',
                    'message': 'Produit non trouvé'
                }, 404
                
        except Exception as e:
            return {
                'response': 'error',
                'message': f'Erreur lors de la mise à jour: {str(e)}'
            }, 500
    
    def delete(self, product_id):
        """Supprimer un produit"""
        try:
            if not product_id:
                return {
                    'response': 'error',
                    'message': 'ID du produit requis'
                }, 400
            
            success = delete_product(product_id)
            
            if success:
                return {
                    'response': 'success',
                    'message': 'Produit supprimé avec succès'
                }, 200
            else:
                return {
                    'response': 'error',
                    'message': 'Produit non trouvé'
                }, 404
                
        except Exception as e:
            return {
                'response': 'error',
                'message': f'Erreur lors de la suppression: {str(e)}'
            }, 500


class CategoriesApi(Resource):
    """API pour la gestion des catégories"""
    
    def get(self):
        """Récupérer toutes les catégories"""
        try:
            categories = get_all_categories()
            return {
                'response': 'success',
                'categories': categories
            }, 200
        except Exception as e:
            return {
                'response': 'error',
                'message': f'Erreur lors de la récupération des catégories: {str(e)}'
            }, 500


class StoresApi(Resource):
    """API pour la gestion des magasins"""
    
    def get(self):
        """Récupérer tous les magasins"""
        try:
            stores = get_all_stores()
            return {
                'response': 'success',
                'stores': stores
            }, 200
        except Exception as e:
            return {
                'response': 'error',
                'message': f'Erreur lors de la récupération des magasins: {str(e)}'
            }, 500
