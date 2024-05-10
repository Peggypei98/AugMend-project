from flask import Flask, jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256
from app import db


class User:

  def start_session(self, user):
      del user['password']
      session['logged_in'] = True
      session['user'] = user
      return jsonify(user), 200
  
  
  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }
    
    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])
    
    
    
    # Check for existing email address
    if db.user.find_one({"email": user['email']}):
        return jsonify({"error": "Email address already in use"}), 400

    # Attempt to insert the user document
    result = db.user.insert_one(user)
    if result.acknowledged:
        return self.start_session(user)  # Ensure `start_session` is properly implemented to handle session start.

    return jsonify({"error": "Signup failed"}), 400