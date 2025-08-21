import json
from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from config.db import db
from model.price_comparison import ps_users, user_activity_log, receipts, receipt_items
from helpers.mailer import send_mailer_custom
# from helpers.mailer import *


# @jwt_required()
def upload_receipt():
    """
    Upload et enregistrement d’un reçu scanné par un utilisateur
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        
        new_receipt = receipts()
        new_receipt.user_id = current_user_id
        new_receipt.store_name = request.json.get("store_name", "")
        new_receipt.total_amount = request.json.get("total_amount", 0.0)
        new_receipt.purchase_date = request.json.get("purchase_date", datetime.now())
        new_receipt.image_url = request.json.get("image_url", "")
        new_receipt.status = "pending"  # pending, processing, completed, failed
        new_receipt.created_at = datetime.now()

        db.session.add(new_receipt)
        db.session.commit()


        # Traitement asynchrone (idéalement avec Celery ou un worker)
        process_receipt_image(new_receipt.receipt_id, image_data)

        # Log activity
        log_user_activity(current_user_id, "receipt_uploaded", {"receipt_id": new_receipt.receipt_id})

        response["response"] = "success"
        response["message"] = "Receipt uploaded successfully"
        response["receipt_id"] = new_receipt.receipt_id

    except SQLAlchemyError as e:
        db.session.rollback()
        response["response"] = "error"
        response["error_code"] = "RC01"
        response["error_description"] = str(e.__dict__.get("orig", e))

    return response


# @jwt_required()
def add_receipt_items():
    """
    Ajouter les articles extraits d’un reçu
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        receipt_id = request.json.get("receipt_id")

        receipt = receipts.query.filter_by(receipt_id=receipt_id, user_id=current_user_id).first()
        if not receipt:
            response["response"] = "error"
            response["error_code"] = "RC02"
            response["error_description"] = "Receipt not found"
            return response

        items = request.json.get("items", [])
        for item in items:
            new_item = receipt_items()
            new_item.receipt_id = receipt_id
            new_item.product_name = item.get("product_name")
            new_item.quantity = item.get("quantity", 1)
            new_item.unit_price = item.get("unit_price", 0.0)
            new_item.total_price = new_item.quantity * new_item.unit_price
            db.session.add(new_item)

        db.session.commit()

        log_user_activity(current_user_id, "receipt_items_added", {"receipt_id": receipt_id})

        response["response"] = "success"
        response["message"] = "Receipt items added successfully"

    except SQLAlchemyError as e:
        db.session.rollback()
        response["response"] = "error"
        response["error_code"] = "RC03"
        response["error_description"] = str(e.__dict__.get("orig", e))

    return response


# @jwt_required()
def get_user_receipts():
    """
    Récupérer tous les reçus d’un utilisateur
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        user_receipts = receipts.query.filter_by(user_id=current_user_id).all()

        receipts_data = []
        for r in user_receipts:
            receipts_data.append({
                "receipt_id": r.receipt_id,
                "store_name": r.store_name,
                "total_amount": r.total_amount,
                "purchase_date": r.purchase_date.strftime("%Y-%m-%d"),
                "image_url": r.image_url
            })

        response["response"] = "success"
        response["receipts"] = receipts_data

    except SQLAlchemyError as e:
        response["response"] = "error"
        response["error_code"] = "RC04"
        response["error_description"] = str(e.__dict__.get("orig", e))

    return response


def log_user_activity(user_id, activity_type, metadata=None):
    """
    Enregistrer l’activité utilisateur liée aux reçus
    """
    try:
        activity = user_activity_log()
        activity.user_id = user_id
        activity.activity_type = activity_type
        activity.metadata = json.dumps(metadata) if metadata else None
        activity.created_at = datetime.now()

        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging user activity: {e}")
