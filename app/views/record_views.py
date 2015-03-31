from flask import render_template, Response
from flask.ext.login import current_user, login_required

from app import app, models
from app.forms.upload_forms import RecordForm
from app.views.util.selectors import personChoicesForSelectField, selectPersonsWhoAreDoctors, selectPersonsWhoAreRadiologists, selectPersonsWhoArePatients


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Upload a new Radiology Record
    """
    form = RecordForm()

    # Populate the Form
    patients = selectPersonsWhoArePatients()
    patientChoices = personChoicesForSelectField(patients)

    doctors = selectPersonsWhoAreDoctors()
    doctorChoices = personChoicesForSelectField(doctors)

    radiologists = selectPersonsWhoAreRadiologists()
    radiologistChoices = personChoicesForSelectField(radiologists)

    form.patient_id.choices = personChoicesForSelectField()
    form.doctor_id.choices = doctorChoices
    form.radiologist_id.choices = radiologistChoices

    # Create the Record
    if form.validate_on_submit():
        record = models.Record()
        form.populate_obj(record)
        db.session.add(record)
        db.session.commit()
        flash(u'Record {} has been saved'.format(record.record_id))

    return render_template('upload_record.html', title='Upload a Record', form=form)


# @app.route('/image/<int:image_id>.jpg')
# def image(imageid):
#     jpeg_byte_string = get_avatar_or_404(user_id)
#     return Response(png_byte_string, mime_type='image/jpeg')