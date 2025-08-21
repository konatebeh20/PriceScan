import os
from flask import Flask, flash, jsonify, redirect, request, url_for
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from config.constant import *
from config.db import db
from helpers.mailer import *
from model.PriceScan_db import *
import json


def CreateFavorite():
    response = {}
    try:

        new_fav = ps_favorite()

        new_fav.u_uid = request.json.get('u_uid')
        new_fav.htl_uid = request.json.get('htl_uid')
        new_fav.status = request.json.get('status')

        db.session.add(new_fav)
        db.session.commit()

        receipt_info = {}
        try:
            item = ps_receipts.query.filter_by(htl_uid=new_fav.htl_uid).first()
            
            if item:
                receipt_info['htl_uid'] = item.htl_uid
                receipt_info['htl_title'] = item.htl_title
                receipt_info['htl_status'] = item.htl_status
                receipt_info['htl_stars'] = item.htl_stars
                receipt_info['htl_address'] = item.htl_address
                receipt_info['htl_description'] = item.htl_description
                receipt_info['htl_amenities'] = item.htl_amenities
                receipt_info['htl_longitude'] = item.htl_longitude
                receipt_info['htl_latitude'] = item.htl_latitude
                receipt_info['htl_tel_number'] = item.htl_tel_number
                receipt_info['htl_room_quantity'] = item.htl_room_quantity
                receipt_info['htl_category'] = item.htl_category
                receipt_info['htl_feature_image'] = str(IMGHOSTNAME) + str(item.htl_feature_image)
                receipt_info['creation_date'] = str(item.creation_date)
                receipt_info['updated_on'] = str(item.updated_on)
            else:
                raise NoResultFound("receipt not found")
        
        except NoResultFound:
            receipt_info['error'] = 'receipt not found'

        response['fav_uid'] = new_fav.fav_uid
        response['response'] = 'success'
        response['result'] = receipt_info  
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOC01'
        response['error_description'] = str(e.__dict__['orig'])
        return response
    
    return response




def ReadFavorite():
    result = []
    
    getFavorite = ps_favorite.query.filter_by().all()
    
    for item in getFavorite:
        rs = {}
        
        rs['fav_uid'] = item.fav_uid
        rs['u_uid'] = item.u_uid
        rs['room_uid'] = item.room_uid
        rs['status'] = item.status
        rs['creation_date'] = str(item.creation_date)
        rs['updated_on'] = str(item.updated_on)

        receipt_info = {}
        try:
            receipt = ps_receipts.query.filter_by(htl_uid=item.htl_uid).first()
            if receipt:
                receipt_info['htl_uid'] = receipt.htl_uid
                receipt_info['htl_title'] = receipt.htl_title
                receipt_info['htl_status'] = receipt.htl_status
                receipt_info['htl_stars'] = receipt.htl_stars
                receipt_info['htl_address'] = receipt.htl_address
                receipt_info['htl_description'] = receipt.htl_description
                receipt_info['htl_amenities'] = receipt.htl_amenities
                receipt_info['htl_longitude'] = receipt.htl_longitude
                receipt_info['htl_latitude'] = receipt.htl_latitude
                receipt_info['htl_tel_number'] = receipt.htl_tel_number
                receipt_info['htl_room_quantity'] = receipt.htl_room_quantity
                receipt_info['htl_category'] = receipt.htl_category
                receipt_info['htl_feature_image'] = str(IMGHOSTNAME) + str(receipt.htl_feature_image)
                receipt_info['creation_date'] = str(receipt.creation_date)
                receipt_info['updated_on'] = str(receipt.updated_on)
            else:
                receipt_info['error'] = 'receipt not found'
        except Exception as e:
            receipt_info['error'] = f'Error retrieving receipt info: {str(e)}'
        
        rs['receipt_info'] = receipt_info
        
        result.append(rs)
    
    return result


