from datetime import date

from flask import render_template, flash, redirect, url_for, g
from flask.ext.login import login_required

from app import app, db, models
from app.forms.user_management import UserForm, PersonForm, DoctorPatientForm
from app.views.util.login import requires_roles, mustMatchOrPrivilegeError
from app.views.util.selectors import personChoicesForSelectField, selectPersonsWhoAreDoctors, selectPersonsWhoArePatients


@app.route('/user_management')
@login_required
@requires_roles('a')
def user_management():
    """Render user management main page."""
    return render_template('user_management.html')


@app.route('/user/list')
@login_required
@requires_roles('a')
def list_users():
    """List all users."""
    users = models.User.query.all()
    return render_template('list_users.html', users=users)


@app.route('/person/list')
@login_required
@requires_roles('a')
def list_persons():
    """List all persons."""
    persons = models.Person.query.all()
    return render_template('list_persons.html', persons=persons)


@app.route('/user/add', methods=['GET', 'POST'])
@app.route('/person/<personId>/add/user', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def add_user(personId=None):
    """
    Add a user.
    :param personId: If this is supplied, autofills in the personID in the form.
    :return: Edit user template with "Add" action.
    """
    form = UserForm(person_id=personId)
    form.person_id.choices = personChoicesForSelectField()
    if form.validate_on_submit():
        user = models.User()
        form.populate_obj(user)
        user.date_registered = date.today()
        db.session.add(user)
        db.session.commit()
        flash(u'Data has been saved for User {}'.format(form.user_name.data))
        return redirect(url_for('user_management'))
    return render_template('edit_user.html', form=form, actionName="Add")


@app.route('/person/add', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def add_person():
    """
    Add a person.
    Requires admin privileges.
    :return: Edit person template with "Add" action.
    """
    form = PersonForm()
    if form.validate_on_submit():
        person = models.Person()
        form.populate_obj(person)
        db.session.add(person)
        db.session.commit()
        flash(u'Data has been saved for Person {} {}'.format(form.first_name.data,
                                                             form.last_name.data))
        return redirect(url_for('user_management'))
    return render_template('edit_person.html', form=form, actionName="Add")


@app.route('/user/<userName>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(userName):
    """
    Edit a user.
    :param userName: user name of person to edit.
    :return: Edit user template with "Edit" action.
    """
    # Users should only be able to edit themselves unless admin
    mustMatchOrPrivilegeError(g.user.user_name, userName)

    user = models.User.query.get_or_404(userName)
    form = UserForm(obj=user)
    form.person_id.choices = personChoicesForSelectField()
    if form.validate_on_submit():
        flash(u'Saving data for User {}'.format(form.user_name.data))
        form.populate_obj(user)
        db.session.commit()
        flash(u'Data has been saved for User {}'.format(form.user_name.data))
        return redirect(url_for('user_management'))
    return render_template('edit_user.html', form=form, actionName="Edit")


@app.route('/person/<personId>/edit', methods=['GET', 'POST'])
@login_required
def edit_person(personId):
    """
    Edit a person.
    :param personId: id of person to edit.
    :return: Edit person template with "Edit" action.
    """
    mustMatchOrPrivilegeError(g.user.person_id, personId)
    person = models.Person.query.get_or_404(personId)
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        form.populate_obj(person)
        db.session.commit()
        flash(u'Data has been saved for Person {} {}'.format(form.first_name.data,
                                                             form.last_name.data))
        return redirect(url_for('user_management'))
    return render_template('edit_person.html', form=form, actionName="Edit")


@app.route('/person/<personId>/detail')
@login_required
def person_detail(personId):
    """
    View details of a person.
    :param personId: id of person details to view.
    :return: Person detail template with list of doctors and patients.
    """
    mustMatchOrPrivilegeError(g.user.person_id, personId)
    person = models.Person.query.get_or_404(personId)
    return render_template('person_detail.html',
                           person=person,
                           doctorList=", ".join([str(d.person_id) for d in person.doctors]),
                           patientList=", ".join([str(p.person_id) for p in person.patients]))


@app.route('/user/<userName>/delete', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def delete_user(userName):
    """
    Delete a user.
    :param userName: user name of user to delete.
    :return: Delete warning dialogue page.
    """
    user = models.User.query.get_or_404(userName)
    form = UserForm(obj=user)
    if form.is_submitted():
        db.session.delete(user)
        db.session.commit()
        flash(u'{} has been deleted'.format(userName))
        return redirect(url_for('user_management'))
    return render_template('delete_warning.html',
                           form=form,
                           objType="User",
                           objId=userName)


@app.route('/person/<personId>/delete', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def delete_person(personId):
    """
    Delete a person.
    :param personId: id of person to delete.
    :return: Delete warning dialogue page.
    """
    person = models.Person.query.get_or_404(personId)
    form = PersonForm(obj=person)
    if form.is_submitted():
        db.session.delete(person)
        db.session.commit()
        flash(u'{} has been deleted'.format(personId))
        return redirect(url_for('user_management'))
    return render_template('delete_warning.html',
                           form=form,
                           objType="Person",
                           objId=personId)


@app.route('/doctor_patient/list')
@login_required
@requires_roles('a')
def list_doctor_patients():
    """
    List doctor patient relationships.
    :return: List doctor patient relationship template.
    """
    docPatRels = models.Doctor.query.all()
    return render_template('list_doctor_patients.html', docPatRels=docPatRels)


@app.route('/doctor_patient/add', methods=['GET', 'POST'])
@app.route('/doctor/<doctorId>/patient/<patientId>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def add_edit_doctor_patient_relation(doctorId=None, patientId=None):
    """
    Add or edit a doctor patient relationship.
    :param doctorId: id of doctor in relationship.
    :param patientId: id of patient in relationship.
    :return: If doctorId and patientId are given, return the template with
        these fields prepopulated. Else return a template for adding a
        relationship.
    """
    # Are we editing or adding?
    editing = True if doctorId and patientId else False

    # Want just doctors selectable on the left select field
    doctors = selectPersonsWhoAreDoctors()
    doctorChoices = personChoicesForSelectField(doctors)

    patients = selectPersonsWhoArePatients()
    choices = personChoicesForSelectField(patients)

    if editing:
        # setup the template for editing
        docPatRel = models.Doctor.query.get((doctorId, patientId))
        form = DoctorPatientForm(obj=docPatRel)
        actionName = "Edit"
    else:
        # setup the template for adding
        docPatRel = models.Doctor()
        form = DoctorPatientForm()
        actionName = "Add"

    form.doctor_id.choices = doctorChoices
    form.patient_id.choices = choices
    if form.is_submitted():
        form.populate_obj(docPatRel)
        if not editing:
            db.session.add(docPatRel)
        db.session.commit()
        return redirect(url_for('list_doctor_patients'))
    return render_template('edit_doctor_patient.html', form=form, actionName=actionName)


@app.route('/doctor/<doctorId>/patient/<patientId>/delete', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def delete_doctor_patient_relation(doctorId, patientId):
    """
    Delete a doctor patient relationship.
    :param doctorId: id of doctor in relationship.
    :param patientId: id of patient in relationship.
    :return: Delete warning dialogue.
    """
    docPatRel = models.Doctor.query.get_or_404((doctorId, patientId))
    form = DoctorPatientForm(obj=docPatRel)
    if form.is_submitted():
        db.session.delete(docPatRel)
        db.session.commit()
        flash(u'Doctor {} Patient {} relation has been deleted'.format(doctorId, patientId))
        return redirect(url_for('list_doctor_patients'))
    return render_template('delete_warning.html',
                           form=form,
                           objType="Doctor Patient Relation",
                           objId="{} <-> {}".format(doctorId, patientId))
