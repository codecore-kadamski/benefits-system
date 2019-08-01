import os
from api import create_app

app = application = create_app()


if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', False))
