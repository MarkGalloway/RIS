#!flask/bin/python
from migrate.versioning import api
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import db
from app.models import Person, User
import os.path
import datetime

db.drop_all()
db.create_all()


# if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
#     api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
#     api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# else:
#     api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

# Add Default person

person = Person(
    person_id = 1,
    first_name = "Colin",
    last_name = "Hunt",
    address = "Follow the yellow brick road",
    email = "colin@ualberta.ca",
    phone = "1231231234"
)

# Add Admin
admin = User(
    user_name = "admin",
    password = "admin",
    date_registered = datetime.date.today(),
    person_id = 1,
    user_class = 'a'
)

db.session.add(person)
db.session.add(admin)
db.session.commit()
