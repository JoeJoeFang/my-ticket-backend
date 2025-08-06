from flask import Flask, request, jsonify, flash
# from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_mail import Mail, Message
import logging
from routes import bp as routes_blueprint
from models import db

app = Flask(__name__)

# Configure the app from the config.Config class
app.config.from_object('config.Config')

# Initialize the database with the app
db.init_app(app)

# Initialize the email with the app
mail = Mail(app)

# Initialize the password hashing with the app
# bcrypt = Bcrypt(app)

# Enable Cross-Origin Resource Sharing for the app
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",   # 本地前端开发
    "https://joejoefang.github.io"  # 部署后的前端
]}}, supports_credentials=True)

# Register the routes blueprint
app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    # Context for the app
    with app.app_context():
        # Drop all tables in the database
        # db.drop_all()
        # Create all tables in the database
        db.create_all()
        # Create a default user
        # create_default_user()
    # Initialize the email
    # Run the app with the specified host and port with debug mode on
    app.run(host='127.0.0.1', port=5005, debug=True)
    # Set the logging level for the app
    app.logger.setLevel(logging.DEBUG)