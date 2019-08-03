import unittest
from flask_testing import TestCase
from api import create_app, db
from api.models import UserModel


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
        user = UserModel(
            email='test@test.com',
            password='test',
            username='test'
        )

        self.db.session.add(user)
        self.db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        #  self.db.table('users').delete()
        user = UserModel(
            email='test2@test.com',
            password='test',
            username='test2'
        )
        self.db.session.add(user)
        self.db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(UserModel.decode_auth_token(auth_token) == 1)


if __name__ == '__main__':
    unittest.main()
