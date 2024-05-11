import os
import pathlib
import requests
from flask import Flask, render_template, session, redirect, abort, request, jsonify
from functools import wraps
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import pymongo


app = Flask(__name__)


app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "797513288745-4prkpjdsael7djviefo0hh1fvu1bsbj3.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

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
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session or 'google_id' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return decorated_function



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

@app.route('/google_login')
def google_login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session.clear()
    session['google_id'] = id_info.get('sub')  # Unique identifier for the user
    session['logged_in'] = True
    session['user'] = {'_id': id_info.get('sub'), 'name': id_info.get('name'), 'email': id_info.get('email')}
    
    # Extract name and email
    user_name = id_info.get('name')
    user_email = id_info.get('email')

    # Check if user already exists in database
    existing_user = app.db.users.find_one({"email": user_email})
    if not existing_user:
        # If user does not exist, create new user entry
        app.db.users.insert_one({
            "name": user_name,
            "email": user_email,
            "google_id": session['google_id']
        })
    
    
    return render_template('questions.html')
  
  

@app.route('/submit_survey', methods=['POST'])
@login_required
def submit_survey():
    survey_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "age": request.form['age'],
        "marital_status": request.form['marital_status'],
        "other_marital_status": request.form.get('other_marital_status', ''),
        "therapy": request.form['therapy'],
        "medication": request.form['medication'],
        "medication_details": request.form.getlist('medication_name[]')
    }
    # Check if there is an existing survey with the same email
    existing_survey = app.db.survey.find_one({"email": survey_data['email']})
    if existing_survey:
        # Update the existing survey
        app.db.survey.update_one({"email": survey_data['email']}, {"$set": survey_data})
    else:
        # Insert a new survey
        app.db.survey.insert_one(survey_data)
    return render_template('thanku.html')
  
@app.route('/check_survey', methods=['POST'])
def check_survey():
    email = request.form.get('email')
    survey = app.db.survey.find_one({"email": email})
    if survey:
        return jsonify({"exists": True, "message": "Survey data already exists. Do you want to overwrite it?"})
    return jsonify({"exists": False})
  



