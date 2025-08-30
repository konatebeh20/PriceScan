#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'envoi d'emails pour PriceScan-API
Gère l'envoi d'emails de vérification, bienvenue, et notifications
"""

import smtplib
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Configuration email (à configurer dans .env)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', 'noreply@pricescan.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'

def send_mailer_custom(email, subject, body, is_html=True):
    """
    Envoyer un email personnalisé
    
    Args:
        email (str): Adresse email du destinataire
        subject (str): Sujet de l'email
        body (str): Contenu de l'email
        is_html (bool): Si le contenu est en HTML
    """
    try:
        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = subject
        
        # Ajouter le contenu
        if is_html:
            msg.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Connexion SMTP
        if EMAIL_USE_TLS:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        
        # Authentification
        if EMAIL_PASSWORD:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
        
        # Envoi
        text = msg.as_string()
        server.sendmail(EMAIL_USER, email, text)
        server.quit()
        
        print(f"Email envoyé avec succès à {email}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email à {email}: {e}")
        return False

def send_verification_email(email, username, verification_token):
    """
    Envoyer un email de vérification
    
    Args:
        email (str): Adresse email
        username (str): Nom d'utilisateur
        verification_token (str): Token de vérification
    """
    subject = "Vérification de votre compte PriceScan"
    
    body = f"""
    <html>
    <body>
        <h2>Bonjour {username} !</h2>
        <p>Bienvenue sur PriceScan ! 🎉</p>
        <p>Pour activer votre compte, veuillez cliquer sur le lien suivant :</p>
        <p><a href="https://pricescan.com/verify?token={verification_token}">Vérifier mon compte</a></p>
        <p>Ce lien expirera dans 24 heures.</p>
        <br>
        <p>Cordialement,</p>
        <p>L'équipe PriceScan</p>
    </body>
    </html>
    """
    
    return send_mailer_custom(email, subject, body, is_html=True)

def send_welcome_email(email, username):
    """
    Envoyer un email de bienvenue
    
    Args:
        email (str): Adresse email
        username (str): Nom d'utilisateur
    """
    subject = "Bienvenue sur PriceScan ! ��"
    
    body = f"""
    <html>
    <body>
        <h2>Bonjour {username} !</h2>
        <p>Félicitations ! Votre compte PriceScan est maintenant actif. 🎉</p>
        <p>Vous pouvez maintenant :</p>
        <ul>
            <li>Scanner vos reçus pour comparer les prix</li>
            <li>Recevoir des alertes de prix</li>
            <li>Gagner des points de fidélité</li>
            <li>Participer à notre communauté</li>
        </ul>
        <br>
        <p>Merci de nous faire confiance !</p>
        <p>L'équipe PriceScan</p>
    </body>
    </html>
    """
    
    return send_mailer_custom(email, subject, body, is_html=True)

def send_password_reset_email(email, username, reset_token):
    """
    Envoyer un email de réinitialisation de mot de passe
    
    Args:
        email (str): Adresse email
        username (str): Nom d'utilisateur
        reset_token (str): Token de réinitialisation
    """
    subject = "Réinitialisation de votre mot de passe PriceScan"
    
    body = f"""
    <html>
    <body>
        <h2>Bonjour {username} !</h2>
        <p>Vous avez demandé la réinitialisation de votre mot de passe.</p>
        <p>Cliquez sur le lien suivant pour créer un nouveau mot de passe :</p>
        <p><a href="https://pricescan.com/reset-password?token={reset_token}">Réinitialiser mon mot de passe</a></p>
        <p>Ce lien expirera dans 1 heure.</p>
        <p>Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.</p>
        <br>
        <p>Cordialement,</p>
        <p>L'équipe PriceScan</p>
    </body>
    </html>
    """
    
    return send_mailer_custom(email, subject, body, is_html=True)

def send_price_alert_email(email, username, product_name, old_price, new_price, store_name):
    """
    Envoyer une alerte de prix
    
    Args:
        email (str): Adresse email
        username (str): Nom d'utilisateur
        product_name (str): Nom du produit
        old_price (float): Ancien prix
        new_price (float): Nouveau prix
        store_name (str): Nom du magasin
    """
    subject = f"🚨 Alerte de prix : {product_name}"
    
    savings = old_price - new_price
    savings_percent = (savings / old_price) * 100
    
    body = f"""
    <html>
    <body>
        <h2>Bonjour {username} !</h2>
        <p>🚨 <strong>Alerte de prix !</strong></p>
        <p>Le prix de <strong>{product_name}</strong> a baissé !</p>
        <br>
        <p><strong>Ancien prix :</strong> {old_price:.2f} €</p>
        <p><strong>Nouveau prix :</strong> {new_price:.2f} €</p>
        <p><strong>Économies :</strong> {savings:.2f} € ({savings_percent:.1f}%)</p>
        <p><strong>Magasin :</strong> {store_name}</p>
        <br>
        <p>Ne manquez pas cette opportunité ! 🛒</p>
        <br>
        <p>Cordialement,</p>
        <p>L'équipe PriceScan</p>
    </body>
    </html>
    """
    
    return send_mailer_custom(email, subject, body, is_html=True)

def send_receipt_processed_email(email, username, receipt_id, items_count, total_amount):
    """
    Envoyer une confirmation de traitement de reçu
    
    Args:
        email (str): Adresse email
        username (str): Nom d'utilisateur
        receipt_id (str): ID du reçu
        items_count (int): Nombre d'articles
        total_amount (float): Montant total
    """
    subject = f" Reçu traité : {items_count} articles"
    
    body = f"""
    <html>
    <body>
        <h2>Bonjour {username} !</h2>
        <p> Votre reçu a été traité avec succès !</p>
        <br>
        <p><strong>Détails du reçu :</strong></p>
        <p>ID : {receipt_id}</p>
        <p>Articles détectés : {items_count}</p>
        <p>Montant total : {total_amount:.2f} €</p>
        <br>
        <p>Vous avez gagné des points de fidélité ! 🎯</p>
        <p>Consultez votre profil pour voir vos économies.</p>
        <br>
        <p>Cordialement,</p>
        <p>L'équipe PriceScan</p>
    </body>
    </html>
    """
    
    return send_mailer_custom(email, subject, body, is_html=True)

def send_weekly_summary_email(email, username, stats):
    """
    Envoyer un résumé hebdomadaire
    
    Args:
        email (str): Adresse email
        username (str): Nom d'utilisateur
        stats (dict): Statistiques de la semaine
    """
    subject = " Votre résumé hebdomadaire PriceScan"
    
    body = f"""
    <html>
    <body>
        <h2>Bonjour {username} !</h2>
        <p> Voici votre résumé de la semaine :</p>
        <br>
        <p><strong>Reçus scannés :</strong> {stats.get('receipts_scanned', 0)}</p>
        <p><strong>Articles traités :</strong> {stats.get('items_processed', 0)}</p>
        <p><strong>Économies réalisées :</strong> {stats.get('total_savings', 0):.2f} €</p>
        <p><strong>Points gagnés :</strong> {stats.get('points_earned', 0)}</p>
        <br>
        <p>Continuez à scanner pour plus d'économies ! 🛒</p>
        <br>
        <p>Cordialement,</p>
        <p>L'équipe PriceScan</p>
    </body>
    </html>
    """
    
    return send_mailer_custom(email, subject, body, is_html=True)

# Fonctions de compatibilité avec l'ancien code
def send_mailer(username, email, user_validation_token):
    """Fonction de compatibilité pour l'ancien code"""
    return send_verification_email(email, username, user_validation_token)

def send_welcome_mailer(username, email):
    """Fonction de compatibilité pour l'ancien code"""
    return send_welcome_email(email, username)

def send_receipt(username, invoice, order_details, qr_code, email):
    """Fonction de compatibilité pour l'ancien code"""
    return send_receipt_processed_email(email, username, invoice, len(order_details), sum(order_details.values()))

def send_contactUs_mailer(username, email, msg):
    """Fonction de compatibilité pour l'ancien code"""
    subject = "Message de contact PriceScan"
    body = f"""
    <html>
    <body>
        <h2>Message de {username}</h2>
        <p><strong>Email :</strong> {email}</p>
        <p><strong>Message :</strong></p>
        <p>{msg}</p>
    </body>
    </html>
    """
    return send_mailer_custom(email, subject, body, is_html=True)