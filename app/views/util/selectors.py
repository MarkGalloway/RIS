from app import app, db, models


def personChoicesForSelectField(persons=models.Person.query.all()):
    """
    Creates select field data for a list of persons.
    Formats the field as "ID - Last, First" to give a unique, readable entry.
    :param persons: List of persons to generate the data from.
        If not supplied, just queries the db for all persons.
    :return: Formatted list of choice tuples.
    """
    choices = []
    for person in persons:
        choices.append((person.person_id,
                        str(person.person_id) + " - " + ", ".join([person.last_name, person.first_name])))
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
