from flask import render_template, flash, redirect, g, url_for, session
from flask.ext.login import current_user, login_required, logout_user

from app import app, db, lm
from app.forms.login import LoginForm
from app.models import User
from app.views.util.login import tryLogin, requires_roles


@app.route('/index')
@login_required
def index():
    """
    Display the home page.
    :return: Index template.
    """
    user = g.user  # get the currently logged in user
    return render_template("index.html",
                           title='Home',
                           user=user)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page.
    :return: Login template.
    """
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return tryLogin(User.query.get(form.username.data), form.password.data)

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    """
    Log the user out.
    :return: Redirect to index.
    """
    flash('Goodbye, %s!' % g.user.user_name)
    logout_user()
    return redirect(url_for('login'))


@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


@app.route('/test_login')
@login_required
def test_login():
    return 'You are logged in as ' + g.user.user_name


@app.route('/test_admin')
@login_required
@requires_roles('a')
def test_admin():
    return g.user.user_name + " is an admin!"


@app.route('/test_doctor')
@login_required
@requires_roles('d')
def test_doctor():
    return "Good morning Dr. " + g.user.user_name


@lm.user_loader
def load_user(id):
    """
    Used by Flask-Login to get a user by id.
    :param id: user id.
    :return: User.
    """
    return User.query.get(id)

@app.before_request
def before_request():
    """
    Anything we want to happen before every request goes here.
    """
    # Set the global user to the current user as given by Flask-Login
    # This allows us to access the current user from forms and templates
    g.user = current_user


