from wtforms.fields.core import RadioField
from flask.ext.wtf import Form
from wtforms import BooleanField

__author__ = 'colinhunt'


class DataAnalysis(Form):
    YEAR_LABEL = 'Year'
    MONTH_LABEL = 'Month'
    WEEK_LABEL = 'Week'

    patient = BooleanField('Patient', default=False)
    test_type = BooleanField('Test type', default=False)
    enable_test_date = BooleanField('Period of time', default=False)
    test_date = RadioField('Test Date', choices=[(YEAR_LABEL, YEAR_LABEL),
                                                 (MONTH_LABEL, MONTH_LABEL),
                                                 (WEEK_LABEL, WEEK_LABEL)])
