from unittest import TestCase
from datetime import datetime

from hotel import Reservation, Visitor


class TestReservartions(TestCase):
    def setUp(self):
        self.reservetion = Reservation()
        delete_visitor1 = Visitor(
            first_name='Andrey', last_name='Voronov', room_number=51,
            start_date=datetime(year=2017, month=5, day=2),
            end_date=datetime(year=2017, month=5, day=15))
        fail_add_visitor2 = Visitor(
            first_name='Tony', last_name='Bler',room_number=51,
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

    def _update(self):
        _err = self.reservetion.update(
            visitor=self.reserve_data['reserve4'],
            visitor_update=self.reserve_data['reserve5'])
        self.assertNotEqual(_err, [], 'Has errors: "%s"' % _err)

        _err = self.reservetion.update(
            visitor=self.reserve_data['reserve4'],
            visitor_update=self.reserve_data['reserve6'])
        self.assertEqual(_err, [], 'Has errors: "%s"' % _err)

    def _create(self):
        _err = self.reservetion.create(self.reserve_data['reserve1'])
        self.assertEqual(_err, [], 'Has errors: "%s"' % _err)

        _err = self.reservetion.create(self.reserve_data['reserve2'])
        self.assertNotEqual(_err, [], 'Has errors: "%s"' % _err)

        _err = self.reservetion.create(self.reserve_data['reserve3'])
        self.assertEqual(_err, [], 'Has errors: "%s"' % _err)

        _err = self.reservetion.create(self.reserve_data['reserve4'])
        self.assertEqual(_err, [], 'Has errors: "%s"' % _err)

    def _delete(self):
        _err = self.reservetion.delete(self.reserve_data['reserve1'])
        self.assertEqual(_err, [], 'Has errors: "%s"' % _err)

    def _read(self):
        reserved, _err = self.reservetion.get_reserve(self.reserve_data[
            'reserve3'])
        print(reserved)
        self.assertEqual(_err, [], 'Has errors: "%s"' % _err)


