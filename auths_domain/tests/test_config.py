import flask_testing
import unittest
from flask import Flask
from flask_testing import TestCase


#from flask import current_app
#from api import create_app
from api.config import POSTGRES

#  app = create_app()


# def create_app(self):
#         app.config.from_object('api.config.DevConfig')
#         return app


class TestDevConfig(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDevConfig, self).__init__(*args, **kwargs)

    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookie=True)

    def tearDown(self):
        self.app_context.pop()

    def test_costam(self):
        import ipdb; ipdb.set_trace()
    # def test_app_is_development(self):
    #     self.assertTrue(app.config['DEBUG'] is True)
    #     self.assertFalse(current_app is None)
    #     import ipdb; ipdb.set_trace()
    #     self.assertTrue(
    #         app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    #     )


if __name__ == '__main__':
    unittest.main()
