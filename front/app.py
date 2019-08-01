import os
import connexion
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver
from api.views import UserProvider

from injector import Binder
from flask_cors import CORS


db = SQLAlchemy()
POSTGRES = {
    'user': os.environ.get('POSTGRES_USER'),
    'pw': os.environ.get('POSTGRES_PASSWORD'),
    'db': os.environ.get('POSTGRES_DB'),
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    'port': '5432',
}


def configure(binder: Binder) -> Binder:
    binder.bind(
        UserProvider
    )
    return binder


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, specification_dir='.')  # Provide the app and the directory of the docs
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    db.init_app(app.app)
    #  db.create_all()
    CORS(app.app)
    app.add_api('api.yml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    app.run(port=int(os.environ.get('PORT', 5000)), debug=True)  # os.environ is handy if you intend to launch on heroku
