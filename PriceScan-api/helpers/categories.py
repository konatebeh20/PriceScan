#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper pour la gestion des catégories PriceScan
"""

from config.db import db
from model.PriceScan_db import ps_categories


def get_all_categories():
    """Récupérer toutes les catégories actives"""
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
                'creation_date': category.creation_date.isoformat() if category.creation_date else None,
                'updated_on': category.updated_on.isoformat() if category.updated_on else None
            })
        
        return categories_list
        
    except Exception as e:
        print(f"Erreur lors de la récupération des catégories: {e}")
        return []


def get_category_by_id(category_id):
    """Récupérer une catégorie par son ID"""
    try:
        category = ps_categories.query.get(category_id)
        
        if not category:
            return None
        
        return {
            'id': category.id,
            'cat_uid': category.cat_uid,
            'cat_label': category.cat_label,
            'cat_description': category.cat_description,
            'cat_is_featured': category.cat_is_featured,
            'cat_banner': category.cat_banner,
            'cat_icon': category.cat_icon,
            'creation_date': category.creation_date.isoformat() if category.creation_date else None,
            'updated_on': category.updated_on.isoformat() if category.updated_on else None
        }
        
    except Exception as e:
        print(f"Erreur lors de la récupération de la catégorie {category_id}: {e}")
        return None


def get_featured_categories():
    """Récupérer les catégories mises en avant"""
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
        
        return categories_list
        
    except Exception as e:
        print(f"Erreur lors de la récupération des catégories mises en avant: {e}")
        return []
