import os

# WTForms Config
WTF_CSRF_ENABLED = True
SECRET_KEY = 'colin-is-cool'  # nobody will guess

# Database Config
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
