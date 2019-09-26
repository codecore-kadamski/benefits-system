# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_injector import FlaskInjector
# from flask_migrate import Migrate

# import connexion
# from connexion.resolver import RestyResolver
# from auths_domain.views import UserProvider

# from config import config_by_name
# from injector import Binder
# from flask_cors import CORS


# db = SQLAlchemy()
# migration = Migrate()


# def configure(binder: Binder) -> Binder:
#     binder.bind(
#         UserProvider
#     )
#     return binder


# def create_app(config_name) -> Flask:
#     app = connexion.FlaskApp(__name__, specification_dir='./../')
#     app.add_api('swagger.yml', resolver=RestyResolver('api'))
#     app.app.config.from_object(config_by_name[config_name])
#     CORS(app.app)
#     FlaskInjector(app=app.app, modules=[configure])

#     db.init_app(app.app)
#     migration.init_app(app.app, db)

#     with app.app.app_context() as cont:
#         # from . import routes
#         from auths_domain import models
#         # db.create_all()
#         cont.push()
#         return app


# app = create_app(os.getenv('ENVIRON', 'dev'))
