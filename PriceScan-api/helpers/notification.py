
from flask import jsonify, request
from werkzeug.utils import secure_filename
from config.db import db
from config.constant import *
from model.goparadize import go_notification
import boto3



def CreateNotification():
    
    response = {}
    try:
        new_notification = go_notification()
        new_notification.header = request.json.get('header')
        new_notification.body = request.json.get('body')
        new_notification.destined_for = request.json.get('destined_for') # 'All' or 'recipient uid'
        new_notification.status = 'Active'
        
        db.session.add(new_notification)
        db.session.commit()

        rs = {}
        rs['notification_id'] = new_notification.notification_id
        rs['header'] = new_notification.header
        rs['body'] = new_notification.body
        rs['destined_for'] = new_notification.destined_for
        rs['status'] = new_notification.status

        response['satus'] = 'success'
        response['notification_infos'] = rs

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response



# def UpdateNotification():
#     response = {}

#     try:
#         notification_id = request.json.get('notification_id')
#         update_notification = go_notification.query.filter_by(notification_id = notification_id).first()
        
#         if update_notification:
#             update_notification.notification_name = request.json.get('notification_name', update_notification.notification_name)
#             update_notification.start_date = request.json.get('start_date', update_notification.start_date)
#             update_notification.end_date = request.json.get('end_date', update_notification.end_date)
#             update_notification.status = request.json.get('status', update_notification.status)
#             uploaded_files = upload_files()  
#             if uploaded_files:
#                 update_notification.notification_image = uploaded_files 

#         db.session.add(update_notification)
#         db.session.commit() 
        
#         rs = {}
#         rs['notification_id'] = update_notification.notification_id
#         rs['notification_name'] = update_notification.notification_name
#         rs['notification_image'] = str(IMGHOSTNAME) + str(update_notification.notification_image)
#         rs['start_date'] = update_notification.start_date
#         rs['end_date'] = update_notification.end_date
#         rs['status'] = update_notification.status

#         response['status'] = 'success'
#         response['notification_infos'] = rs
#         response['message'] = "the notification has been updated!"

#     except Exception as e:
#         response['status'] = 'error'
#         response['error_description'] = str(e)

#     return response



def DeleteNotification():
    response = {}

    try:
        notification_id = request.json.get('notification_id')
        delete_notification = go_notification.query.filter_by(notification_id=notification_id).first()

        if delete_notification:
            db.session.delete(delete_notification)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'notification not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response



def ReadAllNotification():
    response = {}
    
    try:
        all_notification = go_notification.query.all()
        notification_info = []
        for notification  in all_notification:
            notification_infos = {
                'notification_id': notification.notification_id,              
                'header': notification.header,              
                'body': notification.body,            
                'destined_for': notification.destined_for,          
                'status': notification.status,          
            }
            notification_info.append(notification_infos)

        response['status'] = 'success'
        response ['notification'] = notification_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def ReadSingleNotification():
    response = {}

    try:
        notification_id = request.json.get('notification_id')
        single_notification = go_notification.query.filter_by(notification_id=notification_id).first()
        notification_infos = {
            'notification_id': single_notification.notification_id,
            'header': single_notification.header,  
            'body': single_notification.body,              
            'destined_for': single_notification.destined_for,              
            'status': single_notification.status,              
        }
        response['status'] = 'success'
        response['notification'] = notification_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 