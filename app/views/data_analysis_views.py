from datetime import date

from flask import render_template, flash, redirect, url_for, g
from flask.ext.login import login_required

from app import app, db, models
from app.forms.data_analysis import DataAnalysis
from app.views.util.login import requires_roles, mustMatchOrPrivilegeError


@app.route('/data_analysis', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def data_analysis():
    """Render data analysis main page."""
    form = DataAnalysis()
    return render_template('data_analysis.html', form=form)

