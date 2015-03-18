from functools import wraps
from flask import g, session, flash, redirect, request, url_for
from flask.ext.login import login_user


def getCurrentUserRole():
    return g.user.user_class


def privilegeError():
    flash("The user has insufficient privileges to access this resource.")
    return redirect(url_for('index'))


def requires_roles(*roles):
    """http://flask.pocoo.org/snippets/98/"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if getCurrentUserRole() not in roles:
                return privilegeError()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def match_person(personIdKey):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.user.user_class is not 'a':
                if g.user.person_id is not int(kwargs.get(personIdKey)):
                    return privilegeError()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def match_user(userNameKey):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.user.user_class is not 'a':
                if g.user.user_name != kwargs.get(userNameKey):
                    return privilegeError()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def tryLogin(user, password):
    if user and user.password == password:
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        return redirect(request.args.get('next') or url_for('index'))
    else:
        flash("Invalid login. Please try again.")
        return redirect(url_for('index'))
