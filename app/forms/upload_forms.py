from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Required
from wtforms_html5 import DateField
from wtforms_html5 import DateRange
from datetime import date


class RecordForm(Form):
    patient_id = SelectField('Patient ID', validators=[DataRequired()], coerce=int)
    doctor_id = SelectField('Doctor ID', validators=[DataRequired()], coerce=int)
    radiologist_id = SelectField('Radiologist ID', validators=[DataRequired()], coerce=int)
    test_type = StringField('Test Type', validators=[DataRequired(), Length(max=24)])
    prescribing_date = DateField('Prescribing Date', default=date.today(),
                                 validators=[DateRange(date(1900, 1, 1), date(2016, 1, 1))])
    test_date = DateField('Test Date', default=date.today(),
                          validators=[DateRange(date(1900, 1, 1), date(2016, 1, 1))])
    diagnosis = StringField('Diagnosis', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1024)])
    images = FileField(u'Image Files', validators=[FileAllowed(['jpg'], 'We only support jpg!')])

    def validate(self):
        # Validate
        if not super(RecordForm, self).validate():
            # Debug Print
            print(super(RecordForm, self).errors)
            return False

        return True

# class ImageForm(Form):

#     description  = TextAreaField(u'Image Description')

#     def validate_image(form, field):
#         if field.data:
#             field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

# def upload(request):
#     form = UploadForm(request.POST)
#     if form.image.data:
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)