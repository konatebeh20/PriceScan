
import json

import requests
from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.sql.expression import null

from config.constant import *
from config.db import db
from helpers.users import *


class UsersApi(Resource):
    def post(self, route):
        if route == 'CreateUsers':
            return CreateUsers()
        
        if route == 'ReadSingleUsers':
            return get_single_user()
        
        if route == 'UpdateUsers':
            return update_user()   
        
        if route == 'VerifyUser':
            return verify_user()   
        
    def patch(self, route): 
        if route == 'UpdateUsers':
            return update_user() 

        if route == 'updatepassword':
            return UpdatePassword()   

    def delete(self, route):
        if route == 'DeleteUsers':
            return delete_users()  
        
    def get(self, route):
        if route == 'ReadUsers':
            return get_all_users()
        
        if route == 'ReadSingleUsers':
            return get_single_user()