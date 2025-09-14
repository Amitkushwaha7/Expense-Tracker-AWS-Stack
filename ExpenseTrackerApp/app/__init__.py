from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    from app.routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

from app import models