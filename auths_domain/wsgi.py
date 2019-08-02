

import ipdb; ipdb.set_trace()
from . import app

application = app

if __name__ == '__main__':
    application.run(debug=app.app.config.get('DEBUG', False))  # os.environ is handy if you intend to launch on heroku
