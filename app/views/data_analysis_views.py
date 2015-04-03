from flask import render_template
from flask.ext.login import login_required

from app import app
from app.forms.data_analysis import DataAnalysis
from app.views.util.login import requires_roles
from app.views.util.selectors import selectTableRowsUsingFormForDataAnalysis


@app.route('/data_analysis', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def data_analysis():
    """Render data analysis main page."""
    form = DataAnalysis()
    data = selectTableRowsUsingFormForDataAnalysis(form)
    return render_template('dynamic_table.html', base="data_analysis_selector.html", form=form, data=data)

