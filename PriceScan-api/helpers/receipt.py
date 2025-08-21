import json
import re
from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

import pytesseract
from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np

from config.db import db
from config.constant import *
# from config.constant import OCR_API_KEY, OCR_API_URL
from model.PriceScan_db import *
from helpers.mailer import *
# from helpers.mailer import send_mailer_custom


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
        activity = ps_user_activity_log()
        activity.user_id = user_id
        activity.activity_type = activity_type
        activity.metadata = json.dumps(metadata) if metadata else None
        activity.created_at = datetime.now()

        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging user activity: {e}")

def process_receipt_image(receipt_id, image_data):
    """
    Traitement OCR du reçu et extraction des articles
    """
    try:
        receipt = receipts.query.filter_by(receipt_id=receipt_id).first()
        if not receipt:
            return

        receipt.status = "processing"
        db.session.commit()

        # Préparer l'image (selon si c'est une URL ou base64)
        if image_data.startswith('http'):
            # Télécharger l'image depuis l'URL
            response = requests.get(image_data)
            img = Image.open(BytesIO(response.content))
        else:
            # Décoder l'image base64
            import base64
            img_data = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            img = Image.open(BytesIO(img_data))

        # Prétraitement de l'image pour améliorer l'OCR
        img = preprocess_image(img)
        
        # Utiliser un service OCR spécialisé (Google Vision, Azure Form Recognizer, etc.)
        # ou Tesseract en fallback
        extracted_text = extract_text_with_ocr(img)
        
        # Parser le texte pour extraire les articles et prix
        items = parse_receipt_text(extracted_text)
        
        # Enregistrer les articles
        for item in items:
            new_item = receipt_items()
            new_item.receipt_id = receipt_id
            new_item.product_name = item.get("product_name")
            new_item.quantity = item.get("quantity", 1)
            new_item.unit_price = item.get("unit_price", 0.0)
            new_item.total_price = item.get("total_price", new_item.quantity * new_item.unit_price)
            db.session.add(new_item)
            
            # Ajouter aussi aux soumissions de prix pour la comparaison
            add_to_price_submissions(
                receipt.user_id, 
                item.get("product_name"), 
                item.get("unit_price"),
                receipt.store_name,
                receipt.purchase_date
            )

        # Mettre à jour le statut
        receipt.status = "completed"
        receipt.processed_at = datetime.now()
        db.session.commit()
        
        # Attribuer des points de fidélité
        award_loyalty_points(receipt.user_id, len(items), "receipt_processing")
        
        # Log activity
        log_user_activity(receipt.user_id, "receipt_processed", {
            "receipt_id": receipt_id, 
            "items_count": len(items)
        })

    except Exception as e:
        receipt.status = "failed"
        receipt.error_message = str(e)
        db.session.commit()
        print(f"Error processing receipt {receipt_id}: {e}")

def preprocess_image(img):
    """
    Prétraiter l'image pour améliorer la précision de l'OCR
    """
    # Convertir en numpy array pour OpenCV
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Seuillage adaptatif pour mieux gérer les variations d'éclairage
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Retourner à PIL Image
    return Image.fromarray(thresh)

def extract_text_with_ocr(img):
    """
    Extraire le texte d'une image en utilisant OCR
    """
    try:
        # Essayer d'abord avec un service cloud (meilleure précision)
        if OCR_API_KEY and OCR_API_URL:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            response = requests.post(
                OCR_API_URL,
                headers={"Authorization": f"Bearer {OCR_API_KEY}"},
                files={"image": buffered.getvalue()},
                data={"language": "fr"}
            )
            if response.status_code == 200:
                return response.json().get("text", "")
    except:
        pass  # Fallback à Tesseract
    
    # Fallback à Tesseract
    return pytesseract.image_to_string(img, lang='fra')

def parse_receipt_text(text):
    """
    Parser le texte du reçu pour extraire les articles et prix
    Cette fonction devra être adaptée selon les formats de tickets
    """
    items = []
    lines = text.split('\n')
    
    # Expressions régulières pour détecter les articles et prix
    price_pattern = r'(\d+[\.,]\d{2})'
    product_pattern = r'[A-Za-zÉÈÊËéèêëÀÂÄàâäÎÏîïÔÖôöÙÛÜùûüÇç\s]+'
    
    current_product = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Chercher des prix dans la ligne
        prices = re.findall(price_pattern, line)
        if prices:
            # Chercher un nom de produit (avant le premier prix)
            product_part = line.split(prices[0])[0].strip()
            if product_part and len(product_part) > 2:  # Filtrer les trop courts
                product_name = re.findall(product_pattern, product_part)
                if product_name:
                    product_name = product_name[0].strip()
                    # Nettoyer le prix
                    price = float(prices[0].replace(',', '.'))
                    
                    items.append({
                        "product_name": product_name,
                        "unit_price": price,
                        "quantity": 1,
                        "total_price": price
                    })
    
    return items

