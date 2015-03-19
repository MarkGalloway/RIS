from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired


class UserForm(Form):
    user_name = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    person_id = SelectField('Person ID', validators=[DataRequired()])
    user_class = SelectField('Class',
                             choices=[('a', 'Administrator'),
                                      ('p', 'Patient'),
                                      ('d', 'Doctor'),
                                      ('r', 'Radiologist')])


class PersonForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])


class DoctorPatientForm(Form):
    doctor_id = SelectField('Doctor')
    patient_id = SelectField('Patient')
