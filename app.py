from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from api.routes import views, auth, admin
# Initialize the database object
db = SQLAlchemy()

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Configure the app with the database URI and other settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

    # Initialize the database with the app
    db.init_app(app)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    # Ensure tables are created (you can comment this out once tables are created initially)
    with app.app_context():
        db.create_all()

    return app

# Create the Flask app
app = create_app()
@app.route('/')
def home():
    return render_template('home.html')  

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Specify the login view for users who are not logged in
login_manager.login_view = 'auth.login'  # Adjust according to your auth route

# Load user
@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))
# Run the app in debug mode for development
if __name__ == '__main__':
    app.run(debug=True)  # This will run your Flask app locally on http://127.0.0.1:5000/
