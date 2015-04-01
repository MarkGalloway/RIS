from flask import render_template, Response, request, flash, redirect, url_for
from flask.ext.login import login_required

from app import app, db, models
from app.forms.upload_forms import RecordForm
from app.views.util.login import requires_roles
from app.views.util.selectors import personChoicesForSelectField, selectPersonsWhoAreDoctors, selectPersonsWhoAreRadiologists, selectPersonsWhoArePatients


@app.route('/records/list', methods=['GET'])
@login_required
@requires_roles('r', 'a')
def list_records():
    """
    List of all the Radiology Records
    """
    records = models.Record.query.all()
    return render_template('list_records.html', records=records)


@app.route('/records/upload', methods=['GET', 'POST'])
@login_required
@requires_roles('r', 'a')
def upload_record():
    """
    Upload a new Radiology Record
    """
    form = RecordForm(request.form)

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
        print("hello")
        record = models.Record()
        form.populate_obj(record)
        db.session.add(record)

        # TODO:  Get image from request, create Image object, attach record

        db.session.commit()
        flash(u'Record {} has been saved'.format(record.record_id))
        return redirect(url_for('list_records'))

    return render_template('upload_record.html', title='Upload a Record', form=form)


@app.route('/records/<id>/delete', methods=['GET', 'POST'])
@login_required
@requires_roles('r', 'a')
def delete_record(id):
    """
    Delete a record.
    :param id: id of record to delete.
    :return: Delete warning dialogue page.
    """
    record = models.Record.query.get_or_404(id)
    form = RecordForm(obj=record)
    if form.is_submitted():
        db.session.delete(record)

        # TODO:  Add delete image

        db.session.commit()
        flash(u'{} has been deleted'.format(id))
        return redirect(url_for('list_records'))
    return render_template('delete_warning.html', form=form, objType="Record", objId=id)





# @app.route('/image/<int:image_id>.jpg')
# def image(imageid):
#     jpeg_byte_string = get_avatar_or_404(user_id)
#     return Response(png_byte_string, mime_type='image/jpeg')