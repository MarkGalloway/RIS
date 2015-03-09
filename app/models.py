from app import db


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

    def __repr__(self):
        return '<User %r>' % (self.user_name)


class Doctor(db.Model):
    """To indicate who is whose family doctor"""
    __tablename__ = 'family_doctor'

    # Fields
    doctor_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'), primary_key=True)

    # Relationships
    doctor = db.relationship("Person", foreign_keys=[doctor_id], backref="doctor_doctors")
    patient = db.relationship("Person", foreign_keys=[patient_id], backref="doctor_patients")

    def __repr__(self):
        return '<FamilyDoctor %r %r>' % (self.doctor_id, self.patient_id)


class Record(db.Model):
    """To store the radiology records"""
    __tablename__ = 'radiology_record'

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
    record_id = db.Column(db.Integer, db.ForeignKey('radiology_record.record_id'), primary_key=True)
    thumbnail = db.Column(db.BLOB)
    regular_size = db.Column(db.BLOB)
    full_size = db.Column(db.BLOB)

    def __repr__(self):
        return '<Pacs Image %r %r>' % (self.image_id, self.record_id)
