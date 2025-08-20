import os
from flask import Flask, flash, jsonify, redirect, request, url_for
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from config.constant import *
from config.db import db
from helpers.mailer import *
from model.goparadize import *
import json


def CreateFavorite():
    response = {}
    try:

        new_fav = go_favorite()

        new_fav.u_uid = request.json.get('u_uid')
        new_fav.htl_uid = request.json.get('htl_uid')
        new_fav.status = request.json.get('status')

        db.session.add(new_fav)
        db.session.commit()

        hotel_info = {}
        try:
            item = go_hotels.query.filter_by(htl_uid=new_fav.htl_uid).first()
            
            if item:
                hotel_info['htl_uid'] = item.htl_uid
                hotel_info['htl_title'] = item.htl_title
                hotel_info['htl_status'] = item.htl_status
                hotel_info['htl_stars'] = item.htl_stars
                hotel_info['htl_address'] = item.htl_address
                hotel_info['htl_description'] = item.htl_description
                hotel_info['htl_amenities'] = item.htl_amenities
                hotel_info['htl_longitude'] = item.htl_longitude
                hotel_info['htl_latitude'] = item.htl_latitude
                hotel_info['htl_tel_number'] = item.htl_tel_number
                hotel_info['htl_room_quantity'] = item.htl_room_quantity
                hotel_info['htl_category'] = item.htl_category
                hotel_info['htl_feature_image'] = str(IMGHOSTNAME) + str(item.htl_feature_image)
                hotel_info['creation_date'] = str(item.creation_date)
                hotel_info['updated_on'] = str(item.updated_on)
            else:
                raise NoResultFound("Hotel not found")
        
        except NoResultFound:
            hotel_info['error'] = 'Hotel not found'

        response['fav_uid'] = new_fav.fav_uid
        response['response'] = 'success'
        response['result'] = hotel_info  
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOC01'
        response['error_description'] = str(e.__dict__['orig'])
        return response
    
    return response




def ReadFavorite():
    result = []
    
    getFavorite = go_favorite.query.filter_by().all()
    
    for item in getFavorite:
        rs = {}
        
        rs['fav_uid'] = item.fav_uid
        rs['u_uid'] = item.u_uid
        rs['room_uid'] = item.room_uid
        rs['status'] = item.status
        rs['creation_date'] = str(item.creation_date)
        rs['updated_on'] = str(item.updated_on)

        hotel_info = {}
        try:
            hotel = go_hotels.query.filter_by(htl_uid=item.htl_uid).first()
            if hotel:
                hotel_info['htl_uid'] = hotel.htl_uid
                hotel_info['htl_title'] = hotel.htl_title
                hotel_info['htl_status'] = hotel.htl_status
                hotel_info['htl_stars'] = hotel.htl_stars
                hotel_info['htl_address'] = hotel.htl_address
                hotel_info['htl_description'] = hotel.htl_description
                hotel_info['htl_amenities'] = hotel.htl_amenities
                hotel_info['htl_longitude'] = hotel.htl_longitude
                hotel_info['htl_latitude'] = hotel.htl_latitude
                hotel_info['htl_tel_number'] = hotel.htl_tel_number
                hotel_info['htl_room_quantity'] = hotel.htl_room_quantity
                hotel_info['htl_category'] = hotel.htl_category
                hotel_info['htl_feature_image'] = str(IMGHOSTNAME) + str(hotel.htl_feature_image)
                hotel_info['creation_date'] = str(hotel.creation_date)
                hotel_info['updated_on'] = str(hotel.updated_on)
            else:
                hotel_info['error'] = 'Hotel not found'
        except Exception as e:
            hotel_info['error'] = f'Error retrieving hotel info: {str(e)}'
        
        rs['hotel_info'] = hotel_info
        
        result.append(rs)
    
    return result


def ReadFavoriteByUser():
    response = {}
    try:
        result = []

        u_uid = request.json.get('u_uid')
        all_favorite = go_favorite.query.filter_by(u_uid=u_uid).all()

        for item in all_favorite:
            rs = {}
            rs['fav_uid'] = item.fav_uid
            rs['u_uid'] = item.u_uid
            rs['htl_uid'] = item.htl_uid
            rs['status'] = item.status
            rs['creation_date'] = str(item.creation_date)
            rs['updated_on'] = str(item.updated_on)

            hotel_info = {}
            try:
                hotel = go_hotels.query.filter_by(htl_uid=item.htl_uid).first()
                if hotel:
                    hotel_info['htl_uid'] = hotel.htl_uid
                    hotel_info['htl_title'] = hotel.htl_title
                    hotel_info['htl_status'] = hotel.htl_status
                    hotel_info['htl_stars'] = hotel.htl_stars
                    hotel_info['htl_address'] = hotel.htl_address
                    hotel_info['htl_description'] = hotel.htl_description
                    hotel_info['htl_amenities'] = hotel.htl_amenities
                    hotel_info['htl_longitude'] = hotel.htl_longitude
                    hotel_info['htl_latitude'] = hotel.htl_latitude
                    hotel_info['htl_tel_number'] = hotel.htl_tel_number
                    hotel_info['htl_room_quantity'] = hotel.htl_room_quantity
                    hotel_info['htl_category'] = hotel.htl_category
                    hotel_info['htl_feature_image'] = str(IMGHOSTNAME) + str(hotel.htl_feature_image)
                    hotel_info['creation_date'] = str(hotel.creation_date)
                    hotel_info['updated_on'] = str(hotel.updated_on)
                else:
                    hotel_info['error'] = 'Hotel not found'
            except Exception as e:
                hotel_info['error'] = f'Error retrieving hotel info: {str(e)}'

            rs['hotel_info'] = hotel_info

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
        single_favorite = go_favorite.query.filter_by(fav_uid=fav_uid).all()

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
        favorite_to_delete = go_favorite.query.filter_by(fav_uid=fav_uid).first()
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
#         getFavorite = go_favorite.query.filter_by(u_uid=u_uid).first()
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