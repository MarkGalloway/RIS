import os

# WTForms Config
WTF_CSRF_ENABLED = True
SECRET_KEY = 'colin-is-cool'  # nobody will guess

# Database Config
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'app.db')

# DB name: risDB
# username: 'ris_user'
# password: 'r1s_p4ssw0rd'
# Server: 45.56.81.81

# This points to MySQL, set up remotely
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://ris_user:r1s_p4ssw0rd@45.56.81.81/risDB'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Upload stuffs
# UPLOAD_FOLDER = '/Users/markgalloway/Documents/images'  # Local
UPLOAD_FOLDER = '/home/mark/static/'    # Remote
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
