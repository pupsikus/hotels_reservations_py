from sqlalchemy import and_, or_

from settings.set_db import Session
from models.base_models import RoomReservation
from utils.utils import check_dates_range, check_int, check_string


class Visitor:
    """
    Hotel visitor with all necessary for registration fields.
    All fields are checked on initialization step
    """
    def __init__(self, first_name, last_name, room_number,
                 start_date, end_date):
        err_list = []
        err_list.extend(check_string(in_value=first_name, name='First Name'))
        err_list.extend(check_string(in_value=last_name, name='Last Name'))
        err_list.extend(check_int(in_value=room_number, name='Room number'))
        dates_errors, start_date, end_date = check_dates_range(start_date, end_date)
        err_list.extend(dates_errors)
        if err_list:
            raise ValueError(err_list)

        self.first_name = first_name
        self.last_name = last_name
        self.room_number = room_number
        self.start_date = start_date
        self.end_date = end_date


class Reservation:
    def __init__(self):
        self.session = Session()

    def create(self, visitor):
        """
        :param visitor: Visitor object with reservation info
        :type visitor: Visitor
        :return:
        """
        err_list = []
        err_list.extend(self._check_reserve(
            room_num=visitor.room_number,
            new_start_date=visitor.start_date,
            new_end_date=visitor.end_date))
        if err_list:
            return err_list

        new_reserve = [RoomReservation(
            first_name=visitor.first_name,
            last_name=visitor.last_name,
            room_number=visitor.room_number,
            start_date=visitor.start_date, end_date=visitor.end_date
        )]
        self._commit_session_add(new_reserve)

        return err_list

    def delete(self, visitor):
        """
        :param visitor: Visitor object with reservation info
        :type visitor: Visitor
        :return:
        """
        reservation, _err_list = self.get_reserve(visitor)
        if _err_list:
            return _err_list

        self.session.delete(reservation)
        self.session.commit()

        return []

    def update(self, visitor, visitor_update):
        """

        :param visitor:
        :type visitor: Visitor
        :param visitor_update:
        :type visitor_update: Visitor
        :return:
        """
        current_reserve, _err_list = self.get_reserve(visitor)
        if _err_list:
            return _err_list

        reservations = self._get_crossed_reservations(
            room_num=visitor_update.room_number,
            new_start_date=visitor_update.start_date,
            new_end_date=visitor_update.end_date
        )
        if len(reservations) > 1:
            _err_list.append(ValueError(
                "Cannot update reserve as it  crosses reservation from "
                "another visitor"))
        if _err_list:
            return _err_list

        if reservations:
            if reservations[0] != current_reserve:
                _err_list.append(ValueError(
                    "Cannot update reserve as it  crosses reservation from "
                    "another visitor"))
                return _err_list

        current_reserve.first_name = visitor_update.first_name
        current_reserve.last_name = visitor_update.last_name
        current_reserve.room_number = visitor_update.room_number
        current_reserve.start_date = visitor_update.start_date
        current_reserve.end_date = visitor_update.end_date

        self.session.commit()
        all = self.session.query(RoomReservation).filter_by().all()
        print(all)
        return []

    def _get_crossed_reservations(self, room_num, new_start_date, new_end_date):
        """
        Check cross reservation, reservation dates must not be crossed in
        range.
        It is OK if some new start reservation date equals some previous end
        reservation date, as new reserve starts at 2 p.m at the same day as
        previous reserve ends (at 12 a.m)
        """
        reserved = self.session.query(RoomReservation).filter(
            and_(
                RoomReservation.room_number == room_num,
                or_(
                    and_(
                        RoomReservation.start_date < new_end_date,
                        RoomReservation.end_date >= new_end_date
                    ),
                    and_(
                        RoomReservation.end_date > new_start_date,
                        RoomReservation.start_date <= new_start_date
                    )
                )
            )
        ).all()

        return reserved

    def get_reserve(self, visitor):
        """
        :param visitor: Visitor object with reservation info
        :type visitor: Visitor
        :return: RoomReservation | None, list
        """
        _err_list = []

        reserved = self.session.query(RoomReservation).filter(
            RoomReservation.room_number == visitor.room_number,
            RoomReservation.start_date == visitor.start_date,
            RoomReservation.end_date == visitor.end_date).one_or_none()

        if reserved is None:
            _msg = ('Reservation not found for the room = {room}, '
                    'start_date: {start_date}, end_data={end_date}').format(
                room=visitor.room_number, start_date=visitor.start_date,
                end_date=visitor.end_date)
            _err_list.append(ValueError(_msg))

        return reserved, _err_list

    def _check_reserve(self, room_num, new_start_date, new_end_date):
        err_list = []
        reserved = self._get_crossed_reservations(room_num, new_start_date,
                                                  new_end_date)
        if reserved:
            err_list.append(ValueError('Room reservation rejection. Room is '
                                       'already reserved'))
        return err_list

    def _commit_session_add(self, obj_list):
        self.session.add_all(obj_list)
        self.session.commit()