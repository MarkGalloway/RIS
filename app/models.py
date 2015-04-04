from app import db

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy

class Doctor(db.Model):
    """To indicate who is whose family doctor"""
    __tablename__ = 'family_doctor'

    # Fields
    doctor_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'), primary_key=True)

    # Relationships
    doctor = db.relationship("Person",
                             foreign_keys=[doctor_id],
                             backref=db.backref("doctor_doctors", lazy='dynamic'))
    patient = db.relationship("Person", foreign_keys=[patient_id], backref="doctor_patients")

    def __repr__(self):
        return '<FamilyDoctor %r %r>' % (self.doctor_id, self.patient_id)


class Person(db.Model):
    """To Store Personal Information"""
    __tablename__ = 'persons'

    # Fields
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(24))
    last_name = db.Column(db.VARCHAR(24))
    address = db.Column(db.VARCHAR(128))
    email = db.Column(db.VARCHAR(128), unique=True)
    phone = db.Column(db.CHAR(10))

    # Relationships
    users = db.relationship('User', backref='person')
    doctors = db.relationship('Person', secondary='family_doctor',
                              primaryjoin=person_id == Doctor.patient_id,
                              secondaryjoin=person_id == Doctor.doctor_id,
                              backref=db.backref('patients', lazy='dynamic'))

    def __repr__(self):
        return '<Person %r>' % (self.person_id)


class User(db.Model):
    """To store the log-in information
    Note that a person may have been assigned different
    user_name(s), depending on his/her role in the log-in"""
    __tablename__ = 'users'

    # Fields
    user_name = db.Column(db.VARCHAR(24), primary_key=True)
    password = db.Column(db.VARCHAR(24))
    user_class = db.Column('class', db.Enum('a', 'p', 'd', 'r'))
    date_registered = db.Column(db.Date)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))

    # Required for Flask-Login to use this as a User class
    def is_authenticated(self):
        return True

    # Required for Flask-Login to use this as a User class
    def is_active(self):
        return True

    # Required for Flask-Login to use this as a User class
    def is_anonymous(self):
        return False

    # Required for Flask-Login to use this as a User class
    def get_id(self):
        return str(self.user_name)

    def __repr__(self):
        return '<User %r>' % (self.user_name)


class Record(db.Model):
    """To store the radiology records"""
    __tablename__ = 'radiology_record'
    __searchable__ = ['test_type', 'prescriding_date', 'test_date', 'diagnosis', 'description']
    # Fields
    record_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))
    radiologist_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))
    test_type = db.Column(db.VARCHAR(24))
    prescribing_date = db.Column(db.Date)
    test_date = db.Column(db.Date)
    diagnosis = db.Column(db.VARCHAR(128))
    description = db.Column(db.VARCHAR(1024))

    # Relationships
    images = db.relationship('Image', backref="record", lazy='dynamic')
    doctor = db.relationship("Person", foreign_keys=[doctor_id], backref="record_doctor")
    patient = db.relationship("Person", foreign_keys=[patient_id], backref="record_patient")
    radiologist = db.relationship("Person", foreign_keys=[radiologist_id], backref="record_radiologist")

    def __repr__(self):
        return '<Record %r>' % (self.record_id)


class Image(db.Model):
    """To store the pacs images"""
    __tablename__ = 'pacs_images'

    image_id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('radiology_record.record_id'))
    thumbnail = db.Column(db.BLOB)
    regular_size = db.Column(db.BLOB)
    full_size = db.Column(db.BLOB)

    def __repr__(self):
        return '<Pacs Image %r %r>' % (self.image_id, self.record_id)

if enable_search:
    whooshalchemy.whoosh_index(app, Record)

