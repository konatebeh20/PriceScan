import json

import requests
from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.sql.expression import null

from config.constant import *
from config.db import db
from helpers.favorite import *


class FavoriteApi(Resource):
        

    def post(self, route):
        if route == 'createFavorite':
            return CreateFavorite()
        
        if route == 'readSingleFavorite':
            return ReadSingleFavorite()  
        
        if route == 'readFavoriteUsers':
            return ReadFavoriteByUser() 
        #if route == 'deleteFavorite':
        #    return DeleteFavorite()  
        
        
    def get(self, route):
        if route == 'readAllFavorite':
            return ReadFavorite()  
        
    def patch(self, route):
        if route == 'updateFavorite':
            return UpdateFavorite()
        
    def delete(self, route):
        if route == 'deleteFavorite':
            return DeleteFavorite()  
        
        
        