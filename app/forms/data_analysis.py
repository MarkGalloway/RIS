from wtforms.fields.core import RadioField
from flask.ext.wtf import Form
from wtforms import BooleanField

__author__ = 'colinhunt'


class DataAnalysis(Form):
    NONE_LABEL = 'None'
    YEAR_LABEL = 'Year'
    MONTH_LABEL = 'Month'
    WEEK_LABEL = 'Week'

    patient = BooleanField('Patient', default=False)
    test_type = BooleanField('Test type', default=False)
    test_date = RadioField('Test Date', default=NONE_LABEL, choices=[(NONE_LABEL, NONE_LABEL),
                                                                     (YEAR_LABEL, YEAR_LABEL),
                                                                     (MONTH_LABEL, MONTH_LABEL),
                                                                     (WEEK_LABEL, WEEK_LABEL)])
