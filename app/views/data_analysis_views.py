from copy import copy
from datetime import date

from flask import render_template, flash, redirect, url_for, g
from flask.ext.login import login_required
from sqlalchemy import text

from app import app, db, models
from app.forms.data_analysis import DataAnalysis
from app.views.util.login import requires_roles, mustMatchOrPrivilegeError


def getData(form=None):
    """
    Builds a sql query from form parameters, executes it, and returns the results as a list.
    :param form: Form containing user selected dimensions to aggregate data by.
    :return: List of rows returned by the query.
    """
    selectFields = []
    groupByClause = []

    # SQL to create year, month, day fields
    year = "year(test_date) as year"
    month = "month(test_date) as month"
    day = "day(test_date) as day"

    # Populate selectFields and groupByClause from form
    if form.patient.data:
        selectFields.append("patient_id")
    if form.test_type.data:
        selectFields.append("test_type")
    if form.test_date.data:
        groupByClause = copy(selectFields)
        if form.test_date.data == "year":
            selectFields.append(year)
            groupByClause.append("year")
        if form.test_date.data == "month":
            selectFields.append(year)
            selectFields.append(month)
            groupByClause.append("year")
            groupByClause.append("month")
        if form.test_date.data == "day":
            selectFields.append(year)
            selectFields.append(month)
            selectFields.append(day)
            groupByClause.append("year")
            groupByClause.append("month")
            groupByClause.append("day")

    # Format the results for the SQL query
    if selectFields:
        selectFields = ",".join(selectFields) + ","
        groupByClause = "group by " + ",".join(groupByClause)

    # Plug in the selectFields and groupByClause to the query
    query = """
        SELECT {selectFields} count(*) as num_images
        from radiology_record r join pacs_images p on r.record_id = p.record_id
        {groupByClause};
        """.format(selectFields=selectFields, groupByClause=groupByClause)
    
    # debug
    print(text(query))

    # execute
    results = db.engine.execute(text(query))

    # need to reformat as list
    results = list(results)

    return results


@app.route('/data_analysis', methods=['GET', 'POST'])
@login_required
@requires_roles('a')
def data_analysis():
    """Render data analysis main page."""
    form = DataAnalysis()
    data = getData(form)
    return render_template('data_analysis.html', form=form, data=data)

