from flask import render_template, flash, redirect
from app import app, db, models
from .forms.login import LoginForm
from .forms.user_management import UserManagementForm



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

@app.route('/user_management', methods=['GET', 'POST'])
def userManagement():
    form = UserManagementForm()
    if form.validate_on_submit():
        person = models.Person(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            address=form.address.data,
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(person)
        db.session.commit()
    return render_template('create_edit_user.html', form=form)