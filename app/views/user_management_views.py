from datetime import date
from flask import render_template, flash, redirect, url_for
from app import app, db, models
from app.forms.user_management import UserForm


@app.route('/user_management')
def user_management():
    users = models.User.query.all()
    return render_template('list_users.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = models.User()
        form.populate_obj(user)
        user.date_registered = date.today()
        db.session.add(user)
        db.session.commit()
        flash(u'Data has been saved for User {}'.format(form.user_name.data))
        return redirect(url_for('user_management'))
    return render_template('edit_user.html', form=form, actionName="Add")


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

@app.route('/delete_user/<userName>', methods=['GET', 'POST'])
def delete_user(userName):
    user = models.User.query.get_or_404(userName)
    form = UserForm(obj=user)
    if form.is_submitted():
        db.session.delete(user)
        db.session.commit()
        flash(u'{} has been deleted'.format(userName))
        return redirect(url_for('user_management'))
    return render_template('delete_user.html', form=form)