import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import create_app, db, models

app = create_app()
migrate = Migrate(app.app, db)
manager = Manager(app.app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests/', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
