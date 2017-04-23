from unittest import TestCase
from datetime import datetime

from hotel import Reservation, Visitor
from utils.exceptions import VisitorException, ReservationException


class TestReservations(TestCase):
    def setUp(self):
        """
        Initialize reservation object with CRUD methods
        and add visitors into dictionary for the later use
        """
        self.reservation = Reservation()
        try:
            delete_visitor1 = Visitor(
                first_name='Andrey', last_name='Voronov', room_number=51,
                start_date=datetime(year=2017, month=5, day=2),
                end_date=datetime(year=2017, month=5, day=15))
            fail_add_visitor2 = Visitor(
                first_name='Tony', last_name='Bler', room_number=51,
                start_date=datetime(year=2017, month=5, day=7),
                end_date=datetime(year=2017, month=5, day=13))
            read_visitor3 = Visitor(first_name='Mickle', last_name='Jordan',
                                    room_number=32,
                                    start_date=datetime(year=2017, month=6, day=2),
                                    end_date=datetime(year=2017, month=6, day=12))
            add_visitor4 = Visitor(first_name='Chuck', last_name='Norris',
                                   room_number=32,
                                   start_date=datetime(year=2017, month=6, day=14),
                                   end_date=datetime(year=2017, month=6, day=22))
            fail_update_visitor5 = Visitor(
                first_name='Chuck', last_name='Norris',
                room_number=32,
                start_date=datetime(year=2017, month=6, day=11),
                end_date=datetime(year=2017, month=6, day=17)

            )
            update_visitor6 = Visitor(
                first_name='Chuck', last_name='Norris',
                room_number=32,
                start_date=datetime(year=2017, month=6, day=12),
                end_date=datetime(year=2017, month=6, day=17)

            )
        except VisitorException:
            raise ValueError('Error during creation new visitors')

        else:
            self.reserve_data = {
                'reserve1': delete_visitor1,
                'reserve2': fail_add_visitor2,
                'reserve3': read_visitor3,
                'reserve4': add_visitor4,
                'reserve5': fail_update_visitor5,
                'reserve6': update_visitor6
            }

    def test_crud(self):
        self._create()
        self._read()
        self._update()
        self._delete()

        self._search_by_date_range()

    def _search_by_date_range(self):
        reserve = self.reservation.search_reservations_by_date_range(
            start_date=datetime(year=2017, month=5, day=2).date(),
            end_date=datetime(year=2017, month=6, day=12).date()
        )
        self.assertEqual(len(reserve), 2)

    def _update(self):
        self.assertRaises(ReservationException, self.reservation.update,
                          visitor=self.reserve_data['reserve4'],
                          visitor_update=self.reserve_data['reserve5'])

        try:
            self.reservation.update(
                visitor=self.reserve_data['reserve4'],
                visitor_update=self.reserve_data['reserve6'])
        except ReservationException:
            self.fail(str(ReservationException))
        else:
            reserve = self.reservation.get_reserve(self.reserve_data['reserve6'])
            self.assertEqual(reserve.start_date, self.reserve_data[
                'reserve6'].start_date)

    def _create(self):
        try:
            self.reservation.create(self.reserve_data['reserve1'])
            self.reservation.create(self.reserve_data['reserve3'])
            self.reservation.create(self.reserve_data['reserve4'])
        except ReservationException:
            print(str(ReservationException))
        finally:
            result = self.reservation.get_all()
            self.assertEqual(len(result), 3, 'Reservation Table misses records')

        self.assertRaises(
            ReservationException,
            self.reservation.create,
            self.reserve_data['reserve2']
        )

    def _delete(self):
        try:
            self.reservation.delete(self.reserve_data['reserve1'])
        except ReservationException:
            self.fail(str(ReservationException))
        else:
            self.assertRaises(ReservationException,
                              self.reservation.get_reserve,
                              visitor=self.reserve_data['reserve1'])

    def _read(self):
        try:
            reserved = self.reservation.get_reserve(self.reserve_data[
                'reserve3'])
        except ReservationException:
            self.fail(str(ReservationException))
        else:
            self.assertEqual(
                reserved.start_date,
                self.reserve_data['reserve3'].start_date)
