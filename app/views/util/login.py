from functools import wraps
from flask import g, session, flash, redirect, request, url_for
from flask.ext.login import login_user
from werkzeug.routing import RequestRedirect


def getCurrentUserRole():
    return g.user.user_class


def privilegeError():
    """Actions to perform when user has wrong role."""
    flash("The user has insufficient privileges to access this resource.")
    raise RequestRedirect(url_for('index'))


def requires_roles(*roles):
    """
    Require that the user have the specified roles to access the view.
    http://flask.pocoo.org/snippets/98/
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if getCurrentUserRole() not in roles:
                return privilegeError()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def mustMatchOrPrivilegeError(first, second):
    """Utility function to require two things to match unless user is an admin."""
    if g.user.user_class is not 'a' and str(first) != str(second):
        return privilegeError()


def tryLogin(user, password):
    """
    Tries to log the user in with given password.
    Handles remember me.
    If successful, redirects to the requested page.
    Else, redirects to index.
    """
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
