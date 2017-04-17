from unittest import TestCase
from datetime import datetime

from hotel import Reservation


class TestReservartions(TestCase):
    def setUp(self):
        self.reservetion = Reservation()
        self.reserve_data = {
            'reserve1': {
                'first_name': 'Andrey',
                'last_name': 'Voronov',
                'room_num': 51,
                'start_date': datetime(year=2017, month=5, day=2),
                'end_date': datetime(year=2017, month=5, day=15),
            },
            'reserve2': {
                'first_name': 'Tony',
                'last_name': 'Bler',
                'room_num': 51,
                'start_date': datetime(year=2017, month=5, day=7),
                'end_date': datetime(year=2017, month=5, day=13),
            }
        }

    def test_create(self):
        _err = self.reservetion.create(**self.reserve_data['reserve1'])
        self.assertEqual(_err, [], 'Has errors: "%s"' % _err)

        _err = self.reservetion.create(**self.reserve_data['reserve2'])
        self.assertNotEqual(_err, [], 'Has errors: "%s"' % _err)
