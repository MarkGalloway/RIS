from flask import render_template
from flask.ext.login import login_required

from app import app
from app.forms.report_generator import ReportGenerator
from app.views.util.login import requires_roles
from app.views.util.selectors import selectPatientsUsingFormForReportGenerator, diagnosesForSelectField


@app.route('/report_generator', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def report_generator():
    """Render report generator main page."""
    form = ReportGenerator(diagnosis=ReportGenerator.ALL_LABEL)
    form.diagnosis.choices = diagnosesForSelectField()
    data = selectPatientsUsingFormForReportGenerator(form)
    return render_template('dynamic_table.html', base='report_generator_selector.html', form=form, data=data)

