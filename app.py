import os
import pathlib
from flask import Flask, render_template, session, redirect, request
from google_auth_oauthlib.flow import Flow
import pymongo

# Configurations
app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "797513288745-4prkpjdsael7djviefo0hh1fvu1bsbj3.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# Google Auth Setup
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# Database
client = pymongo.MongoClient('localhost', 27017)
app.db = client.user_login_system

# Routes
from user.routes import setup_routes
setup_routes(app, app.db)

# Decorators
from user.decorators import login_required

# Views
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/signout')
def signout():
    session.clear()
    return render_template('home.html')


@app.route('/login')
def login_page():
  return render_template('login.html')

@app.route('/questions/')
@login_required
def questions():
  return render_template('questions.html')

# Google login
@app.route('/google_login')
def google_login():
    from user.google_auth_setup import initiate_google_auth
    return initiate_google_auth(flow)

@app.route('/callback')
def callback():
    from user.google_auth_setup import handle_auth_callback
    return handle_auth_callback(flow, app.db)

# Survey
@app.route('/submit_survey', methods=['POST'])
@login_required
def submit_survey():
    from user.survey_handling import handle_survey_submission
    return handle_survey_submission(request, app.db)

@app.route('/check_survey', methods=['POST'])
def check_survey():
    from user.survey_handling import check_existing_survey
    return check_existing_survey(request, app.db)

if __name__ == "__main__":
    app.run(debug=True)