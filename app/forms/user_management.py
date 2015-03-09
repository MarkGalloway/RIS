from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class UserManagementForm(Form):
    user_name = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address')
    email = StringField('Email')
    phone = StringField('Phone')
    doctor_id = IntegerField('Doctor ID')