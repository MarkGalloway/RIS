from flask import Flask

# Application object
app = Flask(__name__)

# Load Config File
app.config.from_pyfile('config.py')

# Import Views
from app import views
