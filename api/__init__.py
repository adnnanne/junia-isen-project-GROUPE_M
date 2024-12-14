from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the database object
db = SQLAlchemy()

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Configure the app with the database URI and other settings
    
    try:
        app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')  # Secure secret key
        # Gather database credentials from environment variables
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT', 5432)  # Default to 5432 if not specified
        db_name = os.getenv('DB_NAME')
        # Construct the database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        )

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking of object modifications
    except KeyError as e:
        print(f"Error: {e}")
    

    # Initialize the database with the app
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Adjust according to your auth route

    # Load user function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from api.models import Customer  # Import inside the function to avoid circular imports
        return Customer.query.get(int(user_id))

    # Register blueprints
    from api.routes import views, auth, admin  # Import here to avoid circular imports
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    # Create the database if not created
    with app.app_context():
        db.create_all()  # Ensure tables are created (comment this out once tables are created)

    return app
