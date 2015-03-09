from flask import render_template, flash, redirect, url_for
from app import app, db, models
from app.forms.user_management import UserForm

@app.route('/edit_user/<userName>', methods=['GET', 'POST'])
def editUser(userName):
    user = models.User.query.get_or_404(userName)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        flash(u'Saving data for User {}'.format(form.user_name.data))
        form.populate_obj(user)
        db.session.commit()
        flash(u'Data has been saved for User {}'.format(form.user_name.data))
        return redirect(url_for('index'))
    else:
        form.user_name.data = user.user_name
        form.password.data = user.password
        form.user_class.data = user.user_class
        form.person_id.data = user.person_id
    return render_template('edit_user.html', form=form)