from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Application object
app = Flask(__name__)

# Load Config File
app.config.from_pyfile('config.py')

# DB object
db = SQLAlchemy(app)

# Login Object
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Import Views
from app import views, models
