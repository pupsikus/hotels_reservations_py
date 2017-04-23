from datetime import datetime
import re

from utils.exceptions import *


def check_dates_range(start_date, end_date):
    """
    :type start_date: datetime
    :type end_date: datetime
    :return: corrected start_date, end_date
    """
    if not start_date:
        raise ReservationValueError('"start date" has an empty value. ')

    if not end_date:
        raise ReservationValueError('"end date" has an empty value. ')

    if type(start_date) is not datetime:
        _msg = ('"start date" has a wrong type(not a datetime). '
                '"start date" type = "%s", value = "%s"') \
               % (type(start_date), start_date)
        raise ReservationTypeError(_msg)

    if type(end_date) is not datetime:
        _msg = ('"end date" has a wrong type(not a datetime). '
                '"end date" type = "%s", value = "%s"') \
               % (type(end_date), end_date)
        raise ReservationTypeError(_msg)

    today = datetime.now().date()
    start_date = start_date.date()
    end_date = end_date.date()
    if start_date < today:
        raise ReservationValueError('"start date" is earlier than today '
                                'date')
    if end_date < start_date:
        raise ReservationValueError('"end date" is earlier than start '
                                'date')
    # TODO: check maximum number of reservations dates and other handlers
    return start_date, end_date


def check_int(in_value, name):
    """
    :param in_value: input value
    :type in_value: int
    :param name: description of the input value
    :type name: str
    """
    if not in_value:
        raise ReservationValueError('Empty value. Arg name = "%s"' % name)

    if type(in_value) is not int:
        _msg = ('Wrong argument type(not an interger). Arg name = "%s", '
                'value = "%s", type = "%s"') % (name, in_value, type(in_value))
        raise ReservationTypeError(_msg)
    # TODO: check maximum int number


def check_string(in_value, name):
    """
    :param in_value: input value
    :type in_value: str
    :param name: description of the input value
    :type name: str
    """
    if not in_value:
        raise ReservationValueError('Empty value. Arg name = "%s"' % name)

    if type(in_value) is not str:
        _msg = ('Wrong argument type(not a string). Arg name = "%s", '
                'value = "%s", type = "%s"') % (name, in_value,
                                                type(in_value))
        raise ReservationValueError(_msg)

    _failed = re.match(r'[^a-z^A-Z]', in_value)
    if _failed:
        raise ReservationValueError(
            'Wrong argument value. Arg name = "%s", value = "%s"' % (name, in_value))
    # TODO: check maximum string length
