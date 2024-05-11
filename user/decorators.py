from flask import session, redirect
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session or 'google_id' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return decorated_function