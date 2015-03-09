from datetime import datetime, date
from flask import render_template, flash, redirect, url_for
from app import app, db, models
from .forms.login import LoginForm
from .forms.user_management import UserForm



@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Mark'}  # fake user
    return render_template("index.html",
                           title='Home',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Debug Print
        flash('Login requested for Username="%s", remember_me=%s' %
              (form.username.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'

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
    return render_template('create_edit_user.html', form=form)