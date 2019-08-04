import os
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector

import connexion
from connexion.resolver import RestyResolver
from api.models import BaseModel

from config import config_by_name
from injector import Binder
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


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
    # # Base.metadata.drop_all(engine)
    # # Base.metadata.create_all(engine)
    return engine, session


def create_app(config_name):
    app = connexion.FlaskApp(__name__, specification_dir='.')
    app.add_api('swagger.yml', resolver=RestyResolver('api'))
    app.app.config.from_object(config_by_name[config_name])
    CORS(app.app)
    FlaskInjector(app=app.app, modules=[configure])

    db.init_app(app.app)
    # return app

    with app.app.app_context():
        engine, session = get_engine_session(app.app.config)
        from api import routes
        from api import models
        return app

# print(os.getenv('ENVIRON', 'prod'))
current_app = create_app(os.getenv('ENVIRON', 'prod'))
