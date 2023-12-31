from flask import Flask, render_template
from flask_restx import Api

from templates.auth import auth_api
from templates.home_safety_rating import home_safety_rating_api 
from templates.alarm import alarm_api
from templates.survey import survey_api
from templates.inquiry import inquiry_api


app = Flask(__name__)


api = Api(
    app,
    version='0.1',
    title="Homey API",
    description="Homey API Server!",
    terms_url="/",
    contact="seungjaelim@kaist.ac.kr",
    license="MIT"
)


api.add_namespace(auth_api)
api.add_namespace(home_safety_rating_api)
api.add_namespace(survey_api)
api.add_namespace(alarm_api)
api.add_namespace(inquiry_api)


@app.route("/")
def index():
    return render_template('./index.html')



if __name__ == "__main__":
    # Send a ping to confirm a successful connection
    try:
        # client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    app.run(debug=True, host='0.0.0.0', port=5000)
