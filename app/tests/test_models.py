import unittest
from datetime import datetime
from app.models import User, Bean, Roast, Roaster


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.user = User(username='testuser', password='testpassword')

    def test_username(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_password_retrieval_error(self):
        with self.assertRaises(AttributeError):
            test = self.user.password

    def test_bad_password_check(self):
        self.assertFalse(self.user.check_password('badpassword'))

    def test_correct_password_check(self):
        self.assertTrue(self.user.check_password('testpassword'))


class BeanTestCase(unittest.TestCase):

    def setUp(self):
        self.bean = Bean(id=10, name='testbean', description='test description')

    def test_id(self):
        self.assertEqual(self.bean.id, 10)

    def test_name(self):
        self.assertEqual(self.bean.name, 'testbean')

    def test_description(self):
        self.assertEqual(self.bean.description, 'test description')


class RoasterTestCase(unittest.TestCase):

    def setUp(self):
        self.roaster = Roaster(id=20, name='testroaster', description='test description')

    def test_id(self):
        self.assertEqual(self.roaster.id, 20)

    def test_name(self):
        self.assertEqual(self.roaster.name, 'testroaster')

    def test_description(self):
        self.assertEqual(self.roaster.description, 'test description')


class RoastTestCase(unittest.TestCase):

    def setUp(self):
        self.bean = Bean(id=10, name='testbean', description='test description')
        self.roaster = Roaster(id=20, name='testroaster', description='test description')
        self.roast = Roast(id=30, bean=self.bean, roaster=self.roaster, start_time="7:30:00 PM",
                           start_temp=200, start_weight=200, fc_start_time="7:40:00 PM", fc_start_temp=400,
                           fc_end_time="7:45:00 PM", fc_end_temp=420, sc_start_time="7:47:00 PM",
                           sc_start_temp=430, sc_end_time="7:48:00 PM", sc_end_temp=450, end_time="7:50:00 PM",
                           end_temp=460, end_weight=154, roast_datetime=datetime(2015, 5, 6, 19, 30),
                           notes='test roast notes')

    def test_id(self):
        self.assertEqual(self.roast.id, 30)

    def test_bean(self):
        self.assertEqual(self.bean.id, 10)

    def test_roaster(self):
        self.assertEqual(self.roaster.id, 20)

    def test_start_time(self):
        self.assertEqual(self.roast.start_time, "7:30:00 PM")

    def test_start_temp(self):
        self.assertEqual(self.roast.start_temp, 200)

    def test_start_weight(self):
        self.assertEqual(self.roast.start_weight, 200)

    def test_fc_start_time(self):
        self.assertEqual(self.roast.fc_start_time, "7:40:00 PM")

    def test_fc_start_temp(self):
        self.assertEqual(self.roast.fc_start_temp, 400)

    def test_fc_end_time(self):
        self.assertEqual(self.roast.fc_end_time, "7:45:00 PM")

    def test_fc_end_temp(self):
        self.assertEqual(self.roast.fc_end_temp, 420)

    def test_sc_start_time(self):
        self.assertEqual(self.roast.sc_start_time, "7:47:00 PM")

    def test_sc_start_temp(self):
        self.assertEqual(self.roast.sc_start_temp, 430)

    def test_sc_end_time(self):
        self.assertEqual(self.roast.sc_end_time, "7:48:00 PM")

    def test_sc_end_temp(self):
        self.assertEqual(self.roast.sc_end_temp, 450)

    def test_end_time(self):
        self.assertEqual(self.roast.end_time, "7:50:00 PM")

    def test_end_temp(self):
        self.assertEqual(self.roast.end_temp, 460)

    def test_end_weight(self):
        self.assertEqual(self.roast.end_weight, 154)

    def test_roast_datetime(self):
        self.assertEqual(self.roast.roast_datetime, datetime(2015, 5, 6, 19, 30))

    def test_notes(self):
        self.assertEqual(self.roast.notes, 'test roast notes')

    def test_time_elapsed(self):
        self.assertEqual(self.roast.time_elapsed, 1200)

    def test_first_crack_start(self):
        self.assertEqual(self.roast.first_crack_start, 600)

    def test_first_crack_end(self):
        self.assertEqual(self.roast.first_crack_end, 900)

    def test_second_crack_start(self):
        self.assertEqual(self.roast.second_crack_start, 1020)

    def test_second_crack_end(self):
        self.assertEqual(self.roast.second_crack_end, 1080)

    def test_weight_loss(self):
        self.assertEqual(self.roast.weight_loss, 46)

    def test_percent_weight_loss(self):
        self.assertEqual(self.roast.percent_weight_loss, 23.0)

    def test_formatted_datetime(self):
        self.assertEqual(self.roast.formatted_datetime, '05/06/2015 07:30:00 PM')

    def test_unix_datetime(self):
        self.assertEqual(self.roast.unix_datetime, 1430940600.0)

    def test_line_chart_data(self):
        self.assertEqual(self.roast.line_chart_data(), '[{"y": 200, "x": 0, "label": "Start"}, {"y": 400, "x": 600, "label": "First Crack Start"}, {"y": 420, "x": 900, "label": "First Crack End"}, {"y": 430, "x": 1020, "label": "Second Crack Start"}, {"y": 450, "x": 1080, "label": "Second Crack End"}, {"y": 460, "x": 1200, "label": "End"}]')


if __name__ == "__main__":
    unittest.main()
