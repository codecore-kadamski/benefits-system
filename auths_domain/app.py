import os

import connexion
from connexion.resolver import RestyResolver
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from injector import Binder
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api.models import BaseModel
from config import config_by_name

db = SQLAlchemy()


def configure(binder: Binder) -> Binder:
    from api.views import UserProvider, AuthProvider
    binder.bind(
        UserProvider,
        AuthProvider
    )
    return binder


def get_engine_session(config):
    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
    session = scoped_session(sessionmaker(bind=engine))
    BaseModel.set_session(session)
    return engine, session


def create_app(config_name):
    app = connexion.FlaskApp(__name__, specification_dir='.')
    app.add_api('swagger.yml', resolver=RestyResolver('api'))
    app.app.config.from_object(config_by_name[config_name])
    CORS(app.app)
    FlaskInjector(app=app.app, modules=[configure])

    db.init_app(app.app)

    with app.app.app_context():
        engine, session = get_engine_session(app.app.config)
        return app


current_app = create_app(os.getenv('ENVIRON', 'prod'))
