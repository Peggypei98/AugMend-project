from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system
# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')


@app.route('/questions/')
def questions():
  return render_template('questions.html')

@app.route('/view-users/')
def view_users():
    users = db.user.find()
    return render_template('view_users.html', users=users)

