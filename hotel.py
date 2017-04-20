import re
from datetime import datetime
from sqlalchemy import and_, or_

from settings.set_db import Session
from models.base_models import RoomReservation


class Reservation:
    def __init__(self):
        self.session = Session()

    def create(self, first_name, last_name, room_num, start_date, end_date):
        err_list = []
        err_list.extend(self._check_string(in_value=first_name, name='First Name'))
        err_list.extend(self._check_string(in_value=last_name, name='Last Name'))
        err_list.extend(self._check_int(in_value=room_num, name='Room number'))
        dates_errors, start_date, end_date = self._check_dates(start_date, end_date)
        err_list.extend(dates_errors)
        if err_list:
            return err_list

        err_list.extend(self._check_reserve(
            room_num=room_num, new_start_date=start_date, new_end_date=end_date))
        if err_list:
            return err_list

        new_reserve = [RoomReservation(
            first_name=first_name, last_name=last_name, room_number=room_num,
            start_date=start_date, end_date=end_date
        )]
        self._commit_session_add(new_reserve)

        return err_list

    def delete(self, first_name=None, last_name=None, room_num=None,
               start_date=datetime.now(), end_date=datetime.now()):
        _err_list = []
        _err_list.extend(self._check_int(in_value=room_num, name='Room number'))
        if _err_list:
            return _err_list

        reservation, _err_list = self.get_reserve(
            room_num=room_num, start_date=start_date, end_date=end_date)
        if _err_list:
            return _err_list

        self.session.delete(reservation)
        self.session.commit()

        return []

    def get_reserve(self, first_name=None, last_name=None, room_num='',
                    start_date=datetime.now(), end_date=datetime.now()):
        _err_list = []
        dates_errors, start_date, end_date = self._check_dates(
            start_date, end_date)
        _err_list.extend(dates_errors)
        if _err_list:
            return _err_list

        reserved = self.session.query(RoomReservation).filter(
            RoomReservation.room_number == room_num,
            RoomReservation.start_date == start_date,
            RoomReservation.end_date == end_date).one_or_none()
        if reserved is None:
            _msg = ('Reservation not found for the room = {room}, '
                    'start_date: {start_date}, end_data={end_date}').format(
                room=room_num, start_date=start_date, end_date=end_date)
            _err_list.append(ValueError(_msg))

        return reserved, _err_list

    def _check_reserve(self, room_num, new_start_date, new_end_date):
        err_list = []
        reserved = self.session.query(RoomReservation).filter(
            and_(
                RoomReservation.room_number == room_num,
                or_(
                    and_(
                        RoomReservation.start_date <= new_end_date,
                        RoomReservation.end_date >= new_end_date
                    ),
                    and_(
                        RoomReservation.end_date > new_start_date,
                        RoomReservation.start_date <= new_start_date
                    )
                )
            )
        ).all()
        if reserved:
            err_list.append(ValueError('Room reservation rejection. Room is '
                                       'already reserved'))
        return err_list

    def _commit_session_add(self, obj_list):
        self.session.add_all(obj_list)
        self.session.commit()

    def _check_dates(self, start_date, end_date):
        """
        :type start_date: datetime
        :type type end_date: datetime
        :return: list of errors
        :type return: list
        """
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

        if err_list:
            return err_list, start_date, end_date

        today = datetime.now().date()
        start_date = start_date.date()
        end_date = end_date.date()
        if start_date < today:
            err_list.append(ValueError('"start date" is earlier than today '
                                       'date'))
        if end_date < start_date:
            err_list.append(ValueError('"end date" is earlier than start '
                                       'date'))
        # TODO: check maximum number of reservations dates and other handlers
        return err_list, start_date, end_date

    def _check_int(self, in_value, name):
        err_list = []
        if not in_value:
            err_list.append(
                ValueError('Empty value. Arg name = "%s"' % name))
            return err_list

        if type(in_value) is not int:
            _msg = ('Wrong argument type(not an interger). Arg name = "%s", '
                    'value = "%s", type = "%s"') % (name, in_value,
                                                    type(in_value))
            err_list.append(TypeError(_msg))
        # TODO: check maximum int number
        return err_list

    def _check_string(self, in_value, name):
        err_list = []
        if not in_value:
            err_list.append(ValueError('Empty value. Arg name = "%s"' % name))
            return err_list

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
        # TODO: check maximum string length
        return err_list
