import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import app, db


app.app.app_context().push()

migrate = Migrate(app.app, db)
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
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
