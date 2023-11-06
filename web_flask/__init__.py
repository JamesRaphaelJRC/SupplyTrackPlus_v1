''' Handles our Flask app initializations and configurations '''
from flask import Flask
from web_flask.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Global Flask application variable: app
app = Flask(__name__)
app.config.from_object(Config)

# Global strict slashes
app.url_map.strict_slashes = False

# Intialize app with flask LoginManager to manage user logins
login = LoginManager(app)
# Set the 'login' view function as the login_view of the login instance
login.login_view = 'login'

# Set up database for 
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from web_flask.routes import *
from models.user import User
from models.vendor import Vendor
from models.order import Order
from models.review import Review
