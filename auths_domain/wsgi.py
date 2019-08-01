import os
#  from api import create_app
#  app = application = create_app(os.getenv('ENVIRON', 'dev'))
from api import app

application = app


if __name__ == '__main__':
    application.run(debug=app.app.config.get('DEBUG', False))  # os.environ is handy if you intend to launch on heroku
