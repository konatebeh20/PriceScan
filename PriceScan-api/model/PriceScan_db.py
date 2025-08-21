import datetime
import enum
# from sqlalchemy.dialects.postgresql import UUID
import uuid
from cProfile import label
from email.policy import default
from pickle import TRUE

from sqlalchemy.sql import expression
from sqlalchemy.sql import text

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
    cat_is_featured = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
    cat_is_active = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
    cat_banner = db.Column(db.String(256))  # bannière pour la catégorie (URL ou chemin)
    cat_icon = db.Column(db.String(256), unique=True, default='')  # icône catégorie

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Méthode pour retourner la catégorie en dict (utile pour JSON)
    # def as_dict(self):
    #     return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}



class go_favorite(db.Model):
    __tablename__ = 'go_favorite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fav_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128), db.ForeignKey('go_users.u_uid'), nullable=False)
    room_uid = db.Column(db.String(128), db.ForeignKey('go_rooms.room_uid'), nullable=True)
    htl_uid = db.Column(db.String(128), db.ForeignKey('go_hotels.htl_uid'), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    # def as_dict(self):
    #     return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class go_contact_us(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ct_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    ct_name = db.Column(db.String(128))
    ct_email = db.Column(db.String(128))
    ct_subject = db.Column(db.String(255))
    ct_number = db.Column(db.String(255))
    ct_body = db.Column(db.Text)

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    # def as_dict(self):
    #    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class ps_device_tokens(db.Model):
    __tablename__ = 'ps_device_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_tokens_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128))
    device_token = db.Column(db.String(255), unique=True)  # The APNs/FCM token
    device_type = db.Column(db.String(50))  # e.g., "ios" or "android"
    is_active = db.Column(db.Boolean, default=True)  # Whether the token is active
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow) # When the token was created
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow) # When it was last updated

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
    # u_status = db.Column(db.Text(), nullable=False, default=0)
    u_status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.INACTIVE)
    u_password = db.Column(db.String(128))
    u_first_login = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    u_id_scan = db.Column(db.Text())
    is_active = db.Column(db.Boolean, default=True) 
    deleted_at = db.Column(db.DateTime, nullable=True)  
    device_token = db.Column(db.String(128))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    # u_is_verified = db.Column(db.Boolean, default=False)
    # u_is_active = db.Column(db.Boolean, default=True)
    # u_is_deleted = db.Column(db.Boolean, default=False)
    # u_is_banned = db.Column(db.Boolean, default=False)
    # u_is_active = db.Column(db.Boolean, default=True)
    # u_is_deleted = db.Column(db.Boolean, default=False)
    # u_is_banned = db.Column(db.Boolean, default=False)

    # def as_dict(self):
    #    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class ps_favorite(db.Model):
    __tablename__ = 'ps_favorite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fav_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128), db.ForeignKey('ps_users.u_uid'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    # def as_dict(self):
    #     return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class ps_notification(db.Model):
    __tablename__ = 'ps_notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notification_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    header = db.Column(db.String(128))
    body = db.Column(db.Text())
    destined_for = db.Column(db.String(128))
    status = db.Column(db.String(128))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # def as_dict(self):
    #    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}