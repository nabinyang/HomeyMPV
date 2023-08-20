# apis/inquiry.py
"""
This module defines the Flask-RestX resources for the Home Safety Rating API.

The Home Safety Rating API provides resources for fetching safety-related data 
based on geographical location and for performing safety rating calculations 
and anomaly detection on that data.
"""
from flask_restx import Namespace, Resource
from flask import request
from db_config import db

inquiry = db.inquiry


inquiry_api = Namespace(
    name='inquiry',
    description='API for saving inquiry results'
)


@inquiry_api.route('/saveInquiry')
class Saving(Resource):
    def post(self):
        params = request.get_json()
        print(params)
        result = {}
        result['id'] = int(params['id'])
        result['inquiry_message'] = str(params['inquiry_message'])

        try: 
           print(result)
           inquiry.insert_one(result)

           return "success"
        
        except Exception as e:
            
            return e
        
