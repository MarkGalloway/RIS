from flask_wtf import Form
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
