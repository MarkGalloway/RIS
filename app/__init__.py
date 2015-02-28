from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Application object
app = Flask(__name__)

# Load Config File
app.config.from_pyfile('config.py')

# DB object
db = SQLAlchemy()

# Import Views
from app import views, models
