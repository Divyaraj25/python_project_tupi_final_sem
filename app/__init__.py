import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from datetime import datetime, timezone

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = 'auth.login'

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///scom_portal.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Add template context processor
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    # Register blueprints
    from app.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.admin import bp as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from app.seller import bp as seller_blueprint
    app.register_blueprint(seller_blueprint, url_prefix='/seller')
    
    # Create database tables
    with app.app_context():
        from . import models
        db.create_all()
        
        # Create default admin user if not exists
        from .models import User
        from werkzeug.security import generate_password_hash
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash(os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin123')),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
    
    return app
