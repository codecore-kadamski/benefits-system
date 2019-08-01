from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector

import connexion
from connexion.resolver import RestyResolver
from .views import UserProvider

from config import config_by_name
from injector import Binder
from flask_cors import CORS


db = SQLAlchemy()


def configure(binder: Binder) -> Binder:
    binder.bind(
        UserProvider
    )
    return binder


def create_app(config_name):
    app = connexion.FlaskApp(__name__, specification_dir='../')
    app.add_api('swagger.yml', resolver=RestyResolver('api'))

    app.app.config.from_object(config_by_name[config_name])

    db.init_app(app.app)
    #  db.create_all()

    CORS(app.app)
    FlaskInjector(app=app.app, modules=[configure])

    with app.app.app_context():

        from . import routes
        from . import models

        # Create tables for our models
        db.create_all()
        return app
