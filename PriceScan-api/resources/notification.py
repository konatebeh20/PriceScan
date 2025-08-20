import json

import requests
from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.sql.expression import null

from config.constant import *
from config.db import db
from helpers.notification import *


class NotificationApi(Resource):
    
    def get(self, route):
        if route == 'readallnotification':
            return ReadAllNotification()
        
    def post(self, route):
        if route == 'createnotification':
            return CreateNotification()
        
        if route == 'readsinglenotification':
            return ReadSingleNotification()
        
        
    # def patch(self, route):
    #     if route == 'updatenotification':
    #         return UpdateNotification()
        
    def delete(self, route):
        if route == 'deletenotification':
            return DeleteNotification()
        