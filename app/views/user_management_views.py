from datetime import date
from flask import render_template, flash, redirect, url_for
from app import app, db, models
from app.forms.user_management import UserForm, PersonForm, DoctorPatientForm


@app.route('/user_management')
def user_management():
    return render_template('user_management.html')


@app.route('/list_users')
def list_users():
    users = models.User.query.all()
    return render_template('list_users.html', users=users)


@app.route('/list_persons')
def list_persons():
    persons = models.Person.query.all()
    return render_template('list_persons.html', persons=persons)


@app.route('/add_user', methods=['GET', 'POST'])
@app.route('/add_user/<personId>', methods=['GET', 'POST'])
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


@app.route('/delete_user/<userName>', methods=['GET', 'POST'])
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
def list_doctor_patients():
    docPatRels = models.Doctor.query.all()
    return render_template('list_doctor_patients.html', docPatRels=docPatRels)


@app.route('/add_doctor_patient_relation', methods=['GET', 'POST'])
def add_doctor_patient_relation():
    persons = models.Person.query.all()
    choices = []
    for person in persons:
        choices.append((person.person_id, ", ".join([person.last_name, person.first_name])))
    form = DoctorPatientForm()
    form.doctor_id.choices = choices
    form.patient_id.choices = choices
    if form.is_submitted():
        docPatRel = models.Doctor()
        form.populate_obj(docPatRel)
        db.session.add(docPatRel)
        db.session.commit()
        return redirect(url_for('list_doctor_patients'))
    return render_template('add_doctor_patient.html', form=form)
