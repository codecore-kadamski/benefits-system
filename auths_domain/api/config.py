import os


basedir = os.path.abspath(os.path.dirname(__file__))
POSTGRES = {
    'user': os.environ.get('POSTGRES_USER', 'root'),
    'pw': os.environ.get('POSTGRES_PASSWORD', 'test'),
    'db': os.environ.get('POSTGRES_DB', 'benefits'),
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    'port': '5432',
}


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'H*%@B^*5t86exh834')
    DEBUG = os.getenv('DEBUG', False)
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


SETTINGS = {
    'DEV': DevConfig,
    'PROD': ProdConfig
}
