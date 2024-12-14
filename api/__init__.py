from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from api.routes import views, auth, admin
from api.models import Customer, Cart, Product, Order  # Models are imported here to avoid circular imports

db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


def create_database():
    db.create_all()
    print('Database Created')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'  # Replace with a secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking of object modifications

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Load the user for login management
    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))  # Ensure the Customer model has a primary key defined

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Create the database if not created (uncomment this to auto-create tables on app start)
    with app.app_context():
        create_database()

    return app
