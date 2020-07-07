from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from flask_login import LoginManager
from .models import db, Users, Notes, Content
from .auth_handler import auth_schema_handler
from .auth_handler import login_require_action

@auth_schema_handler
@app.route('/')
def default():
    return 'Hello World!'


@auth_schema_handler
@login_require_action
@app.route('/dashboard')
def dashboard():
    return 'Dashboard'


