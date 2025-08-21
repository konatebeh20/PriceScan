import logging
import os
import sys
from urllib import response

from config.constant import *
import pdfkit
import qrcode
import sentry_sdk
from flask import (Flask, make_response, redirect, render_template, request,session)
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sentry_sdk.integrations.flask import FlaskIntegration

from config.constant import *
from config.db import db
from helpers.mailer import *
from model.PriceScan_db import *
from resources.auth import AuthApi
# from resources.categories import CategoriesApi
from resources.favorite import FavoriteApi
# from resources.contact_us import ContactUsApi
# from resources.hotels import HotelsApi
# from resources.reports import ReportsApi
from resources.users import UsersApi
from resources.device_tokens import DeviceTokens

sentry_sdk.init(
    dsn="https://e55540efdb25abee9b6509335cfb5bae@o295794.ingest.sentry.io/4506298354499584",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

handler = logging.FileHandler('logger/app.log')  # errors logged to this file
handler.setLevel(logging.ERROR)  # only log errors and above
app.logger.addHandler(handler)

api = Api(app)

db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

#categoryApi
api.add_resource(CategoriesApi, '/api/categories/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(CategoriesApi, '/api/categories/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#userApi
api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='users_all', methods=["GET","POST"])
api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='users_all_patch', methods=["PATCH","DELETE"])

#authApi
api.add_resource(AuthApi, '/api/auth/<string:route>', endpoint='auth_all', methods=["GET","POST"])
api.add_resource(AuthApi, '/api/auth/<string:route>', endpoint='auth_all_patch', methods=["PATCH","DELETE"])


#contactUsApi
api.add_resource(ContactUsApi, '/api/contact/<string:route>', endpoint='contact_all', methods=["GET","POST"])
api.add_resource(ContactUsApi, '/api/contact/<string:route>', endpoint='contact_all_patch', methods=["PATCH","DELETE"])

#ReportsApi
api.add_resource(ReportsApi, '/api/reports/<string:route>', endpoint='reports_all', methods=["GET","POST"])
api.add_resource(ReportsApi, '/api/reports/<string:route>', endpoint='reports_all_patch', methods=["PATCH","DELETE"])

#FavoriteApi
api.add_resource(FavoriteApi, '/api/favorite/<string:route>', endpoint='favorite_all', methods=["GET","POST"])
api.add_resource(FavoriteApi, '/api/favorite/<string:route>', endpoint='favorite_all_patch', methods=["PATCH","DELETE"])

#DeviceTokens
api.add_resource(DeviceTokens, '/api/device_tokens/<string:route>', endpoint='device_tokens_all', methods=["GET","POST"])

api.add_resource(DeviceTokens, '/api/device_tokens/<string:route>', endpoint='device_tokens_all_patch', methods=["PATCH","DELETE"])

#ScraperAPI
# api.add_resource(ScraperAPI, '/api/scrape/<string:route>', endpoint='scraper_all', methods=["GET","POST"])
# api.add_resource(ScraperAPI, '/api/scrape/<string:route>', endpoint='scraper_all_patch', methods=["PATCH","DELETE"])

#PriceTrendAPI
# api.add_resource(PriceTrendAPI, '/api/price_trends/<string:route>', , endpoint='price_trend_all', methods=["GET","POST"])
# api.add_resource(PriceTrendAPI, '/api/price_trends/<string:route>', endpoint='price_trend_all_patch', methods=["PATCH","DELETE"])

@app.route(BASE_URL + '/')
def hello():
    return render_template("home.html")

# @app.route("/receipt")
# def receipt():
#     order_details = ps_orders.query.filter_by(order_reference='GO2023249627').first()
#     user = str(order_details.order_lastname) + ' ' + str(order_details.order_firstname)
#     # Data to be encoded
#     data = order_details.order_reference
#     # Encoding data using make() function
#     img = qrcode.make(data)
#     # Saving as an image file
#     img.save('static/order_qr_code.png')
    
#     print(img)
#     send_receipt(user, order_details.id, order_details)
#     return render_template("receipt.html", order_details=order_details)


@app.route("/authenticate/")
def authenticate():
    return "authentication"

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")