import datetime
import enum
import uuid

from sqlalchemy.sql import expression

from config.db import db


class UserStatus(enum.Enum):
    ACTIVE = 1
    INACTIVE = 0
    BANNED = -1


class ps_categories(db.Model):
    __tablename__ = "ps_categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    cat_label = db.Column(db.String(128), nullable=False)  # nom de la catégorie
    cat_description = db.Column(db.Text, nullable=True)
    cat_is_featured = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
    cat_is_active = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
    cat_banner = db.Column(db.String(256))  # bannière pour la catégorie (URL ou chemin)
    cat_icon = db.Column(db.String(256), unique=True, default='')  # icône catégorie

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ps_stores(db.Model):
    __tablename__ = "ps_stores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    store_name = db.Column(db.String(255), nullable=False)  # nom du magasin
    store_address = db.Column(db.String(255))  # adresse du magasin
    store_city = db.Column(db.String(128))  # ville du magasin
    store_country = db.Column(db.String(128), default="Côte d'Ivoire")
    store_phone = db.Column(db.String(128))  # téléphone du magasin
    store_email = db.Column(db.String(128))  # email du magasin
    store_website = db.Column(db.String(255))  # site web du magasin
    store_logo = db.Column(db.String(255))  # logo du magasin
    store_is_active = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ps_products(db.Model):
    __tablename__ = "ps_products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    product_name = db.Column(db.String(255), nullable=False)  # nom du produit
    product_description = db.Column(db.Text)  # description du produit
    product_brand = db.Column(db.String(128))  # marque du produit
    product_barcode = db.Column(db.String(128))  # code-barres du produit
    category_id = db.Column(db.Integer, db.ForeignKey("ps_categories.id"))  # catégorie du produit
    product_image = db.Column(db.String(255))  # image du produit
    product_is_active = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    category = db.relationship("ps_categories", backref="products")


class ps_prices(db.Model):
    __tablename__ = "ps_prices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.Integer, db.ForeignKey("ps_products.id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("ps_stores.id"), nullable=False)
    price_amount = db.Column(db.Float, nullable=False)  # prix du produit
    price_currency = db.Column(db.String(10), default="CFA")  # devise
    price_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)  # date du prix
    price_is_promo = db.Column(db.Boolean(), default=False)  # si c'est un prix promotionnel
    price_promo_end = db.Column(db.DateTime)  # fin de la promotion
    price_source = db.Column(db.String(50), default="manual")  # source: manual, scraper, receipt
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    product = db.relationship("ps_products", backref="prices")
    store = db.relationship("ps_stores", backref="prices")


class ps_scans(db.Model):
    __tablename__ = "ps_scans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scan_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    store_name = db.Column(db.String(128), nullable=False)   # Magasin du reçu
    total_amount = db.Column(db.Float, nullable=False)       # Montant total du reçu
    purchase_date = db.Column(db.DateTime, nullable=False)   # Date d'achat figurant sur le reçu
    scan_image = db.Column(db.String(256), nullable=True)    # Lien/nom du fichier image reçu scanné
    category_id = db.Column(db.Integer, db.ForeignKey("ps_categories.id"))  # Lien avec catégorie

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    category = db.relationship("ps_categories", backref="scans")


class ps_device_tokens(db.Model):
    __tablename__ = 'ps_device_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_tokens_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128))
    device_token = db.Column(db.String(255), unique=True)  # The APNs/FCM token
    device_type = db.Column(db.String(50))  # e.g., "ios" or "android"
    is_active = db.Column(db.Boolean, default=True)  # Whether the token is active
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow) # When the token was created
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow) # When it was last updated


