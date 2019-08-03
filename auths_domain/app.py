import os
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector

import connexion
from connexion.resolver import RestyResolver
from api.views import UserProvider, AuthProvider

from config import config_by_name
from injector import Binder
from flask_cors import CORS


db = SQLAlchemy()


def configure(binder: Binder) -> Binder:
    binder.bind(
        UserProvider,
        AuthProvider
    )
    return binder


def create_app(config_name):
    app = connexion.FlaskApp(__name__, specification_dir='.')
    app.add_api('swagger.yml', resolver=RestyResolver('api'))
    app.app.config.from_object(config_by_name[config_name])
    CORS(app.app)
    FlaskInjector(app=app.app, modules=[configure])

    db.init_app(app.app)
    return app

    # with app.app.app_context():
    #     from api import routes
    #     #from api import models
    #     db.create_all()
    #     return app

# print(os.getenv('ENVIRON', 'prod'))
current_app = create_app(os.getenv('ENVIRON', 'prod'))
