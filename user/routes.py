from flask import Blueprint
from user.models import User

user_bp = Blueprint('user', __name__)

def setup_routes(app, db):
    user_instance = User(db)

    @user_bp.route('/signup', methods=['POST'])
    def signup():
        return user_instance.signup()

    @user_bp.route('/login', methods=['POST'])
    def login_user():
        return user_instance.login()
    
    

    app.register_blueprint(user_bp, url_prefix='/user')

