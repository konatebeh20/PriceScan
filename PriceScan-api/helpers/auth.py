import csv
import json
import uuid
# libraries to be imported
import smtplib
import string
import time
import urllib.request
from datetime import date, datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import lxml
import requests
import urllib3
import xmltodict
from bs4 import BeautifulSoup
from flask import jsonify, request
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

from config.constant import *
from config.db import db
from helpers.mailer import *
from model.PriceScan_db import ps_users, UserStatus


def login():
    response = {}
    username = request.json.get('username')
    password = request.json.get('password')
    try:
        rs = {}

        user = ps_users.query.filter(
            (ps_users.u_username == username) | (ps_users.u_email == username),
            ps_users.u_password == password,
            ps_users.u_status == UserStatus.ACTIVE
        ).first()

        if not user:
            raise ValueError("Invalid credentials or inactive user")

        rs['u_uid'] = user.u_uid
        rs['u_firstname'] = user.u_firstname
        rs['u_lastname'] = user.u_lastname
        rs['u_username'] = user.u_username
        rs['u_email'] = user.u_email
        rs['u_status'] = user.u_status.value if hasattr(user.u_status, 'value') else str(user.u_status)
        rs['u_first_login'] = user.u_first_login

        response['response'] = 'success'
        response['admin_infos'] = rs

    except Exception as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOE07'
        response['error_description'] = str(e)
        c = BadRequest(str(e))
        c.data = response
        raise c

    return response



def loginSocial():
    response = {}
    username = request.form.get('email')
    try:
        rs = {}
        
        user = ps_users.query.filter_by(u_email=username).first()
        
        rs['u_uid'] = user.u_uid
        rs['u_name'] = user.u_name
        rs['u_firstname'] = user.u_firstname
        rs['u_lastname'] = user.u_lastname
        rs['u_username'] = user.u_username
        rs['u_mobile'] = user.u_mobile
        rs['u_address'] = user.u_address
        rs['u_country'] = user.u_country
        rs['u_state'] = user.u_state
        rs['u_city'] = user.u_city
        rs['u_email'] = user.u_email
        rs['u_image_link'] = user.u_image_link
        rs['u_status'] = user.u_status
        rs['u_password'] = user.u_password
        rs['u_first_login'] = user.u_first_login
        
        response['response'] = 'succcess'
        response['result'] = rs
    except:
        return CreateUsersSocial()        
        
    return response




def CreateUsersSocial():
    response = {}
    try:
        newUser = ps_users()
        
        newUser.u_name = request.form.get('name')
        newUser.u_firstname = request.form.get('family_name')
        newUser.u_lastname = request.form.get('given_name')
        newUser.u_username = request.form.get('email')
        newUser.u_mobile = request.form.get('000000000')
        newUser.u_address = request.form.get('u_address')
        newUser.u_country = request.form.get('u_country')
        newUser.u_state = request.form.get('u_state')
        newUser.u_city = request.form.get('u_city')
        newUser.u_email = request.form.get('email')
        newUser.u_image_link = request.form.get('picture')
        newUser.u_status = 1
        newUser.u_password = request.form.get('u_password')
        newUser.u_first_login = 1
        
        db.session.add(newUser)
        db.session.commit()
        
        response['u_uid'] = newUser.u_uid
        response['u_firstname'] = newUser.u_firstname
        response['u_lastname'] = newUser.u_lastname
        response['response'] = 'success'
        
        email = []
        email.append(newUser.u_email)
        send_welcome_mailer(newUser.u_username,email)

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU01'
        response['error_description'] = str(e.__dict__['orig'])
        c = BadRequest(str(e.__dict__['orig']))
        c.data = response
        raise c
        
    return response


def register():
    response = {}
    try:
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        firstname = request.json.get('firstname', '')
        lastname = request.json.get('lastname', '')
        account_type = request.json.get('accountType', 'particulier')
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = ps_users.query.filter(
            (ps_users.u_username == username) | (ps_users.u_email == email)
        ).first()
        
        if existing_user:
            response['response'] = 'error'
            response['error'] = 'User already exists'
            response['error_code'] = 'GOU04'
            response['error_description'] = 'Username or email already registered'
            return response, 400
        
        # Créer un nouvel utilisateur
        new_user = ps_users()
        new_user.u_uid = str(uuid.uuid4())
        new_user.u_username = username
        new_user.u_email = email
        new_user.u_password = password
        new_user.u_firstname = firstname
        new_user.u_lastname = lastname
        new_user.u_status = UserStatus.ACTIVE
        new_user.u_first_login = True
        new_user.u_account_type = account_type
        
        db.session.add(new_user)
        db.session.commit()
        
        # Retourner les informations de l'utilisateur créé
        rs = {}
        rs['u_uid'] = new_user.u_uid
        rs['u_firstname'] = new_user.u_firstname
        rs['u_lastname'] = new_user.u_lastname
        rs['u_username'] = new_user.u_username
        rs['u_email'] = new_user.u_email
        rs['u_status'] = new_user.u_status.value if hasattr(new_user.u_status, 'value') else str(new_user.u_status)
        rs['u_first_login'] = new_user.u_first_login
        
        response['response'] = 'success'
        response['admin_infos'] = rs
        
    except Exception as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU05'
        response['error_description'] = str(e)
        if 'db' in locals():
            db.session.rollback()
        c = BadRequest(str(e))
        c.data = response
        raise c
        
    return response


def delete_account():
    response = {}

    try:
        u_uid = request.json.get('u_uid')
        user = ps_users.query.filter_by(u_uid=u_uid, is_active=True).first()

        if not user:
            response['response'] = 'error'
            response['error'] = 'User not found'
            response['error_code'] = 'GOU02'
            response['error_description'] = 'The user does not exist or is already deleted'
            return response, 404
        
        user.is_active = False
        user.deleted_at = datetime.utcnow()
        db.session.commit()

        response['response'] = 'success'
        response['message'] = 'User account marked as deleted'
        return response, 200

    except Exception as e:
        response['response'] = 'error'
        response['error'] = 'Internal server error'
        response['error_code'] = 'GOU03'
        response['error_description'] = str(e)
        return response, 500