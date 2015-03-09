from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired


class UserForm(Form):
    user_name = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    user_class = SelectField('Class',
                             choices=[('a', 'Administrator'),
                                      ('p', 'Patient'),
                                      ('d', 'Doctor'),
                                      ('r', 'Radiologist')])