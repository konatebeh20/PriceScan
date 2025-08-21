
import json

import requests
from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.sql.expression import null

from config.constant import *
from config.db import db
from helpers.promo_room import *


class PromoDealsApi(Resource):
        
    def post(self, route):
        if route == 'readpromodeals': 
            return ReadPromoDeals()
        
        if route == 'autoupdatepromodeals':
            return AutoUpdatePromoDeals()
        

    #     if route == 'readSingleDeals':
    #         return ReadSingleDeals()  
        
    #     if route == 'readDealsusers':
    #         return getDealsByreceipt() 
        
    #     # if route == 'updateDeals':
    #     #     return UpdateDeals()
    
        
    # def get(self, route):
    #     if route == 'readpromodeals':
    #         return ReadPromoDeals()
        
        
    def patch(self, route):
        if route == 'updatepromodeals':
            return UpdatePromoDeals()
        
    # def delete(self, route):
    #     if route == 'deletedeals':
    #         return DeleteDeals()  
        