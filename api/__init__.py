from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import psycopg2  # Import psycopg2 for PostgreSQL connection

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
    # Initialize the database with the app
    db.init_app(app)
    # Test database connection
    test_db_connection(app)

    # Create the database if not created
    with app.app_context():
        db.create_all()  # Ensure tables are created (comment this out once tables are created)

    return app

def test_db_connection(app):
    """Test the database connection"""
    try:
        # Retrieve database credentials from the app's configuration
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT', 5432)
        db_name = os.getenv('DB_NAME')

        # Attempt to connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
            
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        app.logger.info(f"Connected to PostgreSQL database. Version: {db_version[0]}")
        cursor.close()
        conn.close()
    except Exception as e:
        app.logger.error(f"Failed to connect to the database: {str(e)}")
