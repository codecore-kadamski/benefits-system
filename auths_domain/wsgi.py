from api import app

application = app


if __name__ == '__main__':
    application.run(debug=app.app.config.get('DEBUG', False))
