import os
from api import create_app

app, db = create_app(os.getenv('ENVIRON', 'prod'))