class ps_users(db.Model):
    __tablename__ = 'ps_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    u_name = db.Column(db.String(128))
    u_firstname = db.Column(db.String(128))
    u_lastname = db.Column(db.String(128))
    u_username = db.Column(db.String(128), unique=True)
    u_mobile = db.Column(db.String(128))
    u_address = db.Column(db.String(128))
    u_country = db.Column(db.String(128))
    u_state = db.Column(db.String(128))
    u_city = db.Column(db.String(128))
    u_email = db.Column(db.String(128))
    u_image_link = db.Column(db.Text())
    u_status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.INACTIVE)
    u_password = db.Column(db.String(128))
    u_first_login = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    u_id_scan = db.Column(db.Text())
    is_active = db.Column(db.Boolean, default=True) 
    deleted_at = db.Column(db.DateTime, nullable=True)  
    device_token = db.Column(db.String(128))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ps_favorite(db.Model):
    __tablename__ = 'ps_favorite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fav_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128), db.ForeignKey('ps_users.u_uid'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('ps_products.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="active")
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    user = db.relationship("ps_users", backref="favorites")
    product = db.relationship("ps_products", backref="favorites")


class ps_notification(db.Model):
    __tablename__ = 'ps_notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notification_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128), db.ForeignKey('ps_users.u_uid'), nullable=False)
    header = db.Column(db.String(128))
    body = db.Column(db.Text())
    notification_type = db.Column(db.String(50))  # price_alert, promo, system, etc.
    is_read = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(128), default="sent")
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = db.relationship("ps_users", backref="notifications")


class ps_receipt(db.Model):
    __tablename__ = "ps_receipts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receipt_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))

    # Lien avec l'utilisateur qui a scanné
    u_uid = db.Column(db.String(128), db.ForeignKey("ps_users.u_uid"), nullable=False)

    # Informations sur le reçu
    store_name = db.Column(db.String(255), nullable=False)   # ex : Carrefour, Prosuma, etc.
    store_address = db.Column(db.String(255))                # optionnel
    purchase_date = db.Column(db.DateTime, nullable=True)    # date d'achat (extrait du reçu)
    total_amount = db.Column(db.Float, nullable=True)        # total du reçu
    currency = db.Column(db.String(10), default="CFA")       # devise

    # Image du reçu scanné (URL ou chemin fichier)
    receipt_image = db.Column(db.Text(), nullable=True)

    # Statut du reçu
    status = db.Column(db.String(50), default="pending")     # pending / verified / rejected

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column( db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = db.relationship("ps_users", backref="receipts")


class ps_receipt_items(db.Model):
    __tablename__ = "ps_receipt_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))

    receipt_uid = db.Column(db.String(128), db.ForeignKey("ps_receipts.receipt_uid"), nullable=False)

    product_name = db.Column(db.String(255), nullable=False)
    category_uid = db.Column(db.String(128), db.ForeignKey("ps_categories.cat_uid"), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=True)
    total_price = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    receipt = db.relationship("ps_receipt", backref="items")
    category = db.relationship("ps_categories", backref="receipt_items")


class ps_price_alerts(db.Model):
    __tablename__ = "ps_price_alerts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alert_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128), db.ForeignKey("ps_users.u_uid"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("ps_products.id"), nullable=False)
    target_price = db.Column(db.Float, nullable=False)  # prix cible pour l'alerte
    alert_type = db.Column(db.String(20), default="below")  # below, above, equal
    is_active = db.Column(db.Boolean, default=True)
    last_triggered = db.Column(db.DateTime)  # dernière fois que l'alerte a été déclenchée
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = db.relationship("ps_users", backref="price_alerts")
    product = db.relationship("ps_products", backref="price_alerts")


class ps_comparison_history(db.Model):
    __tablename__ = "ps_comparison_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comparison_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128), db.ForeignKey("ps_users.u_uid"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("ps_products.id"), nullable=False)
    compared_stores = db.Column(db.Text)  # JSON des magasins comparés
    best_price = db.Column(db.Float, nullable=False)
    best_store_id = db.Column(db.Integer, db.ForeignKey("ps_stores.id"), nullable=False)
    comparison_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    user = db.relationship("ps_users", backref="comparison_history")
    product = db.relationship("ps_products", backref="comparison_history")
    best_store = db.relationship("ps_stores", backref="comparison_history")
