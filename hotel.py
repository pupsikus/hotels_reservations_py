from sqlalchemy import and_, or_

from settings.set_db import Session
from models.base_models import RoomReservation
from utils.utils import check_dates_range, check_int, check_string
from utils.exceptions import *


class Visitor:
    """
    Hotel visitor with all necessary for registration fields.
    All fields are checked on initialization step
    """
    def __init__(self, first_name, last_name, room_number,
                 start_date, end_date):
        try:
            check_string(in_value=first_name, name='First Name')
            check_string(in_value=last_name, name='Last Name')
            check_int(in_value=room_number, name='Room number')
            start_date, end_date = check_dates_range(start_date, end_date)
        except ReservationException:
            raise VisitorException(str(ReservationException))

        self.first_name = first_name
        self.last_name = last_name
        self.room_number = room_number
        self.start_date = start_date
        self.end_date = end_date


class Reservation:
    """
    Contains all methods for CRUD operations
    """
    def __init__(self):
        self.session = Session()

    def create(self, visitor):
        """
        :param visitor: object with reservation data
        :type visitor: Visitor
        """
        reserved = self._is_reserved(
            room_num=visitor.room_number,
            start_date=visitor.start_date,
            end_date=visitor.end_date)
        if reserved:
            raise ReservationException(
                'Room reservation rejection. Room "%s" is already reserved'
                % visitor.room_number
            )

        new_reserve = [RoomReservation(
            first_name=visitor.first_name,
            last_name=visitor.last_name,
            room_number=visitor.room_number,
            start_date=visitor.start_date, end_date=visitor.end_date
        )]
        self._commit_session_add(new_reserve)

    def delete(self, visitor):
        """
        :param visitor: reservation data object
        :type visitor: Visitor
        """
        try:
            reservation = self.get_reserve(visitor)
        except ReservationException:
            raise

        self.session.delete(reservation)
        self.session.commit()

    def update(self, visitor, visitor_update):
        """
        :param visitor: old reservation data
        :type visitor: Visitor
        :param visitor_update: reservation data to update
        :type visitor_update: Visitor
        """
        try:
            current_reserve = self.get_reserve(visitor)
        except ReservationException:
            raise

        reservations = self._get_crossed_reservations(
            room_num=visitor_update.room_number,
            start_date=visitor_update.start_date,
            end_date=visitor_update.end_date
        )

        if len(reservations) > 1:
            raise ReservationValueError(
                "Cannot update reserve as it  crosses reservation from "
                "another visitor")

        if reservations:
            if reservations[0] != current_reserve:
                raise ReservationValueError(
                    "Cannot update reserve as it crosses reservation from "
                    "another visitor")

        current_reserve.first_name = visitor_update.first_name
        current_reserve.last_name = visitor_update.last_name
        current_reserve.room_number = visitor_update.room_number
        current_reserve.start_date = visitor_update.start_date
        current_reserve.end_date = visitor_update.end_date

        self.session.commit()

    def get_all(self):
        """
        :return: list of all RoomReservation objects from the table
        """
        return self.session.query(RoomReservation).filter_by().all()

    def search_reservations_by_date_range(self, start_date, end_date):
        reserved = self.session.query(RoomReservation).filter(
            or_(
                and_(
                    RoomReservation.start_date <= end_date,
                    RoomReservation.end_date >= end_date
                ),
                and_(
                    RoomReservation.end_date >= start_date,
                    RoomReservation.start_date <= start_date
                )
            )
        ).all()
        return reserved

    def _get_crossed_reservations(self, room_num, start_date, end_date):
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
                        RoomReservation.start_date < end_date,
                        RoomReservation.end_date >= end_date
                    ),
                    and_(
                        RoomReservation.end_date > start_date,
                        RoomReservation.start_date <= start_date
                    )
                )
            )
        ).all()

        return reserved

    def get_reserve(self, visitor):
        """
        :param visitor: Visitor object with reservation info
        :type visitor: Visitor
        :return: RoomReservation
        """

        reserved = self.session.query(RoomReservation).filter(
            RoomReservation.room_number == visitor.room_number,
            RoomReservation.start_date == visitor.start_date,
            RoomReservation.end_date == visitor.end_date).one_or_none()

        if reserved is None:
            _msg = ('Reservation not found for the room = {room}, '
                    'start_date: {start_date}, end_data={end_date}').format(
                room=visitor.room_number, start_date=visitor.start_date,
                end_date=visitor.end_date)
            raise ReservationException(_msg)

        return reserved

    def _is_reserved(self, room_num, start_date, end_date):
        """
        :return: bool
        """
        result = False
        reserved = self._get_crossed_reservations(room_num, start_date,
                                                  end_date)
        if reserved:
            result = True

        return result

    def _commit_session_add(self, obj_list):
        """
        Add multiple objects into database
        :param obj_list: list of objects to add into db
        """
        self.session.add_all(obj_list)
        self.session.commit()
