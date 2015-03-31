from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class RecordForm(Form):
    patient_id = SelectField('Patient ID', validators=[DataRequired()])
    doctor_id = SelectField('Doctor ID', validators=[DataRequired()])
    radiologist_id = SelectField('Radiologist ID', validators=[DataRequired()])
    test_type = StringField('Test Type', validators=[DataRequired(), Length(max=24)])
    prescribing_date = DateField('Prescribing Date', validators=[DataRequired()])
    test_date = DateField('Test Date', validators=[DataRequired()])
    diagnosis = StringField('Diagnosis', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1024)])

    def validate(self):
        return True


# class UploadForm(Form):
#     image        = FileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])
#     description  = TextAreaField(u'Image Description')

#     def validate_image(form, field):
#         if field.data:
#             field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

# def upload(request):
#     form = UploadForm(request.POST)
#     if form.image.data:
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)