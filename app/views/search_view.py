from flask import render_template, flash, redirect, g, url_for, session
from flask.ext.login import current_user, login_required, logout_user
import sqlalchemy.orm.query

from datetime import datetime
from app import app, db, lm
from app.forms.login import LoginForm
from app.forms.search_form import SearchForm
from app.models import User, Record
from app.views.util.login import tryLogin, requires_roles

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Record.query.whoosh_search(query, 50).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
