from app import db


class Person(db.Model):
    """To Store Personal Information"""
    __tablename__ = 'persons'
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(24))
    last_name = db.Column(db.VARCHAR(24))
    address = db.Column(db.VARCHAR(128))
    email = db.Column(db.VARCHAR(128), unique=True)
    phone = db.Column(db.CHAR(10))
    users = db.relationship('User', backref='person', lazy='dynamic')

    def __repr__(self):
        return '<Person %r>' % (self.person_id)


class User(db.Model):
    """To store the log-in information
    Note that a person may have been assigned different
    user_name(s), depending on his/her role in the log-in"""
    __tablename__ = 'users'
    user_name = db.Column(db.VARCHAR(24), primary_key=True)
    password = db.Column(db.VARCHAR(24))
    date_registered = db.Column(db.Date)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    def __repr__(self):
        return '<User %r>' % (self.user_name)


class FamilyDoctor(db.Model):
    """To indicate who is whose family doctor"""
    __tablename__ = 'family_doctor'
    doctor_id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)

    def __repr__(self):
        return '<FamilyDoctor %r>' % (self.doctor_id)


class RadiologyRecord(db.Model):
    """To store the radiology records"""
    __tablename__ = 'radiology_record'
    record_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    radiologist_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    test_type = db.Column(db.VARCHAR(24))
    prescribing_date = db.Column(db.Date)
    test_date = db.Column(db.Date)
    diagnosis = db.Column(db.VARCHAR(128))
    description = db.Column(db.VARCHAR(1024))

    def __repr__(self):
        return '<Record %r>' % (self.record_id)


class PacsImage(db.Model):
    """To store the pacs images"""
    __tablename__ = 'pacs_images'
    record_id = db.Column(db.Integer, db.ForeignKey('radiology_record.record_id'), primary_key=True)
    image_id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.BLOB)
    regular_size = db.Column(db.BLOB)
    full_size = db.Column(db.BLOB)