def add_to_price_submissions(user_id, product_name, price, store_name, date):
    """
    Ajouter les articles extraits à la table des soumissions de prix
    """
    try:
        submission = price_submissions()
        submission.user_id = user_id
        submission.product_name = product_name
        submission.price = price
        submission.store_name = store_name
        submission.source = "receipt_scan"
        submission.submission_date = date
        submission.created_at = datetime.now()
        submission.is_verified = True  # Les prix de tickets sont considérés vérifiés
        
        db.session.add(submission)
        db.session.commit()
    except Exception as e:
        print(f"Error adding to price submissions: {e}")

def award_loyalty_points(user_id, items_count, activity_type):
    """
    Attribuer des points de fidélité pour le traitement d'un ticket
    """
    try:
        user = ps_users.query.filter_by(user_id=user_id).first()
        if user:
            # 5 points par article + bonus de 50 points pour le ticket
            points = (items_count * 5) + 50
            user.loyalty_points += points
            user.total_submissions += items_count
            db.session.add(user)
            db.session.commit()
            
            log_user_activity(user_id, "loyalty_points_awarded", {
                "points": points,
                "reason": activity_type,
                "items_count": items_count
            })
    except Exception as e:
        print(f"Error awarding loyalty points: {e}")

@jwt_required()
def get_receipt_status(receipt_id):
    """
    Vérifier le statut de traitement d'un reçu
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        receipt = receipts.query.filter_by(receipt_id=receipt_id, user_id=current_user_id).first()
        
        if not receipt:
            response["response"] = "error"
            response["error_code"] = "RC03"
            response["error_description"] = "Receipt not found"
            return response
        
        response["response"] = "success"
        response["status"] = receipt.status
        response["processed_at"] = receipt.processed_at.strftime("%Y-%m-%d %H:%M:%S") if receipt.processed_at else None
        response["items_count"] = receipt_items.query.filter_by(receipt_id=receipt_id).count()
        
        if receipt.status == "failed":
            response["error_message"] = receipt.error_message
            
    except SQLAlchemyError as e:
        response["response"] = "error"
        response["error_code"] = "RC04"
        response["error_description"] = str(e.__dict__.get("orig", e))
        
    return response

@jwt_required()
def get_user_receipts():
    """
    Récupérer tous les reçus d'un utilisateur avec statistiques
    """
    response = {}
    try:
        current_user_id = get_jwt_identity()
        user_receipts = receipts.query.filter_by(user_id=current_user_id).order_by(receipts.created_at.desc()).all()

        receipts_data = []
        for r in user_receipts:
            items_count = receipt_items.query.filter_by(receipt_id=r.receipt_id).count()
            receipts_data.append({
                "receipt_id": r.receipt_id,
                "store_name": r.store_name,
                "total_amount": r.total_amount,
                "purchase_date": r.purchase_date.strftime("%Y-%m-%d"),
                "image_url": r.image_url,
                "status": r.status,
                "items_count": items_count,
                "processed_at": r.processed_at.strftime("%Y-%m-%d %H:%M:%S") if r.processed_at else None,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        # Statistiques
        total_receipts = len(user_receipts)
        completed_receipts = len([r for r in user_receipts if r.status == "completed"])
        total_items = sum([receipt_items.query.filter_by(receipt_id=r.receipt_id).count() 
                          for r in user_receipts if r.status == "completed"])

        response["response"] = "success"
        response["receipts"] = receipts_data
        response["stats"] = {
            "total_receipts": total_receipts,
            "completed_receipts": completed_receipts,
            "total_items": total_items
        }

    except SQLAlchemyError as e:
        response["response"] = "error"
        response["error_code"] = "RC05"
        response["error_description"] = str(e.__dict__.get("orig", e))

    return response

def log_user_activity(user_id, activity_type, metadata=None):
    """
    Enregistrer l'activité utilisateur liée aux reçus
    """
    try:
        activity = ps_user_activity_log()
        activity.user_id = user_id
        activity.activity_type = activity_type
        activity.metadata = json.dumps(metadata) if metadata else None
        activity.created_at = datetime.now()

        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging user activity: {e}")
