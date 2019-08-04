import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker


basedir = os.path.abspath(os.path.dirname(__file__))
POSTGRES = {
    'user': os.environ.get('POSTGRES_USER', 'root'),
    'pw': os.environ.get('POSTGRES_PASSWORD', 'test'),
    'db': os.environ.get('POSTGRES_DB', 'benefits'),
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    'port': '5432',
}


class Config(object):
    """Set Flask configuration vars from .env file."""

    # General
    DEBUG = os.environ.get('DEBUG', False)
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'H*%@B^*5t86exh834')

    # Database
    #  SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{basedir}/data.db'.format(basedir=basedir)
    #  SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    APIKEYINFO_FUNC = None


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    #  SQLALCHEMY_DATABASE_URI = 'sqlite:///data-test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{basedir}/data-test.db'.format(basedir=basedir)
    TESTING = True


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
