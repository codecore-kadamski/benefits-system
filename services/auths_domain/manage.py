import os
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from auths_domain.core import app, db
from auths_domain import models


MIGRATION_DIR = {
    'dev': os.path.join('auths_domain', 'migrations', 'dev'),
    'test': os.path.join('auths_domain', 'migrations', 'test'),
    'prod': os.path.join('auths_domain', 'migrations', 'prod'),
}

migrate = Migrate(app.app, db, directory=MIGRATION_DIR.get(os.getenv('ENVIRON', 'dev')))

manager = Manager(app.app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def test():
    """Runs the unit tests."""
    #  app = create_app(os.getenv('ENVIRON', 'test'))
    tests = unittest.TestLoader().discover('auths_domain/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
