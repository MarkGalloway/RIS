from flask.ext.wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length


class UserForm(Form):
    user_name = StringField('Username', validators=[DataRequired(), Length(max=24)])
    password = StringField('Password', validators=[DataRequired(), Length(max=24)])
    person_id = SelectField('Person ID', validators=[DataRequired()], coerce=int)
    user_class = SelectField('Class',
                             choices=[('a', 'Administrator'),
                                      ('p', 'Patient'),
                                      ('d', 'Doctor'),
                                      ('r', 'Radiologist')])


class PersonForm(Form):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=24)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=24)])
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    email = StringField('Email', validators=[DataRequired(), Length(max=128)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=10)])


class DoctorPatientForm(Form):
    doctor_id = SelectField('Doctor', coerce=int)
    patient_id = SelectField('Patient', coerce=int)
