from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import psycopg2  

load_dotenv()

db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__)

    
    try:
        app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')  
        
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT', 5432)  
        db_name = os.getenv('DB_NAME')
       
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    except KeyError as e:
        print(f"Error: {e}")

    

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  

    @login_manager.user_loader
    def load_user(user_id):
        from api.models import Customer  
        return Customer.query.get(int(user_id))

    from api.routes import views, auth, admin  
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    db.init_app(app)
    test_db_connection(app)

    with app.app_context():
        db.create_all()  

    return app

def test_db_connection(app):
    """Test the database connection"""
    try:
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT', 5432)
        db_name = os.getenv('DB_NAME')

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
