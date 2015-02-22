from flask import render_template, flash, redirect
from app import app
from .forms.login import LoginForm


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
