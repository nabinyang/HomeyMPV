# apis/survey.py

from flask_restx import Namespace, Resource
from flask import request
from db_config import db
from datetime import datetime
from kakao_config import api


homeSurveys = db.homeSurveys
alarm = db.alarm

survey_api = Namespace(
    name='survey',
    description='API for saving survey results'
)


@survey_api.route('/saveHomeSurvey')
class SavingHomeSurvey(Resource):
    def post(self):
        params = request.get_json()
        now = datetime.now()
        #print('now: ', now.strftime("%Y/%m/%d/%H"))
        result = {}
        result['id'] = int(params['id'])
        result['address'] = str(params['address'])
        result['dwellingType'] = str(params['dwellingType'])
        result['toiletNumber'] = str(params['toiletNumber'])
        result['floorNumber'] = str(params['floorNumber'])
        result['facility'] = list(params['facility'])
        result['standard'] = list(params['standard'])
        result['prefer1'] = str(params['prefer1'])
        result['prefer2'] = str(params['prefer2'])
        result['prefer3'] = str(params['prefer3'])
        result['prefer4'] = str(params['prefer4'])
        result['safety'] = list(params['safety'])
        result['another'] = str(params['another'])
        result['isSafety'] = str(params['isSafety'])
        result['reason'] = str(params['reason'])
        result['yesOrNo'] = list(params['yesOrNo'])
        result['timestamp'] = now.strftime("%Y/%m/%d/%H")
        result['confirm'] = False

        
        try:
            count = homeSurveys.count_documents({'id': result['id']})
            print(f'count: {count}')
            result['surveyNo'] = count + 1
            
            try:
                homeSurveys.insert_one(result)
                alarm_list = {}
                alarm_list['id'] = result['id']
                alarm_list['alarm'] = []
                alarm_list['alarm'].append({str(result['surveyNo']): '설문결과완료'})
                try: 
                    alarm.insert_one(alarm_list)
                    return "success"
                except Exception as e:
                    return e
            except Exception as e:
                return e
            
        except Exception as e:
            
            return e
        
@survey_api.route('/showHomeSurvey')
class ShowingHomeSurvey(Resource):
    def get(self):
        params = request.get_json()
        
        try:
            survey = homeSurveys.find_one({'id': int(params['id']), 'surveyNo': int(params['surveyNo'])})
            print(type(survey))
            if survey is None:
                return '저장된 결과 없음'
            else:
                result = {}
                result['id'] = survey['id']
                result['surveyNo'] = survey['surveyNo']
                result['address'] = survey['address']
                result['dwellingType'] =survey['dwellingType']
                result['toiletNumber'] = survey['toiletNumber']
                result['floorNumber'] = survey['floorNumber']
                result['facility'] = survey['facility']
                result['standard'] = survey['standard']
                result['prefer1'] = survey['prefer1']
                result['prefer2'] = survey['prefer2']
                result['prefer3'] = survey['prefer3']
                result['prefer4'] = survey['prefer4']
                result['safety'] = survey['safety']
                result['another'] = survey['another']
                result['isSafety'] = survey['isSafety']
                result['reason'] = survey['reason']
                result['yesOrNo'] = survey['yesOrNo']
                
                return result
            
        except Exception as e:
            
            return e
        
@survey_api.route('/showSurveyList')
class ShowingHomeSurvey(Resource):
    def post(self):
        params = request.get_json()
        
        try:
            surveys = homeSurveys.find({'id': int(params['id'])})
            print(type(surveys))
            
            if surveys is None:
                return '저장된 결과 없음'
            else:
                list = []
                for survey in surveys:
                    myDict = {}
                    myDict['address'] = survey['address']
                    myDict['time'] = survey['timestamp']
                    result = api.search_address(survey['address'])
                    if result['meta']['total_count'] > 0:
                        myDict['coords'] = [result['documents'][0]['y'], result['documents'][0]['x']]
                    myDict['confirm'] = survey['confirm']
                             
                    print(myDict)
                    list.append(myDict)

                return list
            
        except Exception as e:
            
            return e

