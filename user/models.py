from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid

class User:
    def __init__(self, db):
        self.db = db

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if self.db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if self.db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def login(self):
        user = self.db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401
    
    def check_survey_exists(self, email):
        survey = self.db.survey.find_one({"email": email})
        if survey:
            return jsonify({"exists": True, "message": "Survey data already exists. Do you want to overwrite it?"})
        return jsonify({"exists": False})
      
    
    
      

      
