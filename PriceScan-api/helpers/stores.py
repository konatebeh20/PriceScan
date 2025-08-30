#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper pour la gestion des magasins PriceScan
"""

from config.db import db
from model.PriceScan_db import ps_stores


def get_all_stores():
    """Récupérer tous les magasins actifs"""
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
                'creation_date': store.creation_date.isoformat() if store.creation_date else None,
                'updated_on': store.updated_on.isoformat() if store.updated_on else None
            })
        
        return stores_list
        
    except Exception as e:
        print(f"Erreur lors de la récupération des magasins: {e}")
        return []


def get_store_by_id(store_id):
    """Récupérer un magasin par son ID"""
    try:
        store = ps_stores.query.get(store_id)
        
        if not store:
            return None
        
        return {
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
            'creation_date': store.creation_date.isoformat() if store.creation_date else None,
            'updated_on': store.updated_on.isoformat() if store.updated_on else None
        }
        
    except Exception as e:
        print(f"Erreur lors de la récupération du magasin {store_id}: {e}")
        return None


def get_stores_by_city(city):
    """Récupérer les magasins par ville"""
    try:
        stores = ps_stores.query.filter_by(
            store_city=city,
            store_is_active=True
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
        
        return stores_list
        
    except Exception as e:
        print(f"Erreur lors de la récupération des magasins de {city}: {e}")
        return []
