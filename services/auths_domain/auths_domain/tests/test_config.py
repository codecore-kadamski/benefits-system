import unittest
from flask_testing import TestCase
#  from flask import current_app
from auths_domain import create_app, db


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        return create_app('dev').app

    def setUp(self):
        self.app = self.create_app()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_app_is_development(self):
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue('data.db' in self.app.config['SQLALCHEMY_DATABASE_URI'])


class TestProductionConfig(TestCase):

    def create_app(self):
        return create_app('prod').app

    def setUp(self):
        self.app = self.create_app()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_app_is_prod(self):
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://root:test@localhost:5432/benefits'
        )


class TestTestingConfig(TestCase):

    def create_app(self):
        return create_app('test').app

    def setUp(self):
        self.app = self.create_app()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_app_is_test(self):
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertTrue('data-test.db' in self.app.config['SQLALCHEMY_DATABASE_URI'])


if __name__ == '__main__':
    unittest.main()
