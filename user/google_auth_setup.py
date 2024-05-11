from google_auth_oauthlib.flow import Flow
from flask import redirect, session, render_template
import os
import pathlib

def setup_google_auth(client_secrets_file):
    return Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri="http://127.0.0.1:5000/callback"
    )

def initiate_google_auth(flow):
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

def handle_auth_callback(flow, db):
    from flask import request, abort, session
    from google.oauth2 import id_token
    import google.auth.transport.requests
    import requests
    from pip._vendor import cachecontrol

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
        audience=os.getenv("GOOGLE_CLIENT_ID")
    )

    session.clear()
    session['google_id'] = id_info.get('sub')
    session['logged_in'] = True
    session['user'] = {'_id': id_info.get('sub'), 'name': id_info.get('name'), 'email': id_info.get('email')}

    # Extract name and email
    user_name = id_info.get('name')
    user_email = id_info.get('email')

    # Check if user already exists in the database
    existing_user = db.users.find_one({"email": user_email})
    if not existing_user:
        db.users.insert_one({
            "name": user_name,
            "email": user_email,
            "google_id": session['google_id']
        })
    
    return render_template('questions.html')
