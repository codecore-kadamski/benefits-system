import unittest

from flask_testing import TestCase

from api.models import User
from app import create_app, db


class TestUserModel(TestCase):

    def create_app(self):
        return create_app('test').app

    def setUp(self):
        self.app = self.create_app()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            username='test'
        )
        user.save()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test2@test.com',
            password='test',
            username='test2'
        )
        user.save()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == user.id)


if __name__ == '__main__':
    unittest.main()
