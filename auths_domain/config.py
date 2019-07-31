import os


class Config:
    """Set Flask configuration vars from .env file."""

    POSTGRES = {
        'user': os.environ.get('POSTGRES_USER', 'root'),
        'pw': os.environ.get('POSTGRES_PASSWORD', 'test'),
        'db': os.environ.get('POSTGRES_DB', 'benefits'),
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': '5432',
    }

    # General
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'H*%@B^*5t86exh834')

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
