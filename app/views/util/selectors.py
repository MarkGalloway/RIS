from sqlalchemy import func

from app import db, models


def personChoicesForSelectField(persons=None):
    """
    Creates select field data for a list of persons.
    Formats the field as "ID - Last, First" to give a unique, readable entry.
    :param persons: List of persons to generate the data from.
        If not supplied, just queries the db for all persons.
    :return: Formatted list of choice tuples.
    """
    if not persons:
        persons = models.Person.query.all()
    choices = []
    for person in persons:
        choices.append((person.person_id,
                        str(person.person_id) + " - " + ", ".join([person.last_name, person.first_name])))
    return choices


def diagnosesForSelectField():
    results = models.Record.query.group_by(models.Record.diagnosis).all()
    choices = [('all', 'All')]
    for res in results:
        choices.append((res.diagnosis, res.diagnosis))
    return choices


def selectPersonsWhoAreDoctors():
    """
    Helper method to select all persons who are doctors.
    :return: A list of persons who are doctors.
    """
    return db.session.query(models.Person).join(models.User).filter(models.User.user_class == 'd').all()


def selectPersonsWhoAreRadiologists():
    """
    Helper method to select all persons who are radiologists.
    :return: A list of persons who are radiologists.
    """
    return db.session.query(models.Person).join(models.User).filter(models.User.user_class == 'r').all()


def selectPersonsWhoArePatients():
    """
    Helper method to select all persons who are patients.
    :return: A list of persons who are patients.
    """
    return db.session.query(models.Person).join(models.User).filter(models.User.user_class == 'p').all()


def selectTableRowsUsingFormForDataAnalysis(form):
    """
    Builds an sql query from form parameters, executes it, and returns the results as a list.
    Used for Data Analysis Module.
    :param form: Form containing user selected dimensions to aggregate data by.
    :return: List of rows returned by the query. First row is table header.
    """
    selectFields = []

    # Populate selectFields from form
    # Patient and Test Type
    if form.patient.data:
        selectFields.append(models.Record.patient_id.label(form.patient.label.text))
    if form.test_type.data:
        selectFields.append(models.Record.test_type.label(form.test_type.label.text))

    # Test Date Period
    # Hierarchy is Year, Year > Month, Year > Week
    if form.test_date.data != form.NONE_LABEL:
        # just year
        if form.test_date.data == form.YEAR_LABEL:
            selectFields.append(func.year(models.Record.test_date).label(form.YEAR_LABEL))
        # month
        if form.test_date.data == form.MONTH_LABEL:
            selectFields.append(
                func.concat(func.monthname(models.Record.test_date), ', ', func.year(models.Record.test_date)).label(
                    form.MONTH_LABEL))
        # week
        if form.test_date.data == form.WEEK_LABEL:
            selectFields.append(
                func.concat(func.weekofyear(models.Record.test_date), ', ', func.year(models.Record.test_date)).label(
                    form.WEEK_LABEL))

    # construct query
    query = db.session.query(models.Record).join(models.Image).group_by(*["`" + c.name + "`" for c in selectFields])

    # Count results as number of images
    selectFields.append(func.count('*').label("# of Images"))

    # Execute the query with the selected fields
    results = query.values(*selectFields)

    # Reformat as list of rows with a header
    # Construct header
    resultsList = [[c.name for c in selectFields]]

    # Add results from query
    resultsList += list(results)

    return resultsList


def selectPatientsUsingFormForReportGenerator(form):
    """
    Creates a list of patients with the selected diagnosis for the date range specified.
    Used by the Report Generator.
    :param form: Form containing the selected options.
    :return: List of rows returned by the query. First row is table header.
    """

    # base query
    query = db.session.query(models.Person).join(models.Person.record_patient).group_by(models.Record.diagnosis) \
        .order_by(models.Record.test_date)

    # filter by diagnosis if not 'all'
    if form.diagnosis.data != form.ALL_LABEL:
        query = query.filter(models.Record.diagnosis == form.diagnosis.data)

    # filter by date range if specified
    if form.start_date.data:
        query = query.filter(form.start_date.data <= models.Record.test_date)
    if form.end_date.data:
        query = query.filter(form.end_date.data >= models.Record.test_date)

    # header row
    resultsList = [["ID", "Last Name", "First Name", "Phone", "Address", "Diagnosis Date"]]

    # get the results as tuples rather than Person objects (closer to what we want)
    results = query.values(models.Person.person_id,
                           models.Person.last_name,
                           models.Person.first_name,
                           models.Person.phone,
                           models.Person.address,
                           models.Record.test_date)
    resultsList += list(results)
    return resultsList
