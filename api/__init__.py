from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database object
db = SQLAlchemy()
engine = create_engine("postgresql:///?User=postgres&Password=admin&Database=postgres&Server=127.0.0.1&Port=5432")
DB_NAME = 'database.postgresql'

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Configure the app with the database URI and other settings
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking of object modifications

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
        db.create_all()  # Ensure tables are created (you can comment this out once tables are created initially)

    return app
