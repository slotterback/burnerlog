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

    def test_update_username(self):
        name1 = 'Steven'
        name2 = 'April'
        u = User(username=name1)
        self.assertEqual(u.getName(), name1)
        u.setName(name2)
        self.assertEqual(u.getName(), name2)

    def test_update_email(self):
        email1 = 'test@yahoo.com'
        email2 = 'test@gmail.com'
        u = User(username = 'test', email=email1)
        self.assertEqual(u.getEmail(), email1)
        u.setEmail(email2)
        self.assertEqual(u.getEmail(), email2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
