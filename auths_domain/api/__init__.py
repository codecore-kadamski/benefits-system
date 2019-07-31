# from api.routes import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
import connexion
from connexion.resolver import RestyResolver
from .views import UserProvider

from injector import Binder
from flask_cors import CORS


db = SQLAlchemy()


def configure(binder: Binder) -> Binder:
    binder.bind(
        UserProvider
    )
    return binder


def create_app():
    """Construct the core application."""
    #  app = Flask(__name__, instance_relative_config=False)
    app = connexion.FlaskApp(__name__, specification_dir='.')  # Provide the app and the directory of the docs
    db.init_app(app.app)
    app.app.config.from_object('config.Config')
    CORS(app.app)
    app.add_api('api.yml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])

    with app.app.app_context():
        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()
        return app