def ReadFavoriteByUser():
    response = {}
    try:
        result = []

        u_uid = request.json.get('u_uid')
        all_favorite = ps_favorite.query.filter_by(u_uid=u_uid).all()

        for item in all_favorite:
            rs = {}
            rs['fav_uid'] = item.fav_uid
            rs['u_uid'] = item.u_uid
            rs['htl_uid'] = item.htl_uid
            rs['status'] = item.status
            rs['creation_date'] = str(item.creation_date)
            rs['updated_on'] = str(item.updated_on)

            receipt_info = {}
            try:
                receipt = ps_receipts.query.filter_by(htl_uid=item.htl_uid).first()
                if receipt:
                    receipt_info['htl_uid'] = receipt.htl_uid
                    receipt_info['htl_title'] = receipt.htl_title
                    receipt_info['htl_status'] = receipt.htl_status
                    receipt_info['htl_stars'] = receipt.htl_stars
                    receipt_info['htl_address'] = receipt.htl_address
                    receipt_info['htl_description'] = receipt.htl_description
                    receipt_info['htl_amenities'] = receipt.htl_amenities
                    receipt_info['htl_longitude'] = receipt.htl_longitude
                    receipt_info['htl_latitude'] = receipt.htl_latitude
                    receipt_info['htl_tel_number'] = receipt.htl_tel_number
                    receipt_info['htl_room_quantity'] = receipt.htl_room_quantity
                    receipt_info['htl_category'] = receipt.htl_category
                    receipt_info['htl_feature_image'] = str(IMGHOSTNAME) + str(receipt.htl_feature_image)
                    receipt_info['creation_date'] = str(receipt.creation_date)
                    receipt_info['updated_on'] = str(receipt.updated_on)
                else:
                    receipt_info['error'] = 'receipt not found'
            except Exception as e:
                receipt_info['error'] = f'Error retrieving receipt info: {str(e)}'

            rs['receipt_info'] = receipt_info

            result.append(rs)

        response['status'] = 'success'
        response['fav_result'] = result
        
    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return jsonify(response)



def ReadSingleFavorite():
    response = {}
    try:
        result = []

        fav_uid = request.json.get('fav_uid')
        single_favorite = ps_favorite.query.filter_by(fav_uid=fav_uid).all()

        for item in single_favorite:
            rs = {}
            rs['fav_uid'] = item.fav_uid
            rs['u_uid'] = item.u_uid
            rs['htl_uid'] = item.htl_uid
            rs['status'] = item.status
            rs['creation_date'] = str(item.creation_date)
            rs['updated_on'] = str(item.updated_on)

            result.append(rs)

        response['status'] = 'success'
        response['fav_result'] = result
        
    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return jsonify(response)




def DeleteFavorite():
    response = {}
    try:
        fav_uid = request.json.get('fav_uid')
        favorite_to_delete = ps_favorite.query.filter_by(fav_uid=fav_uid).first()
        if favorite_to_delete:
            db.session.delete(favorite_to_delete)
            db.session.commit()
            response['status'] = 'success'
            response['fav_status'] = 'null'
        else:
            response['status'] = 'error'
            response['error_description'] = 'Favorite not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response

# def verify_favorite():
    
#     response = {}
#     try:
#         rs = {}
#         u_uid = request.json.get('u_uid')
#         getFavorite = ps_favorite.query.filter_by(u_uid=u_uid).first()
#         # print(getUsers.u_status)
#         if int(getUsers.u_status) == 0:
#             getUsers.u_status = 1
#             db.session.add(getUsers)
#             db.session.commit()
#             response['message'] = 'User Verified Successfuly!'
#             response['response'] = 'success'
#             response['code'] = '001'
#             email = []
#             email.append(getUsers.u_email)
#             send_welcome_mailer(getUsers.u_name, email)
#         else:
#             response['message'] = 'User Already Verified Successfuly!'
#             response['response'] = 'success'
#             response['code'] = '002'


#     except SQLAlchemyError as e:
#         response['response'] = 'error'
#         response['error'] = 'Unavailable'
#         response['error_code'] = 'GOU02'
#         response['error_description'] = str(e.__dict__['orig'])   
    
#     return response