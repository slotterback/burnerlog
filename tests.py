from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Report, Customer
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_create_report(self):
        u = User(username='susan')
        c = Customer(customer_name='Building')
        r = Report(author=u, 
                   customer=c,
                   summary="No Heat",
                   action = "Turned on Boiler",
                   recommendation = "N/A")
        self.assertEqual(u, r.author)
        self.assertEqual(c, r.customer)


if __name__ == '__main__':
    unittest.main(verbosity=2)
