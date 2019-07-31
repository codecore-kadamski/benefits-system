import os
from api import create_app

application = create_app()


if __name__ == '__main__':
    application.run(debug=True)  # os.environ is handy if you intend to launch on heroku
