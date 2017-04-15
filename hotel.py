import re
from datetime import datetime

from settings.set_db import Session
from models.base_models import RoomReservation


class Reservation:
    def __init__(self):
        self.session = Session()

    def create(self, first_name, last_name, room_num, start_date, end_date):
        err_list = []
        err_list.extend(self._check_string(in_value=first_name, name='First Name'))
        err_list.extend(self._check_string(in_value=last_name, name='Last Name'))
        self._check_int(in_value=room_num)
        session = Session()

    def _check_dates(self, start_date, end_date):
        err_list = []
        if not start_date:
            err_list.append(ValueError('"start date" has an empty value. '))

        if not end_date:
            err_list.append(ValueError('"end date" has an empty value. '))

        if type(start_date) is not datetime:
            _msg = ('"start date" has a wrong type(not a datetime). '
                    '"start date" type = "%s", value = "%s"') \
                   % (type(start_date), start_date)
            err_list.append(TypeError(_msg))

        if type(end_date) is not datetime:
            _msg = ('"end date" has a wrong type(not a datetime). '
                    '"end date" type = "%s", value = "%s"') \
                   % (type(end_date), end_date)
            err_list.append(TypeError(_msg))

        # TODO: check start vs end



    def _check_int(self, in_value, name):
        err_list = []
        if not in_value:
            err_list.append(
                ValueError('Empty value. Arg name = "%s"' % name))

        if type(in_value) is not int:
            _msg = ('Wrong argument type(not an interger). Arg name = "%s", '
                    'value = "%s", type = "%s"') % (name, in_value,
                                                    type(in_value))
            err_list.append(TypeError(_msg))

        return err_list

    def _check_string(self, in_value, name):
        err_list = []
        if not in_value:
            err_list.append(ValueError('Empty value. Arg name = "%s"' % name))

        if type(in_value) is not str:
            _msg = ('Wrong argument type(not a string). Arg name = "%s", '
                    'value = "%s", type = "%s"') % (name, in_value,
                                                    type(in_value))
            err_list.append(TypeError(_msg))

        _failed = re.match(r'[^a-z^A-Z]', in_value)
        if _failed:
            err_list.append(
                ValueError('Wrong argument value. Arg name = "%s", '
                           'value = "%s"' % (name, in_value))
            )
        return err_list
