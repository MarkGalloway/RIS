from wtforms.fields.core import RadioField
from flask.ext.wtf import Form
from wtforms import BooleanField

__author__ = 'colinhunt'


class DataAnalysis(Form):
    patient = BooleanField('Patient', default=False)
    test_type = BooleanField('Test Type', default=False)
    test_date = RadioField('Test Date', choices=[('year', 'Yearly'), ('month', 'Monthly'), ('day', 'Daily')])
