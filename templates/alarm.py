# apis/alarm.py
"""
This module defines the Flask-RestX resources for the Home Safety Rating API.

The Home Safety Rating API provides resources for fetching safety-related data 
based on geographical location and for performing safety rating calculations 
and anomaly detection on that data.
"""
from flask_restx import Namespace, Resource
from flask import request
from db_config import db



alarm = db.alarm


alarm_api = Namespace(
    name='alarm',
    description='API for saving survey results'
)


@alarm_api.route('/showAlarm')
class Saving(Resource):
    def post(self):

        params = request.get_json()

        try: 
            results = alarm.find({'id':int(params['id'])})
            if results is None:
                return 'No result'
            else: 
                list = []
                for result in results:
                    myDict = {}
                    myDict["id"] = result["id"]
                    myDict["alarm"] = result["alarm"]
                    list.append(myDict)
                return list
        except Exception as e: 
            return e
