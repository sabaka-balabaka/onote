from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha
from .auth import auth_bp
from .utils import errors_bp

db = SQLAlchemy()
login_manager = LoginManager()
store = SQLAlchemyStore(db)
captcha = FlaskSessionCaptcha()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(errors_bp, url_prefix='/error')
    app.config.from_object('config.Config')

    db.init_app(app)
    store.bind(db)
    login_manager.init_app(app)
    Session(app)
    captcha = FlaskSessionCaptcha(app)
    captcha.init_app(app)


    with app.app_context():
        from . import routes  # Import routes
        db.create_all()  # Create sql tables for our data models

        return app