# from api.routes import *
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
import connexion
from connexion.resolver import RestyResolver
from .views import UserProvider

from injector import Binder
from flask_cors import CORS
from .config import SETTINGS


db = SQLAlchemy()
app_settings = 'api.config.{}'.format(SETTINGS.get('APP_SETTINGS', 'DevConfig'))


def configure(binder: Binder) -> Binder:
    binder.bind(
        UserProvider
    )
    return binder


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='.')  # Provide the app and the directory of the docs
    app.app.config.from_object(app_settings)
    CORS(app.app)
    app.add_api('api.yml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    db.init_app(app.app)

    with app.app.app_context():
        # Imports
        from . import routes
        from . import models

        # Create tables for our models
        db.create_all()
        return app
