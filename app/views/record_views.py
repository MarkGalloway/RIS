from flask import render_template, Response, request, flash, redirect, url_for, abort, send_from_directory
from flask.ext.login import login_required
from werkzeug import secure_filename

from app import app, db, models
from app.forms.upload_forms import RecordForm
from app.views.util.login import requires_roles
from app.views.util.image import resize_image_thumb, resize_image_regular
from app.views.util.selectors import personChoicesForSelectField, selectPersonsWhoAreDoctors, selectPersonsWhoAreRadiologists, selectPersonsWhoArePatients

import uuid
import os


@app.route('/record/list', methods=['GET'])
@login_required
@requires_roles('r', 'a')
def list_records():
    """
    List of all the Radiology Records
    """
    records = models.Record.query.all()
    return render_template('list_records.html', records=records)


@app.route('/record/upload', methods=['GET', 'POST'])
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

    form.patient_id.choices = patientChoices
    form.doctor_id.choices = doctorChoices
    form.radiologist_id.choices = radiologistChoices

    if form.validate_on_submit():
        # Create the Record
        record = models.Record()
        form.populate_obj(record)
        db.session.add(record)
        db.session.commit()

        # Create the images
        images = request.files.getlist("images")
        if images:
            for img in images:
                # Create Images
                file_name = str(uuid.uuid4()) + secure_filename(img.filename)
                image_file = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                img.save(image_file)
                thumb_file_name = os.path.splitext(file_name)[0] + ".thumbnail"
                thumb_file = os.path.splitext(image_file)[0] + ".thumbnail"
                regular_file_name = os.path.splitext(file_name)[0] + ".regular"
                regular_file = os.path.splitext(image_file)[0] + ".regular"

                # Resize
                resize_image_thumb(img, thumb_file)
                resize_image_regular(img, regular_file)

                image = models.Image(record_id=record.record_id,
                                     thumbnail=thumb_file_name.encode('utf-8'),
                                     regular_size=regular_file_name.encode('utf-8'),
                                     full_size=file_name.encode('utf-8'))
                db.session.add(image)

        db.session.commit()

        flash(u'Record {} has been saved'.format(record.record_id))
        return redirect(url_for('list_records'))

    return render_template('upload_record.html', title='Upload a Record', form=form)


@app.route('/record/<id>/delete', methods=['GET', 'POST'])
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
        # Delete the record's images
        for image in record.images:
            db.session.delete(image)
            db.session.commit()

        # Delete the record
        db.session.delete(record)
        db.session.commit()
        flash(u'{} has been deleted'.format(id))
        return redirect(url_for('list_records'))
    return render_template('delete_warning.html', form=form, objType="Record", objId=id)


@app.route('/image/<int:image_id>/full')
@login_required
@requires_roles('r', 'a')
def full_img(image_id):
    """
    Returns a full size of an image from the database as a jpeg.
    :param id: id of image to display.
    """
    image = models.Image.query.get_or_404(image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], image.full_size.decode("utf-8"))


@app.route('/image/<int:image_id>/regular/<template>')
@app.route('/image/<int:image_id>/regular')
@login_required
@requires_roles('r', 'a')
def regular_img(image_id, template=""):
    """
    Returns a regular of an image from the database as a jpeg.
    :param id: id of image to display.
    """
    image = models.Image.query.get_or_404(image_id)
    if template != "":
        return render_template('regular_image.html', image=image)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], image.regular_size.decode("utf-8"))


@app.route('/image/<int:image_id>/thumbnail')
@login_required
@requires_roles('r', 'a')
def thumbnail_img(image_id):
    """
    Returns a thumbnail of an image from the database as a jpeg.
    :param id: id of image to display.
    """
    image = models.Image.query.get_or_404(image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], image.thumbnail.decode("utf-8"))
