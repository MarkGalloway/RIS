from datetime import date
from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_required
from app import app, db, models
from app.forms.user_management import UserForm, PersonForm, DoctorPatientForm
from app.views.util.login import requires_roles


@app.route('/user_management')
@login_required
@requires_roles('a')
def user_management():
    return render_template('user_management.html')


@app.route('/list_users')
@login_required
@requires_roles('a')
def list_users():
    users = models.User.query.all()
    return render_template('list_users.html', users=users)


@app.route('/list_persons')
@login_required
@requires_roles('a')
def list_persons():
    persons = models.Person.query.all()
    return render_template('list_persons.html', persons=persons)


@app.route('/add_user', methods=['GET', 'POST'])
@app.route('/add_user/<personId>', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def add_user(personId=None):
    form = UserForm(person_id=personId)
    if form.validate_on_submit():
        user = models.User()
        form.populate_obj(user)
        user.date_registered = date.today()
        db.session.add(user)
        db.session.commit()
        flash(u'Data has been saved for User {}'.format(form.user_name.data))
        return redirect(url_for('user_management'))
    return render_template('edit_user.html', form=form, actionName="Add")


@app.route('/add_person', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def add_person():
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


@app.route('/edit_user/<userName>', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def edit_user(userName):
    user = models.User.query.get_or_404(userName)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        flash(u'Saving data for User {}'.format(form.user_name.data))
        form.populate_obj(user)
        db.session.commit()
        flash(u'Data has been saved for User {}'.format(form.user_name.data))
        return redirect(url_for('user_management'))
    else:
        form.user_name.data = user.user_name
        form.password.data = user.password
        form.user_class.data = user.user_class
        form.person_id.data = user.person_id
    return render_template('edit_user.html', form=form, actionName="Edit")


@app.route('/edit_person/<personId>', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def edit_person(personId):
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
@requires_roles('a')
def person_detail(personId):
    person = models.Person.query.get_or_404(personId)
    return render_template('person_detail.html',
                           person=person,
                           doctorList=", ".join([str(d.person_id) for d in person.doctors]),
                           patientList=", ".join([str(p.person_id) for p in person.patients]))


@app.route('/delete_user/<userName>', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def delete_user(userName):
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


@app.route('/delete_person/<personId>', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def delete_person(personId):
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


@app.route('/list_doctor_patients')
@login_required
@requires_roles('a')
def list_doctor_patients():
    docPatRels = models.Doctor.query.all()
    return render_template('list_doctor_patients.html', docPatRels=docPatRels)


@app.route('/add_doctor_patient_relation', methods=['GET', 'POST'])
@app.route('/edit/doctor/<doctorId>/patient/<patientId>', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def add_edit_doctor_patient_relation(doctorId=None, patientId=None):
    editing = True if doctorId and patientId else False
    persons = models.Person.query.all()
    choices = []
    for person in persons:
        choices.append((person.person_id, ", ".join([person.last_name, person.first_name])))

    if editing:
        docPatRel = models.Doctor.query.get((doctorId, patientId))
        form = DoctorPatientForm(obj=docPatRel)
        actionName = "Edit"
    else:
        docPatRel = models.Doctor()
        form = DoctorPatientForm()
        actionName = "Add"

    form.doctor_id.choices = choices
    form.patient_id.choices = choices
    if form.is_submitted():
        form.populate_obj(docPatRel)
        if not editing:
            db.session.add(docPatRel)
        db.session.commit()
        return redirect(url_for('list_doctor_patients'))
    return render_template('edit_doctor_patient.html', form=form, actionName=actionName)


@app.route('/delete/doctor/<doctorId>/patient/<patientId>', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def delete_doctor_patient_relation(doctorId, patientId):
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
