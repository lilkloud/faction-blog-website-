from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from datetime import datetime
import os
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
bcrypt = Bcrypt()
csrf = CSRFProtect()
mail = Mail()

# Initialize migrate after db is created in create_app

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    migrate = Migrate(app, db)  # Initialize migrate with app and db
    mail.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Configure file uploads
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'profile_pics')
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    
    # Register blueprints
    from app.main.routes import main
    from app.auth.routes import auth
    from app.posts import posts_bp as posts
    from app.user.routes import user_bp as user_blueprint
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(posts, url_prefix='/')
    
    # Add context processor to make current_year available in all templates
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app
