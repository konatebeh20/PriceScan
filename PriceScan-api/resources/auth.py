
import json

import requests
from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.sql.expression import null

from config.constant import *
from config.db import db
from helpers.auth import *
from helpers.categories import *


class AuthApi(Resource):
    def get(self, route):
        return True
        
    def post(self, route):
        if route == 'login':
            return login()
        
        if route == 'loginSocial':
            return loginSocial()
        
    def patch(self, route):
        return True
        
    def delete(self, route):
        if route == 'delete_account':
            return delete_account()
        