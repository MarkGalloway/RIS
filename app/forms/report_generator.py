from flask.ext.wtf import Form
from wtforms import SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

__author__ = 'colinhunt'


class ReportGenerator(Form):
    ALL_LABEL = 'all'

    diagnosis = SelectField('Diagnosis', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
