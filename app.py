from api import create_app
from flask import render_template
# Create the Flask app using the factory function
app = create_app()

# Define the root route
@app.route('/')
def home():
    return render_template('home.html')
# Run the app in debug mode for development
if __name__ == '__main__':
    app.run(debug=True)  # This will run your Flask app locally on http://127.0.0.1:5000/
